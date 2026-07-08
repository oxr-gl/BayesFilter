# SIR Gradient HMC-Direction Claude Review Ledger

Date: 2026-06-30

Status: `INITIALIZED`

Claude is a read-only reviewer only.  Claude review does not authorize boundary
crossings, scientific claims, runtime policy changes, model-file changes,
funding decisions, or detached execution.

## Reviews

### 2026-06-30 - Master/Runbook/Phase 0/Phase 1 Review Round 1

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Scope:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-master-program-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-gated-overnight-execution-runbook-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase0-route-inventory-subplan-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-subplan-2026-06-30.md`

Verdict: `VERDICT: REVISE`

Findings:

- Phase 1 candidate gate let `<1%` relative error against SIR regression FD act
  as a standalone pass condition.
- Phase 1 required seed-gradient MCSE only to be finite, so MCSE did not
  materially enter the HMC-direction classification or veto logic.
- No major issue was found with detached-execution prohibition, CPU/GPU
  boundary, unsupported exactness claims, or required Phase 0/1 sections.

Codex response:

- Revised the Phase 1 candidate gate to use
  `combined_se = sqrt(regression_slope_standard_error^2 + standard_error_of_batch_mean^2)`.
- Changed the `<1%` relative-error screen to `near_equal_supportive`, not a
  standalone `direction_pass`.
- Added an explicit forbidden action that finite MCSE alone is insufficient;
  MCSE must enter the comparison uncertainty or veto classification.

### 2026-06-30 - Phase 1 Gate Revision Review Round 2

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Scope:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-subplan-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-claude-review-ledger-2026-06-30.md`

Verdict: `VERDICT: REVISE`

Findings:

- Round-1 proxy-promotion and MCSE concerns were substantially addressed.
- Remaining issue: `abs(delta) <= 2 * combined_se` could pass merely because
  `combined_se` is very large, treating unresolved disagreement as positive
  HMC-direction evidence.
- Clause 2 must also avoid letting improving MCSE/residual trends rescue an
  imprecise comparison.

Codex response:

- Added predeclared `direction_scale` and `precision_pass`:
  `2 * combined_se <= 0.25 * max(abs(regression_fd_slope), abs(manual_score), 1.0)`.
- Added `inconclusive_precision_veto` for large uncertainty bands.
- Required `precision_pass` for both the `2 * combined_se` and ladder-assisted
  `4 * combined_se` pass arms.
- Added same-sign reporting for non-negligible directions and an explicit
  `near_zero_direction` label when both estimates are within `2 * combined_se`
  of zero.

### 2026-06-30 - Phase 1 Gate Revision Review Round 3

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Scope:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-subplan-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-claude-review-ledger-2026-06-30.md`

Verdict: `VERDICT: AGREE`

Findings:

- No remaining material blocker for launching Phase 0.
- `precision_pass` and `inconclusive_precision_veto` address the Round-2
  uncertainty-band loophole.
- The ladder-assisted `4 * combined_se` arm now also requires
  `precision_pass`.
- Minor nonblocking wording cleanup suggested: separate supportive labels from
  pass arms in Phase 1 before executing that phase.

### 2026-06-30 - Phase 2 Implementation Review Round 1

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Scope:

- `docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py`
- `tests/test_p8p_sir_hmc_direction_gate.py`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase1-gate-contract-result-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase2-diagnostic-reporting-subplan-2026-06-30.md`

Verdict: `VERDICT: REVISE`

Findings:

- Material blocker: the numeric direction classifier did not include route
  prerequisites, so CPU/non-XLA/wrong-route runs could still emit
  `direction_pass=True`.
- Tests covered numeric gate arms but not route-prerequisite suppression.

Codex response:

- Added `_route_prerequisite_gate`.
- Added `route_prerequisite_pass`, `route_prerequisite_failed_checks`,
  `numeric_direction_pass`, and `numeric_direction_gate_reason`.
- Made `direction_pass = route_prerequisite_pass and numeric_direction_pass`.
- Added a route-prerequisite veto test.

### 2026-06-30 - Phase 2 Implementation Review Round 2

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Scope:

- `docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py`
- `tests/test_p8p_sir_hmc_direction_gate.py`

Verdict: `VERDICT: AGREE`

Findings:

- Round-1 blocker resolved.
- `direction_pass` is route-gated.
- Numeric pass remains preserved separately for debugging.
- Aggregate `all_raw_directions_hmc_direction_pass` now depends on
  route-gated `direction_pass`.
- The added route-veto regression test covers the blocker.

