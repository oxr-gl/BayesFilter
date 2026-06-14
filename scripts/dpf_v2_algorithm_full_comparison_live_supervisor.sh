#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:?ROOT is required}"
RUN_ID="${RUN_ID:?RUN_ID is required}"
RUN_DIR="${RUN_DIR:?RUN_DIR is required}"
WORKER="${WORKER:-/home/chakwong/python/claudecodex/scripts/claude_worker.sh}"
GATE_SCRIPT="$ROOT/scripts/dpf_v2_algorithm_full_comparison_live_gate.py"
REVIEW_SCRIPT="$ROOT/scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh"
PLAN="docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-live-gated-execution-plan-2026-06-07.md"
MAX_REVIEW_ITERATIONS="${MAX_REVIEW_ITERATIONS:-5}"

ALLOWED_CHANGED_PATTERNS=(
  "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-"
  "docs/plans/logs/dpf-v2-algorithm-full-comparison-"
  "experiments/dpf_implementation/reports/dpf-v2-"
  "experiments/dpf_implementation/reports/outputs/dpf_v2_"
  "experiments/dpf_implementation/tf_tfp/"
  "scripts/dpf_v2_algorithm_full_comparison_"
)

PHASES=(
  "P0|PASS_P0_READY_FOR_P1|governance and artifact contract|docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-subplan-2026-06-07.md"
  "P1|PASS_P1_ARCHITECTURE_READY_FOR_P2|BF/FF adapter architecture|docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p1-architecture-subplan-2026-06-07.md"
  "P2|PASS_P2_BOOTSTRAP_OT_CONTRACTS_READY_FOR_P3|bootstrap-OT frozen contracts|docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p2-bootstrap-ot-contracts-subplan-2026-06-07.md"
  "P3|PASS_P3_BOOTSTRAP_OT_VALUES_READY_FOR_P4|bootstrap-OT values|docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p3-bootstrap-ot-values-subplan-2026-06-07.md"
  "P4|PASS_P4_BOOTSTRAP_OT_GRADIENTS_READY_FOR_P5|bootstrap-OT fixed-branch AD gradients|docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-bootstrap-ot-gradients-subplan-2026-06-07.md"
  "P5|PASS_P5_LEDH_PFPF_OT_CONTRACTS_READY_FOR_P6|LEDH-PFPF-OT frozen contracts|docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-subplan-2026-06-07.md"
  "P6|PASS_P6_LEDH_PFPF_OT_VALUES_READY_FOR_P7|LEDH-PFPF-OT values|docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-subplan-2026-06-07.md"
  "P7|PASS_P7_LEDH_PFPF_OT_GRADIENTS_READY_FOR_P8|LEDH-PFPF-OT fixed-branch AD gradients|docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-subplan-2026-06-07.md"
  "P8|PASS_FULL_COMPARISON|closeout or reviewed blocker classification|docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p8-closeout-subplan-2026-06-07.md"
)

cd "$ROOT"

command -v unshare >/dev/null 2>&1 || {
  echo "unshare is required so phase workers see .localsource/filterflow read-only" >&2
  exit 2
}

check_filterflow_clean() {
  if [[ -d "$ROOT/.localsource/filterflow/.git" ]]; then
    local expected_head actual_head
    expected_head="$(tr -d '[:space:]' < "$RUN_DIR/filterflow-head.txt")"
    actual_head="$(git -C "$ROOT/.localsource/filterflow" rev-parse HEAD)"
    if [[ "$actual_head" != "$expected_head" ]]; then
      echo ".localsource/filterflow HEAD changed; this lane forbids mutation" >&2
      echo "expected: $expected_head" >&2
      echo "actual:   $actual_head" >&2
      exit 30
    fi
    if [[ -n "$(git -C "$ROOT/.localsource/filterflow" status --short)" ]]; then
      echo ".localsource/filterflow changed; this lane forbids mutation" >&2
      git -C "$ROOT/.localsource/filterflow" status --short >&2
      exit 30
    fi
    find "$ROOT/.localsource/filterflow" -path "$ROOT/.localsource/filterflow/.git" -prune -o -type f -print0 \
      | sort -z \
      | xargs -0 sha256sum > "$RUN_DIR/filterflow-current-file-sha256.txt"
    if ! cmp -s "$RUN_DIR/filterflow-prelaunch-file-sha256.txt" "$RUN_DIR/filterflow-current-file-sha256.txt"; then
      echo ".localsource/filterflow file checksums changed; this lane forbids mutation" >&2
      exit 30
    fi
  fi
}

