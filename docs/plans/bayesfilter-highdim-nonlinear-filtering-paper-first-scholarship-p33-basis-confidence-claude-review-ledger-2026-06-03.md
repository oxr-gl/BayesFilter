# P33 Basis-Choice Confidence Claude Review Ledger

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Trefethen, *Approximation Theory and Approximation Practice*.
- Xiu and Karniadakis, "The Wiener--Askey Polynomial Chaos for Stochastic Differential Equations."

what_is_not_concluded:
- Claude review does not certify mathematical correctness by itself.
- Claude review is a hostile review aid; Codex remains final authority.

## Review Rounds

| phase | iteration | status | Claude findings | Codex audit |
|---|---:|---|---|---|
| plan | 1 | `CLAUDE_WORKER_STALLED_TERMINATED` | No findings returned after several minutes; worker process was terminated by Codex. | Not treated as review or convergence.  Retried with a narrower prompt. |
| plan | 2 | `REVIEW_RETURNED_ACTIONABLE_FINDINGS` | 3 blocker themes, 8 major/minor themes: add explicit 11-issue ledger; define residual norms/measures; add quadrature/discretization checks; operationalize conditioning/ridge/veto/tie-breaks; distinguish basis vs rank insufficiency; add tensor shapes/index conventions; define learned-basis freeze boundary; add PDF-text validation anchors; define allowed files; add panel-facing conclusion. | `ACCEPT`: findings 1,2,3,4,5,7,8,9,10,12,13,14,15. `PARTIAL`: finding 11 because allowed writes already existed but needed a sharper validation statement. Plan patched before execution. |
| plan | 3 | `CONDITIONAL_APPROVE_WITH_COHERENCE_BLOCKER` | Blocker: reconcile old P30 basis subsection with new P33 framework. Major: add exact fitted scalar, concrete quadrature exactness example, deterministic no-pass fallback and derivative-parity scope, learned-basis optional/non-default scope. Minor: harmonize \(\mathcal H\)/\(\mathfrak D\), vectorization range, rank-saturation scope, basis-vs-map distinction. | `ACCEPT`: all findings. P33 plan and P30 note patched before execution review. |
| execution | 1 | `REVIEW_RETURNED_TARGETED_FINDINGS` | Blockers: result ledger still pending; source ledger claim mapping incomplete. Majors: governance/process wording in main note; old/new basis protocols only partially reconciled; background citations need local scope sentence; 11-question table lacks separate decisive-equations field. Minors: \(r_k\)/\(z_k\) bridge, aggregate \(\delta_{\rm quad}^{(q)}\), optional learned-basis status in formal subsection, plain-language bridge after fitted scalar. | `ACCEPT`: all findings. P30 note and P33 ledgers patched; execution review rerun required. |
| execution | 2 | `REJECT_WITH_STALE_LEDGER_FINDINGS_ONLY` | Blocker: result ledger still said `PENDING_FINAL_REVIEW_AFTER_PATCH` and validation/review remained outstanding. Major: Claude review ledger had not recorded execution iteration 2. Claude explicitly stated this was a package-level reject, not a math-content reject, and that the substantive P30 basis section was strong enough. | `ACCEPT`: both findings. Patched result ledger with final validation status and patched this review ledger with execution iteration 2 details. |
| execution | 3 | `ACCEPT` | Narrow review confirmed both iteration-2 package-state findings are closed and found no overclaim of final acceptance before iteration 3. | Codex agrees. Patch final result status from pending iteration 3 to accepted. |

## Codex Plan-Review Audit Details

| Claude finding | classification | Codex action |
|---|---|---|
| Add explicit 11-issue checklist | ACCEPT | Add Section J to the P33 plan. |
| Define residual norm/measures and relation to projection error | ACCEPT | Add requirements in Sections D/F. |
| Add quadrature/discretization assumptions and aliasing checks | ACCEPT | Add requirements in Sections C/F. |
| Operationalize conditioning/ridge policy | ACCEPT | Add deterministic thresholds/veto language. |
| Distinguish basis misfit from rank misfit | ACCEPT | Add discrimination ladder. |
| Warn orthogonality depends on pulled-back measure | ACCEPT | Add taxonomy requirement. |
| Deterministic candidate ordering/tie-breaks | ACCEPT | Add selection rule requirement. |
| Explicit tensor shapes and index conventions | ACCEPT | Add Section B shape requirements. |
| Learned-basis freeze boundary | ACCEPT | Add frozen artifact requirement. |
| PDF-text confirmation ledger | ACCEPT | Add validation anchors. |
| Allowed file set undefined | PARTIAL | Existing allowed writes existed; strengthen validation. |
| Panel-facing synthesis | ACCEPT | Add conclusion requirement. |
| Compare against one arbitrary basis | ACCEPT | Add candidate-family comparison requirement. |
| Scope literature recommendations | ACCEPT | Add scoped-citation requirement. |

