# Phase 6 Result: Shared Benchmark Runner And Invariant Metrics

Date: 2026-07-04

Status: `PASSED_WITH_LOCAL_CHECKS`

## Phase Objective

Create the shared SSL-LSTM benchmark runner and invariant metric suite used to
evaluate admitted filter adapters under the same data, priors, runtime, and
evidence classification.

## Entry Conditions

- Phase 5 recorded `fixed_sgqf` and `svd_ukf` as locally admitted, with
  `zhaocui_fixed` blocked by missing SSL-LSTM implementation and
  `ledh_streaming_ot` blocked by missing manual VJP streaming-OT score path.
- The shared value/score protocol and artifact schema from Phase 2 remain
  active.
- Parameter-by-parameter matching is not the primary criterion.

## Implementation Summary

Added `docs/benchmarks/benchmark_ssl_lstm_filter_hmc_phase6.py`.

The runner:

- builds one deterministic synthetic SSL-LSTM fixture;
- evaluates admitted `fixed_sgqf` and `svd_ukf` lanes only;
- records blocked `zhaocui_fixed` and `ledh_streaming_ot` rows as status-only;
- emits invariant metrics and target-scope provenance;
- keeps `heldout_predictive_log_score` as a filter-likelihood proxy, not a
  ranking claim;
- preserves a top-level nonclaim that parameter matching is not primary.

Added/updated `tests/test_ssl_lstm_phase6_benchmark.py`.

Updated `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase6-benchmark-runner-invariant-metrics-subplan-2026-07-04.md`
to match the implemented benchmark semantics.

## Smoke Artifact

- JSON: `docs/benchmarks/ssl_lstm_filter_hmc_phase6_shared_benchmark_cpu_hidden_2026-07-04.json`
- Markdown: `docs/benchmarks/ssl_lstm_filter_hmc_phase6_shared_benchmark_cpu_hidden_2026-07-04.md`

Key smoke fields:

| Field | Value |
| --- | --- |
| Status | `PHASE6_SHARED_BENCHMARK_READY` |
| Parameter matching primary criterion | `false` |
| Score finite for admitted filters | `true` |
| Admitted filters | `fixed_sgqf`, `svd_ukf` |
| Blocked filters | `zhaocui_fixed`, `ledh_streaming_ot` |
| Device scope | `cpu` |
| Device | `/CPU:0` |
| GPU trust basis | `cpu_hidden_debug` |

## Required Checks Run

| Check | Command | Result |
| --- | --- | --- |
| Syntax/compile check | `python -m compileall -q docs/benchmarks/benchmark_ssl_lstm_filter_hmc_phase6.py tests/test_ssl_lstm_phase6_benchmark.py` | Passed |
| Protocol + adapter + Phase 6 suite | `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 pytest -q tests/test_ssl_lstm_protocol.py tests/test_ssl_lstm_sgqf_ukf_adapters.py tests/test_ssl_lstm_phase6_benchmark.py` | Passed: 19 tests |
| Phase 6 smoke run | `timeout 240 python docs/benchmarks/benchmark_ssl_lstm_filter_hmc_phase6.py ...` | Passed; wrote JSON and Markdown artifacts |

## Skeptical Plan Audit

| Risk | Phase 6 finding |
| --- | --- |
| Wrong baseline | The runner uses one shared deterministic SSL-LSTM fixture and the Phase 2 protocol. |
| Proxy promotion | Heldout predictive log score is explicitly a proxy, not a ranking claim. |
| Missing stop conditions | Blocked Zhao-Cui and LEDH remain status-only rows and were not run. |
| Unfair comparison | Admitted filters share the same data, split, runtime, and artifact schema. |
| Hidden assumptions | Parameter matching stays non-primary; target-scope provenance is explicit. |
| Stale context | Phase 5 blocker statuses were carried forward unchanged. |
| Environment mismatch | CPU-hidden smoke is labeled debug/reference, not production GPU evidence. |
| Artifact mismatch | The smoke JSON/Markdown now answer the benchmark question directly. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Phase 6 shared benchmark gate | Passed | No schema, provenance, or test veto fired | HMC mechanics and longer-chain evidence remain future work | Refresh Phase 7 and proceed to HMC evidence ladder planning | No estimation success, no method ranking, no HMC convergence, no default readiness |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for admitted filters; blocked rows remained status-only |
| Statistically supported ranking | Not applicable |
| Descriptive-only differences | The two admitted filters are close descriptively, but no ranking is claimed |
| Default-readiness | Not checked and not claimed |
| Next evidence needed | Phase 7 HMC mechanics and evidence ladder |

## Phase 7 Subplan Review

Phase 7 was refreshed to inherit the Phase 6 benchmark output and proceed with
HMC hard-veto classification only. It must not rank candidates by descriptive
metrics alone.

## Phase 6 Gate Status

`PASSED_WITH_LOCAL_CHECKS`
