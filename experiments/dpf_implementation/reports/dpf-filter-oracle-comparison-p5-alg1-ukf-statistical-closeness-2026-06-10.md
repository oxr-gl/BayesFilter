# P5 Result: Filter-Oracle Algorithm 1 UKF Statistical Closeness Replacement

metadata_date: 2026-06-10
phase: P5
status: LOCAL_PASS_P5_FILTER_ORACLE_ALG1_UKF_STATISTICAL_CLOSENESS_DIAGNOSTIC_ONLY_PENDING_CLAUDE_REVIEW

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the filter-oracle P5 rows that previously contained dpf_ledh_pfpf_ot be replaced by Algorithm 1 UKF evidence or reviewed target-route blockers? |
| Baseline/comparator | P0/P4 filter-oracle target registry for old eligible target set; P2-P4 Algorithm 1 UKF artifacts for current evidence. |
| Primary criterion | Each old dpf_ledh_pfpf_ot P5-eligible target has a replacement status.  Algorithm 1 rows include mandatory route fields and Monte Carlo uncertainty; rows without same-target adapters are blocked with concrete adapter items. |
| Promotion policy | No P5 row is promoted because value and gradient tolerances remain N/A diagnostic-only or adapter-blocked. |

## Rows

| Target | Method | Status | Reference | Main reason |
| --- | --- | --- | --- | --- |
| `lgssm_2d_h25_rich` | `ledh_pfpf_alg1_ukf_no_resampling_tf` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `exact_kalman_for_lgssm` | P2/P5 numeric promotion bands are N/A diagnostic-only; P4 gradient seed count is diagnostic-only and below the old P5 minimum seed-count expectation; finite Algorithm 1 execution is not a statistical-closeness promotion criterion |
| `p44_m2_cubic_additive_gaussian_panel` | `ledh_pfpf_alg1_ukf_no_resampling_tf` | `BLOCKED_REQUIRES_ADAPTER` | `dense_refined_quadrature` | reviewed same-target Algorithm 1 transition_sample/transition_log_density callbacks missing for this P44 target |
| `p44_m3_quadratic_observation_panel` | `ledh_pfpf_alg1_ukf_no_resampling_tf` | `BLOCKED_REQUIRES_ADAPTER` | `dense_refined_quadrature` | reviewed same-target Algorithm 1 transition_sample/transition_log_density callbacks missing for this P44 target |
| `p44_m4_nonlinear_transition_h2_panel` | `ledh_pfpf_alg1_ukf_no_resampling_tf` | `BLOCKED_REQUIRES_ADAPTER` | `dense_refined_quadrature` | reviewed same-target Algorithm 1 transition_sample/transition_log_density callbacks missing for this P44 target |

## Summary

- Eligible targets: `['lgssm_2d_h25_rich', 'p44_m2_cubic_additive_gaussian_panel', 'p44_m3_quadratic_observation_panel', 'p44_m4_nonlinear_transition_h2_panel']`.
- Diagnostic rows: `['lgssm_2d_h25_rich']`.
- Blocked rows: `['p44_m2_cubic_additive_gaussian_panel', 'p44_m3_quadratic_observation_panel', 'p44_m4_nonlinear_transition_h2_panel']`.
- Promoted rows: `[]`.

## LGSSM Diagnostic Statistics

| Particle | Value seeds | Value SE | Value RMSE | Gradient seeds | Mean grad error norm | Grad error SE |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 32 | 5 | 0.20582366822077328 | 0.41825736258132357 | 3 | 1.065789869289693 | 0.9318296506783853 |

## Veto Diagnostics

| Diagnostic | Status |
| --- | --- |
| `eligible_target_set_mismatch` | `False` |
| `row_count_or_order_mismatch` | `False` |
| `p2_contract_not_ready` | `False` |
| `p3_values_not_ready` | `False` |
| `p4_gradients_not_ready` | `False` |
| `old_ledh_pfpf_ot_used_as_current_method` | `False` |
| `algorithm1_route_fields_missing` | `False` |
| `p44_row_promoted_without_same_target_adapter` | `False` |
| `finite_only_promoted` | `False` |
| `missing_monte_carlo_uncertainty_on_diagnostic_lgssm` | `False` |
| `threshold_or_band_missing_without_na_reason` | `False` |
| `unsupported_comparator_promoted` | `False` |
| `value_used_to_promote_gradient` | `False` |
| `stochastic_score_claimed` | `False` |
| `zhao_cui_used_as_p5_comparator` | `False` |
| `registry_missing_expected_target` | `False` |

