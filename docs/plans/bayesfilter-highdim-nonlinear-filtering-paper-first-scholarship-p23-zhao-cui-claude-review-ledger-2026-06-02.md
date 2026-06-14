# P23 Zhao--Cui Chemist And Implementation Gap-Closure Claude Review Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P22 integrated readable companion and fixed-branch gradient note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive branches.
- No HMC convergence claim.
- No production implementation readiness claim.
- No executable prototype claim.

## Status

Decision: `EXECUTION_REVIEW_ITERATION_3_ACCEPTED`.

Codex drafted the P23 plan with an explicit eleven-gap closure contract, P22
carry-forward guardrail, and Claude review protocol.

## Plan Review Iteration 1

Claude status: `REJECT`.

Codex audit decision: Codex independently agrees with all eight findings.
They identify review-control weaknesses rather than over-scoped preferences.

| Finding | Claude concern | Codex classification | Patch/control added |
|---|---|---|---|
| F1 preservation anchors missing | Copy-P22 guardrail lacked a reviewable section/equation preservation ledger. | `ACCEPT` | Added required P22 preservation ledger with inherited block rows, destination anchors, shortening checks, cross-reference replacement checks, and failure flags. |
| F2 count guardrail weak | P22 count baseline lacked exact artifact paths and validation table. | `ACCEPT` | Added exact P22 TeX/PDF paths and non-waivable count validation table requirement. |
| F3 veto power insufficient | Material Claude disputes could be closed too loosely. | `ACCEPT` | Added veto-blocker rule for P22 compression, missing closures, overclaims, and forbidden edits unless rebutted with anchors and rereviewed. |
| F4 non-gap control anchors missing | Non-claims, scope, allowed writes, and preservation controls needed exact anchors. | `ACCEPT` | Added required non-gap control anchors. |
| F5 minimum content vague | Some closures could be shallowly satisfied by headings. | `ACCEPT` | Added minimum-content contract table for all eleven gap closures. |
| F6 threaded example recurrence not validated | Example anchors alone would not prove threading through promised sections. | `ACCEPT` | Added recurrence table validation for filtering, squared-TT, preconditioning, and gradient reuse. |
| F7 cross-reference substitution not explicitly banned | P23 could replace P22 derivations with shorter references. | `ACCEPT` | Added explicit ban on replacing inherited derivations with shorter cross-references. |
| F8 unresolved findings stop condition missing | Iteration cap did not force blocked status for unresolved material issues. | `ACCEPT` | Added blocked/rejected outcome for unresolved accepted, partial, clarify, or material disputed findings at cap. |

No disputed findings in plan iteration 1.

Decision after patch: rerun Claude plan review.

## Plan Review Iteration 3

Claude status: `ACCEPT`.

Codex audit decision: Codex independently agrees.  The patched plan,
eleven-gap ledger, and P22 preservation ledger now contain exact enough
controls for hostile execution review.

Residual risks accepted for execution review:

- the ledger assertions still require TeX/PDF validation;
- count validation must be recorded after final build;
- inherited non-claim anchors must be confirmed in the P23 TeX/PDF.

No disputed findings in plan iteration 3.

## Execution Review Iteration 1

Claude status: `REJECT`.

Codex audit decision: Codex independently agrees with all eight findings.
The first, second, and sixth findings were completion-artifact gaps.  The
third through fifth, seventh, and eighth findings were substantive
self-containedness or implementation-specification gaps in the P23 note.

