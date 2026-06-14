# P8 Generalized SV Prior-Mean Amendment Result

metadata_date: 2026-06-12
status: PASS_P8_GENERALIZED_SV_PRIOR_MEAN_AMENDMENT
owner: Codex

## Decision

The generalized-SV Phase 8 row no longer blocks on missing Zhao--Cui posterior
estimates.  Following the user's amendment, the active test case is a synthetic
`svmodels` row generated from the Zhao--Cui Section 6.2 S&P 500 prior-center
convention.

This is a dataset/specification readiness result, not a filter performance
result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generalized-SV row use the Zhao--Cui S&P prior-center test point instead of waiting for posterior estimates? |
| Baseline/comparator | Former active blocker `BLOCK_GENERALIZED_SV_NUMERIC_RUN_ESTIMATED_VALUES_PENDING`. |
| Primary criterion | Active spec, source-scope, dataset, gate, and closure artifacts carry the prior-center convention and generated synthetic row without using author defaults or SP500 returns as truth/data. |
| Veto diagnostics | Reintroducing the old estimated-values blocker; using author defaults as truth; using SP500 returns as benchmark observations; claiming finite ordinary means for `sigma^2` or `beta`; claiming filter ranking. |
| Explanatory diagnostics | Dataset summaries, hashes, status matrices, and source-coordinate caveats. |
| Not concluded | No value/gradient benchmark result, no generalized-SV evaluator correctness, no DPF gradient certification, no posterior estimate from SP500 returns. |
| Preserved artifact | This result note plus regenerated P8 artifacts under `docs/plans`. |

## Prior-Center Test Point

Source anchors:

- Zhao--Cui Section 6.2 S&P 500 prior: `(gamma+1)/2 ~ Beta(20,1.5)`, `sigma^2 ~ IG(1,0.005)`, `log(beta)|sigma ~ N(0, sigma^2/0.8)`, `T=1008`.
- Author-code route: `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels`.

Finite-coordinate convention:

| Quantity | Value |
| --- | ---: |
| `E[(gamma+1)/2]` | `0.9302325581395349` |
| `E[gamma]` | `0.8604651162790697` |
| `E[sigma]` / source `tau` | `0.12533141373155002` |
| third active center | `0.0` |
| active transformed theta | `[1.0824113944610982, -2.076793740349318, 0.0]` |

Caveats:

- `E[sigma^2]` is infinite under the inverse-gamma shape `1`.
- The ordinary unconditional `E[beta]` is not used.
- The paper writes the third transformed coordinate as `log(beta)/sigma`; the mirrored `svmodels` code names the third active coordinate `mu` and maps `mu = z_mu * tau`.  The prior-center value is zero under both labels, but score-coordinate semantics still need evaluator review.

## Generated Dataset

| Field | Value |
| --- | --- |
| Row | `zhao_cui_generalized_sv_synthetic_from_estimated_values` |
| Dataset status | `generated` |
| Horizon | `1008` |
| Seed | `81105` |
| Observation SHA256 | `c990947b16d5ef108870fcb716836166a41b1fe31503b9cb5e0cd0459d4a53f2` |
| State SHA256 | `2a976493f58cc839667f8f4c892e92853dc232f5fe02fc617dad202b300ee358` |
| Observation mean/std | `0.010268641317545358` / `1.0098939524994113` |
| State mean/std | `0.15324624283601654` / `1.9321074929792903` |

## Updated Active Status

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.json`
  now reports `PASS_GENERALIZED_SV_PRIOR_MEAN_TEST_CASE_READY_NUMERIC_EVALUATOR_PENDING`.
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`
  has `estimated_values_pending_source_row_ids: []`.
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json`
  has `dataset_status_counts: {"generated": 6}`.
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-blocker-fix-gates-2026-06-11.json`
  keeps only `BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE` and
  `P8_B7_NUMERIC_EVALUATOR_RUN_NOT_EXECUTED` as active numeric blockers.

## Validation

Command:

```text
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_generalized_sv_spec.py tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_fix_gates.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_closure.py tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py tests/highdim/test_p58_m9_source_route_pipeline_readiness.py tests/highdim/test_p59_author_sir_36d_target_fit.py
```

Result:

```text
55 passed, 2 warnings
```

Warnings were TensorFlow Probability deprecation warnings only.

## Claude Review

The first Opus review prompt produced no output; a small probe returned
`PROBE_OK`, confirming Claude was available and the prompt was too heavy.  The
compact read-only review then returned:

```text
PASS_P8_GENERALIZED_SV_PRIOR_MEAN_REVIEW
```

Claude checked that the old estimated-values blocker was replaced by the
Zhao--Cui S&P prior-center row, the finite-coordinate mean caveats were present,
author defaults were not promoted to truth, SP500 returns were not benchmark
observations, and no filter-performance claim was made.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Adopt generalized-SV prior-center synthetic row | Met: active artifacts carry source prior, finite-coordinate convention, generated dataset, and hashes. | Passed: no author-default truth, no SP500 benchmark data, no finite-mean overclaim for `sigma^2`/`beta`, no filter ranking. | Source-route evaluator and score-coordinate semantics remain pending. | Implement/run value and eligible score evaluators under P8-B7. | Filter performance, DPF gradient validity, posterior SP500 estimate. |
| Keep full P8 numeric benchmark blocked | Met: value/score tables have not been run and SIR source-route blocker remains. | Passed: numeric benchmark status remains blocked. | SIR d=18 source-route phases and evaluator execution. | Continue P59/P8-B7 rather than ranking filters. | Filtering closeout or Bayesian-estimation readiness. |
