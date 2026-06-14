# Result: P8 LGSSM Exact-Oracle Amendment

Date: 2026-06-12

## Decision

LGSSM is no longer blocked on reproducing Zhao-Cui's MATLAB `rng(0); rand(3,3)`
observation matrix. Per the user amendment, LGSSM is simple enough that Phase 8
may use any valid identifiable LGSSM as an exact-oracle benchmark row.

The active row is now:

| Field | Value |
| --- | --- |
| row_id | `benchmark_lgssm_exact_oracle_m3_T50` |
| state/observation dimension | `3 / 3` |
| horizon | `50` |
| seed | `81100` |
| transition | diagonal with `phi = [0.72, 0.55, 0.35]` |
| observation matrix | fixed full-rank 3x3 matrix |
| process scale | `0.35` |
| observation scale | `0.45` |
| role | exact Kalman oracle benchmark, not Zhao-Cui MATLAB reproduction |

The historical `zhao_cui_lgssm_kalman_m3_T50` row is preserved only as an
excluded/historical row. It is not an active P8 blocker.

## Skeptical Audit

| Risk | Resolution |
| --- | --- |
| Wrong baseline | The row is explicitly labeled exact-oracle benchmark, not source-paper reproduction. |
| Proxy promotion | Dataset/gate artifacts still say `BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN`; no filter performance is claimed. |
| Hidden source substitution | The contract forbids claiming this row reproduces Zhao-Cui's MATLAB random `C`. |
| Stale blocker | Active P8 artifacts no longer contain `BLOCK_P8_B2_LGSSM_AUTHOR_C_MATRIX_PENDING`. |
| Unfair comparison | Approximate filters remain target-compatible/protocol-pending; Kalman is exact only for LGSSM or declared mixture rows. |

## Artifacts Updated

| Artifact | Outcome |
| --- | --- |
| `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json` | Active LGSSM row renamed to `benchmark_lgssm_exact_oracle_m3_T50`. |
| `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json` | LGSSM generated with finite 50x3 states and observations. |
| `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-blocker-fix-gates-2026-06-11.json` | LGSSM adapter cells are protocol-ready numeric-pending, not blocked. |
| `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-status-2026-06-11.json` | Row-level blocks now exclude LGSSM. |

## Remaining Blocks

| Block | Status |
| --- | --- |
| Generalized SV | `BLOCK_GENERALIZED_SV_NUMERIC_RUN_ESTIMATED_VALUES_PENDING` |
| SIR d=18 | `BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE` |
| Numeric benchmark | `BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN` |

## Validation

```text
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_fix_gates.py \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_closure.py \
  tests/highdim/test_filtering_value_gradient_benchmark_generalized_sv_spec.py \
  tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py \
  tests/highdim/test_p58_m9_source_route_pipeline_readiness.py \
  tests/highdim/test_p59_author_sir_36d_target_fit.py
```

Result: `55 passed, 2 warnings`.

## Claude Review

The first broad read-only Claude prompt hung. A tiny probe returned `PROBE_OK`,
so the review prompt was narrowed to the regenerated summary artifacts and this
amendment note.

Result: `PASS_P8_LGSSM_ORACLE_AMENDMENT_REVIEW`.

## Run Manifest

| Field | Value |
| --- | --- |
| git state | dirty worktree; edited/generated artifacts are uncommitted |
| environment | local Python/TensorFlow environment |
| CPU/GPU | CPU-only intent via `CUDA_VISIBLE_DEVICES=-1`; TensorFlow printed CUDA plugin/cuInit noise but commands exited 0 |
| random seed | LGSSM dataset seed `81100` |
| output summary | generated rows `5`, blocked rows `1` |
| not concluded | filter ranking, DPF gradient validity, Bayesian-estimation readiness |
