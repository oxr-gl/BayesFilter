# P17 Zhao-Cui Section 3 Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, JMLR 2024, Section 3.
- Cui and Dolgov, FoCM 2022, as cited by Zhao--Cui for squared-TT/KR support.
- P10 paper-code crosswalk.
- P16 annotated reconstruction.

what_is_not_concluded:
- Lemma 1's external proof is not re-proved from Cui--Dolgov.
- No claim that particle correction has low variance on BayesFilter targets.
- No claim that smoothing weights avoid degeneracy in all models.

## Section 3 Reconstruction

Decision: `SECTION_3_EXPANDED_WITH_KR_COSTS_AND_WEIGHT_PATHS`

P17 expands square-root fitting, defensive density, normalizer, support ratio,
Lemma 1 inequalities, squared-TT mass matrices, marginalization, lower and
upper conditional KR maps, triangular Jacobian proof, map costs, Algorithm 2,
particle proposal and correction, ESS diagnostic, backward smoothing, Markov
identity, backward weights, and variable-ordering cost reason.

Main P16 misses repaired:

- Lemma 1 inequalities;
- upper-map reverse-order construction;
- map evaluation/rootfinding complexity;
- normalized particle weights and ESS;
- smoothing Markov identity;
- normalized backward weights;
- endpoint versus middle marginalization costs \(O(pR^3)\) vs \(O(pR^6)\).

