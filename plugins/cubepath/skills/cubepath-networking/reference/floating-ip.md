# cubecli floating-ip

Manage floating IPs

## `cubecli floating-ip acquire`

Acquire a new floating IP

Usage: `cubecli floating-ip acquire [flags]`

- `-l, --location string`: Location name (required)
- `-t, --type string`: IP type (IPv4 or IPv6) (default IPv4)

## `cubecli floating-ip assign`

Assign a floating IP to a server

Usage: `cubecli floating-ip assign <address> [flags]`

- `--baremetal int`: Baremetal ID to assign to
- `--vps int`: VPS ID to assign to

## `cubecli floating-ip list`

List floating IPs

Usage: `cubecli floating-ip list [flags]`

- `-l, --location string`: Filter by location

## `cubecli floating-ip release`

Release a floating IP

Usage: `cubecli floating-ip release <address> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli floating-ip reverse-dns`

Configure reverse DNS for a floating IP

Usage: `cubecli floating-ip reverse-dns <ip> [flags]`

- `-r, --hostname string`: Reverse DNS hostname (empty string to delete) (required)

## `cubecli floating-ip unassign`

Unassign a floating IP from a server

Usage: `cubecli floating-ip unassign <address> [flags]`

- `-f, --force`: Skip confirmation prompt
