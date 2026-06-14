# P28 Zhao--Cui Submission Audit Result

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," Annals of Mathematical Statistics 1952.
- Cui and Dolgov, squared inverse Rosenblatt transport / squared TT background used by Zhao and Cui.

audit_scope:
- P28 pre-submission audit of the P27 Zhao--Cui companion note.
- Equation inventory, source fidelity, MathDevMCP narrow algebra checks, notation/dimension review, implementation-readiness review, chair-reader review, and numerical-test review.

what_is_not_concluded:
- This audit does not prove P27 is flawless.
- This audit does not machine-certify all 754 displayed equation environments.
- This audit does not prove exact posterior accuracy or production readiness.
- This audit does not run large-scale experiments.

## Inspected

- P27 TeX, PDF, log, and P27 ledgers.
- Local Zhao--Cui PDF and extracted text.
- P27 title/author block.
- P27 equation environments and theorem-like blocks.
- P27 source citations and human-facing language scan.
- P27 validation section and benchmark models.

## Freeze Status

- P27 TeX: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`
- P27 PDF: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.pdf`
- page_count: 103
- author: Chak Wong
- build_status: PDF previously rebuilt successfully with `latexmk`.
- bibliography_status: no undefined citation/reference blocker found in the prior log scan; final validation repeated below.

## Equation Inventory

- equation_environments: 754
- aligned_subblocks: 41
- theorem_like_blocks: 10
- propositions: 3
- lemmas: 2
- proofs: 5
- critical_risk_equations: 229
- high_risk_equations: 293
- medium_risk_equations: 1
- low_risk_equations: 231

equation_audit_verdict: `INVENTORY_COMPLETE_DEEP_AUDIT_INCOMPLETE`

The mechanical equation inventory is complete, but the release gate for a "flawless" mathematical submission is not met because the 229 critical and 293 high-risk displays have not all been deep-checked.

## Source-Fidelity Verdict

source_fidelity_verdict: `NOT_READY_FOR_FLAWLESS_CLAIM`

P27 appears to reconstruct the main Zhao--Cui equation spine for Sections 1--3 and 5, including Eqs. (1)--(26), Eqs. (30)--(35), Algorithm 1, Algorithm 2, and Algorithm 5.  The audit used PDF text extraction plus targeted matching, so a visual source-fidelity pass remains required before claiming complete annotation fidelity.

## MathDevMCP Status

mathdevmcp_status: `NARROW_SUPPORT_ONLY`

MCP-verified scalar algebra:

- quotient derivative algebra;
- squared-term differential algebra;
- log-normalizer scalar form;
- Bayes normalizer cancellation;
- squared-density normalization cancellation;
- shifted squared-mass derivative algebra.

MCP tool-limited or unverified:

- callable functional derivative notation;
- matrix/linear-solve derivative in assumption form;
- triangular determinant using matrix-constructor syntax.

These scalar checks must not be cited as verification of the full functional derivative, matrix solve derivative, TT contraction derivative, or KR transport chain.

## Notation And Dimension Verdict

notation_dimension_verdict: `NOT_READY_FOR_FLAWLESS_CLAIM`

No global notation collapse was found, but the coordinate systems, KR Jacobians, TT core indexing, and fixed-branch derivative objects remain high-risk and require detailed equation-level review.

## Implementation-Readiness Verdict

implementation_readiness_verdict: `PROTOTYPE_READY_NOT_PRODUCTION_CERTIFIED`

P27 is detailed enough to begin a prototype implementation of the squared-TT filter and fixed-branch derivative.  A production-grade implementation handoff should convert the critical equations into a compact crosswalk with inputs, outputs, shapes, primitives, stabilization, differentiability status, and tests.

## Chair-Reader Verdict

chair_reader_verdict: `PERSUASIVE_WITH_HIGH_RISK_SECTIONS`

The broad narrative is likely understandable and persuasive to the chemistry chair.  The highest trust-risk sections remain KR/preconditioning and fixed-branch derivative Proposition 2.

## Numerical Sanity-Test Verdict

numerical_sanity_verdict: `VALIDATION_PROTOCOL_GOOD_BUT_NOT_EXECUTED`

