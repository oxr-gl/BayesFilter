# BF/FilterFlow Seeded-Ancestor Robustness Diagnostic

metadata_date: 2026-06-07
decision: PASS_SEEDED_ANCESTOR_DIAGNOSTIC

## Question

Do BayesFilter and executable local FilterFlow-side adapters remain aligned when several seeded pseudo-stochastic ancestor schedules are frozen and replayed under the V2 fixed-ancestor contract?

## Evidence Contract

Primary status: diagnostic-only branch robustness.  The schedule is seeded, frozen, and replayed on both sides.  This is not RNG equality and not stochastic-resampling distribution correctness.

## Result

- JSON artifact: `experiments/dpf_implementation/reports/outputs/dpf_bf_filterflow_seeded_ancestor_robustness_2026-06-07.json`
- Reproducibility digest: `8663b8a99c66c6a52b3b70ef5bb68563399a8612e7d15cba4901aea8eda5330d`

## Summary

- status counts: `{'MATCHED': 18}`
- max abs delta: `0.0`
- seeds: `[1101, 2202, 3303]`

## Cells

| Seed | Model | Status | Max abs delta |
|---:|---|---|---:|
| `1101` | `lgssm_2d_h25_rich` | `MATCHED` | `0.0` |
| `1101` | `sv_1d_h18_rich` | `MATCHED` | `0.0` |
| `1101` | `range_bearing_4d_h20_rich` | `MATCHED` | `0.0` |
| `1101` | `structural_ar1_quadratic_h16` | `MATCHED` | `0.0` |
| `1101` | `spatial_sir_j3_rk4` | `MATCHED` | `0.0` |
| `1101` | `predator_prey_rk4` | `MATCHED` | `0.0` |
| `2202` | `lgssm_2d_h25_rich` | `MATCHED` | `0.0` |
| `2202` | `sv_1d_h18_rich` | `MATCHED` | `0.0` |
| `2202` | `range_bearing_4d_h20_rich` | `MATCHED` | `0.0` |
| `2202` | `structural_ar1_quadratic_h16` | `MATCHED` | `0.0` |
| `2202` | `spatial_sir_j3_rk4` | `MATCHED` | `0.0` |
| `2202` | `predator_prey_rk4` | `MATCHED` | `0.0` |
| `3303` | `lgssm_2d_h25_rich` | `MATCHED` | `0.0` |
| `3303` | `sv_1d_h18_rich` | `MATCHED` | `0.0` |
| `3303` | `range_bearing_4d_h20_rich` | `MATCHED` | `0.0` |
| `3303` | `structural_ar1_quadratic_h16` | `MATCHED` | `0.0` |
| `3303` | `spatial_sir_j3_rk4` | `MATCHED` | `0.0` |
| `3303` | `predator_prey_rk4` | `MATCHED` | `0.0` |

## Veto Diagnostics

- student_command_executed: `False`
- localsource_filterflow_mutated: `False`
- stochastic_distribution_claimed: `False`
- rng_equality_claimed: `False`
- finite_difference_used_as_gate: `False`
- missing_filterflow_subprocess_environment: `False`
- nonfinite_path_value: `False`
- unclassified_mismatch: `False`

## Command Manifest

| Field | Value |
|---|---|
| git commit | `7ccb9c39883471c2d5ec2891cbf33b9ed436bada` |
| command | `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_bf_filterflow_seeded_ancestor_robustness_tf` |
| CPU/GPU status | CPU-only TensorFlow; pre-import `CUDA_VISIBLE_DEVICES=-1`; visible GPUs `[]` |
| random seeds | `[1101, 2202, 3303]`; used only to generate frozen ancestor schedules |
| dtype | `tf.float64` |

## Non-Claims

- no stochastic resampling distribution correctness claim
- no random-number-generator equality claim
- no differentiable-resampling or gradient-through-ancestor-selection claim
- no filtering-algorithm correctness proof
- no student-repository tie-out claim
