# Claude Read-Only Review Bundle

Date: 2026-07-03
Review name: `bayesfilter-ledh-leaderboard-score-repair-plan-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review the LEDH leaderboard score-repair master program and visible runbook
before Codex launches Phase 0/1 execution.

This is a plan review only.  It does not decide scientific truth and does not
admit any LEDH score row.

## Artifacts To Inspect

Inspect these bounded local paths:

- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-master-program-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-visible-gated-execution-runbook-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase0-launch-boundary-score-meaning-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase1-row-score-inventory-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase2-lgssm-score-repair-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-result-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-reset-memo-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-total-vjp-score-repair-result-2026-07-01.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase5-final-decision-result-2026-07-01.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is this runbook safe and scientifically clear enough to launch Phase 0/1 for LEDH leaderboard score repair? |
| Baseline/comparator | July 3 LEDH-inclusive leaderboard closeout and reset memo. |
| Primary criterion | The plan must preserve that no LEDH score row is admitted yet and must require total-derivative same-target evidence for any future score row. |
| Veto diagnostics | Contract E reused as leaderboard score; partial derivative allowed as score; scoped diagnostics promoted to full row; missing stop conditions; Claude given execution authority; GPU/XLA runs allowed without trusted context. |
| Explanatory diagnostics | Phase ordering, artifact coverage, local check coverage, review loop clarity. |
| Not concluded | No implementation correctness, no row score admission, no HMC readiness. |

## Review Questions

1. Is there a material correctness or boundary issue in the master program,
   runbook, or first three phase subplans?
2. Is the evidence contract internally consistent with the current LEDH
   leaderboard state?
3. Are required artifacts and checks sufficient for Phase 0/1 launch?
4. Does the plan avoid evasive language around partial derivatives versus true
   scores?
5. Does the plan prevent wrong-target evidence, especially Contract E and P8p
   diagnostics, from being promoted to leaderboard score evidence?

## Required Output

Return concise findings.  End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
