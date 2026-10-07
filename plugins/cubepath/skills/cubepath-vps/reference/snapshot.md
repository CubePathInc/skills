# cubecli snapshot

Manage VPS snapshots

## `cubecli snapshot create`

Take a snapshot of a VPS now, or convert one of its backups

Take a snapshot of a VPS now, or convert one of its completed backups.

Without --backup the snapshot is taken now, with the server running: it copies
the current disk of the VPS and backups do not need to be enabled. Pause the
writes of a database first if you need it consistent.

With --backup it converts that completed backup instead (find the ID with
"cubecli vps backup list <vps_id>").

The snapshot is billed per GB of the VPS disk per month until you delete it.
It is queued and takes a few minutes: follow it with
"cubecli snapshot get <uuid>" until its status is available.

Usage: `cubecli snapshot create [flags]`

- `--backup int`: Convert this completed backup of the VPS instead of taking the snapshot now
- `--vps int`: Source VPS ID (required)
- `-d, --description string`: Snapshot description (up to 500 characters)
- `-n, --name string`: Snapshot name (up to 100 characters) (required)

Examples:

```
  cubecli snapshot create --vps 20467 --name web-01-golden
  cubecli snapshot create --vps 20467 --backup 991 --name web-01-before-upgrade
```

## `cubecli snapshot delete`

Delete a snapshot permanently and stop its billing

Delete a snapshot permanently and stop its billing.

Servers already deployed from the snapshot are not affected. A snapshot can not
be deleted while it is being created or while a deployment is using it.

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
