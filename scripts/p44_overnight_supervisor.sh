#!/usr/bin/env bash
set -euo pipefail

if [[ "${P44_ENABLE_DETACHED_LEGACY_SUPERVISOR:-0}" != "1" ]]; then
  cat >&2 <<'EOF'
refusing supervisor start: detached shell-supervised P44 execution is not the
primary runbook route. Codex must supervise and execute phases directly, with
Claude restricted to read-only review.
EOF
  exit 2
fi

ROOT="${ROOT:?ROOT is required}"
TRUSTED_ROOT="${TRUSTED_ROOT:-$ROOT}"
TRUSTED_GATE_SCRIPT="${TRUSTED_GATE_SCRIPT:-$TRUSTED_ROOT/scripts/p44_phase_gate.py}"
TRUSTED_GATE_SHA256="${TRUSTED_GATE_SHA256:-}"
WORKER="${WORKER:-/home/chakwong/python/claudecodex/scripts/claude_worker.sh}"
SETTINGS="${SETTINGS:?SETTINGS is required}"
RUN_ID="${RUN_ID:?RUN_ID is required}"
OUTER_LOG_DIR="${OUTER_LOG_DIR:?OUTER_LOG_DIR is required}"
DIRTY_MANIFEST="${DIRTY_MANIFEST:?DIRTY_MANIFEST is required}"
DIRTY_TRACKED_MANIFEST="${DIRTY_TRACKED_MANIFEST:?DIRTY_TRACKED_MANIFEST is required}"

PHASES=(
  "P44-M0|PASS_P44_M0_CODE_GOVERNANCE|target governance matrix|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase0-target-governance-subplan-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase0-target-governance-result-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase0-target-governance-claude-review-ledger-2026-06-07.md"
  "P44-M1|PASS_P44_M1_CODE_GOVERNANCE|LGSSM exact baseline|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase1-lgssm-subplan-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase1-lgssm-result-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase1-lgssm-claude-review-ledger-2026-06-07.md"
  "P44-M2|PASS_P44_M2_CODE_GOVERNANCE|cubic additive-Gaussian observation|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase2-cubic-additive-gaussian-subplan-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase2-cubic-additive-gaussian-result-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase2-cubic-additive-gaussian-claude-review-ledger-2026-06-07.md"
  "P44-M3|PASS_P44_M3_CODE_GOVERNANCE|quadratic observation multimodality stress|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase3-quadratic-observation-subplan-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase3-quadratic-observation-result-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase3-quadratic-observation-claude-review-ledger-2026-06-07.md"
  "P44-M4|PASS_P44_M4_CODE_GOVERNANCE|nonlinear additive-Gaussian transition|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-subplan-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-result-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase4-nonlinear-transition-claude-review-ledger-2026-06-07.md"
  "P44-M5|PASS_P44_M5_CODE_GOVERNANCE|spatial SIR diagnostic closure|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase5-spatial-sir-diagnostic-subplan-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase5-spatial-sir-diagnostic-result-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase5-spatial-sir-diagnostic-claude-review-ledger-2026-06-07.md"
  "P44-M6|PASS_P44_M6_CODE_GOVERNANCE|predator-prey diagnostic closure|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase6-predator-prey-diagnostic-subplan-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase6-predator-prey-diagnostic-result-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase6-predator-prey-diagnostic-claude-review-ledger-2026-06-07.md"
  "P44-M7|PASS_P44_M7_CODE_GOVERNANCE|generalized SV target-definition gate|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-subplan-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-result-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase7-generalized-sv-target-claude-review-ledger-2026-06-07.md"
  "P44-M8|PASS_P44_M8_CODE_GOVERNANCE|integration closeout|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase8-integration-closeout-subplan-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase8-integration-closeout-result-2026-06-07.md|docs/plans/bayesfilter-highdim-zhao-cui-p44-phase8-integration-closeout-claude-review-ledger-2026-06-07.md"
)

cd "$ROOT"

for row in "${PHASES[@]}"; do
  IFS="|" read -r phase token description subplan result_note review_ledger <<<"$row"
  manifest="${result_note%-result-2026-06-07.md}-evidence-manifest-${RUN_ID}.json"
  phase_log="$OUTER_LOG_DIR/${RUN_ID}-${phase}.log"
  phase_prompt="$OUTER_LOG_DIR/${RUN_ID}-${phase}-prompt.txt"
  cat > "$phase_prompt" <<PROMPT
Execute ${phase}: ${description} for the P44 overnight gated self-recovery run.

Subplan:
${subplan}

Runbook:
docs/plans/bayesfilter-highdim-zhao-cui-p44-overnight-gated-self-recovery-runbook-2026-06-07.md

Rules:
- The user has already approved autonomous overnight execution of this phase.
- Do not stop after writing a plan, proposal, checklist, or approval request.
  A planning-only response is a phase failure.
- If a plan or repair amendment is needed, write it as an artifact, run the
  required Claude review loop yourself, implement the reviewed repair when it
  passes, and continue to the phase gate.
- Stop only for true human intervention under the runbook: incompatible target
  definitions, infeasible reference route under declared resources,
  license/governance uncertainty, trusted infrastructure unavailable, or
  max-five review exhaustion without explicit PASS.
- If you stop for human intervention, write the required STOP result note and
  do not emit the phase pass token.
