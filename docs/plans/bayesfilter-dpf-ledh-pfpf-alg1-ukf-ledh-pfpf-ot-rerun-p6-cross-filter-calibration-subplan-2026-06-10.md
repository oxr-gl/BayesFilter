# P6 Subplan: Cross-Filter Calibration Replacement

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_OPUS_MAX_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | How do Algorithm 1 UKF DPF value and gradient error scales compare to valid deterministic filters, with old calibrated rows used only as historical explanatory deltas? |
| Baseline/comparator | P5 replacement rows, exact/approximation filter-oracle references, UKF/SVD/CUT4/Zhao-Cui only on compatible rows. |
| Primary pass criterion | Cross-filter calibration tables include Algorithm 1 UKF rows, separate exact and approximation targets, normalized value/gradient errors, MC uncertainty, and applicability labels. |
| Veto diagnostics | Ranking filters on unsupported models; old LEDH row included as current evidence; missing uncertainty; thresholds changed after seeing results; gradient/value conflation. |
| Explanatory diagnostics | Filter point counts, ESS, runtime, route status, blocked adapters, old-vs-new deltas. |
| Not concluded | No universal ranking or production default. |

## Planned Runner

`experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p6_alg1_ukf_cross_filter_calibration_tf.py`

## Required Row Fields

Calibration tables must preserve mandatory Algorithm 1 route fields,
core/extension resampling fields, predeclared tolerance status, seed count,
particle ladder, uncertainty columns, comparator applicability class, and
per-row manifest links.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p6_alg1_ukf_cross_filter_calibration_tf
```

## Required Artifacts

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p6_alg1_ukf_cross_filter_calibration_2026-06-10.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p6-alg1-ukf-cross-filter-calibration-2026-06-10.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p6-cross-filter-calibration-result-2026-06-10.md`

## Exit Criteria

P6 passes when the comparison table is complete for all eligible rows and
every ineligible row is labelled `N/A_NOT_APPLICABLE` or
`BLOCKED_REQUIRES_ADAPTER` with a reason.
