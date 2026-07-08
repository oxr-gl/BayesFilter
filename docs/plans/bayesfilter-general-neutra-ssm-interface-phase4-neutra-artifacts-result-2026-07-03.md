# Phase 4 Result: Frozen NeuTra Transport Artifact Loader

Date: 2026-07-03

Status: `PHASE4_GATE_PASSED`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can BayesFilter represent frozen NeuTra transports as reusable target transforms without retraining or weakening target authority? |
| Baseline/comparator | Existing `FixedTransportValueScoreAdapter` chain-rule behavior plus synthetic frozen affine transport fixture. |
| Primary criterion | Passed: synthetic artifact loads to a stable frozen transport manifest, mismatches fail closed, and fixed-transport wrapper preserves base value/score authority. |
| Veto diagnostics | No active veto. Tests reject unsupported schema, wrong dimension, target-signature mismatch, missing log-Jacobian availability, bad shift/scale dimensions, and process-local identities. Fallback base authority is not promoted to XLA. |
| Explanatory diagnostics | Stable artifact signature, transport manifest hash, synthetic affine roundtrip, and fixed-transport wrapper behavior. |
| Not concluded | No real artifact availability, no HMC tuning, no posterior convergence, no NeuTra training readiness, no sampler validity. |

## Source Paths

- `bayesfilter/inference/neutra_artifacts.py`
- `bayesfilter/inference/__init__.py`
- `tests/test_neutra_artifact_loader.py`

## Exported Symbol Inventory

New public `bayesfilter.inference.__all__` exports added in Phase 4:

- `FrozenAffineDiagonalTransport`
- `FrozenNeuTraArtifactManifest`
- `InvalidNeuTraArtifact`
- `LoadedFrozenNeuTraArtifact`
- `NEUTRA_ARTIFACT_NONCLAIMS`
- `load_frozen_neutra_artifact`
- `stable_frozen_neutra_artifact_signature`

## Loader Ledger

Loader correctness:

- synthetic `bayesfilter.neutra.frozen_affine_diag.v1` artifacts load;
- target signatures must match `expected_target_signature`;
- log-Jacobian availability is required;
- dimension, shift, and raw-scale lengths must match;
- manifest signatures reject process-local identity;
- loaded transports expose `manifest_payload`, `forward`, `forward_batch`,
  `log_abs_det_jacobian`, and `log_abs_det_jacobian_batch`.

Artifact availability:

- only synthetic test fixtures were loaded;
- no real external artifact availability was checked;
- no large generated payload was added.

Sampler validity:

- not checked;
- no HMC run was performed;
- no convergence, ESS, R-hat, acceptance, or posterior validity conclusion is
  supported.

## Local Checks

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_neutra_artifact_loader.py tests/test_batched_value_score.py -q -p no:cacheprovider
25 passed in 7.04s
```

Passed cumulative focused check:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_contracts.py tests/test_general_ssm_target_builder.py tests/test_general_ssm_filter_registry.py tests/test_neutra_artifact_loader.py -q -p no:cacheprovider
38 passed in 3.74s
```

Passed export smoke:

```text
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
from bayesfilter.inference import load_frozen_neutra_artifact, InvalidNeuTraArtifact
print('NEUTRA_EXPORT_SMOKE_OK')
PY
```

Output included existing TensorFlow/matplotlib import noise from the inference
namespace and then:

```text
NEUTRA_EXPORT_SMOKE_OK
```

Static import scan:

```text
{'imports': [('__future__', 7), (None, 9), (None, 10), (None, 11), ('collections.abc', 12), ('dataclasses', 13), ('typing', 14), (None, 16), ('bayesfilter.ssm', 151)]}
```

The loader imports no external model packages and no `~/python` training
modules.

CPU hiding was intentional for these loader/wrapper checks. No GPU/CUDA device
was benchmarked or used.

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | Passed for synthetic frozen artifact loader scope. |
| Veto diagnostic status | No active Phase 4 veto. |
| Main uncertainty | Real existing NeuTra artifacts have not been inventoried or loaded. |
| Next justified action | Refresh and review Phase 5 fixed-transport HMC binding subplan. |
| What is not concluded | No real artifact reuse success, NeuTra training readiness, HMC readiness, posterior validity, sampler convergence, or default-policy change. |

## Phase 5 Handoff

Phase 5 may rely on:

- `LoadedFrozenNeuTraArtifact`;
- `FrozenAffineDiagonalTransport`;
- `FrozenNeuTraArtifactManifest`;
- `load_frozen_neutra_artifact`;
- `stable_frozen_neutra_artifact_signature`;
- existing `FixedTransportValueScoreAdapter` chain-rule behavior.

Phase 5 must preserve:

- tiny HMC mechanics tests are not convergence evidence;
- CPU-only smoke tests must be labeled as CPU-only;
- fallback value/score authority cannot be promoted into XLA HMC;
- no serious HMC ladder, GPU HMC, or default-policy change without a reviewed
  later-phase gate and required approvals.

## Gate Status

`PHASE4_GATE_PASSED`

Phase 4 local checks passed and the refreshed Phase 5 subplan review gate
converged with Claude `VERDICT: AGREE`.
