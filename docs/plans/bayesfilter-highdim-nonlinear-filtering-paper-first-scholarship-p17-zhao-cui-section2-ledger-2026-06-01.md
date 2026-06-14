# P17 Zhao-Cui Section 2 Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, JMLR 2024, Section 2.
- P10 paper-code crosswalk.
- P16 annotated reconstruction.

what_is_not_concluded:
- No claim that TT rank adaptation is globally smooth.
- No claim that moderate TT ranks hold for BayesFilter target models.

## Section 2 Reconstruction

Decision: `SECTION_2_EXPANDED_WITH_DISPLAYED_TT_FORMULAS`

P17 expands recursive posterior equations (9)--(11), the functional TT product,
the source summation form with endpoint rank indices, basis coefficient cores,
core integration, complexity statements, Algorithm 1 target construction,
separable reapproximation, marginalization, normalizer, parameter/filter
marginals, and retained evaluator.

Main P16 misses repaired:

- source TT summation with \(R_0=R_D=1\);
- coefficient-axis interpretation for \(A_k\)/\(C_k\);
- approximate proportionality after normalization;
- \(O(DpR^2)\) and \(O(DpR^3)\) cost statements with rank caveat;
- retained two-block evaluator \(\widehat\pi_t(x_t,\theta)\).

