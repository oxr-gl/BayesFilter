# P6 Result: Algorithm 1 UKF Cross-Filter Calibration Replacement

metadata_date: 2026-06-10
phase: P6
status: LOCAL_PASS_P6_ALG1_UKF_CROSS_FILTER_CALIBRATION_DIAGNOSTIC_ONLY_PENDING_CLAUDE_REVIEW

## Skeptical Plan Audit

Status: `PASS_FOR_ARTIFACT_CALIBRATION_ONLY`.

Deterministic rows retain their own target/reference class; Algorithm 1 DPF rows use P5 replacement evidence only.

Algorithm 1 finite rows remain diagnostic-only because P5 declared no numeric promotion band.

Exact-target, approximation-target, and Algorithm 1 DPF rows are separate ledgers.  No global ranking is emitted.

## Decision Table

| Field | Status |
| --- | --- |
| decision | claim-class separated calibration ledger; no global ranking emitted |
| exact-target deterministic rows | `12` |
| approximation-target deterministic rows | `3` |
| Algorithm 1 DPF rows | `4`; diagnostic `['lgssm_2d_h25_rich']`; blocked `['p44_m2_cubic_additive_gaussian_panel', 'p44_m3_quadratic_observation_panel', 'p44_m4_nonlinear_transition_h2_panel']` |
| blocked rows | `20` |
| primary uncertainty | Algorithm 1 P5 promotion bands and nonlinear same-target adapters remain missing; P3 exact-transformed and P44-M3/M4 deterministic metrics need structured reference-uncertainty JSON before calibration |
| not concluded | global filter ranking, default-policy change, HMC readiness, production readiness, GPU readiness |

## Exact-Target Deterministic Calibration Rows

| target | dim | route | claim | abs value err | rel score err | ref uncertainty |
| --- | ---: | --- | --- | ---: | ---: | --- |
| `p44_m2_cubic_additive_gaussian_panel` | 1 | `ukf` | `DIAGNOSTIC_ONLY` | 0.00602149 | 0.0858287 | `dense_refinement_recorded` |
| `p44_m2_cubic_additive_gaussian_panel` | 1 | `svd_sigma_point` | `DIAGNOSTIC_ONLY` | 0.0060215 | 0.0858288 | `dense_refinement_recorded` |
| `p44_m2_cubic_additive_gaussian_panel` | 1 | `cut4` | `CERTIFIED_APPROXIMATION` | 0.00592047 | 0.0851923 | `dense_refinement_recorded` |
| `p44_m2_cubic_additive_gaussian_panel` | 1 | `zhao_cui_fixed_design_tt` | `CERTIFIED_APPROXIMATION` | 0.000193191 | 0.00111501 | `dense_refinement_recorded` |
| `p44_m2_cubic_additive_gaussian_panel` | 2 | `ukf` | `DIAGNOSTIC_ONLY` | 0.00709291 | 0.106946 | `dense_refinement_recorded` |
| `p44_m2_cubic_additive_gaussian_panel` | 2 | `svd_sigma_point` | `DIAGNOSTIC_ONLY` | 0.00709292 | 0.106946 | `dense_refinement_recorded` |
| `p44_m2_cubic_additive_gaussian_panel` | 2 | `cut4` | `CERTIFIED_APPROXIMATION` | 0.0107055 | 0.104193 | `dense_refinement_recorded` |
| `p44_m2_cubic_additive_gaussian_panel` | 2 | `zhao_cui_fixed_design_tt` | `CERTIFIED_APPROXIMATION` | 0.000222426 | 0.00093957 | `dense_refinement_recorded` |
| `p44_m2_cubic_additive_gaussian_panel` | 3 | `ukf` | `DIAGNOSTIC_ONLY` | 0.0135437 | 0.112748 | `dense_refinement_recorded` |
| `p44_m2_cubic_additive_gaussian_panel` | 3 | `svd_sigma_point` | `DIAGNOSTIC_ONLY` | 0.0135437 | 0.112748 | `dense_refinement_recorded` |
| `p44_m2_cubic_additive_gaussian_panel` | 3 | `cut4` | `CERTIFIED_APPROXIMATION` | 0.0098753 | 0.0981453 | `dense_refinement_recorded` |
| `p44_m2_cubic_additive_gaussian_panel` | 3 | `zhao_cui_fixed_design_tt` | `CERTIFIED_APPROXIMATION` | 0.00034963 | 0.000999185 | `dense_refinement_recorded` |

## Approximation-Target Deterministic Calibration Rows

| target | dim | route | claim | abs value err | rel score err | reference |
| --- | ---: | --- | --- | ---: | ---: | --- |
| `sv_ksc_transformed_mixture_panel` | 1 | `cut4` | `CERTIFIED_APPROXIMATION` | 0 | 1.66046e-16 | `kalman_exact` |
| `sv_ksc_transformed_mixture_panel` | 2 | `cut4` | `CERTIFIED_APPROXIMATION` | 0 | 1.21544e-15 | `kalman_exact` |
| `sv_ksc_transformed_mixture_panel` | 3 | `cut4` | `CERTIFIED_APPROXIMATION` | 5.32907e-15 | 1.29019e-15 | `kalman_exact` |

## Algorithm 1 DPF Rows

