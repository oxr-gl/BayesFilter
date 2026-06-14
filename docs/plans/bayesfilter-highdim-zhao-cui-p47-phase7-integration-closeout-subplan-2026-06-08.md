# P47-M7 Subplan: Integration Closeout

metadata_date: 2026-06-08
phase: P47-M7
status: `DRAFT_FOR_CLAUDE_PLAN_REVIEW`

## Purpose

Close P47 by reconciling all claim ledgers, promoted rows, blocker rows,
nonclaims, documentation, and next downstream decisions.

## Phase Prerequisites

- `PASS_P47_M0_GOVERNANCE`
- `PASS_P47_M1_ADAPTIVE_ROUTE`
- `PASS_P47_M2_PAPER_SCALE_READINESS`
- `PASS_P47_M3_GENERALIZED_SV_EQUALITY`
- `PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY`
- `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING`
- `PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING`
- `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING`
- `PASS_P47_M6_SCORE_HMC_READINESS`

If any upstream phase blocks, M7 may write a blocker closeout artifact but must
not emit `PASS_P47_M7_CLOSEOUT`.

## Tasks

1. Audit P47-M0--M6 result artifacts and review ledgers.
2. Update traceability rows without overwriting P37/P45/P46 history.
3. Separate promoted filtering evidence from diagnostics, blockers, and
   surrogate-usefulness evidence.
4. Record what can and cannot be declared about Zhao--Cui filtering after P47.
5. Verify every promoted Zhao--Cui row carries the M1 route label:
   `adaptive route candidate` or `documented-deviation fixed-design
   substitute`.
6. Create a final decision table and post-run red-team note.

## Evidence Contract

Question: can P47 close without overclaiming adaptive reproduction,
paper-scale completion, equality, score API stability, or HMC readiness?

Primary pass criterion: every promoted row has a corresponding result artifact
and every blocked row has a blocker class and nonclaim; every promoted
Zhao--Cui row preserves the M1 route label.

Veto diagnostics:

- P45/P46 historical blockers are erased;
- S&P 500 scope exclusion is lost;
- first-gate or diagnostic evidence is promoted as production evidence;
- HMC/API/readiness claims lack P42 evidence.
- generic Zhao--Cui wording hides a documented-deviation substitute.
- `PASS_P47_M7_CLOSEOUT` is emitted while any upstream phase is blocked.

## Local Gates

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim
git diff --check -- bayesfilter/highdim tests/highdim docs/plans
```

## Claude Gate

Expected full-closeout token only if all prerequisites passed:

```text
PASS_P47_M7_CLOSEOUT
```

If any upstream phase is blocked, the expected terminal token for a truthful
blocker closeout is:

```text
PASS_P47_M7_BLOCKER_CLOSEOUT
```
