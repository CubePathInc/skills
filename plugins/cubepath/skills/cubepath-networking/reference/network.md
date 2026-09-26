# cubecli network

Manage networks

## `cubecli network create`

Create a new network

Usage: `cubecli network create [flags]`

- `--label string`: Optional label
- `-c, --cidr string`: CIDR notation (e.g. 10.0.0.0/24) (required)
- `-l, --location string`: Location for the network (required)
- `-n, --name string`: Name of the network (required)
- `-p, --project int`: Project ID (required)

## `cubecli network delete`

Delete a network

Usage: `cubecli network delete <network_id> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli network list`

List networks

Usage: `cubecli network list [flags]`

- `-l, --location string`: Filter by location
- `-p, --project int`: Filter by project ID

## `cubecli network route create`

Create a route on a private network

Usage: `cubecli network route create <network_id> [flags]`

- `--description string`: Optional description
- `-d, --destination string`: Destination CIDR (e.g. 0.0.0.0/0) (required)
- `-g, --next-hop-target string`: Next hop target (IP address, or numeric VPS/baremetal ID) (required)
- `-t, --next-hop-type string`: Next hop type (ip, vps, baremetal) (required)

## `cubecli network route delete`

Delete a route from a private network

Usage: `cubecli network route delete <network_id> <route_id> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli network route list`

List routes for a private network

Usage: `cubecli network route list <network_id>`

## `cubecli network update`

Update a network

Usage: `cubecli network update <network_id> [flags]`

- `--label string`: New label for the network
- `-n, --name string`: New name for the network