| target | method | status | value RMSE/blocked | norm value RMSE | value SE | grad error/blocked | norm grad error | grad error SE |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `lgssm_2d_h25_rich` | `ledh_pfpf_alg1_ukf_no_resampling_tf` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `0.41825736258132357` | `0.16454394715425597` | `0.20582366822077328` | `1.065789869289693` | `1.065789869289693` | `0.9318296506783853` |
| `p44_m2_cubic_additive_gaussian_panel` | `ledh_pfpf_alg1_ukf_no_resampling_tf` | `BLOCKED_REQUIRES_ADAPTER` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` |
| `p44_m3_quadratic_observation_panel` | `ledh_pfpf_alg1_ukf_no_resampling_tf` | `BLOCKED_REQUIRES_ADAPTER` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` |
| `p44_m4_nonlinear_transition_h2_panel` | `ledh_pfpf_alg1_ukf_no_resampling_tf` | `BLOCKED_REQUIRES_ADAPTER` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` |

## Historical Old DPF Quarantine

- `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p5_dpf_statistical_closeness_2026-06-08.json`: HISTORICAL_ONLY_NOT_CURRENT_ALGORITHM1_EVIDENCE
- `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_cross_filter_error_calibration_2026-06-08.json`: HISTORICAL_ONLY_NOT_CURRENT_ALGORITHM1_EVIDENCE
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`: QUARANTINED_OLD_IMPLEMENTATION_NOT_IMPORTED

## Veto Diagnostics

| Diagnostic | Status |
| --- | --- |
| `global_ranking_emitted` | `False` |
| `data_law_variability_used_to_excuse_mismatch` | `False` |
| `old_ledh_pfpf_ot_used_as_current_evidence` | `False` |
| `old_dpf_metric_consumed_as_current_algorithm1` | `False` |
| `algorithm1_route_fields_missing` | `False` |
| `algorithm1_diagnostic_uncertainty_missing` | `False` |
| `algorithm1_row_promoted` | `False` |
| `p44_algorithm1_metric_fabricated` | `False` |
| `approximation_route_ranked_as_exact` | `False` |
| `reference_uncertainty_omitted_from_p2_dense_rows` | `False` |
| `exact_target_row_lacks_accepted_reference_uncertainty` | `False` |
| `blocked_row_has_metric` | `False` |
| `nonfinite_calibration_row` | `False` |
| `value_used_to_promote_gradient` | `False` |
| `zhao_cui_used_as_dpf_correctness_oracle` | `False` |

## Blocked Or Unstructured

- Blocked row count: `20`.
- Unstructured metric row count: `5`.
- Blocked/unstructured rows are not assigned value or score gaps in P6.

## Artifacts

- JSON: `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_alg1_ukf_cross_filter_calibration_2026-06-10.json`
- Report: `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p6-alg1-ukf-cross-filter-calibration-2026-06-10.md`
- Result: `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p6-cross-filter-calibration-result-2026-06-10.md`

## Run Manifest

```json
{
  "branch": "main",
  "command": "/home/chakwong/anaconda3/envs/tf-gpu/bin/python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p6_alg1_ukf_cross_filter_calibration_tf",
  "commit": "26485010c28e11b3591da59b7ca375d4764c3d8d",
  "cpu_gpu_status": "pure_python_artifact_calibration_only; TensorFlow not imported",
  "data_version": "historical deterministic filter-oracle artifacts plus P5/P3/P4 Algorithm 1 replacement artifacts",
  "dirty_state_digest": "db61743ccd53ba52c4ef823b485ce4709c7c36ec60d622cd03634f051ea13a8b",
  "dirty_state_line_count": 1572,
  "json_path": "experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_alg1_ukf_cross_filter_calibration_2026-06-10.json",
  "particle_counts": "consumed from P5/P3/P4 Algorithm 1 rows only",
  "plan_path": "docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p6-cross-filter-calibration-subplan-2026-06-10.md",
  "python_version": "3.11.14",
  "report_path": "experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p6-alg1-ukf-cross-filter-calibration-2026-06-10.md",
  "result_path": "docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p6-cross-filter-calibration-result-2026-06-10.md",
  "review_ledger_path": "docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-claude-review-ledger-2026-06-10.md",
  "scoped_dirty_state_summary": "?? docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-visible-execution-ledger-2026-06-10.md\n?? experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p6_alg1_ukf_cross_filter_calibration_tf.py",
  "seeds": "consumed from P5/P3/P4 Algorithm 1 rows only",
  "tensorflow_imported": false,
  "tensorflow_probability_imported": false,
  "timestamp_utc": "2026-06-10T11:07:36Z",
  "wall_time_seconds": 0.01642774697393179
}
```

## Nonclaims

- P6 does not certify Algorithm 1 statistical closeness.
- P6 does not revive old dpf_ledh_pfpf_ot or dpf_bootstrap_ot rows as current evidence.
- P6 does not rank filters globally across incompatible targets.
- P6 does not use Zhao-Cui, CUT4, SVD, UKF, or FilterFlow as a DPF correctness oracle.
- P6 does not establish nonlinear P44 Algorithm 1 DPF value or gradient closeness.
- P6 does not establish stochastic-resampling gradient correctness.
- P6 does not establish HMC readiness, production readiness, GPU readiness, or paper-scale claims.
