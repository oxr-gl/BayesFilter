# Phase 1 Result: Low-Rank SPD Quadratic Geometry Utility

Date: 2026-07-08
Status: `PASSED_FOCUSED_UTILITY_CHECKS`

## Decision

Phase 1 passed. A reusable low-rank SPD quadratic geometry utility was added with focused tests for the declared mechanical gates.

The utility remains a diagnostic geometry initializer. It does not certify a MAP, posterior correctness, HMC convergence, default readiness, or Zhao-Cui source-faithfulness.

## Implementation

| Artifact | Path |
| --- | --- |
| Utility | `bayesfilter/inference/quadratic_geometry.py` |
| Export update | `bayesfilter/inference/__init__.py` |
| Tests | `tests/test_quadratic_geometry.py` |

## Checks

| Check | Status |
| --- | --- |
| `py_compile bayesfilter/inference/quadratic_geometry.py tests/test_quadratic_geometry.py` | passed |
| `pytest tests/test_quadratic_geometry.py -q` | passed: `8 passed, 4 warnings` |
| `git diff --check` | passed |

## Evidence Contract Assessment

| Field | Result |
| --- | --- |
| Question | The utility enforces declared mechanical gates on controlled targets. |
| Baseline/comparator | Synthetic quadratic and adversarial nonfinite/undersampled/bad-holdout cases. |
| Primary criterion | Passed focused tests and structured payload diagnostics. |
| Veto diagnostics | No accepted under-sampled fit, non-SPD precision, over-condition precision, nonfinite silent accept, bad holdout accept, or out-of-trust center accept was observed in focused tests. |
| Explanatory only | Residual magnitudes and condition numbers are descriptive within tests. |
| Not concluded | No HMC performance, posterior correctness, MAP certification, target-specific readiness, GPU/XLA readiness, or source-faithful Zhao-Cui evidence. |

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | `ADVANCE_TO_PHASE2` |
| Primary criterion status | `PASSED` |
| Veto diagnostic status | `NO_PHASE1_VETO` |
| Main uncertainty | Real minimal SSL-LSTM values may be nonquadratic or too noisy for accepted geometry. |
| Next justified action | Integrate the utility as an optional minimal SSL-LSTM diagnostic geometry path with explicit fallback/provenance. |
| What is not being concluded | No sampler convergence, posterior correctness, MAP quality, default readiness, or source-faithfulness. |

## Notes

The synthetic recovery test verifies bounded low-rank SPD approximation rather than exact dense Hessian recovery. That matches the design: `Q` is learned from a pilot directional-curvature sketch and is not an oracle eigenspace.
