# P01 Harness Integration Subplan

Status: `DRAFT_FOR_REVIEW`

## Phase Objective

Create an owned actual-SIR route-validation harness that reuses the existing
actual-SIR callbacks, observations, seeds, dtype/TF32/device checks, and
semantics metadata while adding route selection for `streaming` versus
`low_rank`.

## Entry Conditions Inherited From Previous Phase

- P00 governance result passed.
- Master program and visible runbook exist.
- Claude plan review converged or a documented nonmaterial waiver exists.
- No shared contract/API/export change is required.

## Required Artifacts

- New harness:
  `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
- Focused tests:
  `tests/test_actual_sir_low_rank_route_validation.py`
- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p01-harness-result-2026-06-21.md`
- Refreshed P02 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p02-smoke-subplan-2026-06-21.md`

## Required Checks, Tests, Reviews

- `python -m py_compile docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
- `pytest tests/test_actual_sir_low_rank_route_validation.py -q`
- `pytest tests/test_low_rank_coupling_solver_tf.py tests/test_low_rank_ledh_pfpf_integration_smoke.py -q`
- Claude read-only review if implementation diff or result introduces material boundary risk.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the harness correctly route actual-SIR LEDH/PFPF-OT through streaming or low-rank while preserving route-fired evidence and diagnostics? |
| Baseline/comparator | Existing actual-SIR streaming route semantics from `benchmark_p8j_tf32_batched_actual_sir.py`. |
| Primary pass criterion | Harness compiles, focused tests pass, both route choices are encoded, actual-SIR semantics are preserved, and low-rank diagnostics are recorded. |
| Veto diagnostics | Missing route-fired evidence, missing actual-SIR metadata, public export/shared contract change, dense materialization for low-rank, or invalid low-rank diagnostic contract. |
| Explanatory diagnostics | Test-level small route outputs and path checks. |
| Not concluded | No actual-SIR speed claim, no large-N feasibility, no posterior correctness. |
| Artifact | P01 result and harness/test files. |

## Forbidden Claims/Actions

- Do not change existing actual-SIR benchmark behavior.
- Do not edit BayesFilter public exports.
- Do not claim low-rank improves actual-SIR before smoke/ladder phases.
- Do not use POT, package installs, network, or external solvers.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if the harness and focused tests pass, P01 result
records no hard vetoes, and P02 smoke commands are concrete with bounded
timeouts and artifact paths.

## Stop Conditions

- `BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED` if route integration needs shared
  contract or public export changes.
- `LOW_RANK_ACTUAL_SIR_HARNESS_BLOCKED` if the existing low-rank solver cannot
  produce finite nonnegative factors or transported particles on tiny
  actual-SIR rows without forbidden work.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the P01 phase result.
3. Draft or refresh P02.
4. Review P02 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
