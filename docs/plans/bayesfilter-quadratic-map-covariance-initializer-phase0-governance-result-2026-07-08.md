# Phase 0 Result: Governance And API Boundary

Date: 2026-07-08

## Status

`PASSED_WITH_CODEX_FALLBACK_REVIEW`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 0 passes. Proceed to Phase 1 implementation under the reviewed runbook. |
| Primary criterion status | Passed: planning artifacts encode BFGS as locator only, constrained SPD quadratic as covariance authority, sample-budget guard, fail-closed behavior, focused tests, review/repair loop, and nonclaims. |
| Veto diagnostic status | No local py_compile failure, unsupported MAP/HMC claim, missing stop condition, or BFGS curvature authority found. |
| Main uncertainty | Claude external review could not be used because the managed approval reviewer blocked external transfer of private repo planning context. |
| Next justified action | Implement reusable initializer API with a binding requirement that accepted precision routes through `covariance_from_precision`. |
| Not concluded | No implementation correctness, no global MAP, no posterior covariance correctness, no HMC readiness, no sampler convergence, no default readiness, no Zhao-Cui source faithfulness. |

## Checks Run

| Check | Result |
| --- | --- |
| `git status --short` | Passed: only new planning/review artifacts were untracked at check time. |
| `python -m py_compile bayesfilter/inference/quadratic_geometry.py bayesfilter/inference/mass_matrix.py bayesfilter/inference/__init__.py` | Passed, exit 0. |
| Planning-boundary text search | Passed: nonclaim and covariance-authority boundaries are present in the artifacts. |

## Review Record

Requested Claude review gate:

```text
bash /home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh \
  --cwd /home/ubuntu/python/BayesFilter \
  --review-name bayesfilter-quadratic-map-covariance-initializer-phase0-review \
  --bundle /home/ubuntu/python/BayesFilter/docs/reviews/bayesfilter-quadratic-map-covariance-initializer-phase0-review-bundle-2026-07-08.md \
  --model opus \
  --effort max \
  --probe-timeout 90 \
  --timeout-seconds 180 \
  --max-retries 1 \
  --allow-bounded-fallback
```

The command was not executed after approval review rejected it as unsafe
external transfer of private repository planning context. This is a review
availability/boundary event, not evidence against the plan.

Fresh Codex read-only fallback review was then run. It returned:

```text
VERDICT: AGREE
```

Residual risk from fallback review:

- `fit_low_rank_spd_quadratic_geometry` currently computes covariance by direct
  inversion internally. Phase 1 must ensure the new initializer path routes any
  accepted precision through `covariance_from_precision` and records that
  provenance.

## Plain-Language Gate

| Item | Status |
| --- | --- |
| Claimed target | Correct: Phase 0 planning readiness only. |
| Computed quantity | Correct: local checks and read-only planning review status. |
| Unsupported claims | None accepted; MAP/HMC/posterior/default/Zhao-Cui claims remain forbidden. |
| Mismatches | None found. |
| Remaining unevaluated | Implementation, public API, unit validation, benchmark smoke, and HMC readiness. |

## Handoff To Phase 1

Phase 1 may start with the following binding conditions:

- BFGS/L-BFGS output is a locator result only.
- The accepted covariance candidate must be built through
  `covariance_from_precision`, not through optimizer inverse Hessian and not by
  relying only on direct inversion from `fit_low_rank_spd_quadratic_geometry`.
- The result payload must include explicit nonclaims.
- Focused tests must cover sign convention, Gaussian mode/covariance recovery,
  fail-closed nonfinite behavior, locator failure fallback, sample-budget guard,
  and public export behavior.
