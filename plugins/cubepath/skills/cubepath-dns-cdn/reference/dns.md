# cubecli dns

Manage DNS zones and records

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

- `-p, --project int`: Project ID (required)

## `cubecli dns zone delete`

Delete a DNS zone

Usage: `cubecli dns zone delete <zone_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli dns zone list`

List DNS zones

Usage: `cubecli dns zone list [flags]`

- `-p, --project int`: Filter by project ID

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
