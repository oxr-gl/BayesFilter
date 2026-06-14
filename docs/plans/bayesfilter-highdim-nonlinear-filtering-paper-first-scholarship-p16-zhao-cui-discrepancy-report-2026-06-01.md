# P16 Zhao-Cui Annotated Reconstruction Discrepancy Report

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code audit, paper-code crosswalk, filtering-scalar, reproducibility, and gradient-feasibility ledgers.
- P15 fixed-branch implementability specification and two-step reference example.

what_is_not_concluded:
- No claim that adaptive TT-cross or rank-changing Zhao--Cui code is globally differentiable.
- No claim that the fixed-branch approximate filter equals the exact filtering posterior.
- No claim that the P16 note proves high-dimensional empirical performance.
- No production BayesFilter implementation claim.
- No default-method recommendation.

## Review Outcome

Claude plan review converged after two iterations:

- Iteration 1: `REJECT`; Codex classified all findings as `ACCEPT` and patched the plan controls.
- Iteration 2: `ACCEPT`; Codex independently agreed.

Claude execution review converged after four iterations:

- Iteration 1: `REJECT`; Codex classified findings as `ACCEPT` or `PARTIAL` and expanded implementability, reader exposition, and gradient detail.
- Iteration 2: `REJECT`; Codex classified the shifted-convention finding as `ACCEPT` and patched the main proof and gradient path.
- Iteration 3: `REJECT`; Codex classified the two-step example finding as `ACCEPT` and patched the example.
- Iteration 4: `ACCEPT`; Codex independently agreed that no blocker-level finding remains.

## Open Disagreements

None.

## Residual Non-Blocking Limitations

- The PDF is 24 pages, not the aspirational 50--60 page teaching target.
- The note is still a standalone reconstruction and fixed-branch derivation, not a production implementation.
- MathDevMCP could not certify broad functional TT identities; those remain human-reviewed project derivations.
- The LaTeX build reports one overfull heading warning, which is a layout issue rather than a mathematical or implementability blocker.

