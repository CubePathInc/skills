# cubecli baremetal

Manage baremetal servers

## `cubecli baremetal deploy`

Deploy a new baremetal server

Usage: `cubecli baremetal deploy [flags]`

- `--disk-layout string`: Disk layout name
- `--hostname string`: Hostname for the server (required)
- `--label string`: Optional label
- `--os string`: OS name
- `--password string`: Password for the server (required)
- `-l, --location string`: Location name (required)
- `-m, --model string`: Model name (required)
- `-p, --project int`: Project ID (required)
- `-s, --ssh intSlice`: SSH key IDs
- `-u, --user string`: Username (default root)

## `cubecli baremetal ipmi`

Create an IPMI proxy session

Usage: `cubecli baremetal ipmi <id>`

## `cubecli baremetal kvm`

Show the KVM console URL and credentials of a server

Usage: `cubecli baremetal kvm <id>`

## `cubecli baremetal list`

List baremetal servers

Usage: `cubecli baremetal list [flags]`

- `-l, --location string`: Filter by location
- `-p, --project int`: Filter by project ID

## `cubecli baremetal model list`

List available baremetal models

Usage: `cubecli baremetal model list [flags]`

- `--in-stock`: Show only in-stock models
- `--out-of-stock`: Show only out-of-stock models

## `cubecli baremetal monitoring disable`

Disable monitoring for a baremetal server

Usage: `cubecli baremetal monitoring disable <id>`

## `cubecli baremetal monitoring enable`

Enable monitoring for a baremetal server

Usage: `cubecli baremetal monitoring enable <id>`

## `cubecli baremetal monitoring status`

Show monitoring status for a baremetal server

Usage: `cubecli baremetal monitoring status <id>`

## `cubecli baremetal move-project`

Move a baremetal server to another project in the same organization

Usage: `cubecli baremetal move-project <id> [flags]`

Aliases: move

- `-p, --project int`: Target project ID (required)

## `cubecli baremetal network attach`

Attach a server to a private network in its location

Attach a baremetal server to a private network. An address is picked
automatically; restart the server to apply the change.

Usage: `cubecli baremetal network attach <id> [flags]`

- `--network int`: Private network ID (required)

## `cubecli baremetal network detach`

Detach a server from its private network

Usage: `cubecli baremetal network detach <id> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli baremetal os`

List the operating systems and disk layouts a server can be installed with

Usage: `cubecli baremetal os <id>`

## `cubecli baremetal power restart`

Restart a baremetal server

Usage: `cubecli baremetal power restart <id>`

## `cubecli baremetal power start`

Power on a baremetal server

Usage: `cubecli baremetal power start <id>`

## `cubecli baremetal power stop`

Power off a baremetal server

Usage: `cubecli baremetal power stop <id>`

## `cubecli baremetal protection`

Enable or disable destruction protection

Usage: `cubecli baremetal protection <id> [flags]`

- `--disable`: Disable destruction protection
- `--enable`: Enable destruction protection

## `cubecli baremetal reinstall cancel`

Cancel a pending or running reinstallation

Usage: `cubecli baremetal reinstall cancel <id> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli baremetal reinstall start`

Start a baremetal server reinstallation

Usage: `cubecli baremetal reinstall start <id> [flags]`

- `--disk-layout string`: Disk layout name
- `--hostname string`: Hostname for the server (required)
- `--os string`: OS name to install (required)
- `--password string`: Password for the server (required)
- `-f, --force`: Skip confirmation prompt
- `-u, --user string`: Username (default root)

## `cubecli baremetal reinstall status`

Check reinstallation status

Show whether an OS reinstallation is running: the server status is deploying while it runs.

Usage: `cubecli baremetal reinstall status <id>`

## `cubecli baremetal rescue`

Boot baremetal server into rescue mode

Usage: `cubecli baremetal rescue <id>`

## `cubecli baremetal reset-bmc`

Reset the BMC of a baremetal server

Usage: `cubecli baremetal reset-bmc <id> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli baremetal sensors`

Show BMC sensor data for a baremetal server

Usage: `cubecli baremetal sensors <id>`

## `cubecli baremetal show`

Show baremetal server details

Usage: `cubecli baremetal show <id>`

## `cubecli baremetal ssh-key add`

Add SSH keys to a server (used by the next install)

Usage: `cubecli baremetal ssh-key add <id> <ssh_key_id>...`

## `cubecli baremetal ssh-key remove`

Remove an SSH key from a server

Usage: `cubecli baremetal ssh-key remove <id> <ssh_key_id>`

## `cubecli baremetal update`

Update a baremetal server

Usage: `cubecli baremetal update <id> [flags]`

- `--hostname string`: New hostname
- `--tags string`: Tags for the server
