# cubecli dns

Manage DNS zones and records

## `cubecli dns health-check delete`

Delete the health check of a record

Usage: `cubecli dns health-check delete <zone_uuid> <record_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli dns health-check list`

List the health checks of a zone

Usage: `cubecli dns health-check list <zone_uuid>`

## `cubecli dns health-check set`

Create or replace the health check of an A/AAAA record

Usage: `cubecli dns health-check set <zone_uuid> <record_uuid> [flags]`

- `--disabled`: Save the check disabled (not billed, no failover)
- `--expected-status int`: Expected HTTP status (http/https) (default 200)
- `--healthy-threshold int`: Successes before healthy (1-10) (default 2)
- `--interval int`: Seconds between checks (10-3600) (default 60)
- `--path string`: HTTP path, e.g. /health (http/https)
- `--port int`: Port (required for tcp)
- `--target string`: Hostname or IP to probe (default: the record's value)
- `--timeout int`: Timeout in seconds (1-60, below the interval) (default 5)
- `--type string`: Check type: http, https, tcp or ping (required)
- `--unhealthy-threshold int`: Failures before unhealthy (1-10) (default 3)
- `-n, --name string`: Name (required)

Examples:

```
  cubecli dns health-check set <zone_uuid> <record_uuid> --name web --type https --path /health
  cubecli dns health-check set <zone_uuid> <record_uuid> --name db --type tcp --port 5432 --interval 30
```

## `cubecli dns health-check show`

Show the health check of a record

Usage: `cubecli dns health-check show <zone_uuid> <record_uuid>`

## `cubecli dns record create`

Create a DNS record

Usage: `cubecli dns record create <zone_uuid> [flags]`

- `--comment string`: Record comment
- `--port int`: Record port (for SRV)
- `--priority int`: Record priority (for MX, SRV)
- `--ttl int`: Time to live in seconds (default 3600)
- `--weight int`: Record weight (for SRV)
- `-c, --content string`: Record content (required)
- `-n, --name string`: Record name (required)
- `-t, --type string`: Record type (A, AAAA, CNAME, MX, TXT, etc.) (required)

## `cubecli dns record delete`

Delete a DNS record

Usage: `cubecli dns record delete <zone_uuid> <record_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli dns record list`

List DNS records in a zone

Usage: `cubecli dns record list <zone_uuid> [flags]`

- `-t, --type string`: Filter by record type

## `cubecli dns record update`

Update a DNS record

Usage: `cubecli dns record update <zone_uuid> <record_uuid> [flags]`

- `--comment string`: Record comment
- `--port int`: Record port
- `--priority int`: Record priority
- `--ttl int`: Time to live in seconds
- `--weight int`: Record weight
- `-c, --content string`: Record content

## `cubecli dns regions`

List the GeoDNS regions records can target

Usage: `cubecli dns regions`

## `cubecli dns soa show`

Show SOA record for a zone

Usage: `cubecli dns soa show <zone_uuid>`

## `cubecli dns soa update`

Update SOA record for a zone

Usage: `cubecli dns soa update <zone_uuid> [flags]`

- `--expire int`: SOA expire time in seconds
- `--hostmaster string`: SOA hostmaster email
- `--minimum int`: SOA minimum TTL in seconds
- `--refresh int`: SOA refresh interval in seconds
- `--retry int`: SOA retry interval in seconds

## `cubecli dns zone create`

Create a new DNS zone

Usage: `cubecli dns zone create <domain> [flags]`

- `--scan`: Import the records currently served by public DNS
- `--zone-file string`: Import records from this BIND zone file
- `-p, --project int`: Project ID (required)

## `cubecli dns zone delete`

Delete a DNS zone

Usage: `cubecli dns zone delete <zone_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli dns zone import`

Import records from a BIND zone file into an existing zone

Import records from a BIND zone file (max 1 MB). NS records are skipped,
duplicates and conflicting CNAMEs are reported and skipped, and the file's SOA
timers are applied to the zone.

Usage: `cubecli dns zone import <zone_uuid> <zone_file>`

## `cubecli dns zone list`

List DNS zones

Usage: `cubecli dns zone list [flags]`

- `-p, --project int`: Filter by project ID

## `cubecli dns zone move-project`

Move a DNS zone to another project in the same organization

Usage: `cubecli dns zone move-project <zone_uuid> [flags]`

Aliases: move

- `-p, --project int`: Target project ID (required)

## `cubecli dns zone scan`

Scan a DNS zone for records

Usage: `cubecli dns zone scan <zone_uuid> [flags]`

- `--import`: Auto-import discovered records (default true)
- `--preview`: Preview records without importing

## `cubecli dns zone show`

Show DNS zone details

Usage: `cubecli dns zone show <zone_uuid>`

## `cubecli dns zone verify`

Verify a DNS zone

Usage: `cubecli dns zone verify <zone_uuid>`
