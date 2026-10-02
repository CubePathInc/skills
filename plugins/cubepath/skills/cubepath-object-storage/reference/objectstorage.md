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

Usage: `cubecli objectstorage bucket create <name> [flags]`

- `--tag stringArray`: Tag as key=value (repeatable)
- `--tier string`: Storage tier: slug, uuid or ia (see 'objectstorage tiers') (required)
- `--versioning`: Enable object versioning
- `-p, --project int`: Project ID (default: the organization's first project)

Examples:

```
  cubecli objectstorage bucket create photos --tier ia
  cubecli s3 bucket create backups --tier infrequent_access --project 12 --versioning
  cubecli s3 bucket create logs --tier ia --tag env=prod --tag team=data
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

- `--tag stringArray`: Only buckets with this tag: key (any value) or key=value (repeatable, all must match, up to 10)
- `--tier string`: Only buckets of this tier (slug, uuid or ia)
- `-p, --project int`: Only buckets of this project ID

Examples:

```
  cubecli s3 bucket list --tag env=prod --tag team
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
