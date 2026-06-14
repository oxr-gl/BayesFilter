# P51-M1 Result: Stable Score API Contract

metadata_date: 2026-06-09
phase: P51-M1
status: PASS_P51_M1_STABLE_SCORE_API
supervisor: Codex
reviewer: Claude Code read-only

## Decision

P51-M1 partially closes the original P50 `stable_top_level_score_api` gap.

The stable subpackage contract is implemented as:

- `bayesfilter.highdim.HighDimScoreAPIResult`
- `bayesfilter.highdim.evaluate_highdim_score_api`

Root-level `bayesfilter` public score API remains blocked under
`BLOCKED_PUBLIC_API_DECISION`.  This phase does not add or approve a root-level
export.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | `bayesfilter.highdim` can expose a stable deterministic score API contract for fixed TensorFlow float64 value functions. |
| Baseline/comparator | Existing P47 experimental score helper, P47 score/HMC readiness guards, P50 HMC tier guards, and the P51-M0 split manifest. |
| Primary criterion | Passed for the subpackage lane; root-level public export remains blocked pending policy approval. |
| Veto diagnostics | No root-level public export was added; finite gradients are not labeled HMC-ready; target identity, route label, parameterization, branch identity, dtype, shape, and nonclaims are guarded. |
| Not concluded | No HMC readiness. No production HMC readiness. No production model readiness. No root-level public score API. |

## Implementation

`bayesfilter/highdim/score_api.py` now contains a stable subpackage-scoped
wrapper, `evaluate_highdim_score_api`, and immutable result type,
`HighDimScoreAPIResult`.  The older `evaluate_experimental_score_api` contract
is preserved for backward compatibility.

The stable wrapper requires a rank-1 `tf.float64` parameter tensor and a scalar
`tf.float64` value.  It differentiates the value with `tf.GradientTape`, checks
that the score is finite and has the same shape as `theta`, and records
diagnostics that explicitly say:

- API scope is `bayesfilter.highdim`;
- subpackage API is stable;
- stable top-level API is false;
- HMC readiness is not claimed.

## Original P50 Gap Classification

| Original gap | P51-M1 classification | Reason |
| --- | --- | --- |
| `stable_top_level_score_api` | Partially closed | Stable `bayesfilter.highdim` score API contract passes; root-level `bayesfilter` public export remains `BLOCKED_PUBLIC_API_DECISION`. |

## Validation

Focused validation actually run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p51_stable_score_api.py tests/highdim/test_p47_score_hmc_readiness.py tests/highdim/test_p50_hmc_readiness_tiers.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/score_api.py bayesfilter/highdim/__init__.py tests/highdim/test_p51_stable_score_api.py
git diff --check -- bayesfilter/highdim/score_api.py bayesfilter/highdim/__init__.py tests/highdim/test_p51_stable_score_api.py docs/plans/bayesfilter-highdim-zhao-cui-p51-m1-stable-score-api-manifest-2026-06-09.json docs/plans/bayesfilter-highdim-zhao-cui-p51-m1-stable-score-api-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p51-visible-execution-ledger-2026-06-09.md
```

Results:

- `15 passed, 2 warnings` for the focused pytest command.  The warnings were
  TensorFlow Probability deprecation warnings from the local environment.
- `compileall` passed.
- `git diff --check` passed.

## Nonclaims

- No HMC readiness.
- No production HMC readiness.
- No production model readiness.
- No root-level `bayesfilter` public score API.
- No GPU readiness.
- No source-faithful adaptive TT/SIRT filtering.
- No S&P 500 reproduction.
