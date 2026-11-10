#!/usr/bin/env bash
# Link this repo's skills, subagents, and global agent instructions into each harness's user-level directories.
# Usage: ./install.sh [--with-science] [--with-optional] [--all] [--no-memory] [--defaults] [--force] [--dry-run]
#        ./install.sh --update [--force] [--dry-run]   pull this repo, then relink
#        ./install.sh --uninstall
# Selection flags are saved per machine and reused when none are given; --defaults resets to the default set.
# Entries that are not links into this repo are machine-local and are kept; --force moves same-name entries to backup.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$REPO/skills"
AGENT_SRC="$REPO/agents"
MEMORY_SRC="$REPO/global/AGENTS.md"
SKILL_TARGETS=("$HOME/.agents/skills" "$HOME/.claude/skills")
# Claude Code and Cursor both load subagents from ~/.claude/agents.
AGENT_TARGETS=("$HOME/.claude/agents")
LEGACY_SKILL_DIRS=("$HOME/.codex/skills")
MEMORY_TARGETS=("$HOME/.codex/AGENTS.md" "$HOME/.claude/CLAUDE.md" "$HOME/.gemini/GEMINI.md")
BACKUP="$HOME/.skills-backup/$(date +%Y%m%d-%H%M%S)"
SELECTION_FILE="${XDG_CONFIG_HOME:-$HOME/.config}/portable-skills/install-flags"

with_science=0 with_optional=0 memory=1 uninstall=0 dry=0 update=0 force=0
selection=()
parse() {
  case "$1" in
    --with-science) with_science=1 ;;
    --with-optional) with_optional=1 ;;
    --all) with_science=1 with_optional=1 ;;
    --no-memory) memory=0 ;;
    --defaults) ;;
    --update) update=1 ;;
    --force) force=1 ;;
    --uninstall) uninstall=1 ;;
    --dry-run) dry=1 ;;
    -h | --help) sed -n '2,7p' "$0"; exit 0 ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
  case "$1" in --with-science | --with-optional | --all | --no-memory | --defaults) selection+=("$1") ;; esac
}
reexec=()
for arg in "$@"; do
  parse "$arg"
  if [[ "$arg" != --update ]]; then reexec+=("$arg"); fi
done

run() { if ((dry)); then echo "+ $*"; else "$@"; fi; }

if ((update)); then
  run git -C "$REPO" pull --ff-only
  # Re-exec so the relink runs the freshly pulled installer.
  exec "$REPO/install.sh" ${reexec[@]+"${reexec[@]}"}
fi

if ((${#selection[@]} == 0)) && [[ -f "$SELECTION_FILE" ]]; then
  while IFS= read -r flag; do
    if [[ -n "$flag" ]]; then parse "$flag"; fi
  done <"$SELECTION_FILE"
fi

points_into_repo() { [[ -L "$1" && "$(readlink "$1")" == "$REPO/"* ]]; }

backup() {
  local path="$1" rel="${1#"$HOME"/}"
  run mkdir -p "$(dirname "$BACKUP/$rel")"
  run mv "$path" "$BACKUP/$rel"
}

kept=()
# Returns 1 when a machine-local entry occupies dest and --force is not set.
claim() {
  local dest="$1"
  if [[ ! -e "$dest" && ! -L "$dest" ]] || points_into_repo "$dest"; then return 0; fi
  if ((force)); then backup "$dest"; return 0; fi
  kept+=("$dest")
  return 1
}

link() {
  run mkdir -p "$(dirname "$2")"
  if claim "$2"; then run ln -s "$1" "$2"; fi
}

names_in() {
  if [[ -f "$1" ]]; then sed -e '/^#/d' -e '/^[[:space:]]*$/d' "$1"; fi
}

excluded() {
  local dir
  if ((with_science == 0)); then
    for dir in "$REPO"/upstreams/*/; do
      if grep -q '"install_profile": *"science"' "$dir/source.json" 2>/dev/null; then
        names_in "$dir/SKILL_NAMES.txt"
        names_in "$dir/LOCAL_SKILLS.txt"
      fi
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

for target in "${SKILL_TARGETS[@]}" "${LEGACY_SKILL_DIRS[@]}" "${AGENT_TARGETS[@]}"; do
  [[ -d "$target" ]] || continue
  for entry in "$target"/*; do
    if points_into_repo "$entry" || [[ -L "$entry" && ! -e "$entry" ]]; then run rm "$entry"; fi
  done
done
for target in "${MEMORY_TARGETS[@]}"; do
  if points_into_repo "$target"; then run rm "$target"; fi
done
if ((uninstall)); then
  run rm -f "$SELECTION_FILE"
  echo "Removed links into $REPO."
  exit 0
fi

count=0
while IFS= read -r name; do
  for target in "${SKILL_TARGETS[@]}"; do link "$SRC/$name" "$target/$name"; done
  # Cursor also scans the legacy directory, so a same-name copy there would shadow the repo skill.
  for legacy in "${LEGACY_SKILL_DIRS[@]}"; do claim "$legacy/$name" || true; done
  count=$((count + 1))
done < <(selected)
echo "Linked $count skills into: ${SKILL_TARGETS[*]}"

count=0
for agent in "$AGENT_SRC"/*.md; do
  [[ -f "$agent" ]] || continue
  for target in "${AGENT_TARGETS[@]}"; do link "$agent" "$target/$(basename "$agent")"; done
  count=$((count + 1))
done
echo "Linked $count subagents into: ${AGENT_TARGETS[*]}"

if ((memory)) && [[ -f "$MEMORY_SRC" ]]; then
  for target in "${MEMORY_TARGETS[@]}"; do link "$MEMORY_SRC" "$target"; done
  echo "Linked global instructions into: ${MEMORY_TARGETS[*]}"
fi

if ((!dry)); then
  mkdir -p "$(dirname "$SELECTION_FILE")"
  printf '%s\n' ${selection[@]+"${selection[@]}"} >"$SELECTION_FILE"
fi

if ((${#kept[@]})); then
  echo "Kept ${#kept[@]} machine-local entries that share a repo name; rerun with --force to replace them:"
  printf '  %s\n' "${kept[@]}"
fi
if [[ -d "$BACKUP" ]]; then echo "Replaced files moved to $BACKUP"; fi
