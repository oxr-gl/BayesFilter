# SIR Gradient Reparameterization Root-Cause Claude Review Ledger

Date: 2026-07-01

Status: `OPEN`

Claude is a read-only reviewer only.  Claude reviews do not authorize boundary
changes, production default changes, scientific claims, package installation,
network fetches, detached execution, or destructive operations.

## Review Rounds

### 2026-07-01T04:54:39+08:00 - Launch Plan Review Iteration 1

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Prompt scope:

- Master program.
- Visible gated execution runbook.
- Phase 0 through Phase 5 subplans.

Outcome:

- `VERDICT: REVISE`

Material findings:

1. Subplans did not specify exact commands/environment for planned checks or
   material runs.
2. Claude-review execution path was boundary-ambiguous between visible runbook
   and worker-script review.
3. Phase 4 overclaimed that kappa/nu covariance-independence alone can rule out
   non-centering relevance.
4. Phase 1 baseline used stale/ambiguous "Phase 5" wording instead of the exact
   prior budget-10 artifact path.
5. Phase 2/4 criteria were too artifact-production oriented and needed explicit
   evidence patterns for advance/block/inconclusive.

Patch response:

- Patched exact-command templates, Claude worker boundary, Phase 4
  covariance-independence overclaim, Phase 1 baseline path, and Phase 2/4
  classification criteria.

### 2026-07-01T05:00:20+08:00 - Launch Plan Review Iteration 2

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Prompt scope:

- Re-review of Iteration 1 material findings only.

Outcome:

- `VERDICT: REVISE`

Remaining material finding:

1. Phases 1-4 still used placeholder command paths such as
   `<new_or_touched_phase1_diagnostic.py>` and material commands "to be
   finalized"; exact commands/environment were therefore not fully frozen.

Findings resolved by Iteration 1 patch:

- Claude worker boundary is now substantially clearer.
- Phase 4 no longer rules out non-centering from covariance-independence alone.
- Phase 1 names exact prior baseline artifacts.
- Phase 2 and Phase 4 classify outcomes rather than merely requiring reports.

Patch response:

- Patched Phases 1-4 to pin planned diagnostic, test, wrapper, and exact
  command paths instead of placeholders.

### 2026-07-01T05:04:58+08:00 - Launch Plan Review Iteration 3

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Prompt scope:

- Re-review only the remaining Iteration 2 blocker about placeholder commands
  in Phases 1-4.

Outcome:

- `VERDICT: AGREE`

Findings:

- Phase 1 satisfies the blocker.
- Phase 2 satisfies the blocker.
- Phase 3 satisfies the blocker for its narrower scope.
- Phase 4 is concretized enough for this blocker; Claude noted one consistency
  nit that Phase 4 wrapper execution is conditional while `bash -n` is listed
  in local checks.  This is not a launch blocker because Phase 4 is pending
  and the Phase 4 subplan must be refreshed before execution.

### 2026-07-01T05:37:36+08:00 - Phase 1 Result / Phase 2 Subplan Review Iteration 1

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Prompt scope:

- Phase 1 result close record.
- Refreshed Phase 2 subplan.
- Phase 1 JSON.
- Phase 1 diagnostic code and wrapper.

Outcome:

- `VERDICT: REVISE`

Material findings:

1. The docs over-labeled the material route as GPU/XLA/TF32 even though the
   Phase 1 wrapper and JSON record GPU/TF32 but not explicit XLA compiler
   status.
2. The focused score-parity command was recorded as a placeholder comment
   rather than the actual reproducible command.
3. Phase 2 mentioned `whitened_2` without anchoring it to a specific prior
   artifact.

Patch response:

- Patched Phase 1/2 route language to GPU/TF32 unless explicit compiler status
  is recorded.
