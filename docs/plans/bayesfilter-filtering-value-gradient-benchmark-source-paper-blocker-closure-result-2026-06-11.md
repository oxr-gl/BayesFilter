# Source-Paper Benchmark Blocker-Closure Result

metadata_date: 2026-06-11
phase: FILTER_BENCH_SOURCE_PAPER_BLOCKER_CLOSURE
status: PASS_FILTER_BENCH_SOURCE_PAPER_BLOCKER_CLOSURE
numeric_benchmark_status: BLOCK_FILTER_BENCH_SOURCE_PAPER_NUMERIC_RUN_PENDING
supervisor: Codex
executor: Codex in this dialogue
reviewer: Claude Code read-only

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What fixable blockers must be closed before the filtering benchmark can use exact source-paper/code values across the in-scope model families? |
| Baseline/comparator | P10 truth-prior audit, current P8/P9 synthetic-truth artifacts, visible runbook, master program, and local Zhao--Cui paper/code anchors. |
| Primary criterion | Passed at scope-contract level: a superseding source-paper scope contract now removes P44 diagnostics from promoted source-paper benchmark tables, locks source values, and records remaining implementation blockers. |
| Veto diagnostics | No source-scope veto fired.  Numeric benchmark remains blocked because reviewed source-paper evaluators and value/score/curvature/stochastic tables do not yet exist. |
| Nonclaims | This result is not a numeric benchmark, filter ranking, DPF gradient certification, SIR d=18 route pass, generalized-SV adapter pass, or Bayesian-estimation handoff. |

## Claude Plan Review

Plan review iteration 1 with the longer prompt produced no output in the
allotted wait.  Per runbook protocol, Codex ran a small read-only Claude probe,
which returned:

```text
PROBE_OK
```

That showed Claude availability was not the issue.  Codex shortened the review
prompt and retried.

Plan review iteration 1b returned:

```text
VERDICT: AGREE
```

## Artifacts

- Plan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-blocker-closure-plan-2026-06-11.md`
- Source-paper scope contract:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`
- Source-paper summary CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-summary-2026-06-11.csv`
- Source-paper summary Markdown:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-summary-2026-06-11.md`
- Emitter:
  `scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py`
- Focused tests:
  `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- Updated visible runbook:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-gated-execution-runbook-2026-06-10.md`
