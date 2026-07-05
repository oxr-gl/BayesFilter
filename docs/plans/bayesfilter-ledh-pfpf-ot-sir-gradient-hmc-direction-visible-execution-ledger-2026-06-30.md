# SIR Gradient HMC-Direction Visible Execution Ledger

Date: 2026-06-30

Status: `INITIALIZED`

## Ledger

### 2026-06-30T17:58:00+08:00 - Phase 0 - PRECHECK

Evidence contract:

- Question: What exact SIR route and diagnostics are available for the SIR
  gradient program?
- Baseline/comparator: local source inventory of P8p scripts and tests.
- Primary criterion: active route, default flags, route vetoes, existing
  checks, and output artifacts are identified accurately.
- Veto diagnostics: missing scripts, syntax failure, manual score unit failure,
  or discovery that the intended material route is not GPU/XLA/TF32 capable.
- Non-claims: no gradient correctness, FD correctness, HMC readiness,
  posterior validity, or production budget promotion.

Skeptical audit:

- Wrong baseline: Phase 0 does not use numerical SIR results as correctness
  evidence.
- Proxy metrics: none promoted in Phase 0.
- Environment mismatch: CPU-hidden unit test is allowed only as tiny wiring
  evidence; material GPU evidence is deferred to Phase 3.
- Artifact adequacy: Phase 0 will write a route inventory result and refresh
  Phase 1 if needed.

Actions:

- Launch Phase 0 visibly after local plan checks and Claude review convergence.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase0-route-inventory-subplan-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase0-route-inventory-result-2026-06-30.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run Phase 0 local checks and write route inventory result.

### 2026-06-30T18:02:00+08:00 - Phase 0 - ASSESS_GATE

Actions:

- Ran py_compile for active P8p SIR diagnostics.
- Ran tiny CPU-hidden manual-score pytest.
- Ran route inventory grep for manual reverse, XLA compiler metadata, TF32,
  GPU expectation, FD slope SE, seed-gradient MCSE, row residual, and manual
  streaming transport constants.
- Wrote Phase 0 result.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase0-route-inventory-result-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-claude-review-ledger-2026-06-30.md`

Gate status:

- `PASSED`

Next action:

- Refresh Phase 1 wording cleanup, run focused checks, and enter Phase 1 under
  the visible state machine if no blocker appears.

### 2026-06-30T18:04:00+08:00 - Phase 1 - PRECHECK

Evidence contract:

- Question: What SIR-specific gate can classify the manual reverse score as
  HMC-direction useful without overclaiming exact correctness?
- Baseline/comparator: same fixed-randomness 13-point regression FD in raw
  theta directions, with slope SE and seed-gradient MCSE.
- Primary criterion: written gate separates route validity, derivative
  agreement, MCSE/FD uncertainty, relative-error support, precision vetoes, and
  row residual vetoes.
- Veto diagnostics: treating FD as exact truth, hiding row residuals, using
  CPU route, omitting MCSE or slope SE, or changing thresholds after material
  Phase 4 results.
- Non-claims: no exact SIR gradient proof, no posterior correctness, no
  nonlinear-model validation, no HMC/NUTS readiness.

Skeptical audit:

- Wrong baseline: Phase 1 explicitly uses regression FD only as fixed-randomness
  comparator, not an exact oracle.
- Proxy metrics: relative error is supportive only; pass arms require combined
  uncertainty and precision floor.
- Environment mismatch: material GPU execution is still deferred; this phase
  defines the gate and checks field availability.
- Artifact adequacy: Phase 1 will write a result and refresh Phase 2.

Actions:

- Applied nonblocking wording cleanup requested by Claude Round 3, separating
  supportive labels from pass arms.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-subplan-2026-06-30.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run Phase 1 local field-availability check and write Phase 1 gate result.

### 2026-06-30T18:08:00+08:00 - Phase 1 - ASSESS_GATE

Actions:

- Ran Phase 1 field-availability `rg` check.
- Ran focused `git diff --check`.
- Wrote Phase 1 gate result.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-result-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-subplan-2026-06-30.md`

Gate status:

- `PASSED`

Next action:

- Refresh Phase 2 subplan for the Phase 1 gate fields, then enter Phase 2.

### 2026-06-30T18:11:00+08:00 - Phase 2 - PRECHECK

Evidence contract:

