# Object Storage replication

Follow the `cubepath-cli` skill first (session, profile, `--json`, confirmations).
Exact flags: [reference/objectstorage.md](reference/objectstorage.md).

Replication copies every new object version of a **source** bucket to one
destination, asynchronously, object by object (usually within seconds or
minutes). Two kinds of destination:

| Destination | Use it for | Cost |
|---|---|---|
| **CubePath bucket** (same tier; same organization, or another one with a grant) | a second copy for another team or organization, a separate access scope, a copy that survives a deleted bucket | no egress; the copies are billed as storage of the destination bucket |
| **External** S3 compatible bucket (AWS S3, Wasabi, another provider) | an **off site** copy, disaster recovery | everything sent is **egress of the source bucket** at the tier price (shares the monthly free egress), initial copy and resyncs included |

A CubePath destination is in the same location as the source: it is **not
disaster recovery**. When the user wants a copy that survives a problem at
CubePath, recommend an external destination and tell them about the egress.

Rules before creating one:

- **Versioning must be `enabled`** on the source and on the destination
  (`bucket update <bucket> --versioning enabled`; also on the external
  provider's bucket). It cannot be suspended while the bucket replicates.
- **Buckets with Object Lock cannot be sources.** A destination with Object
  Lock is fine (the copies take its default retention).
- One destination per source bucket; a bucket cannot be a source and a
  destination at once; at most 10 replications per organization and 5 into one
  destination bucket.
- External endpoints: public **HTTPS on port 443 only** (a host name such as
  `s3.eu-west-1.amazonaws.com`, optionally with `:443`; no scheme, no IP
  address, no other port). `*.cubestorage.io` is refused: use a CubePath
  destination instead.
- What is copied: new versions, metadata and object tags. Delete markers only
  with `--delete-markers`, deletes of a specific version only with `--deletes`
  (leave both off for a backup that protects against deletions). Never bucket
  settings (lifecycle, Object Lock, bucket tags) nor objects encrypted with
  SSE-KMS.

Confirm destination, filter and (for external destinations) the egress cost
with the user, then:

```bash
cubecli objectstorage replication create photos --dest-bucket photos-copy --json
cubecli objectstorage replication create photos --dest-bucket photos-copy --prefix img/ --no-existing-objects
printf '%s' "$AWS_SECRET" | cubecli objectstorage replication create photos --external --provider aws \
  --endpoint s3.eu-west-1.amazonaws.com --region eu-west-1 --bucket acme-photos-backup \
  --access-key AKIA... --secret-key-stdin
cubecli objectstorage replication get photos --json   # .status pending -> active; .health; .backfill
```

- The external **secret access key never goes on the command line**: pipe it
  with `--secret-key-stdin` or set `CUBEPATH_REPL_SECRET`. It is never shown
  again. The external key needs write access to that bucket only.
- By default the objects already in the bucket are copied too (the backfill,
  `.backfill.status` `queued` -> `running` -> `completed`); large buckets take
  hours. `--no-existing-objects` copies only new writes.
- Filters: `--prefix` or `--tag key=value` (repeatable, all must match), not
  both; `--delete-markers` cannot be combined with `--tag`.
- `health`: `ok`, `lagging` (queue growing), `failing` (see `health_reason`,
  for example `credentials rejected` or `destination suspended`), `unknown`
  (no measurement yet). `status` `error`: configuration failed, see
  `error_message`; delete and create it again.

Change, pause, resend, remove (the replication's uuid or the source bucket's
name):

```bash
cubecli objectstorage replication list --json                        # outgoing and incoming
cubecli objectstorage replication update photos --enabled=false      # pause; --enabled resumes
cubecli objectstorage replication update photos --prefix img/        # replaces the filter; --clear-filter removes it
printf '%s' "$NEW_SECRET" | cubecli objectstorage replication update photos --rotate-credentials --access-key AKIA... --secret-key-stdin
cubecli objectstorage replication resync photos --older-than-days 3  # copy existing objects again
cubecli objectstorage replication delete photos --force              # after the user confirms
```

- A resync sends the existing objects again (to an external destination that
  is egress again). Use it after the destination was unavailable.
- Deleting a replication keeps everything already copied in the destination.
- `pause_reason` `org`, `abuse`, `admin` or `source_blocked`: paused by
  CubePath; the user contacts support.

## Replicate into a bucket of another organization

The owner of the destination bucket creates a **grant** and sends the token to
the source organization. Grants are one use, expire (7 days by default, 1 to
30) and can be revoked until used. Inside one organization no grant is needed.

```bash
# destination organization
cubecli objectstorage replication grant create photos-backup --note "for Acme" --expires-in-days 3
cubecli objectstorage replication grant list photos-backup --json     # status open/used/expired/revoked
cubecli objectstorage replication grant delete <grant_uuid> --force   # revoke an unused grant
# source organization
cubecli objectstorage replication create photos --dest-bucket <destination bucket uuid> --grant-token cprg_...
```

The token is shown only once: pass it to the other organization through a
private channel and never store it in notes. The destination owner sees the
replication in `replication list --direction incoming` and can stop it at any
time with `cubecli objectstorage replication revoke <uuid>` (confirm first; the source
owner then can only delete it and ask for a new grant).
