# cubecli kubernetes

Manage Kubernetes clusters

## `cubecli kubernetes addon install`

Install an addon on a cluster

Usage: `cubecli kubernetes addon install <cluster_uuid> <addon_slug> [flags]`

- `--values string`: Custom Helm values (JSON string or file path)

## `cubecli kubernetes addon installed`

List addons installed on a cluster

Usage: `cubecli kubernetes addon installed <cluster_uuid>`

## `cubecli kubernetes addon list`

Browse available addons

Usage: `cubecli kubernetes addon list`

## `cubecli kubernetes addon show`

Show addon details

Usage: `cubecli kubernetes addon show <slug>`

## `cubecli kubernetes addon uninstall`

Uninstall an addon from a cluster

Usage: `cubecli kubernetes addon uninstall <cluster_uuid> <addon_uuid> [flags]`

- `-f, --force`: Skip confirmation

## `cubecli kubernetes create`

Create a new Kubernetes cluster

Usage: `cubecli kubernetes create [flags]`

- `--allocate-ipv4`: Assign a public IPv4 to each worker (set false for private workers behind a NAT gateway) (default true)
- `--allocate-ipv6`: Assign a public IPv6 to each worker (set false for private workers behind a NAT gateway) (default true)
- `--ha`: Enable HA control plane
- `--network-id int`: Existing network ID
- `--node-cidr string`: Custom node CIDR
- `--nodes int`: Number of initial worker nodes (default 1)
- `--plan string`: Server plan for the default node pool (required)
- `--pod-cidr string`: Pod CIDR (default 10.42.0.0/16)
- `--service-cidr string`: Service CIDR (default 10.43.0.0/16)
- `--version string`: Kubernetes version (default: latest)
- `-l, --location string`: Location name (required)
- `-n, --name string`: Cluster name (required)
- `-p, --project int`: Project ID (required)

## `cubecli kubernetes delete`

Delete a Kubernetes cluster

Usage: `cubecli kubernetes delete <cluster_uuid> [flags]`

- `-f, --force`: Skip confirmation

## `cubecli kubernetes kubeconfig`

Download kubeconfig for a cluster

Usage: `cubecli kubernetes kubeconfig <cluster_uuid> [flags]`

- `-o, --output string`: Save kubeconfig to file

## `cubecli kubernetes list`

List Kubernetes clusters

Usage: `cubecli kubernetes list`

## `cubecli kubernetes loadbalancers`

List load balancers targeting a cluster

Usage: `cubecli kubernetes loadbalancers <cluster_uuid>`

## `cubecli kubernetes metrics`

Show cluster health metrics, or a node's with --node

Show the cluster's health series (nodes ready, pending and failed pods, API
latency) or, with --node, a node's readiness and usage plus its server's.

Usage: `cubecli kubernetes metrics <cluster_uuid> [flags]`

- `--node string`: Node name (see 'kubernetes show')
- `--range string`: Time range: 1h, 3h, 6h, 12h, 24h, 3d, 7d, 30d (default 1h)

## `cubecli kubernetes move`

Move a cluster to another project

Usage: `cubecli kubernetes move <cluster_uuid> [flags]`

- `-p, --project int`: Target project ID (required)

## `cubecli kubernetes node-pool add-nodes`

Add worker nodes to a pool

Usage: `cubecli kubernetes node-pool add-nodes <cluster_uuid> <pool_uuid> [flags]`

- `--count int`: Number of nodes to add (default 1)

## `cubecli kubernetes node-pool create`

Create a new node pool

Usage: `cubecli kubernetes node-pool create <cluster_uuid> [flags]`

- `--auto-scale`: Enable auto scaling (default true)
- `--count int`: Number of worker nodes (default 1)
- `--label stringSlice`: Node labels (key=value, can specify multiple)
- `--plan string`: Server plan (required)
- `--taint stringSlice`: Node taints (key=value:Effect, can specify multiple)
- `-n, --name string`: Node pool name (default default)

## `cubecli kubernetes node-pool delete`

Delete a node pool

Usage: `cubecli kubernetes node-pool delete <cluster_uuid> <pool_uuid> [flags]`

- `-f, --force`: Skip confirmation

## `cubecli kubernetes node-pool list`

List node pools in a cluster

Usage: `cubecli kubernetes node-pool list <cluster_uuid>`

## `cubecli kubernetes node-pool remove-node`

Remove a specific worker node from a pool

Usage: `cubecli kubernetes node-pool remove-node <cluster_uuid> <pool_uuid> <vps_id> [flags]`

- `-f, --force`: Skip confirmation

## `cubecli kubernetes node-pool update`

Update a node pool

Usage: `cubecli kubernetes node-pool update <cluster_uuid> <pool_uuid> [flags]`

- `--auto-scale`: Enable/disable auto scaling
- `--desired-nodes int`: Desired number of nodes
- `--label stringSlice`: Node labels (key=value)
- `--max-nodes int`: Maximum number of nodes
- `--min-nodes int`: Minimum number of nodes
- `--taint stringSlice`: Node taints (key=value:Effect)
- `-n, --name string`: New pool name

## `cubecli kubernetes plans`

List server plans compatible with Kubernetes

Usage: `cubecli kubernetes plans [flags]`

- `--version string`: Filter plans by Kubernetes version

## `cubecli kubernetes protection`

Enable or disable destruction protection

Usage: `cubecli kubernetes protection <cluster_uuid> [flags]`

- `--disable`: Disable destruction protection
- `--enable`: Enable destruction protection

## `cubecli kubernetes show`

Show Kubernetes cluster details

Usage: `cubecli kubernetes show <cluster_uuid>`

## `cubecli kubernetes update`

Update a Kubernetes cluster

Usage: `cubecli kubernetes update <cluster_uuid> [flags]`

- `--label string`: New cluster label
- `-n, --name string`: New cluster name

## `cubecli kubernetes versions`

List available Kubernetes versions

Usage: `cubecli kubernetes versions`
