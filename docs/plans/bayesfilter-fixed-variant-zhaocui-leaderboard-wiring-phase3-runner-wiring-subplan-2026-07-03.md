# Phase 3 Subplan: Runner Wiring And Guards

Date: 2026-07-03

Status: `READY_EXECUTED_PHASE3_RESULT_WRITTEN`

## Phase Objective

Patch the highdim leaderboard runner and focused tests so the SIR Zhao-Cui row
uses the Phase 2 fixed-variant scope and cannot accidentally select the demoted
retained-grid route as production evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 2 has emitted a reviewed row-scope verdict.

Phase 2 verdict to implement:

- add/report `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`
  as `scoped_component_row_admitted`;
- declared scope is local complete-data/component value and analytical/manual
  score, not full observed-data/filtering likelihood;
- preserve `zhao_cui_spatial_sir_austria_j9_T20` as fixed/no-free-theta
  source-parity evidence and do not mutate it into the parameterized row;
- require explicit `target_scope` metadata because the row id encodes the
  parameterization but not the local-complete-data/component boundary;
- do not select the demoted retained-grid route.

## Required Artifacts

- Code changes in `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
  if Phase 2 admits or reclassifies a row.
- Focused tests in `tests/test_two_lane_highdim_leaderboard_*.py`.
- Phase 3 result:
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase3-runner-wiring-result-2026-07-03.md`

## Required Checks / Tests / Reviews

- `git diff --check` on touched code/tests/docs.
- CPU-only focused tests for changed leaderboard behavior.
- No GPU tests unless Phase 2 requires new GPU evidence.
- Claude read-only review required if code changes alter row admission status.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does runner code select/report the fixed-variant scope and exclude retained-grid production admission? |
| Baseline/comparator | Phase 2 row contract and current runner behavior. |
| Primary criterion | Focused tests prove row id, route role, score provenance, scope, and retained-grid exclusion fields are emitted as contracted. |
| Veto diagnostics | Autodiff/FD admitted; retained-grid route selected; stale fixed/no-free-theta row promoted; value/score nonfinite; tests only check strings without exercising row builder. |
| Explanatory diagnostics | Runtime and sidecar evidence paths. |
| Not concluded | No final leaderboard regeneration, no full filtering derivative closure unless explicitly tested. |
| Artifact | Phase 3 result plus code/test diff. |

## Forbidden Claims / Actions

- Do not change unrelated rows.
- Do not relax analytical-score admission.
- Do not remove historical blocker records.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only if focused tests pass and Phase 3 result records the
exact row behavior.

## Stop Conditions

- Runner cannot express Phase 2 scope without schema redesign.
- Focused tests fail for a non-mechanical reason.
- Fix would require changing owner-directed scientific target.

## End-Of-Subplan Protocol

1. Run required local checks.
2. Write Phase 3 result / close record.
3. Draft or refresh Phase 4 subplan.
4. Review Phase 4 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