- Question: Does the diagnostic emit the fields needed to apply the SIR
  HMC-direction gate without manual reinterpretation?
- Baseline/comparator: Phase 1 gate contract and existing P8p diagnostic
  schema.
- Primary criterion: local checks pass and the diagnostic schema records route,
  `combined_se`, `precision_pass`, pass/veto reason, supportive labels, and
  nonclaims.
- Veto diagnostics: missing route fields, missing pass/veto reason, missing
  `combined_se` or `precision_pass`, missing nonclaims, or test/script logic
  divergence.
- Non-claims: no GPU performance, no material SIR gradient result, no HMC
  readiness.

Actions:

- Implemented SIR HMC-direction gate reporting and focused tests.
- Ran local checks.
- Sent implementation to Claude read-only review.
- Patched route-prerequisite veto after Claude Round 1.
- Reran checks and received Claude Round 2 `VERDICT: AGREE`.

Artifacts:

- `docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py`
- `tests/test_p8p_sir_hmc_direction_gate.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase2-diagnostic-reporting-result-2026-06-30.md`

Gate status:

- `PASSED`

Next action:

- Enter Phase 3 trusted GPU/XLA/TF32 route smoke.

### 2026-06-30T18:17:00+08:00 - Phase 3 - PRECHECK

Evidence contract:

- Question: Does the SIR manual reverse route run under trusted GPU/XLA/TF32
  and emit finite route metadata?
- Baseline/comparator: route metadata and finite AD-only manual reverse score,
  not FD agreement.
- Primary criterion: escalated GPU visible, tensors on GPU, TF32 enabled,
  compiler XLA, manual score route, finite objective/score/MCSE, and route
  prerequisites pass.
- Veto diagnostics: CPU tensors, XLA disabled, TF32 disabled, nonfinite score,
  dense/full transport autodiff, missing metadata, or failed route
  prerequisite gate.
- Non-claims: no FD agreement, no material SIR gradient validation, no HMC
  readiness.

Skeptical audit:

- Wrong baseline: this is a route smoke only and will not compare to FD.
- Proxy metrics: finite score/MCSE are route viability checks, not correctness.
- Environment mismatch: commands use escalated execution per `AGENTS.md`.
- Artifact adequacy: JSON output must preserve device, compiler, score route,
  TF32, and route metadata.

Gate status:

- `IN_PROGRESS`

Next action:

- Run escalated `nvidia-smi` and GPU/XLA/TF32 AD-only smoke.

### 2026-06-30T19:24:00+08:00 - Phase 3 - REPAIR_LOOP

Issue:

- The first escalated GPU smoke used
  `benchmark_p8p_regression_fd_reparameterization.py --fd-mode ad-only`.
  It validated GPU/XLA/TF32 manual reverse execution, but that script does not
  emit the Phase 2 `route_prerequisites` field.

Repair:

- Updated the Phase 3 subplan to use a tiny one-budget
  `diagnose_p8p_sir_sinkhorn_budget.py` smoke so the exact Phase 2 route gate
  is exercised.
- Preserved the completed regression-script smoke as supporting route evidence
  only, not as the Phase 3 gate artifact.

Gate status:

- `IN_PROGRESS`

Next action:

- Run the repaired Phase 3 diagnostic smoke with trusted GPU execution.

### 2026-06-30T19:28:00+08:00 - Phase 3 - BLOCKED

Actions:

- Ran escalated `nvidia-smi`; GPU visible.
- Ran escalated regression-script AD-only GPU/XLA/TF32 manual reverse route
  smoke successfully.
- Repaired Phase 3 subplan because the regression script did not emit the new
  Phase 2 `route_prerequisites` field.
- Attempted the repaired `diagnose_p8p_sir_sinkhorn_budget.py` GPU smoke twice
  with escalation.

Artifacts:

- Supporting route smoke:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.json`
- Phase 3 result/blocker:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-result-2026-06-30.md`

Gate status:

- `BLOCKED_ESCALATION_APPROVAL_TIMEOUT_FOR_REPAIRED_GPU_SMOKE`

Next action:

- Ask user for explicit approval/guidance before retrying the repaired bounded
  GPU diagnostic.

### 2026-06-30T19:35:00+08:00 - Phase 3 - RESUME_AFTER_HUMAN_APPROVAL

Human approval:

- User explicitly approved retrying the bounded repaired Phase 3 GPU
  diagnostic after the escalation approval timeout blocker.

