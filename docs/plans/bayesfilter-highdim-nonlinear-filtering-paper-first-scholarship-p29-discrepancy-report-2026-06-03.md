# P29 Discrepancy Report

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

audit_scope:
- Unresolved P29 critical-equation audit discrepancies.

what_is_not_concluded:
- Absence of disagreements does not imply all P27 equations are correct.

## Discrepancies

No unresolved Codex--Claude disagreements remain after the P29 execution review.

## Remaining Non-Disagreement Limitation

P29-I001 remains a human-review-required limitation:

- Algorithm 5(c.2)'s retained physical marginal derivation, P27 `eq:p24-p16`--`eq:p24-p17`, is not source-fidelity-cleared until visual review.

This limitation is not a Codex--Claude disagreement.  It is an explicit blocker for any claim that Algorithm 5(c.2) is fully certified.
