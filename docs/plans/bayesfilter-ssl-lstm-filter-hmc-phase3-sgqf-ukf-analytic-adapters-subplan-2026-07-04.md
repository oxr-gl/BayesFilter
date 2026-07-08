# Phase 3 Subplan: Fixed SGQF And UKF Analytic Adapters

Date: 2026-07-04

Status: `DRAFT_FUTURE_PHASE`

## Phase Objective

Build or wire fixed SGQF and UKF analytic-gradient adapters for the Gaussian
additive SSL-LSTM target under the shared value/score protocol. SGQF and UKF
enter the same benchmark as all other candidate filters.

## Entry Conditions Inherited From Previous Phase

- Phase 2 closed the shared value/score protocol and artifact schema.
- Phase 1 closed the SSL-LSTM target, priors, transforms, shapes, and fixture
  definitions.
- Analytic first-order score paths exist or can be adapted from local fixed
  SGQF and UKF derivative modules.

## Required Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase3-sgqf-ukf-analytic-adapters-result-2026-07-04.md`
- Code and tests for SSL-LSTM SGQF adapter.
- Code and tests for SSL-LSTM UKF adapter.
- Value/score JSON artifacts for tiny deterministic fixtures.
- Finite-difference diagnostic artifacts for selected parameters.
- Refreshed Phase 4 subplan.

## Required Checks, Tests, And Reviews

- Focused tests for shape, finite values, deterministic repeated evaluation,
  analytic score presence, and finite-difference residuals.
- XLA/JIT smoke for production-like adapter paths when feasible.
- Cross-check on affine-Gaussian fixtures where Kalman reference is available;
  this is an implementation sanity check only.
- Claude read-only review for material adapter diffs and result claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can fixed SGQF and UKF provide deterministic analytic value/score adapters for SSL-LSTM? |
| Baseline/comparator | Shared Phase 2 protocol; affine-Gaussian Kalman sanity fixture only for implementation checks. |
| Primary pass criterion | SGQF and UKF adapters pass contract tests and finite-difference diagnostics on tiny SSL-LSTM fixtures. |
| Veto diagnostics | Non-finite value/score, missing analytic score path, deterministic repeat failure, shape mismatch, or XLA/JIT failure without reviewed exception. |
| Explanatory diagnostics | Score residual distribution, runtime, compile mode, and conditioning summaries. |
| Not concluded | SGQF or UKF sufficiency for SSL-LSTM, HMC success, or ranking against Zhao-Cui/LEDH. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase3-sgqf-ukf-analytic-adapters-result-2026-07-04.md` |

## Forbidden Claims And Actions

- Do not conclude SGQF or UKF is sufficient outside the shared benchmark.
- Do not bypass the Phase 6 metric harness.
- Do not use parameter recovery as a pass condition.
- Do not rely on automatic differentiation as the target score route.
- Do not modify Zhao-Cui or LEDH code in this phase except read-only inventory.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only when:

- SGQF/UKF adapter results are recorded as passed, failed, or blocked with
  reason;
- any implementation defects have focused tests or blocker records;
- the shared protocol remains unchanged or Phase 2 has been amended;
- Phase 4 subplan has been refreshed for Zhao-Cui fixed-variant work.

## Stop Conditions

- Both SGQF and UKF analytic adapters require a new unreviewed gradient path.
- The SSL-LSTM model spec from Phase 1 is incomplete for sigma-point filtering.
- Contract tests reveal a shared protocol flaw that must return to Phase 2.
- Human approval is required for an API/default-policy change.

## End-Of-Phase Protocol

1. Run focused adapter tests and diagnostic commands.
2. Write the Phase 3 result/close record.
3. Draft or refresh the Phase 4 subplan.
4. Review Phase 4 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
