# P85 Phase 6 Subplan: P84 Handoff And Reset Memo

Date: 2026-06-23

Status: `DRAFT_READY_AFTER_PHASE5`

## Phase Objective

Write the P85 close record, reset memo, and P84 handoff that state whether the
P84 Phase 1 basis/domain blocker is repaired, still blocked, or partially
reframed.

## Entry Conditions Inherited From Previous Phase

- Phase 5 has reviewed manifest classification and regression evidence and
  passed locally.
- Any implementation/test blockers are recorded.
- P84 Phase 2 fitting remains blocked unless Phase 6 explicitly hands off a
  repaired Phase 1 status and Phase 2 still receives its own approval.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase6-p84-handoff-reset-result-2026-06-23.md`
- P85 final reset memo:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-configurable-basis-domain-reset-memo-2026-06-23.md`
- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase5-manifest-classification-regression-result-2026-06-23.md`
- Updated P85 stop handoff.
- Optional refreshed P84 Phase 2 subplan or handoff note, if Phase 1 is
  repaired.
- Final Claude review entry if the P84 handoff changes blocker status.

## Required Checks / Tests / Reviews

- Run P85 documentation hygiene checks.
- Scan final artifacts for forbidden production claims:

```bash
rg -n "production ready|posterior correctness|HMC ready|LEDH superiority|d=50|d=100|default production|PASS_P84" docs/plans/bayesfilter-highdim-zhao-cui-p85*.md -S
```

- Claude read-only review of the Phase 6 result or reset memo if it changes
  P84 blocker status.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What exactly did P85 repair or block, and what is the safe P84 handoff? |
| Baseline/comparator | P84 Phase 1 blocker, P85 phase results, and P85 manifest/test evidence. |
| Primary criterion | Final handoff states a precise status and preserves all remaining P84 production gaps. |
| Veto diagnostics | Claiming P84 production readiness; launching Phase 2 fitting without approval; omitting remaining blockers; unsupported source-faithfulness claim. |
| Explanatory diagnostics | Review trail, local checks, result artifacts, implementation diff summary. |
| Not concluded | No production readiness unless P84 later gates pass with owner approval. |
| Artifact | Phase 6 result, reset memo, updated stop handoff. |

## Forbidden Claims / Actions

- Do not run P84 Phase 2 fitting.
- Do not commit or push unless separately requested.
- Do not claim production readiness, correctness, HMC readiness, LEDH agreement,
  scaling, or default-policy change.
- Do not erase P84 blockers outside the basis/domain blocker.

## Exact Next-Phase Handoff Conditions

P85 completes if Phase 6 writes one of:

- `PASS_P85_P84_PHASE1_BASIS_DOMAIN_REPAIR`, with exact remaining P84 approval
  gates; or
- `BLOCK_P85_P84_PHASE1_BASIS_DOMAIN_REPAIR`, with the smallest next repair; or
- `PARTIAL_P85_P84_PHASE1_BASIS_DOMAIN_REPAIR`, with explicit limitations.

Any continuation into P84 Phase 2 still requires its own reviewed subplan and
exact human approval for fitting.

## Stop Conditions

Stop if:

- final status cannot be stated without overclaiming;
- Claude and Codex do not converge after five rounds for a handoff blocker;
- a human decision is needed to accept an extension or default change.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 6 result / close record;
3. draft or refresh the next P84/P85 handoff artifact;
4. review the handoff for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
