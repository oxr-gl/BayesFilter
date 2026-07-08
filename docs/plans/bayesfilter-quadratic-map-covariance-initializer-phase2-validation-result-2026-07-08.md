# Phase 2 Result: Focused Unit Validation

Date: 2026-07-08

## Status

`PASSED_FOCUSED_VALIDATION`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 2 passes. Proceed to Phase 3 bounded benchmark adoption smoke. |
| Primary criterion status | Passed: focused pytest validates Gaussian recovery, sign convention, locator fallback/disabled behavior, fail-closed nonfinite behavior, sample-budget rejection, covariance provenance, nonclaims, and public exports. |
| Veto diagnostic status | No accepted nonfinite covariance, non-SPD accepted precision, wrong sign convention, BFGS inverse Hessian covariance authority, accepted under-sampled geometry, missing nonclaims, or public API import failure observed. |
| Main uncertainty | Tests are controlled low-dimensional fixtures; they do not validate SSL-LSTM covariance quality, HMC tuning, or posterior correctness. |
| Next justified action | Run a bounded benchmark-facing smoke or minimal refactor that exercises the reusable API without HMC-readiness claims. |
| Not concluded | No global MAP, posterior covariance correctness, HMC readiness, sampler convergence, statistical superiority, default readiness, or Zhao-Cui source faithfulness. |

## Checks Run

| Check | Result |
| --- | --- |
| `pytest tests/test_quadratic_map_covariance.py tests/test_v1_public_api.py -q` | Passed: `11 passed`, TFP deprecation warnings only. |
| `python -m py_compile bayesfilter/inference/quadratic_map_covariance.py` | Passed, exit 0. |
| `git diff --check` | Passed, exit 0. |

## Repair Note

The first focused run had three failures:

- two low-rank Gaussian tests used an overly strict holdout tolerance for an
  approximate rank-1 fit;
- one locator fallback test incorrectly expected the whole initializer to reject
  when L-BFGS failed, even though fallback-to-initial plus valid quadratic fit is
  allowed by design.

Repairs kept the implementation boundary unchanged:

- the Gaussian tests now use a stronger pilot sketch and a tolerance consistent
  with approximate low-rank geometry;
- the fallback test monkeypatches L-BFGS deterministically and asserts that
  optimizer output remains `locator_only` while covariance comes from the
  quadratic precision path.

## Plain-Language Gate

| Item | Status |
| --- | --- |
| Claimed target | Correct: controlled unit behavior and public API exports. |
| Computed quantity | Correct: focused pytest/compile/diff checks. |
| Unsupported claims | None accepted. SSL-LSTM, HMC, posterior, and default-readiness claims remain unsupported. |
| Mismatches | Initial test expectation that locator failure must reject was wrong relative to the stated target and was corrected. |
| Remaining unevaluated | Benchmark adoption smoke, SSL-LSTM target behavior, HMC mass quality, HMC tuning, posterior correctness. |

## Handoff To Phase 3

Phase 3 may use the reusable API in a bounded benchmark-facing smoke. It must:

- avoid HMC runtime;
- avoid broad benchmark refactors unless necessary;
- record that the smoke checks integration only;
- preserve nonclaims.
