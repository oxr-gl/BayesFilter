# P76 Phase 3 Result: Opt-In UKF Initializer Implementation

metadata_date: 2026-06-18
status: PHASE3_PASSED_CLAUDE_AGREE_READY_FOR_PHASE4
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase3-optin-ukf-initializer-implementation-subplan-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase2-implementation-surface-result-2026-06-18.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Scope

Phase 3 implemented the opt-in TensorFlow UKF initializer:

`ukf_whitened_gaussian_sqrt_projection_v1`.

This phase does not run a training pilot, does not change defaults, does not
export the module from `bayesfilter/highdim/__init__.py`, and does not claim
lower-gate repair, validation readiness, HMC readiness, scaling, or
source-faithfulness.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the Phase 1 UKF initializer be implemented as an opt-in TensorFlow surface with focused contract tests? |
| Exact baseline/comparator | Phase 2 named surface and current `ukf_scout.py` / `stochastic_density_training.py`. |
| Primary criterion | Implementation and focused CPU-only tests pass, finite cores are produced, manifests/nonclaims are preserved, and source-route prefit is not used. |
| Veto diagnostics | Nonfinite cores, invalid covariance handling, missing degree guard, source-prefit call path, audit leakage, default export/change, GPU use, or tests fail. |
| Explanatory only | Exact projection coefficients, finite log-density values, manifest summaries, runtime. |
| Not concluded | No lower-gate repair, no validation/HMC readiness, no large mini-batch pilot, no scaling claim. |

## Implementation Summary

New implementation module:

- `bayesfilter/highdim/ukf_initializer.py`

New focused tests:

- `tests/highdim/test_p76_ukf_initializer.py`

The module implements:

- adjacent UKF moment extraction from `UKFScoutResult.mean_path` and
  `UKFScoutResult.covariance_path`;
- block-diagonal adjacent covariance convention;
- covariance symmetrization and eigenvalue flooring;
- UKF-whitened local affine frame \(r=m_A^U+L_Uz\);
- normalized one-dimensional Gaussian square-root projection under the active
  `ProductBasis` mass convention;
- TT core construction and deterministic seeded rank-channel embedding;
- JSON-friendly manifest fields recording `source_route_prefit_used: false`,
  `audit_data_used: false`, `default_behavior_changed: false`, and
  `scout_not_truth` nonclaims.

The implementation remains opt-in.  It is not imported from
`bayesfilter/highdim/__init__.py`.

## Focused Test Coverage

The new P76 tests cover:

1. adjacent moment extraction and the `time_index == 1` previous block using
   `mean_path[0]` and `covariance_path[0]`;
2. covariance stabilization flooring a tiny negative eigenvalue;
3. degree-one guard for curvature-carrying UKF initializers;
4. finite rank-one degree-two core shapes;
5. finite rank-four seeded core shapes;
6. manifest nonclaims and forbidden-data-use flags;
7. compatibility with `TrainableFunctionalTT` finite `rho_theta`,
   normalizer, and log density;
8. downstream `P75ObjectiveBatch` audit-record rejection;
9. static absence of the failed P75 source-prefit call names in the new module.

## Local Checks

Commands run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/ukf_initializer.py tests/highdim/test_p76_ukf_initializer.py
rg -n "square_root_prefit|source_guided_prefit|source-route prefit" bayesfilter/highdim/ukf_initializer.py tests/highdim/test_p76_ukf_initializer.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_ukf_initializer.py tests/highdim/test_p75_stochastic_density_training.py
git diff --check -- bayesfilter/highdim/ukf_initializer.py tests/highdim/test_p76_ukf_initializer.py docs/plans/bayesfilter-highdim-zhao-cui-p76-phase3-optin-ukf-initializer-implementation-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase4-tiny-ukf-initializer-smoke-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
```

Observed results:

- compile: passed;
- source-prefit leakage search: no hits, exit code 1 as expected for no match;
- tests: `24 passed, 2 warnings in 3.79s`;
- `git diff --check`: passed;
- warnings: TensorFlow Probability `distutils Version` deprecation warnings
  from the installed environment, not P76 failures.

## Implementation Notes

The projection coefficients use the normalized one-dimensional factor
\[
  h_{U,k}(z)
  =
  \frac{\exp(-\gamma^2z^2/4)}
       {\left(\int_{-1}^1\exp(-\gamma^2z^2/2)\,d\nu_k(z)\right)^{1/2}},
\]
matching the Phase 1 \(h_U=\sqrt{q_U}\) contract.

The rank embedding keeps the projected rank-one factor on channel 0 and adds
small deterministic extra-channel paths.  These extra paths are trainability
guards only; they are not source-faithful Zhao--Cui behavior and do not prove
rank necessity.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Proceed to Phase 4 tiny smoke planning/review | Passed locally | No Phase 3 veto observed locally | Whether the initializer improves any tiny downstream diagnostic remains untested | Review implementation/result/subplan with Claude, then run the reviewed tiny smoke if agreed | No lower-gate repair, no validation/HMC readiness, no large mini-batch pilot |

## Phase 4 Handoff

Phase 4 may run only a tiny CPU-only diagnostic comparing the implemented UKF
initializer against historical failure criteria at smoke scale.  It must not
launch a large mini-batch pilot, change defaults, use GPU/CUDA, or claim that
the lower gate is repaired.
