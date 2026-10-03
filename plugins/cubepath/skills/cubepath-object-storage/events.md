# Object Storage event notifications

Follow the `cubepath-cli` skill first (session, profile, `--json`, confirmations).
Exact flags: [reference/objectstorage.md](reference/objectstorage.md).

Event notifications send `object.created`, `object.removed` and `object.tagging`
of a bucket to a **destination**: a webhook (https, port 443 or 8443, public
address) or a Slack/Discord channel of Cloud Alerts (`cubecli alert notificator
list`). A **rule** on the bucket picks the events, an optional key prefix and
suffix, and the destination; it is `pending` for a few seconds, then `active`.
Names: letters, digits, hyphens and spaces. Deliveries page back with
`--before <next_before>` (unix ms); `failed` is retried, `dead` was given up.

```bash
cubecli objectstorage events destination create --name uploads-hook --webhook https://example.com/hooks/storage [--format s3]
cubecli objectstorage events rule create --bucket photos --destination uploads-hook --events created,removed --prefix incoming/ --suffix .jpg
cubecli objectstorage events destination test uploads-hook                     # sends a cubepath.ping
cubecli objectstorage events destination deliveries uploads-hook --status failed --json   # {deliveries, next_before}
cubecli objectstorage events destination rotate-secret uploads-hook --force    # after the user confirms
```

- The signing secret (`whsec_...`) is printed **only** by `create` and
  `rotate-secret`: tell the user to store it at once. After a rotation the old
  secret keeps signing for 24 hours. Channel destinations are not signed.
- Verify every delivery on the raw body: `CubePath-Signature` holds one or more
  `v1=<hex>` (`v1=<new>, v1=<previous>` after a rotation), each
  HMAC-SHA256(secret, `CubePath-Timestamp` + "." + body).
  Compare in constant time, accept any `v1=`, reject timestamps over 5 minutes
  old, deduplicate by `CubePath-Event-Id` (delivery is at least once). The SDKs
  ship `VerifyStorageEventSignature` / `verifyStorageEventSignature` /
  `verify_storage_event_signature` / `Webhooks::verifyStorageEventSignature`.
- A destination that keeps failing is disabled (`auto_disabled`); fix the
  receiver, then `destination update <name> --enable`. Delete its rules before
  deleting a destination.
