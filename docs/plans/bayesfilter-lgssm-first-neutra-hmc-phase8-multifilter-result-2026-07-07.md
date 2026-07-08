# Phase 8 Result: Simple Nonlinear Multi-Filter Target Gate

Date: 2026-07-07

## Scope

This result closes the Phase 8 multi-filter target/filter semantics gate for
the LGSSM-first NeuTra/HMC program.  It extends the Phase 7 simple nonlinear
Model B generic adapter from one deterministic sigma-point route to two
admitted deterministic routes and records two deferred routes with explicit
blockers.

This is not NeuTra training, HMC sampling, sampler tuning, posterior
convergence validation, production readiness, or a scientific validity claim.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | `PASSED_SIMPLE_NONLINEAR_MULTIFILTER_GATE` |
| Primary criterion status | Passed for `tf_svd_ukf` and `tf_svd_cubature`: each has explicit deterministic approximation semantics, stable metadata, finite batch-native value/score, and finite-difference score checks. |
| Veto diagnostic status | No veto fired for admitted routes: no hidden training, HMC, GPU work, nonfinite value/score, unstable default signature, or filter-evidence borrowing. |
| Main uncertainty | Finite value/score and finite-difference checks are interface diagnostics only; they do not establish posterior correctness or learned transport quality. |
| Next justified action | Phase 9 may plan GPU-only NeuTra training preflight for admitted simple nonlinear routes, with CPU multicore sample generation kept separate. |
| What is not concluded | Learned NeuTra quality, HMC convergence, posterior correctness, sampler superiority, production readiness, default-policy change, or scientific validity. |

## Route Outcomes

| Route | Backend | Outcome |
| --- | --- | --- |
| `model-b-svd-ukf-deterministic-loglikelihood` | `tf_svd_ukf` | Admitted; Phase 7 default signature preserved. |
| `model-b-svd-cubature-deterministic-loglikelihood` | `tf_svd_cubature` | Admitted; finite value/score and finite-difference checks passed through generic adapter. |
| `model-b-svd-cut4-deterministic-loglikelihood` | `tf_svd_cut4` | Deferred until a dedicated generic-adapter finite-difference and branch-diagnostic gate is reviewed. |
| `model-b-principal-sqrt-ukf-deterministic-loglikelihood` | `tf_principal_sqrt_ukf` | Deferred until principal-square-root/custom-op availability and provenance are gated for this target. |

## Signatures

Default SVD-UKF target signature:

```text
c6a942c251e08f111b5647f814c1815535f931fcd13a09d337a74b8fb5eacaa0
```

Default SVD-UKF adapter signature:

```text
9fdc2ef475992711dd1ed5aadc0b47aeed235d7ccea9e9567740b57aaf2a04dd
```

SVD cubature target signature:

```text
19e87b2090c353ddc855791c36a1a325246b0a275886c92f3fa8dc625467d1ee
```

SVD cubature adapter signature:

```text
39927792f114f9d80f540b4f6759e9b5cd22c4c55d1d5cb7df13fc0e4756a9b9
```

Validation JSON:

```text
docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase8-multifilter-validation-2026-07-07.json
```

## Skeptical Plan Audit

| Risk | Control |
| --- | --- |
| Wrong baseline | Phase 8 compares route admissibility against the Phase 7 Model B adapter only; it does not borrow DSGE/c603, LGSSM training, or LEDH evidence. |
| Proxy metric promoted | Finite value/score and finite-difference checks are adapter gates only, not posterior correctness or route ranking. |
| Missing stop conditions | Deferred routes are explicitly blocked; admitted routes require stable metadata and finite value/score checks. |
| Hidden assumptions | Both admitted routes are deterministic sigma-point approximations, and this is recorded in each `FilterProgram`. |
| Artifact mismatch | Required output is route inventory, focused tests, result, validation JSON, and next subplan, not a trained transport or sampler artifact. |

Audit status: passed for Phase 8 target/filter interface execution.

## Implementation Artifacts

- `bayesfilter/testing/simple_nonlinear_generic_target_adapter_tf.py`
- `tests/test_simple_nonlinear_generic_target_adapter_tf.py`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase8-multifilter-semantics-note-2026-07-07.md`

## Local Checks

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_simple_nonlinear_generic_target_adapter_tf.py -q
```

Result:

```text
23 passed, 2 warnings in 8.08s
```

Required combined Phase 7/8 replay:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_simple_nonlinear_generic_target_adapter_tf.py \
  tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py -q
```

Result:

```text
32 passed, 2 warnings in 12.91s
```

```text
python -m py_compile \
  bayesfilter/testing/simple_nonlinear_generic_target_adapter_tf.py \
  tests/test_simple_nonlinear_generic_target_adapter_tf.py
```

Result:

```text
passed
```

The validation command was CPU-hidden with `CUDA_VISIBLE_DEVICES=-1`.
TensorFlow emitted CUDA/cuInit registration noise on import; under the local
policy this is CPU-hidden adapter evidence, not GPU evidence and not a GPU
failure diagnosis.

## Review

Claude review was attempted through the project review gate but was blocked by
the approval reviewer before execution because the external Claude destination
was not established as trusted for private workspace review material.  This is
recorded in:

```text
docs/reviews/bayesfilter-lgssm-first-neutra-hmc-phase8-claude-review-unavailability-2026-07-07.md
```

A fresh Codex read-only fallback review inspected the Phase 8 result and Phase
9 subplan boundaries and returned:

```text
VERDICT: AGREE
```

The fallback result is recorded in:

```text
docs/reviews/bayesfilter-lgssm-first-neutra-hmc-phase8-codex-review-result-2026-07-07.md
```

## Nonclaims

- No NeuTra training was run.
- No HMC sampling or tuning was run.
- No GPU work was run.
- No route ranking is claimed.
- No exact nonlinear likelihood claim is made for either admitted route.
- No posterior correctness, convergence, sampler superiority, production
  readiness, default-policy change, or scientific validity is claimed.
