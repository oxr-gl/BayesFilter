# P07 Closeout And Claim Classification Subplan

Status: `DRAFT_AFTER_P06_OR_STOP`

## Phase Objective

Close the program with a result note that separates candidate rejection,
tuning-required outcomes, route-repair outcomes, bounded support, envelope-only
evidence, and forbidden scientific/product claims.

## Entry Conditions Inherited From Previous Phase

All earlier phases either passed, produced a blocker, or stopped under a
predeclared stop condition.

## Required Artifacts

- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-result-2026-06-22.md`
- Updated stop handoff if stopped early:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-visible-stop-handoff-2026-06-22.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-claude-review-ledger-2026-06-22.md`

## Required Checks/Tests/Reviews

- Verify final result links every executed phase artifact.
- Include decision table and inference-status table.
- Include run manifest with git commit, commands, environment, CPU/GPU status,
  seeds, wall time, output paths, plan file, and result file.
- Include post-run red-team note.
- Claude read-only review of final claim classification.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exactly did the program establish, reject, or leave open? |
| Baseline/comparator | The phase artifacts actually executed. |
| Primary pass criterion | Final note accurately classifies evidence and nonclaims without overstatement. |
| Veto diagnostics | Unsupported claim, missing artifact link, stale status, candidate rejection conflated with research-direction rejection, or missing uncertainty/nonclaim language. |
| Explanatory diagnostics | Phase-level metrics and blocker details. |
| Not concluded | Anything not supported by executed held-out artifacts remains forbidden. |
| Artifact | Final result, review ledger, stop handoff if applicable. |

## Forbidden Claims/Actions

- Do not claim speedup unless P05 passed.
- Do not claim large-N same-row speedup from low-rank-only rows.
- Do not claim posterior correctness, HMC readiness, default/public API
  readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or
  statistical ranking.
- Do not hide negative results.

## Exact Next-Phase Handoff Conditions

No next phase. If the result is blocked or tuning-required, the final note must
state the smallest justified next human or agent action.

## Stop Conditions

- Stop for human direction if final claim classification cannot be reconciled
  with artifacts after five Claude review rounds.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the final result/close record.
3. Update the stop handoff if the program stopped before completion.
4. Review final claims for consistency, correctness, artifact coverage, and
   boundary safety.