check_protected_tracked_clean() {
  local protected_file
  : > "$RUN_DIR/current-dirty-tracked-worktree-sha256.txt"
  : > "$RUN_DIR/current-dirty-tracked-index.txt"
  while IFS= read -r protected_file; do
    [[ -n "$protected_file" ]] || continue
    if [[ -e "$protected_file" ]]; then
      sha256sum "$protected_file" >> "$RUN_DIR/current-dirty-tracked-worktree-sha256.txt"
    else
      printf 'MISSING  %s\n' "$protected_file" >> "$RUN_DIR/current-dirty-tracked-worktree-sha256.txt"
    fi
    git ls-files -s -- "$protected_file" >> "$RUN_DIR/current-dirty-tracked-index.txt"
  done < "$RUN_DIR/prelaunch-dirty-tracked.txt"
  if ! cmp -s "$RUN_DIR/prelaunch-dirty-tracked-worktree-sha256.txt" "$RUN_DIR/current-dirty-tracked-worktree-sha256.txt"; then
    echo "protected prelaunch dirty tracked file worktree content changed during live run" >&2
    exit 31
  fi
  if ! cmp -s "$RUN_DIR/prelaunch-dirty-tracked-index.txt" "$RUN_DIR/current-dirty-tracked-index.txt"; then
    echo "protected prelaunch dirty tracked file index state changed during live run" >&2
    exit 31
  fi
}

path_allowed() {
  local path="$1"
  local pattern
  for pattern in "${ALLOWED_CHANGED_PATTERNS[@]}"; do
    if [[ "$path" == "$pattern"* ]]; then
      return 0
    fi
  done
  return 1
}

check_changed_paths_allowed() {
  local changed_file
  while IFS= read -r changed_file; do
    [[ -n "$changed_file" ]] || continue
    if grep -Fxq "$changed_file" "$RUN_DIR/prelaunch-dirty-tracked.txt"; then
      continue
    fi
    if grep -Fxq "$changed_file" "$RUN_DIR/prelaunch-untracked-files.txt"; then
      continue
    fi
    if ! path_allowed "$changed_file"; then
      echo "live run changed path outside allowlist: $changed_file" >&2
      exit 32
    fi
  done < <(git status --porcelain=v1 | sed -E 's/^.. //; s/^"//; s/"$//; s/.* -> //' | sort -u)

  : > "$RUN_DIR/current-untracked-file-sha256.txt"
  while IFS= read -r changed_file; do
    [[ -n "$changed_file" ]] || continue
    sha256sum "$changed_file" >> "$RUN_DIR/current-untracked-file-sha256.txt"
  done < "$RUN_DIR/prelaunch-untracked-files.txt"
  if ! cmp -s "$RUN_DIR/prelaunch-untracked-file-sha256.txt" "$RUN_DIR/current-untracked-file-sha256.txt"; then
    echo "pre-existing untracked file content changed during live run" >&2
    exit 33
  fi

  while IFS= read -r changed_file; do
    [[ -n "$changed_file" ]] || continue
    if grep -Fxq "$changed_file" "$RUN_DIR/prelaunch-ignored-files.txt"; then
      continue
    fi
    if ! path_allowed "$changed_file"; then
      echo "live run created ignored path outside allowlist: $changed_file" >&2
      exit 34
    fi
  done < <(git ls-files --others --ignored --exclude-standard | sort -u)

  : > "$RUN_DIR/current-ignored-file-sha256.txt"
  while IFS= read -r changed_file; do
    [[ -n "$changed_file" ]] || continue
    if [[ -f "$changed_file" ]]; then
      sha256sum "$changed_file" >> "$RUN_DIR/current-ignored-file-sha256.txt"
    fi
  done < "$RUN_DIR/prelaunch-ignored-files.txt"
  if ! cmp -s "$RUN_DIR/prelaunch-ignored-file-sha256.txt" "$RUN_DIR/current-ignored-file-sha256.txt"; then
    echo "pre-existing ignored file content changed during live run" >&2
    exit 35
  fi
}

