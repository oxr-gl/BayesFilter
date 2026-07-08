# Phase 4 Subplan: Regeneration And Validation

Date: 2026-07-03

Status: `SCOPED_ROW_VALIDATED_FULL_REGEN_BLOCKED`

## Phase Objective

Regenerate the highdim leaderboard JSON/MD and validate that the fixed-variant
Zhao-Cui SIR row is reported according to the reviewed contract.

## Entry Conditions Inherited From Previous Phase

- Phase 3 focused runner tests passed.
- Code changes, if any, are recorded in the Phase 3 result.

## Required Artifacts

- Regenerated leaderboard JSON/MD under `docs/plans`.
- Phase 4 result:
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase4-regeneration-validation-result-2026-07-03.md`

## Required Checks / Tests / Reviews

- CPU-only leaderboard runner command with explicit output path.
- JSON syntax validation.
- Focused tests covering generated artifacts.
- `git diff --check` on changed artifacts.
- Claude read-only review if generated artifacts change row admission status.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do regenerated leaderboard artifacts preserve the fixed-variant row contract? |
| Baseline/comparator | Phase 3 runner behavior and previous July leaderboard artifacts. |
| Primary criterion | JSON and MD contain the contracted row fields and no retained-grid production admission. |
| Veto diagnostics | Missing row, stale row id, missing score provenance, retained-grid route admitted, malformed JSON/MD, or unsupported readiness claim. |
| Explanatory diagnostics | Runtime and row summary differences. |
| Not concluded | No new GPU result unless a trusted GPU command is explicitly run; no posterior correctness. |
| Artifact | Regenerated JSON/MD and Phase 4 result. |

## Forbidden Claims / Actions

- Do not overwrite unrelated benchmark artifacts.
- Do not rank sidecar timing as main leaderboard timing.
- Do not use GPU evidence from sandboxed/non-trusted commands.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only if regenerated artifacts and focused tests pass.

## Stop Conditions

- Regeneration is too slow or nonfinite beyond reviewed scope.
- Generated artifact contradicts Phase 2 contract.
- Any required trusted GPU evidence is unavailable.

## End-Of-Subplan Protocol

1. Run required local checks.
2. Write Phase 4 result / close record.
3. Draft or refresh Phase 5 subplan.
4. Review Phase 5 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
