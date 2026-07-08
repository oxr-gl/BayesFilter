# Phase 6 Subplan: Closeout And Next Handoff

Date: 2026-06-30

Status: `READY_AFTER_PHASE5_BLOCKER`

## Phase Objective

Close the visible SIR gradient program with a compact decision table, artifact
manifest, review trail, unresolved blockers, and next justified action.

## Entry Conditions Inherited From Previous Phase

- Phase 4 produced a memory blocker after correct GPU/XLA/TF32 route launch.
- Phase 5 completed budget 10 as a full material artifact and sharpened budget
  100 to a single-budget exit-137 blocker.
- The remaining blocker is diagnostic artifact construction for budget 100,
  not a completed scientific classification.

## Required Artifacts

- Phase result: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase6-closeout-result-2026-06-30.md`
- Updated stop handoff.
- Updated execution ledger.
- Final Claude review ledger entry.

## Required Checks, Tests, And Reviews

Local checks:

```bash
rg -n "Status:|Decision|Primary criterion|Veto|Nonclaims|Artifacts" docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-*.md
git diff --check -- docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-*.md
```

Review:

- Claude read-only final review is required.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exactly did the SIR gradient program establish, fail to establish, or leave blocked? |
| Baseline/comparator | All phase results and reviewed diagnostic artifacts. |
| Primary criterion | Closeout preserves the result, gate status, veto status, strongest alternative explanation, and next justified action. |
| Veto diagnostics | Unsupported HMC/posterior/exact-gradient claims; missing artifact links; missing review trail; missing stop/handoff update. |
| Explanatory diagnostics | Summary tables, runtime notes, row residual/MCSE/FD trends. |
| Not concluded | Anything not supported by the reviewed phase artifacts. |

## Forbidden Claims And Actions

- Do not promote scientific claims beyond phase artifacts.
- Do not hide failed or blocked diagnostics.
- Do not start new experiments in closeout.
- Do not edit unrelated files.

## Exact Next-Phase Handoff Conditions

This is the terminal phase.  Completion requires:

- final status written;
- stop handoff updated;
- Claude final review converged or blocker recorded;
- user-facing summary can cite exact artifacts.

## Stop Conditions

- Final review does not converge within five rounds.
- Closeout reveals a missing material artifact that cannot be reconstructed
  without a new run.
- Human direction is needed to decide a new scientific or default-policy claim.

## End-Of-Phase Close Protocol

1. Run required local checks.
2. Write final closeout.
3. Update stop handoff.
4. Preserve Claude review trail.