json_path_for_phase() {
  case "$1" in
    P0) echo "experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p0_governance_2026-06-07.json" ;;
    P1) echo "experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_p1_architecture_2026-06-07.json" ;;
    P2) echo "experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_contracts_2026-06-07.json" ;;
    P3) echo "experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_values_2026-06-07.json" ;;
    P4) echo "experiments/dpf_implementation/reports/outputs/dpf_v2_bootstrap_ot_gradients_2026-06-07.json" ;;
    P5) echo "experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_contracts_2026-06-07.json" ;;
    P6) echo "experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_values_2026-06-07.json" ;;
    P7) echo "experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_ot_gradients_2026-06-07.json" ;;
    P8) echo "experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_closeout_2026-06-07.json" ;;
    *) echo "unknown phase: $1" >&2; return 2 ;;
  esac
}

markdown_report_path_for_phase() {
  case "$1" in
    P0) echo "N/A" ;;
    P1) echo "experiments/dpf_implementation/reports/dpf-v2-algorithm-full-comparison-p1-architecture-2026-06-07.md" ;;
    P2) echo "experiments/dpf_implementation/reports/dpf-v2-bootstrap-ot-contracts-2026-06-07.md" ;;
    P3) echo "experiments/dpf_implementation/reports/dpf-v2-bootstrap-ot-values-2026-06-07.md" ;;
    P4) echo "experiments/dpf_implementation/reports/dpf-v2-bootstrap-ot-gradients-2026-06-07.md" ;;
    P5) echo "experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-contracts-2026-06-07.md" ;;
    P6) echo "experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-values-2026-06-07.md" ;;
    P7) echo "experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-ot-gradients-2026-06-07.md" ;;
    P8) echo "experiments/dpf_implementation/reports/dpf-v2-algorithm-full-comparison-closeout-2026-06-07.md" ;;
    *) echo "unknown phase: $1" >&2; return 2 ;;
  esac
}

run_codex_phase_worker() {
  local phase_prompt="$1"
  env ROOT="$ROOT" PHASE_PROMPT="$phase_prompt" \
    unshare --user --map-root-user --mount --propagation private \
      bash -c '
        set -euo pipefail
        if [[ -d "$ROOT/.localsource/filterflow" ]]; then
          mount --bind "$ROOT/.localsource/filterflow" "$ROOT/.localsource/filterflow"
          mount -o remount,bind,ro "$ROOT/.localsource/filterflow"
        fi
        exec codex exec --cd "$ROOT" --sandbox workspace-write --full-auto "$(cat "$PHASE_PROMPT")"
      '
}

