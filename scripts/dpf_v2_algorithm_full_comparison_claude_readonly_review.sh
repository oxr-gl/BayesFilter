#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE' >&2
Usage:
  dpf_v2_algorithm_full_comparison_claude_readonly_review.sh [--cwd DIR] [--name NAME] [--model MODEL] PROMPT...

Launch Claude Code as a read-only critical reviewer. The tool set is restricted
to file reads/search/listing. No edit/write/Bash tools are exposed.
USAGE
}

cwd="${PWD}"
name="dpf-v2-readonly-review"
model="${CLAUDE_REVIEW_MODEL:-sonnet}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cwd)
      [[ $# -ge 2 ]] || { usage; exit 2; }
      cwd="$2"
      shift 2
      ;;
    --name)
      [[ $# -ge 2 ]] || { usage; exit 2; }
      name="$2"
      shift 2
      ;;
    --model)
      [[ $# -ge 2 ]] || { usage; exit 2; }
      model="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "unknown option: $1" >&2
      usage
      exit 2
      ;;
    *)
      break
      ;;
  esac
done

[[ $# -gt 0 ]] || { usage; exit 2; }
[[ -d "$cwd" ]] || { echo "review cwd does not exist: $cwd" >&2; exit 2; }

cd "$cwd"

exec claude -p \
  --output-format text \
  --permission-mode dontAsk \
  --tools "Read,Grep,Glob,LS" \
  --disallowedTools "Edit,MultiEdit,Write,NotebookEdit,Bash" \
  --name "$name" \
  --model "$model" \
  "$*"
