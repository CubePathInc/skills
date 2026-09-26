---
name: cubepath-kubernetes
description: Create and operate CubePath managed Kubernetes clusters with cubecli - versions and plans, HA control plane, private clusters behind a NAT gateway, node pools and autoscaling, kubeconfig, Helm addons from the catalog, and exposing services through a CubePath load balancer. Use when the user wants a Kubernetes/k8s cluster on CubePath or needs to scale, access or change one.
---

# CubePath managed Kubernetes

Follow the `cubepath-cli` skill first (session, profile, `--json`, confirmations).
Exact flags: [reference/kubernetes.md](reference/kubernetes.md).

CubePath runs the control plane; the workers are VPS in node pools, billed as
VPS. Each node pool is backed by an availability group (spread strategy) named
`k8s-<cluster>-<pool>`.

## Create a cluster

1. Pick inputs:
   - `cubecli kubernetes versions --json`: latest unless the user needs a
     specific one;
   - `cubecli kubernetes plans --json` (optionally `--version`): this list is
     not per location, so check the plan is in stock in the chosen location
     with `cubecli vps plan list --json`;
   - project and location (see `cubepath-cli`).
2. Decide with the user:
   - `--nodes` for the default pool (at least 2 for anything that should
     survive a node failure);
   - `--ha` for a highly available control plane (production);
   - public or private workers (below).
3. Confirm the plan, node count and price, then create:

```bash
cubecli kubernetes create --json --name prod --project 882 --location eu-bcn-1 \
  --plan gp.small --nodes 3 --ha
cubecli kubernetes show <cluster_uuid> --json    # poll until status is active
```

Provisioning takes several minutes. `status` goes `provisioning` -> `active`;
`degraded` or `error` means something needs attention (check the workers'
`k8s_status` in `show`).

### Private workers

Workers without public IPs need an existing private network with an active NAT
gateway (or a `0.0.0.0/0` route) in the same location, or the create is
rejected:

```bash
# see cubepath-networking for network + NAT gateway creation
cubecli kubernetes create ... --network-id <network_id> --allocate-ipv4=false --allocate-ipv6=false
```

Pod and service CIDRs default to `10.42.0.0/16` and `10.43.0.0/16`. Only change
them (`--pod-cidr`, `--service-cidr`) if they overlap the private network or
the user's other ranges.

## Access

```bash
cubecli kubernetes kubeconfig <cluster_uuid> -o ~/.kube/cubepath-prod.yaml
chmod 600 ~/.kube/cubepath-prod.yaml
KUBECONFIG=~/.kube/cubepath-prod.yaml kubectl get nodes
```

Only available once the cluster is `active` or `degraded`. The kubeconfig is a
credential: write it to a file with restrictive permissions, never print it
into the conversation, and do not overwrite `~/.kube/config` without asking.

## Node pools

```bash
cubecli kubernetes node-pool list <cluster_uuid> --json
cubecli kubernetes node-pool create <cluster_uuid> --name gpu --plan <plan> --count 2 \
  --label workload=batch --taint dedicated=batch:NoSchedule
cubecli kubernetes node-pool update <cluster_uuid> <pool_uuid> --min-nodes 2 --max-nodes 6 --auto-scale
cubecli kubernetes node-pool add-nodes <cluster_uuid> <pool_uuid> --count 1
cubecli kubernetes node-pool remove-node <cluster_uuid> <pool_uuid> <vps_id> --force
```

- Adding nodes and pools is billable; removing nodes evicts their pods. Confirm
  both.
- With autoscaling on, the autoscaler may recreate a node you removed by hand;
  adjust `--min-nodes`/`--desired-nodes` instead.
- Before removing a node, suggest `kubectl drain <node>` so workloads move
  cleanly.

## Addons

Curated Helm charts installed by CubePath:

```bash
cubecli kubernetes addon list --json
cubecli kubernetes addon show <slug> --json
cubecli kubernetes addon install <cluster_uuid> <slug> [--values values.json]
cubecli kubernetes addon installed <cluster_uuid> --json
```

`--values` takes JSON or a file path with Helm values. Installation is
asynchronous; check `addon installed` for its status.

## Expose a service

There is no automatic `Service type: LoadBalancer`. Expose workloads with a
NodePort (or an ingress controller addon listening on a NodePort) and put a
CubePath load balancer in front of the node pool:

1. `kubectl` a Service of type `NodePort` (for example port 30080).
2. Find the pool's availability group: `cubecli availability-group list <project_id> --json`
   (named `k8s-<cluster>-<pool>`).
3. Create a load balancer in the same location, attached to the cluster's
   private network if it has one, with a listener on 80/443 whose target port
   is the NodePort and whose target is the availability group
   (`--type availability_group --target <group_uuid>`). See `cubepath-networking`.
4. `cubecli kubernetes loadbalancers <cluster_uuid> --json` lists the load
   balancers pointing at the cluster.

Targeting the availability group keeps the load balancer in sync as nodes are
added or removed.

## Delete

`cubecli kubernetes delete <cluster_uuid> --force` destroys the control plane,
every worker VPS and their public IPs. Confirm explicitly, naming the cluster
and its node count. A cluster still `provisioning`, or with a task running,
cannot be deleted yet.