latest_artifact_status() {
  local path="$1"
  awk '
    BEGIN { latest = "" }
    /^[[:space:]]*(status|Status|Verdict):[[:space:]]*`?[^`]+`?[[:space:]]*\.?[[:space:]]*$/ {
      line = $0
      sub(/^[[:space:]]*(status|Status|Verdict):[[:space:]]*`?/, "", line)
      sub(/`?[[:space:]]*\.?[[:space:]]*$/, "", line)
      latest = line
    }
    END { print latest }
  ' "$path"
}

result_path_for_phase() {
  case "$1" in
    P0) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-result-2026-06-07.md" ;;
    P1) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p1-architecture-result-2026-06-07.md" ;;
    P2) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p2-bootstrap-ot-contracts-result-2026-06-07.md" ;;
    P3) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p3-bootstrap-ot-values-result-2026-06-07.md" ;;
    P4) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-bootstrap-ot-gradients-result-2026-06-07.md" ;;
    P5) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-result-2026-06-07.md" ;;
    P6) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-result-2026-06-07.md" ;;
    P7) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-result-2026-06-07.md" ;;
    P8) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-closeout-result-2026-06-07.md" ;;
    *) echo "unknown phase: $1" >&2; return 2 ;;
  esac
}

review_path_for_phase() {
  case "$1" in
    P0) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p0-governance-claude-review-ledger-2026-06-07.md" ;;
    P1) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p1-architecture-claude-review-ledger-2026-06-07.md" ;;
    P2) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p2-bootstrap-ot-contracts-claude-review-ledger-2026-06-07.md" ;;
    P3) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p3-bootstrap-ot-values-claude-review-ledger-2026-06-07.md" ;;
    P4) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p4-bootstrap-ot-gradients-claude-review-ledger-2026-06-07.md" ;;
    P5) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p5-ledh-pfpf-ot-contracts-claude-review-ledger-2026-06-07.md" ;;
    P6) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p6-ledh-pfpf-ot-values-claude-review-ledger-2026-06-07.md" ;;
    P7) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-p7-ledh-pfpf-ot-gradients-claude-review-ledger-2026-06-07.md" ;;
    P8) echo "docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-closeout-claude-review-ledger-2026-06-07.md" ;;
    *) echo "unknown phase: $1" >&2; return 2 ;;
  esac
}

write_review_ledger() {
  local phase="$1"
  local token="$2"
  local iteration="$3"
  local review_output="$4"
  local status="$5"
  local review_ledger
  review_ledger="$ROOT/$(review_path_for_phase "$phase")"
  {
    echo "# DPF V2 Algorithm Full Comparison ${phase} Claude Read-Only Review Ledger"
    echo
    echo "metadata_date: 2026-06-07"
    echo "run_id: \`${RUN_ID}\`"
    echo "review_type: \`read_only_result_governance\`"
    echo "review_iteration: \`${iteration}\`"
    echo "expected_phase_token: \`${token}\`"
    echo "status: \`${status}\`"
    echo
    echo "## Claude Output"
    echo
    sed 's/^/> /' "$review_output"
  } > "$review_ledger"
}

for row in "${PHASES[@]}"; do
  IFS="|" read -r phase token description subplan <<<"$row"
  blocker_context=""

  for ((iteration = 1; iteration <= MAX_REVIEW_ITERATIONS; iteration++)); do
    phase_log="$RUN_DIR/${phase}-codex-iter${iteration}.log"
    phase_prompt="$RUN_DIR/${phase}-codex-iter${iteration}-prompt.txt"
    review_prompt="$RUN_DIR/${phase}-claude-review-iter${iteration}-prompt.txt"
    review_output="$RUN_DIR/${phase}-claude-review-iter${iteration}.txt"
    gate_output="$RUN_DIR/${phase}-gate-iter${iteration}.txt"

    cat > "$phase_prompt" <<PROMPT
You are Codex supervising the live-workspace DPF V2 full algorithm BF/FilterFlow comparison phase ${phase}: ${description}.

Run id: ${RUN_ID}

Execution plan:
${PLAN}

Phase subplan:
${subplan}

Required phase pass token:
${token}

Core rules:
- Execute the phase end to end in the live workspace; do not stop at a plan.
- Begin by recording a local skeptical phase audit against the phase evidence contract.
- Use CPU-only TensorFlow commands: set CUDA_VISIBLE_DEVICES=-1 before TensorFlow import.
- Do not mutate .localsource/filterflow.
- Do not run student implementation commands or derive student metrics.
- Do not treat BayesFilter, FilterFlow, students, TT, dense quadrature, paper tables, or simulated truth as an oracle.
- Do not relax tolerances, fixtures, branch masks, scalar definitions, OT settings, or gradient knobs after seeing results without a reviewed amendment.
- Finite differences are diagnostic-only and cannot promote gradient agreement.
- Preserve all six V2 rows in order.
- Write JSON, markdown/report, docs/plans result ledger, command logs, and ${RUN_DIR}/${phase}-command-manifest.json.
- The result ledger and command manifest must include run_id: \`${RUN_ID}\`.
- The result ledger latest status must be \`${token}\`, except P8 may close as \`BLOCKED_WITH_REVIEWED_CLASSIFICATION\` if a blocker is reviewed and classified.
- Do not invoke Claude yourself. The live shell supervisor invokes Claude as a separate read-only reviewer after your phase worker returns.
- If this is a repair iteration, write a repair amendment before changing code unless the blocker is only missing metadata/artifact formatting.
- Stop only for true human intervention, forbidden .localsource/filterflow mutation need, contract weakening, or five review iterations without PASS.

Protected tracked dirty files are listed in:
${RUN_DIR}/prelaunch-dirty-tracked.txt
Do not modify them.

Run logs for this phase should be written under:
${RUN_DIR}

Previous blocker context, if any:
${blocker_context}
PROMPT

    echo "=== ${phase} iteration ${iteration} start: ${description} ==="
    if ! run_codex_phase_worker "$phase_prompt" > "$phase_log" 2>&1; then
      blocker_context="Codex phase worker failed on iteration ${iteration}. See ${phase_log}."
      if [[ "$iteration" -eq "$MAX_REVIEW_ITERATIONS" ]]; then
        echo "phase ${phase} failed after max iterations; see ${phase_log}" >&2
        exit 20
      fi
      continue
    fi

    check_filterflow_clean
    check_protected_tracked_clean
    check_changed_paths_allowed

    cat > "$review_prompt" <<PROMPT
You are Claude acting only as a read-only critical reviewer for DPF V2 full algorithm BF/FilterFlow comparison phase ${phase}: ${description}.

Run id: ${RUN_ID}
Required phase token: ${token}
Execution plan: ${PLAN}
Phase subplan: ${subplan}
Codex phase log: ${phase_log}

Review the phase artifacts for material blockers only. You may read/search/list
files, but you must not edit files, run shell commands, or propose relaxed
criteria as a pass route.

Check explicitly:
- all six required V2 rows are preserved;
- no .localsource/filterflow mutation is needed or performed;
- no student implementation command or student metric entered the lane;
- no implementation is treated as an oracle;
- finite differences are diagnostic-only;
- branch masks, fixtures, scalar, tolerance, OT settings, and gradient knobs
  were not changed after result inspection without reviewed amendment;
- required JSON/report/result artifacts exist and preserve the evidence
  contract;
- the result ledger uses run_id ${RUN_ID};
- the latest result status is ${token}, except P8 may instead be
  BLOCKED_WITH_REVIEWED_CLASSIFICATION if the blocker classification is
  reviewed and honest.

Output format:
Verdict: PASS
Material blockers: none

or:

Verdict: BLOCK
Material blockers:
- <specific blocker with file/path evidence>
PROMPT

    if ! bash "$REVIEW_SCRIPT" --cwd "$ROOT" --name "${RUN_ID}-${phase}-review-${iteration}" "$(cat "$review_prompt")" > "$review_output" 2>&1; then
      blocker_context="Claude read-only review command failed on iteration ${iteration}. See ${review_output}."
      write_review_ledger "$phase" "$token" "$iteration" "$review_output" "CLAUDE_REVIEW_COMMAND_FAILED"
      if [[ "$iteration" -eq "$MAX_REVIEW_ITERATIONS" ]]; then
        echo "phase ${phase} Claude review command failed after max iterations; see ${review_output}" >&2
        exit 22
      fi
      continue
    fi

    if ! grep -Eq '^Verdict:[[:space:]]+PASS[[:space:]]*$' "$review_output"; then
      blocker_context="Claude read-only review blocked phase ${phase} on iteration ${iteration}. See ${review_output}."
      write_review_ledger "$phase" "$token" "$iteration" "$review_output" "BLOCKED_BY_CLAUDE_READ_ONLY_REVIEW"
      if [[ "$iteration" -eq "$MAX_REVIEW_ITERATIONS" ]]; then
        echo "phase ${phase} exhausted Claude review iterations; see ${review_output}" >&2
        exit 23
      fi
      continue
    fi

    review_status="$token"
    if [[ "$phase" == "P8" ]]; then
      result_status="$(latest_artifact_status "$ROOT/$(result_path_for_phase "$phase")")"
      if [[ "$result_status" == "BLOCKED_WITH_REVIEWED_CLASSIFICATION" ]]; then
        review_status="BLOCKED_WITH_REVIEWED_CLASSIFICATION"
      fi
    fi
    write_review_ledger "$phase" "$token" "$iteration" "$review_output" "$review_status"

    if python "$GATE_SCRIPT" --root "$ROOT" --phase "$phase" --run-id "$RUN_ID" --run-dir "$RUN_DIR" > "$gate_output" 2>&1; then
      echo "=== ${phase} pass: ${token} ==="
      break
    fi

    blocker_context="Local phase gate failed after Claude PASS on iteration ${iteration}. Gate output: $(cat "$gate_output")"
    if [[ "$iteration" -eq "$MAX_REVIEW_ITERATIONS" ]]; then
      echo "phase gate failed for ${phase} after max iterations; required token ${token}" >&2
      cat "$gate_output" >&2
      exit 21
    fi
  done
done

filterflow_after_head="N/A"
filterflow_after_status=""
if [[ -d "$ROOT/.localsource/filterflow/.git" ]]; then
  filterflow_after_head="$(git -C "$ROOT/.localsource/filterflow" rev-parse HEAD)"
  filterflow_after_status="$(git -C "$ROOT/.localsource/filterflow" status --short)"
fi

protected_after="none"
if ! cmp -s "$RUN_DIR/prelaunch-dirty-tracked-worktree-sha256.txt" "$RUN_DIR/current-dirty-tracked-worktree-sha256.txt" \
  || ! cmp -s "$RUN_DIR/prelaunch-dirty-tracked-index.txt" "$RUN_DIR/current-dirty-tracked-index.txt"; then
  protected_after="changed"
fi

p8_status="$(latest_artifact_status "$ROOT/$(result_path_for_phase P8)")"
p8_json="$ROOT/experiments/dpf_implementation/reports/outputs/dpf_v2_algorithm_full_comparison_closeout_2026-06-07.json"
p8_blocked_items="N/A"
if [[ -f "$p8_json" ]]; then
  p8_blocked_items="$(python - "$p8_json" <<'PY'
import json
import sys
from pathlib import Path

payload = json.loads(Path(sys.argv[1]).read_text())
items = payload.get("blocked_items", [])
if items:
    print("; ".join(str(item) for item in items))
else:
    print("none")
PY
)"
fi

{
  echo "# DPF V2 Algorithm Full Comparison Live Execution Result"
  echo
  echo "metadata_date: 2026-06-07"
  echo "run_id: \`${RUN_ID}\`"
  echo "status: \`LIVE_GATED_EXECUTION_COMPLETED\`"
  echo "final_status: \`${p8_status}\`"
  echo
  echo "All phase gates P0--P8 returned success for this run id. The P8 outcome was \`${p8_status}\`."
  echo
  echo "## Artifacts"
  echo
  for row in "${PHASES[@]}"; do
    IFS="|" read -r phase token description subplan <<<"$row"
    echo "- ${phase} subplan: \`${subplan}\`"
    echo "- ${phase} result: \`$(result_path_for_phase "$phase")\`"
    echo "- ${phase} review: \`$(review_path_for_phase "$phase")\`"
    echo "- ${phase} JSON: \`$(json_path_for_phase "$phase")\`"
    echo "- ${phase} markdown report: \`$(markdown_report_path_for_phase "$phase")\`"
    echo "- ${phase} command manifest: \`${RUN_DIR}/${phase}-command-manifest.json\`"
    echo "- ${phase} Codex prompt/log pattern: \`${RUN_DIR}/${phase}-codex-iter<N>-prompt.txt\`, \`${RUN_DIR}/${phase}-codex-iter<N>.log\`"
    echo "- ${phase} Claude prompt/output pattern: \`${RUN_DIR}/${phase}-claude-review-iter<N>-prompt.txt\`, \`${RUN_DIR}/${phase}-claude-review-iter<N>.txt\`"
    echo "- ${phase} gate output pattern: \`${RUN_DIR}/${phase}-gate-iter<N>.txt\`"
    echo "- ${phase} gate token: \`${token}\`"
  done
  echo "- run directory: \`${RUN_DIR}\`"
  echo "- P8 JSON: \`${p8_json}\`"
  echo
  echo "## FilterFlow State"
  echo
  echo "- before HEAD: \`$(tr -d '[:space:]' < "$RUN_DIR/filterflow-head.txt")\`"
  echo "- after HEAD: \`${filterflow_after_head}\`"
  echo "- after status: \`${filterflow_after_status:-clean}\`"
  echo
  echo "## Protected Dirty Tracked Files"
  echo
  echo "- prelaunch manifest: \`${RUN_DIR}/prelaunch-dirty-tracked.txt\`"
  echo "- protected changes after run: \`${protected_after:-none}\`"
  echo
  echo "## Decision"
  echo
  echo "- P8 outcome: \`${p8_status}\`"
  echo "- blocked items: \`${p8_blocked_items}\`"
  echo "- strongest alternative explanation: BF and FilterFlow-side adapters may share a contract or adapter error, so agreement is same-contract agreement rather than an implementation correctness proof."
  echo "- overturn condition: any later audit showing a mismatched frozen contract, missing required row or gradient knob, hidden branch/fixture/tolerance change, `.localsource/filterflow` mutation, nonfinite primary quantity, or unsupported oracle use would overturn the closeout."
  echo
  echo "## Non-Claims"
  echo
  echo "- no BayesFilter correctness proof"
  echo "- no FilterFlow correctness proof"
  echo "- no stochastic resampling distribution correctness claim"
  echo "- no gradient-through-random/discrete-branch claim"
  echo "- no student implementation claim"
  echo "- no TT/SIRT, paper-table, HMC, DSGE, GPU, scalability, deployment, or production-readiness claim"
} > "$ROOT/docs/plans/bayesfilter-dpf-v2-algorithm-full-bf-filterflow-comparison-live-gated-execution-result-2026-06-07.md"
