#!/usr/bin/env bash
# Link this repo's skills and global agent instructions into each harness's user-level directories.
# Usage: ./install.sh [--with-science] [--with-optional] [--all] [--no-memory] [--uninstall] [--dry-run]
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$REPO/skills"
MEMORY_SRC="$REPO/global/AGENTS.md"
SKILL_TARGETS=("$HOME/.agents/skills" "$HOME/.claude/skills")
LEGACY_SKILL_DIRS=("$HOME/.codex/skills")
MEMORY_TARGETS=("$HOME/.codex/AGENTS.md" "$HOME/.claude/CLAUDE.md" "$HOME/.gemini/GEMINI.md")
BACKUP="$HOME/.skills-backup/$(date +%Y%m%d-%H%M%S)"

with_science=0 with_optional=0 memory=1 uninstall=0 dry=0
for arg in "$@"; do
  case "$arg" in
    --with-science) with_science=1 ;;
    --with-optional) with_optional=1 ;;
    --all) with_science=1 with_optional=1 ;;
    --no-memory) memory=0 ;;
    --uninstall) uninstall=1 ;;
    --dry-run) dry=1 ;;
    -h | --help) sed -n '2,3p' "$0"; exit 0 ;;
    *) echo "unknown flag: $arg" >&2; exit 2 ;;
  esac
done

run() { if ((dry)); then echo "+ $*"; else "$@"; fi; }

points_into_repo() { [[ -L "$1" && "$(readlink "$1")" == "$REPO/"* ]]; }

backup() {
  local path="$1" rel="${1#"$HOME"/}"
  run mkdir -p "$(dirname "$BACKUP/$rel")"
  run mv "$path" "$BACKUP/$rel"
}

names_in() { [[ -f "$1" ]] && grep -v '^#' "$1" | sed '/^[[:space:]]*$/d' || true; }

excluded() {
  local dir
  if ((with_science == 0)); then
    for dir in "$REPO"/upstreams/*/; do
      grep -q '"install_profile": *"science"' "$dir/source.json" 2>/dev/null && names_in "$dir/SKILL_NAMES.txt"
    done
  fi
  if ((with_optional == 0)); then names_in "$REPO/profiles/optional.txt"; fi
}

selected() {
  local skip dir name
  skip="$(excluded)"
  for dir in "$SRC"/*/; do
    name="$(basename "$dir")"
    [[ -f "$dir/SKILL.md" ]] || continue
    grep -qxF "$name" <<<"$skip" && continue
    echo "$name"
  done
}

for target in "${SKILL_TARGETS[@]}" "${LEGACY_SKILL_DIRS[@]}"; do
  [[ -d "$target" ]] || continue
  for link in "$target"/*; do
    if points_into_repo "$link" || [[ -L "$link" && ! -e "$link" ]]; then run rm "$link"; fi
  done
done
for target in "${MEMORY_TARGETS[@]}"; do
  if points_into_repo "$target"; then run rm "$target"; fi
done
if ((uninstall)); then echo "Removed links into $REPO."; exit 0; fi

count=0
while IFS= read -r name; do
  for target in "${SKILL_TARGETS[@]}"; do
    run mkdir -p "$target"
    if [[ -e "$target/$name" || -L "$target/$name" ]]; then backup "$target/$name"; fi
    run ln -s "$SRC/$name" "$target/$name"
  done
  for legacy in "${LEGACY_SKILL_DIRS[@]}"; do
    if [[ -e "$legacy/$name" || -L "$legacy/$name" ]]; then backup "$legacy/$name"; fi
  done
  count=$((count + 1))
done < <(selected)
echo "Linked $count skills into: ${SKILL_TARGETS[*]}"

if ((memory)) && [[ -f "$MEMORY_SRC" ]]; then
  for target in "${MEMORY_TARGETS[@]}"; do
    run mkdir -p "$(dirname "$target")"
    if [[ -e "$target" || -L "$target" ]]; then backup "$target"; fi
    run ln -s "$MEMORY_SRC" "$target"
  done
  echo "Linked global instructions into: ${MEMORY_TARGETS[*]}"
fi

if [[ -d "$BACKUP" ]]; then echo "Replaced files moved to $BACKUP"; fi