## Codex Plan-Review Iteration 3 Audit Details

| Claude finding | classification | Codex action |
|---|---|---|
| Reconcile older P30 basis subsection with P33 audited design tuple | ACCEPT | Patched P30 to use \(\mathfrak D\) in `eq:p30-basis-hyper`, state that `eq:p33-design-tuple` is the expanded audited version, and remove competing \(\mathcal H\) language. |
| State exact fitted scalar in core regression | ACCEPT | Added `eq:p33-fitted-scalar`, defining \(y_j=e^{c/2}\sqrt{\widetilde q_\nu(z^{(j)})}\), with measure-consistency warning. |
| Add concrete quadrature exactness example | ACCEPT | Added Legendre mass-degree and Gauss--Legendre threshold equations `eq:p33-legendre-mass-degree` and `eq:p33-legendre-quadrature-threshold`. |
| Define no-pass fallback and derivative-parity scope | ACCEPT | Added `eq:p33-no-candidate` and text requiring no accepted basis if all candidates fail; derivative parity is a veto when gradients are reported or used. |
| Learned-basis discussion needs optional/non-default boundary | ACCEPT | Patched earlier learned-basis paragraph to state it is optional and non-default absent an accepted pilot study. |
| Harmonize notation and vectorization range | ACCEPT | Added one-framework statement and `eq:p33-vectorization-range`. |
| Rank saturation should be relative to declared budget | ACCEPT | Added text that rank saturation is not proof that TT structure fails at all budgets. |
| Distinguish bad basis from bad coordinate map/preconditioner | ACCEPT | Added basis-vs-geometry distinction before the discrimination ladder. |

## Codex Execution-Review Iteration 1 Audit Details

| Claude finding | classification | Codex action |
|---|---|---|
| P33 result ledger still pending | ACCEPT | Replaced pending status with execution result, review history, validation, and remaining gaps. |
| P33 source ledger claim mapping incomplete | ACCEPT | Filled source/claim mapping with P30 section and equation anchors. |
| Governance/process wording remains in main note | ACCEPT | Renamed and rewrote basis selection prose to mathematical language: controlled approximation, selection criteria, stored record, satisfying candidate; removed visible `artifact` wording. |
| Old preview subsection and P33 formal protocol overlap | ACCEPT | Added sentence that the earlier subsection is a readable preview and that \S\ref{subsec:p33-complete-basis-audit} is the authoritative specification. |
| Background citations need local scope sentence | ACCEPT | Added sentence after approximation-literature citations that they support only heuristics/background, not correctness/optimality for nonlinear filtering. |
| 11-question checklist lacks separate decisive-equations field | ACCEPT | Split table into `Question`, `Section`, `Decisive equations`, and `Diagnostic`. |
| \(r_k\)/\(z_k\) bridge missing | ACCEPT | Added bridge explaining Legendre example uses physical interval coordinates while formal specification uses basis coordinates. |
| \(\delta_{\rm quad}^{(q)}\) used before definition | ACCEPT | Added aggregate quadrature diagnostic `eq:p33-quadrature-aggregate`. |
| Learned-basis formal subsection should restate optional/non-default status | ACCEPT | Added opening line to `Learned Bases And The Freeze Boundary`. |
| Plain-language bridge after fitted scalar | ACCEPT | Added sentence that the regression target is the square root of the density in the same coordinates and measure as the basis and mass matrices. |

## Codex Execution-Review Iteration 2 Audit Details

| Claude finding | classification | Codex action |
|---|---|---|
| Result ledger still marked P33 as pending, with validation and execution-review iteration 2 listed as outstanding. | ACCEPT | Replaced the pending result status with final post-patch status, validation commands, and remaining nonblocking limitations. |
| Claude review ledger still ended at execution iteration 1. | ACCEPT | Added execution iteration 2 row and this Codex audit table. |

Claude substantive review conclusion: the note itself is close to accept; the
11 basis-choice issues are addressed with equations and diagnostics; learned
bases are optional and frozen before fixed-branch differentiation; the frozen
and moving-basis derivative equations are separated correctly at note level;
and no forbidden visible governance/process words were found in the main basis
prose.  The rejection was only because the review package had stale ledger
status text before this patch.

## Codex Execution-Review Iteration 3 Audit Details

| Claude finding | classification | Codex action |
|---|---|---|
| Both iteration-2 package-state findings are closed. | ACCEPT | Record execution iteration 3 as accepted. |
| Result ledger did not overclaim final acceptance before iteration 3. | ACCEPT | Update result ledger to final accepted status after this review. |
