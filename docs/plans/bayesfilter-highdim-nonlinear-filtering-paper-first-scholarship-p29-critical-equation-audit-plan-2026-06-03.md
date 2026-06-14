# P29 Zhao--Cui Critical Equation Audit Plan

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," Annals of Mathematical Statistics 1952.
- Cui and Dolgov, squared inverse Rosenblatt transport / squared TT background used by Zhao and Cui.

audit_scope:
- Focused critical-equation audit responding to P28 blockers.
- Load-bearing equations only: Proposition 2 fixed-branch derivative, KR/preconditioning Jacobians, normalizer/mass contractions, fixed linear-solve derivatives, and Zhao--Cui Algorithm 1/2/5 provenance.

what_is_not_concluded:
- This is not a complete audit of all 754 P27 equation environments.
- This does not certify exact posterior accuracy or production implementation readiness.
- This does not prove the adaptive Zhao--Cui algorithm is globally differentiable.
- This does not run numerical experiments.

## Skeptical Pre-Execution Audit

P28 showed that a full flawlessness claim is too broad without checking 522 critical/high-risk displays.  P29 therefore narrows the question to the load-bearing equations most likely to damage reviewer trust:

1. same-scalar fixed-branch derivative;
2. mass/normalizer contractions;
3. KR and preconditioning Jacobian directions;
4. source provenance for Algorithms 1, 2, and 5.

The plan passes the pre-execution audit because it does not claim to finish all P28 blockers.  Its evidence contract is to determine whether the most dangerous mathematical pillars pass targeted audit, require patching, or remain human-review-required.

## Evidence Contract

Question:
- Do the load-bearing equations in P27 survive a focused source/algebra/notation audit well enough to reduce P28's main submission blockers?

Primary pass criterion:
- No audited load-bearing equation is found wrong.
- Any ambiguity is recorded as `HUMAN_REVIEW_REQUIRED` or `PATCH_REQUIRED`, not silently passed.

Veto diagnostics:
- wrong Jacobian direction in KR or preconditioning;
- derivative of fixed branch differentiates a scalar different from \(\widehat\ell_T(\beta;B)\);
- mass contraction has incompatible dimensions or transpose order;
- Algorithm 1/2/5 provenance contradicts Zhao--Cui source text;
- accepted Claude finding remains unpatched in P29 artifacts.

What will not be concluded even if P29 passes:
- P27 is not globally certified equation-by-equation.
- P27 is not production implementation-ready.
- P27 validation protocol is not empirically executed.

## Ledgers

Create:

- `...p29-critical-equation-audit-plan-2026-06-03.md`
- `...p29-proposition2-derivative-ledger-2026-06-03.md`
- `...p29-kr-preconditioning-jacobian-ledger-2026-06-03.md`
- `...p29-mass-normalizer-ledger-2026-06-03.md`
- `...p29-algorithm-provenance-ledger-2026-06-03.md`
- `...p29-notation-shape-contract-ledger-2026-06-03.md`
- `...p29-mathdevmcp-ledger-2026-06-03.md`
- `...p29-claude-review-ledger-2026-06-03.md`
- `...p29-discrepancy-report-2026-06-03.md`
- `...p29-critical-equation-audit-result-2026-06-03.md`

Every ledger must contain `metadata_date`, `target_document`, `seed_papers`, `audit_scope`, and `what_is_not_concluded`.

## Audit Rules

Use statuses:

- `PASS_TARGETED_AUDIT`;
- `PASS_WITH_LIMITATION`;
- `PATCH_REQUIRED`;
- `HUMAN_REVIEW_REQUIRED`;
- `MCP_VERIFIED`;
- `MCP_TOOL_LIMIT`;
- `SOURCE_MATCH_TARGETED`;
- `SOURCE_VISUAL_REQUIRED`.

For each audited formula record:

- P27 label/line;
- role;
- source or project-derivation support;
- dimensions/measures;
- algebra/proof status;
- implementation implication;
- final status.

## Claude Review

Run Claude hostile execution review after ledgers are drafted.  Claude is a bounded reviewer only; Codex classifies every finding as `ACCEPT`, `PARTIAL`, `DISPUTE`, or `CLARIFY`.

If Claude file-reading stalls, use a direct self-contained prompt summarizing the P29 evidence and decision, and record that limitation.

## Validation

- Run MathDevMCP on narrow encodable obligations.
- Run `git diff --check`.
- Confirm required metadata fields.
- Confirm only P29 markdown artifacts are created unless a specific P27 correction is required.
- Do not edit chapters, production code, DPF lane, public APIs, or unrelated dirty files.
