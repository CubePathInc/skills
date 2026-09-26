---
name: cubepath-vps
description: Create, inspect, resize, reinstall, back up, power-manage and destroy CubePath VPS and baremetal servers with cubecli, including choosing location, plan and OS template, SSH keys, cloud-init and availability groups. Use when the user wants a server, VM, VPS or dedicated/baremetal machine on CubePath, or asks about one they already have.
---

# CubePath VPS and baremetal

Follow the `cubepath-cli` skill first (session, profile, `--json`, confirmations).
Exact flags: [reference/vps.md](reference/vps.md),
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