- The phase gate is executed from the read-only trusted gate copy outside the
  worker-writable launch workspace using:
  ${TRUSTED_GATE_SCRIPT}
  Its SHA-256 is checked immediately before each phase gate when
  TRUSTED_GATE_SHA256 is set.
  Do not modify gate scripts; any attempted gate-script change is a governance
  failure, not a repair route.
- Perform and record the skeptical plan audit before implementation.
- Preserve P42/P44 target, parameterization, baseline, and nonclaim governance.
- Use CPU-only commands by default: CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp.
- Treat prelaunch tracked-dirty paths as protected:
  ${DIRTY_TRACKED_MANIFEST}
- Do not modify protected already-dirty tracked files unless a human explicitly authorizes it.
- If you encounter a fixable blocker, write a repair amendment/result note and run Claude repair review with explicit PASS before implementing the repair.
- Review loops may run at most five iterations; max-five exhaustion without explicit PASS writes a stop note and does not authorize progression.
- Create or update phase result and Claude review ledger artifacts under docs/plans.
- The required current-run phase result note is:
  ${result_note}
- The required current-run phase Claude review ledger is:
  ${review_ledger}
- The required current-run evidence manifest is:
  ${manifest}
- Both required artifacts must include:
  run_id: \`${RUN_ID}\`
- Both required artifacts' latest Status/status/Verdict line must equal:
  \`${token}\`
- The evidence manifest must be JSON with schema_version
  "p44.phase_evidence.v1", run_id "${RUN_ID}", phase "${phase}", pass_token
  "${token}", status "${token}", artifact_paths for result_note,
  claude_review_ledger, and evidence_manifest, all ten evidence_chain states
  set to true, a nonempty evidence_contract, at least one successful command,
  diagnostics.veto_status of PASS or NONCLAIM_RECORDED, review_loops with
  claude_code_governance.iterations between 1 and 5 and verdict "${token}",
  repair.iterations between 0 and 5, and long_run_controls with caps and
  pre_mortem whenever long_run_used is true.
- The phase result note must contain anchored machine-check markers:
  p44_evidence_manifest: \`${manifest}\`
  p44_local_evidence_run: \`COMPLETE\`
  p44_evidence_audit: \`COMPLETE\`
  p44_result_note_substance: \`COMPLETE\`
  p44_traceability_or_nonclaim: \`COMPLETE\`
  p44_command_count: \`<number of manifest commands>\`
  p44_long_run_used: \`true\` or \`false\`
  and when p44_long_run_used is true, also:
  p44_long_run_resource_caps: \`COMPLETE\`
  p44_long_run_pre_mortem: \`COMPLETE\`
- The phase Claude review ledger must contain anchored machine-check markers:
  p44_evidence_manifest: \`${manifest}\`
  p44_claude_code_governance_verdict: \`${token}\`
  p44_claude_code_governance_iterations: \`<1..5>\`
- The phase Claude review ledger must also contain machine-parseable review
  records for code/governance review:
  review_cycle: \`<integer>\`
  review_type: \`code_governance\`
  review_iteration: \`<strictly increasing integer 1..5>\`
  status: \`${token}\`
  The latest such status must equal the phase pass token. If repair review was
  needed, the manifest repair iteration count must match the latest explicit
  bounded repair PASS record in a separate repair stream in the same ledger:
  review_cycle: \`<integer>\`
  review_type: \`repair\`
  review_iteration: \`<strictly increasing integer 1..5>\`
  status: \`PASS_${phase//-/_}_REPAIR_REVIEW\`
  The repair stream must have no duplicate, reset, decreasing, or out-of-range
  repair review iterations.
- Every manifest command must have a relative log_path. Each command log must
  exist and contain:
  p44_run_id: \`${RUN_ID}\`
  p44_phase: \`${phase}\`
  p44_command_index: \`<zero-based command index>\`
  p44_command_exit_code: \`0\`
- Do not complete this phase unless the phase result/review artifacts contain exactly this pass token:
  ${token}
- If the phase requires human intervention, write a STOP result note with the exact reason and do not emit the pass token.
PROMPT

  echo "=== ${phase} start: ${description} ==="
  if ! env \
    CLAUDE_WORKER_SETTINGS="$SETTINGS" \
    CLAUDE_WORKER_PERMISSION_MODE=acceptEdits \
    bash "$WORKER" --cwd "$ROOT" --name "${RUN_ID}-${phase}" --permission-mode acceptEdits "$(cat "$phase_prompt")" > "$phase_log" 2>&1; then
    echo "phase worker failed for ${phase}; see ${phase_log}" >&2
    exit 20
  fi

  if [[ -n "$TRUSTED_GATE_SHA256" ]]; then
    actual_gate_sha256="$(sha256sum "$TRUSTED_GATE_SCRIPT")"
    actual_gate_sha256="${actual_gate_sha256%% *}"
    if [[ "$actual_gate_sha256" != "$TRUSTED_GATE_SHA256" ]]; then
      echo "trusted phase gate hash changed before ${phase}" >&2
      exit 22
    fi
  fi
  if ! python "$TRUSTED_GATE_SCRIPT" --root "$ROOT" --phase "$phase" --token "$token" --run-id "$RUN_ID"; then
    echo "phase gate failed for ${phase}; required token ${token} not found" >&2
    echo "see ${phase_log}" >&2
    exit 21
  fi
  echo "=== ${phase} pass: ${token} ==="
done
