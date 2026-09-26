---
name: cubepath-networking
description: Manage CubePath networking with cubecli - private networks and routes, NAT gateways for outbound Internet from private servers, floating IPs and reverse DNS, load balancers (listeners, targets, health checks) and DDoS attack history. Use when the user wants to connect servers privately, put servers behind a load balancer, move or reserve a public IP, set a PTR record, or give private servers Internet access on CubePath.
---

# CubePath networking

Follow the `cubepath-cli` skill first (session, profile, `--json`, confirmations).
Exact flags: [network](reference/network.md), [nat-gateway](reference/nat-gateway.md),
[floating-ip](reference/floating-ip.md), [lb](reference/lb.md),
[ddos-attack](reference/ddos-attack.md).

Everything here is per location: a private network, the servers on it, its NAT
gateway and a load balancer attached to it must all be in the same location.

## Private networks

```bash
cubecli network list --json          # same shape as project list: .[].networks[]
cubecli network create --name backend --project 882 --location eu-bcn-1 --cidr 10.10.0.0/24
cubecli vps create ... --network <network_id>    # attach a new VPS
```

- Pick an RFC 1918 CIDR that does not overlap the user's other networks or
  their VPN/office ranges. A /24 is plenty for most setups.
- The first address (`.1`) is the gateway; servers get the next free address.
- A VPS can be created without public IPv6 only if it has a private network
  (`--no-ipv6 --network <id>`); `--no-ipv4` drops the public IPv4.

### Routes

Send traffic for a destination through a server on the network (for example a
VPN or firewall VPS):

```bash
cubecli network route create <network_id> --destination 192.168.50.0/24 \
  --next-hop-type vps --next-hop-target <vps_id>
cubecli network route list <network_id> --json
```

`--next-hop-type` is `ip`, `vps` or `baremetal`; the target is an IP or the
numeric server ID.

## NAT gateway (outbound Internet for private servers)

Servers without public IPs reach the Internet through a NAT gateway attached to
their private network. It is egress-only: it does not publish services (use a
load balancer or floating IP for inbound).

```bash
cubecli nat-gateway plans --json
cubecli nat-gateway create --name egress --network-id <network_id> --plan <plan>
cubecli nat-gateway show <uuid> --json
```

It is billable; confirm plan and price first. `nat-gateway protection --enable`
prevents accidental deletion.

## Floating IPs

Public IPs that belong to the organization and can move between servers.

```bash
cubecli floating-ip list --json          # {"single_ips": [...], "subnets": [...]}
cubecli floating-ip acquire --location eu-bcn-1 --type IPv4
cubecli floating-ip assign <address> --vps <vps_id>        # or --baremetal <id>
cubecli floating-ip unassign <address> --force
cubecli floating-ip reverse-dns <address> --hostname mail.example.com
cubecli floating-ip release <address> --force               # gives it back, irreversible
```

- Acquiring is billable; releasing is irreversible (the address may go to
  another customer). Confirm both.
- Unassigning takes the IP off a running server and breaks whatever uses it.
- For reverse DNS, the hostname should resolve forward to the same IP (mail
  servers in particular). Pass an empty hostname to remove the PTR.

## Load balancers

Managed load balancers in front of VPS, baremetal servers or a whole availability
group.

```bash
cubecli lb plan list --json
cubecli lb create --name web-lb --location eu-bcn-1 --plan <plan> --project 882 \
  [--network-id <network_id>]
cubecli lb show <lb_uuid> --json        # wait for status active before adding listeners
cubecli lb listener create <lb_uuid> --name http --port 80 --target-port 8080 --protocol http
cubecli lb target add <lb_uuid> <listener_uuid> --type vps --target <vps_id>
cubecli lb health-check configure <lb_uuid> <listener_uuid> --path /healthz
```

- `--target` depends on `--type`: the numeric ID for `vps` and `baremetal`,
  the group UUID for `availability_group` (targets every VPS in it, the usual
  choice for redundant web servers).
- The UUID used later by `target update|drain|remove` is the target's own UUID
  from `lb show`, not the VPS ID.
- Attach the load balancer to the servers' private network (`--network-id`) so
  it reaches them over private IPs; same location required.
- Protocols: `http` and `tcp` work from the CLI. `https` needs an SSL
  certificate, which is configured in the dashboard; tell the user.
- Algorithm (`-a`) defaults to `round_robin`; `--sticky` pins clients to a
  target.
- Maintenance on a target: `lb target drain` first, then work on the server.
- Changes to an LB that is still provisioning, or has a task pending, return
  409; wait and retry.

## DDoS

`cubecli ddos-attack list --json` shows attacks detected against the
organization's IPs. Every public IP has DDoS protection; there is nothing to
enable from the CLI.
