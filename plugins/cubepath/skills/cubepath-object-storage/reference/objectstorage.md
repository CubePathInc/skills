# cubecli objectstorage

Manage Object Storage buckets and access keys (S3 compatible)

## `cubecli objectstorage bucket create`

Create a bucket (billed hourly while it exists)

Create a bucket. Names are 3 to 63 characters of lowercase letters, numbers
and hyphens, and are unique across all CubePath customers.

The bucket is created asynchronously: it is usable once its status is active
(usually 10 to 20 seconds). Uploads may answer 503 for the first minutes.

Usage: `cubecli objectstorage bucket create <name> [flags]`

- `--tier string`: Storage tier: slug, uuid or ia (see 'objectstorage tiers') (required)
- `--versioning`: Enable object versioning
- `-p, --project int`: Project ID (default: the organization's first project)

Examples:

```
  cubecli objectstorage bucket create photos --tier ia
  cubecli s3 bucket create backups --tier infrequent_access --project 12 --versioning
```

## `cubecli objectstorage bucket delete`

Delete a bucket

Delete a bucket. Without --purge only an empty bucket is deleted; otherwise
the bucket stays active and shows the error. With --purge every object, version
and pending upload is deleted first, which cannot be undone.

The bucket name stays reserved for your organization for 90 days.

Usage: `cubecli objectstorage bucket delete <bucket> [flags]`

- `--purge`: Also delete every object and version in the bucket (the API's force delete)
- `-f, --force`: Skip confirmation prompt

## `cubecli objectstorage bucket get`

Show a bucket with its connection details, month usage and CDN status

Usage: `cubecli objectstorage bucket get <bucket>`

Aliases: show

## `cubecli objectstorage bucket list`

List buckets

Usage: `cubecli objectstorage bucket list [flags]`

- `--tier string`: Only buckets of this tier (slug, uuid or ia)
- `-p, --project int`: Only buckets of this project ID

## `cubecli objectstorage bucket update`

Change a bucket's versioning or deletion protection

Usage: `cubecli objectstorage bucket update <bucket> [flags]`

- `--protected`: Deletion protection: --protected or --protected=false
- `--versioning string`: enabled or suspended (versioning cannot be turned off once enabled)

Examples:

```
  cubecli s3 bucket update photos --versioning enabled
  cubecli s3 bucket update photos --protected=false
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

Usage: `cubecli objectstorage key create [flags]`

- `--bucket stringSlice`: Limit the key to these buckets (name or uuid, repeatable; default: every bucket)
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
- `--tier string`: Only this tier (slug, uuid or ia)
- `-p, --project int`: Only buckets of this project ID