Actions:

- Resume Phase 3 from
  `BLOCKED_ESCALATION_APPROVAL_TIMEOUT_FOR_REPAIRED_GPU_SMOKE`.

Gate status:

- `IN_PROGRESS`

Next action:

- Rerun the repaired `diagnose_p8p_sir_sinkhorn_budget.py` GPU/XLA/TF32 smoke
  with escalation and inspect `route_prerequisites.route_prerequisite_pass`.

### 2026-06-30T19:38:00+08:00 - Phase 3 - REPAIR_LOOP

Issue:

- The direct long repaired Phase 3 GPU command still timed out in the
  automatic escalation approval review after human approval.

Repair:

- Added `scripts/run_sir_gradient_phase3_gpu_smoke.sh` containing the exact
  bounded repaired Phase 3 command, to make the escalation request shorter and
  more auditable.

Gate status:

- `IN_PROGRESS`

Next action:

- Run the wrapper script with escalation.

### 2026-06-30T19:53:00+08:00 - Phase 3 - REPAIR_LOOP

Issue:

- The wrapper launched under trusted GPU execution but failed argument parsing:
  `--regression-offsets -3,-2,-1,0,1,2,3` was parsed as an option-like token.
- The wrapper also still included `--transport-plan-mode` and
  `--transport-ad-mode`, which are fixed internally by
  `diagnose_p8p_sir_sinkhorn_budget.py` rather than exposed as CLI flags.

Repair:

- Changed to `--regression-offsets=-3,-2,-1,0,1,2,3`.
- Removed the non-exposed fixed-internal transport CLI flags.

Gate status:

- `IN_PROGRESS`

Next action:

- Rerun the wrapper script with escalation.

### 2026-06-30T20:09:00+08:00 - Phase 3 - ASSESS_GATE

Question:

- Did the repaired SIR Sinkhorn budget diagnostic itself exercise and pass the
  Phase 2 route prerequisite gate under trusted GPU/XLA/TF32 execution?

Command:

```bash
bash scripts/run_sir_gradient_phase3_gpu_smoke.sh
```

Artifact:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.md`

Focused local check:

```bash
python - <<'PY'
import json, math
from pathlib import Path
p = Path('docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.json')
data = json.loads(p.read_text())
r = data['records'][0]
route = r['route_prerequisites']
checks = route['checks']
required = [
    'device_scope_visible',
    'expect_device_kind_gpu',
    'outputs_on_gpu',
    'dtype_float32',
    'tf32_enabled',
    'manual_reverse_compiler_xla',
    'compiler_jit_compile',
    'manual_score_route',
    'streaming_transport_plan',
    'stabilized_transport_ad',
    'manual_streaming_transport_gradient',
    'finite_objective',
    'finite_gradient',
]
missing = [k for k in required if not checks.get(k)]
assert route['route_prerequisite_pass'] is True
assert not route['failed_checks']
assert not missing
assert math.isfinite(r['transport']['objective'])
assert r['transport']['row_residual_pass'] is True
print('PHASE3_ROUTE_GATE_PASS')
PY
```

Observed gate facts:

- `route_prerequisite_pass`: `true`
- `failed_checks`: `[]`
- `compiler.mode`: `xla`
- `compiler.jit_compile`: `true`
- `score_route`: `manual_reverse_scan_no_autodiff`
- `output_devices`: GPU for objective and gradient tensors.
- `precision.tf32_execution_enabled`: `true`
- `max_row_residual`: `3.933906555175781e-06`
- `row_residual_pass`: `true`

Gate status:

- `PASSED`

Nonclaims:

- The tiny Phase 3 smoke does not validate SIR gradient accuracy.
- Phase 4 remains the first material SIR gradient diagnostic.

Next action:

- Refresh Phase 4 to use a wrapper with corrected CLI syntax and run Claude
  read-only review before the material GPU/XLA/TF32 diagnostic.

### 2026-06-30T20:10:00+08:00 - Phase 4 - PRECHECK

Objective:

- Prepare the material SIR gradient diagnostic after Phase 3 route smoke
  passed.

Skeptical pre-run audit:

- Status: `PASS_WITH_CONSTRAINTS`.
- The Phase 4 command varies only Sinkhorn budget across
  `10,100,200,400` while holding route, seeds, theta, chunks, dtype, TF32, and
  fixed-randomness FD contract constant.
- The Phase 1 HMC-direction gate remains frozen; relative error, row residual,
  R2, and runtime remain explanatory unless the gate explicitly uses them.
- Route mismatch is a veto: CPU, non-GPU outputs, non-XLA, non-TF32, or wrong
  manual score route cannot produce material evidence.
- `N=64`, `T=3`, five seeds is a first material diagnostic, not a global
  finite-N exclusion.

Repairs before execution:

- Added `scripts/run_sir_gradient_phase4_material_diagnostic.sh`.
- Corrected negative offset syntax to
  `--regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6`.
- Omitted fixed-internal `--transport-plan-mode` and `--transport-ad-mode`
  CLI flags.
- Added progress artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-progress-2026-06-30.json`.