### 2026-06-30 - Phase 4 Material Diagnostic Subplan Review Round 1

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Scope:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-subplan-2026-06-30.md`
- `scripts/run_sir_gradient_phase4_material_diagnostic.sh`

Verdict: `VERDICT: AGREE`

Findings:

- Wrapper CLI syntax is sound and uses the protected negative-offset form
  `--regression-offsets=-6,...,6`.
- Wrapper and subplan match on GPU/XLA/TF32 route, `N=64`, `T=3`, five seeds,
  progress JSON, JSON output, and Markdown output.
- The phase-result note is correctly a post-run artifact rather than wrapper
  output.
- Forbidden-claim boundaries and stop conditions are present.

Disposition:

- Phase 4 subplan converged for execution.

### 2026-06-30 - Human Claude Read-Only Artifact Approval Clarification

Human approval:

- The user approved sending all artifacts in this repository to Claude Code for
  read-only review.

Scope:

- This approval applies to bounded Claude read-only review prompts and exact
  repository paths used for review.
- Claude remains a reviewer only and does not authorize runtime execution,
  product/scientific claims, model-file changes, funding decisions, or boundary
  crossings.

Operational consequence:

- Future Claude review prompts for this program may include exact repository
  paths and full artifacts when useful, while still keeping the prompt scoped
  to the review question.

### 2026-06-30 - Phase 4 Exit-137 Repair Review

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Scope:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-subplan-2026-06-30.md`
- `scripts/run_sir_gradient_phase4_material_diagnostic.sh`

Context:

- Original Phase 4 GPU/XLA/TF32 run started correctly, completed budget 10,
  then was killed with exit code 137 during budget 100.
- Repair adds `--seed-microbatch-size 1` and `--theta-offset-batch-size 2`.

Verdict: `VERDICT: AGREE`

Findings:

- Wrapper and subplan both include exactly the two chunking flags.
- Route-defining controls remain GPU, float32, TF32 enabled, XLA manual reverse,
  same seeds, same budgets, same theta, same FD offsets, and same transport
  gradient mode.
- Required JSON, Markdown, progress JSON, and post-run Phase 4 result note are
  covered.
- The stated boundary, execution-shape repair only with no widened scientific
  claim, is respected in the reviewed files.

Caveat:

- The narrow review did not prove semantic equivalence of chunking inside the
  Python diagnostic implementation.  Codex separately traced the local code and
  found that seed microbatching recombines the same fixed seeds by seed-weighted
  means, while theta-offset batching evaluates the same FD theta rows in chunks
  before the same regression/gate logic.

Disposition:

- Phase 4 repaired wrapper is approved for rerun as an execution-shape repair.

### 2026-06-30 - Phase 5 Process-Isolation Review Round 1

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Scope:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-result-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-subplan-2026-06-30.md`
- `scripts/run_sir_gradient_phase5_budget10.sh`
- `scripts/run_sir_gradient_phase5_budget100.sh`

Verdict: `VERDICT: FIX`

Finding:

- Phase 5 wrappers preserved the process-boundary repair but omitted the
  Phase 4 reviewed chunking knobs `--seed-microbatch-size 1` and
  `--theta-offset-batch-size 2`.  Without those flags, Phase 5 would change
  more than the process boundary.

Codex response:

- Added `--seed-microbatch-size 1` and `--theta-offset-batch-size 2` to both
  Phase 5 wrappers.
- Updated the Phase 5 subplan baseline and forbidden-change sections to freeze
  these exact chunking knobs.
- Reran focused shell syntax and compile checks.

### 2026-06-30 - Phase 5 Process-Isolation Review Round 2

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Scope:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-subplan-2026-06-30.md`
- `scripts/run_sir_gradient_phase5_budget10.sh`
- `scripts/run_sir_gradient_phase5_budget100.sh`

Verdict: `VERDICT: AGREE`

Findings:

- The prior blocker is fixed in both wrappers.
- The Phase 5 subplan records the exact chunking knobs consistently.
- Claude did not identify a new material issue in the reviewed scope.

Disposition:

- Phase 5 budget-10 isolated process may run.

### 2026-07-01 - Phase 6 Final Closeout Review Round 1

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Scope:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-repair-ladders-result-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase6-closeout-result-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-stop-handoff-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.md`

Verdict: `VERDICT: FIX`

Finding:

- The visible handoff compressed the next FD-objective split to one process per
  FD direction and theta-offset chunk, omitting explicit budget and seed-group
  partitioning.  That did not exactly match the Phase 5/6 closeout artifacts.

Codex response:

- Updated the handoff to require one process per budget, FD direction,
  theta-offset chunk, and seed group.
- Added that aggregation must exactly reproduce the current
  estimator/comparator before any material rerun.

### 2026-07-01 - Phase 6 Final Closeout Review Round 2

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Scope:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-stop-handoff-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase6-closeout-result-2026-06-30.md`

Verdict: `VERDICT: FIX`

Finding:

- The FD-objective split was fixed, but manual-score splitting still differed:
  the closeout specified one process per budget and seed group, while the
  handoff specified only one process per seed group.

Codex response:

- Updated the handoff to require one process per budget and seed group for
  manual score.

### 2026-07-01 - Phase 6 Final Closeout Review Round 3

Reviewer: Claude Opus via `scripts/claude_worker.sh`

Scope:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-stop-handoff-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase6-closeout-result-2026-06-30.md`

Verdict: `VERDICT: AGREE`

Findings:

- Handoff and closeout are aligned:
  - manual score split by budget and seed group;
  - FD objective split by budget, raw/FD direction, theta-offset chunk, and
    seed group.
- No material unsupported promotion claim was found.
- Both documents preserve the budget-100 exit-137 blocker and deny SIR gradient
  correctness, HMC readiness, and posterior correctness claims.

Disposition:

- Final closeout review converged.
