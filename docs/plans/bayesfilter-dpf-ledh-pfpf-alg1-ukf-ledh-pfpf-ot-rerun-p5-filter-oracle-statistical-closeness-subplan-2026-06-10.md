# P5 Subplan: Filter-Oracle Statistical Closeness Replacement

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_OPUS_MAX_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the filter-oracle P5 rows that previously contained `dpf_ledh_pfpf_ot` be rerun with Algorithm 1 UKF and valid target-route classifications? |
| Baseline/comparator | P0 rerun registry, P2-P4 Algorithm 1 contracts/results, and filter-oracle target-route registry; exact and approximation references must stay separate. |
| Primary pass criterion | Replacement rows report value and fixed-branch gradient closeness against P0/P2 predeclared tolerances, MC uncertainty, particle ladders, and row-level decisions for each eligible model; rows without thresholds are diagnostic or blocked, not promoted. |
| Veto diagnostics | Exact and approximation targets merged; old method id used; missing promotion tolerance from pre-run registry; seed variability absent; unsupported row promoted; gradient target mismatch. |
| Explanatory diagnostics | ESS, runtime, resampling count, covariance spectra, determinant ranges, old-vs-new deltas. |
| Not concluded | No correctness beyond tested rows, no stochastic branch-gradient correctness, no HMC readiness. |

## Planned Runner

Either amend the existing filter-oracle P5 runner to add a new method id
without importing old LEDH-PFPF-OT, or create:

`experiments/dpf_implementation/tf_tfp/runners/run_filter_oracle_comparison_p5_alg1_ukf_statistical_closeness_tf.py`

## Required Row Fields

Each row must include mandatory Algorithm 1 route fields, exact-vs-approximation
target class, core/extension resampling fields, predeclared value and gradient
tolerances, chosen binding statistic, seed count, particle ladder, confidence
intervals, maximum errors, and per-row manifest link.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_filter_oracle_comparison_p5_alg1_ukf_statistical_closeness_tf
```

## Required Artifacts

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filter_oracle_comparison_p5_alg1_ukf_statistical_closeness_2026-06-10.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-filter-oracle-comparison-p5-alg1-ukf-statistical-closeness-2026-06-10.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p5-filter-oracle-statistical-closeness-result-2026-06-10.md`

## Exit Criteria

P5 passes when every eligible old `dpf_ledh_pfpf_ot` statistical-closeness row
is replaced, downgraded, or blocked with reviewed row-level evidence.
