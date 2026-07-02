# Streaming Manual VJP Phase 8 Subplan: P82 Handoff

status: DRAFT
date: 2026-06-23
phase: S8-P82-HANDOFF

## Phase Objective

Prepare the reviewed handoff back to P82: exact actual-gradient artifact,
route metadata, and the governed same-scalar FD comparison conditions.

## Entry Conditions

- S7 produced a valid `N=10000` actual-gradient artifact, or S7 produced a
  blocker that requires closeout instead of P82 handoff.

## Required Artifacts

- S8 handoff result.
- Exact P82 next-step commands if valid.
- Refreshed P82 subplan or blocker note.
- Refreshed S9 closeout subplan.

## Required Checks/Tests/Reviews

- Verify S7 JSON exists and records the new blockwise VJP route.
- Verify P82 FD protocol remains: `N=1000`, five seeds, 13 points, trim highest
  and lowest, OLS on remaining 11 points, slope standard error, two-SE
  diagnostic threshold, FD is not oracle.
- `git diff --check` on plan artifacts.
- Claude one-path review of S8 result.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is P82 ready to resume governed FD comparison using the new actual-gradient artifact? |
| Baseline/comparator | S7 actual-gradient artifact and P82 FD protocol. |
| Primary pass criterion | Handoff contains exact artifact paths, exact commands, route metadata, entry conditions, and stop conditions. |
| Veto diagnostics | Missing S7 artifact; route mismatch; FD protocol drift; Zhao-Cui comparator reintroduced; FD treated as oracle. |
| Explanatory only | Runtime, MCSE, warning summaries. |
| Not concluded | FD agreement until P82 actually runs; posterior/HMC/default readiness. |

## Forbidden Claims/Actions

- Do not run FD comparison inside S8 unless a refreshed P82 subplan explicitly
  authorizes it.
- Do not use Zhao-Cui as comparator.
- Do not weaken the FD protocol.

## Exact Next-Phase Handoff Conditions

Advance to S9 only if:

- S8 result either authorizes a separate P82 run under exact conditions or
  records why P82 remains blocked;
- Claude review returns `VERDICT: AGREE`.

## Stop Conditions

Stop if:

- S7 artifact is missing or invalid;
- FD protocol cannot be preserved;
- Claude review does not converge.

## End-Of-Phase Protocol

1. Run required checks.
2. Write the S8 result or blocker.
3. Draft or refresh S9.
4. Review S9 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
