# P39 Claude Review Ledger: SV Gaussian-Mixture CUT4

metadata_date: 2026-06-06
phase: P39

This ledger records Claude review loops for the P39 transformed stochastic
volatility Gaussian-mixture CUT4 comparator.

## Iteration 1

status: `BLOCKED_P39_PLAN_DOC_GOVERNANCE`

Reviewer summary:
- The chapter introduced Gaussian-mixture CUT4 without a self-contained CUT4
  definition or CUT/CUT4 source citation.
- The mixture table was not pinned in the LaTeX section.
- KSC/CNS source governance used topic-level anchors rather than exact
  technical anchors.
- The scalar simple-SV fixture could be overread as validating nonlinear CUT4
  accuracy, even though the conditional component update is linear Gaussian.
- The TT same-target boundary needed to mirror the chapter boundary.

Response:
- Added a CUT4 paragraph with point-count semantics and Adurthi--Singla--Singh
  citations.
- Added the pinned seven-component mixture table to the chapter and recorded
  it as the BayesFilter P39 implementation fixture.
- Tightened the source-support and claim-support ledgers to separate
  bibliographic context, project derivation, implementation evidence, and
  unresolved publication-readiness source gaps.
- Added explicit non-claims that the scalar fixtures validate mixture
  bookkeeping/component-update reduction, not nonlinear CUT4 accuracy.
- Mirrored the same-target TT requirements in the plan veto list.

## Iteration 2

status: `PASS_P39_PLAN_DOC_GOVERNANCE`

Reviewer summary:
- CUT4 semantics are now defined with the CUT4-G rule family, point-count
  formula, implemented polynomial-degree diagnostic, and
  Adurthi--Singla--Singh citations.
- The seven-component mixture table is pinned in the chapter as the
  BayesFilter P39 implementation fixture.
- Source-support ledgers separate contextual support from unresolved
  primary-source KSC/CNS technical-anchor gaps.
- The scalar fixture non-claim is explicit in the plan and chapter.
- The same-target TT boundary is mirrored in the plan veto list and chapter.

Minor non-blocking note:
- Before publication use, recheck exact KSC table and offset convention from
  primary text.

## Code/Governance Review Iteration 1

status: `BLOCKED_P39_CODE_GOVERNANCE`

Reviewer summary:
- The chapter described CUT4 as fourth-degree while the implemented
  `tf_cut4g_sigma_point_rule` reports polynomial degree `5`.
- The `point_count_per_component` diagnostic actually stored a max over
  time/components.
- The tests checked the derived point count but did not explicitly test the
  `dim >= 3` CUT4-G padding boundary.

Response:
- Reworded the chapter to describe CUT4 as the named CUT4-G rule family and
  state that BayesFilter diagnostics report polynomial degree `5`.
- Replaced the ambiguous point-count diagnostic with `cut4_point_counts`,
  `max_cut4_point_count`, `cut4_augmented_dims`, and
  `cut4_polynomial_degrees`.
- Added a test that `tf_cut4g_sigma_point_rule(2)` fails and that the padded
  `q=3` rule has 14 points and polynomial degree 5.

## Code/Governance Review Iteration 2

status: `PASS_P39_CODE_GOVERNANCE_SUPERSEDED_BY_KSC_SHIFT_AUDIT`

Reviewer summary:
- The three prior code-governance blockers were fixed: CUT4-G degree wording,
  unambiguous point-count diagnostics, and the explicit `dim >= 3` padding
  boundary test.
- Focused P39 tests passed in the reviewer environment.

Codex source-audit follow-up:
- After this pass, Codex inspected the accessible Kim--Shephard--Chib
  working-paper PDF and found a material convention issue: KSC tabulates
  locations for `log(epsilon_t^2) + 1.2704`, while the BayesFilter observation
  equation uses `log(epsilon_t^2)`.  The implementation and chapter were
  patched to use effective component means `a_j - 1.2704` and to test the
  resulting mixture mean/variance.  This requires another code/governance
  review iteration.

## Code/Governance Review Iteration 3

status: `SUPERSEDED_TIMEOUT`

Reviewer summary:
- Broad review over code, tests, chapter, plan ledgers, bibliography, and
  traceability was launched after the KSC mean-shift correction.
- The worker remained silent for roughly fifteen minutes and was stopped by
  the exact review label.  No substantive pass/block verdict was received.

Response:
- Launched a narrower blocker-only review focused on the KSC convention,
  overclaim boundary, diagnostics naming, and CUT4-G padding/degree guardrails.

## Code/Governance Review Iteration 3B

status: `PASS_P39_CODE_GOVERNANCE_ITER3B`

Reviewer summary:
- The corrected KSC convention is acceptable for the P39 implementation:
  raw Table 4 locations are treated as shifted locations and the code uses
  effective means `a_j - 1.2704`.
- Tests cover the shifted mixture mean, variance sanity, CUT4-G diagnostic
  names, and `dim >= 3` padding boundary.
- No reviewed blocker remained for native-SV exactness, KSC reweighting, CNS
  implementation, same-target TT, nonlinear CUT4 accuracy, production default,
  or paper-scale overclaim.
