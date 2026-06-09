# P6 Result: Cross-Filter Error Calibration

metadata_date: 2026-06-08
phase: P6
status: PASS_P6_CROSS_FILTER_CALIBRATION_PENDING_CLAUDE_REVIEW

## Skeptical Plan Audit

Status: `PASS_FOR_ARTIFACT_CALIBRATION_ONLY`.

Every row records its target and exact or approximation reference route.

DPF P5 rows remain diagnostic/blocked and are excluded from valid calibration tables.

Exact-target and approximation-target tables are separate; no global route ranking is emitted.

## Decision Table

| Field | Status |
| --- | --- |
| decision | calibration tables are claim-class separated; no global ranking emitted |
| exact-target rows | `12` |
| approximation-target rows | `3` |
| DPF diagnostic rows | `8`; not valid calibration rows |
| blocked rows | `23` |
| primary uncertainty | DPF promotion bands and nonlinear same-target adapters remain missing; P3 exact-transformed and P44-M3/M4 metrics need structured reference-uncertainty JSON before calibration |
| not concluded | global filter ranking, default-policy change, HMC readiness, production readiness, GPU readiness |

## Exact-Target Calibration Rows

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

## Approximation-Target Calibration Rows

| target | dim | route | claim | abs value err | rel score err | reference |
| --- | ---: | --- | --- | ---: | ---: | --- |
| `sv_ksc_transformed_mixture_panel` | 1 | `cut4` | `CERTIFIED_APPROXIMATION` | 0 | 1.66046e-16 | `kalman_exact` |
| `sv_ksc_transformed_mixture_panel` | 2 | `cut4` | `CERTIFIED_APPROXIMATION` | 0 | 1.21544e-15 | `kalman_exact` |
| `sv_ksc_transformed_mixture_panel` | 3 | `cut4` | `CERTIFIED_APPROXIMATION` | 5.32907e-15 | 1.29019e-15 | `kalman_exact` |

## DPF Diagnostic Rows

| target | method | decision | value RMSE/blocked | value SE | grad-norm SE | mean relative score err |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `lgssm_2d_h25_rich` | `dpf_bootstrap_ot` | `DOWNGRADED_TO_DIAGNOSTIC_ONLY` | `0.8339700259704327` | `0.1445548048132311` | `0.561820578906778` | `0.4565046565890657` |
| `lgssm_2d_h25_rich` | `dpf_ledh_pfpf_ot` | `DOWNGRADED_TO_DIAGNOSTIC_ONLY` | `0.3114821802004455` | `0.15023326462722864` | `0.4424529115282028` | `0.1724329499486878` |
| `p44_m2_cubic_additive_gaussian_panel` | `dpf_bootstrap_ot` | `BLOCKED` | `N/A` | `None` | `None` | `N/A` |
| `p44_m2_cubic_additive_gaussian_panel` | `dpf_ledh_pfpf_ot` | `BLOCKED` | `N/A` | `None` | `None` | `N/A` |
| `p44_m3_quadratic_observation_panel` | `dpf_bootstrap_ot` | `BLOCKED` | `N/A` | `None` | `None` | `N/A` |
| `p44_m3_quadratic_observation_panel` | `dpf_ledh_pfpf_ot` | `BLOCKED` | `N/A` | `None` | `None` | `N/A` |
| `p44_m4_nonlinear_transition_h2_panel` | `dpf_bootstrap_ot` | `BLOCKED` | `N/A` | `None` | `None` | `N/A` |
| `p44_m4_nonlinear_transition_h2_panel` | `dpf_ledh_pfpf_ot` | `BLOCKED` | `N/A` | `None` | `None` | `N/A` |

## Blocked Or Unstructured

- Blocked row count: `23`.
- Unstructured metric row count: `5`.
- Blocked/unstructured rows are not assigned value or score gaps in P6.

## Artifacts

- JSON: `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_cross_filter_error_calibration_2026-06-08.json`
- Report: `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-2026-06-08.md`
- Result: `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-result-2026-06-08.md`

## Run Manifest

```json
{
  "branch": "main",
  "command": "/home/chakwong/anaconda3/envs/tf-gpu/bin/python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf",
  "commit": "137f6ba5a03ebab199c8ab4699354d50bd560123",
  "cpu_gpu_status": "pure_python_artifact_calibration_only; TensorFlow not imported",
  "data_version": "P1-P5 local artifacts; no new observations generated",
  "dirty_state_digest": "f1e107f0d48950c3ae03f8d3e8cb463aae0718c6642c6b240b01e9cc84c65cae",
  "dirty_state_line_count": 1432,
  "json_path": "experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_cross_filter_error_calibration_2026-06-08.json",
  "particle_counts": "reused only in DPF diagnostic rows from P1/P5",
  "plan_path": "docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-subplan-2026-06-08.md",
  "python_version": "3.11.14",
  "report_path": "experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-2026-06-08.md",
  "result_path": "docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-result-2026-06-08.md",
  "review_ledger_path": "docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-claude-review-ledger-2026-06-08.md",
  "scoped_dirty_state_summary": "?? docs/plans/bayesfilter-dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-result-2026-06-08.md\n?? docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md\n?? docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-gated-execution-runbook-2026-06-08.md\n?? experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p6-cross-filter-error-calibration-2026-06-08.md\n?? experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_cross_filter_error_calibration_2026-06-08.json\n?? experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p6_cross_filter_error_calibration_tf.py",
  "seeds": "reused only in DPF diagnostic rows from P1/P5",
  "tensorflow_imported": false,
  "tensorflow_probability_imported": false,
  "timestamp_utc": "2026-06-08T20:00:45Z",
  "wall_time_seconds": 0.012831258121877909
}
```

## Nonclaims

- no global filter ranking across incompatible targets
- no DPF correctness or stochastic-score correctness claim
- no approximation route exactness claim
- no data-law variability tolerance used to excuse bias
- no default-policy change
- no HMC readiness, production readiness, GPU readiness, or paper-scale claim
