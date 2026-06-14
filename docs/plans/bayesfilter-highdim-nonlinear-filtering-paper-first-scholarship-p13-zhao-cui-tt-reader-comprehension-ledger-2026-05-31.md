# P13 Zhao-Cui TT Reader-Comprehension Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- P12 self-contained proof expansion note.

what_is_not_concluded:
- This ledger does not prove scientific validity or numerical accuracy.
- This ledger does not certify that every future reader will find the note easy.

## Reader Standard

Target reader:
An educated academic from numerical analysis, physics, chemistry, applied
mathematics, or industrial quantitative modeling.  The reader may know
probability and numerical linear algebra, but not Zhao-Cui, SIRT, TT filtering,
or the companion MATLAB code.

## Required Fresh-Reader Questions

| Question a reader should be able to answer | P13 answer location | Status |
|---|---|---|
| What is the filtering object? | `What Problem Are We Solving?`, equations for \(q_t\), \(Z_t\), and \(p_t\). | `ADDRESSED` |
| Why is the integral of \(q_t\) an evidence increment? | Direct derivation after equation for \(Z_t\). | `ADDRESSED` |
| Why might a Gaussian approximation be inadequate in the scalar toy model? | Scalar example discussion of \(y_t=x_t^2+\epsilon_t\). | `ADDRESSED` |
| What does \(\phi_t^2+\tau_t\lambda_t\) mean? | Scalar example and Zhao-Cui human-language section. | `ADDRESSED` |
| How does TT connect to high dimension? | TT section explains cores, ranks, and storage scaling. | `ADDRESSED` |
| How does the TT approximation become a filter? | Zhao-Cui human-language section: approximate, integrate, normalize, marginalize. | `ADDRESSED` |
| Why freeze the branch? | Adaptive-versus-gradient section. | `ADDRESSED` |
| What is frozen? | Fixed-branch algorithm enumerated list. | `ADDRESSED` |
| Why do the two propositions matter? | `Why We Need Two Propositions`. | `ADDRESSED` |
| Could Codex prototype the gradient path from the note? | `How To Compute The Gradient` and Proposition 2. | `ADDRESSED_BUT_REQUIRES_IMPLEMENTATION_CHOICES` |
| Can the scalar example be followed end to end? | Product defensive density and marginal decomposition in `A Scalar Example Before Tensor Trains`. | `ADDRESSED_AFTER_ITER1_PATCH` |
| Does the implementation recipe avoid ambiguous equation-number references? | Section `How To Compute The Gradient` now names the required identities directly. | `ADDRESSED_AFTER_ITER1_PATCH` |

## Remaining Reader Risks

- The TT mass-contraction derivative is still mathematically dense.
- The note is standalone for the fixed-branch construction, but a production
  implementation would still need concrete basis/domain choices for a target
  model.
- The scalar example is illustrative, not a worked numerical fit with actual
  TT cores.

Decision:
`FRESH_READER_FLOW_SUBSTANTIALLY_IMPROVED_PENDING_CLAUDE_EXECUTION_ITER2`
