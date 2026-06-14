# P28 Zhao--Cui Submission Audit Discrepancy Report

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

audit_scope:
- Unresolved Codex--Claude disagreements and blockers discovered during P28 submission audit.

what_is_not_concluded:
- Absence of listed discrepancies does not mean every equation is machine-certified.

## Discrepancies

No unresolved Codex--Claude disagreements remain after plan review and execution review.

## Blockers

The audit records submission blockers, not Codex--Claude disagreements:

- P28-I020: 522 critical/high-risk P27 equations are inventoried but not fully deep-checked.
- P28-I021: Proposition 2 remains a high-risk load-bearing proof.
- P28-I022: KR/preconditioning Jacobian and invertibility details remain high-risk.
- P28-I027: source fidelity relied partly on PDF text extraction and targeted matching; visual source audit remains required.
- P28-I026: negative-control validation gap remains if P27 is used as a testing specification.

These blockers support the final decision `NOT_READY_PATCH_REQUIRED`.
