# P22 Zhao--Cui Integrated Readable Companion Claude Review Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.
- P21 chair guide and implementation-ready mathematical specification.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive branch choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No executable prototype claim.

## Plan Review Iteration 1

Claude status: `REJECT`.

Codex audit decision: Codex independently agrees with all three findings.

| Finding | Claude concern | Codex classification | Patch/control added |
|---|---|---|---|
| F1 anti-summary validation not enforceable | The plan said not to summarize P20 but did not require a carry-forward audit or P20/P22 size validation. | `ACCEPT` | Added a required P20 carry-forward map, required P20 vs P22 TeX line and PDF page counts, and vetoes for incomplete carry-forward or shorter P22. |
| F2 P21 implementation controls not field-level validated | The plan named carried-filter and finite-difference controls but did not require checking each required field. | `ACCEPT` | Added required field-level implementation controls for \(Q_t,\dot Q_t,P_t,\dot P_t\), query basis, evaluator outputs, next-step query rule, scalar, derivative, manifest, recompute-core rule, step sizes, errors, pass/fail status, trend, failures, and non-conclusions. |
| F3 trusted Claude execution missing | The plan did not state Claude reviews must be run with elevated/trusted permissions under repo policy. | `ACCEPT` | Added trusted/elevated Claude worker requirement and sandbox-failure caveat under review protocol. |

No disputed findings in iteration 1.

Decision after patch: rerun Claude plan review.

## Plan Review Iteration 2

Claude status: `ACCEPT`.

Codex audit decision: Codex independently agrees.  The patched plan now has
enforceable anti-summary validation, field-level implementation-control
validation, and trusted Claude-worker requirements.

| Review point | Claude summary | Codex classification | Codex audit |
|---|---|---|---|
| Anti-summary validation | Required P20 carry-forward map, failure flags, and P20/P22 line/page count validation are now present. | `ACCEPT` | The plan now makes summarization reviewable rather than aspirational. |
| Field-level implementation controls | Carried-filter and finite-difference schema fields must each have exact P22 anchors. | `ACCEPT` | This preserves the implementation-critical gains from P21. |
| Trusted Claude execution | Plan and execution reviews must run with elevated/trusted permissions; non-trusted failures are sandbox evidence only. | `ACCEPT` | This matches repository cross-agent policy. |

Residual non-blocking risk:

- The carry-forward map still requires human/Codex judgment rather than a
  semantic diff, but its required rows and failure flags are sufficient for
  execution.

Final plan-review status: `ACCEPTED_AFTER_PLAN_REVIEW_ITERATION_2`.

## Execution Review Iteration 1

Claude status: `REJECT`.

Codex audit decision: Codex independently agrees with the three blockers.

| Finding | Claude concern | Codex classification | Patch/control planned |
|---|---|---|---|
| F1 executable/runnable framing | P22 still had runnable-example, required-output, and procedural-forward-step language, which conflicted with the non-code framing. | `ACCEPT` | Rewrite runnable/procedural language into non-executable mathematical example and object-flow language. |
| F2 residual audience-coaching tone | P22 still has reader-facing/readability-targeted titles and inherited chemistry-chair framing signals. | `ACCEPT` | Rename remaining titles and phrases to neutral academic language. |
| F3 FD ledger exact-anchor inconsistency | The implementation ledger claims exact P22 anchors but uses inherited P19 anchors for several finite-difference fields. | `ACCEPT` | Add P22-local finite-difference field anchors in the note and update the ledger to cite them explicitly. |

No disputed findings in execution iteration 1.

Decision after patch: rerun Claude execution review.

## Invalid Execution Review Attempt

One attempted iteration-2 Claude command was invalid because shell backticks in
the prompt caused Bash command substitution before the prompt reached Claude.
Codex did not treat that run as a content review.  A quote-safe clean
iteration-2 review was launched instead.

## Execution Review Iteration 2

Claude status: `REJECT`.

Codex audit decision: Codex independently agrees.  The main TeX content was
materially improved, but the package documentation still had control
inconsistencies.

| Finding | Claude concern | Codex classification | Patch/control added |
|---|---|---|---|
| F1 FD ledger still cited inherited P19 anchors | Branch-manifest equality and failure-interpretation rows still included P19 anchors despite the plan requiring exact P22 anchors. | `ACCEPT` | Updated implementation-specification ledger to cite P22-FD2 and P22-FD2--P22-FD5 plus local explanatory text only. |
| F2 stale size metrics | Result and integration ledgers reported old P22 line counts rather than the then-current post-patch line/page count. | `ACCEPT` | Updated integration ledger and result artifact after iteration 2; the later iteration-4 patch records the current count. |
| F3 status artifacts stale | Result, discrepancy, and review ledger still described an unfinished rerun state. | `ACCEPT` | Updated status artifacts to record iteration-2 rejection and post-patch rerun-ready state. |

