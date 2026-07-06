# P01 Harness And Tuning-Grid Readiness Result

Date: 2026-06-22
Status: `PASS`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | P01 passed after local checks and Claude R5 convergence. |
| Primary criterion status | Passed. Harness exposes required knobs and diagnostics; wrapper dry-run records planned commands, planned row artifact paths, planned logs, grid parameters, TF32/GPU execution policy, and candidate-label schema. |
| Veto diagnostic status | No unresolved P01 veto remains. |
| Main uncertainty | P02 may reveal trusted GPU availability, actual row execution, or artifact schema issues. |
| Next justified action | Advance to P02 tiny actual-SIR mini-grid smoke precheck. |
| Not concluded | No tuning result, candidate viability, speedup, posterior correctness, HMC readiness, default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or GPU evidence. |

## Implementation

Added:

- `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`
- `tests/test_actual_sir_low_rank_tuning_grid.py`

The wrapper is orchestration only. It does not import TensorFlow, NumPy, the
actual-SIR harness, or the low-rank solver at module import. It enumerates
subprocess commands for `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py`
and aggregates row JSON when run in execution or aggregate-existing mode.

## Local Checks

| Check | Result |
| --- | --- |
| Existing harness focused test | `PASS`: `3 passed, 70 warnings` |
| Wrapper plus harness focused tests | `PASS`: initial `6 passed, 70 warnings`; after R1 repairs `9 passed, 70 warnings`; after R2 repairs `11 passed, 70 warnings`; after R3 repairs `15 passed, 70 warnings`; after R4 repairs `16 passed, 70 warnings` |
| Wrapper dry-run schema command | `PASS` |
| Wrapper py_compile | `PASS` |

## Dry-Run Artifact

- JSON:
  `docs/benchmarks/actual-sir-low-rank-tuning-p01-dry-run-grid-2026-06-22.json`
- Markdown:
  `docs/benchmarks/actual-sir-low-rank-tuning-p01-dry-run-grid-2026-06-22.md`
- Log:
  `docs/benchmarks/logs/actual-sir-low-rank-tuning-p01-dry-run-grid-2026-06-22.log`

Dry-run summary, which validates enumeration and schema only:

| Field | Value |
| --- | --- |
| Schema | `actual_sir_low_rank_tuning_grid.v1` |
| Status | `DRY_RUN` |
| Candidate count | `4` |
| Labels | `{'DRY_RUN': 4}` |

Dry-run does not verify actual row JSON/Markdown/log existence, TF32 runtime
state, GPU UUID, route execution, paired comparability, or factor diagnostics.
Those are checked only after execute/aggregate-existing modes ingest real row
artifacts.

## Claude R1 Repair Record

Claude R1 returned `VERDICT: REVISE` with these fixable findings:

- stale-row/environment mismatch risk from row paths and aggregate-existing
  trusting row JSON without request validation;
- missing structured veto for missing/corrupt row JSON or missing row Markdown;
- provenance-complete logic was too weak for GPU/TF32 evidence;
- `freeze-eligible` label was too optimistic and blurred nomination/support;
- aggregate summary did not inline enough review-critical classification fields;
- P01 dry-run wording overstated what dry-run proved;
- P02 said "tiny row" while the handoff command is a four-candidate mini-grid.

Repairs applied:

- row paths now include seed list, route, transport policy, dtype, TF32 mode,
  device scope, and CUDA token;
- aggregate-existing and execute mode validate row JSON/Markdown existence,
  JSON parseability, and row request identity before aggregation;
- missing/corrupt/mismatched artifacts become structured hard-veto rows instead
  of crashes or silent reuse;
- GPU/TF32 provenance is separated from basic low-rank provenance, and CPU-hidden
  rows cannot be `freeze-nominated`;
- labels now distinguish `freeze-nominated`, `comparable-but-slow`,
  `schema-valid-nonpromotional`, `faster-but-incomparable`, and hard vetoes;
- inline classification records paired delta summaries, route-fired count,
  factor residual, selected GPU, and precision payload;
- P01 and P02 wording now state dry-run/mini-grid limits.

Focused local checks after repair:

- `tests/test_actual_sir_low_rank_tuning_grid.py`
- `tests/test_actual_sir_low_rank_route_validation.py`
- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`
- wrapper dry-run schema command

## Claude R2 Repair Record

Claude R2 returned `VERDICT: REVISE` with two remaining wrapper findings:

- request identity still omitted `streaming_timing_source`, Sinkhorn settings,
  annealing settings, and chunk sizes;
- top-level aggregate status did not fail for `CORRUPT`, `MISMATCH`, or
  `TIMEOUT` structured hard-veto rows.

Repairs applied:

- row paths and request signatures now include streaming timing source,
  Sinkhorn iterations/epsilon, annealing scaling/threshold, and row/column/
  particle chunk sizes;
- aggregate-existing validates those fields against row artifacts where the
  harness records them and validates chunk sizes against the row command string;
- top-level status now fails for any row status outside the expected pass set
  for the current mode;
- regression tests cover request drift and corrupt-artifact failure propagation.

Focused local checks after R2 repair:

- `tests/test_actual_sir_low_rank_tuning_grid.py`
- `tests/test_actual_sir_low_rank_route_validation.py`
- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`
- wrapper dry-run schema command

## Claude R3 Repair Record

Claude R3 returned `VERDICT: REVISE` with four focused findings:

- timing-source validation was asymmetric and only checked `compiled_core`;
- streaming-only aggregate-existing artifacts were rejected because low-rank row
  validation was unconditional;
- tests did not cover `row_json_missing`, execute-mode `TIMEOUT`, or
  execute-mode `ERROR`;
- P02 still had one singular "Tiny row" pass-criterion phrase.

Repairs applied:

- timing-source validation now checks any streaming row against the requested
  timing source;
- low-rank row validation is required only for `both` and `low_rank` requests;
- regression tests cover missing JSON, nonzero subprocess exit, timeout, and
  streaming-only aggregate-existing behavior;
- P02 pass criterion now says "tiny mini-grid."

Focused local checks after R3 repair:

- `tests/test_actual_sir_low_rank_tuning_grid.py`
- `tests/test_actual_sir_low_rank_route_validation.py`
- wrapper dry-run schema command

## Claude R4 Repair Record

Claude R4 returned `VERDICT: REVISE` with one remaining wrapper finding:

- request validation required low-rank rows for `both`/`low_rank`, but did not
  require a streaming row for `both`/`streaming` artifacts.

Repairs applied:

- streaming row validation is now required for `both` and `streaming` requests;
- regression test covers a streaming request whose artifact has no streaming
  row.

Focused local checks after R4 repair:

- `tests/test_actual_sir_low_rank_tuning_grid.py`
- `tests/test_actual_sir_low_rank_route_validation.py`
- `python -m py_compile docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`
- wrapper dry-run schema command

## Claude R5 Closeout

Claude R5 returned `VERDICT: AGREE`. P01 may advance to P02.

## Handoff Decision

P02 should use the wrapper in `execute` mode for a four-candidate tiny
actual-SIR mini-grid smoke:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --num-particles 128 \
  --time-steps 3 \
  --batch-seeds 81120 \
  --low-rank-ranks 16,32 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --warmups 0 \
  --repeats 1 \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --tf32-mode enabled \
  --output docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22.md \
  --quiet
```

If trusted GPU is unavailable or busy, P02 must either use GPU0 with recorded
physical UUID or stop for human direction; CPU-hidden execution may debug schema
only and cannot support GPU evidence.

## Required Review

Because P01 added a wrapper, Claude read-only review is required before P01 can
advance to P02.
