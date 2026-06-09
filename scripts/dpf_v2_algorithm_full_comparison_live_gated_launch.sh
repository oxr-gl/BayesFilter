#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/home/chakwong/BayesFilter}"
RUN_ID="${RUN_ID:-dpf-v2-algorithm-full-comparison-live-$(date +%Y%m%d-%H%M%S)}"
LOG_ROOT="$ROOT/docs/plans/logs"
RUN_DIR="$LOG_ROOT/$RUN_ID"
SUPERVISOR_SCRIPT="$ROOT/scripts/dpf_v2_algorithm_full_comparison_live_supervisor.sh"
GATE_SCRIPT="$ROOT/scripts/dpf_v2_algorithm_full_comparison_live_gate.py"

cd "$ROOT"

python "$GATE_SCRIPT" --root "$ROOT" --check-plan-review

if [[ -e "$RUN_DIR" ]]; then
  echo "refusing launch: run directory already exists: $RUN_DIR" >&2
  exit 2
fi
mkdir -p "$RUN_DIR"

git status --short > "$RUN_DIR/prelaunch-git-status.txt"
git status --porcelain=v1 | sed -E 's/^.. //; s/^"//; s/"$//; s/.* -> //' | sort -u > "$RUN_DIR/prelaunch-status-paths.txt"
git ls-files --others --exclude-standard > "$RUN_DIR/prelaunch-untracked-paths.txt"
git ls-files --others --ignored --exclude-standard | sort -u > "$RUN_DIR/prelaunch-ignored-files.txt"
git ls-files --others --exclude-standard | while IFS= read -r path; do
  [[ -n "$path" ]] || continue
  if [[ -d "$path" ]]; then
    find "$path" -type f
  elif [[ -f "$path" ]]; then
    echo "$path"
  fi
done | sort -u > "$RUN_DIR/prelaunch-untracked-files.txt"
{
  git diff --name-only
  git diff --cached --name-only
} | sort -u > "$RUN_DIR/prelaunch-dirty-tracked.txt"
git rev-parse HEAD > "$RUN_DIR/root-head.txt"

: > "$RUN_DIR/prelaunch-dirty-tracked-worktree-sha256.txt"
: > "$RUN_DIR/prelaunch-dirty-tracked-index.txt"
while IFS= read -r path; do
  [[ -n "$path" ]] || continue
  if [[ -e "$path" ]]; then
    sha256sum "$path" >> "$RUN_DIR/prelaunch-dirty-tracked-worktree-sha256.txt"
  else
    printf 'MISSING  %s\n' "$path" >> "$RUN_DIR/prelaunch-dirty-tracked-worktree-sha256.txt"
  fi
  git ls-files -s -- "$path" >> "$RUN_DIR/prelaunch-dirty-tracked-index.txt"
done < "$RUN_DIR/prelaunch-dirty-tracked.txt"

: > "$RUN_DIR/prelaunch-untracked-file-sha256.txt"
while IFS= read -r path; do
  [[ -n "$path" ]] || continue
  sha256sum "$path" >> "$RUN_DIR/prelaunch-untracked-file-sha256.txt"
done < "$RUN_DIR/prelaunch-untracked-files.txt"

: > "$RUN_DIR/prelaunch-ignored-file-sha256.txt"
while IFS= read -r path; do
  [[ -n "$path" ]] || continue
  if [[ -f "$path" ]]; then
    sha256sum "$path" >> "$RUN_DIR/prelaunch-ignored-file-sha256.txt"
  fi
done < "$RUN_DIR/prelaunch-ignored-files.txt"

if [[ -d "$ROOT/.localsource/filterflow/.git" ]]; then
  git -C "$ROOT/.localsource/filterflow" rev-parse HEAD > "$RUN_DIR/filterflow-head.txt"
  git -C "$ROOT/.localsource/filterflow" status --short > "$RUN_DIR/filterflow-prelaunch-status.txt"
  find "$ROOT/.localsource/filterflow" -path "$ROOT/.localsource/filterflow/.git" -prune -o -type f -print0 \
    | sort -z \
    | xargs -0 sha256sum > "$RUN_DIR/filterflow-prelaunch-file-sha256.txt"
  if [[ -s "$RUN_DIR/filterflow-prelaunch-status.txt" ]]; then
    echo "refusing launch: .localsource/filterflow is dirty before launch" >&2
    cat "$RUN_DIR/filterflow-prelaunch-status.txt" >&2
    exit 2
  fi
else
  : > "$RUN_DIR/filterflow-head.txt"
  : > "$RUN_DIR/filterflow-prelaunch-status.txt"
  : > "$RUN_DIR/filterflow-prelaunch-file-sha256.txt"
fi

log_file="$RUN_DIR/supervisor.log"
pid_file="$RUN_DIR/supervisor.pid"
rm -f "$pid_file"

setsid -f env \
  ROOT="$ROOT" \
  RUN_ID="$RUN_ID" \
  RUN_DIR="$RUN_DIR" \
  bash "$SUPERVISOR_SCRIPT" > "$log_file" 2>&1 &

echo "$!" > "$pid_file"

printf 'RUN_ID=%s\n' "$RUN_ID"
printf 'PID=%s\n' "$(cat "$pid_file")"
printf 'RUN_DIR=%s\n' "$RUN_DIR"
printf 'LOG_FILE=%s\n' "$log_file"
printf 'PID_FILE=%s\n' "$pid_file"
