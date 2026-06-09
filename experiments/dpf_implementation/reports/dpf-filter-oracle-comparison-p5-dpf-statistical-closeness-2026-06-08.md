# P5 Result: DPF Statistical Closeness

metadata_date: 2026-06-08
phase: P5
status: PASS_P5_DPF_STATISTICAL_CLOSENESS_PENDING_CLAUDE_REVIEW

## Skeptical Plan Audit

Status: `PASS_FOR_CLASSIFICATION_ONLY_EXECUTION`.

P5 consumes P0/P4 reference-route decisions and P1 Kalman evidence; it does not compare against BayesFilter-owned FilterFlow adapters or Zhao-Cui approximations.

Placeholder P0 DPF bands, missing directional residuals, and aggregate-only branch decisions prevent promotion; finite values or BF/FilterFlow agreement cannot substitute.

LGSSM exact-target evidence and P44 dense-reference rows are kept separate; P44 rows are blocked until reviewed same-target DPF adapters and evaluator variance exist.

## Decision Table

| Field | Status |
| --- | --- |
| decision | no DPF row promoted |
| primary criterion | all `8` eligible target-route rows classified |
| veto diagnostics | clear at phase level; row-level blockers/downgrades recorded |
| main uncertainty | numeric P5 DPF bands and reviewed nonlinear same-target adapters are still missing |
| next justified action | P6 may calibrate cross-filter error; a later amendment is needed before DPF nonlinear promotion runs |
| not concluded | DPF correctness, stochastic-score correctness, HMC readiness, production readiness, GPU readiness |

## Row Summary

- Eligible targets: `['lgssm_2d_h25_rich', 'p44_m2_cubic_additive_gaussian_panel', 'p44_m3_quadratic_observation_panel', 'p44_m4_nonlinear_transition_h2_panel']`.
- Promoted rows: `[]`.
- Downgraded/diagnostic rows: `['lgssm_2d_h25_rich/dpf_bootstrap_ot', 'lgssm_2d_h25_rich/dpf_ledh_pfpf_ot']`.
- Blocked rows: `['p44_m2_cubic_additive_gaussian_panel/dpf_bootstrap_ot', 'p44_m2_cubic_additive_gaussian_panel/dpf_ledh_pfpf_ot', 'p44_m3_quadratic_observation_panel/dpf_bootstrap_ot', 'p44_m3_quadratic_observation_panel/dpf_ledh_pfpf_ot', 'p44_m4_nonlinear_transition_h2_panel/dpf_bootstrap_ot', 'p44_m4_nonlinear_transition_h2_panel/dpf_ledh_pfpf_ot']`.

## Exact Reference Rows

| target | reference | DPF decision |
| --- | --- | --- |
| `lgssm_2d_h25_rich` | `kalman_exact` | dpf_bootstrap_ot=DOWNGRADED_TO_DIAGNOSTIC_ONLY, dpf_ledh_pfpf_ot=DOWNGRADED_TO_DIAGNOSTIC_ONLY |
| `p44_m2_cubic_additive_gaussian_panel` | `dense_refined_quadrature` | dpf_bootstrap_ot=BLOCKED, dpf_ledh_pfpf_ot=BLOCKED |
| `p44_m3_quadratic_observation_panel` | `dense_refined_quadrature` | dpf_bootstrap_ot=BLOCKED, dpf_ledh_pfpf_ot=BLOCKED |
| `p44_m4_nonlinear_transition_h2_panel` | `dense_refined_quadrature` | dpf_bootstrap_ot=BLOCKED, dpf_ledh_pfpf_ot=BLOCKED |

## LGSSM DPF Diagnostics

| method | N | mean value err | value CI95 | score RMSE | mean relative score err | decision |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| `dpf_bootstrap_ot` | 128 | 0.782254 | `[0.4989267853919508, 1.0655816202598167]` | 3.31184 | 0.456505 | `DOWNGRADED_TO_DIAGNOSTIC_ONLY` |
| `dpf_ledh_pfpf_ot` | 128 | 0.0821037 | `[-0.21235352408532082, 0.3765608732534155]` | 1.47236 | 0.172433 | `DOWNGRADED_TO_DIAGNOSTIC_ONLY` |

