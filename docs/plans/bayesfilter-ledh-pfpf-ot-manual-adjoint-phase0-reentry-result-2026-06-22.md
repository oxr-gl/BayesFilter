# Manual Adjoint Phase 0 Result: Re-Entry And Boundary Lock

status: COMPLETE
date: 2026-06-22
phase: M0-REENTRY

## Question

Is the LEDH-PFPF-OT manual-adjoint/custom-gradient lane ready to proceed from
verified repo state without repeating the known-bad full-AD route or making
unsupported gradient claims?

## Short Answer

Yes, for derivation planning only.  The reset and inventory artifacts are
present, the P82 correction now blocks raw `transport_ad_mode=full` as the
governed `N=10000` actual-gradient route, and no existing manual-adjoint
implementation is claimed.

The next phase is a derivation/chapter-contract phase.  It does not authorize
implementation, GPU work, or P82 FD validation.

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Question | Answered for planning re-entry. |
| Baseline/comparator | Reset memo, inventory result, P8p Phase 3j runtime blocker, and P82 full-AD correction were present. |
| Primary criterion | Passed: artifacts agree that raw/full AD is forbidden for governed `N=10000`, no implementation is claimed yet, and M1 has a bounded derivation subplan. |
| Veto status | No veto.  The stale FD-only amendment text was patched so it no longer names full AD as the active actual-gradient route. |
| Explanatory diagnostics | File existence checks, targeted route-lock text scan, and diff hygiene. |
| Not concluded | No manual-adjoint correctness, implementation readiness, streaming memory improvement, P82 FD agreement, HMC/default/posterior readiness. |

## Checks Run

```bash
test -f docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-reset-memo-2026-06-22.md
test -f docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-inventory-result-2026-06-22.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p82-full-ad-route-correction-2026-06-22.md
test -f docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-n10000-full-transport-fd-result-2026-06-19.md
rg -n "N=10000.*transport_ad_mode=full|transport_ad_mode=full.*N=10000|known-bad|BLOCKED_WAITING_FOR_MEMORY_DISCIPLINED" docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-* docs/plans/bayesfilter-highdim-zhao-cui-p82-*
git diff --check -- docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-* docs/plans/bayesfilter-highdim-zhao-cui-p82-*
```

Observed:

- required files existed;
- route-lock scan found the intended correction/boundary text;
- `git diff --check` passed before this result/subplan write.

## Artifacts Created Or Updated

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-full-ad-route-correction-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-master-program-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase0-reentry-subplan-2026-06-22.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase1-derivation-subplan-2026-06-22.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-fd-only-scope-amendment-2026-06-22.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase4-fd-only-ledh-consistency-subplan-2026-06-22.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-visible-stop-handoff-2026-06-22.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-visible-execution-ledger-2026-06-22.md`

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Close M0 re-entry | Passed | No veto | Exact manual-adjoint equations and stopped/frozen objects still need derivation | Execute M1 derivation/chapter-contract phase | No implementation or validation claim |
| Keep P82 blocked | Passed | Raw full-AD N10000 route vetoed | Which memory-disciplined route will be feasible | Continue manual/custom-adjoint program | No LEDH-vs-FD agreement |

## Handoff To M1

M1 should define the exact mathematical and implementation contract before code:

- scalar/objective differentiated;
- finite Sinkhorn object versus exact regularized OT object;
- barycentric projection adjoint;
- potential/softmin adjoint equations;
- stopped/frozen quantities;
- supported and unsupported transport modes;
- primitive parity tests required for M2.

M1 must not implement code or launch GPU work.
