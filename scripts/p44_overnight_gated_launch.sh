#!/usr/bin/env bash
set -euo pipefail

if [[ "${P44_ENABLE_DETACHED_LEGACY_SUPERVISOR:-0}" != "1" ]]; then
  cat >&2 <<'EOF'
refusing launch: detached shell-supervised P44 execution is not the primary
runbook route. Codex must supervise and execute phases directly, with Claude
restricted to read-only review. Set P44_ENABLE_DETACHED_LEGACY_SUPERVISOR=1
only for a separately gated narrow operational subtask.
EOF
  exit 2
fi

ROOT="${ROOT:-/home/chakwong/BayesFilter}"
WORKER="${WORKER:-/home/chakwong/python/claudecodex/scripts/claude_worker.sh}"
SETTINGS="$ROOT/.claude/p44-overnight-worker-settings.json"
RUNBOOK_LEDGER="$ROOT/docs/plans/bayesfilter-highdim-zhao-cui-p44-overnight-gated-self-recovery-claude-review-ledger-2026-06-07.md"
EXECUTION_RESULT="$ROOT/docs/plans/bayesfilter-highdim-zhao-cui-p44-overnight-gated-self-recovery-execution-result-2026-06-07.md"
LOG_DIR="$ROOT/docs/plans/logs"
REVIEW_CYCLE="${REVIEW_CYCLE:?REVIEW_CYCLE is required}"
MAX_REVIEW_ITERATION="${MAX_REVIEW_ITERATION:-5}"
RUN_ID="p44-overnight-gated-$(date +%Y%m%d-%H%M%S)"
LOG_FILE="$LOG_DIR/${RUN_ID}.log"
PID_FILE="$LOG_DIR/${RUN_ID}.pid"
WRAPPER_PID_FILE="$LOG_DIR/${RUN_ID}.wrapper.pid"
SUPERVISOR_PID_FILE="$LOG_DIR/${RUN_ID}.supervisor.pid"
HANDOFF_READY_FILE="$LOG_DIR/${RUN_ID}.handoff.ready"
TRUSTED_GATE_DIR="${TRUSTED_GATE_DIR:-/tmp/${RUN_ID}-trusted-gate}"
TRUSTED_GATE_SCRIPT="$TRUSTED_GATE_DIR/p44_phase_gate.py"
TRUSTED_GATE_SHA256=""
DIRTY_MANIFEST="$LOG_DIR/${RUN_ID}-prelaunch-git-status.txt"
DIRTY_TRACKED_MANIFEST="$LOG_DIR/${RUN_ID}-prelaunch-dirty-tracked.txt"
LAUNCH_ROOT="${LAUNCH_ROOT:-/tmp/${RUN_ID}-workspace}"
SOURCE_ROOT="$ROOT"
HANDOFF_WAIT_ATTEMPTS="${HANDOFF_WAIT_ATTEMPTS:-50}"
HANDOFF_WAIT_SECONDS="${HANDOFF_WAIT_SECONDS:-0.2}"

mkdir -p "$LOG_DIR"

python "$ROOT/scripts/p44_phase_gate.py" \
  --root "$ROOT" \
  --runbook-ledger "$RUNBOOK_LEDGER" \
  --execution-result "$EXECUTION_RESULT" \
  --review-cycle "$REVIEW_CYCLE" \
  --max-review-iteration "$MAX_REVIEW_ITERATION" \
  --check-runbook-pass \
  --check-execution-ready

if [[ ! -f "$SETTINGS" ]]; then
  echo "refusing launch: dedicated worker settings missing: $SETTINGS" >&2
  exit 2
fi
if ! command -v unshare >/dev/null 2>&1; then
  echo "refusing launch: unshare is required for mount-namespace isolation" >&2
  exit 2
fi

(
  cd "$ROOT"
  git status --short > "$DIRTY_MANIFEST"
  {
    git diff --name-only
    git diff --cached --name-only
  } | sort -u > "$DIRTY_TRACKED_MANIFEST"
)

if [[ -e "$LAUNCH_ROOT" ]]; then
  echo "refusing launch: launch workspace already exists: $LAUNCH_ROOT" >&2
  exit 2
fi
if [[ -e "$TRUSTED_GATE_DIR" ]]; then
  echo "refusing launch: trusted gate directory already exists: $TRUSTED_GATE_DIR" >&2
  exit 2
fi
mkdir -p "$LAUNCH_ROOT"
cp -a "$ROOT/." "$LAUNCH_ROOT/"
mkdir -p "$TRUSTED_GATE_DIR"
cp "$ROOT/scripts/p44_phase_gate.py" "$TRUSTED_GATE_SCRIPT"
TRUSTED_GATE_SHA256="$(sha256sum "$TRUSTED_GATE_SCRIPT")"
TRUSTED_GATE_SHA256="${TRUSTED_GATE_SHA256%% *}"
chmod 0555 "$TRUSTED_GATE_DIR"
chmod 0444 "$TRUSTED_GATE_SCRIPT"
rm -f "$PID_FILE" "$WRAPPER_PID_FILE" "$SUPERVISOR_PID_FILE" "$HANDOFF_READY_FILE"