- Updated master program:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-closure-master-program-2026-06-10.md`

## Source-Scope Summary

Promoted source-paper rows:

| Row | Status |
| --- | --- |
| `zhao_cui_lgssm_kalman_m3_T50` | source values locked; evaluator pending |
| `zhao_cui_sv_actual_nongaussian_T1000` | source values locked; evaluator pending |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | source values locked; surrogate row with KSC source-gap note; evaluator pending |
| `zhao_cui_spatial_sir_austria_j9_T20` | source values locked; d=18 value route/rank-selection repair pending |
| `zhao_cui_predator_prey_T20` | source values locked; evaluator pending |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | amended synthetic `svmodels` row; Zhao--Cui estimated values pending extraction before data generation |

Excluded or historical rows:

- `p44_cubic_additive_gaussian_dim_1_2_3`
- `p44_quadratic_observation_dim_1_2_3`
- `p44_nonlinear_transition_h2_dim_1_2_3`
- `p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3`
- `lgssm_exact_kalman_dim_1_2_3`
- `native_generalized_sv_dense_lower_rung_dim_2`
- `zhao_cui_generalized_sv_sp500_author_code`
- `spatial_sir_lower_rung_j1_dim_2`
- `predator_prey_production_tuned_h25_dim_2`

The excluded rows may still be useful engineering diagnostics, but they are not
promoted source-paper benchmark rows.

## Fixed Blockers

| Blocker | Result |
| --- | --- |
| P44 diagnostics still in active-looking P8 roster | Repaired by superseding source-paper scope contract; old P8 preserved as historical. |
| LGSSM project coordinates versus Zhao--Cui values | Repaired at scope level with source row `(a,d)=(0.8,0.5)`, `T=50`, `m=n=3`. |
| SV/KSC source values | Repaired at scope level with `sigma=1`, `(gamma,beta)=(0.6,0.4)`, `T=1000`; KSC remains surrogate-labeled. |
| Native generalized SV project fixture | Repaired at scope level by excluding the fixture and retaining a Zhao--Cui `svmodels` synthetic row whose truth vector is blocked until estimated values are extracted. |
| Spatial SIR lower rung versus source row | Repaired at scope level by promoting `J=9`, `d=18`, `T=20` and marking value route repair pending. |
| Predator-prey T=25 project stress row | Repaired at scope level by promoting Zhao--Cui `T=20` source row and marking T=25 as project stress/diagnostic. |
| SP500 direct-data generalized SV scope | Amended: SP500 returns are source-estimation input only; benchmark data must be synthetic data generated from Zhao--Cui estimated `svmodels` parameter values after those values are materialized. |

## Claude Execution Review

Claude execution review iteration 1 returned:

```text
VERDICT: AGREE
```

Non-blocking caveat:

- LGSSM locks the author-code observation matrix procedurally as
  `rng(0) author-code random C with n=3, m=3` rather than materializing the
  numeric matrix in this scope contract.  This is acceptable for blocker
  closure, but the next numeric source-paper phase should materialize or
  otherwise exactly replay the author-code `C` path in its run manifest.

## Remaining Fixable Tasks

- Implement source-paper target/evaluator rows for LGSSM T=50, SV T=1000,
  KSC surrogate, and predator-prey T=20.
- Materialize or exactly replay the Zhao--Cui LGSSM author-code observation
  matrix `C` used with `rng(0)` for numeric reproducibility.
- Repair or explicitly block the spatial SIR `J=9`, `d=18` rank-selection and
  value route before numeric source-paper SIR performance.
- Extract, digitize, or regenerate the Zhao--Cui generalized-SV estimated
  `svmodels` parameter vector, then implement the source-route synthetic data
  generator/evaluator.  Do not use author-code defaults or the BayesFilter
  native generalized-SV fixture as substitutes.
- Run the source-paper numeric benchmark and produce value, componentwise
  score, curvature, failure, and stochastic uncertainty tables.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; artifacts uncommitted |
| Dirty-state summary | dirty worktree preserved; unrelated changes not reverted |
| Command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py` |
| Environment | local Python environment |
| CPU/GPU status | CPU-only metadata/schema emission; no GPU conclusion |
| Seeds | N/A; no random draws generated |
| Plan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-blocker-closure-plan-2026-06-11.md` |
| Result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-blocker-closure-result-2026-06-11.md` |
| Output JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json` |

## Validation

Commands run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
git diff --check -- scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-blocker-closure-plan-2026-06-11.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-blocker-closure-result-2026-06-11.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-summary-2026-06-11.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-summary-2026-06-11.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-gated-execution-runbook-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-closure-master-program-2026-06-10.md
```

Results:

```text
emitter: exited 0; PASS_FILTER_BENCH_SOURCE_PAPER_SCOPE_CONTRACT; BLOCK_FILTER_BENCH_SOURCE_PAPER_NUMERIC_RUN_PENDING
json.tool: exited 0
pytest: 8 passed in 0.05s
compileall: exited 0
git diff --check: exited 0
```

## Decision Table

| Decision | Primary criterion | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass source-paper scope repair | Source-paper rows/exclusions are frozen with source anchors and no P44 diagnostic promotion | No scope veto fired | Numeric evaluator implementation remains pending | Implement source-paper numeric benchmark phase using the new scope | Filter ranking, DPF gradient validity, SIR d=18 readiness, Bayesian-estimation handoff |
| Block source-paper numeric performance | No source-paper numeric values have been generated in this phase | Numeric-run-pending block active | Whether generalized-SV estimates can be extracted locally or require digitization/rerun, and which route repairs are needed for SIR d=18 | Write/execute focused numeric benchmark implementation plan | That any algorithm performs better or worse on source-paper rows |

Required tokens:

```text
PASS_FILTER_BENCH_SOURCE_PAPER_BLOCKER_CLOSURE
BLOCK_FILTER_BENCH_SOURCE_PAPER_NUMERIC_RUN_PENDING
```
