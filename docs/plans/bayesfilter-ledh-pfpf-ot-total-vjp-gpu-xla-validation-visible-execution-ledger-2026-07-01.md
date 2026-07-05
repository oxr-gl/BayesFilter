# Visible Execution Ledger: Total-VJP GPU/XLA Validation

Date: 2026-07-01

Status: `COMPLETE`

## Ledger

### 2026-07-01 - Program Initialization - PRECHECK

Evidence contract:

- Question: Can the corrected total-derivative finite-Sinkhorn route run under
  trusted GPU/XLA/TF32 and scale enough for the next SIR direction gate?
- Baseline/comparator: CPU float64 same-finite-scalar repair artifact.
- Primary criterion: each phase passes its reviewed evidence gate.
- Veto diagnostics: CPU fallback, XLA missing, `transport_ad_mode!="full"`,
  stopped partial route treated as score, nonfinite outputs, OOM, unsupported
  claims.
- Non-claims: no HMC readiness, no posterior correctness, no production
  promotion.

Actions:

- Created draft master program, phase subplans, visible runbook, ledger, and
  stop handoff.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-master-program-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-visible-gated-execution-runbook-2026-07-01.md`

Gate status:

- `IN_PROGRESS`

Next action:

- Run local plan checks and Claude read-only review before Phase 0 execution.

### 2026-07-01 - Pre-Phase 0 - SKEPTICAL_AUDIT_AND_LOCAL_CHECKS

Skeptical audit:

- Wrong baseline checked: the stopped partial derivative is not a correctness
  baseline.  GPU phases test viability of the corrected full route only.
- Proxy metric checked: finite GPU gradients are viability evidence, not HMC
  readiness or posterior correctness.
- Environment mismatch checked: GPU/CUDA and Claude commands require trusted
  execution; non-escalated failures must not be treated as hardware evidence.
- Route metadata checked: Phase 1 must fail unless Phase 0 records static
  dispatch proof and output records `transport_ad_mode="full"`, GPU tensors,
  and XLA JIT.
- Stale naming checked: the current CLI gradient-mode string contains
  `stopped_scale_keys`; Phase 1 now states that the derivative claim depends on
  `transport_ad_mode="full"`, not the legacy selector name.

Actions:

- Ran compile checks for the benchmark, comparator, transport, and batched core
  Python files.  Result: passed.
- Ran focused pytest suite:
  `tests/test_p8p_sir_active_transport_comparator_contract.py`,
  `tests/test_ledh_pfpf_ot_p7_manual_score.py`,
  `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`.
  Result: `36 passed, 2 warnings`.

Artifacts:

- Updated Phase 1 subplan wording around the legacy gradient-mode selector.

Gate status:

- `LOCAL_CHECKS_PASSED`

Next action:

- Run Claude health probe and bounded read-only review of the master program,
  runbook, and Phase 0/Phase 1 subplans.

### 2026-07-01 - Phase 0 - EXECUTE_MINIMAL_AND_ASSESS_GATE

Evidence contract:

- Question: Are artifacts, local checks, static dispatch proof, and trusted GPU
  visibility sufficient to launch the tiny GPU/XLA full-route smoke?
- Baseline/comparator: CPU float64 total-VJP repair artifact.
- Primary criterion: local checks pass, dispatch proof is recorded, trusted GPU
  is visible, Phase 1 subplan is ready.
- Veto diagnostics: missing proof, compile/test failure, GPU not visible.
- Non-claims: no GPU/XLA viability of the corrected route yet.

Actions:

- Ran trusted `nvidia-smi`.
- Ran trusted TensorFlow GPU probe.
- Extracted static code anchors proving the Phase 1 selector pair reaches
  `_filterflow_manual_streaming_finite_transport_total_vjp`.
- Wrote Phase 0 result.
- Refreshed Phase 1 subplan status.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase0-route-inventory-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-subplan-2026-07-01.md`

Gate status:

- `PASSED_PENDING_CLAUDE_RESULT_REVIEW`

Next action:

- Send Phase 0 result and refreshed Phase 1 subplan to Claude read-only review.

### 2026-07-01 - Phase 1 - LAUNCH_BLOCKER

Evidence contract:

- Question: Can the reviewed Phase 1 trusted GPU/XLA smoke launch and produce a
  JSON artifact?
