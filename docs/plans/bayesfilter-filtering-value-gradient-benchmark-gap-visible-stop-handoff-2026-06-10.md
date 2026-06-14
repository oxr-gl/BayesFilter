# Filtering Value/Gradient Benchmark Gap-Closure Visible Stop Handoff

metadata_date: 2026-06-11
program: filtering-value-gradient-benchmark-gap-closure
status: BLOCKED_AT_P9_NUMERIC_BENCHMARK_PENDING
supervisor: Codex
reviewer: Claude Code read-only

## Current State

Execution launched in the current dialogue on 2026-06-10 23:17 HKT.  It first
stopped on 2026-06-11 02:12 HKT at the old P8 matrix blocker, then resumed on
2026-06-11 with a reviewed synthetic-truth P8 repair.

Passed gates:

- P0: `PASS_FILTER_BENCH_P0_CONTRACT`
- P1: `PASS_FILTER_BENCH_P1_TARGET_REGISTRY`
- P2: `PASS_FILTER_BENCH_P2_ADAPTER_PROTOCOL`
- P3: `PASS_FILTER_BENCH_P3_REFERENCE_ORACLES`
- P4: `PASS_FILTER_BENCH_P4_DETERMINISTIC_FILTERS`
- P5: `PASS_FILTER_BENCH_P5_DPF_FILTERS`
- P6: `PASS_FILTER_BENCH_P6_GRADIENT_SEMANTICS`
- P7: `PASS_FILTER_BENCH_P7_PREFLIGHT_MATRIX`
- P8 revised contract: `PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT`

Active blocked gates:

- P8 full numeric benchmark:
  `BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING`
- P9 handoff closeout:
  `BLOCK_FILTER_BENCH_P9_NUMERIC_BENCHMARK_PENDING`

P9 was attempted after the revised P8 contract pass and correctly blocked
Bayesian-estimation handoff because the full numeric synthetic-truth benchmark
has not yet run.

## Historical Blocker

The old P8 matrix gate blocked with:

```text
BLOCK_FILTER_BENCH_P8_RUNNER_MATRICES
```

Reason: no reviewed full numeric benchmark runner computed value and eligible
gradient errors for the frozen 7 algorithm by 12 model roster.  P8 emitted
complete structured JSON/CSV/Markdown matrices with reason-coded cells, but
numeric benchmark error fields remained null.  Promoting P4/P5 smoke fixtures
or P7 preflight status expansion to performance evidence would violate the
evidence contract.

Disposition: P8 criteria were explicitly revised under Claude review to the
synthetic-truth likelihood-geometry contract.

## Current Blocker

```text
BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING
BLOCK_FILTER_BENCH_P9_NUMERIC_BENCHMARK_PENDING
```

The revised P8 synthetic-truth contract is emitted and reviewed, but accepted
truth draws, synthetic datasets, horizon calibration, stochastic seed
calibration, and reviewed numeric evaluator outputs do not yet exist.  The
filtering benchmark therefore cannot be used as Bayesian-estimation handoff
evidence yet.

## Key Artifacts

- Runbook:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-gated-execution-runbook-2026-06-10.md`
- Execution ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md`
- Reviewed methodology:
  `docs/plans/bayesfilter-synthetic-truth-filter-benchmark-methodology-proposal-2026-06-11.md`
- Old P8 matrix result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-runner-matrices-result-2026-06-10.md`
- Revised P8 subplan:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-subplan-2026-06-11.md`
- Revised P8 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-synthetic-truth-runner-result-2026-06-11.md`
- Revised P8 contract JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json`
- Revised P8 capability crosswalk:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-capability-crosswalk-2026-06-11.md`
- Revised P8 emitter:
  `scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py`
- Revised P8 focused tests:
  `tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py`
- P9 closeout result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p9-closeout-result-2026-06-11.md`

## Last Validation

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py
status PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT
numeric_benchmark_status BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING

python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json
exited 0

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py
8 passed in 0.05s

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_emit_synthetic_truth.py tests/highdim/test_filtering_value_gradient_benchmark_synthetic_truth_p8.py
exited 0

git diff --check -- revised P8/P9 artifacts
exited 0
```

Claude execution review:

- Initial broad P8 execution review prompt produced no useful output.
- Small probe returned `PROBE_OK`; the review prompt was shortened.
- Contract/result review returned `VERDICT: AGREE`.
- Script/test review returned `VERDICT: AGREE`.

## Required Repair To Resume

Create a reviewed numeric synthetic-truth benchmark execution plan that uses
the revised P8 contract as its governing schema.

The next program must preserve:

- P7 frozen roster: 7 current algorithms by 12 model rows;
- old `ledh_pfpf_ot_historical` remains historical-only;
- P6 gradient semantics, especially DPF gradients as status-only unless a new
  reviewed gradient route is admitted;
- canonical `phi` derivative coordinates and chain-rule/Hessian transform
  policy;
- mandatory componentwise score artifact;
- tuple-level accepted-draw manifest for
  `(model_row_id, truth_draw_id, algorithm_id)`;
- MC uncertainty for stochastic DPF value cells;
- no proxy promotion from smoke/preflight fixtures to benchmark performance.

The next execution should generate accepted truth draws, synthetic datasets,
horizon calibration, stochastic seed calibration, and reviewed evaluator outputs
before any filtering closeout or Bayesian-estimation handoff is claimed.
