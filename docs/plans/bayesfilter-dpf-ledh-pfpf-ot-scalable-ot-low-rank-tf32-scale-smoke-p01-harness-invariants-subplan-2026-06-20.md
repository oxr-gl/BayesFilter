# LR-TF32-1 Subplan: Harness And Small Invariants

Date: 2026-06-20
Owner: peer agent

## Status

`P01_PASSED`

## Phase Objective

Implement a lane-owned scale-smoke diagnostic harness and focused tests that
validate the low-rank algorithm invariants on small fixtures before any medium
or GPU scale execution.

## Entry Conditions Inherited From Previous Phase

- P00 governance/review gate passed.
- Thresholds and non-claims are frozen.
- Low-rank solver-route implementation is the algorithm under test.
- Positive-feature artifacts are not evidence.

## Required Artifacts

- Diagnostic script:
  `docs/benchmarks/scalable_ot_low_rank_tf32_scale_smoke.py`
- Focused tests:
  `tests/test_low_rank_tf32_scale_smoke.py`
- Small invariant JSON/Markdown:
  `docs/benchmarks/scalable-ot-low-rank-tf32-scale-smoke-small-2026-06-20.json`
  and `.md`
  The JSON must include the top-level `run_manifest` object defined by the
  master program.
- P01 result/close record.

## Required Checks, Tests, And Reviews

- `python -m py_compile` for the diagnostic script and focused test.
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_low_rank_tf32_scale_smoke.py`
- CPU-hidden small diagnostic run with tiny materialized parity enabled:
  `B=2`, `N=32`, `D=4`, `rank=8`, `dtype=float64`,
  `fixture_id=bounded_smooth_v1`.
- JSON parse and schema/field checks.
- Local forbidden-claim/action scan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the new scale-smoke harness correctly exercise low-rank resampling invariants before any scale claim is attempted? |
| Baseline/comparator | Tiny materialized `Q diag(1/g) R^T` apply is a local invariant comparator only. |
| Primary pass criterion | Compile/test/small diagnostic all pass; JSON is valid and includes the embedded run manifest; hard vetoes are empty; the fixed small fixture has finite transported particles/factors, `Q,R >= 0`, `g > 0`, uniform log weights, residuals below thresholds, and tiny lazy/materialized parity below `1e-10`. |
| Veto diagnostics | Compile/test failure, invalid JSON, missing embedded run manifest, fixture mismatch, nonfinite factors/particles, negative factors, nonpositive `g`, residual/parity failure, dense materialization outside small mode, missing non-claims, or unsupported claim. |
| Explanatory diagnostics | Rank, projection iterations, factor minima, small fixture moment errors, runtime. Small-mode moment errors are recorded but are not P01 hard vetoes; downstream moment thresholds begin in LR-TF32-2 and LR-TF32-3. |
| Not concluded | No medium/large scale feasibility, GPU feasibility, TF32 help, speedup, ranking, readiness, or dense equivalence. |

## Forbidden Claims And Actions

- Do not attempt 50k/100k in this phase.
- Do not use GPU evidence.
- Do not compare against positive-feature.
- Do not materialize `[B,N,N]` except tiny invariant matrices.
- Do not change fixture scale, dimensions, rank, dtype, or thresholds after
  seeing results.

## Exact Next-Phase Handoff Conditions

Advance to LR-TF32-2 only if P01 checks pass, P01 result is written, P02
subplan is refreshed/reviewed, and no dense-materialization or invariant
blocker remains.

## Stop Conditions

Stop with `LOW_RANK_TF32_SCALE_HARNESS_BLOCKED` if the harness cannot validate
basic invariants without forbidden actions or if small invariants fail and
cannot be repaired inside lane-owned files.
