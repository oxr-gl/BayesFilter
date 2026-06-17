# Phase 1 Result: Baseline Fixture Contract

Date: 2026-06-17

## Status

`PHASE_1_BASELINE_FIXTURE_PASSED`

## Phase Objective

Define deterministic transport fixtures and record dense/streaming baseline
diagnostics from the current TensorFlow FilterFlow-style annealed transport.
These baseline artifacts are the comparator for later scalable OT candidates.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Is the current TensorFlow dense/streaming annealed transport baseline deterministic and diagnostically rich enough to compare scalable OT candidates? |
| Baseline/comparator | `annealed_transport_tf.py` dense mode and streaming mode. |
| Primary criterion | Passed: baseline fixtures wrote JSON/Markdown artifacts with finite dense and streaming transported particles, deterministic metadata, residuals, and dense-vs-streaming comparison. |
| Veto diagnostics | No hard veto fired. |
| Explanatory diagnostics | Runtime, row/column residuals, transported-particle norm/error, cost scale, and iteration count were recorded. |
| Not concluded | No scalable candidate correctness, no speedup, no posterior validity, no production default, no statistically supported ranking, no GPU performance claim. |
| Artifact preserving result | Fixture spec, JSON diagnostics, Markdown summary, log, targeted pytest log, this result, and ledger entry. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `70ab32644cedeb95d4b56e096448f3bb2c908763` |
| Timestamp | `2026-06-17T16:00:47+08:00` |
| Environment | CPU-only TensorFlow diagnostic; `CUDA_VISIBLE_DEVICES=-1` |
| TensorFlow | `2.20.0` |
| Diagnostic command | `timeout 240 python docs/benchmarks/scalable_ot_p01_baseline_fixture_diagnostics.py --device-scope cpu --output docs/benchmarks/scalable-ot-p01-baseline-fixture-diagnostics-2026-06-17.json --markdown-output docs/benchmarks/scalable-ot-p01-baseline-fixture-diagnostics-2026-06-17.md` |
| Diagnostic log | `docs/benchmarks/scalable-ot-p01-baseline-fixture-diagnostics-2026-06-17.log` |
| Targeted pytest command | `CUDA_VISIBLE_DEVICES=-1 timeout 180 pytest -q tests/test_experimental_batched_ledh_pfpf_ot_tf.py::test_batched_annealed_transport_streaming_matches_dense_without_matrix tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py::test_streaming_transport_returns_no_dense_transport_matrix` |
| Targeted pytest log | `docs/benchmarks/scalable-ot-p01-targeted-pytest-2026-06-17.log` |

## Required Artifacts

| Artifact | Status |
| --- | --- |
| Fixture spec | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-spec-2026-06-17.md` |
| Baseline diagnostic JSON | `PASS`: `docs/benchmarks/scalable-ot-p01-baseline-fixture-diagnostics-2026-06-17.json` |
| Baseline diagnostic Markdown | `PASS`: `docs/benchmarks/scalable-ot-p01-baseline-fixture-diagnostics-2026-06-17.md` |
| Baseline diagnostic log | `PASS`: `docs/benchmarks/scalable-ot-p01-baseline-fixture-diagnostics-2026-06-17.log` |
| Targeted pytest log | `PASS`: `docs/benchmarks/scalable-ot-p01-targeted-pytest-2026-06-17.log` |
| Phase 2 subplan | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-candidate-audit-notes-subplan-2026-06-17.md` |

## Fixture Summary

| Fixture | Dense finite | Streaming finite | Dense row residual | Dense column residual | Max dense-streaming particle error |
| --- | --- | --- | --- | --- | --- |
| `tiny_manual` | `True` | `True` | `1.257253e-02` | `4.440892e-16` | `1.110223e-16` |
| `small_parity` | `True` | `True` | `1.875914e-02` | `6.661338e-16` | `1.665335e-16` |
| `high_dim_low_rank` | `True` | `True` | `3.468684e-04` | `2.220446e-15` | `4.440892e-16` |
| `high_dim_locality` | `True` | `True` | `1.283582e-03` | `1.554312e-15` | `2.498002e-16` |

Streaming mode intentionally records `not_materialized_reason =
streaming_no_dense_matrix` rather than returning a dense plan.  Dense mode is
the materialized reference for later candidate checks.

## Local Check Result

| Check | Status | Notes |
| --- | --- | --- |
| Diagnostic script syntax | `PASS` | `python -m py_compile docs/benchmarks/scalable_ot_p01_baseline_fixture_diagnostics.py` |
| Diagnostic JSON gate | `PASS` | Status `PASS`; hard vetoes `[]`. |
| Targeted pytest | `PASS` | `2 passed`; TensorFlow/AutoGraph deprecation warnings only. |
| Phase 2 subplan structure | `PASS` | Required sections and boundaries are present. |

The diagnostic log contains a CUDA initialization warning despite CPU-only
configuration.  Because `CUDA_VISIBLE_DEVICES=-1` was set and this phase makes
no GPU claim, this is recorded as environment noise, not GPU evidence.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PHASE_1_BASELINE_FIXTURE_PASSED` | Dense and streaming baseline fixtures emitted finite diagnostics and JSON/MD artifacts. | No hard veto fired. | Candidate audit notes may still find paper-code mismatches or blocked source lanes. | Begin Phase 2 candidate audit notes. | No candidate correctness, no speedup, no ranking, no production readiness. |

## Post-Run Red Team

Strongest alternative explanation: the chosen fixtures may be too small or too
structured to expose all baseline weaknesses.  Later phases must not infer
large-scale performance or candidate viability from this Phase 1 baseline gate.

What would overturn this phase decision: a later reproducibility check finds
these fixtures are nondeterministic, or dense-vs-streaming parity fails after a
baseline code change.

Weakest evidence link: runtime differences in this phase are descriptive only
and not optimized; streaming is much slower on these tiny CPU chunked fixtures,
which says nothing about eventual GPU or large-memory behavior.

## Exact Phase 2 Handoff

Phase 2 may begin because:

- this result records `PHASE_1_BASELINE_FIXTURE_PASSED`;
- fixture spec, JSON diagnostics, Markdown summary, and logs exist;
- dense baseline outputs exist for all required fixtures;
- streaming diagnostics are recorded with explicit non-materialization reason;
- local checks passed;
- Phase 2 candidate-audit-notes subplan exists and has been locally reviewed for
  consistency, correctness, feasibility, artifact coverage, and boundary safety;
- no human-required stop condition is active.
