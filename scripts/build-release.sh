#!/usr/bin/env bash
# Builds the release artifacts that `cubecli skills install` downloads:
#   dist/cubepath-skills-<version>.tar.gz  (manifest.json + skills/<name>/...)
#   dist/SHA256SUMS
# The version comes from manifest.json and must match the tag being released.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

VERSION="$(python3 -c 'import json; print(json.load(open("manifest.json"))["version"])')"
if [[ -n "${GITHUB_REF_NAME:-}" && "$GITHUB_REF_NAME" != "v$VERSION" ]]; then
  echo "tag $GITHUB_REF_NAME does not match manifest version v$VERSION" >&2
  exit 1
fi

python3 scripts/validate.py

NAME="cubepath-skills-v$VERSION"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/$NAME"
cp manifest.json LICENSE "$STAGE/$NAME/"
cp -R plugins/cubepath/skills "$STAGE/$NAME/skills"

mkdir -p dist
# Deterministic archive: fixed order, owner and mtime.
tar -C "$STAGE" --sort=name --owner=0 --group=0 --numeric-owner \
  --mtime="@${SOURCE_DATE_EPOCH:-0}" -czf "dist/$NAME.tar.gz" "$NAME" 2>/dev/null \
  || COPYFILE_DISABLE=1 tar -C "$STAGE" --no-mac-metadata -czf "dist/$NAME.tar.gz" "$NAME"   # BSD tar (macOS): no ._* AppleDouble files
(cd dist && shasum -a 256 "$NAME.tar.gz" > SHA256SUMS)
echo "Built dist/$NAME.tar.gz"
