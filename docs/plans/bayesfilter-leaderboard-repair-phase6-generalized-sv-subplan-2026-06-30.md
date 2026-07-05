# Phase 6 subplan: generalized SV target and evaluator repair

Date: 2026-06-30

Status: `DRAFT_REVIEW_READY`

## Phase Objective

Repair generalized-SV leaderboard cells by first freezing a target contract, then wiring SGQF and Zhao-Cui value/score cells only where the target and derivative routes are reviewed.

## Entry Conditions Inherited From Previous Phase

- Phase 5 closed or precisely blocked SIR d18.
- Leaderboard schema distinguishes target status from value status and score status.
- Generalized-SV governed artifacts from 2026-06-29 are available for context only until revalidated against the current exact source-row contract.
- The active source row remains `zhao_cui_generalized_sv_synthetic_from_estimated_values`; native dense-oracle, precursor, auxiliary, actual-SV, and KSC-surrogate evidence are not source-row SGQF/Zhao-Cui admission evidence.

## Required Artifacts

- Generalized-SV target/evaluator contract.
- Exact source-row admission contract for each candidate cell, identifying the reviewed target, evaluator route, derivative route if any, and blocker semantics.
- Code/tests for SGQF and/or Zhao-Cui evaluator paths if implemented.
- Regenerated highdim leaderboard.
- Phase result:
  `docs/plans/bayesfilter-leaderboard-repair-phase6-generalized-sv-result-2026-06-30.md`
- Refreshed Phase 7 subplan.

## Required Checks, Tests, Reviews

- Target contract review before code execution.
- Finite value tests.
- Analytical score tests only if a strict derivative route exists.
- FD diagnostic and multi-replicate expected-score calibration if generated-data truth is available.
- Result artifact must record backend/context for every check and regeneration: CPU-only, trusted GPU/XLA, or document-only blocker closeout.
- Claude review of target contract and result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can generalized-SV cells be converted from generic blocked status to reviewed target/evaluator status? |
| Baseline/comparator | Exact source-row contract for `zhao_cui_generalized_sv_synthetic_from_estimated_values`: target definition, truth/test-point convention, evaluator route, and derivative route if any. Prior blocked rows and 2026-06-29 governed artifacts are context, not admission comparators. |
| Primary criterion | Each generalized-SV cell is either exact-row executed under a reviewed target/evaluator route, with strict derivative route reviewed before any score claim, or blocked with a precise missing target/evaluator/derivative item. Mere execution of a precursor, native oracle, auxiliary diagnostic, actual-SV route, or KSC route is not admission. |
| Veto diagnostics | Unsupported same-target claim; score without theta; tape/autodiff analytical score; nonfinite value; stale assumptions from older generalized-SV experiments. |
| Explanatory diagnostics | Value magnitude, score norm, FD residual, runtime. |
| Not concluded | No broad generalized-SV production readiness unless all separate gates pass. |
| Artifact | Target contract, leaderboard, Phase 6 result. |

## Forbidden Claims And Actions

- Do not use generalized-SV labels without specifying the exact target.
- Do not promote an auxiliary diagnostic row as a rankable leaderboard row.
- Do not use precursor, native-oracle, auxiliary, actual-SV, or KSC-surrogate evidence to satisfy SGQF or Zhao-Cui source-row admission for `zhao_cui_generalized_sv_synthetic_from_estimated_values`; such evidence may inform debugging only.
- Do not call a tape/autodiff score analytical.

## Exact Next-Phase Handoff Conditions

Advance to Phase 7 if:

- Generalized-SV rows have reviewed target/evaluator statuses.
- Remaining blockers identify missing target, value adapter, analytical score, or batch/GPU path separately.
- The Phase 6 result states whether the phase was document-only, CPU-only, trusted GPU/XLA, or mixed, so Phase 7 cannot overread environment readiness.

## Stop Conditions

Stop if:

- The target cannot be fixed without user product/scientific direction.
- Existing artifacts are too stale to support a safe target contract.
- Review finds unsupported claims that cannot be repaired.

## End-of-Subplan Protocol

1. Run required local checks.
2. Write Phase 6 result/close record.
3. Draft or refresh Phase 7 subplan.
4. Review Phase 7 subplan for benchmark and trusted GPU safety.
