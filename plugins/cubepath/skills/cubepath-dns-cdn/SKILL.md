---
name: cubepath-dns-cdn
description: Manage CubePath DNS zones and records and the CubePath CDN (zones, origins, custom domains with SSL, cache/redirect/header rules, WAF, rate limits and traffic metrics) with cubecli. Use when the user wants to host a domain's DNS on CubePath, add or change DNS records, put a site behind the CubePath CDN, cache or redirect paths, block IPs/countries/bots, or look at CDN traffic.
---

# CubePath DNS and CDN

Follow the `cubepath-cli` skill first (session, profile, `--json`, confirmations).
Exact flags: [reference/dns.md](reference/dns.md), [reference/cdn.md](reference/cdn.md).

## DNS

### Host a domain

```bash
cubecli dns zone create example.com --project 882 --json
cubecli dns zone scan <zone_uuid> --preview      # records found in public DNS today
cubecli dns zone scan <zone_uuid>                 # import them
```

1. Create the zone. It starts as `pending_verification` with the nameservers
   `atlas.ns.cubepath.com` and `titan.ns.cubepath.com`.
2. Scan and import the existing records **before** the delegation changes, so
   the domain keeps resolving. The scan only finds common names; ask the user
   for anything else (DKIM selectors, unusual subdomains) and review the list.
3. The user changes the nameservers at their registrar. You cannot do this.
4. `cubecli dns zone verify <zone_uuid>`, then check `zone show` until `status`
   is `active`. Records only go live once the zone is active. Delegation can
   take hours to propagate; do not retry verify in a loop.

### Records

```bash
cubecli dns record list <zone_uuid> --json
cubecli dns record create <zone_uuid> --name www --type A --content 203.0.113.10
cubecli dns record create <zone_uuid> --name @ --type MX --content mail.example.com --priority 10
cubecli dns record update <zone_uuid> <record_uuid> --content 203.0.113.20
cubecli dns record delete <zone_uuid> <record_uuid> --force
```

- `--name` is relative to the zone: `www` becomes `www.example.com`, `@` is
  the apex, `*.dev` is a wildcard.
- MX needs `--priority`; SRV needs `--priority`, `--weight` and `--port`.
- A CNAME cannot share a name with any other record (including the apex, which
  has NS records). For the apex use `ALIAS`, or A/AAAA.
- TTL defaults to 3600; the minimum depends on the zone tier (60 s on the free
  tier). The free tier allows 3 zones and 50 records per zone.
- SOA and apex NS records are managed by CubePath and cannot be edited.
- Before changing or deleting a record in use (A of a live site, MX), show the
  current and new values and confirm.

## CDN

A CDN zone gets a system domain `<name>.cubecdn.io` and can serve a custom
domain with automatic SSL. It fetches content from one or more origins.

### Put a site behind the CDN

```bash
cubecli cdn plan list --json
cubecli cdn zone create --name mysite --plan <plan> --project 882 --json    # name: 3-32 chars, a-z 0-9 -
cubecli cdn origin create <zone_uuid> --name main --url https://origin.example.com
cubecli cdn zone update <zone_uuid> --domain cdn.example.com
```

1. The zone is usable at once on `https://<name>.cubecdn.io`. Test it there.
2. For a custom domain, the user points it at the system domain with a CNAME
   (`cdn.example.com CNAME mysite.cubecdn.io`). If the domain's DNS is on
   CubePath you can create that record yourself (see DNS above).
3. SSL is issued automatically once the CNAME resolves. If it was set after the
   domain, re-trigger it: `cubecli cdn zone request-ssl <zone_uuid>`. Check
   `custom_domain_ssl_status` in `cdn zone show`.

Origins: `--url` (full URL) or `--address` + `--port` + `--protocol`. Several
origins balance by `--weight`/`--priority`; `--backup` marks a fallback.
The health check is a TCP connect by default, so it does not request any path.
An HTTP check is opt-in: `--health-type http --health-path /ping --health-expect 200`
(also `--health-method HEAD`, `--health-interval`, `--health-threshold`). Pick a
path that answers 2xx/3xx without cookies, because the edge sends no session.
An HTTP check that fails takes the origin out, and if it is the only origin of
the zone the zone answers 503. All the origins of a zone share one check, the
one of the first origin by priority with its check enabled; the check flags of
the others are stored and do not apply. `--no-health-check` turns it off. While another
origin of the zone has its check on, the nodes still check this one too; when none has
it on, `cubecli cdn origin list` shows `not checked` (the API says `unknown`).

An Object Storage bucket can be an origin too: `cubecli cdn origin create
<zone_uuid> --name photos --bucket photos` (name or uuid, no address flags).
Deleting that origin disconnects the bucket. See `cubepath-object-storage`.

### Rules

`cdn rule create <zone_uuid> --name <n> --type <type> --match '<json>' --action '<json>'`

Match conditions (all optional; empty matches all traffic): `path_pattern`
(starts with `/`, `*` wildcard), `method` (list), `host`, `headers`,
`query_params`, `cookies` (objects), `country` (ISO codes), `ip_range` (list of
CIDRs), `user_agent_pattern`. Patterns only allow `A-Z a-z 0-9 . _ ~ : / @ % + = * -`:
no spaces (use `*`), quotes, braces or `#`.