setsid -f env \
  ROOT="$SOURCE_ROOT" \
  SOURCE_ROOT="$SOURCE_ROOT" \
  TRUSTED_ROOT="$SOURCE_ROOT" \
  TRUSTED_GATE_DIR="$TRUSTED_GATE_DIR" \
  TRUSTED_GATE_SCRIPT="$TRUSTED_GATE_SCRIPT" \
  TRUSTED_GATE_SHA256="$TRUSTED_GATE_SHA256" \
  LAUNCH_ROOT="$LAUNCH_ROOT" \
  WORKER="$WORKER" \
  SETTINGS="$SOURCE_ROOT/.claude/p44-overnight-worker-settings.json" \
  RUN_ID="$RUN_ID" \
  OUTER_LOG_DIR="$SOURCE_ROOT/docs/plans/logs" \
  DIRTY_MANIFEST="$DIRTY_MANIFEST" \
  DIRTY_TRACKED_MANIFEST="$DIRTY_TRACKED_MANIFEST" \
  SUPERVISOR_PID_FILE="$SOURCE_ROOT/docs/plans/logs/${RUN_ID}.supervisor.pid" \
  HANDOFF_READY_FILE="$SOURCE_ROOT/docs/plans/logs/${RUN_ID}.handoff.ready" \
  unshare --user --map-root-user --mount --propagation private \
    bash -c '
      set -euo pipefail
      mount --bind "$TRUSTED_GATE_DIR" "$TRUSTED_GATE_DIR"
      mount -o remount,bind,ro "$TRUSTED_GATE_DIR"
      mkdir -p /tmp/"$RUN_ID"-outer-logs
      mount --bind "'"$LOG_DIR"'" /tmp/"$RUN_ID"-outer-logs
      mount --bind "$LAUNCH_ROOT" "$SOURCE_ROOT"
      mkdir -p "$SOURCE_ROOT/docs/plans/logs"
      mount --bind /tmp/"$RUN_ID"-outer-logs "$SOURCE_ROOT/docs/plans/logs"
      printf "%s\n" "$$" > "$SUPERVISOR_PID_FILE"
      printf "ready\n" > "$HANDOFF_READY_FILE"
      exec bash "$SOURCE_ROOT/scripts/p44_overnight_supervisor.sh"
    ' > "$LOG_FILE" 2>&1 &
echo "$!" > "$WRAPPER_PID_FILE"

for ((attempt = 1; attempt <= HANDOFF_WAIT_ATTEMPTS; attempt++)); do
  if [[ -s "$SUPERVISOR_PID_FILE" && -f "$HANDOFF_READY_FILE" ]]; then
    break
  fi
  sleep "$HANDOFF_WAIT_SECONDS"
done

if [[ ! -s "$SUPERVISOR_PID_FILE" || ! -f "$HANDOFF_READY_FILE" ]]; then
  echo "refusing launch: supervisor did not complete handoff" >&2
  echo "see $LOG_FILE" >&2
  exit 20
fi

SUPERVISOR_PID="$(tr -d '[:space:]' < "$SUPERVISOR_PID_FILE")"
if [[ ! "$SUPERVISOR_PID" =~ ^[0-9]+$ ]]; then
  echo "refusing launch: invalid supervisor PID: $SUPERVISOR_PID" >&2
  exit 21
fi
if ! kill -0 "$SUPERVISOR_PID" 2>/dev/null; then
  echo "refusing launch: supervisor PID is not alive: $SUPERVISOR_PID" >&2
  echo "see $LOG_FILE" >&2
  exit 22
fi
echo "$SUPERVISOR_PID" > "$PID_FILE"

printf 'RUN_ID=%s\n' "$RUN_ID"
printf 'REVIEW_CYCLE=%s\n' "$REVIEW_CYCLE"
printf 'PID=%s\n' "$SUPERVISOR_PID"
printf 'LOG_FILE=%s\n' "$LOG_FILE"
printf 'PID_FILE=%s\n' "$PID_FILE"
printf 'WRAPPER_PID_FILE=%s\n' "$WRAPPER_PID_FILE"
printf 'SUPERVISOR_PID_FILE=%s\n' "$SUPERVISOR_PID_FILE"
printf 'HANDOFF_READY_FILE=%s\n' "$HANDOFF_READY_FILE"
printf 'TRUSTED_GATE_SCRIPT=%s\n' "$TRUSTED_GATE_SCRIPT"
printf 'TRUSTED_GATE_SHA256=%s\n' "$TRUSTED_GATE_SHA256"
printf 'DIRTY_MANIFEST=%s\n' "$DIRTY_MANIFEST"
printf 'DIRTY_TRACKED_MANIFEST=%s\n' "$DIRTY_TRACKED_MANIFEST"
printf 'LAUNCH_ROOT=%s\n' "$LAUNCH_ROOT"
