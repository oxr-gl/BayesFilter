# P18 Zhao--Cui Equation Count Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- Equation count is not a proof of readability or correctness.
- Equation count does not establish production readiness or posterior accuracy.

## Gate

Source counted equations in Zhao--Cui Sections 1--3 and 5:

- Sections 1--3: Eqs. (1)--(26): 26 equations.
- Section 5: Eqs. (30)--(35): 6 equations.
- Baseline: 32 equations.
- Required P18 counted equations before fixed-branch boundary: `ceil(1.2 * 32) = 39`.

Counting rule: cosmetic line breaks, duplicate restatements, and layout-only
subcases do not count as added derivation equations.

## Row-Wise Count Before Boundary

The hard boundary is:
`End of Zhao--Cui Annotation and Start of BayesFilter Fixed-Branch Extension`.

| Tag | Source anchor clarified | Category | Non-cosmetic justification |
|---|---|---|---|
| `N1` | Section 1.4 notation | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `N2` | Section 1.4 notation | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `N3` | Section 1.4 notation | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `N4` | Section 1.4 notation | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `N5` | Section 1.4 notation | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `BF-1` | Sections 1--2 Bayes recursion and marginals | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `BF-2` | Sections 1--2 Bayes recursion and marginals | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `BF-3` | Sections 1--2 Bayes recursion and marginals | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `BF-3a` | Sections 1--2 Bayes recursion and marginals | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `BF-4` | Sections 1--2 Bayes recursion and marginals | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `BF-5` | Sections 1--2 Bayes recursion and marginals | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `BF-6` | Sections 1--2 Bayes recursion and marginals | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `BF-7` | Sections 1--2 Bayes recursion and marginals | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `BF-8` | Sections 1--2 Bayes recursion and marginals | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `BF-9` | Sections 1--2 Bayes recursion and marginals | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `BF-10` | Sections 1--2 Bayes recursion and marginals | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `BF-11` | Sections 1--2 Bayes recursion and marginals | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-1` | Section 2.2 TT representation/integration | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-1a` | Section 2.2 TT representation/integration | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-2` | Section 2.2 TT representation/integration | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-2a` | Section 2.2 TT representation/integration | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-3` | Section 2.2 TT representation/integration | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-3a` | Section 2.2 TT representation/integration | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-6` | Section 2.2 TT representation/integration | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-7` | Section 2.2 TT representation/integration | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-8` | Section 2.2 TT representation/integration | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-9` | Section 2.2 TT representation/integration | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-10` | Section 2.2 TT representation/integration | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-11` | Section 2.2 TT representation/integration | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-4` | Section 2.2 TT representation/integration | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `TT-5` | Section 2.2 TT representation/integration | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A1-1` | Algorithm 1 and Eq. (12) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A1-0` | Algorithm 1 and Eq. (12) | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A1-2` | Algorithm 1 and Eq. (12) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A1-2a` | Algorithm 1 and Eq. (12) | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A1-2b` | Algorithm 1 and Eq. (12) | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A1-2c` | Algorithm 1 and Eq. (12) | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A1-2d` | Algorithm 1 and Eq. (12) | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A1-3` | Algorithm 1 and Eq. (12) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A1-4` | Algorithm 1 and Eq. (12) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A1-5` | Algorithm 1 and Eq. (12) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A1-6` | Algorithm 1 and Eq. (12) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A1-7` | Algorithm 1 and Eq. (12) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `S1` | Section 3.1 squared-TT density and Lemma 1 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `S2` | Section 3.1 squared-TT density and Lemma 1 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `S3` | Section 3.1 squared-TT density and Lemma 1 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `S4` | Section 3.1 squared-TT density and Lemma 1 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `S5` | Section 3.1 squared-TT density and Lemma 1 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `S6` | Section 3.1 squared-TT density and Lemma 1 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `M1` | Proposition 2 / Eq. (14) mass matrices | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `M2` | Proposition 2 / Eq. (14) mass matrices | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `M3` | Proposition 2 / Eq. (14) mass matrices | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `M4` | Proposition 2 / Eq. (14) mass matrices | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `M5` | Proposition 2 / Eq. (14) mass matrices | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `M6` | Proposition 2 / Eq. (14) mass matrices | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `M7` | Proposition 2 / Eq. (14) mass matrices | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `M8` | Proposition 2 / Eq. (14) mass matrices | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `M9` | Proposition 2 / Eq. (14) mass matrices | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `K1` | Section 3.1 KR maps and Remark 3 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `K2` | Section 3.1 KR maps and Remark 3 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `K3` | Section 3.1 KR maps and Remark 3 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `K4` | Section 3.1 KR maps and Remark 3 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `K5` | Section 3.1 KR maps and Remark 3 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `K6` | Section 3.1 KR maps and Remark 3 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `K7` | Section 3.1 KR maps and Remark 3 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `K8` | Section 3.1 KR maps and Remark 3 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `K9` | Section 3.1 KR maps and Remark 3 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `K10` | Section 3.1 KR maps and Remark 3 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `K11` | Section 3.1 KR maps and Remark 3 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A2-1` | Algorithm 2 / Eqs. (15)--(16) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A2-2` | Algorithm 2 / Eqs. (15)--(16) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A2-3` | Algorithm 2 / Eqs. (15)--(16) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A2-4` | Algorithm 2 / Eqs. (15)--(16) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `A2-5` | Algorithm 2 / Eqs. (15)--(16) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `F1` | Algorithm 3 / Eqs. (20)--(23) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `F2` | Algorithm 3 / Eqs. (20)--(23) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `F3` | Algorithm 3 / Eqs. (20)--(23) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `F4` | Algorithm 3 / Eqs. (20)--(23) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `F5` | Algorithm 3 / Eqs. (20)--(23) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `F6` | Algorithm 3 / Eqs. (20)--(23) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `F7` | Algorithm 3 / Eqs. (20)--(23) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `B1` | Algorithm 4 / Eqs. (24)--(26) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `B2` | Algorithm 4 / Eqs. (24)--(26) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `B3` | Algorithm 4 / Eqs. (24)--(26) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `B4` | Algorithm 4 / Eqs. (24)--(26) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `B5` | Algorithm 4 / Eqs. (24)--(26) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `B6` | Algorithm 4 / Eqs. (24)--(26) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `B7` | Algorithm 4 / Eqs. (24)--(26) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `B8` | Algorithm 4 / Eqs. (24)--(26) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `B9` | Algorithm 4 / Eqs. (24)--(26) | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P1` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P2` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P3` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P4` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P5` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P6a` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P6b` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P6c` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P6` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7a` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7b` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7c` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7d` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7e` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7f` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7g` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7h` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7i` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7j` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7k` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P7l` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P8` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P9` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P10` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P11` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P11a` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P11b` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P11c` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P12` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P13` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P13a` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P14` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P15` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P16` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P16a` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P16b` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P16b.1` | Section 5 preconditioning / Algorithm 5(c.2) | `added derivation` | defines the two retained transformed coordinates needed for the conditional bridge derivation |
| `P16b.2` | Section 5 preconditioning / Algorithm 5(c.2) | `added derivation` | derives the conditional pushforward identity for the old-state block |
| `P16b.3` | Section 5 preconditioning / Algorithm 5(c.2) | `added derivation` | expands the transformed reference density into conditional and marginal factors |
| `P16b.4` | Section 5 preconditioning / Algorithm 5(c.2) | `added derivation` | rewrites the conditional reference density as the ratio used in the bridge decomposition |
| `P16c` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P16d` | Section 5 preconditioning / Algorithm 5 | `added derivation` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P17` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |
| `P18` | Section 5 preconditioning / Algorithm 5 | `source restatement` | distinct formula used for source-unit derivation or implementation contract; not a cosmetic line split |

## Summary

Corrected subtotal by source scope:

- Section 1 and notation: 16 counted equations.
- Section 2: 26 counted equations.
- Section 3: 57 counted equations.
- Section 5: 36 counted equations.
- Total counted equations from Zhao--Cui Sections 1--3 and 5 before the
  fixed-branch boundary: `135`.

Excluded from this gate:

- Fixed-branch and derivative equations after the hard boundary.
- Section 4 context equation `E1`, because the gate is explicitly limited to
  Zhao--Cui Sections 1--3 and 5.

Decision: `EQUATION_COUNT_GATE_PASS_135_GE_39`.
