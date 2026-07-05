# Phase 5 Subplan: Generic Code-Wiring Implementation

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Implement the reviewed generic contracts across the structural, nonlinear, and
highdim layers without silent model-by-model fallback.

## Entry Conditions Inherited From Previous Phase

- Phase 4 has reviewed the derivative contract.
- The target-and-authority contract, structural-admission categories, generic
  value-lane architecture, and derivative taxonomy are frozen.
- Runtime promotion is still not authorized; this phase may implement and run
  only the focused checks named by its reviewed executable refresh.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase5-code-wiring-result-2026-07-01.md`
- refreshed Phase 6 subplan:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-subplan-2026-07-01.md`
- likely implementation files:
  - `bayesfilter/structural_tf.py`
  - `bayesfilter/inference/posterior_adapter.py`
  - `bayesfilter/nonlinear/fixed_sgqf_tf.py`
  - `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
  - `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`
  - `bayesfilter/highdim/filtering.py`
  - `bayesfilter/highdim/score_api.py`
- representative tests:
  - `tests/test_nonlinear_benchmark_models_tf.py`
  - `tests/test_fixed_sgqf_integration_tf.py`
  - `tests/test_fixed_sgqf_values_tf.py`
  - `tests/highdim/test_p51_stable_score_api.py`

## Required Checks/Tests/Reviews

This phase requires a reviewed executable refresh before any code edit or test
command. The executable refresh must narrow:

- exact files to modify,
- exact tests to run,
- whether CPU-only TensorFlow import checks are needed,
- whether `CUDA_VISIBLE_DEVICES=-1` must be set.

Required read-only Claude reviews:

- Phase 5 result,
- refreshed Phase 6 subplan.

## Skeptical Plan Audit

| Risk Checked | Phase 5 Control |
| --- | --- |
| Wrong baseline | Only implement the contracts frozen in Phases 1-4. |
| Proxy metric promoted | Compilation or API-shape success is not value/gradient admission. |
| Missing stop condition | Any code path that cannot preserve exact lane semantics must fail closed or remain blocked. |
| Unfair comparison | Generic code wiring must not silently repurpose model-specific routes as generic support. |
| Hidden assumption | The phase must name exact files and tests before edits begin. |
| Stale context | Code edits are constrained to the reviewed seam map. |
| Environment mismatch | Runtime commands require an executable refresh and CPU/GPU policy clarity. |
| Artifact-answer mismatch | Phase 5 must produce a code-wiring result and a value-validation handoff, not a promotion claim. |

Audit status: executable only after a refreshed reviewed implementation subplan is written.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the reviewed contracts be implemented across the structural, nonlinear, and highdim layers without silent semantic fallback? |
| Baseline/comparator | reviewed contracts from Phases 1-4 and the current implementation seams. |
| Primary criterion | Phase 5 implements the reviewed contracts, passes focused local checks, and writes a result that preserves lane semantics without claiming value or gradient admission. |
| Veto diagnostics | silent model-specific fallback, hidden target drift, unreviewed API-scope widening, or implementation that cannot state which scalar it computes. |
| Explanatory diagnostics | compile/import checks, focused tests, and implementation notes. |
| Not concluded | No value-gate pass, no gradient-gate pass, no HMC readiness, and no top-level/production promotion. |
| Artifact | reviewed implementation result and refreshed Phase 6 subplan. |

## Forbidden Claims/Actions

- Do not claim generic support is validated merely because the code compiles.
- Do not widen API scope beyond the reviewed contract.
- Do not run any test or runtime command not named in the reviewed executable
  refresh.

## Exact Next-Phase Handoff Conditions

Phase 6 may start only if:

- the executable Phase 5 refresh is reviewed `AGREE` before implementation;
- the Phase 5 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 6 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records the exact implementation files and focused checks
  actually used.

## Stop Conditions

- Implementation would require violating the reviewed lane semantics.
- A generic route can be implemented only by silently hiding a model-specific
  fallback.
- Focused local checks fail and cannot be repaired within reviewed scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require wider runtime authority than the reviewed executable
  refresh provides.

## End-Of-Phase Requirements

1. Write an executable refresh before editing code.
2. Implement only the reviewed file set.
3. Run the reviewed focused checks.
4. Write the Phase 5 result.
5. Refresh the Phase 6 subplan.
6. Review the Phase 5 result and refreshed Phase 6 subplan.
7. Update the execution ledger and Claude review ledger.
