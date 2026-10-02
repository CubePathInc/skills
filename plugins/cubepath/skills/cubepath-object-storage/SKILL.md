---
name: cubepath-object-storage
description: Manage CubePath Object Storage (S3 compatible) with cubecli - storage tiers and prices, buckets, versioning and deletion protection, Object Lock (immutable WORM buckets for backups and retention), bucket and object tags, access keys for AWS CLI, rclone, boto3 and other S3 clients, temporary share links (presigned URLs), serving a bucket publicly through the CubePath CDN, lifecycle rules that delete old objects or versions, replication of a bucket to another CubePath bucket or to an external S3 provider, bucket charts, monthly usage and cost, and usage or budget alerts. Use when the user wants S3 storage, a bucket, S3 credentials, to store backups or static files on CubePath, immutable or ransomware proof backups (Veeam, Kopia, restic), to share a file with a temporary link, to expire old files automatically, to copy a bucket continuously to another bucket or provider (off site backup), or to serve files from a bucket through a CDN.
---

# CubePath Object Storage

Follow the `cubepath-cli` skill first (session, profile, `--json`, confirmations).
Exact flags: [reference/objectstorage.md](reference/objectstorage.md).
`s3` is a short alias of the `objectstorage` command group.

## How it works

- Buckets live on a **tier**: `infrequent_access` (alias `ia`, HDD) today;
  `standard` (SSD) is coming later. Every tier of a region shares one endpoint:
  `https://eu.cubestorage.io`, S3 region `eu`. Path style
  (`https://eu.cubestorage.io/<bucket>/<key>`) and virtual host
  (`https://<bucket>.eu.cubestorage.io/<key>`) both work.
- Any S3 client works with an **access key** created here. There are no public
  buckets, no anonymous access and no static website hosting: public delivery
  is only through the CubePath CDN (see below).
- Billing is hourly, in arrears, per bucket: stored GiB-month, egress GiB,
  class A (writes, lists) and class B (reads) requests. The free tier is per
  organization, month and tier. Only projects billed hourly can hold buckets.
