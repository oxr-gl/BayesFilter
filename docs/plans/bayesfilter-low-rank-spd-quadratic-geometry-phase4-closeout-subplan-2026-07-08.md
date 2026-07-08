# Phase 4 Subplan: Closeout And Handoff

Date: 2026-07-08
Status: `DRAFT_READY_FOR_EXECUTION`
Master program: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-master-program-2026-07-08.md`

## Phase Objective

Close out the low-rank SPD quadratic geometry runbook, record final artifacts and remaining gaps, and hand off the next repair target without overclaiming.

## Entry Conditions Inherited From Phase 3

- Phase 3 checks passed.
- Final bounded CPU-hidden rerun wrote structured JSON/Markdown artifacts.
- Low-rank geometry rejected by holdout and fallback provenance was preserved.
- Final diagnostic had no hard vetoes but remained non-promoting.

## Required Artifacts

- Phase 4 result: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase4-closeout-result-2026-07-08.md`
- Updated execution ledger: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-visible-execution-ledger-2026-07-08.md`

## Required Checks, Tests, Reviews

- Verify Phase 3 result exists and references final artifacts.
- Run `git diff --check`.
- Codex closeout review for unsupported claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the runbook complete enough for a future agent to continue from the right blocker? |
| Baseline/comparator | Master program and Phase 0-3 results. |
| Primary criterion | Closeout records implemented artifacts, checks, final diagnostic decision, remaining gaps, and forbidden claims. |
| Veto diagnostics | Unsupported readiness/convergence/source-faithfulness claim, missing artifact path, conflating low-rank rejection with research-direction rejection. |
| Explanatory only | Dirty worktree size and pre-existing unrelated changes. |
| Not concluded | No scientific or runtime readiness claims. |

## Stop Conditions

- Missing Phase 3 result or final artifact.
- `git diff --check` fails and cannot be repaired.
- Closeout cannot separate candidate failure from research-direction failure.
