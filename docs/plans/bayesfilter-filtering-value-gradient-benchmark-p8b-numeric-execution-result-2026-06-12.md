# P8b Numeric Execution Result

metadata_date: 2026-06-12
status: PARTIAL_P8_B7_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS
numeric_benchmark_status: partial_numeric_execution_remaining_adapter_and_seed_ladder_gaps

## Role Contract

Codex executed this phase visibly in the current dialogue as supervisor and
executor.  Claude was used only for read-only review/probe attempts.  No
detached Codex agent or overnight launcher was used.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P8 move from source/dataset/preflight readiness to actual numeric value/score/curvature artifacts without silent matrix holes? |
| Baseline | P8a synthetic-truth contract, source-paper scope contract, generated dataset manifest, P8 adapter-status matrix, and source-row refresh result. |
| Primary criterion | Every promoted source-paper algorithm/model cell has either a real numeric result or an explicit machine-readable pending, structured not-applicable, or DPF MC-SE blocker status. |
| Veto diagnostics | Old status-only matrices promoted as numeric evidence; P8a treated as completion; old LEDH-PFPF-OT evidence used as current evidence; DPF cells ranked before seed-ladder MC-SE; score coordinate provenance omitted. |
| Nonclaims | This is not full P8 closeout, not a filter ranking, not Bayesian-estimation readiness, and not DPF gradient certification. |

## Skeptical Audit

The P8b launch passed only as a partial-scope numeric run.  The old
`filtering_value_gradient_benchmark_emit_matrices.py` artifact remains
status-only and was not reused as performance evidence.  The new runner fills
only cells with executable, reviewed-enough routes and preserves every remaining
cell explicitly as pending, structured not-applicable, or DPF seed-ladder
blocked.

## Artifacts

- JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-results-2026-06-12.json`
- Value table:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-value-table-2026-06-12.csv`
- Score table:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-score-table-2026-06-12.csv`
- Curvature table:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-curvature-table-2026-06-12.csv`
- Status table:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-status-table-2026-06-12.csv`
- Stochastic uncertainty table:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-stochastic-uncertainty-table-2026-06-12.csv`
- Markdown summary:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-summary-2026-06-12.md`
- Runner:
  `scripts/filtering_value_gradient_benchmark_run_p8_numeric.py`
- Focused tests:
  `tests/highdim/test_filtering_value_gradient_benchmark_p8b_numeric.py`

## Numeric Coverage

| Metric | Count |
| --- | ---: |
| Full source-scope cells | 42 |
| Executed numeric/value cells | 5 |
| Explicit pending, structured not-applicable, or DPF MC-SE blocked cells | 37 |

Executed cells:

| Algorithm | Row | Status | Average log likelihood | Score norm | Curvature status |
| --- | --- | --- | ---: | ---: | --- |
| `kalman_exact_or_mixture_enumeration` | `benchmark_lgssm_exact_oracle_m3_T50` | `executed_numeric` | -2.721519497158494 | 8.331768835665503 | `observed_negative_log_likelihood_hessian_positive_definite` |
| `ukf` | `benchmark_lgssm_exact_oracle_m3_T50` | `executed_value_only` | -2.721519497158494 | N/A | `hessian_not_exposed_numeric_pending` |
| `svd_sigma_point` | `benchmark_lgssm_exact_oracle_m3_T50` | `executed_value_only` | -2.721519497158494 | N/A | `hessian_not_exposed_numeric_pending` |
| `cut4` | `benchmark_lgssm_exact_oracle_m3_T50` | `executed_value_only` | -2.721519497158494 | N/A | `hessian_not_exposed_numeric_pending` |
| `kalman_exact_or_mixture_enumeration` | `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `executed_value_only_declared_surrogate` | -2.2846321465997916 | N/A | `hessian_not_exposed_numeric_pending` |

## Validation

Commands run:

```text
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8_numeric.py
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8b_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_closure.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_fix_gates.py
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_run_p8_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8b_numeric.py
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8b_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-results-2026-06-12.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-value-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-score-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-curvature-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-status-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-stochastic-uncertainty-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-summary-2026-06-12.md
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-results-2026-06-12.json
```

Observed validation:

```text
23 passed in 19.42s
```

`compileall`, `git diff --check`, and `json.tool` passed.

## Claude Review Attempts

Claude probe:

```text
PROBE_OK
```

Read-only review prompts with file paths and then inline facts did not return
within the visible review window.  Host process checks showed two named review
workers still alive:

- `filter-bench-p8b-numeric-review-iter1b`;
- `filter-bench-p8b-numeric-review-iter1c`.

Both named review workers were terminated.  No named P8b Claude review worker
remained afterward.  Because the review did not converge, this result does not
claim `PASS_P8_B8_REVIEWED_CLOSEOUT`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Keep P8 open and continue remaining phases | Partial: no silent holes and 5 executed cells, but 37 cells remain pending/not-applicable/DPF blocked | Passed for executed subset; full closeout blocked by missing review and remaining numeric adapters | Non-LGSSM adapters, DPF seed ladders/MC-SE, and score/curvature provenance | Continue P8-B5/P8-B7 adapter execution and rerun Claude review with a smaller artifact slice | Full benchmark ranking, DPF gradient validity, and Bayesian-estimation readiness |

## Required Tokens

```text
PARTIAL_P8_B7_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS
BLOCK_P8_B8_REVIEWED_CLOSEOUT_CLAUDE_NONRESPONSE_AFTER_PROBE
```

