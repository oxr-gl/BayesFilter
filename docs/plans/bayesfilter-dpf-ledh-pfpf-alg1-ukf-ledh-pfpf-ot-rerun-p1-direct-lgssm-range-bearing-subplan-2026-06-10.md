# P1 Subplan: Direct LGSSM, Range-Bearing, And Gradient Replacement

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_OPUS_MAX_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the old direct LEDH-PFPF-OT LGSSM, range-bearing, stress, and gradient checks be replaced by Algorithm 1 UKF runs? |
| Baseline/comparator | Exact Kalman for LGSSM value and analytic score; bootstrap/no-flow PF comparator; UKF or reviewed approximation for range-bearing only if target-compatible. |
| Primary pass criterion | Direct replacement runner(s) produce reviewed row statuses using P0 predeclared thresholds: promoted only if value/gradient criteria and veto diagnostics pass; otherwise finite runs are diagnostic, N/A, or blocked. |
| Veto diagnostics | Old `ledh_pfpf_ot_tf.py` imported in replacement path; missing per-particle covariance diagnostics; range-bearing comparator used outside scope; value-only result promoted to gradient claim; one-seed ranking promoted. |
| Explanatory diagnostics | ESS, determinant ranges, covariance eigenvalues, particle-count ladder, runtime, old-vs-new delta. |
| Not concluded | No V2/filter-oracle coverage, no stochastic-score correctness, no OT extension claim. |

## Required Old-Lane Replacements

| Old runner | Required P1 action |
| --- | --- |
| `run_lgssm_ledh_pfpf_ot_tf.py` | Algorithm 1 LGSSM value rerun against Kalman and bootstrap/no-flow comparator. |
| `run_lgssm_multiseed_ledh_pfpf_ot_tf.py` | Multiseed paired particle ladder with uncertainty intervals. |
| `run_range_bearing_ledh_pfpf_ot_tf.py` | Algorithm 1 range-bearing runner if adapters exist; otherwise `BLOCKED_REQUIRES_ADAPTER` with exact missing callbacks. |
| `run_range_bearing_stress_ledh_pfpf_ot_tf.py` | Stress rerun after non-stress range-bearing passes, or blocked/tuning classification. |
| `run_ledh_pfpf_gradient_checks_tf.py` | Same-scalar fixed-branch gradient smoke and, if feasible, a bounded ladder. |

## Planned Implementation Work

If the existing P5 LGSSM runner is insufficient, create a narrowly scoped
replacement runner under:

`experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_alg1_ukf_direct_replacements_tf.py`

The runner must not import the old LEDH-PFPF-OT implementation path.  It must
emit JSON and Markdown reports with route identifiers and run manifests.

## Required Row Fields

Every output row must include the mandatory Algorithm 1 route fields from the
master program, `evidence_route_class`, `core_resampling_route`,
`extension_resampling_route`, predeclared value/gradient tolerances from P0,
seed count, particle ladder, uncertainty summaries, and per-row manifest link.
OT-augmented rows must be labelled
`BAYESFILTER_EXTENSION_NOT_SOURCE_CORE`.

## Planned Commands

CPU-only TensorFlow commands must set `CUDA_VISIBLE_DEVICES=-1` before import.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_ledh_pfpf_alg1_ukf_tf.py -q
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_alg1_ukf_p5_lgssm_comparison_tf
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_alg1_ukf_direct_replacements_tf
```

## Required Artifacts

- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_alg1_ukf_direct_replacements_2026-06-10.json`
- Markdown report:
  `experiments/dpf_implementation/reports/dpf-ledh-pfpf-alg1-ukf-direct-replacements-2026-06-10.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p1-direct-lgssm-range-bearing-result-2026-06-10.md`

## Exit Criteria

P1 passes only if LGSSM direct value reruns are reviewed against predeclared
thresholds, gradient status is explicit, uncertainty is preserved, and
range-bearing/stress lanes are either executed or blocked with precise adapter
requirements.  Finite-only rows can pass the phase as `DIAGNOSTIC_ONLY`, but
cannot be promoted.
