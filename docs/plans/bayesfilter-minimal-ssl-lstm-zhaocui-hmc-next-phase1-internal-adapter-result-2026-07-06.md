# Phase 1 Result: Internal Reusable Adapter Surface

Date: 2026-07-06

Status: `COMPLETE`

## Phase Objective

Extract the benchmark-only `MinimalZhaoCuiHMCTargetAdapter` and minimal fixture
helpers into a reusable internal BayesFilter module while preserving the
completed ladder behavior and evidence boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the minimal scalar `zhaocui_fixed` HMC target adapter be moved from benchmark-only code into an internal module without behavior drift or evidence inflation? |
| Baseline/comparator | Existing benchmark adapter behavior and existing ladder tests/artifacts. |
| Primary pass criterion | Focused tests and existing ladder tests pass CPU-hidden, immutable predecessor comparator passes or records a justified non-behavioral schema repair, forbidden-token scan has no target-path hits, benchmark harness consumes the internal module, and artifacts/nonclaims remain unchanged or stricter. |
| Veto diagnostics | Nonfinite value/score, shape drift, unexplained value/score/signature drift, target-path NumPy/autodiff bridge, new Zhao-Cui route choice without classification/anchors/approval, public API export, default-policy change, failed tests, invalid artifact role, or unsupported claim. |
| Explanatory diagnostics | Code diff, score norm/log probability equality, runtime, adapter metadata, and dirty-worktree summary. |
| Not concluded | GPU/XLA behavior, HMC convergence, posterior correctness, ranking, source-faithful parity, public API/package readiness, default readiness, or LEDH result. |

## Implementation Summary

Created internal module:

- `bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py`

The module contains:

- `MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS`
- `MinimalZhaoCuiHMCTargetAdapter`
- frozen minimal fixture helpers
- deterministic initial-state helper
- JSON-ready fixture payload helper

Updated benchmark harness:

- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py`

Added tests:

- `tests/test_ssl_lstm_zhaocui_hmc_minimal.py`

No top-level package exports were added.

## Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Compile | `PASSED` | Internal module, benchmark harness, new tests, and existing ladder tests compiled. |
| Focused pytest | `PASSED` | `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 pytest -q tests/test_ssl_lstm_zhaocui_hmc_minimal.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py` returned `12 passed`. |
| Forbidden-token scan | `PASSED` | `rg -n "GradientTape|tf\\.py_function|import numpy|np\\." bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py` returned no matches. |
| Focused `git diff --check` | `PASSED` | No whitespace errors in Phase 1 code/test diff. |
| Public export scan | `PASSED` | New module imported directly only by benchmark/tests; not added to `bayesfilter/__init__.py` or `bayesfilter/nonlinear/__init__.py`. |

## Immutable Predecessor Comparator

Pre-extraction snapshot:

- `/tmp/bayesfilter_phase1_pre_extraction.json`

Post-extraction snapshot:

- `/tmp/bayesfilter_phase1_post_extraction_final.json`

Semantic comparator:

| Field group | Status |
| --- | --- |
| schema version | `MATCHED` |
| artifact role and filter name | `MATCHED` |
| fixture dimensions and values | `MATCHED` |
| `log_prob` | `MATCHED` |
| score norm/min/max | `MATCHED` |
| scalar score shape `(24,)` | `MATCHED` |
| batch score shape `(2, 24)` | `MATCHED` |
| capability authority/backend/scope/nonclaims | `MATCHED` |
| adapter signature | `MATCHED` |
| gradient path and value-score authority | `MATCHED` |
| top-level nonclaims | `MATCHED` |
| `zhaocui_fixed` manifest | `MATCHED` |

Comparator summary:

- `semantic_keys_checked`: 19
- `mismatch_count`: 0

Raw artifact diff showed only command path, timestamp, wall/runtime, and dirty
preview differences.

## Boundary Classification

| Boundary | Status |
| --- | --- |
| Mechanical extraction only | `PASSED` |
| New Zhao-Cui route choice | `NOT_INTRODUCED` |
| Public API/default-policy change | `NOT_INTRODUCED` |
| GPU/CUDA/XLA command | `NOT_RUN` |
| Long sampler diagnostics | `NOT_RUN` |
| Source-faithful parity claim | `NOT_CLAIMED` |

## Review Record

External Claude review remained denied for private-context transfer risk. A
fresh visible Codex substitute implementation review returned `VERDICT: AGREE`.

Review findings:

- Mechanical extraction preserved.
- Predecessor guard is sufficient for the Phase 1 boundary.
- Module remains internal and non-public.
- No target-path `import numpy`, `np.`, `tf.py_function`, or `GradientTape`
  appeared in the reviewed module/harness.
- Phase 2 CPU regression subplan is executable and boundary-safe.

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `PASS_PHASE1_ADVANCE_TO_PHASE2` |
| Primary criterion status | `PASSED` |
| Veto diagnostic status | `NO_PHASE1_HARD_VETO_OBSERVED` |
| Main uncertainty | Evidence remains CPU-hidden extraction/mechanics evidence only. |
| Next justified action | Execute Phase 2 CPU regression through the internal surface. |
| What is not being concluded | GPU/XLA behavior, HMC convergence, posterior correctness, ranking, source-faithful parity, public API/package readiness, default readiness, or LEDH result. |
