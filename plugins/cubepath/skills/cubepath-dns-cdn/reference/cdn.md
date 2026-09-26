# cubecli cdn

Manage CDN zones and distribution

## `cubecli cdn metrics bandwidth`

Show CDN bandwidth metrics

Usage: `cubecli cdn metrics bandwidth <zone_uuid> [flags]`

- `--interval int`: Interval in seconds (default 60)
- `-g, --group-by string`: Group by field (default time)
- `-m, --minutes int`: Time range in minutes (default 60)

## `cubecli cdn metrics blocked`

Show blocked request metrics

Usage: `cubecli cdn metrics blocked <zone_uuid> [flags]`

- `-m, --minutes int`: Time range in minutes (default 60)

## `cubecli cdn metrics cache`

Show CDN cache metrics

Usage: `cubecli cdn metrics cache <zone_uuid> [flags]`

- `-m, --minutes int`: Time range in minutes (default 60)

## `cubecli cdn metrics file-extensions`

Show metrics by file extension

Usage: `cubecli cdn metrics file-extensions <zone_uuid> [flags]`

- `-l, --limit int`: Maximum number of results (default 20)
- `-m, --minutes int`: Time range in minutes (default 60)

## `cubecli cdn metrics pops`

Show metrics by PoP location

Usage: `cubecli cdn metrics pops <zone_uuid> [flags]`

- `-m, --minutes int`: Time range in minutes (default 60)

## `cubecli cdn metrics requests`

Show CDN request metrics

Usage: `cubecli cdn metrics requests <zone_uuid> [flags]`

- `--interval int`: Interval in seconds (default 60)
- `-m, --minutes int`: Time range in minutes (default 60)

## `cubecli cdn metrics status-codes`

Show CDN status code metrics

Usage: `cubecli cdn metrics status-codes <zone_uuid> [flags]`

- `-m, --minutes int`: Time range in minutes (default 60)

## `cubecli cdn metrics summary`

Show CDN metrics summary

Usage: `cubecli cdn metrics summary <zone_uuid> [flags]`

- `-m, --minutes int`: Time range in minutes (default 60)

## `cubecli cdn metrics top-asn`

Show top ASNs by requests

Usage: `cubecli cdn metrics top-asn <zone_uuid> [flags]`

- `-l, --limit int`: Maximum number of results (default 20)
- `-m, --minutes int`: Time range in minutes (default 60)

## `cubecli cdn metrics top-countries`

Show top countries by requests

Usage: `cubecli cdn metrics top-countries <zone_uuid> [flags]`

- `-l, --limit int`: Maximum number of results (default 20)
- `-m, --minutes int`: Time range in minutes (default 60)

## `cubecli cdn metrics top-urls`

Show top requested URLs

Usage: `cubecli cdn metrics top-urls <zone_uuid> [flags]`

- `-l, --limit int`: Maximum number of results (default 20)
- `-m, --minutes int`: Time range in minutes (default 60)

## `cubecli cdn metrics top-user-agents`

Show top user agents by requests

Usage: `cubecli cdn metrics top-user-agents <zone_uuid> [flags]`

- `-l, --limit int`: Maximum number of results (default 20)
- `-m, --minutes int`: Time range in minutes (default 60)

## `cubecli cdn origin create`

Create a new CDN origin

Usage: `cubecli cdn origin create <zone_uuid> [flags]`

- `--backup`: Mark origin as backup
- `--base-path string`: Base path for the origin
- `--health-path string`: Health check path (default /health)
- `--host-header string`: Host header override
- `--no-health-check`: Disable health checks
- `--no-verify-ssl`: Disable SSL verification
- `--priority int`: Origin priority (default 1)
- `--protocol string`: Origin protocol
- `-a, --address string`: Origin address
- `-n, --name string`: Name of the origin (required)
- `-p, --port int`: Origin port
- `-u, --url string`: Origin URL
- `-w, --weight int`: Origin weight (default 100)

## `cubecli cdn origin delete`

Delete a CDN origin

Usage: `cubecli cdn origin delete <zone_uuid> <origin_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli cdn origin list`

List CDN origins for a zone

Usage: `cubecli cdn origin list <zone_uuid>`

## `cubecli cdn origin update`

Update a CDN origin

Usage: `cubecli cdn origin update <zone_uuid> <origin_uuid> [flags]`

