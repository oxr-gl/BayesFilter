# P29 Claude Review Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

audit_scope:
- Claude hostile review of P29 critical-equation audit artifacts.

what_is_not_concluded:
- Claude review does not certify all equations.
- Claude review does not replace Codex audit judgment.

## Review Attempts

### Execution Review Iteration 1

Command `highdim-p29-critical-equation-audit-exec-review-iter1` used a direct self-contained prompt because prior Claude file-reading attempts in P28 often stalled. Claude agreed that `READY_WITH_TARGETED_LIMITATIONS` is appropriate only as a strictly scoped triage verdict, not as algorithm-level or document-level signoff.

## Codex Classifications

| issue id | Claude finding summary | Codex classification | Patch/control added |
|---|---|---|---|
| P29-I002 | Headline verdict can be misread as Algorithm 5 cleared despite P29-I001. | ACCEPT | Added front-page exclusion in result: no source-fidelity clearance for Algorithm 5(c.2) pending visual review. |
| P29-I003 | Need compact provenance table preventing broader Algorithm 1/2/5 claims. | ACCEPT | Added provenance decision table in result. |
| P29-I004 | Pass verdicts need assumption envelope. | ACCEPT | Added assumption envelope and non-claims to result. |
| P29-I005 | Notation-shape contract should become executable checks before code signoff. | ACCEPT | Added implementation-test requirement to result. |
| P29-I006 | KR/preconditioning needs direction ledger for map/inverse/Jacobian orientation. | ACCEPT | Added direction-ledger requirement in result and residual action list. |
| P29-I007 | MathDevMCP evidence must be segregated as sanity-check only. | ACCEPT | Added explicit sanity-check-only warning in result. |
| P29-I008 | Need decision table to prevent ledger promotion. | ACCEPT | Added claim/status/allowed/prohibited inference table. |
| P29-I009 | Residual risk from unaudited critical/high P28 displays must be operational. | ACCEPT | Added residual-risk register in result. |
