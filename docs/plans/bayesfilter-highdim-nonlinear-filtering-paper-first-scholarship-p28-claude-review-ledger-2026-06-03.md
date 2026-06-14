# P28 Zhao--Cui Submission Audit Claude Review Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

audit_scope:
- Claude Code hostile review of the P28 audit plan and execution artifacts.
- Codex-supervisor classification of every Claude finding.

what_is_not_concluded:
- Claude review does not certify the document.
- Claude review does not replace Codex source/audit judgment.
- Claude review does not prove all equations correct.

## Review Attempts

### Plan Review Iteration 1

Command attempt `highdim-p28-submission-audit-plan-review-iter1` stalled and was stopped.

Command attempt `highdim-p28-submission-audit-plan-review-iter1b` was over-constrained by "do not run tools"; Claude requested pasted plan text and produced no findings.

Command attempt `highdim-p28-submission-audit-plan-review-iter1c` with read-only file access stalled and was stopped.

Command attempt `highdim-p28-submission-audit-plan-review-iter1d` used a direct self-contained prompt summarizing the plan.  Claude returned 8 findings.

### Execution Review Iteration 1

Command attempt `highdim-p28-submission-audit-exec-review-iter1` with read-only artifact access stalled and was stopped.

Command attempt `highdim-p28-submission-audit-exec-review-iter1b` used a direct self-contained prompt summarizing the P28 audit result.  Claude returned 12 findings across four personas and agreed that `NOT_READY_PATCH_REQUIRED` is appropriate if the document is positioned as deep-verified, source-faithful, or implementation-safe.

## Codex Classifications

| Issue id | Claude finding summary | Codex classification | Patch/control added |
|---|---|---|---|
| P28-I001 | High-risk equation selection was underspecified for 754 equation environments. | ACCEPT | Added explicit `CRITICAL`/`HIGH`/`MEDIUM`/`LOW` risk rubric and mandatory coverage floor. |
| P28-I002 | Source-fidelity scope could miss assumptions or proof dependencies outside Zhao--Cui Sections 1--3 and 5. | ACCEPT | Added appendix/dependency escalation rule and source-gap blocker classification. |
| P28-I003 | Release/pass-fail thresholds were too subjective. | ACCEPT | Added hard release gates for unresolved findings, critical equations, source contradictions, dimension/measure contradictions, implementation blockers, numerical-test coverage, and cross-ledger issues. |
| P28-I004 | Cross-ledger conflicts lacked propagation protocol. | ACCEPT | Added canonical `P28-I###` cross-ledger issue protocol with downstream re-review requirement. |
| P28-I005 | Numerical sanity-test audit lacked predeclared falsification checks. | ACCEPT | Added minimal test matrix with closed-form comparator, normalization, recursion, KR Jacobian, finite-difference, and negative-control requirements. |
| P28-I006 | Implementation-readiness audit could drift into prose. | ACCEPT | Required each implementation-relevant formula to map to inputs, outputs, shapes, primitive, stabilization, differentiability status, and implementability status. |
| P28-I007 | Persona review should also challenge plan coverage before execution. | PARTIAL | Direct Claude plan review already served as a pre-execution coverage challenge. No new persona loop added to avoid duplicating review; execution persona review remains required. |
| P28-I008 | Chair-reader audit could induce stylistic churn. | ACCEPT | Added boundary limiting chair-reader ledger to decision-relevant risks: unsupported claims, missing caveats, assumption/limitation narrative failures, correctness/plausibility/implementability rejection points. |

| Issue id | Claude execution finding summary | Codex classification | Patch/control added |
|---|---|---|---|
| P28-I020 | Inventory plus 522 critical/high-risk equations is coverage evidence, not correctness evidence. | ACCEPT | Result already says `NOT_READY_PATCH_REQUIRED`; strengthened final decision and allowed wording table. |
| P28-I021 | Proposition 2 is load-bearing and high-risk. | ACCEPT | Added P29 recommended scope requiring full Proposition 2 dependency graph audit. |
| P28-I022 | KR/preconditioning needs assumptions, invertibility, determinant convention, and failure modes. | ACCEPT | Added KR/preconditioning to required critical-equation audit scope and chair-reader blocker list. |
| P28-I023 | MathDevMCP scalar checks must not be presented as coverage of functional/matrix derivative chain. | ACCEPT | MathDevMCP ledger and result already narrow scope; strengthened wording in result. |
| P28-I024 | Implementation-readiness should be tiered as prototype-plausible, production-unverified. | ACCEPT | Implementation ledger already says prototype-ready not production-certified; strengthened final decision table. |
| P28-I025 | Need compact notation-shape contract for risky subsystems. | ACCEPT | Added to P29 recommended next action. |
| P28-I026 | Negative-control gap means P27 is not a sufficient validation oracle. | ACCEPT | Numerical sanity ledger records gap; final decision now marks it as required for testing-spec use. |
| P28-I027 | PDF text extraction is insufficient for equation-level source fidelity. | ACCEPT | Source-fidelity ledger already records limitation; final result now requires visual source audit for critical/high source-mapped equations. |
| P28-I028 | Need reconstructed/adapted/original/unaudited coverage table. | ACCEPT | Added to recommended P29 scope and final claim/evidence table. |
| P28-I029 | Algorithms 1, 2, and 5 need line-by-line provenance. | ACCEPT | Added to recommended P29 scope. |
| P28-I030 | Abstract/introduction/conclusion confidence would be risky if P27 implies full verification. | PARTIAL | P28 cannot rewrite P27 unless creating corrected candidate; result now says no corrected note was created and P27 should not be submitted as verified without either narrowing claim language or P29 audit. |
| P28-I031 | Need one-page decision table. | ACCEPT | Added claim/evidence/status table to P28 result. |
