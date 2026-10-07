---
name: cubepath-vps
description: Create, inspect, resize, reinstall, back up, power-manage and destroy CubePath VPS and baremetal servers with cubecli, including choosing location, plan and OS template, SSH keys, cloud-init, availability groups and VPS snapshots (convert a backup and deploy copies in any location). Use when the user wants a server, VM, VPS or dedicated/baremetal machine on CubePath, or asks about one they already have.
---

# CubePath VPS and baremetal

Follow the `cubepath-cli` skill first (session, profile, `--json`, confirmations).
Exact flags: [reference/vps.md](reference/vps.md),
[reference/snapshot.md](reference/snapshot.md),
[reference/availability-group.md](reference/availability-group.md),
[reference/baremetal.md](reference/baremetal.md).

## Create a VPS

1. **Resolve inputs** (see the ID table in `cubepath-cli`):
   - project ID, location, SSH key IDs;
   - plan: in stock (`status` 2) in that location. Families: `gp.*` general
     purpose, `rz.*` high frequency, `dc.*` dedicated CPU, `hd.*` high frequency
     dedicated CPU. The cheapest usable one is usually `gp.nano`;
   - template: an `operating_systems[].template_name`. Prefer the latest Debian or
     Ubuntu LTS unless the user asks otherwise.
2. **Access**: at least one SSH key (`--ssh`, repeatable) or a `--password`.
   Prefer SSH keys. If the user has none uploaded, offer to upload their public
   key (`cubecli ssh-key create --name <n> --public-key-from-file ~/.ssh/id_ed25519.pub`).
   Never generate or choose a password for them silently; if one is needed, ask.
3. **Confirm** name, location, plan (CPU/RAM/disk and `price_per_hour`),
   template and project with the user.
4. **Create** and keep the `vps_id` from the response:

```bash
cubecli vps create --json \
  --name web-01 --project 882 --location eu-bcn-1 \
  --plan gp.nano --template debian-12 --ssh 64
# -> {"detail": "VPS created", "vps_id": 123, "status": "deploying",
#     "ipv4_address": "...", "ipv6_address": "..."}
```

5. **Wait** until `cubecli vps show <vps_id> --json | jq -r .status` is `active`
   (usually under a minute or two), then give the user the IPs and the SSH
   command (`ssh root@<ipv4>`).

Rules the API enforces:

- `--name` must be a valid hostname: letters, digits and hyphens, no spaces or
  underscores. Use `--label` for a free-text description.
- `--no-ipv6` requires `--network <private network id>`.
- Templates have a minimum RAM; a too-small plan is rejected with a message
  naming the minimum.
- Windows templates ignore SSH keys and cloud-init; the user is `Administrator`.

### Cloud-init

`-c/--cloudinit` takes inline YAML or a file path (Linux only, max 64 KB). It
must start with `#cloud-config` and only a whitelist of directives is accepted
(`packages`, `runcmd`, `bootcmd`, `write_files`, ...). If it is rejected, the
error names the reason; adjust rather than retrying blindly.

```yaml
#cloud-config
packages: [nginx]
runcmd:
  - systemctl enable --now nginx
```

## Inspect

```bash
cubecli vps list --json                 # every project with its .vps[] array
cubecli vps show <vps_id> --json        # one VPS
```

Useful fields of a VPS: `status`, `plan.plan_name`, `location.location_name`,
`template.template_name`, `floating_ips.list[]` (`address`, `type`, `is_primary`),
`network`, `protected`, `backup_enabled`.

To find a VPS by name:
`cubecli vps list --json | jq '[.[].vps[]] | map(select(.name=="web-01"))'`.

## Change an existing VPS

| Goal | Command | Notes |
|---|---|---|
| Rename / relabel | `cubecli vps update <id> --name <n> --label <l>` | |
| Bigger plan | `cubecli vps resize <id> --plan <plan> --force` | billable; confirm first; expect 5 to 10 minutes of downtime |
| New OS (wipes disk) | `cubecli vps reinstall <id> --template <t> --force` | destroys all data; confirm explicitly |
| Power | `cubecli vps power restart <id>` (also `start`, `stop`, `reset`) | `stop` and `reset` are abrupt; prefer `restart` |
| Root password | `cubecli vps change-password <id> --new-password <p>` | ask the user for the password |
| Mount an ISO | `cubecli vps iso list <id>`, `cubecli vps iso mount <id> <iso_id>` | |

Only one operation at a time: while a task is running, others return 409.
Wait for `status` to return to `active`.

## Backups

```bash
cubecli vps backup settings <id> --json
cubecli vps backup configure <id> --enable --hour 3 --retention 7 --max 3
cubecli vps backup create <id> --notes "before upgrade"
cubecli vps backup list <id> --json
cubecli vps backup restore <id> <backup_id> --force   # overwrites the disk, confirm first
```

Suggest a manual backup before a reinstall, resize or risky change.

## Snapshots

