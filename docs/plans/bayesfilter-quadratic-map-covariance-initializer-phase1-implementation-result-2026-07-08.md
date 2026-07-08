# Phase 1 Result: Reusable Initializer Implementation

Date: 2026-07-08

## Status

`PASSED_SOURCE_COMPILE_IMPORT_GATE`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 1 source implementation gate passes. Proceed to Phase 2 focused validation. |
| Primary criterion status | Passed: source compiles and exports a reusable API whose accepted covariance is rebuilt through `covariance_from_precision`; optimizer diagnostics label L-BFGS as locator only. |
| Veto diagnostic status | No compile failure, BFGS inverse Hessian covariance authority, direct HMC launch, broad benchmark refactor, or missing nonclaims observed in the source diff. |
| Main uncertainty | Behavioral correctness is not yet proven; sign convention, fallback behavior, covariance recovery, and failure handling still require Phase 2 tests. |
| Next justified action | Run focused pytest validation on controlled targets and public API behavior. |
| Not concluded | No global MAP, posterior covariance correctness, HMC readiness, sampler convergence, default readiness, or Zhao-Cui source faithfulness. |

## Source Changes

- Added `bayesfilter/inference/quadratic_map_covariance.py`.
- Exported new symbols through `bayesfilter.inference`.
- Added lazy top-level exports through `bayesfilter`.
- Extended common public API symbol coverage for the new exports.

## Checks Run

| Check | Result |
| --- | --- |
| `python -m py_compile bayesfilter/inference/quadratic_map_covariance.py bayesfilter/inference/__init__.py bayesfilter/__init__.py` | Passed, exit 0. |
| Import smoke for new symbols through `bayesfilter.inference` and top-level `bayesfilter` | Passed; all checked symbols are importable and in top-level `__all__`. |
| `git diff --check` | Passed, exit 0. |

## Authority Split

| Quantity | Source in implementation | Status |
| --- | --- | --- |
| Locator position | Optional TFP L-BFGS on negative log probability, fallback to finite initial point | `locator_only` |
| Fitted precision | `fit_low_rank_spd_quadratic_geometry` | covariance authority input |
| Accepted covariance | `covariance_from_precision(geometry.precision, ...)` | required provenance satisfied |
| Map candidate | Quadratic refined center if accepted, otherwise locator position | diagnostic only |

## Plain-Language Gate

| Item | Status |
| --- | --- |
| Claimed target | Correct: source compile/import and authority split only. |
| Computed quantity | Correct: source diff plus compile/import checks. |
| Unsupported claims | None accepted; behavioral correctness deferred to Phase 2. |
| Mismatches | None found. |
| Remaining unevaluated | Gaussian recovery, sign convention, fallback behavior, nonfinite rejection, sample-budget rejection, public API pytest, benchmark smoke. |

## Handoff To Phase 2

Phase 2 must validate:

- Gaussian/quadratic target recovers the mode and covariance within stated
  tolerances.
- Log-probability sign convention is correct.
- L-BFGS failure or disabled locator does not provide covariance authority.
- Nonfinite initial target fails closed.
- Insufficient finite samples reject.
- Public API symbols pass the existing public API test.
