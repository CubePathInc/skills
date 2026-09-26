# cubecli lb

Manage load balancers

## `cubecli lb create`

Create a new load balancer

Usage: `cubecli lb create [flags]`

- `--label string`: Optional label
- `--network-id int`: Attach to a private network (reaches targets by their private IP; same location required)
- `--project int`: Project ID
- `-l, --location string`: Location name (required)
- `-n, --name string`: Name of the load balancer (required)
- `-p, --plan string`: Plan name (required)

## `cubecli lb delete`

Delete a load balancer

Usage: `cubecli lb delete <lb_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli lb health-check configure`

Configure a health check for a listener

Usage: `cubecli lb health-check configure <lb_uuid> <listener_uuid> [flags]`

- `--codes string`: Expected HTTP status codes (default 200-399)
- `--healthy int`: Healthy threshold (1-10) (default 2)
- `--interval int`: Interval in seconds (5-300) (default 30)
- `--path string`: Health check path (default /)
- `--timeout int`: Timeout in seconds (1-60) (default 5)
- `--unhealthy int`: Unhealthy threshold (1-10) (default 3)
- `-p, --protocol string`: Health check protocol (default http)

## `cubecli lb health-check delete`

Delete a health check from a listener

Usage: `cubecli lb health-check delete <lb_uuid> <listener_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli lb list`

List load balancers

Usage: `cubecli lb list`

## `cubecli lb listener create`

Create a listener on a load balancer

Usage: `cubecli lb listener create <lb_uuid> [flags]`

- `--no-sticky`: Disable sticky sessions
- `--port int`: Source port (required)
- `--sticky`: Enable sticky sessions
- `--target-port int`: Target port (required)
- `-a, --algorithm string`: Load balancing algorithm (default round_robin)
- `-n, --name string`: Name of the listener (required)
- `-p, --protocol string`: Protocol (e.g. http, https, tcp) (default http)

## `cubecli lb listener delete`

Delete a listener from a load balancer

Usage: `cubecli lb listener delete <lb_uuid> <listener_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli lb listener update`

Update a listener on a load balancer

Usage: `cubecli lb listener update <lb_uuid> <listener_uuid> [flags]`

- `--disable`: Disable the listener
- `--enable`: Enable the listener
- `--target-port int`: New target port
- `-a, --algorithm string`: New load balancing algorithm
- `-n, --name string`: New name for the listener

## `cubecli lb plan list`

List available load balancer plans

Usage: `cubecli lb plan list`

## `cubecli lb resize`

Resize a load balancer

Usage: `cubecli lb resize <lb_uuid> [flags]`

- `-p, --plan string`: New plan name (required)

## `cubecli lb show`

Show load balancer details

Usage: `cubecli lb show <lb_uuid>`

## `cubecli lb target add`

Add a target to a listener

Usage: `cubecli lb target add <lb_uuid> <listener_uuid> [flags]`

- `--target string`: Target UUID (required)
- `-p, --port int`: Target port
- `-t, --type string`: Target type (vps, baremetal, availability_group) (required)
- `-w, --weight int`: Target weight (1-100) (default 100)

## `cubecli lb target drain`

Drain a target

Usage: `cubecli lb target drain <lb_uuid> <listener_uuid> <target_uuid>`

## `cubecli lb target remove`

Remove a target from a listener

Usage: `cubecli lb target remove <lb_uuid> <listener_uuid> <target_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli lb target update`

Update a target

Usage: `cubecli lb target update <lb_uuid> <listener_uuid> <target_uuid> [flags]`

- `--disable`: Disable the target
- `--enable`: Enable the target
- `-p, --port int`: New target port
- `-w, --weight int`: New target weight (1-100)

## `cubecli lb update`

Update a load balancer

Usage: `cubecli lb update <lb_uuid> [flags]`

- `--label string`: New label for the load balancer
- `-n, --name string`: New name for the load balancer
