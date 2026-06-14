# P13 Zhao-Cui TT Human-Readable Rewrite Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- P10/P11/P12 Zhao-Cui BayesFilter artifacts.

what_is_not_concluded:
- No posterior accuracy claim.
- No HMC readiness claim.
- No global adaptive-code gradient claim.
- No production implementation claim.

## Rewrite Purpose

P12 contained the core mathematical proof, but the main exposition still read
like an audit/proof artifact.  P13 rewrites the material as a standalone
reader-facing note for a fresh educated academic reader.

## Main Human-Readability Controls Added

| Control | Location in P13 note | Purpose |
|---|---|---|
| Filtering derived from Bayes' rule before any paper pointer | `What Problem Are We Solving?` | Makes the normalizer and marginalization understandable without opening Zhao-Cui. |
| Scalar nonlinear example \(x_t=\rho x_{t-1}+\eta_t,\ y_t=x_t^2+\epsilon_t\) | `A Scalar Example Before Tensor Trains` | Shows why the joint filtering object can be non-Gaussian and why a square-root density representation helps. |
| Tensor trains introduced only after the scalar filtering object | `From The Scalar Example To Tensor Trains` | Prevents TT notation from arriving before the reader knows what is being approximated. |
| Zhao-Cui algorithm explained as filtering operations | `Zhao-Cui Algorithm In Human Language` | Connects TT fitting to filtering: approximate \(q_t\), integrate, normalize, marginalize. |
| Adaptive-versus-gradient issue explained in ordinary mathematical language | `Why The Published Adaptive Algorithm Is Not Yet A Gradient Algorithm` | Replaces governance labels with the reason a derivative needs a stable scalar formula. |
| Expanded fixed-branch algorithm | `The Fixed-Branch Algorithm` | Specifies variables, bases, ranks, fitting points, shift, defensive density, normalizer, marginalization, saved branch data, and pseudocode. |
| Prototype-level forward details | `The Fixed-Branch Algorithm` | Splits target evaluation, shifted square-root target construction, interpolation-vs-least-squares core solves, mass contraction, normalized joint, marginal numerator, and saved derivative objects. |
| Propositions motivated before formal statements | `Why We Need Two Propositions` | Explains why normalized filtering and same-scalar differentiation are separate obligations. |
| Caveats rewritten as tests still needed | `What Still Must Be Tested` | Replaces audit language with human-readable mathematical limitations. |
| Source/code details moved out of main flow | Appendix `Source And Code Anchors` | Keeps source discipline without interrupting the exposition. |

Decision:
`P13_HUMAN_READABLE_REWRITE_PATCHED_AFTER_EXECUTION_REVIEW_ITER1`
