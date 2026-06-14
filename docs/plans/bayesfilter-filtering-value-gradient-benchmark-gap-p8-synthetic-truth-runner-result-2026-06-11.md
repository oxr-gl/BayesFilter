# P8 Result: Synthetic-Truth Benchmark Runner Contract

metadata_date: 2026-06-11
phase: FILTER_BENCH_P8
status: PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT
numeric_benchmark_status: BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING
supervisor: Codex
reviewer: Claude Code read-only

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can P8 convert the frozen P7 all-filter/all-model roster into a synthetic-truth benchmark runner contract with no silent holes and no oracle-overclaim? |
| Baseline/comparator | Reviewed synthetic-truth methodology, P7 frozen roster, P6 gradient semantics, and the old P8 blocked matrix result. |
| Primary criterion | Passed for contract emission: the artifact preserves all 7 x 12 cells, freezes capability/provenance schemas, componentwise score schema, tuple manifest schema, truth-design requirements, and status tables without numeric overclaim. |
| Veto diagnostics | No contract-emission veto fired.  Numeric performance closeout remains blocked because accepted truth draws, synthetic datasets, horizon calibration, stochastic seed calibration, and reviewed evaluator outputs are not present. |
| Nonclaims | This is not a filter ranking, not a full numeric benchmark result, not nonlinear exact-likelihood evidence, not DPF gradient certification, and not Bayesian-estimation readiness. |

## Plan Review Loop

Claude plan review iteration 1 returned `VERDICT: REVISE`.

Major findings:

- The draft under-specified canonical `phi` derivative semantics, especially
  chain-rule score conversion, full Hessian transforms, and
  `not_available_transform_gap`.
- The draft omitted the mandatory componentwise score artifact/schema.

Repairs:

- Added allowed score and Hessian provenance/status vocabularies.
- Added explicit score and Hessian chain-rule policy, including full Hessian
  transform and partial-transform diagnostic-only handling.
- Added mandatory componentwise score artifact/schema.
- Tightened tuple-level accepted-draw manifest schema.

Claude plan review iteration 2 returned:

```text
VERDICT: AGREE
```

## Artifacts

- P8 revised subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-subplan-2026-06-11.md`
- P8 synthetic-truth contract JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json`
- Capability crosswalk CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-capability-crosswalk-2026-06-11.csv`
- Capability crosswalk Markdown:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-capability-crosswalk-2026-06-11.md`
- Emitter:
  `scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py`
- Focused validation:
  `tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py`

## Output Summary

The frozen P7 roster is preserved:

- algorithms: 7 current rows;
- models: 12 frozen columns;
- current cells: 84;
- historical-only rows: `ledh_pfpf_ot_historical` excluded from current
  evidence.

Capability status counts:

| Status | Count |
| --- | ---: |
| `value_plus_score` | 8 |
| `value_only` | 22 |
| `diagnostic_derivative_only` | 10 |
| `not_available_with_reason` | 44 |

Current performance status counts:

| Status | Count |
| --- | ---: |
| `pending_numeric_execution` | 65 |
| `not_applicable_by_target` | 13 |
| `blocked_before_numeric_execution` | 6 |

Score provenance counts:

| Provenance | Count |
| --- | ---: |
| `native_phi_autodiff` | 8 |
| `algorithm_gradient_not_exposed` | 24 |
| `adapter_required_pending` | 25 |
| `unsupported_by_target` | 13 |
| `blocked_value_route` | 6 |
| `no_theta_gradient_dim0` | 4 |
| `fixed_branch_diagnostic_only` | 4 |

Hessian provenance counts:

| Provenance | Count |
| --- | ---: |
| `native_phi_hessian_autodiff` | 1 |
| `hessian_not_exposed` | 26 |
| `adapter_required_pending` | 25 |
| `unsupported_by_target` | 13 |
| `blocked_value_route` | 6 |
| `not_available_transform_gap` | 5 |
| `no_theta_gradient_dim0` | 4 |
| `partial_transform_diagnostic_only` | 4 |

## Validation

Commands run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py
git diff --check -- scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-subplan-2026-06-11.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-capability-crosswalk-2026-06-11.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-capability-crosswalk-2026-06-11.md
```

Results:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py
wrote docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json
status PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT
numeric_benchmark_status BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING

python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json
exited 0

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py
8 passed in 0.05s

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py
exited 0

git diff --check -- ...
exited 0
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; P8 synthetic-truth artifacts uncommitted |
| Dirty-state summary | dirty worktree preserved; unrelated changes not reverted |
| Command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py` |
| Environment | local Python environment |
| Conda env | N/A |
| CPU/GPU status | CPU-only metadata/schema emission; no GPU conclusion |
| dtype | Manifest-level only; per-row dtype lives in P1 registry |
| Seeds | No new random draws generated in this contract phase |
| Plan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-subplan-2026-06-11.md` |
| Result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-result-2026-06-11.md` |
| Output JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass revised P8 contract gate | Synthetic-truth contract emitted for all frozen cells with provenance and no proxy performance claims | No contract veto fired | Numeric benchmark execution remains pending | Generate accepted truth draws, calibrate horizons/seeds, then run reviewed evaluators | Filter ranking, full numeric value/score/curvature performance, DPF gradient certification, Bayesian-estimation readiness |
| Block full numeric P8 performance closeout | Accepted truth draws and reviewed numeric evaluator outputs are absent | Numeric-run-pending block active | Which evaluator cells become numeric after calibration and adapter repair | Write the next execution plan for truth-draw generation and numeric evaluator implementation | That any algorithm is better or worse on the benchmark ladder |

## Post-Run Red-Team Note

- Strongest alternative explanation: a contract artifact can look like progress
  while still leaving the numeric benchmark unrun.
- What would overturn the numeric block: accepted truth draws, synthetic
  datasets, horizon and seed calibration, and reviewed evaluator outputs for
  reportable cells.
- Weakest part of evidence: no likelihood, score, curvature, or stochastic
  uncertainty measurements are produced in this phase.

Required tokens:

```text
PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT
BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING
```