## Gate Definition

- Local decision semantics: LOCAL_PASS means the artifact satisfies local classification completeness and anti-revival checks before Claude review.  It does not certify statistical closeness.
- P44 block rule: P44 targets remain BLOCKED_REQUIRES_ADAPTER unless a reviewed same-target Algorithm 1 adapter and numeric P5 band exist before execution.
- Promotion rule: finite execution is diagnostic-only without numeric predeclared bands

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `LOCAL_PASS_P5_FILTER_ORACLE_ALG1_UKF_STATISTICAL_CLOSENESS_DIAGNOSTIC_ONLY_PENDING_CLAUDE_REVIEW` | every old P5 dpf_ledh_pfpf_ot eligible target is classified; LGSSM is diagnostic; P44 rows are adapter-blocked | `{'eligible_target_set_mismatch': False, 'row_count_or_order_mismatch': False, 'p2_contract_not_ready': False, 'p3_values_not_ready': False, 'p4_gradients_not_ready': False, 'old_ledh_pfpf_ot_used_as_current_method': False, 'algorithm1_route_fields_missing': False, 'p44_row_promoted_without_same_target_adapter': False, 'finite_only_promoted': False, 'missing_monte_carlo_uncertainty_on_diagnostic_lgssm': False, 'threshold_or_band_missing_without_na_reason': False, 'unsupported_comparator_promoted': False, 'value_used_to_promote_gradient': False, 'stochastic_score_claimed': False, 'zhao_cui_used_as_p5_comparator': False, 'registry_missing_expected_target': False}` | no numeric P5 promotion bands and no P44 same-target Algorithm 1 adapters | Claude P5 review, then P6 calibration classification | no statistical-closeness certification, stochastic-score correctness, HMC, production, or GPU claim |

## Artifacts

- JSON: `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p5_alg1_ukf_statistical_closeness_2026-06-10.json`
- Report: `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p5-alg1-ukf-statistical-closeness-2026-06-10.md`
- Result: `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p5-filter-oracle-statistical-closeness-result-2026-06-10.md`

## Run Manifest

```json
{
  "branch": "main",
  "command": "/home/chakwong/anaconda3/envs/tf-gpu/bin/python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p5_alg1_ukf_statistical_closeness_tf",
  "commit": "26485010c28e11b3591da59b7ca375d4764c3d8d",
  "cpu_gpu_status": "pure_python_classification_only; TensorFlow not imported",
  "data_version": "P2-P4 Algorithm 1 artifacts plus historical filter-oracle target registry",
  "dirty_state_digest": "fc8438e21c987ffa432275f320f122d484b1b7dd8c1da9b0cb042d4e1d468a70",
  "dirty_state_line_count": 1568,
  "json_path": "experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p5_alg1_ukf_statistical_closeness_2026-06-10.json",
  "particle_counts": "consumed from P3/P4 only",
  "plan_path": "docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p5-filter-oracle-statistical-closeness-subplan-2026-06-10.md",
  "python_version": "3.11.14",
  "report_path": "experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p5-alg1-ukf-statistical-closeness-2026-06-10.md",
  "result_path": "docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p5-filter-oracle-statistical-closeness-result-2026-06-10.md",
  "review_ledger_path": "docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-claude-review-ledger-2026-06-10.md",
  "seed_list": "consumed from P3/P4 only",
  "tensorflow_imported": false,
  "tensorflow_probability_imported": false,
  "timestamp_utc": "2026-06-10T10:54:18Z",
  "wall_time_seconds": 0.0139245823957026
}
```

## Nonclaims

- P5 does not certify Algorithm 1 statistical closeness.
- P5 does not revive old dpf_ledh_pfpf_ot results as evidence.
- P5 does not establish nonlinear P44 DPF value or gradient closeness.
- P5 does not use Zhao-Cui, CUT4, SVD, UKF, or FilterFlow as a DPF correctness oracle.
- P5 does not establish stochastic-resampling gradient correctness.
- P5 does not establish HMC readiness, production readiness, GPU readiness, or paper-scale claims.