- Primary criterion: command starts in trusted GPU context and writes the Phase
  1 JSON.
- Veto diagnostics: approval timeout before command start, CPU fallback,
  nonfinite output, wrong route metadata.
- Non-claims: no route failure unless the command actually runs and fails.

Actions:

- Direct trusted GPU command attempt returned an approval-review timeout.
- Wrote `scripts/run_total_vjp_gpu_xla_phase1_smoke.sh` with the exact reviewed
  command.
- `bash -n scripts/run_total_vjp_gpu_xla_phase1_smoke.sh` passed.
- Wrapper trusted GPU launch also returned an approval-review timeout.
- Wrote Phase 1 launch blocker.

Artifacts:

- `scripts/run_total_vjp_gpu_xla_phase1_smoke.sh`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-launch-blocker-2026-07-01.md`

Gate status:

- `BLOCKED_REQUIRES_HUMAN_APPROVAL`

Next action:

- Ask user to explicitly approve trusted execution of
  `bash scripts/run_total_vjp_gpu_xla_phase1_smoke.sh`.

### 2026-07-01 - Phase 1 - TRUSTED_GPU_XLA_SMOKE_PASS

Evidence contract:

- Question: Can the corrected `transport_ad_mode="full"` manual route run
  under trusted GPU/XLA/TF32 at tiny SIR size?
- Primary criterion: Phase 0 dispatch proof is present; GPU tensors, XLA JIT
  manual-reverse unit, `transport_ad_mode="full"`, finite objective, finite
  gradient, finite MCSE, and output artifact present.
- Veto diagnostics: CPU fallback, XLA not used, route metadata not full,
  stopped partial route claimed as score, nonfinite output, missing artifact.
- Non-claims: no material particle-count viability, no HMC readiness, no
  posterior correctness, no production promotion.

Actions:

- User approved trusted execution after the earlier approval-review timeout.
- Ran `bash scripts/run_total_vjp_gpu_xla_phase1_smoke.sh` in trusted GPU
  context.
- TensorFlow created `/device:GPU:0` on the RTX 4080 SUPER and compiled the
  manual-reverse unit with XLA.
- Ran an explicit JSON gate check against the Phase 1 output.
- Wrote Phase 1 result.
- Wrote Phase 2 skipped result because no harness repair was needed.
- Refreshed Phase 3 particle ladder subplan with exact commands and JSON gates.

Key output:

- `status`: `pass`
- `primary_pass`: `True`
- `compiler.mode`: `xla`
- `compiler.jit_compile`: `True`
- `transport.transport_ad_mode`: `full`
- `objective`: `-36.1256103515625`
- `gradient_values`: `[-9.37370777130127, 3.432502508163452, 4.548910617828369]`
- `monte_carlo_gradient_noise_mcse_finite`: `True`
- `elapsed_seconds`: `48.501640795962885`

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase2-harness-repair-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-particle-ladder-subplan-2026-07-01.md`

Gate status:

- `PASSED_PENDING_CLAUDE_RESULT_REVIEW`

Next action:

- Send Phase 1 result, Phase 2 skipped result, and refreshed Phase 3 subplan
  to Claude read-only review.

### 2026-07-01 - Pre-Phase 3 - SKEPTICAL_AUDIT_AND_CLAUDE_REVIEW

Skeptical audit:

- Wrong baseline checked: the stopped partial derivative remains excluded as a
  correctness baseline.
- Proxy metric checked: finite gradients, runtime, and memory are viability
  evidence only; Phase 3 cannot certify HMC direction quality.
- Missing stop conditions checked: the Phase 3 subplan stops on OOM, repeated
  XLA failure, nonfinite gradient/objective, and unsafe `N=1000` continuation.
- Environment mismatch checked: every rung must run under trusted GPU
  execution; CPU fallback is a veto.
- Artifact relevance checked: each rung writes a JSON artifact that records
  device placement, compiler mode, route metadata, objective, gradients, and
  MCSE.  These artifacts answer the Phase 3 viability question.

Claude review:

- Bounded read-only review of the Phase 1 result, Phase 2 skipped result, and
  refreshed Phase 3 subplan returned `VERDICT: AGREE`.

Gate status:

- `PHASE3_READY_TO_EXECUTE`

Next action:

- Launch Phase 3 rungs sequentially under trusted GPU/XLA, gating after each
  rung before advancing.

