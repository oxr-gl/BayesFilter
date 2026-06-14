# R1 Time-3 Observation Log-Probability Micro-Audit

## Decision

`time3_observation_logprob_dtype_delta_dominant`

## Decision Table

| Decision | Primary criterion status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- |
| `time3_observation_logprob_dtype_delta_dominant` | `observed delta 0.00012383188050080207 reconstructed by closed-form delta 0.00012383188050080207` | `whether the tiny predicted-particle delta is acceptable under a future tolerance policy` | `audit the time-3 predicted-particle generation path if we need to remove the remaining state delta` | `correctness of either implementation, dtype policy, tolerance policy` |

## Decomposition

| Quantity | Value |
| --- | ---: |
| `observed_observation_logprob_delta` | `0.00012383188050080207` |
| `closed_form_bf64_vs_filterflow_bf32_delta` | `0.00012383188050080207` |
| `closed_form_reconstruction_residual` | `0.0` |
| `closed_form_reconstruction_relative_residual` | `0.0` |
| `state_delta_bf64_same_dtype` | `2.2275554556472343e-05` |
| `dtype_delta_on_filterflow_state` | `0.00010567705180619669` |
| `predicted_particle_delta` | `8.579276994380436e-08` |
| `pre_log_weight_delta` | `2.3818361171379365e-05` |
| `post_transport_particle_delta` | `9.933807555012608e-08` |
| `per_step_log_normalizer_delta` | `9.738943936099531e-05` |
| `state_fraction_of_observed` | `0.17988545814200135` |
| `dtype_fraction_of_observed` | `0.8533913187687738` |

## Verification

| Command | Result |
| --- | --- |
| `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_time3_observation_logprob_audit_tf.py` | passed |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_r1_time3_observation_logprob_audit_tf` | passed; decision `time3_observation_logprob_dtype_delta_dominant` |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_r1_time3_observation_logprob_audit_tf --validate-only` | passed |
| `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_r1_time3_observation_logprob_audit_2026-06-02.json` | passed |
| `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_time3_observation_logprob_audit_tf.py` | no hits |
| `rg -n "student|vendored|highdim|DSGE|NAWM|docs/chapters|bayesfilter/" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_time3_observation_logprob_audit_tf.py` | no hits |
| lane-scoped trailing whitespace check | passed; `[]` |
| `git diff --check` | passed |
| `git status --short -- bayesfilter tests docs/chapters` | passed; no output |

## Interpretation

The first localized R1 observation-likelihood discrepancy is arithmetic
reproducible. The recorded BayesFilter BF64 observation log-likelihoods and
filterflow BF32 observation log-likelihoods differ by `0.00012383188050080207`;
closed-form recomputation from the recorded predicted particles and observation
reconstructs the same delta exactly in this audit. Dtype arithmetic on the
filterflow predicted state explains about `85.34%` of the observed delta, while
same-dtype BF64 state differences explain about `17.99%`.

This narrows the immediate problem from OT transport to dtype-sensitive
Gaussian observation log-probability arithmetic under an extreme observation
path, with a smaller upstream predicted-particle contribution still present.

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No DSGE/NAWM validation is concluded.
- No banking/model-risk claim is concluded.
- No monograph claim is concluded.
- No gradient correctness beyond this fixed 1D scalar fixture is concluded.
- No correctness claim is made for either implementation.
- No dtype policy change is concluded.
- No tolerance policy change is concluded.
