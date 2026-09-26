# cubecli profile

Manage authentication profiles

## `cubecli profile add`

Add a new profile and log it in (browser login, or --token)

Usage: `cubecli profile add <name> [flags]`

- `--api-url string`: Override API URL for this profile
- `--no-browser`: Print the login URL instead of opening a browser
- `--token`: Store an API token instead of logging in with the browser
- `-f, --force`: Replace profile without confirmation if it already exists

## `cubecli profile current`

Show the active profile

Usage: `cubecli profile current`

## `cubecli profile delete`

Delete a profile

Usage: `cubecli profile delete <name> [flags]`

Aliases: rm

- `-f, --force`: Skip confirmation prompt

## `cubecli profile list`

List configured profiles

Usage: `cubecli profile list`

Aliases: ls

## `cubecli profile rename`

Rename a profile

Usage: `cubecli profile rename <old> <new>`

## `cubecli profile use`

Switch the active profile

Usage: `cubecli profile use <name>`
