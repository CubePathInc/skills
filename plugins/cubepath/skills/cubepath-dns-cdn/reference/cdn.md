# cubecli cdn

Manage CDN zones and distribution

## `cubecli cdn cache purge`

Purge paths, path prefixes, cache tags, hostnames or the whole cache of a zone

Purge cached content on every edge location. Give exactly one of:
up to 100 paths starting with "/" (a trailing "*" purges every URL under a prefix),
--tag (up to 30 cache tags, needs the zone's cache tag header), --host (one or two
of the zone's hostnames) or --everything. Without --host, both the system and the
custom domain are purged.

Usage: `cubecli cdn cache purge <zone_uuid> [path...] [flags]`

- `--everything`: Purge the whole cache of the zone
- `--host stringSlice`: Purge the objects cached for this hostname of the zone (up to 2)
- `--tag stringSlice`: Purge the objects with this cache tag (repeat or comma separate, up to 30)

Examples:

```
  cubecli cdn cache purge <zone_uuid> /assets/app.css "/images/*"
  cubecli cdn cache purge <zone_uuid> --tag news --tag product-42
  cubecli cdn cache purge <zone_uuid> --host www.example.com
  cubecli cdn cache purge <zone_uuid> --everything
```

## `cubecli cdn cache purges`

Show the latest 20 purges and their progress per edge location

Usage: `cubecli cdn cache purges <zone_uuid>`

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

Create a CDN origin. An origin is either an address (--url or --address) or
one of your Object Storage buckets (--bucket): the CDN then reads the bucket with a
read-only key it manages, and deleting the origin disconnects the bucket. A bucket
can be the origin of one zone at a time.

The health check is a TCP connect by default. --health-type http makes the edge request
--health-path and take the origin out when the answer is not one of --health-expect (if it
is the only origin of the zone, the zone answers 503). All the origins of a zone share one
check: the one of the first origin by priority that has its check enabled.

Usage: `cubecli cdn origin create <zone_uuid> [flags]`

- `--backup`: Mark origin as backup
- `--base-path string`: Base path for the origin
- `--bucket string`: Object Storage bucket (name or uuid) to serve through this zone
- `--health-expect string`: Statuses or classes an http health check accepts, up to 8 separated by spaces (default "2xx 3xx"), e.g. "200 301"
- `--health-interval int`: Seconds between health checks from each edge node, 5 to 300 (default 10)
- `--health-method string`: Method of an http health check: GET (default) or HEAD
- `--health-path string`: Health check path (default /health)
- `--health-threshold int`: Results in a row that change the health status, 1 to 10 (default 3)
- `--health-type string`: Health check type: tcp (default) or http
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

Examples:

```
  cubecli cdn origin create <zone_uuid> --name web --url https://origin.example.com
  cubecli cdn origin create <zone_uuid> --name web --url https://origin.example.com --health-type http --health-path /ping --health-expect 200
  cubecli cdn origin create <zone_uuid> --name photos --bucket photos
```

## `cubecli cdn origin delete`

Delete a CDN origin

Delete a CDN origin. If the origin is an Object Storage bucket, this
disconnects the bucket: the CDN stops reading it and its public URLs stop working.

Usage: `cubecli cdn origin delete <zone_uuid> <origin_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli cdn origin list`

List CDN origins for a zone

Usage: `cubecli cdn origin list <zone_uuid>`

## `cubecli cdn origin update`

Update a CDN origin

Usage: `cubecli cdn origin update <zone_uuid> <origin_uuid> [flags]`

- `--base-path string`: New base path
- `--health-expect string`: Statuses or classes an http health check accepts, up to 8 separated by spaces (default "2xx 3xx"), e.g. "200 301"
- `--health-interval int`: Seconds between health checks from each edge node, 5 to 300 (default 10)
- `--health-method string`: Method of an http health check: GET (default) or HEAD
- `--health-threshold int`: Results in a row that change the health status, 1 to 10 (default 3)
- `--health-type string`: Health check type: tcp (default) or http
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

Create an edge rule. --action is a JSON object that depends on --type:
  cache         {"ttl": 3600, "browser_ttl": 600} plus optional "cache_everything" (also cache HTML,
                JSON and XML), "grace", "stale_if_error" and "status_ttl" ({"404": 60})
  cache_key     {"query": "none"} (all, none, allow or strip, with "query_params"), "vary_device"
                and "vary_headers". Adding, changing or removing one empties the cache of the zone.
  url_rewrite   {"path": {"mode": "prefix", "from": "/old/", "to": "/new/"}, "strip_query": ["utm_*"],
                "set_query": {"src": "cdn"}}. The origin gets the rewritten URL and so does the cache.

Usage: `cubecli cdn rule create <zone_uuid> [flags]`

- `--disabled`: Create rule in disabled state
- `-a, --action string`: Action configuration (JSON string) (required)
- `-m, --match string`: Match conditions (JSON string)
- `-n, --name string`: Name of the rule (required)
- `-p, --priority int`: Rule priority (default 100)
- `-t, --type string`: Rule type (cache, cache_key, cache_bypass, url_rewrite, redirect, header_request, header_response) (required)

Examples:

```
  cubecli cdn rule create <zone_uuid> --name key --type cache_key --action '{"query":"none"}'
  cubecli cdn rule create <zone_uuid> --name old --type url_rewrite \
    --action '{"path":{"mode":"prefix","from":"/old/","to":"/new/"}}'
```

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

## `cubecli cdn token-auth disable`

Turn Token Auth off (the secret is kept)

Usage: `cubecli cdn token-auth disable <zone_uuid>`

## `cubecli cdn token-auth enable`

Turn Token Auth on (the first time prints the secret)

Usage: `cubecli cdn token-auth enable <zone_uuid> [flags]`

- `--ip-binding`: Bind signed URLs to the client IP (--ip-binding=false to unbind)

## `cubecli cdn token-auth rotate-secret`

Replace the secret; every URL signed before stops working

Usage: `cubecli cdn token-auth rotate-secret <zone_uuid> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli cdn token-auth sign-url`

Sign a URL of the zone

Usage: `cubecli cdn token-auth sign-url <zone_uuid> <path> [flags]`

- `--client-ip string`: Client IP (required when the zone binds tokens to IPs)
- `--expires-in int`: Seconds the URL stays valid (60-604800) (default 3600)

Examples:

```
  cubecli cdn token-auth sign-url <zone_uuid> /videos/clip.mp4 --expires-in 3600
```

## `cubecli cdn waf create`

Create a new WAF rule

Create a WAF rule. In a firewall_ip or firewall_country rule, allow_ips and
allow_countries mean only these: when the list is not empty, a client that is not on it
gets a 403, and block_ips and block_countries win over the allow lists. In allow_countries,
XX is a client of no known country (blocked unless XX is listed). An IPv6 client is not on a
list of IPv4 addresses.

Usage: `cubecli cdn waf create <zone_uuid> [flags]`

- `--disabled`: Create rule in disabled state
- `-a, --action string`: Action configuration (JSON string); allow_ips and allow_countries mean only these (required)
- `-m, --match string`: Match conditions (JSON string)
- `-n, --name string`: Name of the WAF rule (required)
- `-p, --priority int`: Rule priority (default 100)
- `-t, --type string`: WAF rule type (required)

Examples:

```
  cubecli cdn waf create <zone_uuid> --name eu-only --type firewall_country --action '{"allow_countries":["ES","FR","XX"]}'
```

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

- `--cache-tag-header string`: Origin response header that carries the cache tags (empty turns tag purges off)
- `--certificate string`: SSL certificate
- `--compression`: Compress text responses at the edge (--compression=false to turn it off)
- `--ssl-type string`: SSL type
- `-d, --domain string`: Custom domain
- `-n, --name string`: New name for the CDN zone
