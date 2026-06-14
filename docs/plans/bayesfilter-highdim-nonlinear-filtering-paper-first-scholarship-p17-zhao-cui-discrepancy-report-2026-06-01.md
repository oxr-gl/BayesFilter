# P17 Zhao-Cui Full Equation Reconstruction Discrepancy Report

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code audit and paper-code crosswalk ledgers.
- P11--P16 Zhao-Cui derivative, implementability, and annotated reconstruction artifacts.

what_is_not_concluded:
- No claim that adaptive Zhao--Cui code has a globally smooth analytical gradient.
- No claim that fixed-branch differentiation proves exact posterior accuracy.
- No production BayesFilter implementation claim.
- No high-dimensional empirical validation on BayesFilter target models.
- No default-method recommendation.

## Review Outcome

Claude plan review converged after two iterations:

- Iteration 1: `REJECT`; Codex classified both findings as `ACCEPT` and patched the plan.
- Iteration 2: `ACCEPT`; Codex independently agreed.

Claude execution review converged after two iterations:

- Iteration 1: `REJECT`; Codex classified both Section 5 findings as `ACCEPT` and patched the note.
- Iteration 2: `ACCEPT`; Codex independently agreed.

## Open Disagreements

None.

## Residual Non-Blocking Issues

- The P17 note is 30 pages, still shorter than a full textbook-length 50--60 page treatment.
- Section 5 now has mild duplication between the first derivation and the contiguous five-density chain; Claude judged this non-blocking.
- MathDevMCP certified only a narrow quotient algebra identity; most TT/filtering identities remain human-reviewed project derivations.
- The PDF build reports one overfull heading warning.