Local checks:

```bash
bash -n scripts/run_sir_gradient_phase4_material_diagnostic.sh
python -m py_compile docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
rg -n "transport-plan-mode|transport-ad-mode|--regression-offsets " scripts/run_sir_gradient_phase4_material_diagnostic.sh docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-subplan-2026-06-30.md
```

Result:

- Shell syntax passed.
- Diagnostic compile passed.
- `rg` found the forbidden CLI flags only in explanatory prose, not in the
  executable wrapper.

Gate status:

- `READY_FOR_CLAUDE_REVIEW`

### 2026-06-30T20:13:00+08:00 - Phase 4 - CLAUDE_REVIEW

First review prompt:

- A broad review prompt over five files produced no output in the expected
  window.

Probe:

```bash
bash scripts/claude_worker.sh --name sir-gradient-phase4-probe --model opus --effort max "Read-only probe. Reply with exactly PROBE_OK."
```

Probe result:

- `PROBE_OK`

Repair:

- Replaced the broad prompt with a narrower two-file review scoped to the Phase
  4 subplan and wrapper.

Narrow review result:

- `VERDICT: AGREE`

Claude findings:

- Wrapper CLI syntax is sound and uses the protected negative-offset form.
- Wrapper and subplan match on GPU/XLA/TF32 route, `N=64`, `T=3`, five seeds,
  and output artifacts.
- Forbidden-claim boundaries and stop conditions are present.

Gate status:

- `READY_FOR_MATERIAL_GPU_RUN`

### 2026-06-30T20:15:00+08:00 - Phase 4 - BLOCKED

Attempted command:

```bash
bash scripts/run_sir_gradient_phase4_material_diagnostic.sh
```

Issue:

- The first escalated launch was rejected because automatic permission approval
  review did not finish before its deadline.
- The one policy-allowed retry of the same bounded wrapper also timed out in
  automatic permission approval review.

Classification:

- `BLOCKED_ESCALATION_APPROVAL_TIMEOUT_FOR_PHASE4_GPU_DIAGNOSTIC`

Important non-evidence:

- The Phase 4 diagnostic did not start.
- No GPU runtime, XLA, memory, numerical, or SIR-gradient conclusion can be
  drawn from this approval-layer timeout.

Required next step:

- Ask the user for explicit approval/guidance for this exact bounded wrapper
  command before retrying again:
  `bash scripts/run_sir_gradient_phase4_material_diagnostic.sh`.

### 2026-06-30T20:56:00+08:00 - Phase 4 - RESUME_AFTER_HUMAN_CONTINUE

Human instruction:

- User said `continue`.

Action:

- Retried the exact reviewed Phase 4 wrapper with trusted GPU execution.
- First post-continue attempt hit the automatic permission approval timeout.
- One same-command retry started successfully.

Route evidence before failure:

- TensorFlow created `/device:GPU:0` on NVIDIA GeForce RTX 4080 SUPER.
- XLA service initialized for CUDA.
- XLA compiled the manual route cluster.

Runtime outcome:

- The diagnostic completed budget 10 progress and started budget 100.
- Process was killed with exit code `137` during budget 100.

