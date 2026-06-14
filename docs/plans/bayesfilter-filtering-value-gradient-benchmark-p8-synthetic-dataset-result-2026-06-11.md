# P8-B2 Synthetic Dataset Result

metadata_date: 2026-06-11
status: PASS_P8_B2_SYNTHETIC_DATASET_MANIFEST_PARTIAL_WITH_ROW_BLOCKS
numeric_benchmark_status: BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can Phase P8-B2 materialize reproducible synthetic dataset manifests for the promoted source-paper rows without hiding remaining source preconditions? |
| Baseline/comparator | P8 blocker-closure master plan, source-paper scope contract, P8 blocker status manifest, generalized-SV testing spec, P58/P59 SIR source-route ledgers, and TensorFlow model helpers. |
| Primary criterion | Emit JSON/CSV/Markdown dataset artifacts with seeds, horizons, finite summaries, truth provenance, row-level blocks, and no numeric filter-performance claim. |
| Veto diagnostics | LGSSM substitutes NumPy/Octave RNG for MATLAB `rng(0); rand(3,3)`; generalized SV uses author defaults or SP500 returns as benchmark data; raw SIR synthetic generation is promoted as source-route TT/SIRT validation; predator-prey domain diagnostics are hidden; numeric benchmark status changes to pass. |
| Explanatory diagnostics | Tensor summaries, SHA256 hashes, domain diagnostics, focused schema tests, compile checks, and Claude read-only review. |
| Not concluded | No value/score/curvature benchmark, no filter ranking, no generalized-SV readiness, no SIR d=18 source-route success, and no Bayesian-estimation handoff. |
| Result artifacts | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json`, `.csv`, and `.md`. |

## Skeptical Audit

Status: `PASS_FOR_P8_B2_PARTIAL_DATASET_EXECUTION`.

- Wrong baseline risk: pass.  The manifest uses the source-paper scope rows and
  does not reintroduce P44 diagnostic rows.
- Proxy-risk: pass.  The raw SIR path is labeled a synthetic data artifact, not
  author source-route validation.
- Hidden-substitution risk: pass.  LGSSM remains blocked until the exact MATLAB
  author observation matrix is materialized; generalized SV remains blocked
  until checked estimated values are materialized.
- Artifact-risk: pass.  The emitter is executable and tested by a regeneration
  test, not only static snapshot reads.
- Domain-risk: recorded.  Predator-prey negative post-noise states are visible
  under the model's `diagnose_negative_after_noise` policy.

## Implementation

Added or updated:

- `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.md`

The script now inserts the repository root into `sys.path` before importing
`bayesfilter`, so the direct runbook command works from the repository root.
The central blocker-closure status manifest was regenerated after this phase so
`P8-B2` is no longer stale `not_started`; it is now
`partial_pass_with_row_blocks`.

## Dataset Rows

| Row | Dataset status | Horizon | Seed | Blocker |
| --- | --- | ---: | ---: | --- |
| `zhao_cui_lgssm_kalman_m3_T50` | `blocked` |  |  | `BLOCK_P8_B2_LGSSM_AUTHOR_C_MATRIX_PENDING` |
| `zhao_cui_sv_actual_nongaussian_T1000` | `generated` | 1000 | 81101 |  |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `generated` | 1000 | 81101 |  |
| `zhao_cui_spatial_sir_austria_j9_T20` | `generated` | 20 | 81103 |  |
| `zhao_cui_predator_prey_T20` | `generated` | 20 | 81104 |  |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `blocked` |  |  | `BLOCK_GENERALIZED_SV_NUMERIC_RUN_ESTIMATED_VALUES_PENDING` |

Generated row summaries:

| Row | Observation SHA256 | Observation mean | Observation stddev |
| --- | --- | ---: | ---: |
| `zhao_cui_sv_actual_nongaussian_T1000` | `5e2423149e4f59eb588ccc7f16ec6d9ee984ccc4710a3ae07a3dbcf5c37db748` | -0.016664233094913185 | 0.6828614132399085 |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `891bbf642b948e793a70ee2c8b37002d1b784a1802d359e5304c7fdb57d75cf4` | -3.1418773080332367 | 2.5618932054909043 |
| `zhao_cui_spatial_sir_austria_j9_T20` | `cb72b8ebb705c0f791e6f5edace8b296b7da46e5236a9824a1d5a30a261572e5` | 64.26918068449397 | 46.08794701876618 |
| `zhao_cui_predator_prey_T20` | `dc63294b6e77913aef0c92796dd2d3c7a1721a766f976fcc392cd02a70754387` | 54.92266755966982 | 54.43407000776854 |

## Commands Run

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py
```

