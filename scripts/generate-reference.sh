#!/usr/bin/env bash
# Regenerates the vendored cubecli command reference inside each skill.
#
# The reference comes from `cubecli docs markdown`, so the skills can only
# document commands and flags that exist. CI runs this and fails on any diff.
#
# Usage: scripts/generate-reference.sh            (uses cubecli from PATH)
#        CUBECLI=/path/to/cubecli scripts/generate-reference.sh
set -euo pipefail

CUBECLI="${CUBECLI:-cubecli}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS="$ROOT/plugins/cubepath/skills"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

"$CUBECLI" docs markdown "$TMP"

# skill -> command groups it vendors. README.md is the index of all groups.
declare -a MAP=(
  "cubepath-cli:README auth login logout profile config project ssh-key location version mcp"
  "cubepath-vps:vps snapshot availability-group baremetal"
  "cubepath-networking:network nat-gateway floating-ip lb ddos-attack"
  "cubepath-dns-cdn:dns cdn"
  "cubepath-kubernetes:kubernetes"
  "cubepath-object-storage:objectstorage"
)

for entry in "${MAP[@]}"; do
  skill="${entry%%:*}"
  groups="${entry#*:}"
  dest="$SKILLS/$skill/reference"
  rm -rf "$dest"
  mkdir -p "$dest"
  for g in $groups; do
    if [[ ! -f "$TMP/$g.md" ]]; then
      echo "cubecli has no command group '$g' (needed by $skill)" >&2
      exit 1
    fi
    if [[ "$g" == README ]]; then
      # The index links to every group; only some live in this skill, so keep
      # the list and drop the links.
      sed -E 's/^- \[([^]]+)\]\([^)]+\)/- `\1`/' "$TMP/README.md" > "$dest/commands.md"
    else
      cp "$TMP/$g.md" "$dest/$g.md"
    fi
  done
done

echo "Reference regenerated from $("$CUBECLI" version 2>/dev/null | head -1)"
