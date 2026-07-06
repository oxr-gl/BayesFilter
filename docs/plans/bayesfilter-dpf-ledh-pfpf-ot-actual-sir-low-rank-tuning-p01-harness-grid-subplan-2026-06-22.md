# P01 Harness And Tuning-Grid Readiness Subplan

Status: `DRAFT_AFTER_P00`

## Phase Objective

Verify that the existing actual-SIR validation harness can support tuning-grid
execution, aggregate artifacts, and candidate nomination without changing public
APIs or low-rank solver internals.

## Entry Conditions Inherited From Previous Phase

P00 must pass. The master program, runbook, ledgers, and Claude review protocol
must be converged. No GPU benchmark evidence has been produced yet.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p01-harness-grid-result-2026-06-22.md`
- Optional wrapper, only if needed:
  `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`
- Optional focused test, only if wrapper is added:
  `tests/test_actual_sir_low_rank_tuning_grid.py`
- Local check log:
  `docs/benchmarks/logs/actual-sir-low-rank-tuning-p01-local-checks-2026-06-22.log`

## Required Checks/Tests/Reviews

- Inspect the current harness CLI for all exposed low-rank knobs.
- Run CPU-hidden focused tests for the existing harness:
  `env CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest tests/test_actual_sir_low_rank_route_validation.py -q`
- If a wrapper is added, run its focused tests and a dry-run/schema check.
- Claude read-only review is required if P01 implements or repairs a wrapper.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the existing harness or a minimal wrapper execute a tuning grid and preserve enough evidence for candidate nomination? |
| Baseline/comparator | Existing validation harness with compiled streaming comparator support. |
| Primary pass criterion | Harness exposes all required knobs, local tests pass, and artifact schema can record per-row parameters, hard vetoes, paired metrics, route-fired counts, TF32 provenance, and GPU provenance. |
| Veto diagnostics | Missing knob, missing route-fired/factor/provenance diagnostics, local test failure, wrapper schema gap, or required public/shared API change. |
| Explanatory diagnostics | Test runtime, wrapper dry-run row count, and observed artifact fields. |
| Not concluded | No tuning result, candidate viability, speedup, posterior correctness, or GPU evidence. |
| Artifact | P01 result and local check log. |

## Forbidden Claims/Actions

- Do not change the low-rank solver route.
- Do not change public exports, defaults, package metadata, or shared schemas.
- Do not use GPU evidence from P01 for tuning or promotion.
- Do not treat a wrapper dry run as actual-SIR tuning evidence.

## Exact Next-Phase Handoff Conditions

Advance to P02 only if P01 records either:

- direct repeated harness invocation is sufficient and artifact paths are
  enumerated; or
- a minimal wrapper exists, tests pass, and schema coverage is documented.

## Stop Conditions

- `BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED` if grid evidence requires public API
  or shared schema changes.
- Stop if harness diagnostics cannot identify hard vetoes and paired metrics.
- Stop after five unresolved Claude review rounds for a material P01 blocker.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the P01 phase result.
3. Draft or refresh P02 with exact smoke commands/artifacts.
4. Review P02 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