Partial progress artifact:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-progress-2026-06-30.json`

Partial progress:

- budget `10` completed;
- `max_row_residual`: `1.4185905456542969e-05`;
- `max_abs_fd_z`: `441.06424461688147`;
- final Phase 4 JSON/Markdown artifacts were not written.

Classification:

- `BLOCKED_EXIT137_DURING_PHASE4_BUDGET100`

Interpretation boundary:

- This is a runtime/memory blocker after correct GPU/XLA route launch, not a
  wiring failure and not a completed material gradient result.
- The budget-10 progress is an early warning that small row residual alone does
  not remove the gradient gap, but it is partial evidence only because the
  Phase 4 artifact did not complete.

### 2026-06-30T21:12:00+08:00 - Phase 4 - REPAIR_LOOP

Repair hypothesis:

- The exit-137 kill occurred during the heavier budget-100 batched evaluation.
  The script supports exact runtime chunking through seed microbatching and
  theta-offset batching.

Repair:

- Patched `scripts/run_sir_gradient_phase4_material_diagnostic.sh` to add:
  - `--seed-microbatch-size 1`
  - `--theta-offset-batch-size 2`
- Patched the Phase 4 subplan to document that this is an execution-shape
  repair preserving seeds, theta offsets, budgets, route, regression, and gate.

Local checks:

```bash
bash -n scripts/run_sir_gradient_phase4_material_diagnostic.sh
python -m py_compile docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
rg -n "seed-microbatch-size|theta-offset-batch-size|REPAIRED_AFTER_EXIT137|exit code 137|regression-offsets" scripts/run_sir_gradient_phase4_material_diagnostic.sh docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-subplan-2026-06-30.md
```

Result:

- Shell syntax passed.
- Diagnostic compile passed.
- Repaired chunking flags and subplan documentation are present.

Gate status:

- `READY_FOR_CLAUDE_REPAIR_REVIEW`

### 2026-06-30T21:18:00+08:00 - Phase 4 - CLAUDE_REPAIR_REVIEW

Broad prompt:

- A broader four-file prompt remained silent and was interrupted, consistent
  with the earlier broad-prompt issue.

Narrow repair review:

- Scope:
  - `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-subplan-2026-06-30.md`
  - `scripts/run_sir_gradient_phase4_material_diagnostic.sh`
- Verdict: `VERDICT: AGREE`

Claude findings:

- Wrapper and subplan both include exactly `--seed-microbatch-size 1` and
  `--theta-offset-batch-size 2`.
- Route-defining controls remain GPU, float32, TF32 enabled, XLA manual
  reverse, same seeds, same budgets, same theta, same FD offsets, and same
  transport gradient mode.
- Artifact coverage and execution-shape-only boundary are consistent.

Codex semantic trace:

- `benchmark_p8p_regression_fd_reparameterization._build_microbatch_contexts`
  partitions fixed seeds and records the exact seed groups.
- `_manual_gradient_diagnostic_for_contexts` concatenates per-seed gradients
  across contexts and takes the same mean over per-seed gradients.
- `_value_at_theta_rows` recursively chunks theta rows when
  `theta_offset_batch_size > 0`, concatenates the resulting objective values,
  and then the same FD regression/gate logic is applied.

Gate status:

- `READY_FOR_REPAIRED_MATERIAL_GPU_RUN`

### 2026-06-30T22:58:00+08:00 - Phase 4 - CLOSE_BLOCKER

Outcome:

- The repaired chunked Phase 4 wrapper also exited with code 137.
- It completed budget 10 and started budget 100, but host memory and swap were
  essentially exhausted before the process was killed.

Phase result:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-result-2026-06-30.md`

Final Phase 4 status:

- `BLOCKED_EXIT137_MEMORY_DURING_BUDGET100`

Handoff:

- Advance to Phase 5 per-budget process isolation.

### 2026-06-30T23:00:00+08:00 - Phase 5 - PRECHECK

Objective:

- Repair Phase 4 memory accumulation by running one Sinkhorn budget per trusted
  GPU/XLA/TF32 Python process.