| `--type` | `--action` |
|---|---|
| `cache` | `{"ttl": 86400, "browser_ttl": 3600}` (seconds; `browser_ttl` optional). Optional: `"cache_everything": true`, `"grace"`, `"stale_if_error"`, `"status_ttl"` |
| `cache_key` | `{"query": "none"}`. `query` is `all`, `none`, `allow` or `strip` (the last two need `"query_params": ["page", "utm_*"]`); optional `"vary_device": true` and `"vary_headers": ["Accept-Language"]` |
| `cache_bypass` | `{}` |
| `url_rewrite` | `{"path": {"mode": "prefix", "from": "/old/", "to": "/new/"}, "strip_query": ["utm_*"], "set_query": {"src": "cdn"}}`; `mode` is `exact`, `prefix` or `regex` |
| `redirect` | `{"to": "https://example.com/new", "status": 301}` (301, 302, 307, 308) |
| `header_request` / `header_response` | `{"name": "X-Frame-Options", "value": "DENY"}` (empty value removes the header) |

A redirect matches on `match_conditions.path_pattern`, which is required:
`{"path_pattern": "/old/*"}`. Redirecting a whole zone needs
`{"path_pattern": "/*"}` explicitly; `"/"` is the homepage only. Confirm
zone-wide redirects with the user.

```bash
cubecli cdn rule create <zone_uuid> --name static --type cache \
  --match '{"path_pattern": "/static/*"}' --action '{"ttl": 604800}'
```

Rules apply in `--priority` order (lower first, default 100).

Cache rule options:

- `cache_everything` also caches HTML, JSON and XML (by default they are not).
  Requests with an `Authorization` header and responses marked `private` or
  `no-store` or that set a cookie are never cached.
- `grace` (seconds, 0 to 2592000) serves an expired copy while the edge fetches
  a new one; `stale_if_error` (0, or at least twice `grace`) keeps serving it
  when the origin fails; `status_ttl` caches some statuses for a given time,
  `{"404": 60, "5xx": 5}` (301, 302, 307, 308, 404, 410, 451 up to 86400 s; 500,
  502, 503, 504, 5xx up to 300 s). They need a `ttl` above 0.
- A `cache_key` rule decides what makes a different cached copy: ignore or
  allow-list query parameters, split by device, or by up to 3 request headers
  (`Accept-Language`, `Accept`, `Origin`, `X-*`). At most one per zone without
  `--match`, and every one must use the same `vary_device`. **Adding, changing,
  disabling or deleting one empties the cache of the whole zone**: confirm with
  the user first and prefer a quiet moment. With `none` or `strip` the ignored
  parameters are also removed from the request to the origin; with `allow` the
  origin still gets the whole query string.
- A `url_rewrite` rule changes the path or query the origin receives, and the
  cache stores the object under the rewritten URL (two public URLs that rewrite
  to the same one share a copy). Redirects and firewall rules see the public
  URL. A purge by path names the rewritten path.

### Purge and settings

```bash
cubecli cdn cache purge <zone_uuid> /assets/app.css "/images/*"     # paths
cubecli cdn cache purge <zone_uuid> --tag news --tag product-42      # cache tags
cubecli cdn cache purge <zone_uuid> --host www.example.com           # one hostname
cubecli cdn cache purge <zone_uuid> --everything
cubecli cdn zone update <zone_uuid> --cache-tag-header Cache-Tag     # tag purges: the origin header with the tags
cubecli cdn zone update <zone_uuid> --compression                    # Brotli, Zstandard or gzip for text; off by default
```

Purge by tag needs the zone's cache tag header; files cached before it was set
have no tags, so purge everything once after setting or renaming it. Pass an
empty `--cache-tag-header ""` to turn tag purges off.

### WAF and limits

`cdn waf create <zone_uuid> --name <n> --type <type> --action '<json>' [--match '<json>']`

| `--type` | `--action` |
|---|---|
| `firewall_ip` | `{"block_ips": ["198.51.100.0/24"], "allow_ips": []}` |
| `firewall_country` | `{"block_countries": ["XX"]}` or `{"allow_countries": ["ES", "FR"]}` |
| `firewall_asn` | `{"block_asns": [13335, 15169]}` (client AS numbers, 1 to 4294967295; blocks only, no allow list) |
| `firewall_ua` | `{"block_patterns": ["BadBot*"]}` |
| `js_challenge` | `{"enabled": true}` |
| `rate_limit` | `{"requests": 100, "period": 60, "by": "ip"}` (`period` 1, 10 or 60; `by` `ip` or `ip_path`) |
| `limit_connections` | `{"max_connections": 20}` (concurrent requests per IP) |
| `limit_bandwidth` | `{"max_kbytes_per_sec": 5000}` (per IP, 10 s average; over it gets 429) |
| `limit_download_speed` | `{"speed": 2000}` (kB/s per response) |

- A zone can have at most 3 enabled `rate_limit`, 2 `limit_connections` and 2
  `limit_bandwidth` rules.
- Limits are counted per edge server, so a client may get somewhat more than
  the configured value.
- Unknown fields in limit actions are rejected (422). Rule validation errors
  return 422 with the offending field; fix it and retry.
- `allow_ips` and `allow_countries` mean only these: when not empty, a client
  that is not on the list gets 403 (they used to be ignored). The block list
  wins. In `allow_countries`, `XX` is a client of no known country, blocked
  unless `XX` is listed. An IPv6 client is not on a list of IPv4 addresses.
  Confirm an allow list with the user: it blocks everyone else.

### Metrics

```bash
cubecli cdn metrics summary <zone_uuid> --minutes 1440 --json
cubecli cdn metrics cache <zone_uuid> --json          # hit ratio
cubecli cdn metrics status-codes <zone_uuid> --json
cubecli cdn metrics top-urls <zone_uuid> --limit 20 --json
cubecli cdn metrics blocked <zone_uuid> --json        # WAF effect
```

Other breakdowns: `bandwidth`, `requests`, `pops`, `top-countries`, `top-asn`,
`top-user-agents`, `file-extensions`. For "the site is slow" or "costs are up",
start with `summary`, then `cache` and `top-urls`.
