# P17 Zhao-Cui Section 1 Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, JMLR 2024, Section 1.
- P16 annotated reconstruction.

what_is_not_concluded:
- No claim that related-work coverage is a theorem support source.
- No claim that Section 6 experiments are reproduced.

## Section 1 Reconstruction

Decision: `SECTION_1_EXPANDED_WITH_P16_MISSES_REPAIRED`

P17 expands the state-space model, full joint density, posterior/evidence,
filtering, parameter learning, path learning, smoothing, coordinate grouping,
Hellinger distance, pushforward identity, and pullback identity.

Main P16 misses repaired:

- coordinate grouping \(x_{<j},x_{>j},x_{\le j},x_{\ge j}\);
- Hellinger distance formula;
- pushforward and pullback density formulas;
- implementation meaning of map evaluators and Jacobian determinants.

