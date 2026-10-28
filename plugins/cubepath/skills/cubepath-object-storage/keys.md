# Edit an Object Storage access key

Follow the `cubepath-cli` skill first (session, profile, `--json`, confirmations).
Exact flags: [reference/objectstorage.md](reference/objectstorage.md).

To change what a key may do, edit it instead of revoking and recreating it:
the access key ID and the secret stay the same, so clients keep working.
Only the flags given are changed:

```bash
cubecli objectstorage key update web --name website
cubecli objectstorage key update web --permission read_only
cubecli objectstorage key update web --bucket photos --bucket backups   # replaces the list
cubecli objectstorage key update web --all-buckets                      # every bucket, future ones too
cubecli objectstorage key update backup-admin --bypass-governance=false
```

- `--bucket` and `--all-buckets` are mutually exclusive. A key limited to
  buckets keeps only those; `--all-buckets` widens it again.
- `--bypass-governance` is for read_write keys. To make a bypass key read_only,
  also give `--bypass-governance=false`: nothing is cleared silently.
- Permission, buckets and bypass need the key to be `active` (409 otherwise:
  wait) and apply within a few seconds; a name change works any time.
- The expiry, tier and project cannot change: create a new key for that.
- Confirm with the user before widening a key (`--permission read_write`,
  `--all-buckets`, `--bypass-governance`).
