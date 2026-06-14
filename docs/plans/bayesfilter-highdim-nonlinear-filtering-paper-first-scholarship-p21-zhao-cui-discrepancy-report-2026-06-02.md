# P21 Zhao--Cui Discrepancy Report

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.

what_is_not_concluded:
- No executable prototype claim.
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive branch choices.
- No HMC convergence claim.
- No production implementation readiness claim.

## Status

Decision: `NO_UNRESOLVED_DISCREPANCIES_AFTER_EXECUTION_REVIEW_ITERATION_2`.

The known pre-review discrepancy was terminological: the plan path contains
`reference-implementation`, but the reviewed P21 scope explicitly forbids
executable code and requires an implementation-ready mathematical
specification instead.  This is not a substantive discrepancy because the plan,
note, ledgers, and result all state the non-code scope.

Claude execution review iteration 1 raised three substantive blockers:

1. carried-filter shape/storage contract incomplete;
2. finite-difference print/report contract incomplete;
3. missing teach-back checkpoints after dense derivative blocks.

Codex classified all three as `ACCEPT`, patched the note and ledgers, and
reran Claude.  Claude execution review iteration 2 returned `ACCEPT`.

Unresolved disagreements: none.

Downstream block: none for the P21 mathematical-specification artifact.  A
future coding phase remains blocked on a separate implementation plan and must
not treat P21 as empirical validation or full adaptive Zhao--Cui readiness.