### 2026-07-01 - Phase 3 - PARTICLE_LADDER_PASS

Evidence contract:

- Question: At what particle count does the corrected full route remain finite
  and operational under GPU/XLA?
- Primary criterion: each rung passes finite value/gradient/MCSE and route
  metadata gates without OOM or CPU fallback.
- Veto diagnostics: OOM, XLA failure, CPU fallback, nonfinite output,
  route metadata not full, runtime beyond planned budget.
- Non-claims: no HMC direction validity, no posterior correctness, no exact
  nonlinear likelihood correctness.

Actions:

- Ran and gated `N=16,T=1,seeds=2`.
- Ran and gated `N=64,T=3,seeds=5`.
- Ran and gated `N=256,T=3,seeds=5`.
- Ran and gated conditional `N=1000,T=3,seeds=5`.
- Wrote Phase 3 result and refreshed Phase 4 subplan.

Key outcome:

- All rungs passed with GPU outputs, XLA JIT, `transport_ad_mode="full"`,
  finite objective, finite gradients, finite seed-gradient MCSE, and connected
  gradients.
- `T=3` MCSE decreased from `N=64` to `N=256` to `N=1000` for all three
  parameters.
- The `N=1000` peak TensorFlow allocator memory was `6726029824` bytes.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-particle-ladder-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n16-t1-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n64-t3-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n256-t3-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n1000-t3-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-subplan-2026-07-01.md`

Gate status:

- `PASSED_PENDING_CLAUDE_RESULT_REVIEW`

Next action:

- Send Phase 3 result and refreshed Phase 4 subplan to Claude read-only review.

### 2026-07-01 - Pre-Phase 4 - SKEPTICAL_AUDIT_AND_CLAUDE_REVIEW

Skeptical audit:

- Wrong baseline checked: Phase 4 compares the corrected full-route total
  derivative to regression FD for the same finite scalar, not to the stopped
  partial derivative.
- Proxy metric checked: Phase 3 MCSE decrease can satisfy only the extra
  condition in the `4 MCSE` rule; it cannot pass Phase 4 without same-scalar FD
  direction results.
- Environment mismatch checked: Phase 4 must use trusted GPU execution with
  XLA and `transport_ad_mode="full"`.
- Artifact relevance checked: Phase 4 writes JSON, memory, and progress
  artifacts that expose FD direction windows and route metadata.
- Stop conditions checked: CPU fallback, missing XLA, route metadata not full,
  nonfinite estimates, unavailable MCSE, or same-scalar mismatch veto the
  phase.

Claude review:

- Bounded read-only review of Phase 3 result and refreshed Phase 4 subplan
  returned `VERDICT: AGREE`.

Gate status:

- `PHASE4_READY_TO_EXECUTE`

Next action:

- Launch Phase 4 same-scalar raw-direction regression FD diagnostic under
  trusted GPU/XLA.

### 2026-07-01 - Phase 4 - FIXABLE_DIRECTION_FILTER_ERROR

Evidence contract:

- Question: Can the Phase 4 same-scalar raw-direction regression FD diagnostic
  run under trusted GPU/XLA?
- Primary criterion: command starts, records full-route metadata, and evaluates
  the three raw parameter directions.
- Veto diagnostics: wrong direction filter preventing FD windows from running.
- Non-claims: no derivative failure unless FD windows actually run and fail.

Observation:

- The first Phase 4 command compiled the manual-reverse XLA unit but exited
  before FD windows because the subplan used direction names
  `raw_log_kappa_scale,raw_log_nu_scale,raw_log_obs_noise_scale`.
- The runner's raw basis names are exactly
  `log_kappa_scale,log_nu_scale,log_obs_noise_scale`.

Patch:

- Updated the Phase 4 subplan command to use
  `--direction-filter log_kappa_scale,log_nu_scale,log_obs_noise_scale`.

Gate status:

- `FIXED_RETRY_REQUIRED`

Next action:

- Rerun Phase 4 with the corrected direction filter.

### 2026-07-01 - Phase 4 - SERIAL_FD_RUNTIME_BLOCKER

Evidence contract:

- Question: Can the corrected Phase 4 same-scalar raw-direction regression FD
  command finish in a bounded time?
- Primary criterion: FD windows complete and write direction results.
- Veto diagnostics: first FD window remains incomplete after a long run.
- Non-claims: no derivative failure and no FD disagreement unless the FD
  windows finish.

Observation:

- The corrected direction-filter run compiled the manual-reverse XLA unit and
  entered the first FD window, `log_kappa_scale` at base step `0.00025`.
- The progress artifact remained at that first FD window while memory samples
  continued through roughly 25 minutes of total elapsed time.
- The process traceback after interruption showed the serial FD value path was
  replaying the full streaming transport one theta offset at a time.

Conclusion:

- The serial FD command shape is not a practical Phase 4 gate at `N=1000`.
  This is a diagnostic harness/runtime issue, not evidence that the total
  derivative is wrong.

Patch:

- Updated Phase 4 to use `--fd-evaluation-mode batched-theta` and
  `--theta-offset-batch-size 3`, preserving the same scalar and full route while
  reducing serial value replays.

Gate status:

- `FIXED_REVIEW_REQUIRED`

Next action:

- Review the batched-theta Phase 4 command shape, then rerun if accepted.

### 2026-07-01 - Phase 4 - BATCHED_THETA_REPAIR_REVIEW_PASS

Claude review:

- Bounded read-only review of the Phase 4 batched-theta FD repair returned
  `VERDICT: AGREE`.

Review outcome:

- Batched-theta mode preserves the same theta rows and same scalar while
  changing the objective-evaluation shape.
- The serial attempt is correctly recorded as a harness/runtime blocker.

Gate status:

- `PHASE4_REPAIR_READY_TO_EXECUTE`

Next action:

- Rerun Phase 4 with `--fd-evaluation-mode batched-theta` and
  `--theta-offset-batch-size 3`.

### 2026-07-01 - Phase 4 - HMC_DIRECTION_DIAGNOSTIC_PASS

Evidence contract:

- Question: Is the corrected full-route gradient direction good enough for the
  intended HMC direction use?
- Primary criterion: every raw direction passes if within `2 MCSE`, or within
  `4 MCSE` with MCSE decreasing as `N` increases, or relative error below
  `1%`.
- Veto diagnostics: same-scalar mismatch, nonfinite estimates, MCSE
  unavailable, route metadata not full, CPU fallback.
- Non-claims: no posterior correctness, no exact nonlinear likelihood
  correctness, no production HMC readiness.

Actions:

- Ran reviewed batched-theta same-scalar FD diagnostic under trusted GPU/XLA.
- Parsed the three raw directions against the predeclared rule.
- Wrote Phase 4 result.
- Refreshed Phase 5 final-decision subplan.

Outcome:

- `log_kappa_scale`: passed by `4_MCSE_AND_DECREASING_MCSE` and
  `REL_LT_1_PERCENT`.
- `log_nu_scale`: passed by `4_MCSE_AND_DECREASING_MCSE`.
- `log_obs_noise_scale`: passed by `4_MCSE_AND_DECREASING_MCSE`.
- Runtime caveat: completed batched-theta Phase 4 took `3030.1685376500245`
  seconds.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-memory-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase4-hmc-direction-n1000-raw-progress-2026-07-01.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase5-final-decision-subplan-2026-07-01.md`

Gate status:

- `PASSED_PENDING_CLAUDE_RESULT_REVIEW`

Next action:

- Send Phase 4 result and Phase 5 final-decision subplan to Claude read-only
  review.

### 2026-07-01 - Phase 5 - FINAL_DECISION_COMPLETE

Evidence contract:

- Question: What does the evidence justify doing next with the corrected route?
- Primary criterion: final label is directly supported and nonclaims are
  explicit.
- Veto diagnostics: unsupported promotion, hidden failed gate, missing artifact,
  evasive language.
- Non-claims: no posterior correctness, no exact nonlinear likelihood
  correctness, no full HMC production readiness.

Actions:

- Claude read-only review of Phase 4 result and proposed final label returned
  `VERDICT: AGREE`.
- Wrote Phase 5 final decision result.
- Updated the visible stop handoff.

Final label:

- `GPU_XLA_VIABLE_TOTAL_DERIVATIVE_EXPERIMENTAL_ROUTE_WITH_RAW_DIRECTION_GATE_PASS`

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase5-final-decision-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-visible-stop-handoff-2026-07-01.md`

Gate status:

- `COMPLETE`
