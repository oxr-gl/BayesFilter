# P41 Final-Draft Scholarly Audit Findings

Date: 2026-06-09

## Audit target

- Primary review object:
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p41-fixed-sgqf-expanded-companion-note-audit-remediated-2026-06-09.tex`
- Comparator/provenance:
  - `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p40-fixed-sgqf-expanded-companion-note-2026-06-08.tex`

## Execution summary

### Commands run
- Created p41 by copying p40.
- Compiled p41 with:
  - `latexmk -pdf -interaction=nonstopmode -cd docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p41-fixed-sgqf-expanded-companion-note-audit-remediated-2026-06-09.tex`
- Compared p40 and p41 with:
  - `git diff --no-index -- p40 p41`
- Ran narrow MathDevMCP checks on repaired load-bearing labels.
- Ran Codex execution review against the repaired p41 note and p40-to-p41 diff.

## What is not concluded

- This note is not being claimed as a formal proof of every derivation.
- MathDevMCP outputs remain diagnostic evidence, not blanket certification.
- Codex review remains a bounded hostile second opinion, not mathematical proof.
- A pass here would not imply exact nonlinear filtering correctness or production readiness.

## Evidence contract closeout

Question answered:
- whether p41 fixes the documented p40 blockers while preserving the same mathematical lane and staying within a minimal-diff remediation scope.

Primary criterion status:
- pending final Codex execution-review closeout at the time this file was first written; blocker-by-blocker evidence recorded below.

## Blocker-specific governance table

| Block | Planned edit region | Source / proof basis | Verification method | Veto condition | Status |
| --- | --- | --- | --- | --- | --- |
| A | approximation hierarchy / low-interaction paragraph | local derivation / scope discipline | direct text audit + diff | still implies physical-coordinate low interaction survives dense `x=m+C\xi` automatically | fixed |
| B | state-space model / Gaussian projection assumptions | local derivation + Jia filtering setup | direct text audit + MathDevMCP on affine projection | missing noise/solve/shape assumptions | fixed |
| C | 3D preview / univariate moment matching / cloud construction | Jia 2012 Eq. (34)--(37), Eq. (26)--(29), Algorithm 1 | direct text audit + MathDevMCP on Smolyak coefficient | still confuses 27/10/7/6 or overstates level-2 rule as source-mandated | fixed |
| D | 3D toy-cloud narrative | local consistency with C + Jia Algorithm 1 semantics | direct text audit | still narrates 6-point cloud as direct 27-point collapse | fixed |
| E | value path | existing p40 pass block | regression check only | value-path equations materially drift | unchanged / still sound |
| F | worked numeric oracle | existing p40 pass block | regression check only | numeric oracle materially drift | unchanged / still sound |
| G | same-scalar contract | local derivation / contract discipline | direct text audit + MathDevMCP on fixed scalar | scalar-defining vs derivative-only metadata still entangled enough to misstate target | improved / still sound |
| H | gradient chain / derivation ledger | local derivation | direct text audit + MathDevMCP on gradient chain, Cholesky derivative, innovation score | malformed TeX or wrong dependency order remains | fixed pending final Codex confirmation |
| I | boxed and end-to-end algorithms | local execution-order consistency | direct text audit + diff | innovation veto still after log-likelihood computation | fixed pending final Codex confirmation |
| J | FD same-scalar section | local contract discipline | direct text audit + MathDevMCP on central difference | `\mathcal B` vs `\mathfrak B` still unclear | improved / still sound |
| K | validation models / source map / conclusion | local validation-scope discipline + Jia/Singh/Zhao-Cui source-map bounds | direct text audit | incomplete D/E models or overstrong readiness language remains | fixed pending final Codex confirmation |

## Block C source table

| Claim in p41 | Support anchor | Source medium | Notes |
| --- | --- | --- | --- |
| level-2 source family is tunable, not uniquely fixed at `\sqrt3` | Jia 2012 p. 331, Eq. (34)--(35) | conversation-provided page capture corroborating repo PDF | p41 now states the note fixes the GHQ specialization rather than treating it as the unique source-mandated level-2 rule |
| 3D sparse-grid uses signed combination of lower-total-index rules, not the full `(2,2,2)` tensor rule | Jia 2012 p. 332, Algorithm 1 and associated construction | conversation-provided page capture corroborating repo PDF | p41 now distinguishes full tensor comparator from sparse-grid component rules |
| fixed sparse-grid points grow from raw contributions -> merged nodes -> stored nodes after pruning | Jia 2012 p. 332 Algorithm 1; p. 333 Proposition 3.1 / p. 334 Proposition 3.2 for point-count context | conversation-provided page capture corroborating repo PDF | p41 now separates 10 raw contributions, 7 merged distinct nodes, and 6 stored nodes after zero-weight pruning |
| GHQ is a special case / nested relation context for SGQ | Jia 2012 p. 333 Theorem 3.2 and p. 334 discussion | conversation-provided page capture corroborating repo PDF | used to keep the UKF / level-2 bridge bounded rather than overstated |

## MathDevMCP checkpoint outcomes

| Label | Status | Notes |
| --- | --- | --- |
| `prop:p31-affine-projection` | `unverified` | still requires human review/formalization; no contradiction surfaced |
| `eq:p31-smolyak-coeff` | `inconclusive` | backend/obligation limits; no contradiction surfaced |
| `eq:p32-gradient-chain` | `inconclusive` | backend-limited; provenance points to p41 target |
| `eq:p31-chol-derivative` | `unverified` | assumption/formalization limits remain; no contradiction surfaced |
| `prop:p31-innovation-score` | `unverified` | assumption/shape limits remain; no contradiction surfaced |
| `eq:p31-fixed-scalar` | `unverified` | semantic contract remains human-reviewed rather than backend-certified |
| `eq:p31-central-diff` | `unverified` | semantic diagnostic contract; no contradiction surfaced |

Interpretation:
- all required checkpoint outcomes were logged;
- none produced a direct contradiction to the repaired p41 mathematics;
- remaining `unverified` / `inconclusive` statuses are carried as residual risk, not silently ignored.

## Regression-status table for E/F/G/J

| Block | Regression status | Notes |
| --- | --- | --- |
| E | no regression observed | value-path equations left substantively unchanged |
| F | no regression observed | worked numeric oracle left substantively unchanged |
| G | improved wording, no regression observed | clearer scalar-defining vs derivative-support distinction |
| J | improved wording, no regression observed | `\mathfrak B` clarified as implementation-level branch-identity record induced by `\mathcal B` |

## Global source-map / readiness-language check

- Source map now explicitly says the note fixes a GHQ-specialized level-2 rule rather than implying the source uniquely mandates it.
- Conclusion language has been downgraded from “implementation-ready / justify approval” to “mathematically specified for implementation and audit” and “basis for further implementation and validation review.”
- No new source-backed claims were introduced beyond the documented scope.

## Minimal-diff summary

- p41 remains a localized remediation of p40.
- Changed regions are concentrated in:
  - title / abstract / reader orientation,
  - low-interaction plausibility paragraph,
  - state-space assumptions / affine projection proposition,
  - 3D sparse-grid explanation,
  - univariate moment-matching wording,
  - same-scalar contract clarification,
  - gradient chain / derivation ledger,
  - boxed and end-to-end algorithm ordering,
  - FD branch-identity clarification,
  - validation Models D/E,
  - source map row for quadrature,
  - conclusion readiness language.
- Main value-path equations and the worked numeric oracle were kept substantively intact.

## Compile status

- p41 compiled successfully to PDF.
- No unresolved undefined-reference/citation warnings were reported from the final log grep.
- Remaining log output was limited to layout-style underfull/overfull box warnings, including some pre-existing wide math/table content.

## Residual uncertainty

- MathDevMCP still leaves several repaired derivations/contracts as `unverified` or `inconclusive`, though without contradiction.
- Final status depends on the final Codex execution review after the last chain-notation correction.

## Additional self-contained rule-selection clarification

After the initial p41 remediation, the note was further expanded to make the
univariate-rule selection self-contained rather than merely naming the
Gauss--Hermite family.

Added in the p41 note:
- a direct statement that Jia--Xin--Cheng assumes a **sequence** of univariate
  rules satisfying the exactness property required by Theorem 3.1, rather than a
  unique closed-form rule at every level;
- an explicit note that other point-selection methods are admissible if they
  meet that exactness requirement;
- an explicit declaration of the family fixed in this note:
  - `I_1` = 1-point standard-normal GHQ,
  - `I_2` = 3-point standard-normal GHQ,
  - `I_3` = 5-point standard-normal GHQ,
  - in general, `I_\ell` = the `(2\ell-1)`-point standard-normal GHQ rule;
- an explanation that this is a deliberate specialization, not an accidental
  choice, because it:
  1. satisfies the paper's admissibility condition with margin,
  2. gives the note one concrete deterministic family for the fixed-cloud and
     same-scalar contracts,
  3. keeps the low-level worked examples symmetric and teachable,
  4. makes comparison against dense GHQ and the source's UKF bridge cleaner.

This clarification is recorded in the p41 note around the expanded
`Univariate Moment Matching` subsection and is treated as a strengthening of the
Block C source/selection explanation rather than as a new mathematical lane.

## Final verdict

### Final status after Codex execution refresh
- `P41_FINAL_DRAFT_SCHOLARLY_AUDIT_PASS`

### Final Codex execution verdict
- `PASS_WITH_NOTES`
- Codex reported no remaining blocker-level mathematical, notation, logic, or source-matching issue in p41.
- The remaining notes were non-blocking:
  - a wording nuance in the C/D merged-vs-stored cloud narration,
  - formula display order vs prose veto wording in the value path, while runtime summaries and algorithms correctly enforce veto-before-use,
  - and the fact that some model dimensions remain mostly inferable rather than exhaustively enumerated.

### Final acceptance decision
- p41 is accepted as a successful remediation of the documented p40 blocker set within the intended minimal-diff scope.
- The note is ready for the next round of review as:
  - `P41_FINAL_DRAFT_SCHOLARLY_AUDIT_PASS`