- Patched the Phase 1 result to include the actual parity-check command.
- Patched Phase 2 to anchor any whitened-direction discussion to
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-2026-07-01.json`.

### 2026-07-01T05:47:00+08:00 - Phase 1 Result / Phase 2 Subplan Review Iteration 2

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Prompt scope:

- Focused re-review of Iteration 1 fixes only.

Outcome:

- `VERDICT: AGREE`

Findings:

- No remaining material issue in the focused Iteration 1 fixes.
- XLA overclaim, parity-check provenance, and whitened-direction anchor issues
  were resolved.

### 2026-07-01T06:04:00+08:00 - Phase 2 Result / Phase 3 Subplan Review Iteration 1

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Prompt scope:

- Phase 2 result close record.
- Refreshed Phase 3 subplan.
- Phase 2 JSON.
- Phase 2 diagnostic code, tests, and wrapper.

Outcome:

- `VERDICT: REVISE`

Material findings:

1. Phase 3 introduced a later process-noise/non-centered representation branch
   that was not justified by Phase 2 evidence.
2. Phase 3 primary pass criterion omitted exact tolerances, dtype, and residual
   rule.
3. CPU-only transition checks needed a clearer boundary and cannot clear a
   GPU/TF32 numerical-route issue.
4. Transport-adjoint and stopped-scale-key routes needed to remain live
   alternatives if transition algebra passes.

Patch response:

- Patched Phase 3 to be transition-only.
- Added exact float64 CPU residual criteria: max absolute residual `<= 1.0e-8`
  and relative L2 residual `<= 1.0e-7`.
- Removed pre-authorization of non-centered/process-noise Phase 4.
- Preserved transport-adjoint/stopped-scale-key alternatives.

### 2026-07-01T06:11:04+08:00 - Phase 2 Result / Phase 3 Subplan Review Iteration 2

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Prompt scope:

- Focused re-review of the four Iteration 1 Phase 3 findings only.
- Exact paths reviewed:
  - `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase3-rk4-sensitivity-subplan-2026-07-01.md`
  - `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-visible-execution-ledger-2026-07-01.md`
  - `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-claude-review-ledger-2026-07-01.md`

Outcome:

- `VERDICT: AGREE`

Findings:

- No material findings.
- The Phase 3 subplan resolved the premature non-centered/process-noise
  branch, exact tolerance/dtype/residual rule, CPU-only boundary, and
  transport-adjoint/stopped-scale-key live-alternative findings.

Gate status:

- `PHASE2_CLOSED_PHASE3_CLEARED`

### 2026-07-01T06:22:00+08:00 - Phase 3 Result / Phase 4 Subplan Review Iteration 1

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Prompt scope:

- Phase 3 close record.
- Refreshed Phase 4 transport-adjoint subplan.
- Master program, visible ledger, and stop handoff.

Outcome:

- `VERDICT: REVISE`

Material findings:

1. The Phase 4 comparator boundary was conceptually right, but the subplan did
   not bind it to the exact non-custom-gradient comparator symbol/path.
2. The Phase 4 handoff logic lacked an explicit branch for a clean comparator
   and failed residual test that remains diffuse or not confidently localized.

Patch response:

- Pin the comparator to
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py::_filterflow_manual_streaming_finite_transport_value_stopped_scale_keys`.
- Require the diagnostic to assert it did not call
  `_filterflow_manual_streaming_finite_transport_stopped_scale_keys` or
  `_filterflow_manual_streaming_blockwise_vjp_finite_transport_stopped_scale_keys`
  for the autodiff comparator path.
- Add a `diffuse_transport_mismatch` handoff/stop branch for failed residuals
  that do not localize cleanly.

### 2026-07-01T06:27:00+08:00 - Phase 3 Result / Phase 4 Subplan Review Iteration 2

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Prompt scope:

- Focused re-review of Iteration 1 Phase 4 blockers only.

Outcome:

- `VERDICT: AGREE`

Findings:

- The exact comparator symbol/path blocker is fixed.
- The diffuse clean-comparator failure handoff/stop branch is fixed.
- No new material inconsistency or boundary problem from the fixes.

Gate status:

- `PHASE3_CLOSED_PHASE4_CLEARED`

### 2026-07-01T06:44:00+08:00 - Phase 5 Synthesis Final Review Iteration 1

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Prompt scope:

- Phase 5 synthesis result.
- Visible stop handoff.
- Visible execution ledger.
- Claude review ledger.

Outcome:

- `VERDICT: AGREE`

Findings:

- No material findings.
- Root-cause certainty remains properly qualified.
- No HMC/posterior/production/full-score correctness overclaim.
- Local VJP passes are not treated as full-filter correctness.
- Result/artifact coverage is present.
- Baseline/environment framing is acceptable.
- Recommended next diagnostic, tiny full-route score-assembly parity, is the
  smallest justified next step after Phases 1-4.

Gate status:

- `FINAL_REVIEW_PASSED`
