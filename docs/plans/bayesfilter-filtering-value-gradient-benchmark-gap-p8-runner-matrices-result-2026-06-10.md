# P8 Result: Benchmark Runner And Matrix Emission

metadata_date: 2026-06-10
phase: FILTER_BENCH_P8
status: BLOCK_FILTER_BENCH_P8_RUNNER_MATRICES
supervisor: Codex
reviewer: Claude Code read-only

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can the benchmark produce full value and gradient comparison matrices with no unexplained holes? |
| Baseline/comparator | P7 preflight matrix and P1-P6 registry, adapter, reference, coverage, and gradient-semantics artifacts. |
| Primary criterion | Blocked honestly: structured matrices are complete against the 7 x 12 frozen roster, but no reviewed full numeric benchmark runner exists for every cell. |
| Veto diagnostics | Veto fired: using P4/P5 smoke fixtures or P7 preflight as benchmark evidence would proxy-promote wiring/status data into performance evidence. |
| Nonclaims | P8 output is not a filter ranking, does not contain full numeric benchmark errors, does not certify DPF gradients, and does not claim HMC/GPU/Bayesian-estimation readiness. |

## Artifacts

- Emission command: `scripts/filtering_value_gradient_benchmark_emit_matrices.py`
- Structured matrix JSON: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json`
- Value matrix CSV: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-value-error-matrix-2026-06-10.csv`
- Gradient matrix CSV: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-gradient-error-matrix-2026-06-10.csv`
- Value matrix Markdown: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-value-error-matrix-2026-06-10.md`
- Gradient matrix Markdown: `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-gradient-error-matrix-2026-06-10.md`
- Focused validation test: `tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py`

## Blocker

`BLOCK_FILTER_BENCH_P8_RUNNER_MATRICES`

Claude read-only review iteration 1 agreed with this blocker:

```text
VERDICT: AGREE
MAJOR:
- None.
MINOR:
- None.
```

Reason: no reviewed full numeric benchmark runner currently computes value and
eligible gradient errors for the full frozen 7 algorithm by 12 model roster.
The emitted matrices are complete and reason-coded, but numeric error fields
remain null because promoting smoke/preflight fixtures would violate the
evidence contract.

Required repair: implement actual per-cell numeric benchmark adapters for the
frozen roster, or explicitly revise P8's criterion before claiming benchmark
performance.

## Validation

Commands planned/run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_matrices.py
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json >/dev/null
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_emit_matrices.py tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py
git diff --check -- scripts/filtering_value_gradient_benchmark_emit_matrices.py tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-value-error-matrix-2026-06-10.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-gradient-error-matrix-2026-06-10.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-value-error-matrix-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-gradient-error-matrix-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-runner-matrices-result-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md
```

Results:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_matrices.py
wrote docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json
status BLOCK_FILTER_BENCH_P8_RUNNER_MATRICES

python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json
exited 0

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py
6 passed in 0.03s

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_emit_matrices.py tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py
exited 0

git diff --check -- scripts/filtering_value_gradient_benchmark_emit_matrices.py tests/highdim/test_filtering_value_gradient_benchmark_runner_matrices.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-value-error-matrix-2026-06-10.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-gradient-error-matrix-2026-06-10.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-value-error-matrix-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-gradient-error-matrix-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-runner-matrices-result-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-execution-ledger-2026-06-10.md
exited 0
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; P8 artifacts uncommitted |
| Dirty-state summary | dirty worktree preserved; unrelated changes not reverted |
| Command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_matrices.py` |
| Environment | local Python environment |
| Conda env | N/A |
| CPU/GPU status | CPU-only; no GPU conclusion |
| dtype | Manifest-level only; per-row dtype lives in P1 registry |
| Seeds | Smoke payload seeds retained only as non-performance diagnostics |
| Wall time | local validation completed by 2026-06-11 02:11 HKT |
| Plan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-runner-matrices-subplan-2026-06-10.md` |
| Result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-runner-matrices-result-2026-06-10.md` |
| Output JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Block P8 | Complete structured matrices emitted, but numeric benchmark errors are not available for the frozen roster | Proxy promotion veto fired for smoke/preflight data | Whether to implement missing numeric adapters now or treat this as a future benchmark-run task | Ask Claude read-only reviewer to verify the block is valid and not hiding a fixable same-turn issue | Filter ranking, value/gradient performance, DPF gradient certification, Bayesian-estimation readiness |

## Post-Run Red-Team Note

- Strongest alternative explanation: the complete-looking matrices may be
  mistaken for performance matrices even though all numeric errors are null.
- What would overturn the blocker: a reviewed command that computes actual
  value and eligible gradient errors for the frozen roster, with MC uncertainty
  for stochastic DPF rows and no proxy promotion.
- Weakest part of evidence: P8 currently emits matrix structure and statuses,
  not full benchmark numerical results.

Required token:

`BLOCK_FILTER_BENCH_P8_RUNNER_MATRICES`
