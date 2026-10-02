# cubecli project

Manage projects

## `cubecli project create`

Create a new project

Usage: `cubecli project create [flags]`

- `-d, --description string`: Description of the project
- `-n, --name string`: Name of the project (required)

## `cubecli project delete`

Delete a project

Usage: `cubecli project delete <project_id> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli project list`

List projects

Usage: `cubecli project list`

## `cubecli project show`

Show project details

Usage: `cubecli project show <project_id>`

## `cubecli project update`

Rename a project

Usage: `cubecli project update <project_id> [flags]`

- `-n, --name string`: New name (2-50 characters) (required)
