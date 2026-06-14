# P29 Proposition 2 Fixed-Branch Derivative Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," Annals of Mathematical Statistics 1952.
- Cui and Dolgov, squared inverse Rosenblatt transport / squared TT background used by Zhao and Cui.

audit_scope:
- Targeted audit of P27 Section 47, "Proposition 2: The Fixed-Branch Derivative Differentiates The Same Scalar."
- Dependency graph, fixed-branch assumptions, solve derivative, mass derivative, quotient derivative, and carried-filter recursion.

what_is_not_concluded:
- This does not prove numerical stability of the derivative.
- This does not differentiate the adaptive Zhao--Cui algorithm.
- This does not certify every derivative equation outside the audited dependency graph.

## Targeted Audit Table

| P27 label / line range | role | audit finding | status |
|---|---|---|---|
| `eq:p24-p23-gdag1`--`eq:p24-p23-gdag2`, lines 7159--7183 | Forward and derivative computational graph | Correct high-level dependency: target values to fixed LS rows to fixed solve to cores; derivative graph mirrors it. | PASS_TARGETED_AUDIT |
| `eq:p24-p23-gdag2a` | condition-number caveat | Correctly separates same-scalar differentiability from numerical usability. | PASS_TARGETED_AUDIT |
| `eq:p24-p23-gdag3`--`eq:p24-p23-gdag4` | mass/normalizer derivative graph | Algebraic dependency is right if `c_t`, `tau_t`, and branch choices are fixed. | PASS_WITH_LIMITATION |
| `eq:p24-p23-gdag5`--`eq:p24-p23-gdag6` | carried filter quotient derivative | Quotient derivative is algebraically correct; MathDevMCP verified scalar quotient form. | MCP_VERIFIED |
| `eq:p24-p23-gdag7` | log-likelihood derivative | Log-normalizer derivative is correct under positive finite normalizers. | MCP_VERIFIED |
| `eq:p24-p23-gdag8` | running-example target derivative | Product rule is correct when observation factor is beta-independent. Requires beta-dependence caveat if observation model changes. | PASS_WITH_LIMITATION |
| fixed ridge lemma | differentiability of fixed solve | Correct: differentiating `N_k g_k=d_k` gives `N_k dot g_k=dot d_k-dot N_k g_k`; assumes nonsingular fixed ridge system. | PASS_TARGETED_AUDIT |
| Proposition 2 statement | same scalar derivative | The proposition is correct in scope if all branch objects are fixed and all differentiability-under-integral assumptions hold. | PASS_WITH_LIMITATION |
| Proposition 2 proof | proof chain | Proof is structurally sound and does not differentiate adaptive ranks, pivots, domains, shifts, floors, or sweep count. | PASS_TARGETED_AUDIT |

## Remaining Limitations

- The proof should not be described as a numerical stability theorem.
- The proof depends on fixed branch `B`, fixed shifts/floors, fixed domains, fixed sweep count, nonsingular systems, and valid differentiation under finite contractions/integrals.
- A prototype finite-difference branch-stability check is still needed for empirical confidence.

## Verdict

proposition2_verdict: `PASS_TARGETED_AUDIT_WITH_LIMITATIONS`

P29 reduces the P28 Proposition 2 blocker: the same-scalar derivative argument is mathematically coherent under the stated fixed-branch assumptions. It remains narrow and should be worded as such.

