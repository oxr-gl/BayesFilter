# R1 Observation-Path Mismatch Hypothesis Result

## Decision

`r1_hypothesis_localization_completed`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `r1_hypothesis_localization_completed` | `same-harness control passed; R1 mismatch reproduced; first BF64 failure localized to prefix T=4, time 3, observation-likelihood ledger fields` | `no comparator drift; CPU-only manifests passed; no production/tests/docs-chapters changes; no runner NumPy import; path-boundary manifest clean` | `the first discrepancy is now localized but not algebraically explained; likely interaction is extreme filterflow observation scale with observation log-likelihood evaluation and finite precision` | `run a t=3 micro-ledger audit freezing pre-particles, transition noise, observation, and log weights, then compute observation log-prob in BF64/BF32/filterflow and by closed-form scalar arithmetic` | `correctness of either implementation, production readiness, dtype policy change, tolerance policy change, gradient correctness` |

## Hypothesis Statuses

| Hypothesis | Status | Key evidence |
| --- | --- | --- |
| `H1` | `weakened` | `{"bf32_implementation_agreement": false, "max_field_reduction_ratio": 0.9624485445208848, "scalar_reduction_ratio": 0.137826856225729}` |
| `H2` | `partially_supported` | `{"base_scalar_delta": 2.205229699611664, "field_set_intersections": {"r1_scale_0.01": ["observation_log_likelihoods"], "r1_scale_0.1": ["observation_log_likelihoods", "per_step_log_normalizer", "unnormalized_log_weights"], "r1_scale_1": ...` |
| `H3` | `supported` | `{"first_failing_field_set": ["observation_log_likelihoods", "per_step_log_normalizer", "post_update_log_weights", "unnormalized_log_weights"], "first_failing_prefix": 4, "first_failing_time": 3}` |
| `H4` | `weakened` | `{"column_residual_delta": 4.768371573149466e-07, "first_failure": {"field_set": ["observation_log_likelihoods", "per_step_log_normalizer", "post_update_log_weights", "unnormalized_log_weights"], "status": "failed", "time_index": 3, "trig...` |
| `H5` | `weakened` | `{"first_failure": {"field_set": ["observation_log_likelihoods", "per_step_log_normalizer", "post_update_log_weights", "unnormalized_log_weights"], "status": "failed", "time_index": 3, "triggered": true}}` |
| `H6` | `partially_supported` | `{"first_failure": {"field_set": ["observation_log_likelihoods", "per_step_log_normalizer", "post_update_log_weights", "unnormalized_log_weights"], "status": "failed", "time_index": 3, "triggered": true}, "residual_only_field_failure": fa...` |
| `H7` | `supported` | `{"control_observation_rms": 0.10016792396396304, "monotone_scale_deltas": true, "r1_observation_rms": 288.43812793508806, "rms_ratio": 2879.5458318459123, "scale_scalar_deltas": [2.205229699611664, 0.448161463951692, 0.002258484118101478]}` |
| `H8` | `audit_risk_not_found` | `{"missing_tokens": [], "required_tokens_present": true, "source": "run_filterflow_1d_lgssm_step_gradient_comparison_tf._filterflow_script", "source_digest": "83ac754d8d9524898333a083e1b2de8f8e902f04387674999d26ecf391cfc54d", "status": "a...` |

## Control And R1

| Case | BF64 agreement | BF32 agreement | BF64 scalar delta | BF32 scalar delta | BF64 first failure |
| --- | --- | --- | ---: | ---: | --- |
| `matched_control_generated_T100` | `True` | `True` | `6.720575720819966e-06` | `9.5367431640625e-07` | `t=None, fields=[]` |
| `r1_filterflow_observation_path_unscaled` | `False` | `False` | `2.205229699611664` | `16.0` | `t=3, fields=['observation_log_likelihoods', 'per_step_log_normalizer', 'post_update_log_weights', 'unnormalized_log_weights']` |

## First Prefix Failures

| Prefix | BF64 agreement | BF64 first failure | BF32 agreement |
| ---: | --- | --- | --- |
| `1` | `True` | `t=None, fields=[]` | `True` |
| `2` | `True` | `t=None, fields=[]` | `True` |
| `4` | `False` | `t=3, fields=['observation_log_likelihoods', 'per_step_log_normalizer', 'post_update_log_weights', 'unnormalized_log_weights']` | `False` |
| `8` | `False` | `t=3, fields=['observation_log_likelihoods', 'per_step_log_normalizer', 'post_update_log_weights', 'unnormalized_log_weights']` | `False` |
| `16` | `False` | `t=3, fields=['observation_log_likelihoods', 'per_step_log_normalizer', 'post_update_log_weights', 'unnormalized_log_weights']` | `False` |
| `32` | `False` | `t=3, fields=['observation_log_likelihoods', 'per_step_log_normalizer', 'post_update_log_weights', 'unnormalized_log_weights']` | `False` |
| `64` | `False` | `t=3, fields=['observation_log_likelihoods', 'per_step_log_normalizer', 'post_update_log_weights', 'unnormalized_log_weights']` | `False` |
| `100` | `False` | `t=3, fields=['observation_log_likelihoods', 'per_step_log_normalizer', 'post_update_log_weights', 'unnormalized_log_weights']` | `False` |

