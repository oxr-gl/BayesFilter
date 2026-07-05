# Phase 5 Result: Fixed-Transport HMC Runtime Binding

Date: 2026-07-03

Status: `PHASE5_GATE_PASSED`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can a generic frozen-transport target be passed to BayesFilter HMC mechanics with complete target/transport/HMC manifests and fail-closed authority checks? |
| Baseline/comparator | Existing fixed-transport value/score adapter and existing HMC policy metadata. |
| Primary criterion | Passed: tiny CPU-only mechanics binding emits finite value/score, manifest fields are complete, runtime label states mechanics-only CPU smoke, and fallback value/score authority cannot enter XLA HMC. |
| Veto diagnostics | No active veto. Tests cover target signature, transport hash, HMC policy label/hash, scalar target rejection, fallback authority rejection for XLA, CPU-only mechanics labeling, and stable manifest signatures. |
| Explanatory diagnostics | Value shape, score shape, policy label/hash, target signature, transport hash, and adapter signature. No acceptance, ESS, R-hat, or chain samples were produced. |
| Not concluded | No serious HMC convergence, no default sampler readiness, no real-artifact reuse success, no performance claim, no posterior validity. |

## Source Paths

- `bayesfilter/inference/fixed_transport_hmc.py`
- `bayesfilter/inference/__init__.py`
- `tests/test_fixed_transport_hmc_binding.py`

## Exported Symbol Inventory

New public `bayesfilter.inference.__all__` exports added in Phase 5:

- `FIXED_TRANSPORT_HMC_BINDING_NONCLAIMS`
- `FixedTransportHMCManifest`
- `FixedTransportHMCMechanicsResult`
- `InvalidFixedTransportHMCBinding`
- `bind_fixed_transport_hmc_mechanics`
- `stable_fixed_transport_hmc_manifest_signature`

## Run Manifest Fields

`FixedTransportHMCManifest` records:

- `target_signature`;
- `transport_hash`;
- `hmc_policy_label`;
- `hmc_policy_hash`;
- `xla_hmc_ready`;
- `use_xla`;
- `mass_policy`;
- `seed`;
- `execution_device`;
- `mechanics_only`;
- `adapter_signature`;
- `nonclaims`.

## Mechanics Smoke Scope

What the tiny smoke does:

- constructs `FixedTransportValueScoreAdapter` from a loaded synthetic frozen
  artifact and a base adapter;
- evaluates one batch-shaped `[B, D]` value/score mechanics call;
- records target/transport/HMC policy manifest fields;
- rejects scalar `[D]` initial position;
- rejects fallback value/score authority when `use_xla=True`.

What it does not prove:

- no HMC chain was sampled;
- no adaptation was run;
- no acceptance, ESS, R-hat, or convergence diagnostic exists;
- no real NeuTra artifact was reused;
- no default HMC policy changed.

## Local Checks

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_fixed_transport_hmc_binding.py tests/test_batched_value_score.py -q -p no:cacheprovider
25 passed in 4.10s
```

Passed cumulative focused check:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_contracts.py tests/test_general_ssm_target_builder.py tests/test_general_ssm_filter_registry.py tests/test_neutra_artifact_loader.py tests/test_fixed_transport_hmc_binding.py -q -p no:cacheprovider
44 passed in 4.17s
```

Passed export smoke:

```text
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
from bayesfilter.inference import bind_fixed_transport_hmc_mechanics, FixedTransportHMCManifest
print('FIXED_TRANSPORT_HMC_EXPORT_SMOKE_OK')
PY
```

Output included existing TensorFlow/matplotlib import noise from the inference
namespace and then:

```text
FIXED_TRANSPORT_HMC_EXPORT_SMOKE_OK
```

Static scan:

```text
{'sample_chain_attrs': []}
```

The scan checked `bayesfilter/inference/fixed_transport_hmc.py` for
`sample_chain` calls.

CPU hiding was intentional for this mechanics-only smoke. No GPU/CUDA device was
benchmarked or used.

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for mechanics binding and manifest completeness. |
| Statistically supported ranking | Not supported; no stochastic comparison was run. |
| Descriptive-only differences | Value/score shapes and manifest hashes only. |
| Default-readiness | Not supported. |
| Next evidence needed | Real artifact inventory/signature reuse classification in Phase 6, then a reviewed validation ladder in Phase 7. |

## Decision Table

| Decision field | Status |
| --- | --- |
| Primary criterion | Passed for CPU-only fixed-transport mechanics binding scope. |
| Veto diagnostic status | No active Phase 5 veto. |
| Main uncertainty | Real NeuTra artifacts have not been inventoried, matched, or reused. |
| Next justified action | Refresh and review Phase 6 existing-artifact reuse bridge. |
| What is not concluded | No real-artifact reuse success, HMC convergence, sampler readiness, posterior validity, ranking, or default-policy change. |

## Phase 6 Handoff

Phase 6 may rely on:

- `bind_fixed_transport_hmc_mechanics`;
- `FixedTransportHMCManifest`;
- `stable_fixed_transport_hmc_manifest_signature`;
- loader outputs from Phase 4;
- mechanics-only nonclaims and manifest fields above.

Phase 6 must preserve:

- missing/mismatched artifacts are not reusable;
- hash and target-signature status must be recorded before any canary;
- any canary is loader/value mechanics only unless a later reviewed plan
  authorizes more;
- no retraining, serious HMC, large artifact commits, or network/credential use
  without explicit approval.

## Gate Status

`PHASE5_GATE_PASSED`

Phase 5 local checks passed and the refreshed Phase 6 subplan review gate
converged with Claude `VERDICT: AGREE`.
