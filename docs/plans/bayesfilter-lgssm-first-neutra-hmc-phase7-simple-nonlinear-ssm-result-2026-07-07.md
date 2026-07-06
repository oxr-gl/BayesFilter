# Phase 7 Result: Simple Nonlinear SSM Target Adapter

Date: 2026-07-07

## Scope

This result closes the Phase 7 target-adapter gate for the LGSSM-first
NeuTra/HMC program.  It adds a BayesFilter-owned simple nonlinear non-DSGE SSM
target fixture and exposes it through the generic `SSMTargetContract` and
batch-native posterior adapter boundary.

This is not NeuTra training, HMC sampling, sampler tuning, posterior
convergence validation, production readiness, or a scientific validity claim.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | `PASSED_SIMPLE_NONLINEAR_TARGET_ADAPTER_GATE` |
| Primary criterion status | Passed: Model B nonlinear accumulation has a stable target contract and finite batch-native posterior value/score under deterministic SVD-UKF approximation. |
| Veto diagnostic status | No veto fired: no DSGE/c603 dependency, nonfinite value/score, unstable signature, hidden training, hidden HMC, or GPU work. |
| Main uncertainty | The deterministic sigma-point approximation is an adapter gate only; it does not establish posterior correctness or learned transport quality. |
| Next justified action | Phase 8 may design the multi-filter/nonlinear extension gate under a new subplan. |
| What is not concluded | Learned NeuTra quality, HMC convergence, posterior correctness, sampler superiority, broad nonlinear SSM validity, production readiness, default-policy change, or scientific validity. |

## Selected Target

- Model: `model_b_nonlinear_accumulation`
- Source: `bayesfilter.testing.nonlinear_models_tf`
- Observations: `model_b_observations_tf`
- Parameter coordinate: identity unconstrained fixture chart
- Parameter order: `(rho, sigma, beta)`
- Fixed constants:
  - `alpha = 0.55`
  - `observation_sigma = 0.30`
- Filter semantics: deterministic SVD-UKF sigma-point approximation

## Artifact Evidence

Target signature:

```text
c6a942c251e08f111b5647f814c1815535f931fcd13a09d337a74b8fb5eacaa0
```

Adapter signature:

```text
9fdc2ef475992711dd1ed5aadc0b47aeed235d7ccea9e9567740b57aaf2a04dd
```

Validation JSON:

```text
docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase7-simple-nonlinear-ssm-validation-2026-07-07.json
```

Initial adapter point:

```text
theta = [0.7, 0.25, 0.8]
```

Validation output:

- finite posterior value: `true`
- finite posterior score: `true`
- deterministic residual: `[0.0]`

## Implementation Artifacts

- `bayesfilter/testing/simple_nonlinear_generic_target_adapter_tf.py`
- `tests/test_simple_nonlinear_generic_target_adapter_tf.py`
- `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase7-target-selection-note-2026-07-07.md`

## Local Checks

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_simple_nonlinear_generic_target_adapter_tf.py -q
```

Result:

```text
8 passed, 2 warnings in 4.01s
```

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py -q
```

Result:

```text
9 passed, 2 warnings in 7.96s
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

The validation command wrote the Phase 7 JSON artifact. It was run with
`CUDA_VISIBLE_DEVICES=-1`. TensorFlow emitted CUDA/cuInit registration noise on
import; under the local policy this is CPU-hidden adapter evidence, not GPU
evidence and not a GPU failure diagnosis.

## Nonclaims

- No NeuTra training was run.
- No HMC sampling or tuning was run.
- No GPU evidence is produced.
- No posterior correctness, convergence, sampler ranking, production
  readiness, default-policy change, or scientific validity is claimed.
