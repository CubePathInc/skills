# cubecli snapshot

Manage VPS snapshots

## `cubecli snapshot create`

Convert a completed backup of a VPS into a snapshot

Convert a completed backup of a VPS into a snapshot.

The snapshot is billed per GB of the VPS disk per month until you delete it.
The conversion is queued and takes a few minutes: follow it with
"cubecli snapshot get <uuid>" until its status is available.

Find the backup ID with "cubecli vps backup list <vps_id>".

Usage: `cubecli snapshot create [flags]`

- `--backup int`: Backup ID of that VPS (must be completed) (required)
- `--vps int`: Source VPS ID (required)
- `-d, --description string`: Snapshot description (up to 500 characters)
- `-n, --name string`: Snapshot name (up to 100 characters) (required)

## `cubecli snapshot delete`

Delete a snapshot permanently and stop its billing

Delete a snapshot permanently and stop its billing.

Servers already deployed from the snapshot are not affected. A snapshot can not
be deleted while it is being converted or while a deployment is using it.

Usage: `cubecli snapshot delete <snapshot_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli snapshot get`

Show snapshot details and deploy time estimates

Usage: `cubecli snapshot get <snapshot_uuid>`

Aliases: show

## `cubecli snapshot list`

List the snapshots of the organization

Usage: `cubecli snapshot list [flags]`

- `--limit int`: Maximum number of snapshots (1-100) (default 50)
- `--offset int`: Number of snapshots to skip
- `--status string`: Filter by status (pending, converting, available, failed, deleting)
- `--vps int`: Filter by source VPS ID
- `-l, --location string`: Filter by location name
- `-p, --project int`: Filter by project ID

## `cubecli snapshot move-project`

Move a snapshot to another project in the same organization

Usage: `cubecli snapshot move-project <snapshot_uuid> [flags]`

Aliases: move

- `-p, --project int`: Target project ID (required)

## `cubecli snapshot quota`

Show the snapshot limits, usage and price of the organization

Usage: `cubecli snapshot quota`

## `cubecli snapshot rename`

Rename a snapshot

Usage: `cubecli snapshot rename <snapshot_uuid> <new_name>`

## `cubecli snapshot update`

Rename a snapshot, change its description or move it to another project

Usage: `cubecli snapshot update <snapshot_uuid> [flags]`

- `-d, --description string`: New description ("" clears it)
- `-n, --name string`: New name
- `-p, --project int`: Move to this project ID