No disputed findings in execution iteration 2.

Decision after patch: rerun Claude execution review with quote-safe prompt.

## Execution Review Iteration 5

Claude status: `ACCEPT`.

Codex audit decision: Codex independently agrees.  The exact-anchor blocker
from iteration 4 is resolved, the size guardrail still passes, and no new
blocking finding was raised.

| Review point | Claude finding | Codex classification | Codex audit |
|---|---|---|---|
| Finite-difference exact anchors | The three ledger rows now cite P22-FD8, P22-FD9, and P22-FD7 exactly, with no prose-span fallback. | `ACCEPT` | The implementation-specification ledger now satisfies the field-level-anchor contract. |
| P20/P22 size and expansion | P20 is 4295 TeX lines / 50 pages; P22 is 4815 TeX lines / 55 pages. | `ACCEPT` | The anti-summary size guardrail passes. |
| P20/P21 integration | P22 preserves the source-order P20 spine and integrates P21 carried-filter and report-shape controls. | `ACCEPT` | The integration ledger and note anchors support this at review level. |
| Tone and non-executable framing | Earlier runnable, script-like, and condescending framing is absent from P22. | `ACCEPT` | Local grep and Claude review agree. |
| Overclaim controls | P22 still states no exact posterior accuracy, no adaptive-branch global differentiability, no HMC convergence, no production readiness, and no executable prototype. | `ACCEPT` | These non-claims are explicit in the note and ledgers. |

Residual risks recorded from Claude:

- Review scope was artifact-consistency, not a line-by-line semantic diff of
  every P20 line against P22.
- Claude did not rerun `latexmk`; Codex separately did.
- No executable-code concern remains at the document level, but formulas remain
  mathematically operationalizable by design.
- Nearby inherited P19 tags remain in the note, but the required P22
  implementation-ledger fields now cite exact P22 anchors.
- This review did not independently rederive every mathematical proposition.

Final Claude execution-review status:
`ACCEPTED_AFTER_EXECUTION_REVIEW_ITERATION_5`.

## Execution Review Iteration 4

Claude status: `REJECT`.

Codex audit decision: Codex independently agrees.  Claude identified one
remaining field-level-anchor blocker in the implementation ledger.

| Finding | Claude concern | Codex classification | Patch/control added |
|---|---|---|---|
| F1 exact finite-difference anchors incomplete | The implementation-specification ledger still used prose spans or section-title fallback for expected decreasing-error trend, failure interpretations, and finite-difference non-conclusions. | `ACCEPT` | Added exact note anchors P22-FD7 for finite-difference non-conclusions, P22-FD8 for the decreasing-error trend criterion, and P22-FD9 for failure interpretations. Updated the ledger to cite only those exact anchors. |

No disputed findings in execution iteration 4.

Current size after the iteration-4 patch: P22 is 4815 TeX lines and 55 PDF
pages, still longer than P20's 4295 TeX lines and 50 PDF pages.

Decision after patch: rerun Claude execution review with quote-safe prompt.

## Execution Review Iteration 3

Claude status: `REJECT`.

Codex audit decision: Codex independently agrees.  The P22 package was close,
but the remaining issues were real consistency defects rather than stylistic
preferences.

| Finding | Claude concern | Codex classification | Patch/control added |
|---|---|---|---|
| F1 code-like finite-difference vocabulary | The main note still used code-like vocabulary and typewriter status labels in the finite-difference diagnostic. | `ACCEPT` | Replaced typewriter/code status labels with mathematical prose labels: branch identity failure, copied-core failure, decreasing-window agreement, and inconclusive no-decreasing-window. |
| F2 stale status language | Markdown artifacts still described the package as ready after iteration 2 rather than after the iteration-3 cleanup. | `ACCEPT` | Advanced result and discrepancy decisions to the iteration-3 rereview-ready state and refreshed the size metrics; the later iteration-4 patch records the current count. |
| F3 branch identity not local enough | The finite-difference branch condition needed to state the local equality for the same P22 branch object and scalar. | `ACCEPT` | Retained and foregrounded P22-FD6: \(B(\beta_0)=B(\beta_0+h)=B(\beta_0-h)=B\), with explanatory text that changing ranks, points, shifts, or domains changes the object being compared. |

No disputed findings in execution iteration 3.

Decision after patch: rerun Claude execution review with quote-safe prompt.
