# LR-TF32-1 Result: Harness And Small Invariants

Date: 2026-06-20
Owner: peer agent
Supervisor/executor: Codex

## Status

`PASSED`

## Phase Objective

Implement and validate the lane-owned low-rank scale-smoke harness on the
frozen small fixture before any medium or GPU scale execution.

## Required Artifacts

- Diagnostic script:
  `docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py`
- Focused tests:
  `tests/test_low_rank_tf32_scale_smoke.py`
- Small invariant JSON:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.json`
- Small invariant Markdown:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.md`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | The harness exercises low-rank resampling invariants on the fixed small fixture before scale claims. |
| Baseline/comparator | Tiny materialized `Q diag(1/g) R^T` apply was used only as a local invariant comparator. |
| Primary criterion | Passed: compile/test/small diagnostic all passed; JSON is valid; hard vetoes are empty; factors/particles are finite; `Q,R >= 0`; `g > 0`; uniform output log weights normalize; factor/induced residuals pass; tiny lazy/materialized parity is below `1e-10`. |
| Veto diagnostics | No active P01 veto. |
| Explanatory diagnostics | Small-mode weighted second-moment absolute error is `2.8594539075338404e-01`; runtime/memory/TF32 metadata are explanatory only. |
| Not concluded | No medium/large scale feasibility, GPU feasibility, TF32 help, speedup, ranking, readiness, or dense equivalence. |

## Commands Run

- `python -m py_compile docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py tests/test_low_rank_tf32_scale_smoke.py`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_low_rank_tf32_scale_smoke.py`
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py --mode small --output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.md`
- `python -m json.tool docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.json`

## Diagnostic Summary

| Diagnostic | Value | Role |
| --- | ---: | --- |
| status | `PASS` | hard gate |
| hard vetoes | `[]` | hard gate |
| max factor marginal residual | `2.6095782496710074e-08` | hard veto |
| max induced row residual | `8.350650400057447e-07` | hard veto |
| max induced column residual | `8.034103933240999e-07` | hard veto |
| output log-weight normalization residual | `0.0` | hard veto |
| tiny materialized apply parity | `1.6653345369377348e-16` | hard veto |
| weighted mean absolute error | `6.994832352918978e-08` | explanatory in P01 |
| weighted second-moment absolute error | `2.8594539075338404e-01` | explanatory in P01; hard veto begins in P02/P03 |

## Repair Record

Initial focused tests failed because the harness incorrectly applied downstream
second-moment thresholds as a P01 small-invariant hard gate.  The P01 subplan
classifies small fixture moment errors as explanatory, so the harness was
patched to enforce moment thresholds only in LR-TF32-2 and LR-TF32-3 while
still recording P01 moment errors.  Focused checks were rerun and passed.

## Next-Phase Handoff

LR-TF32-2 may start because:

- P01 required checks passed;
- P01 JSON/Markdown artifacts exist and include an embedded run manifest;
- small dense materialization was confined to the tiny invariant check;
- no P01 invariant blocker remains;
- P02 subplan is refreshed and explicitly treats moment thresholds as hard
  vetoes at the fixed medium CPU screen.

## Stop Conditions

No P01 stop condition is active.
