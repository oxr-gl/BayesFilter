# P8p Visible Execution Ledger

Date: 2026-06-18

Status: `INITIALIZED`

## Ledger

### 2026-06-18 - Phase 0 - PRECHECK

Evidence contract:

- Question: Is P8p scoped correctly as a new parameterized SIR d18 diagnostic-gradient lane, with P8o used only as value-only entry evidence?
- Baseline/comparator: P8o value-only SIR d18 result and current actual-SIR streaming harness.
- Primary criterion: Local checks locate required artifacts/hooks, boundaries are recorded, Claude review converges, and Phase 1 has a concrete target-design subplan.
- Veto diagnostics: Missing P8o artifact; missing streaming value/score hook; P8o treated as gradient/HMC evidence; bootstrap/scalar parity drift; Zhao-Cui fixed-branch/monograph drift; variable randomness or categorical resampling in theta target.
- Non-claims: No gradient correctness, finite-difference correctness, HMC readiness, posterior convergence, exact likelihood correctness, or production/default readiness.

Actions:

- Created P8p master program, Phase 0 subplan, Phase 1 draft subplan, visible runbook, review ledger, execution ledger, and stop handoff.
- Ran first Claude read-only review.  Claude returned `VERDICT: REVISE` with
  material issues: existing score helper zero-fills unconnected gradients,
  Phase 1 needed exact theta-dependent edit points, and runbook needed master
  stop-condition carry-through.
- Patched master program, Phase 0 subplan, Phase 1 subplan, and runbook to
  require explicit per-theta connectivity diagnostics and exact edit points.

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-sir-d18-gradient-hmc-master-program-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase0-governance-target-boundary-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-visible-gated-execution-runbook-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-claude-review-ledger-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-visible-stop-handoff-2026-06-18.md`

Gate status:

- `PASSED_PHASE0`

Next action:

- Execute Phase 1 precheck using
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-subplan-2026-06-18.md`.

### 2026-06-18 - Phase 0 - ASSESS_GATE

Evidence contract:

- Question: Is P8p scoped correctly as a new parameterized SIR d18 diagnostic-gradient lane, with P8o used only as value-only entry evidence?
- Baseline/comparator: P8o value-only SIR d18 result and current actual-SIR streaming harness.
- Primary criterion: Local checks locate required artifacts/hooks, boundaries are recorded, Claude review converges, and Phase 1 has a concrete target-design subplan.
- Veto diagnostics: Missing hooks/artifacts, wrong lane, masked gradient connectivity, missing stop conditions, unsupported claims.
- Non-claims: No gradient correctness, HMC readiness, exact likelihood correctness, posterior validity, production/default readiness, or Zhao-Cui TT/SIRT parity.

Actions:

- Ran Phase 0 local checks.
- Completed Claude read-only review loop: iteration 1 revised, iteration 2 agreed.
- Wrote Phase 0 result.

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase0-governance-target-boundary-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-claude-review-ledger-2026-06-18.md`

Gate status:

- `PASSED`

Next action:

- Start Phase 1 target contract precheck.

### 2026-06-18 - Phase 1 - PRECHECK

Evidence contract:

- Question: Is the proposed theta target differentiable, fixed-randomness,
  SIR d18-shaped, and narrow enough for diagnostic gradient/HMC-mechanics
  testing?
- Baseline/comparator: Current fixed-parameter actual-SIR harness with P8o
  settings at theta zero.
- Primary criterion: Phase 1 specifies theta transforms, fixed observations,
  fixed random streams, relaxed OT, exact implementation surface, Phase 2
  smoke sizes, and forbidden claims.
- Veto diagnostics: Random streams depending on theta, categorical resampling,
  hidden NumPy differentiable implementation, missing fixed-seed contract,
  relying only on the zero-filled score helper, missing exact edit points, or
  scientific posterior claims.
- Non-claims: No gradient correctness, HMC readiness, exact likelihood
  correctness, posterior validity, or production/default readiness.

Actions:

- Read the actual-SIR harness, streaming score helper, and SIR model anchors.
- Wrote Phase 1 result and Phase 2 subplan.

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-subplan-2026-06-18.md`

Gate status:

- `IN_PROGRESS_PENDING_LOCAL_CHECKS_AND_REVIEW`

