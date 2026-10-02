# cubecli availability-group

Manage VPS availability groups

## `cubecli availability-group add-vps`

Add a VPS to an availability group

Usage: `cubecli availability-group add-vps <group_uuid> <vps_id>`

## `cubecli availability-group create`

Create a new availability group

Usage: `cubecli availability-group create [flags]`

- `--description string`: Optional description
- `--strategy string`: Placement strategy (spread or cluster)
- `-l, --location string`: Location name (required)
- `-n, --name string`: Group name (required)
- `-p, --project int`: Project ID (required)

## `cubecli availability-group delete`

Delete an availability group

Usage: `cubecli availability-group delete <group_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli availability-group list`

List availability groups for a project

Usage: `cubecli availability-group list <project_id> [flags]`

- `-l, --location string`: Filter by location

## `cubecli availability-group move-project`

Move a availability group to another project in the same organization

Usage: `cubecli availability-group move-project <group_uuid> [flags]`

Aliases: move

- `-p, --project int`: Target project ID (required)

## `cubecli availability-group remove-vps`

Remove a VPS from an availability group

Usage: `cubecli availability-group remove-vps <group_uuid> <vps_id> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli availability-group show`

Show availability group details

Usage: `cubecli availability-group show <group_uuid>`
