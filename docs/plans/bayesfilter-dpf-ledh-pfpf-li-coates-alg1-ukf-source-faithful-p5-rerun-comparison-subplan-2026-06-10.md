# P5 Subplan: Test Rerun And Filter Comparisons

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After P4 passes, how does the new Algorithm 1 UKF LEDH-PFPF route compare with valid oracles and existing filters on value and gradient metrics? |
| Baseline/comparator | Exact Kalman on LGSSM; bootstrap-OT; UKF/SVD/CUT4/Zhao-Cui where model support is valid; previous LEDH-PFPF-OT only as quarantined historical delta, not as evidence. |
| Primary pass criterion | All relevant new-filter tests and comparison rows run with finite value and fixed-branch gradient diagnostics, uncertainty reporting, and model/filter applicability recorded. |
| Veto diagnostics | Running P5 before P4 passes; using old LEDH-PFPF-OT implementation; ranking filters on unsupported model/filter pairs; one-seed differences treated as conclusions; non-finite rows; missing uncertainty. |
| Explanatory diagnostics | ESS, runtime, covariance spectra, determinant ranges, old-vs-new deltas, particle ladders. |
| Not concluded | No universal superiority, no production default, no full stochastic-resampling gradient correctness, no HMC target readiness. |
| Required artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p5-rerun-comparison-result-2026-06-10.md` |

## Comparison Ladder

Use the broadest valid ladder per model:

- naive/bootstrap baseline where available;
- exact oracle where available, especially LGSSM Kalman value and gradient;
- Gaussian/sigma-point approximations where applicable: UKF, SVD, CUT4;
- Zhao-Cui or sparse/tensor filters only on models where their contracts apply;
- new Algorithm 1 UKF LEDH-PFPF core;
- optional BayesFilter OT-resampling extension, labelled as extension.

If a filter is not valid for a model, record `N/A_NOT_APPLICABLE` with the
reason.  Do not record such rows as blocked unless implementation work is
actually missing for a model/filter pair that should be supported.

## Metrics

Record at minimum:

- value error normalized per observation and, where relevant, per dimension;
- fixed-branch gradient residuals against exact or strongest available
  comparator;
- Monte Carlo uncertainty across seeds;
- particle count, pseudo-time schedule, UKF parameters, resampling route;
- CPU/GPU status and `CUDA_VISIBLE_DEVICES` setting before TensorFlow import;
- route identifiers from P3.

Each serious comparison run must also include a full run manifest with git
branch/commit, exact command, environment or conda environment, data/model
fixture version or digest, random seeds, particle counts, pseudo-time schedule,
UKF parameter settings, wall time, output artifact paths, and plan/result paths.

## Gate

P5 passes only after result tables and JSON outputs are written, uncertainty and
applicability are explicit, and Claude read-only review agrees that no proxy
metric has been promoted beyond its evidence contract.