P27 describes a credible validation protocol and adopts Zhao--Cui model families.  It does not report empirical outcomes.  A negative-control test should be added if P27 becomes a validation specification rather than a companion note.

## Claude Review Summary

Plan review:

- Two repo-reading Claude plan-review attempts stalled.
- One over-constrained attempt refused because it could not read files.
- A direct self-contained plan-review prompt returned 8 findings.
- Codex classified 7 findings as `ACCEPT` and 1 as `PARTIAL`.
- Accepted controls were patched into the P28 plan and recorded in the Claude review ledger.

Execution review:

- Pending at the time this draft result was created.

## Current Submission Decision

final_submission_readiness_decision: `NOT_READY_PATCH_REQUIRED`

Reason:

- P27 is strong and substantially panel-readable.
- However, the P28 release gate for mathematical flawlessness is not met until the critical/high-risk equation set is deep-checked or the submission claim is narrowed.
- No corrected P28 submission-candidate note was created in this pass because the audit found review blockers rather than a small finite patch set.

## Claim/Evidence/Allowed-Wording Table

| claim | evidence currently available | current status | allowed wording before P29 |
|---|---|---|---|
| P27 is a readable companion to Zhao--Cui. | Chair-reader audit and document inspection. | SUPPORTED_WITH_RISK | "P27 is substantially more readable and likely persuasive, with KR/preconditioning and derivative sections still high-risk." |
| P27 reconstructs Zhao--Cui Sections 1--3 and 5. | Source spine matched by extracted text and targeted checks. | PARTIAL_SUPPORT | "P27 appears to reconstruct the main displayed spine; visual source-fidelity audit remains required." |
| All P27 equations are correct. | 754 equations inventoried; 522 critical/high-risk not fully deep-checked. | UNSUPPORTED | Do not claim. |
| MathDevMCP verifies the derivations. | Narrow scalar algebra checks only. | UNSUPPORTED_BROADLY | "MathDevMCP supports selected scalar identities only." |
| Fixed-branch derivative is fully audited. | Story, equations, and scalar checks present; Proposition 2 and dependency graph high-risk. | NOT_YET | "Fixed-branch derivative is prototype-derivable but requires critical-equation audit." |
| P27 is implementation-ready. | Detailed mathematical recipes and object flow. | PROTOTYPE_READY | "Detailed enough to start a prototype; production implementation still needs shape/index/Jacobian crosswalk." |
| P27 is a validation specification. | Validation protocol and model families present; no experiments; negative control gap. | PARTIAL | "Validation protocol is specified but not executed; add negative controls before using as a validation oracle." |

## Blocking Items Before A Flawlessness-Oriented Submission

| issue id | blocker | required resolution |
|---|---|---|
| P28-I020 | 522 critical/high-risk equations not fully deep-checked. | Deep-audit all claim-bearing critical/high equations or narrow submission claims. |
| P28-I021 | Proposition 2 is load-bearing and high-risk. | Audit full dependency graph, branch assumptions, normalizers, quotient derivatives, solve derivatives, and carried-filter derivatives. |
| P28-I022 | KR/preconditioning coordinate transforms remain high-risk. | Audit assumptions, invertibility, determinant/Jacobian directions, and failure modes. |
| P28-I027 | Source matching relied partly on PDF text extraction. | Perform visual source audit for critical/high source-mapped equations and Algorithms 1, 2, and 5. |
| P28-I026 | Negative-control validation gap. | Add explicit negative controls if P27 is used as a validation specification. |

## Recommended Next Action

Create a P29 critical-equation audit pass over:

1. all theorem-like blocks;
2. all normalizer/mass/Jacobian/quotient/linear-solve derivative equations;
3. every display in Proposition 1 and Proposition 2;
4. Algorithm 2 and Algorithm 5 line-by-line against Zhao--Cui;
5. KR/preconditioning coordinate-transform displays.
6. a compact notation-shape contract for risky subsystems;
7. a reconstructed/adapted/original/unaudited coverage table;
8. negative-control validation language if the note is used as a testing specification.

Only after that pass should P27 be described as submission-ready with minor risk.
