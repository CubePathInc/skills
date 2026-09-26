# cubecli nat-gateway

Manage NAT gateways

## `cubecli nat-gateway create`

Create a new NAT gateway on a private network

Usage: `cubecli nat-gateway create [flags]`

- `--label string`: Optional label
- `--network-id int`: ID of the private network to attach (required)
- `--plan string`: Plan name (see 'nat-gateway plans') (required)
- `-n, --name string`: NAT gateway name (required)
- `-p, --project int`: Project ID (inferred from the network if omitted)

## `cubecli nat-gateway delete`

Delete a NAT gateway

Usage: `cubecli nat-gateway delete <ng_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli nat-gateway list`

List NAT gateways

Usage: `cubecli nat-gateway list [flags]`

- `-l, --location string`: Filter by location

## `cubecli nat-gateway move`

Move a NAT gateway to another project

Usage: `cubecli nat-gateway move <ng_uuid> [flags]`

- `-p, --project int`: Target project ID (required)

## `cubecli nat-gateway plans`

List available NAT gateway plans

Usage: `cubecli nat-gateway plans`

## `cubecli nat-gateway protection`

Enable or disable destruction protection

Usage: `cubecli nat-gateway protection <ng_uuid> [flags]`

- `--disable`: Disable destruction protection
- `--enable`: Enable destruction protection

## `cubecli nat-gateway resize`

Resize a NAT gateway to a different plan

Usage: `cubecli nat-gateway resize <ng_uuid> [flags]`

- `-p, --plan string`: New plan name (required)

## `cubecli nat-gateway show`

Show NAT gateway details

Usage: `cubecli nat-gateway show <ng_uuid>`

## `cubecli nat-gateway update`

Update a NAT gateway

Usage: `cubecli nat-gateway update <ng_uuid> [flags]`

- `--label string`: New label for the NAT gateway
- `-n, --name string`: New name for the NAT gateway