Artifacts added:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-subplan-2026-06-30.md`
- `scripts/run_sir_gradient_phase5_budget10.sh`
- `scripts/run_sir_gradient_phase5_budget100.sh`

Skeptical pre-run audit:

- Status: `PASS_WITH_CONSTRAINTS`.
- The only intended change is the process boundary: budget 10 and budget 100
  are run in separate Python processes.
- Seeds, theta, FD offsets, dtype, TF32 mode, compiler mode, transport
  gradient mode, row/column/particle chunks, and the Phase 1 gate remain fixed.
- Budget 10 must be regenerated as a complete Phase 5 artifact; Phase 4
  partial progress is explanatory only.
- Budget 200/400 are forbidden until budget 100 completes and the result says
  they remain necessary and feasible.

Local checks:

```bash
bash -n scripts/run_sir_gradient_phase5_budget10.sh
bash -n scripts/run_sir_gradient_phase5_budget100.sh
python -m py_compile docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
rg -n "candidate-steps|phase5-budget|device-scope|manual-reverse-compiler|tf32-mode|regression-offsets" scripts/run_sir_gradient_phase5_budget10.sh scripts/run_sir_gradient_phase5_budget100.sh docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-subplan-2026-06-30.md
```

Result:

- Both wrappers passed shell syntax checks.
- Diagnostic compile passed.
- `rg` confirmed budget-specific wrappers and route/gate-relevant flags.

Gate status:

- `READY_FOR_CLAUDE_PHASE5_REVIEW`

### 2026-06-30T23:04:00+08:00 - Phase 5 - CLAUDE_REVIEW_ROUND_1

Verdict:

- `VERDICT: FIX`

Finding:

- The Phase 5 wrappers omitted the Phase 4 reviewed chunking knobs
  `--seed-microbatch-size 1` and `--theta-offset-batch-size 2`, so process
  boundary would not have been the only runtime-shape change.

Repair:

- Added both flags to:
  - `scripts/run_sir_gradient_phase5_budget10.sh`
  - `scripts/run_sir_gradient_phase5_budget100.sh`
- Updated Phase 5 subplan baseline and forbidden-change sections.

Focused checks:

```bash
bash -n scripts/run_sir_gradient_phase5_budget10.sh
bash -n scripts/run_sir_gradient_phase5_budget100.sh
python -m py_compile docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
rg -n "seed-microbatch-size|theta-offset-batch-size|process boundary|Baseline/comparator|Do not change seeds" scripts/run_sir_gradient_phase5_budget10.sh scripts/run_sir_gradient_phase5_budget100.sh docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-subplan-2026-06-30.md
```

Result:

- Checks passed.

Gate status:

- `READY_FOR_CLAUDE_PHASE5_REVIEW_ROUND_2`

### 2026-06-30T23:06:00+08:00 - Phase 5 - CLAUDE_REVIEW_ROUND_2

Verdict:

- `VERDICT: AGREE`

Finding:

- Prior blocker fixed; both wrappers now preserve
  `--seed-microbatch-size 1` and `--theta-offset-batch-size 2`.
- No new material issue found in reviewed scope.

Gate status:

- `READY_FOR_PHASE5_BUDGET10_GPU_RUN`

### 2026-07-01T00:21:00+08:00 - Phase 5 - BUDGET10_RESULT

Command:

```bash
bash scripts/run_sir_gradient_phase5_budget10.sh
```

Approval/runtime notes:

- First escalated launch timed out in automatic approval review.
- One same-command retry started successfully.
- GPU device was created, XLA initialized for CUDA, and XLA compiled the manual
  route.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-progress-2026-06-30.json`

Runtime:

- `elapsed_seconds`: `1611.4168632070068`

Gate facts:

- `route_prerequisite_pass`: `true`
- `failed_checks`: `[]`
- `max_row_residual`: `1.4722347259521484e-05`
- `row_residual_pass`: `true`
- `all_raw_directions_hmc_direction_pass`: `false`
- `max_abs_combined_z`: `2.8281962476351596`

Direction classification:

- `log_kappa_scale`: `inconclusive_precision_veto`
  - manual `-143.36988830566406`
  - FD `-263.1854553222656`
  - combined SE `48.95107737607928`
  - combined z `2.447659447739782`
  - precision pass `false`
- `log_nu_scale`: `within_4_combined_se_requires_ladder_certificate`
  - manual `68.2666244506836`
  - FD `105.05280303955078`
  - combined SE `13.006939889559122`
  - combined z `-2.8281962476351596`
  - precision pass `true`
- `log_obs_noise_scale`: `within_2_combined_se`
  - manual `46.060081481933594`
  - FD `46.76679992675781`
  - combined SE `0.5469644182744133`
  - combined z `-1.292073892217348`
  - precision pass `true`

Interpretation:

- Budget 10 is a complete material artifact.
- Row residual convergence alone does not explain the remaining gradient
  concern at budget 10.
- Budget 100 remains the next planned discriminator, because it can test
  whether higher Sinkhorn budget provides the ladder certificate or changes the
  direction classification.

Gate status:

- `READY_FOR_PHASE5_BUDGET100_GPU_RUN`