Result: passed and emitted the dataset manifest artifacts.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_p8_blocker_closure.py
```

Result: passed and refreshed the central P8 blocker-closure status manifest
with the reviewed B2 partial-pass state.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_closure.py tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py tests/highdim/test_filtering_value_gradient_benchmark_generalized_sv_spec.py tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py tests/highdim/test_p58_m9_source_route_pipeline_readiness.py tests/highdim/test_p59_author_sir_36d_target_fit.py
```

Result:

```text
47 passed, 2 warnings
```

The warnings are TensorFlow Probability deprecation warnings from the installed
environment.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py
```

Result: passed.

```text
git diff --check -- scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-result-2026-06-11.md
```

Result: passed before this review addendum was appended.

## Claude Execution Review

Claude read-only review iteration 1 returned:

```text
VERDICT: PASS_REVIEW
```

Claude checked the material failure modes and found no required revision:

- the execution remains a partial P8-B2 dataset manifest and keeps the numeric
  benchmark blocked;
- LGSSM remains blocked until the exact MATLAB-generated `C` matrix is
  materialized and no NumPy/Octave RNG substitute is used;
- generalized SV does not substitute SP500 data or author defaults;
- raw spatial-SIR synthetic data is not promoted as TT/SIRT source-route
  validation;
- predator-prey negative-state diagnostics are visible;
- the tests are not static-only because the suite reruns the generator in a
  subprocess and compares regenerated artifacts.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass P8-B2 as a partial dataset-manifest phase. | Met for SV actual, SV KSC surrogate, raw SIR synthetic path, and predator-prey. | No proxy promotion or forbidden substitution observed. | LGSSM exact author matrix and generalized-SV estimated values remain missing. | Continue P8-B3/P8-B4/P8-B5, while separately closing the LGSSM matrix and generalized-SV estimate materialization gates. | Numeric performance or ranking. |
| Keep P8 numeric benchmark blocked. | Met: evaluator/adapters, horizon calibration, stochastic calibration, and reviewed numeric tables are still absent. | Numeric-run block remains active. | How much of the benchmark can run before SIR source-route and generalized-SV materialization are closed. | Do not rank filters; continue implementation phases. | Bayesian-estimation readiness. |

## Remaining Blocks

- `BLOCK_P8_B2_LGSSM_AUTHOR_C_MATRIX_PENDING`: the source row defines the
  observation matrix as MATLAB `rng(0); rand(3,3)`.  This run did not find a
  checked materialized matrix and did not substitute another RNG.
- `BLOCK_GENERALIZED_SV_NUMERIC_RUN_ESTIMATED_VALUES_PENDING`: synthetic
  generalized-SV data remains forbidden until checked Zhao--Cui estimated
  values are materialized.
- `BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE`: raw synthetic SIR data exists,
  but source-route TT/SIRT validation still requires P59-9b through P59-9e.
- `BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN`: value, score, curvature, and
  uncertainty tables have not been produced.

## Required Tokens

```text
PASS_P8_B2_SYNTHETIC_DATASET_MANIFEST_PARTIAL_WITH_ROW_BLOCKS
BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN
BLOCK_P8_B2_LGSSM_AUTHOR_C_MATRIX_PENDING
BLOCK_GENERALIZED_SV_NUMERIC_RUN_ESTIMATED_VALUES_PENDING
```
