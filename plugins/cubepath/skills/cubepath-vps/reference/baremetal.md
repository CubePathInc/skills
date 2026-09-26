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

## `cubecli baremetal power restart`

Restart a baremetal server

Usage: `cubecli baremetal power restart <id>`

## `cubecli baremetal power start`

Power on a baremetal server

Usage: `cubecli baremetal power start <id>`

## `cubecli baremetal power stop`

Power off a baremetal server

Usage: `cubecli baremetal power stop <id>`

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

## `cubecli baremetal update`

Update a baremetal server

Usage: `cubecli baremetal update <id> [flags]`

- `--hostname string`: New hostname
- `--tags string`: Tags for the server