- Every bucket is **encrypted at rest** with AES-256 (SSE-S3), always on, at no
  cost (`encryption` in `bucket get --json`). SSE-KMS is not available; SSE-C
  (the client's own key in each request) works with any S3 client.

```bash
cubecli objectstorage tiers --json   # .[] | {slug, uuid, endpoint, region, prices, free_tier, accepting_new}
```

Show the user the prices and free tier from this output before creating
anything; never quote prices from memory.

## Create a bucket

Bucket names are 3 to 63 characters (lowercase letters, numbers, hyphens,
starting and ending with a letter or number) and **unique across all CubePath
customers**. Some names are reserved (anything containing `cubepath`, for
example); the API answers 400 for those.

1. Pick the project (see `cubepath-cli`) and the tier (`accepting_new` must be
   true).
2. Confirm name, tier, project and prices with the user (billable), then:

```bash
cubecli objectstorage bucket create photos --tier ia --project 882 --json
cubecli objectstorage bucket get photos --json | jq -r '.status'   # poll until active
```

- Creation takes 10 to 20 seconds (`pending` -> `active`). Uploads may answer
  503 for the first minutes of a new bucket; retry later.
- `--versioning` keeps every version of overwritten or deleted objects (all
  versions count as stored data).
- 409 `A bucket named ... already exists`: the name is taken by someone else;
  propose another one.
- 402 on the first bucket: the organization needs a minimum balance; the user
  tops up in the dashboard.

Buckets accept their name or uuid in every command.

## Access keys

The secret access key is returned **only once**, when the key is created.
Never print it in the conversation, never store it in your memory or notes,
and never read it back from a file. Write it straight into a file the user
chose with `--output`, which prints only the credentials to stdout:

```bash
cubecli objectstorage key create --name backups --tier ia --output env > .env
cubecli objectstorage key create --name laptop --tier ia --output rclone >> ~/.config/rclone/rclone.conf
cubecli objectstorage key create --name ci --tier ia --output aws >> ~/.aws/credentials
```

- `env`: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`,
  `AWS_ENDPOINT_URL` (read by the AWS CLI v2 and most SDKs).
- `rclone`: a remote named `cubepath-<key name>`.
- `aws`: a profile named `cubepath-<key name>` with `region` and `endpoint_url`.

After writing a credentials file, restrict it (`chmod 600 <file>`) and make sure
it is ignored by git when it is inside a repository.

Least privilege: prefer a key limited to the buckets it needs, read-only when
it only reads, and with an expiry for temporary access:

```bash
cubecli objectstorage key create --name web --tier ia --bucket photos \
  --permission read_only --expires-in 30d --output env > .env
```

Without `--bucket` the key reaches every bucket of that project and tier,
including buckets created later. Keys work once `status` is `active` (10 to 20
seconds): `cubecli objectstorage key list --json`.

A lost secret cannot be recovered: create a new key and delete the old one
(`cubecli objectstorage key delete <uuid|access key ID|name>`, confirm first).

## Using the bucket

With the endpoint and region from `tiers` (or `bucket get`):

```bash
aws s3 ls s3://photos --endpoint-url https://eu.cubestorage.io --region eu
aws s3 cp ./file.txt s3://photos/file.txt --endpoint-url https://eu.cubestorage.io --region eu
rclone copy ./backups cubepath-laptop:photos/backups
```

boto3: `boto3.client("s3", endpoint_url="https://eu.cubestorage.io",
region_name="eu")` with the credentials from the environment.

Limits worth knowing: 5 GiB per single PUT (larger files use multipart, 5 MiB
to 5 GiB parts, up to 10,000 parts); 1 TiB per bucket; presigned URLs last at
most 24 hours and must be SigV4; direct downloads are served as attachments;
browser uploads with CORS need path style URLs; incomplete multipart uploads
are always aborted 7 days after they start.

## Share a file

To give someone a temporary download link to one object, sign a presigned URL
with one of the user's access keys. It is signed locally: the secret is never
sent to CubePath or anywhere else.

```bash
# credentials from the environment (or --access-key / --secret-key)
cubecli objectstorage presign photos/2026/report.pdf --expires 6h --json   # {url, expires_at}
```

- At most 24 hours (`--expires 24h`); longer is refused. The receiver needs no
  account and no key.
- The file is always downloaded as an attachment, never shown inline: to serve
  files to the public, connect the bucket to the CDN (next section).
- Every download is egress of the bucket and a class B request, billed to the
  organization. Tell the user before sharing a large file widely.
- Revocation: the only way to cut a link before it expires is to delete the
  access key that signed it (which also breaks everything else using that key).
  Sign with a dedicated read-only key limited to the bucket when the user may
  want to revoke. The dashboard's "Revoke all links" only affects links created
  from the dashboard, not URLs signed with the user's own keys.
- Keys that start with `/` or contain `//` cannot be shared this way.
- `--endpoint https://eu.cubestorage.io --region eu` signs without a login.

## Serve a bucket publicly through the CDN

A bucket is served publicly by adding it as the **origin** of a CDN zone. The
CDN reads it with a read-only key it manages. A bucket can be the origin of one
zone at a time. The zone is billed like any CDN zone. Traffic from the bucket
to the CDN is not billed as egress, but the edges' requests count as class B
requests of the bucket.

Pick an existing zone (`cubecli cdn zone list --json`) or create one following
the `cubepath-dns-cdn` skill (confirm the plan and price first, it is billable),
then:

```bash
cubecli cdn origin create <zone_uuid> --name photos --bucket photos --json
cubecli objectstorage bucket get photos --json | jq '.cdn'   # status connecting -> connected
```

- `--bucket` takes the bucket's name or uuid and cannot be combined with
  `--url`, `--address`, `--port`, `--protocol` or `--host-header`: the API fills
  those in.
- Files are then public at `https://<zone>.cubecdn.io/<key>` (`.cdn.domain`),
  or on the zone's custom domain (see `cubepath-dns-cdn`).
- Cache rules, WAF and metrics of the zone work as usual.

To disconnect, delete that origin after the user confirms. The public URLs stop
working, but the zone **and its billing stay**:

```bash
cubecli objectstorage bucket get photos --json | jq '.cdn | {zone_uuid, origin_uuid}'
cubecli cdn origin delete <zone_uuid> <origin_uuid> --force
cubecli cdn zone delete <zone_uuid> --force   # only if the user wants the zone gone too
```

## Change a bucket

```bash
cubecli objectstorage bucket update photos --versioning enabled
cubecli objectstorage bucket update photos --protected          # deletion protection
cubecli objectstorage bucket update photos --protected=false
```

Versioning can be `enabled` or `suspended`, never turned back off. A bucket
never changes tier or project.

## Object Lock (immutable buckets)

Object Lock (WORM) keeps object **versions** from being deleted or overwritten
until their retention date. Use it for backups that ransomware or a leaked key
must not destroy, and for records that must be kept for a fixed time.

- It can **only be turned on when the bucket is created**, never later, and
  never turned off. A lock bucket always has versioning `enabled` (it cannot be
  suspended) and is created with deletion protection on.
- The user must accept the Object Lock terms (`--accept-object-lock-terms`).
  Ask them explicitly; never pass it on your own.
- Retention protects versions: a plain delete still works but only adds a
  delete marker, and every stored version keeps being billed until it can be
  deleted, also while the bucket is suspended or blocked.

Modes:

| Mode | Who can delete before the date | Use it for |
|---|---|---|
| `governance` | only keys created with `--bypass-governance`, sending `x-amz-bypass-governance-retention: true` | protection against mistakes and stolen keys, short retention (days) |
| `compliance` | **nobody**, CubePath included; the retention cannot be shortened or removed | legal or regulatory retention, immutable backups that must survive anyone |

Compliance is only available once support enables it for the organization
(otherwise 403 `Compliance mode is not enabled for your organization`). Before
a compliance rule, warn the user that the data and its cost cannot be removed
until every version expires; cubecli asks for confirmation unless `--yes`.

```bash
cubecli objectstorage bucket create backups --tier ia --object-lock \
  --lock-mode governance --lock-days 30 --accept-object-lock-terms --json
cubecli objectstorage bucket get backups --json | jq '.object_lock'   # {enabled, default_retention}
cubecli objectstorage bucket object-lock set backups --mode governance --days 14
cubecli objectstorage bucket object-lock set backups --remove
```

- The **default retention** (`--lock-mode` with `--lock-days` or
  `--lock-years`, at most 3650 days or 10 years) applies to every version that
  has no retention of its own, older versions included. It is set only with
  cubecli, the API or the dashboard: S3 `PutBucketObjectLockConfiguration` is
  denied.
- A governance rule can be changed or removed at any time. A compliance rule
  can only be kept or lengthened; turning compliance on or lengthening needs
  `--accept-object-lock-terms` again.
- Over S3, keys can read the lock configuration and retention, set retention
  on objects and put or lift legal holds (`PutObjectRetention`,
  `PutObjectLegalHold`). Read-only keys can only read them.

Keys that may remove governance locked versions (read_write only; it cannot be
changed on an existing key, create another):

```bash
cubecli objectstorage key create --name backup-admin --tier ia --bypass-governance --output env > .env
```

Keep the backup software's own key **without** bypass, so a compromised
backup server cannot delete its backups.

### Backup software

- **Without compliance enabled for the organization** the bucket's default
  retention protects everything, but software that sets a retention per object
  gets 403 on those uploads. Use a bucket default retention and turn off the
  software's own object lock or immutability option: restic and plain
  `aws s3`/rclone uploads work this way.
- **Veeam Backup & Replication** (12 or later): create the bucket with
  `--object-lock` (default retention optional), a read_write key without
  bypass, and add it as an S3 compatible repository with endpoint
  `https://eu.cubestorage.io`, region `eu`, ticking "Make recent backups
  immutable". Veeam sets compliance retention on each object, so it needs
  compliance enabled for the organization; ask support first.
- **Kopia**: `kopia repository create s3 --endpoint eu.cubestorage.io --region eu
  --bucket backups --retention-mode COMPLIANCE --retention-period 720h ...`
  also sets per object retention, so it needs compliance enabled. Without it,
  create the repository without `--retention-mode` and rely on the bucket's
  default retention.
- Old versions accumulate (there are no lifecycle rules for customers); the
  backup tool's own maintenance removes them once their retention ends, and
  they are billed until then.

## Tags

Bucket tags are `key=value` labels to organize buckets and filter lists and
usage (by environment, team, customer...). They are free.

```bash
cubecli objectstorage bucket create logs --tier ia --tag env=prod --tag team=data --json
cubecli objectstorage bucket list --tag env=prod --tag team --json   # key=value or just key; all must match
cubecli objectstorage usage --tag team=data --json                   # cost of those buckets
cubecli objectstorage bucket update logs --tag env=prod --tag team=web
cubecli objectstorage bucket update logs --clear-tags
```

- `bucket update --tag` **replaces every tag**: to add one, read the current
  ones first (`bucket get logs --json | jq '.tags'`) and pass them all again.
- Rules: at most 50 tags per bucket; keys 1 to 128 characters, values 0 to 256;
  letters, numbers, spaces and `_ . : / = + - @`. Keys cannot contain `=`,
  start or end with a space, or start with `aws:`, `cp:` or `cubepath:`. A
  list filter takes at most 10 `--tag`.
- Bucket tags are CubePath metadata, not S3: `GetBucketTagging` and
  `PutBucketTagging` answer 403 (for example Terraform's `aws_s3_bucket_tagging`).
  Use cubecli, the API, the dashboard or the `tags` of the CubePath Terraform
  and Ansible bucket resources.

### Object tags

Objects take standard S3 object tagging (up to 10 tags per object) with any S3
client, for example to classify files:

```bash
aws s3api put-object-tagging --bucket logs --key 2026/09/app.log.gz \
  --tagging 'TagSet=[{Key=class,Value=archive},{Key=team,Value=data}]' \
  --endpoint-url https://eu.cubestorage.io --region eu
aws s3api get-object-tagging --bucket logs --key 2026/09/app.log.gz \
  --endpoint-url https://eu.cubestorage.io --region eu
aws s3api put-object --bucket logs --key report.pdf --body ./report.pdf \
  --tagging 'class=archive' --endpoint-url https://eu.cubestorage.io --region eu
```

boto3: `put_object(..., Tagging="class=archive&team=data")` or
`put_object_tagging(...)`. Put object tagging counts as a class A request, get
as class B, and delete is free. A read-only key can read object tags but not
change them.

## Lifecycle rules

Lifecycle rules delete objects in the background, **permanently**: current
objects after N days or on a date, noncurrent versions of a versioned bucket,
delete markers left without versions, incomplete multipart uploads. Confirm
with the user before setting or changing rules, especially one that covers the
whole bucket with few days.

- Rules are set with cubecli or the API only (S3
  `PutBucketLifecycleConfiguration` answers 403; reading them with S3 works).
- `set` **replaces every rule** of the bucket: read them first with `get`.
- Applying takes seconds, up to about 12 minutes after a previous change of the same
  bucket (`--wait` blocks until applied). Objects then go within 48 hours of
  their due date and are billed until they are gone.
- In a **versioned** bucket an expiration only adds a delete marker and the old
  version keeps being billed: add a `noncurrent_version_expiration` rule.
- On a bucket with Object Lock, rules never remove versions still under
  retention. While a bucket is blocked or on hold the rules are paused.

```bash
cubecli objectstorage bucket lifecycle get photos --json
cubecli objectstorage bucket lifecycle set logs --expire-days 30 --prefix logs/ --wait
cubecli objectstorage bucket lifecycle set photos --file rules.json --wait   # or --file - (stdin)
cubecli objectstorage bucket lifecycle delete photos --force                  # after the user confirms
```

`rules.json` (up to 100 rules; IDs of letters, numbers, `.`, `-`, `_`):

```json
{"rules": [
  {"id": "tmp-7d", "enabled": true, "filter": {"prefix": "tmp/"}, "expiration": {"days": 7}},
  {"id": "old-versions", "enabled": true,
   "noncurrent_version_expiration": {"noncurrent_days": 30, "newer_noncurrent_versions": 3}},
  {"id": "markers", "enabled": true, "expiration": {"expired_object_delete_marker": true}},
  {"id": "uploads", "enabled": true, "abort_incomplete_multipart_upload": {"days_after_initiation": 2}}
]}
```

Other expirations: `{"date": "2027-01-01"}` (after today, UTC). Filters can
also take `tags` (`[{"key": "class", "value": "temp"}]`, up to 10),
`object_size_greater_than` and `object_size_less_than` (bytes).

## Replication

Replication copies every new object version of a bucket to one destination,
asynchronously. Details, filters, health and grants:
[replication.md](replication.md).

- **CubePath destination** (a bucket of the same tier): no egress, the copy is
  billed as storage of the destination bucket. It is in the same location as
  the source: **not disaster recovery**.
- **External destination** (AWS S3, Wasabi, any S3 compatible provider): the
  off site option. Everything sent is **egress of the source bucket** at the
  tier price, initial copy and resyncs included. Public **HTTPS on port 443
  only** (a host name, no IP, no other port).
- **Versioning must be `enabled`** on the source and the destination. **Buckets
  with Object Lock cannot be sources** (a locked destination is fine).
- Another organization's bucket needs a one use **grant** from its owner
  (`replication grant create`); the token is shown once.

Confirm destination and cost with the user first. The external secret never
goes on the command line (`--secret-key-stdin` or `CUBEPATH_REPL_SECRET`):

```bash
cubecli objectstorage replication create photos --dest-bucket photos-copy --json
printf '%s' "$AWS_SECRET" | cubecli objectstorage replication create photos --external --provider aws \
  --endpoint s3.eu-west-1.amazonaws.com --region eu-west-1 --bucket acme-photos-backup \
  --access-key AKIA... --secret-key-stdin
cubecli objectstorage replication get photos --json   # .status pending -> active; .health; .backfill
```

## Usage and cost

```bash
cubecli objectstorage usage --json                      # current month
cubecli objectstorage usage --period 2026-08 --json     # up to 12 months back
cubecli objectstorage bucket list --json                # .[] | {name, size_bytes, objects_count, monthly_charges}
```

`usage` gives per tier and per bucket: `storage_gib_month`, `egress_bytes`,
`cdn_bytes`, class A/B requests, `cost` (already charged) and `projected_cost`
(end of month), plus free tier consumption. With `metrics_available: false` the
quantities are null but the costs are right. Sizes are refreshed every 15
minutes.

## Charts of one bucket

```bash
cubecli objectstorage bucket metrics photos --range 24h               # table: latest size, totals of the range
cubecli objectstorage bucket metrics photos --range 7d --part traffic --json
```

`--range` is 1h, 3h, 6h, 12h, 24h, 3d, 7d or 30d; `--part` any of `storage`,
`traffic`, `responses` (default all). `--json` prints every point:
`storage` (`size_bytes`, `objects`, hourly, `storageMeasuredAt` = newest size
sample), `traffic` (`egress_bytes`, `cdn_bytes`, `ingress_bytes`,
`class_a_requests`, `class_b_requests`, `free_requests`: only the project's
keys, status 2xx or 304, like the invoice) and `responses` (`responses_2xx` ...
`responses_5xx`, `responses_429`, `responses_other`: every caller, anonymous
included). Traffic and responses are totals per step (5 minutes up to 7 days,
1 hour beyond), not rates; the monthly free tier is not subtracted. It reads the
GraphQL API, which needs an API token (`CUBE_API_TOKEN=<token>`), not a browser
login.

Example, "how much egress did my bucket do yesterday?": run
`cubecli objectstorage bucket metrics photos --range 3d --part traffic --json`
and sum the `egress_bytes` points whose `ts` falls inside yesterday (UTC);
`cdn_bytes` is traffic to the CDN, not billed as egress.

## Alerts

Usage alerts notify an email, Slack or Discord channel when a bucket or the
organization's Object Storage crosses a threshold. cubecli has no alert
commands: they are managed from the dashboard, Terraform
(`cubepath_alert_rule`), Ansible (`cubepathinc.cloud.cloud_alert`) or the
CubePath MCP server (`cubepath_alert_list`, `cubepath_alert_set`).

- Bucket (`target_type` `object_storage_bucket`, target the bucket uuid, created
  in the bucket's project): `storage_size_gb`, `storage_egress_gb_month`,
  `storage_error_rate_5xx` and `storage_error_rate_403` (percent of requests
  over the last 5 minutes, needs at least 20 requests).
- Organization (`target_type` `organization`, target the organization ID, still
  attached to a project): `storage_cost_month` (USD billed so far this month,
  about an hour behind billing) and `storage_egress_gb_month` (GiB this month,
  before the free tier).
- Monthly metrics only take `gt`/`gte`, notify once per month and reset on the
  1st (UTC). Up to 50 alerts per organization. Alerts are free.

A monthly budget (for example `storage_cost_month` `gte` 50) is the usual
answer to "warn me before Object Storage costs too much".

## Delete a bucket

Deleting is irreversible. Before asking the user, show the bucket's name, size
and object count (`bucket get`).

1. A protected bucket must be unprotected first (`--protected=false`).
2. A bucket connected to the CDN must be disconnected first (delete its CDN origin).
3. Then, after explicit confirmation:

```bash
cubecli objectstorage bucket delete photos --force            # only if empty
cubecli objectstorage bucket delete photos --purge --force    # deletes every object and version too
```

- Without `--purge`, a bucket that is not empty stays `active` with an error
  message; that is expected. Only use `--purge` when the user explicitly agreed
  to lose the content.
- `--force` only skips the confirmation prompt; `--purge` is what deletes data.
- Large buckets stay `deleting` for a while. The name stays reserved for the
  organization for 90 days.

With Object Lock, versions still under retention or legal hold are never
deleted, not even with `--purge`. The bucket comes back with
`locked_content_kept: true` and an error message, keeps being billed for what
is left, and cannot be deleted (nor its project) until that retention ends;
then delete it again. To also remove versions under governance retention:

```bash
cubecli objectstorage bucket delete backups --purge --bypass-governance --force
```

Compliance versions and legal holds are always kept until they expire.

A project with buckets or access keys cannot be deleted until they are.

## Errors

| Message | What to do |
|---|---|
| `Object Storage is not available for your organization yet.` | Not enabled for this organization; the user contacts support. |
| `Object Storage is only available in projects billed hourly.` | Use (or create) a project billed hourly. |
| `The ... tier is not accepting new buckets right now.` | Try later or another tier; existing buckets keep working. |
| `Bucket limit reached (...)` / `Access key limit reached (...)` | Delete unused ones or ask support. |
| `The bucket is busy with another operation.` (409) | Wait for `pending` or `deleting` to finish, then retry. |
| `This bucket has been blocked by CubePath.` | Abuse or policy block; the user contacts support. |
| `Object Lock is not enabled on this bucket. It can only be enabled when the bucket is created.` | Create a new bucket with `--object-lock` and copy the data. |
| `Compliance mode is not enabled for your organization.` | Use `governance`, or the user asks support to enable compliance. |
| `A compliance default retention cannot be removed or shortened.` | Expected: compliance can only be kept or lengthened. |
| `Some objects are still protected by Object Lock ...` | The delete kept locked versions; delete again when their retention ends. |
| S3 403 on an upload with object lock headers, or `AccessDenied` deleting a version | Compliance not enabled (per object retention), or the version is under retention: see "Object Lock". |
| `Enable versioning on bucket '...' before replicating it.` | Turn versioning on (`bucket update --versioning enabled`) on the source, and on the destination for the destination message. |
| `Buckets with Object Lock cannot be replication sources.` | Expected: replicate from a bucket without Object Lock. |
| `The destination endpoint is not allowed. ...` | Use the provider's public HTTPS host name on port 443, not an IP, a private name or another port. |
| `The replication grant is invalid or has expired. ...` | Ask the destination owner for a new grant. |
| `Bucket '...' already replicates to another destination. ...` | One destination per bucket: delete the current replication first. |
| 403 on a write | The session lacks `object_storage:write` (or `cdn:write` for the CDN commands; adding a bucket as a CDN origin needs both): log in again granting write access. |
| S3 `InvalidRequest` on upload | Bucket quota (1 TiB) reached or the key expired. |
