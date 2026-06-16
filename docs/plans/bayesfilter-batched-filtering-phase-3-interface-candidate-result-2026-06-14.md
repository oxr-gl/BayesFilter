# Phase 3 Result: Production Interface Candidate

Date: 2026-06-14

## Status

`PASSED`

## Objective

Implement and verify a non-default, opt-in interface candidate for experimental
batched filtering value+score.  The candidate must preserve scalar authority
semantics, expose explicit experimental metadata/nonclaims, and avoid changing
public exports or production defaults.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a non-default, opt-in batched value+score interface candidate be exposed without changing public defaults or weakening scalar fallback semantics? |
| Baseline/comparator | Existing experimental batched Kalman and SVD sigma-point kernels, Phase 1-2 tests, public API tests, and explicit scalar callback fallback behavior. |
| Primary pass criterion | Required tests pass; wrappers match underlying kernels; scalar callback fallback stacks value/score rows in order; unsupported backend fails closed; metadata records experimental status and nonclaims; public exports remain unchanged. |
| Veto diagnostics | Public export/default edit; wrapper mismatch; unsafe scalar fallback inference; wrong stacked fallback order/shape; unsupported backend accepted; metadata omits nonclaims; Phase 1-2 regression. |
| Explanatory diagnostics | Test warnings, source audit output, and the public-export test repair. |
| Not concluded | No production readiness, no default policy, no GPU performance claim, no HMC/NeuTra integration claim. |
| Artifact preserving result | This result file, `bayesfilter/experimental_batched_value_score.py`, and `tests/test_experimental_batched_value_score_interface.py`. |

## Implementation

Added:

- `bayesfilter/experimental_batched_value_score.py`
- `tests/test_experimental_batched_value_score_interface.py`

The candidate module is deliberately importable only by explicit module path and
is not added to:

- `bayesfilter.__all__`
- `bayesfilter._EXPORT_MODULES`
- `bayesfilter.linear.__all__`
- `bayesfilter.linear._EXPORT_MODULES`
- `bayesfilter.nonlinear.__all__`
- `bayesfilter.nonlinear._EXPORT_MODULES`

The module provides:

- `ExperimentalBatchedValueScoreMetadata`
- `ExperimentalBatchedValueScoreResult`
- `experimental_batched_kalman_value_score`
- `experimental_batched_svd_sigma_point_value_score`
- `experimental_scalar_callback_fallback_value_score`

## Repair Record

The first full Phase 3 pytest command failed one test:

- `test_experimental_interface_is_not_reexported_from_public_packages`

Cause:

- The test used `hasattr(bayesfilter, "experimental_batched_value_score")`
  after explicitly importing `bayesfilter.experimental_batched_value_score`.
  Python normally attaches imported submodules to their package object, so this
  was not a valid proxy for a public export/default change.

Repair:

- Replaced that assertion with checks against the repo's actual lazy public
  export boundary: `__all__` and `_EXPORT_MODULES`.

## Checks Run

### Interface And Experimental Kernel Gate

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_value_score_interface.py tests/test_experimental_batched_linear_kalman_tf.py tests/test_experimental_batched_svd_sigma_point_tf.py tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py
```

Result:

- `35 passed`
- GPU intentionally hidden with `CUDA_VISIBLE_DEVICES=-1`
- Warnings were TensorFlow/TensorFlow Probability deprecation warnings and were
  not promotion criteria.

### Public API Gate

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_v1_public_api.py -k public_api
```

Result:

- `5 passed`
- GPU intentionally hidden with `CUDA_VISIBLE_DEVICES=-1`

### Source Audit

Command:

```bash
rg -n "experimental_batched_value_score|production default|__all__|tf_batched|fallback|nonclaims" bayesfilter/experimental_batched_value_score.py tests/test_experimental_batched_value_score_interface.py
```

Result:

- Confirmed explicit experimental import path, nonclaim coverage, fallback
  coverage, and no public export additions.

## Claude Review Trail

Phase 3 subplan review converged before execution:

- `docs/plans/bayesfilter-batched-filtering-phase-3-claude-review-round-01-2026-06-14.md`
- `docs/plans/bayesfilter-batched-filtering-phase-3-claude-review-round-02-2026-06-14.md`

Round 2 ended with:

- `VERDICT: AGREE`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 3 passes | Required tests passed after scoped repair | No export/default edit, wrapper mismatch, unsupported backend acceptance, or fallback-order failure observed | Interface is still experimental and not integrated with downstream posterior adapters | Draft and review Phase 4 compiled benchmark ladder subplan | Production readiness, GPU speedup, HMC/NeuTra readiness |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `207419e49d2dbbc5c6aa3bca2f2ce450b6e2ffde` |
| Conda/Python | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| TensorFlow | `2.20.0` from Phase 0 environment validation |
| CPU/GPU status | Deliberate CPU-only checks; `CUDA_VISIBLE_DEVICES=-1` |
| Random seeds | N/A; deterministic fixtures |
| Data version | N/A; synthetic deterministic fixtures |
| Plan file | `docs/plans/bayesfilter-batched-filtering-phase-3-interface-candidate-subplan-2026-06-14.md` |
| Result file | `docs/plans/bayesfilter-batched-filtering-phase-3-interface-candidate-result-2026-06-14.md` |
| Output artifacts | New interface module and test file listed above |

## Handoff To Phase 4

Phase 4 may begin after its subplan is reviewed.  The Phase 4 subplan must
preserve these boundaries:

- GPU comparisons must be JIT/XLA compiled only.
- Compile/first-call time must be separated from warm-call timing.
- Scalar-loop comparators must be present where feasible.
- Eager GPU timing may only be a placement smoke probe, never benchmark
  evidence.
- No production default or public export change is authorized.

