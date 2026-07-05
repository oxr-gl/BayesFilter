# Phase 1 Result: Generic SSM Contract Scaffold

Date: 2026-07-03

Status: `PHASE1_GATE_PASSED`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can BayesFilter represent a generic Bayesian SSM target boundary with stable manifests and fail-closed metadata checks? |
| Baseline/comparator | Existing `NonlinearSSMAdapterContract`, `ValueScoreCapability`, and stable signature discipline. |
| Primary criterion | Passed: focused contract tests passed; all five Phase 1 objective surfaces are represented with stable manifest payloads and fail-closed validation. |
| Veto diagnostics | No Phase 1 veto fired. Tests cover missing dimensions, duplicate parameters, process-local identities, missing prior/filter/transport binding fields, unknown target policy, and import/export failures. |
| Explanatory diagnostics | Added 2 source files and 14 focused tests. |
| Not concluded | No likelihood correctness, no filter implementation, no XLA readiness, no HMC readiness, no NeuTra training or artifact compatibility. |

## Source Paths

- `bayesfilter/ssm/contracts.py`
- `bayesfilter/ssm/__init__.py`
- `tests/test_general_ssm_contracts.py`

## Exported Symbol Inventory

Public `bayesfilter.ssm.__all__` exports:

- `ApproximationSemantics`
- `BayesianSSMProblem`
- `DeterministicTargetPolicy`
- `FilterProgram`
- `FrozenTransportBinding`
- `InvalidSSMContract`
- `LogJacobianConvention`
- `ParameterChart`
- `ParameterPrior`
- `PriorLogDensityAuthority`
- `PriorSupportPolicy`
- `SSMDataSignature`
- `SSMStaticShape`
- `SSMTargetContract`
- `TargetCoordinateConvention`
- `stable_filter_program_signature`
- `stable_frozen_transport_signature`
- `stable_parameter_chart_signature`
- `stable_prior_signature`
- `stable_problem_signature`
- `stable_ssm_target_signature`
- `validate_ssm_target_contract`

Top-level `bayesfilter.__all__` was not expanded in Phase 1.

## Internal-Only Helper Inventory

Internal helpers in `bayesfilter/ssm/contracts.py`:

- `_coerce_manifest`
- `_coerce_shape`
- `_KNOWN_APPROXIMATION_SEMANTICS`
- `_KNOWN_DETERMINISTIC_TARGET_POLICIES`
- `_KNOWN_LOG_JACOBIAN_CONVENTIONS`
- `_KNOWN_PRIOR_AUTHORITIES`
- `_KNOWN_PRIOR_SUPPORT_POLICIES`
- `_KNOWN_TARGET_COORDINATES`
- `_nonempty_text`
- `_normalize_for_json`
- `_PROCESS_LOCAL_SIGNATURE_PATTERNS`
- `_reject_process_local_identity`
- `_require_matching_hash`
- `_shape_size`
- `_stable_hash`

These are not exported and should not be used as public API in Phase 2.

## Guaranteed Manifest And Schema Fields

SSM target identity:

- `problem_id`
- `static_shape`
- `data_signature`
- `target_coordinate_convention`
- `model_manifest`

Static shape:

- `horizon`
- `state_dim`
- `observation_dim`
- `innovation_dim`
- `parameter_dim`

Data signature:

- `dataset_id`
- `observation_shape`
- `mask_shape`
- `data_hash`

Parameter chart:

- `parameter_names`
- `unconstrained_dim`
- `constrained_shape`
- `transform_manifest`
- `log_jacobian_convention`

Prior:

- `prior_manifest`
- `support_policy`
- `log_density_authority`

Filter program:

- `filter_id`
- `required_model_capabilities`
- `deterministic_target_policy`
- `approximation_semantics`
- `filter_manifest`

Frozen transport binding:

- `transport_id`
- `dimension`
- `target_signature`
- `log_jacobian_available`
- `transport_manifest`

Full target contract:

- `problem`
- `chart`
- `prior`
- `filter_program`
- `frozen_transport`

## Guaranteed Validation Behaviors

Phase 1 tests guarantee that the contract scaffold rejects:

- nonpositive SSM dimensions;
- observation horizon mismatch;
- duplicate or empty parameter names;
- missing transform, model, prior, filter, or transport hash/binding fields;
- unknown target coordinate, log-Jacobian, prior support, prior authority,
  deterministic target policy, or approximation semantics labels;
- process-local identities such as `object at 0x...` in manifest/signature
  material;
- frozen transport dimension mismatch;
- frozen transport target-signature mismatch;
- missing frozen transport when explicitly required;
- stochastic-not-HMC-ready filters when deterministic target readiness is
  required.

## Local Checks

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_contracts.py -q -p no:cacheprovider
14 passed in 6.31s
```

Role in evidence contract:

- public namespace/export allowlist;
- import smoke for `bayesfilter`, `bayesfilter.inference`, and
  `bayesfilter.ssm`;
- stable signature checks for problem, chart, prior, filter, frozen transport,
  and full target contract;
- positive and fail-closed cases for each Phase 1 objective surface.

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
import bayesfilter
import bayesfilter.inference
import bayesfilter.ssm
print('IMPORT_SMOKE_OK')
PY
```

Observed output included existing TensorFlow and matplotlib import warnings before
`IMPORT_SMOKE_OK`. This is an existing import-boundary behavior of the current
top-level/inference stack, not a new Phase 1 HMC, training, or GPU claim.

CPU hiding was intentional for these contract/import checks. No GPU/CUDA device
was detected, initialized, benchmarked, or used.

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | Passed for Phase 1 metadata contract scaffold. |
| Veto diagnostic status | No active Phase 1 veto. |
| Main uncertainty | The contracts have not yet been connected to executable value/score builders or real filters. |
| Next justified action | Refresh and review Phase 2 target-builder subplan using the exact Phase 1 exported names. |
| What is not concluded | No posterior correctness, HMC readiness, NeuTra readiness, artifact reuse success, or production default change. |

## Phase 2 Assumptions And Handoff

Phase 2 may rely on:

- `SSMTargetContract.manifest_payload()`;
- `stable_ssm_target_signature(contract)`;
- `validate_ssm_target_contract(contract, require_filter_hmc_target_ready=True)`;
- public contract objects from `bayesfilter.ssm.__all__`;
- stable JSON-normalized SHA-256 signatures that reject process-local identity.

Phase 2 must preserve:

- no training, serious HMC, GPU run, package install, network fetch, or detached
  execution without an explicit later-phase gate and human approval where
  required;
- TensorFlow/TFP default for differentiable implementation paths;
- no NumPy in BayesFilter-owned differentiable target-builder implementation;
- public API boundary: Phase 2 should avoid top-level `bayesfilter.__all__`
  expansion unless reviewed.

## Gate Status

`PHASE1_GATE_PASSED`

Phase 1 local checks passed and the refreshed Phase 2 subplan review gate
converged with Claude `VERDICT: AGREE`.
