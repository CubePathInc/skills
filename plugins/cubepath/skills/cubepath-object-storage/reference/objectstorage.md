# cubecli objectstorage

Manage Object Storage buckets and access keys (S3 compatible)

## `cubecli objectstorage bucket create`

Create a bucket (billed hourly while it exists)

Create a bucket. Names are 3 to 63 characters of lowercase letters, numbers
and hyphens, and are unique across all CubePath customers.

The bucket is created asynchronously: it is usable once its status is active
(usually 10 to 20 seconds). Uploads may answer 503 for the first minutes.

Tags are labels to organize and filter buckets (at most 50; key up to 128 and
value up to 256 characters). They are managed with cubecli, the API and the
dashboard only: S3 bucket tagging calls are not supported.

--object-lock creates the bucket with Object Lock (WORM): object versions cannot
be deleted or overwritten until their retention date. It can only be turned on
now, never later, and implies versioning and deletion protection. It needs
--accept-object-lock-terms. An optional default retention applies to every new
version:

  governance  keys created with --bypass-governance can still delete
  compliance  nobody can delete or shorten it before its date, CubePath included
              (asks for confirmation unless --yes)

Usage: `cubecli objectstorage bucket create <name> [flags]`

- `--accept-object-lock-terms`: Accept the Object Lock terms (required with --object-lock)
- `--lock-days int`: Default retention in days
- `--lock-mode string`: Default retention mode: governance or compliance
- `--lock-years int`: Default retention in years
- `--object-lock`: Create the bucket with Object Lock (only possible now, never later)
- `--tag stringArray`: Tag as key=value (repeatable)
- `--tier string`: Storage tier: slug, uuid or ia (see 'objectstorage tiers') (required)
- `--versioning`: Enable object versioning
- `-p, --project int`: Project ID (default: the organization's first project)
- `-y, --yes`: Skip the compliance confirmation prompt

Examples:

```
  cubecli objectstorage bucket create photos --tier ia
  cubecli s3 bucket create backups --tier infrequent_access --project 12 --versioning
  cubecli s3 bucket create logs --tier ia --tag env=prod --tag team=data
  cubecli s3 bucket create veeam --tier ia --object-lock --accept-object-lock-terms
  cubecli s3 bucket create archive --tier ia --object-lock --lock-mode governance --lock-days 30 --accept-object-lock-terms
```

## `cubecli objectstorage bucket delete`

Delete a bucket

Delete a bucket. Without --purge only an empty bucket is deleted; otherwise
the bucket stays active and shows the error. With --purge every object, version
and pending upload is deleted first, which cannot be undone.

On a bucket with Object Lock, versions still under retention or legal hold are
kept: the bucket stays with "Locked content kept" until their retention ends,
and keeps being billed. --bypass-governance (with --purge) also deletes the
versions under governance retention; compliance versions can never be deleted
early.

The bucket name stays reserved for your organization for 90 days.

Usage: `cubecli objectstorage bucket delete <bucket> [flags]`

- `--bypass-governance`: With --purge on a bucket with Object Lock: also delete versions under governance retention
- `--purge`: Also delete every object and version in the bucket (the API's force delete)
- `-f, --force`: Skip confirmation prompt

## `cubecli objectstorage bucket get`

Show a bucket with its connection details, month usage and CDN status

Usage: `cubecli objectstorage bucket get <bucket>`

Aliases: show

## `cubecli objectstorage bucket lifecycle delete`

Remove every lifecycle rule of a bucket

Remove every lifecycle rule of a bucket: nothing is deleted by rules from then on.
Incomplete multipart uploads are still aborted after 7 days.

Usage: `cubecli objectstorage bucket lifecycle delete <bucket> [flags]`

- `--wait-timeout duration`: With --wait: give up after this long (default 15m0s)
- `--wait`: Wait until the rules are applied
- `-f, --force`: Skip confirmation prompt

## `cubecli objectstorage bucket lifecycle get`

Show a bucket's lifecycle rules and whether they are applied

Usage: `cubecli objectstorage bucket lifecycle get <bucket>`

## `cubecli objectstorage bucket lifecycle set`

Replace every lifecycle rule of a bucket

Replace every lifecycle rule of a bucket, from a JSON file (--file rules.json, or
--file - for stdin) or, for the common case, one expiration rule built from flags:

  cubecli s3 bucket lifecycle set logs --expire-days 30 --prefix logs/

Rule format: {"id": "logs-30d", "enabled": true, "filter": {"prefix": "logs/"},
"expiration": {"days": 30}}. Also "expiration": {"date": "2027-01-01"} or
{"expired_object_delete_marker": true}, "noncurrent_version_expiration":
{"noncurrent_days": 30, "newer_noncurrent_versions": 3} and
"abort_incomplete_multipart_upload": {"days_after_initiation": 2}. Up to 100 rules.

Expiration rules delete objects permanently. --wait returns once the rules are applied.

Usage: `cubecli objectstorage bucket lifecycle set <bucket> [flags]`

- `--expire-days int`: Build one rule that deletes objects this many days after they are written
- `--file string`: JSON file with the rules ({"rules": [...]} or [...]); - reads stdin
- `--id string`: With --expire-days: the rule ID (default expire-<days>d)
- `--prefix string`: With --expire-days: only objects whose key starts with this prefix
- `--wait-timeout duration`: With --wait: give up after this long (default 15m0s)
- `--wait`: Wait until the rules are applied
- `-f, --force`: Skip confirmation prompt

## `cubecli objectstorage bucket list`

List buckets

Usage: `cubecli objectstorage bucket list [flags]`

- `--tag stringArray`: Only buckets with this tag: key (any value) or key=value (repeatable, all must match, up to 10)
- `--tier string`: Only buckets of this tier (slug, uuid or ia)
- `-p, --project int`: Only buckets of this project ID

Examples:

```
  cubecli s3 bucket list --tag env=prod --tag team
```

## `cubecli objectstorage bucket metrics`

Show a bucket's stored size, traffic and responses over a time range

Show the charts of a bucket: stored size and objects (hourly, the value billing
uses), billable traffic (egress, CDN, ingress, class A, class B and free requests of
the project's keys) and every response by status class.

Traffic and responses are totals per step, not rates; the table shows their sum over
the range and the stored size its latest value. --json prints every point.

Usage: `cubecli objectstorage bucket metrics <bucket> [flags]`

- `--part string`: Comma separated parts: storage, traffic, responses (default: all)
- `--range string`: Time range: 1h, 3h, 6h, 12h, 24h, 3d, 7d or 30d (default 24h)

## `cubecli objectstorage bucket object-lock set`

Set or remove the default retention of a bucket with Object Lock

Set or remove the default retention of a bucket created with Object Lock.

A governance rule can be changed or removed at any time. A compliance rule can
only be kept or lengthened: it cannot be removed, shortened or turned into
governance. Turning compliance on or lengthening the retention requires
--accept-object-lock-terms.

Usage: `cubecli objectstorage bucket object-lock set <bucket> [flags]`

- `--accept-object-lock-terms`: Accept the Object Lock terms (needed to turn compliance on or lengthen the retention)
- `--days int`: Retention in days
- `--mode string`: governance or compliance
- `--remove`: Remove the default retention (not possible for compliance)
- `--years int`: Retention in years
- `-y, --yes`: Skip the compliance confirmation prompt

Examples:

```
  cubecli s3 bucket object-lock set backups --mode governance --days 30 --accept-object-lock-terms
  cubecli s3 bucket object-lock set archive --mode compliance --years 7 --accept-object-lock-terms --yes
  cubecli s3 bucket object-lock set backups --remove
```

## `cubecli objectstorage bucket update`

Change a bucket's versioning, deletion protection or tags

Change a bucket's versioning, deletion protection or tags.

--tag replaces every tag of the bucket with the ones given; --clear-tags
removes them all. Tags not given are not kept.

Usage: `cubecli objectstorage bucket update <bucket> [flags]`

- `--clear-tags`: Remove every tag of the bucket
- `--protected`: Deletion protection: --protected or --protected=false
- `--tag stringArray`: Tag as key=value (repeatable); replaces every tag of the bucket
- `--versioning string`: enabled or suspended (versioning cannot be turned off once enabled)

Examples:

```
  cubecli s3 bucket update photos --versioning enabled
  cubecli s3 bucket update photos --protected=false
  cubecli s3 bucket update photos --tag env=prod --tag team=web
  cubecli s3 bucket update photos --clear-tags
```

## `cubecli objectstorage key create`

Create an access key; the secret is shown only once

Create an access key for S3 clients. The secret access key is returned only
once: save it right away. The key works once its status is active (usually 10
to 20 seconds).

Without --bucket the key reaches every bucket of the project in that tier,
present and future. --output prints ready-to-use credentials:

  env     .env file with the standard AWS_* variables
  rclone  rclone.conf remote
  aws     ~/.aws/credentials profile (with region and endpoint_url)

--bypass-governance (read_write keys only) lets the key delete versions under
governance retention in buckets with Object Lock, sending the
x-amz-bypass-governance-retention header. It cannot be changed later.

Usage: `cubecli objectstorage key create [flags]`

- `--bucket stringSlice`: Limit the key to these buckets (name or uuid, repeatable; default: every bucket)
- `--bypass-governance`: Allow deleting versions under governance retention (read_write keys only)
- `--expires-at string`: Expiry time, UTC (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS, or RFC 3339)
- `--expires-in string`: Expiry from now: a duration such as 720h or 30d
- `--permission string`: read_write or read_only (default read_write)
- `--tier string`: Storage tier: slug, uuid or ia (required)
- `-n, --name string`: Key name (required)
- `-o, --output string`: Print the credentials as env, rclone or aws
- `-p, --project int`: Project ID (default: the organization's first project)

Examples:

```
  cubecli s3 key create --name backups --tier ia
  cubecli s3 key create --name web --tier ia --bucket photos --permission read_only --output env > .env.cubepath-storage
  cubecli s3 key create --name nightly --tier ia --expires-in 720h --output rclone >> ~/.config/rclone/rclone.conf
```

## `cubecli objectstorage key delete`

Revoke an access key (uuid, access key ID or name)

Usage: `cubecli objectstorage key delete <key> [flags]`

- `-f, --force`: Skip confirmation prompt

## `cubecli objectstorage key list`

List access keys (secrets are never shown again)

Usage: `cubecli objectstorage key list [flags]`

- `--tier string`: Only keys of this tier (slug, uuid or ia)
- `-p, --project int`: Only keys of this project ID

## `cubecli objectstorage presign`

Create a temporary download link for an object, signed locally

Create a presigned GET URL for one object. It is signed on this machine with
an access key of yours: the secret is never sent anywhere.

Anyone with the URL can download the object until it expires (at most 24 hours).
The file is always downloaded as an attachment, and every download counts as
egress of the bucket. To cut every URL signed with a key before it expires,
delete that access key.

Credentials come from --access-key/--secret-key or the AWS_ACCESS_KEY_ID and
AWS_SECRET_ACCESS_KEY environment variables (preferred: flags end up in the
shell history). The endpoint and region come from the bucket's tier, which
needs a logged-in profile; with --endpoint the command works offline.

Usage: `cubecli objectstorage presign <bucket>/<key> [flags]`

- `--access-key string`: Access key ID (default: $AWS_ACCESS_KEY_ID)
- `--endpoint string`: S3 endpoint URL; skips the API lookup, so no login is needed
- `--expires duration`: How long the URL works, as a Go duration (1m, 6h, 24h); at most 24h (default 1h0m0s)
- `--region string`: Signing region (default: the tier's region, or eu with --endpoint)
- `--secret-key string`: Secret access key (default: $AWS_SECRET_ACCESS_KEY)
- `--tier string`: Tier of the bucket (slug, uuid or ia); default: the bucket's tier

Examples:

```
  AWS_ACCESS_KEY_ID=CP... AWS_SECRET_ACCESS_KEY=... cubecli s3 presign photos/2026/report.pdf --expires 1h
  cubecli s3 presign backups/db.sql.gz --expires 24h --tier ia --json
  cubecli s3 presign photos/a.txt --endpoint https://eu.cubestorage.io --region eu
```

## `cubecli objectstorage tiers`

List storage tiers with endpoint, prices and free tier

Usage: `cubecli objectstorage tiers`

## `cubecli objectstorage usage`

Show the month's Object Storage usage and cost per tier and bucket

Usage: `cubecli objectstorage usage [flags]`

- `--period string`: Month as YYYY-MM (default: current month, up to 12 months back)
- `--tag stringArray`: Only buckets with this tag: key (any value) or key=value (repeatable, all must match, up to 10)
- `--tier string`: Only this tier (slug, uuid or ia)
- `-p, --project int`: Only buckets of this project ID