## Scale Diagnostics

| Scale case | BF64 scalar delta | BF64 first failure | BF32 scalar delta |
| --- | ---: | --- | ---: |
| `r1_scale_1` | `2.205229699611664` | `t=3, fields=['observation_log_likelihoods', 'per_step_log_normalizer', 'post_update_log_weights', 'unnormalized_log_weights']` | `16.0` |
| `r1_scale_0.1` | `0.448161463951692` | `t=10, fields=['observation_log_likelihoods', 'per_step_log_normalizer', 'unnormalized_log_weights']` | `0.375` |
| `r1_scale_0.01` | `0.002258484118101478` | `t=43, fields=['observation_log_likelihoods']` | `0.0009765625` |

## Observation Summaries

```json
{
  "matched_control_generated_T100": {
    "count": 100.0,
    "max": 0.27831194370410534,
    "mean": -1.629568699185381e-05,
    "min": -0.23629403538865712,
    "rms": 0.10016792396396304
  },
  "r1_filterflow_observation_path": {
    "count": 100.0,
    "max": 594.5238037109375,
    "mean": 243.02800384521484,
    "min": -1.0573327541351318,
    "rms": 288.43812793508806
  }
}
```

## Verification

| Command | Result |
| --- | --- |
| `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_observation_path_mismatch_localization_tf.py` | passed |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_r1_observation_path_mismatch_localization_tf` | passed; decision `r1_hypothesis_localization_completed` |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_r1_observation_path_mismatch_localization_tf --validate-only` | passed |
| `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_r1_observation_path_mismatch_localization_2026-06-02.json` | passed |
| `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_observation_path_mismatch_localization_tf.py` | no hits; NumPy not used in the new BayesFilter runner |
| `rg -n "student|vendored|highdim|DSGE|NAWM|docs/chapters|bayesfilter/" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_observation_path_mismatch_localization_tf.py` | no hits in runner |
| broader boundary search over plan/result/runner | hits only governance/caveat text in plan/result; no forbidden implementation import/use |
| lane-scoped trailing whitespace check | passed; `[]` |
| `git diff --check` | passed |
| `git status --short -- bayesfilter tests docs/chapters` | passed; no output |
| `git status --short --branch` | ran; branch `main...origin/main [behind 2]`; many unrelated pre-existing dirty/untracked artifacts remain |

## Run Manifest

| Field | Value |
| --- | --- |
| command | `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_r1_observation_path_mismatch_localization_tf` |
| CPU-only | `true`; `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import |
| GPU visibility | parent and filterflow manifests report `[]` visible GPU devices |
| git commit | recorded in JSON run manifest |
| comparator drift | `false` |
| output JSON | `experiments/dpf_implementation/reports/outputs/dpf_filterflow_r1_observation_path_mismatch_localization_2026-06-02.json` |
| report | `experiments/dpf_implementation/reports/dpf-filterflow-r1-observation-path-mismatch-localization-2026-06-02.md` |

## Unresolved Risks

- The result localizes the first BF64 disagreement to observation-likelihood-related fields at time 3, but does not yet prove the exact arithmetic cause.
- H2/H7 indicate scale stress: R1 observation RMS is about `2879.5x` the matched-control RMS, but scaled-path diagnostics remain explanatory for mechanism, not correctness.
- H6 is only partially supported: relative scalar delta is small, but the first failing field set is not residual-only.
- BF32 does not rescue the mismatch; H1 is weakened, not eliminated as a possible contributor in other settings.

## Blockers

No technical blocker remained for this bounded hypothesis localization. The result-review blocker from Claude round 1 was process/governance only and is addressed by this expanded artifact plus the review-loop entry.

## Post-Run Red-Team Note

Strongest alternative explanation: the scalar 1D fixture is an intentionally awkward projection of a 2D filterflow observation path, so the first discrepancy may be a stress-amplified numeric artifact rather than a meaningful algorithmic mismatch.

What would overturn the current interpretation: a frozen time-3 micro-ledger showing that BayesFilter and filterflow already disagree before observation log-prob evaluation, or that the wrapper feeds different particles/log weights than recorded.

Weakest part of the evidence: the per-time ledger identifies the first failing field set, but does not yet include a closed-form recomputation of the exact time-3 observation log-likelihood entries.

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
- No dtype default-policy change is concluded.
- No tolerance policy change is concluded.
