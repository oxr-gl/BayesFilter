# P91 Phase 9 Subplan: Final Production Decision

Date: 2026-06-29

Status: `REFRESHED_PENDING_PHASE8_RESULT_REVIEW`

## Phase Objective

Make the final P91 production decision from reviewed phase evidence only.
Promote Zhao-Cui SIR d18 only if every P91 production gate passes; otherwise
close with explicit blockers and no unsupported scientific/product/default
claim.

## Entry Conditions Inherited From Previous Phase

- Phase 8 result reviewed pass.
- P91 release-note draft reviewed pass.
- All upstream phase results are available.
- This Phase 9 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- Phase 9 final decision:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md`
- Final reset memo:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-reset-memo-2026-06-29.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-visible-execution-ledger-2026-06-29.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-visible-stop-handoff-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed final document checks:

```bash
rg -n "P91|score identity|FD|GPU/XLA|batched|HMC|benchmark|release|default|production" docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
rg -n "BLOCK_FIXED_TTSIRT|BLOCK_FULL_SOURCE_ROUTE_FD|Phase 3|posterior correctness|exact likelihood correctness|universal GPU|divergence_status|owner-accepted" docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
```

Claude review is required for final decision. No new runtime, GPU/HMC,
package/network, release, CI, or default-policy command is authorized in Phase
9.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the final P91 production decision for Zhao-Cui SIR d18? |
| Baseline/comparator | Reviewed P91 phase results. |
| Primary criterion | Decision exactly reflects upstream pass/blocker statuses and promotes only if every P91 required gate passed. |
| Veto diagnostics | Missing blocker, unsupported exact likelihood/posterior/GPU/default claim, release/default action without authority, or proxy metric promoted across ledgers. |
| Explanatory diagnostics | Phase ledger, FD table, score identity table, GPU/JIT and benchmark summaries, HMC smoke summary, release-note caveats, preserved blocker table. |
| Not concluded | Any unpassed gate remains not concluded. |
| Artifact | Final decision, reset memo, ledgers, stop handoff. |

## Forbidden Claims/Actions

- Do not claim production readiness unless all P91 gates passed.
- Do not claim exact likelihood correctness or posterior correctness unless a
  separate reviewed artifact proves that stronger claim.
- Do not claim GPU is universally faster.
- Do not change defaults, release, publish, or mutate CI in Phase 9.
- Do not weaken blockers.
- Do not convert Phase 3 owner-accepted limited FD evidence into a full
  source-route FD pass.

## Exact Final Handoff Conditions

P91 may be marked complete only if:

- Phase 9 final decision receives Claude `VERDICT: AGREE`;
- final status is explicit;
- unresolved blockers and non-claims are listed;
- safest next action is recorded.

## Stop Conditions

- Upstream result missing or contradictory.
- Final result would imply unsupported scientific/product/default readiness.
- Local checks fail and cannot be repaired.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 9 final decision and reset memo.
3. Review final decision for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
4. Update ledgers and stop handoff.