Next action:

- Run Phase 1 local checks and request Claude review of Phase 1 result plus
  Phase 2 subplan.

### 2026-06-18 - Phase 1 - REVIEW_REPAIR

Actions:

- Claude Phase 1/2 review attempt with the larger prompt was silent and was
  interrupted.
- Small Claude probe returned `PROBE_OK`, confirming the review prompt was the
  issue rather than Claude availability.
- Smaller Claude review returned `VERDICT: REVISE`.
- Patched Phase 1 handoff and Phase 2 subplan to require theta-zero P8j parity,
  repeated same-theta repeatability, fixed random-stream proof, fixed
  resampling-mask proof, relaxed Sinkhorn OT proof, and no categorical
  resampling artifact fields.

Gate status:

- `IN_PROGRESS_PENDING_FOCUSED_CHECKS_AND_REREVIEW`

Next action:

- Rerun focused checks and send bounded Claude rereview.

### 2026-06-18 - Phase 1 - ASSESS_GATE

Actions:

- Reran focused checks after Phase 2 subplan repair.
- Claude iteration 2 returned `VERDICT: AGREE`.
- Updated Phase 1 result status and Phase 2 subplan status.

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase1-parameterized-sir-objective-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-subplan-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-claude-review-ledger-2026-06-18.md`

Gate status:

- `PASSED`

Next action:

- Begin Phase 2 skeptical audit, then implement the diagnostic harness if the
  audit passes.

### 2026-06-18 - Phase 2 - EXECUTE_AND_ASSESS

Evidence contract:

- Question: Does the tiny P8p parameterized SIR d18 fixed-randomness graph
  produce finite values and explicit connected gradients for all three theta
  components?
- Baseline/comparator: Phase 1 theta-zero contract and current P8j
  fixed-parameter route at the same tiny shape.
- Primary criterion: theta-zero P8j parity, finite value/gradient, connected
  nonzero components, repeatability, finite FD sensitivity, fixed random
  streams, fixed mask, relaxed Sinkhorn OT, no categorical resampling, and
  trusted GPU placement.
- Veto diagnostics: missing/failed parity, nonfinite/disconnected gradient,
  masked-zero success, variable randomness, categorical resampling, CPU
  fallback, or broad unrelated mutation.
- Non-claims: no full-horizon gradient correctness, stochastic PF marginal
  score correctness, exact likelihood correctness, HMC readiness, posterior
  convergence, production/default readiness, or filter ranking.

Actions:

- Implemented `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`.
- Ran compile and diff checks.
- Ran CPU-only implementation smoke.
- Ran trusted GPU Phase 2 smoke.
- Validated JSON gate fields programmatically.
- Wrote Phase 2 result and Phase 3 subplan.

Artifacts:

- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase2-gradient-smoke-result-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-subplan-2026-06-18.md`

Gate status:

- `PASSED`

Next action:

- Execute Phase 3 finite-difference validation after precheck.

### 2026-06-18 - Phase 3 - BLOCKED

Evidence contract:

- Question: Do AD gradients and central finite differences agree in sign and
  reasonable scale while preserving Phase 2 route guarantees?
- Baseline/comparator: Phase 2 passed tiny smoke and same-target central finite
  differences.
- Primary criterion: finite route guarantees plus sign agreement and residual
  within `max(10.0, 0.20 * max(1, abs(fd)))`.
- Veto diagnostics: nonfinite, disconnected, repeated-evaluation drift,
  categorical resampling, missing GPU placement, sign disagreement, or residual
  beyond tolerance.
- Non-claims: no exact score correctness, stochastic PF marginal score
  correctness, full-horizon stability, HMC readiness, posterior convergence,
  production/default readiness, or filter ranking.

Actions:

- Ran Phase 3 prechecks.
- Ran trusted GPU Phase 3 finite-difference validation.
- Evaluated AD/FD residuals against the predeclared tolerance.
- Patched harness metadata to accept `--phase-label` for future artifacts.
- Wrote Phase 3 blocker result.

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-result-2026-06-18.md`

Gate status:

- `BLOCKED`

Next action:

- Stop visible execution before Phase 4.  Draft/review a focused Phase 3 repair
  subplan if the user wants to continue.
