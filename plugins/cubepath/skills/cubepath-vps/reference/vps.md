# cubecli vps

Manage VPS instances

## `cubecli vps backup configure`

Configure backup settings for a VPS

Usage: `cubecli vps backup configure <vps_id> [flags]`

- `--disable`: Disable automatic backups
- `--enable`: Enable automatic backups
- `--hour int`: Schedule hour for backups (0-23) (default 3)
- `--max int`: Maximum number of backups to keep (default 3)
- `--retention int`: Retention period in days (default 7)

## `cubecli vps backup create`

Create a backup for a VPS

Usage: `cubecli vps backup create <vps_id> [flags]`

- `-n, --notes string`: Notes for the backup

## `cubecli vps backup delete`

Delete a VPS backup

Usage: `cubecli vps backup delete <vps_id> <backup_id> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli vps backup list`

List backups for a VPS

Usage: `cubecli vps backup list <vps_id>`

## `cubecli vps backup restore`

Restore a VPS from a backup

Usage: `cubecli vps backup restore <vps_id> <backup_id> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli vps backup settings`

Show backup settings for a VPS

Usage: `cubecli vps backup settings <vps_id>`

## `cubecli vps change-password`

Change VPS root password

Usage: `cubecli vps change-password <vps_id> [flags]`

- `-p, --new-password string`: New root password (required)

## `cubecli vps create`

Create a new VPS instance

Usage: `cubecli vps create [flags]`

- `--availability-group string`: UUID of the availability group to place the VPS in
- `--backups`: Enable backups
- `--firewall intSlice`: Firewall group IDs (repeatable)
- `--ipv4`: Enable IPv4 (default true)
- `--ipv6`: Enable public IPv6 (default true)
- `--label string`: VPS label
- `--network int`: Network ID
- `--no-backups`: Disable backups
- `--no-ipv4`: Disable IPv4
- `--no-ipv6`: Disable public IPv6 (requires --network)
- `--password string`: Root password
- `--project int`: Project ID (required)
- `-c, --cloudinit string`: Cloud-init configuration or file path
- `-l, --location string`: Location name (required)
- `-n, --name string`: VPS name (required)
- `-p, --plan string`: Plan name (required)
- `-s, --ssh intSlice`: SSH key IDs (repeatable)
- `-t, --template string`: Template name (required)

## `cubecli vps destroy`

Destroy a VPS instance

Usage: `cubecli vps destroy <vps_id> [flags]`

- `--keep-ips`: Keep floating IPs
- `--release-ips`: Release floating IPs
- `-f, --force`: Skip confirmation

## `cubecli vps iso list`

List available ISOs for a VPS

Usage: `cubecli vps iso list <vps_id>`

## `cubecli vps iso mount`

Mount an ISO to a VPS

Usage: `cubecli vps iso mount <vps_id> <iso_id>`

## `cubecli vps iso unmount`

Unmount the ISO from a VPS

Usage: `cubecli vps iso unmount <vps_id>`

## `cubecli vps list`

List VPS instances

Usage: `cubecli vps list [flags]`

- `-l, --location string`: Filter by location
- `-p, --project int`: Filter by project ID

## `cubecli vps plan list`

List available VPS plans

Usage: `cubecli vps plan list`

## `cubecli vps power reset`

Reset a VPS instance

Usage: `cubecli vps power reset <vps_id>`

## `cubecli vps power restart`

Restart a VPS instance

Usage: `cubecli vps power restart <vps_id>`

## `cubecli vps power start`

Start a VPS instance

Usage: `cubecli vps power start <vps_id>`

## `cubecli vps power stop`

Stop a VPS instance

Usage: `cubecli vps power stop <vps_id>`

## `cubecli vps reinstall`

Reinstall a VPS with a new template

Usage: `cubecli vps reinstall <vps_id> [flags]`

- `-f, --force`: Skip confirmation
- `-t, --template string`: Template name (required)

## `cubecli vps resize`

Resize a VPS instance

Usage: `cubecli vps resize <vps_id> [flags]`

- `-f, --force`: Skip confirmation
- `-p, --plan string`: New plan name (required)

## `cubecli vps show`

Show VPS details

Usage: `cubecli vps show <vps_id>`

## `cubecli vps template list`

List available VPS templates

Usage: `cubecli vps template list`

## `cubecli vps update`

Update a VPS instance

Usage: `cubecli vps update <vps_id> [flags]`

- `--label string`: New label
- `-n, --name string`: New name
