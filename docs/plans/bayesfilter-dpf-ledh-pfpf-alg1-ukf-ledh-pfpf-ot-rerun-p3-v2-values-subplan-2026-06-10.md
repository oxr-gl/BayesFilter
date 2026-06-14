# P3 Subplan: V2 Algorithm 1 Value Replacement

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_OPUS_MAX_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | For V2 rows declared runnable in P2, do Algorithm 1 UKF value runs execute finitely and preserve Monte Carlo uncertainty while all P2-blocked rows remain visible? |
| Baseline/comparator | P2 frozen contracts; exact Kalman on LGSSM; bootstrap/no-flow PF as a baseline comparator; non-LGSSM rows remain diagnostic-only in P3 unless a valid oracle is declared later. |
| Primary pass criterion | Every P2 row appears with a reviewed status; every P2 runnable row is executed or explicitly downgraded; P2-blocked rows may carry forward only with adapter reasons; finite runnable rows include uncertainty, route fields, and no promotion claim. |
| Veto diagnostics | P2 contract absent; old LEDH route imported; nonfinite weights/determinants/covariances; missing MC uncertainty; unsupported comparator ranked. |
| Explanatory diagnostics | ESS, runtime, determinant range, covariance eigenvalues, old-vs-new historical delta. |
| Not concluded | No gradient correctness, no full stochastic resampling correctness, no production default. |

## Planned Runner

`experiments/dpf_implementation/tf_tfp/runners/run_v2_ledh_pfpf_alg1_ukf_values_tf.py`

## Required Row Fields

Every output row must carry mandatory Algorithm 1 route fields, core/extension
resampling fields, predeclared value tolerance/certification band, seed count,
particle ladder, mean error, standard error, confidence interval, RMSE, maximum
absolute error, and per-row manifest link.  Unsupported comparator rows must
not be ranked.

## Planned Command

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_alg1_ukf_values_tf
```

## Required Artifacts

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_alg1_ukf_values_2026-06-10.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-alg1-ukf-values-2026-06-10.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p3-v2-values-result-2026-06-10.md`

## Exit Criteria

P3 local-pass-candidate status is reached when every P2 runnable row is
executed or downgraded with reviewed evidence, every P2-blocked row remains
classified with adapter reasons and does not disappear, and finite-only rows are
not promoted without satisfying predeclared thresholds.  This local status is
not an unconditional phase pass until Claude read-only review agrees.
