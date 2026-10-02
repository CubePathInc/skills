# cubecli network

Manage networks

## `cubecli network bgp-peer create`

Create a BGP peer

Usage: `cubecli network bgp-peer create <network_id> [flags]`

- `--description string`: Description
- `--max-prefix int`: Maximum prefixes accepted (1-1000) (default 100)
- `--remote-asn int64`: ASN of your router (not 64512) (required)
- `--target string`: VPS ID, baremetal ID or IP inside the network (required)
- `--type string`: Peer type: vps, baremetal or ip (required)

Examples:

```
  cubecli network bgp-peer create 42 --type vps --target 123 --remote-asn 65010
  cubecli network bgp-peer create 42 --type ip --target 10.0.0.5 --remote-asn 65010 --max-prefix 50
```

## `cubecli network bgp-peer delete`

Delete a BGP peer

Usage: `cubecli network bgp-peer delete <network_id> <peer_id> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli network bgp-peer list`

List BGP peers and their session state

Usage: `cubecli network bgp-peer list <network_id>`

## `cubecli network bgp-peer update`

Update a BGP peer (type, target and ASN cannot change)

Usage: `cubecli network bgp-peer update <network_id> <peer_id> [flags]`

- `--description string`: Description
- `--enabled`: Enable or disable the session (--enabled=false) (default true)
- `--max-prefix int`: Maximum prefixes accepted (1-1000)

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

## `cubecli network move-project`

Move a network to another project in the same organization

Usage: `cubecli network move-project <network_id> [flags]`

Aliases: move

- `-p, --project int`: Target project ID (required)

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
