# Manual Adjoint Phase 0 Subplan: Re-Entry And Boundary Lock

status: DRAFT_EXECUTABLE
date: 2026-06-22
phase: M0-REENTRY

## Phase Objective

Re-enter the LEDH-PFPF-OT manual-adjoint/custom-gradient lane from verified
checkout state, lock the boundary that raw `transport_ad_mode=full` is not the
governed `N=10000` route, and prepare the next derivation subplan.

## Entry Conditions

- Reset memo exists:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-reset-memo-2026-06-22.md`.
- Inventory result exists:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-inventory-result-2026-06-22.md`.
- P82 correction exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-full-ad-route-correction-2026-06-22.md`.
- P8p Phase 3j runtime blocker exists and is treated as binding evidence
  against governed `N=10000` raw/full-AD validation.

## Required Artifacts

- This subplan.
- Phase 0 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase0-reentry-result-2026-06-22.md`.
- Draft Phase 1 derivation subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase1-derivation-subplan-2026-06-22.md`.
- Updated P82 stop handoff showing downstream blocked state.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the manual-adjoint lane ready to proceed from verified repo state without repeating the known-bad full-AD route or making unsupported gradient claims? |
| Baseline/comparator | Reset memo, inventory result, P8p Phase 3j runtime blocker, and P82 correction artifact. |
| Primary criterion | Artifacts agree that raw/full AD is forbidden for governed `N=10000`, no implementation is claimed yet, and M1 derivation has a bounded executable subplan. |
| Veto diagnostics | Missing reset/inventory evidence; stale claim that manual adjoint already exists; executable plan still using `transport_ad_mode=full` for `N=10000`; missing forbidden claims; missing next subplan. |
| Explanatory diagnostics | File inventory, targeted text search, dirty-worktree note, and line/path anchors for the known-bad route. |
| Not concluded | No manual-adjoint correctness, no implementation readiness, no streaming memory improvement, no P82 FD agreement, no HMC/default/posterior readiness. |
| Preserving artifact | M0 result markdown and updated P82 handoff. |

## Required Checks

Run:

```bash
test -f docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-reset-memo-2026-06-22.md
test -f docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-inventory-result-2026-06-22.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p82-full-ad-route-correction-2026-06-22.md
test -f docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-n10000-full-transport-fd-result-2026-06-19.md
rg -n "N=10000.*transport_ad_mode=full|transport_ad_mode=full.*N=10000|known-bad|BLOCKED_WAITING_FOR_MEMORY_DISCIPLINED" docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-* docs/plans/bayesfilter-highdim-zhao-cui-p82-*
git diff --check -- docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-* docs/plans/bayesfilter-highdim-zhao-cui-p82-*
```

No GPU, Claude, package installation, or code implementation command is
required in M0.

## Forbidden Claims / Actions

- Do not implement manual adjoints in M0.
- Do not launch GPU experiments in M0.
- Do not call existing reset/inventory text implementation evidence.
- Do not claim P82 can proceed before a memory-disciplined gradient route
  exists.
- Do not modify BayesFilter defaults.
- Do not revert unrelated dirty worktree changes.

## Next-Phase Handoff Conditions

M1 may be drafted and executed only if M0 result records:

- reset/inventory artifacts present;
- known-bad full-AD route locked out for governed `N=10000`;
- no existing manual-adjoint implementation claimed;
- exact derivation targets for M1 listed.

## Stop Conditions

Stop and write a blocker result if:

- required reset/correction artifacts are missing;
- the current checkout already contains conflicting manual-adjoint artifacts
  that must be reconciled before planning;
- P82 artifacts cannot be safely amended without overwriting unrelated work;
- any required check fails in a way that changes the phase boundary.
