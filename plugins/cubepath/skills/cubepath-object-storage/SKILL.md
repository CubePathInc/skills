---
name: cubepath-object-storage
description: Manage CubePath Object Storage (S3 compatible) with cubecli - storage tiers and prices, buckets, versioning and deletion protection, bucket and object tags, access keys for AWS CLI, rclone, boto3 and other S3 clients, temporary share links (presigned URLs), serving a bucket publicly through the CubePath CDN, and monthly usage and cost. Use when the user wants S3 storage, a bucket, S3 credentials, to store backups or static files on CubePath, to share a file with a temporary link, or to serve files from a bucket through a CDN.
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
are aborted after 7 days.

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
| 403 on a write | The session lacks `object_storage:write` (or `cdn:write` for the CDN commands; adding a bucket as a CDN origin needs both): log in again granting write access. |
| S3 `InvalidRequest` on upload | Bucket quota (1 TiB) reached or the key expired. |
