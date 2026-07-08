# BayesFilter Quadratic Initializer To Minimal HMC Readiness Visible Ledger

Date: 2026-07-08

## Status

`IN_PROGRESS`

## Ledger

### 2026-07-08T21:50:26+08:00 - Phase 0 - PRECHECK

Evidence contract:

- Question: Which coordinate space does each precision/covariance live in, and
  what must be passed to HMC geometry initialization?
- Baseline/comparator: Existing minimal Phase 5 low-rank path and
  `initialize_hmc_kernel_geometry` contract.
- Primary criterion: Result note states exact mapping from quadratic whitened
  `z` to original theta, HMC mass artifact covariance space, and trajectory
  diagnostic interpretation.
- Veto diagnostics: Ambiguous coordinate state, untransformed whitened precision
  treated as original precision, no line-anchored source evidence, or HMC
  runtime launched.
- Non-claims: No initializer quality, HMC readiness, posterior correctness, or
  convergence.

Actions:

- Committed completed initializer work as `9220d90`.
- Confirmed worktree was clean before starting this runbook.
- Inspected minimal Phase 5 geometry path, HMC geometry initialization, and
  mass artifact code.

Artifacts:

- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-master-program-2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-visible-runbook-2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase0-coordinate-audit-subplan-2026-07-08.md`

Gate status:

- `COMPLETED_WITH_REPAIR`

Next action:

- Phase 1 initializer artifact smoke.

### 2026-07-08T22:31:20+08:00 - Phases 1-2 - EXECUTION RESULT

Evidence contract:

- Phase 1 question: Does the repaired reusable initializer produce a finite SPD
  theta-coordinate mass artifact on the minimal scalar SSL-LSTM target?
- Phase 2 question: Can the Phase 1 theta-coordinate mass artifact be consumed
  by `initialize_hmc_kernel_geometry` without coordinate or SPD failures?
- Non-claims: no HMC runtime readiness, posterior correctness, convergence,
  sampler superiority, default readiness, or Zhao-Cui source-faithfulness.

Actions:

- Patched `estimate_quadratic_map_covariance` so accepted public
  `precision`/`covariance` are transformed from whitened `z` coordinates back
  to original theta coordinates when `scale` is supplied.
- Added focused regression coverage for nontrivial `scale`.
- Created and ran Phase 1 initializer artifact smoke.
- Created and ran Phase 2 HMC geometry-initialization-only smoke.
- Drafted Phase 3 bounded mechanics subplan, not executed.

Artifacts:

- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase0-coordinate-audit-result-2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase1-initializer-artifact-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase1-initializer-artifact-result-2026-07-08.md`
- `docs/benchmarks/benchmark_minimal_ssl_lstm_quadratic_initializer_artifact_2026_07_08.py`
- `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_artifact_cpu_hidden_2026-07-08.json`
- `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_artifact_cpu_hidden_2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase2-geometry-initialization-subplan-2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase2-geometry-initialization-result-2026-07-08.md`
- `docs/benchmarks/benchmark_minimal_ssl_lstm_quadratic_initializer_geometry_2026_07_08.py`
- `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_geometry_cpu_hidden_2026-07-08.json`
- `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_geometry_cpu_hidden_2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase3-bounded-mechanics-subplan-2026-07-08.md`

Key diagnostics:

- Phase 1 accepted/status: `true` / `usable`.
- Phase 1 precision condition number: `55.004100411471235`.
- Phase 1 mass coordinates: precision `theta`, covariance `theta`.
- Phase 2 selected hint: `negative_hessian`.
- Phase 2 fallback used: `false`.
- Phase 2 initial step size: `0.22590050090246147`.
- Phase 2 initial leapfrog steps: `7`.
- Phase 2 target trajectory: `1.570796326794897`.
- Phase 2 `L * step_size`: `1.5813035063172303`.
- Phase 2 HMC runtime invoked: `false`.

Gate status:

- Phase 1: `PASSED_WITH_LOCAL_NEIGHBORHOOD_REPAIR`
- Phase 2: `PASSED_GEOMETRY_ONLY`
- Phase 3: `DRAFT_ONLY_NOT_EXECUTED`

Next action:

- Execute Phase 3 only after preserving the fixed-geometry mechanics evidence
  contract and implementing a tiny bounded mechanics harness.

### 2026-07-08T22:41:38+08:00 - Phase 3 - EXECUTION RESULT

Evidence contract:

- Question: Can the Phase 2 fixed geometry execute the smallest bounded HMC
  mechanics smoke without immediate finite-value or artifact failures?
- Primary criterion: tiny fixed-kernel HMC runtime artifact exists with finite
  samples/log-accept/target-log-prob diagnostics and no hard-veto diagnostics.
- Non-claims: no HMC readiness, convergence, posterior correctness, sampler
  superiority, default readiness, or Zhao-Cui source-faithfulness.

Actions:

- Created Phase 3 fixed-kernel mechanics smoke script.
- First run identified a script diagnostics-wiring bug: trace summary had zero
  nonfinite log-accept and target-log-prob values, but the veto check looked
  for nonexistent top-level keys.
- Patched veto checks to use the trace summary and reran the same fixed
  geometry smoke.
- Wrote Phase 3 result and closeout.

Artifacts:

- `docs/benchmarks/benchmark_minimal_ssl_lstm_quadratic_initializer_mechanics_2026_07_08.py`
- `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_mechanics_cpu_hidden_2026-07-08.json`
- `docs/benchmarks/minimal_ssl_lstm_quadratic_initializer_mechanics_cpu_hidden_2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-phase3-bounded-mechanics-result-2026-07-08.md`
- `docs/plans/bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-closeout-2026-07-08.md`

Key diagnostics:

- Phase 3 decision: `mechanics_smoke_passed=true`.
- Retained samples: `4`.
- Burn-in steps: `1`.
- Fixed/adaptive policy: `fixed_kernel_no_adaptation`.
- Acceptance rate: `1.0`.
- Nonfinite sample count: `0`.
- Log accept nonfinite count: `0`.
- Target log prob nonfinite count: `0`.
- Native divergence trace present: `false`; this is not zero divergences.
- HMC tuning invoked: `false`.

Gate status:

- Phase 3: `PASSED_MECHANICS_SMOKE_ONLY`
- Closeout: `COMPLETED_THROUGH_PHASE_3_MECHANICS_SMOKE`

Next action:

- A separate short-chain validation plan is justified only if it predeclares a
  native-divergence policy and keeps readiness/posterior claims gated behind
  stronger diagnostics.