| Finding | Claude concern | Codex classification | Patch/control added |
|---|---|---|---|
| F1 pending status in artifacts | Result, eleven-gap ledger, and review ledger still reported pending execution/final validation. | `ACCEPT` | Updated ledgers/result toward completed-run state and replaced pending count-validation status with measured count evidence. |
| F2 result file incomplete | Completion artifact lacked build status, validation commands, execution review history, classification summary, files changed, and final residual gaps. | `ACCEPT` | Rewrote result file after patch/build/validation with completed evidence contract fields. |
| F3 sweep protocol underspecified | P23-SWEEP block did not define \(A_k\), \(d_k\), \(y_j\), or environment update recursion in place. | `ACCEPT` | Added P23-SWEEP1a--P23-SWEEP1h defining target vector, core matrices, left/right environments, design row, normal equations, and updates. |
| F4 retained-filter contract thin | Multidimensional \(Q_t\) was not derived from TT contractions or classified as exact versus surrogate. | `ACCEPT` | Added P23-MD4a--P23-MD4e deriving \(Q_t\) from retained interface expansion and non-retained square-mass contraction, with exact/surrogate condition. |
| F5 KR operational bridge missing | 2D KR example did not derive \(d_k(s\mid r_{<k})\) from squared-TT contractions. | `ACCEPT` | Added P23-KR2-8a--P23-KR2-8e deriving the two-dimensional conditional evaluator from the squared-TT mass contraction. |
| F6 count validation pending | Eleven-gap ledger still had `PENDING_FINAL_BUILD`. | `ACCEPT` | Replaced with passed count-validation row citing P22 4815/55 and P23 5715/65. |
| F7 derivative conditioning caveat light | Proposition 2 dependency graph did not foreground numerical conditioning risk. | `ACCEPT` | Added P23-GDAG2a and nearby mass-contraction caveat tying same-scalar math to conditioning diagnostics. |
| F8 running example callbacks weak | Later preconditioning and derivative sections used generic notation without re-instantiating the running example. | `ACCEPT` | Added P23-PREC10--P23-PREC11 and P23-GDAG8 to instantiate the running example in preconditioning and derivative sections. |

No disputed findings in execution iteration 1.

Decision after patch: rebuild and rerun Claude execution review.

## Execution Review Iteration 2

Claude status: `REJECT`.

Codex audit decision: Codex independently agrees with all three findings.
The findings are artifact-state blockers only; Claude did not identify a new
mathematical-gap blocker in the sampled patched note sections.

| Finding | Claude concern | Codex classification | Patch/control added |
|---|---|---|---|
| F1 result file still stub | Result still reported plan-rereview state and pending execution/final validation. | `ACCEPT` | Rewrote the result file as a completed post-patch result note with build, validation, review history, classification summary, files changed, residual gaps, and decision fields. |
| F2 review/discrepancy artifacts stale | Review ledger header and discrepancy report did not record execution review iteration 1 and patch cycle. | `ACCEPT` | Updated review ledger status and discrepancy report to record execution-review rejection/patch cycles and current rereview status. |
| F3 count-validation numbers stale | Eleven-gap ledger still cited the pre-patch P23 count of 5715 lines and 65 pages. | `ACCEPT` | Updated count-validation row to final measured values: P22 4815 TeX lines/55 pages; P23 5966 TeX lines/67 pages, measured by `wc -l` and `pdfinfo`. |

No disputed findings in execution iteration 2.

Decision after patch: rerun Claude execution review.

## Execution Review Iteration 3

Claude status: `ACCEPT`.

Codex audit decision: Codex independently agrees.  The iteration-2
artifact-state blockers are patched, final count-validation evidence is
consistent across the result and eleven-gap ledger, and no remaining blocker
was identified.

Residual limits accepted:

- Claude did not rerun validation commands; Codex validation commands supply
  the recorded evidence.
- Claude sampled the note/PDF rather than re-auditing every page.
- The artifact remains a mathematical/specification companion, not executable
  or empirical validation evidence.

## Plan Review Iteration 2

Claude status: `REJECT`.

Codex audit decision: Codex independently agrees with all three findings.
They identify real auditability gaps in the plan/ledger controls rather than
style preferences.

| Finding | Claude concern | Codex classification | Patch/control added |
|---|---|---|---|
| F1 cross-reference-only preservation loophole | The plan allowed `cross_referenced_without_replacement`, which could satisfy a required inherited block by pointer rather than by preserving P22 content. | `ACCEPT` | Removed cross-reference-only status for required inherited P22 spine rows in the plan. Required rows are now only `copied_verbatim` or `extended_in_place`; substantive cross-reference-only substitution is an automatic failure. |
| F2 preservation ledger not exact-anchor auditable | The P22 preservation ledger used bundled ranges and phrases like `same anchors`, preventing mechanical inheritance checks. | `ACCEPT` | Replaced the preservation ledger with an exact inherited-anchor table listing source and destination anchors per block row, with shortening and cross-reference replacement fields retained. |
| F3 eleven-gap ledger not payload-level auditable | The eleven-gap ledger listed anchor families but did not map each minimum payload requirement to exact anchors. | `ACCEPT` | Expanded the eleven-gap ledger into a payload checklist keyed to exact anchors, with evidence notes and failure flags; non-gap controls now cite exact non-claim anchors. |

No disputed findings in plan iteration 2.

Decision after patch: rerun Claude plan review.
