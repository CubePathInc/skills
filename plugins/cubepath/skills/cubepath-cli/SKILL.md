---
name: cubepath-cli
description: Use cubecli, the CubePath Cloud command-line tool, to inspect and manage CubePath infrastructure. Covers installation, login and profiles (one per organization), JSON output, finding project/location/plan/SSH key IDs, confirmations for destructive actions and common API errors. Load it whenever the user mentions CubePath, cubecli or api.cubepath.com, before using any other cubepath-* skill.
---

# cubecli basics

`cubecli` is the official CLI for CubePath Cloud (VPS, baremetal, private networks,
NAT gateways, floating IPs, load balancers, DNS, CDN, Kubernetes, Object Storage).
Every other `cubepath-*` skill builds on the rules here.

The exact commands and flags are in [reference/](reference/commands.md), generated
from cubecli itself. Check them there or with `cubecli <group> <command> --help`
instead of guessing a flag.

## 1. Check the CLI and the session

```bash
cubecli version
cubecli auth status --json
```

- **Not installed**: tell the user and offer the install command. Do not run it
  without their OK:
  `curl -fsSL https://raw.githubusercontent.com/CubePathInc/cubecli/main/install.sh | sh`
- **No profile, or "logged out"**: ask the user to run `cubecli login` themselves
  in their terminal. It asks for an API token (created at
  https://my.cubepath.com/organization/tokens) or opens a browser, so it cannot
  be completed by you.
- **`env_token: true`**: `CUBE_API_TOKEN` is set and overrides every profile.

Never ask for, print, copy or store API tokens or OAuth tokens. Never read or edit
`~/.cubecli/config.json`. If credentials are missing, the user logs in.

## 2. Profiles and organizations

A profile holds the session of one organization. Before changing anything,
confirm you are in the right one:

```bash
cubecli auth status              # * marks the active profile
cubecli --profile work vps list  # one command against another profile
```

If the user names a company, brand or account, pick the matching profile with
`--profile` on every command rather than switching the active one with
`cubecli profile use`, which would affect their other terminals.

`Access: read-only` means the session can list but not create or change
resources. Ask the user to log in again with `cubecli login <profile>` and grant
write access. `Access: unusable` means the profile must be logged in again with
`cubecli login <profile> --token`.

## 3. Always use `--json`

Tables are for humans and truncate. Pass `--json` and parse the result
(for example with `jq`):

```bash
cubecli project list --json | jq '.[].project | {id, name}'
```

The JSON is the raw API response, and its shape varies by command. Inspect it
first (`jq 'keys'` or `jq '.[0]'`) before writing a filter. Some list filters
(such as `vps list --project`) only apply to the table output. Filter the JSON
yourself.

## 4. Resolve IDs before creating anything

Create commands take IDs and exact names. Look them up and never invent them:

| Needed | Command | Where in the JSON |
|---|---|---|
| Project ID (`--project`) | `cubecli project list --json` | `.[].project.id` (each entry also lists its `vps`, `baremetals`, `networks`) |
| Location name (`--location`) | `cubecli location list --json` | `.vps.locations[].location_name`, e.g. `eu-bcn-1`, `us-hou-1`, `us-mia-1` (also `.baremetal`, `.loadbalancer`, `.cdn`) |
| SSH key IDs (`--ssh`) | `cubecli ssh-key list --json` | `.sshkeys[] \| {id, name}` |
| VPS plan (`--plan`) | `cubecli vps plan list --json` | `.locations[].clusters[].plans[]`: `plan_name`, `cpu`, `ram` (MB), `storage` (GB), `price_per_hour`, `status` (2 in stock, 1 out of stock) |
| VPS template (`--template`) | `cubecli vps template list --json` | `.operating_systems[].template_name`, e.g. `debian-12`, `ubuntu-24` |

Plans are per location: check the plan is in stock **in the chosen location**.

If there are several projects and the user did not say which, ask. If none
exists, propose `cubecli project create --name <name>`.

## 5. Destructive and billable actions

Before running any command that deletes data, interrupts service or costs money,
show the user exactly what will happen (resource name, ID, plan and monthly
price when known) and wait for an explicit yes:

- `destroy`, `delete`, `release`, `reinstall`, `restore`, `remove-node`,
  `power stop|reset`, `reset-bmc`, `unassign`
- `create`, `deploy`, `acquire`, `resize`, `add-nodes` (billable)

Commands that delete ask for confirmation on stdin, which you cannot answer.
After the user confirms in the conversation, add `--force` (or `-f`). Never add
it before they confirm, and never loop over resources deleting them in bulk
without listing them first.

## 6. Asynchronous operations

Creating or changing servers, clusters and gateways returns immediately with a
status such as `deploying`. The work continues in the background. Poll the
`show` command every 15 to 30 seconds until the status settles (`active`, or
`failed`) rather than assuming it is ready:

```bash
cubecli vps show <vps_id> --json | jq -r '.status'
```

Operations on a resource that is still deploying, resizing or has a task pending
are rejected (HTTP 409 or 400). Wait and retry.

## 7. Errors

cubecli prints the API's `detail` message. Common ones:

| Message | What to do |
|---|---|
| `Account not verified` | The organization needs a payment method. The user adds it in the dashboard. |
| `Insufficient balance...` (402) | The organization must top up its balance. |
| `... limit reached. Your {tier} tier allows...` (403) | Tier quota. The user must remove resources or ask support for more. |
| `Plan '...' is currently out of stock` | Suggest another plan or location from the plan list. |
| `session ... expired or was revoked` | The user runs `cubecli login <profile>`. |
| 403 on a write | Read-only session or the member lacks the permission in that organization. |
| 429 | Rate limited. Wait before retrying and do not retry in a tight loop. |

## Other tools

- **MCP server**: the CubePath MCP server (`https://mcp.cubepath.com/mcp`)
  exposes the same operations as tools, for agents without a shell. If the user
  wants it, `cubecli mcp install` adds it to their agents; they then approve
  the access in the browser.
- **Terraform**: for infrastructure the user wants versioned as code, see the
  `cubepath-terraform` skill.
