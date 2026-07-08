# Phase 3 Result: Filter-Program Registry And Capability Gates

Date: 2026-07-03

Status: `PHASE3_GATE_PASSED`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can BayesFilter decide whether a model/filter pair is admissible for a deterministic HMC target before building the target? |
| Baseline/comparator | Phase 2 direct fixture binding with no registry. |
| Primary criterion | Passed: registry descriptors produce stable `FilterProgram` manifests, verify model/filter capability compatibility, and fail closed on missing model capabilities or stochastic nondeterministic HMC targets. |
| Veto diagnostics | No active veto. Tests cover stochastic fresh-randomness rejection, missing capability rejection, deterministic target policy preservation, stable signatures, and downstream `SSMTargetContract` validation. |
| Explanatory diagnostics | Accepted deterministic toy filter, accepted fixed-randomness filter only when explicitly allowed, and rejected missing-capability/stochastic fixtures. |
| Not concluded | No production particle-filter HMC readiness, no all-filter guarantee, no filter accuracy claim, no sampler validity claim. |

## Source Paths

- `bayesfilter/ssm/filter_registry.py`
- `bayesfilter/ssm/__init__.py`
- `tests/test_general_ssm_filter_registry.py`
- `tests/test_general_ssm_contracts.py`

## Exported Symbol Inventory

New public `bayesfilter.ssm.__all__` exports added in Phase 3:

- `FilterProgramDescriptor`
- `FilterProgramRegistry`
- `FilterRegistryDecision`
- `InvalidFilterRegistryContract`
- `build_filter_program_registry`
- `stable_filter_descriptor_signature`

These exports are lazy-loaded through `bayesfilter.ssm.__getattr__`.

Top-level `bayesfilter.__all__` was not expanded.

## Registry Decision Classifications

| Fixture decision | Classification | Evidence |
| --- | --- | --- |
| deterministic toy filter with matching capabilities | accepted | `test_filter_registry_accepts_capability_match_and_preserves_filter_program_signature` |
| deterministic toy filter assembled into `SSMTargetContract` | accepted | `test_filter_registry_output_feeds_ssm_target_contract_validation` |
| missing model capability | wrong relative to requested target | `test_filter_registry_rejects_missing_model_capability` |
| stochastic fresh-randomness particle filter | unsupported for deterministic HMC target | `test_filter_registry_rejects_stochastic_filter_without_deterministic_artifact_state` |
| fixed-randomness particle descriptor with explicit artifact state | accepted only when allowed | `test_filter_registry_can_accept_fixed_randomness_when_explicitly_allowed` |
| duplicate descriptor IDs | wrong relative to registry contract | `test_filter_registry_rejects_duplicate_descriptor_and_process_local_identity` |
| process-local manifest identity | wrong relative to stable artifact contract | `test_filter_registry_rejects_duplicate_descriptor_and_process_local_identity` |
| unknown filter ID | wrong relative to registry request | `test_filter_registry_rejects_unknown_filter_id_and_empty_capability_set` |

## Manifest And Signature Guarantees

`FilterProgramDescriptor` requires:

- `filter_id`;
- `required_model_capabilities`;
- `deterministic_target_policy`;
- `approximation_semantics`;
- `implementation_backend`;
- `filter_hash`;
- optional `manifest_extra`.

`FilterProgramRegistry.bind_filter_program(...)` returns `FilterRegistryDecision`
containing:

- accepted `FilterProgram`;
- stable descriptor signature;
- missing capability tuple, empty for accepted decisions;
- decision label `accepted`;
- registry nonclaims.

The registry does not replace target validation. Focused tests assemble registry
output into `SSMTargetContract` and call `validate_ssm_target_contract`.

## Local Checks

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_contracts.py tests/test_general_ssm_target_builder.py tests/test_general_ssm_filter_registry.py -q -p no:cacheprovider
32 passed in 6.33s
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
import bayesfilter.ssm
print('SSM_IMPORT_SMOKE_OK')
print('FilterProgramRegistry' in bayesfilter.ssm.__all__)
PY
```

Output:

```text
SSM_IMPORT_SMOKE_OK
True
```

Static scan:

```text
{'target_eval_attrs': []}
```

The scan checked `bayesfilter/ssm/filter_registry.py` for target-evaluation
attributes such as `log_prob`, `log_prob_and_grad`, and
`target_log_prob_and_grad`.

CPU hiding was intentional for these metadata/import checks. No GPU/CUDA device
was benchmarked or used.

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | Passed for registry descriptor/admissibility scope. |
| Veto diagnostic status | No active Phase 3 veto. |
| Main uncertainty | Real BayesFilter filter capability descriptors have not yet been inventoried or bound. |
| Next justified action | Refresh and review Phase 4 frozen NeuTra artifact-loader subplan. |
| What is not concluded | No filter correctness, all-filter support, production particle-filter HMC readiness, HMC tuning readiness, NeuTra readiness, posterior validity, or default-policy change. |

## Phase 4 Handoff

Phase 4 may rely on:

- `FilterProgramDescriptor`;
- `FilterProgramRegistry`;
- `FilterRegistryDecision`;
- `build_filter_program_registry`;
- `stable_filter_descriptor_signature`;
- Phase 1 `FrozenTransportBinding` and target-signature discipline.

Phase 4 must preserve:

- loader correctness, artifact availability, and sampler validity are separate
  ledgers;
- no NeuTra training;
- no large generated training payload commits;
- no real artifact reuse claim without target-signature match;
- no CPU-only loader check represented as GPU/training evidence.

## Gate Status

`PHASE3_GATE_PASSED`

Phase 3 local checks passed and the refreshed Phase 4 subplan review gate
converged with Claude `VERDICT: AGREE`.