A snapshot is a permanent copy of a VPS disk, made from one of its completed
backups. Unlike a backup it does not expire and is not deleted when the source
VPS is destroyed. It can be deployed as new VPS in **any location**, not only
where the source lives.

**Cost and quota.** Billed at 0.03 USD per GB of the source VPS disk per month,
until it is deleted (read the live price from `cubecli snapshot quota --json`,
`price_gb_month`). Each organization has a limit on the number of snapshots and
on their total GB; `cubecli snapshot quota --json` returns `count`,
`count_max`, `gb` and `gb_max`; a new conversion needs room left in both.
Snapshots being converted or deleted count towards the quota.

### Convert a backup

1. Pick a backup with `status` completed:
   `cubecli vps backup list <vps_id> --json` (a backup already converted shows
   its `snapshot_uuid`).
2. Check the quota and tell the user the monthly cost (disk GB x price).
   Confirm before creating: it is billable.
3. Create it and follow the conversion (a few minutes):

```bash
cubecli snapshot create --vps <vps_id> --backup <backup_id> --name web-01-base \
  --description "nginx + app, before go-live"
cubecli snapshot get <snapshot_uuid> --json   # wait for status available
```

Statuses: `pending`, `converting`, `available`, `failed`, `deleting`. Only
`available` snapshots can be deployed. A backup that is being restored or
deleted, or whose VPS is being reinstalled, migrated or destroyed, can not be
converted at that moment (409); retry once that task finishes.

### Deploy from a snapshot

```bash
cubecli snapshot list --status available --json
cubecli snapshot get <snapshot_uuid> --json   # disk_gb and deploy_estimates per location
cubecli vps create --json --name web-02 --project 882 --location us-mia-1 \
  --plan gp.small --snapshot <snapshot_uuid> --ssh 64
```

- `--snapshot` replaces `--template`; never pass both. `--cloudinit` is not
  allowed with a snapshot.
- The plan disk must be at least the snapshot `disk_gb`; Windows RAM minimums
  still apply.
- `deploy_estimates[]` gives the expected minutes per location; deploying far
  from where the snapshot is stored (`remote: true`) takes longer. Tell the user.
- At most **3 servers can deploy from the same snapshot at the same time**;
  a fourth gets 409. To make more copies, wait until one is `active`.
- After the deploy, `cubecli vps show <vps_id> --json` has
  `source_snapshot_uuid` and `deploy_health`. `degraded` means the server is
  running but its network was not confirmed from inside the guest: suggest the
  user checks it through the console.

Warn the user before deploying:

- **Linux**: only hostname, user, password and SSH keys are applied, and the
  machine-id is regenerated. If the image does not use cloud-init, the server
  starts with the network and credentials of the source server.
- **Windows**: the copy keeps the same SID as the source (run sysprep before
  joining several copies to a domain). The license is the customer's: Windows
  may ask to activate it again, especially in another location, and deploying
  several copies with one license may break its terms. If the QEMU guest agent
  was removed from the source, the copy starts with the network and
  Administrator password of the source.

### Manage and delete

```bash
cubecli snapshot list --vps <vps_id> --json
cubecli snapshot update <snapshot_uuid> --name <n> --description <d>
cubecli snapshot move-project <snapshot_uuid> --project <project_id>
cubecli snapshot delete <snapshot_uuid> --force   # permanent, confirm first
```

Deleting stops the billing and does not affect servers already deployed from
it. It is refused while the snapshot is converting or while a deploy uses it.

## Destroy

1. Show the VPS (name, IPs, project) and ask for explicit confirmation.
2. Ask whether to keep its IPs as floating IPs (`--keep-ips`) or release them
   (`--release-ips`).
3. `cubecli vps destroy <id> --release-ips --force`.

Protected VPS (`protected: true`) cannot be destroyed until protection is turned
off in the dashboard. Tell the user rather than working around it. A VPS that is
deploying or resizing cannot be destroyed until the operation finishes.

## Availability groups

Place VPS on different hosts (`spread`) or together (`cluster`):

```bash
cubecli availability-group create --name web --project 882 --location eu-bcn-1 --strategy spread
cubecli vps create ... --availability-group <group_uuid>
cubecli availability-group add-vps <group_uuid> <vps_id>
```

The group and its VPS must be in the same location. Use `spread` for
redundant servers behind a load balancer.

## Baremetal

Dedicated servers take longer to deploy and are billed per cycle (monthly or longer). Always confirm
the model and price first.

```bash
cubecli baremetal model list --in-stock --json
cubecli baremetal deploy --model <m> --location <l> --project <id> \
  --hostname <h> --os <os> --password <p> --ssh <key_id>
cubecli baremetal show <id> --json
cubecli baremetal reinstall status <id>
```

`baremetal rescue`, `reset-bmc` and `reinstall start` interrupt the server;
confirm first. `cubecli baremetal ipmi <id>` opens a remote console session for the user.