## Blocked Nonlinear DPF Rows

| target | method | primary blocker |
| --- | --- | --- |
| `p44_m2_cubic_additive_gaussian_panel` | `dpf_bootstrap_ot` | p0_dpf_promotion_tolerance_is_placeholder_not_numeric |
| `p44_m2_cubic_additive_gaussian_panel` | `dpf_ledh_pfpf_ot` | p0_dpf_promotion_tolerance_is_placeholder_not_numeric |
| `p44_m3_quadratic_observation_panel` | `dpf_bootstrap_ot` | p0_dpf_promotion_tolerance_is_placeholder_not_numeric |
| `p44_m3_quadratic_observation_panel` | `dpf_ledh_pfpf_ot` | p0_dpf_promotion_tolerance_is_placeholder_not_numeric |
| `p44_m4_nonlinear_transition_h2_panel` | `dpf_bootstrap_ot` | p0_dpf_promotion_tolerance_is_placeholder_not_numeric |
| `p44_m4_nonlinear_transition_h2_panel` | `dpf_ledh_pfpf_ot` | p0_dpf_promotion_tolerance_is_placeholder_not_numeric |

## Evidence Interpretation

- LGSSM bootstrap-OT and LEDH-PFPF-OT have finite paired multi-seed P1 evidence, but they remain diagnostic in P5.
- P44-M2/M3/M4 references are available, but DPF statistical closeness is blocked until same-target adapters, evaluator variance, branch decisions, and numeric P5 bands are reviewed.
- Zhao-Cui, CUT4, SVD, and UKF rows are not used as P5 DPF comparators.

## Artifacts

- JSON: `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p5_dpf_statistical_closeness_2026-06-08.json`
- Report: `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-2026-06-08.md`
- Result: `docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-result-2026-06-08.md`

## Run Manifest

```json
{
  "branch": "main",
  "command": "/home/chakwong/anaconda3/envs/tf-gpu/bin/python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf",
  "commit": "137f6ba5a03ebab199c8ab4699354d50bd560123",
  "cpu_gpu_status": "pure_python_classification_only; TensorFlow not imported",
  "data_version": "P0-P4 local artifacts; no new DPF observations generated",
  "dirty_state_digest": "4bce2c22c2106c9b9b4e204e098ece368ea6e31b247bc413910a6f3ad0238874",
  "dirty_state_line_count": 1424,
  "json_path": "experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p5_dpf_statistical_closeness_2026-06-08.json",
  "particle_counts": "reused from P1 for LGSSM only: [32, 64, 128]",
  "plan_path": "docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-subplan-2026-06-08.md",
  "python_version": "3.11.14",
  "report_path": "experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-2026-06-08.md",
  "result_path": "docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-dpf-statistical-closeness-result-2026-06-08.md",
  "review_ledger_path": "docs/plans/bayesfilter-dpf-filter-oracle-comparison-p5-claude-review-ledger-2026-06-08.md",
  "scoped_dirty_state_summary": "?? docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-execution-ledger-2026-06-08.md\n?? docs/plans/bayesfilter-dpf-filter-oracle-comparison-visible-gated-execution-runbook-2026-06-08.md\n?? experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p5_dpf_statistical_closeness_tf.py",
  "seed_list": "reused from P1 for LGSSM only: [101, 202, 303, 404, 505]",
  "tensorflow_imported": false,
  "tensorflow_probability_imported": false,
  "timestamp_utc": "2026-06-08T19:43:21Z",
  "wall_time_seconds": 0.013246649876236916
}
```

## Nonclaims

- P5 does not promote DPF bootstrap-OT or LEDH-PFPF-OT correctness.
- P5 does not establish stochastic-resampling distribution correctness.
- P5 does not use BF/FilterFlow agreement as oracle evidence.
- P5 does not use Zhao-Cui, CUT4, SVD, or UKF as DPF comparators.
- P5 does not establish nonlinear P44 DPF value or gradient closeness.
- P5 does not establish HMC readiness, production readiness, GPU readiness, or paper-scale claims.
