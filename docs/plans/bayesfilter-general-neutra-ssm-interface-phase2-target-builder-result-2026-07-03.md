# Phase 2 Result: Posterior Target Builder And Toy Nonlinear Fixture

Date: 2026-07-03

Status: `PHASE2_GATE_PASSED`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the generic contracts produce a deterministic batch-native posterior value/score adapter for a toy nonlinear SSM and deterministic filter? |
| Baseline/comparator | Direct prior plus deterministic toy filter likelihood in unconstrained coordinates. |
| Primary criterion | Passed: the builder emits finite rank-1 values and rank-2 scores for `[B, D]`, rejects `[D]` when batch-native mode is required, allows `[1, D]`, preserves the Phase 1 target signature, carries non-batch `SSMStaticShape` dimensions plus batch-rank policy, and produces stable adapter signatures. |
| Veto diagnostics | No active veto. The implementation contains no hidden row loop, `tf.map_fn`, or `tf.vectorized_map` in `GenericSSMPosteriorAdapter.log_prob_and_grad`; no stochastic fresh randomness is used; no fallback authority is promoted to XLA; top-level `bayesfilter.__all__` was not expanded. |
| Explanatory diagnostics | A finite-difference test initially caught a wrong sign in the toy filter fixture score; the fixture score was corrected and the focused test suite then passed. |
| Not concluded | No correctness for real models, no HMC readiness, no NeuTra training readiness, no all-filter support, no posterior convergence, no production default change. |

## Source Paths

- `bayesfilter/ssm/target_builder.py`
- `bayesfilter/ssm/__init__.py`
- `tests/test_general_ssm_target_builder.py`
- `tests/test_general_ssm_contracts.py`

## Exported Symbol Inventory

New public `bayesfilter.ssm.__all__` exports added in Phase 2:

- `BatchRankPolicy`
- `BatchValueScoreFn`
- `GenericSSMPosteriorAdapter`
- `InvalidSSMTargetBuilderContract`
- `SSMTargetBuilderMetadata`
- `TARGET_BUILDER_NONCLAIMS`
- `build_ssm_posterior_adapter`
- `stable_ssm_posterior_adapter_signature`

These target-builder exports are lazy-loaded through `bayesfilter.ssm.__getattr__`
so `import bayesfilter.ssm` does not initialize TensorFlow. Resolving the
target-builder symbols imports `bayesfilter.ssm.target_builder` and TensorFlow.

Top-level `bayesfilter.__all__` was not expanded.

## Target And Computed Quantity

Claimed toy target:

```text
log posterior(theta) = log prior(theta) + deterministic toy filter log likelihood(theta)
```

Computed quantity:

- `GenericSSMPosteriorAdapter.log_prob_and_grad(theta)` for rank-2
  `theta: [B, D]`.
- Value shape: `[B]`.
- Score shape: `[B, D]`.

Equality checks performed:

- direct value/score equality against separately evaluated prior plus filter
  fixture;
- finite-difference comparison of the total target score for a batch of one;
- shape validation through `evaluate_batch_native_value_score`.

## Manifest And Signature Guarantees

The adapter manifest/signature path includes:

- schema: `bayesfilter.ssm.generic_posterior_adapter.v1`;
- Phase 1 `SSMTargetContract` signature;
- dtype;
- parameter dimension;
- parameter names;
- batch-rank policy: `rank2_required`;
- non-batch static SSM dimensions from `SSMStaticShape`;
- value/score authority;
- runtime backend;
- target scope;
- contract manifest in `manifest_payload()`.

`stable_ssm_posterior_adapter_signature(adapter)` returns the same persisted
signature consumed by `bayesfilter.inference.stable_adapter_signature(adapter)`.

## Local Checks

Passed after one fixture-sign repair:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_contracts.py tests/test_general_ssm_target_builder.py -q -p no:cacheprovider
24 passed in 3.70s
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
import bayesfilter.ssm
print('SSM_IMPORT_SMOKE_OK')
PY
```

Output:

```text
SSM_IMPORT_SMOKE_OK
```

Static scan:

```text
{'loop_hits': []}
```

The scan checked `bayesfilter/ssm/target_builder.py` for `for`, `while`,
`tf.map_fn`, and `tf.vectorized_map` nodes.

CPU hiding was intentional for these toy contract/compile checks. No GPU/CUDA
device was benchmarked or used.

## Repair Note

The first Phase 2 focused test run failed the finite-difference score check for
the toy filter fixture. The posterior builder was not loosened. The fixture
score signs for the nonlinear `sigma` and linear `beta` likelihood terms were
corrected, then the full focused check passed.

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | Passed for toy deterministic target-builder scope. |
| Veto diagnostic status | No active Phase 2 veto. |
| Main uncertainty | The builder has not yet been connected to a registry that checks real model/filter capability compatibility. |
| Next justified action | Refresh and review Phase 3 filter-registry subplan using the Phase 2 exported target-builder names. |
| What is not concluded | No real-model correctness, HMC readiness, NeuTra readiness, all-filter support, posterior validity, or default-policy change. |

## Phase 3 Handoff

Phase 3 may rely on:

- `GenericSSMPosteriorAdapter`;
- `SSMTargetBuilderMetadata`;
- `build_ssm_posterior_adapter`;
- `stable_ssm_posterior_adapter_signature`;
- `SSMTargetContract`, `FilterProgram`, and `validate_ssm_target_contract`;
- target-builder manifest fields listed above.

Phase 3 must preserve:

- no changes to existing filter numerical policy;
- no claim that arbitrary particle filters are HMC-ready;
- no top-level public API expansion without review;
- no serious HMC, NeuTra training, GPU run, package install, network fetch, or
  detached execution.

## Gate Status

`PHASE2_GATE_PASSED`

Phase 2 local checks passed and the refreshed Phase 3 subplan review gate
converged with Claude `VERDICT: AGREE`.