- `--base-path string`: New base path
- `--host-header string`: New host header override
- `--priority int`: New priority
- `--protocol string`: New protocol
- `-a, --address string`: New address
- `-n, --name string`: New name for the origin
- `-p, --port int`: New port
- `-w, --weight int`: New weight

## `cubecli cdn plan list`

List available CDN plans

Usage: `cubecli cdn plan list`

## `cubecli cdn rule create`

Create a new CDN rule

Usage: `cubecli cdn rule create <zone_uuid> [flags]`

- `--disabled`: Create rule in disabled state
- `-a, --action string`: Action configuration (JSON string) (required)
- `-m, --match string`: Match conditions (JSON string)
- `-n, --name string`: Name of the rule (required)
- `-p, --priority int`: Rule priority (default 100)
- `-t, --type string`: Rule type (cache, cache_bypass, redirect, header_request, header_response) (required)

## `cubecli cdn rule delete`

Delete a CDN rule

Usage: `cubecli cdn rule delete <zone_uuid> <rule_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli cdn rule list`

List CDN rules for a zone

Usage: `cubecli cdn rule list <zone_uuid>`

## `cubecli cdn rule show`

Show CDN rule details

Usage: `cubecli cdn rule show <zone_uuid> <rule_uuid>`

## `cubecli cdn rule update`

Update a CDN rule

Usage: `cubecli cdn rule update <zone_uuid> <rule_uuid> [flags]`

- `-a, --action string`: New action configuration (JSON string)
- `-m, --match string`: New match conditions (JSON string)
- `-n, --name string`: New name for the rule
- `-p, --priority int`: New priority

## `cubecli cdn waf create`

Create a new WAF rule

Usage: `cubecli cdn waf create <zone_uuid> [flags]`

- `--disabled`: Create rule in disabled state
- `-a, --action string`: Action configuration (JSON string) (required)
- `-m, --match string`: Match conditions (JSON string)
- `-n, --name string`: Name of the WAF rule (required)
- `-p, --priority int`: Rule priority (default 100)
- `-t, --type string`: WAF rule type (required)

## `cubecli cdn waf delete`

Delete a WAF rule

Usage: `cubecli cdn waf delete <zone_uuid> <rule_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli cdn waf list`

List WAF rules for a zone

Usage: `cubecli cdn waf list <zone_uuid>`

## `cubecli cdn waf show`

Show WAF rule details

Usage: `cubecli cdn waf show <zone_uuid> <rule_uuid>`

## `cubecli cdn waf update`

Update a WAF rule

Usage: `cubecli cdn waf update <zone_uuid> <rule_uuid> [flags]`

- `-a, --action string`: New action configuration (JSON string)
- `-m, --match string`: New match conditions (JSON string)
- `-n, --name string`: New name for the WAF rule
- `-p, --priority int`: New priority

## `cubecli cdn zone create`

Create a new CDN zone

Usage: `cubecli cdn zone create [flags]`

- `--project int`: Project ID
- `-d, --domain string`: Custom domain
- `-n, --name string`: Name of the CDN zone (3-32 characters) (required)
- `-p, --plan string`: Plan name (required)

## `cubecli cdn zone delete`

Delete a CDN zone

Usage: `cubecli cdn zone delete <zone_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli cdn zone list`

List CDN zones

Usage: `cubecli cdn zone list`

## `cubecli cdn zone move-project`

Move a CDN zone to a different project in the same organization

Usage: `cubecli cdn zone move-project <zone_uuid> [flags]`

- `--project int`: Target project ID (required)

## `cubecli cdn zone pricing`

Show CDN zone pricing

Usage: `cubecli cdn zone pricing <zone_uuid>`

## `cubecli cdn zone request-ssl`

Re-trigger automatic SSL issuance for the zone's custom domain

Use after fixing a missing/incorrect CNAME on your custom domain. The initial PATCH zone flow only queues a cert task when custom_domain changes, so this is the way to retry without resetting the field.

Usage: `cubecli cdn zone request-ssl <zone_uuid>`

## `cubecli cdn zone show`

Show CDN zone details

Usage: `cubecli cdn zone show <zone_uuid>`

## `cubecli cdn zone update`

Update a CDN zone

Usage: `cubecli cdn zone update <zone_uuid> [flags]`

- `--certificate string`: SSL certificate
- `--ssl-type string`: SSL type
- `-d, --domain string`: Custom domain
- `-n, --name string`: New name for the CDN zone
