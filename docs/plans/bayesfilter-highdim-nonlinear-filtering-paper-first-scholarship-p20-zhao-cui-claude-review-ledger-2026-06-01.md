# P20 Zhao--Cui Claude Review Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P18 true annotated Zhao--Cui companion note and ledgers.
- P19 chair-readable fixed-branch gradient note and ledgers.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross/rank/pivot/domain
  choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No empirical validation on BayesFilter target models.

## Plan Review Iteration 1

Claude status: `REJECT`.

Codex audit decision: Codex agrees with the rejection.  The original P20 plan
had the right direction but did not make the merge enforceable enough.  In
particular, "longer than P18" was too weak, and generic P18/P19 presence checks
could still permit compression.

| Finding | Claude summary | Codex classification | Control added |
|---|---|---|---|
| P20-V1 | Size gate was not merge-grade; longer than P18 could still drop P19 material. | `ACCEPT` | Added merge-aware size lower bound: P20 must be at least P18 + P19 - replaced P18 tail, with arithmetic logged in the size ledger. |
| P20-V2 | P18 preservation language was too generic and could allow source-order reconstruction to collapse into summary. | `ACCEPT` | Added mandatory P18 carry-forward map for each source-order section/unit and source-coverage appendix. |
| P20-V3 | P19 carry-over contract was too coarse and could lose accepted gradient details. | `ACCEPT` | Added exact P19 import checklist including warmups, design-row derivation, carried-marginal derivative, propositions, finite-difference semantics, and minimal example. |
| P20-N1 | Duplicate-tag control direction is correct. | `ACCEPT` | Kept P19 tag-prefix and duplicate-tag validation requirements. |
| P20-N2 | Fixed-branch semantics are correctly stated. | `ACCEPT` | Added the exact rule to the P19 import checklist and validation. |
| P20-N3 | Codex-supervisor audit protocol is present. | `ACCEPT` | No patch needed beyond retaining the protocol. |

No disputed findings in iteration 1.

## Plan Review Iteration 2

Claude status: `REJECT`.

Codex audit decision: Codex agrees with the remaining veto.  The merge-aware
gate is necessary but not sufficient: the user's plain expectation that P20 be
longer than P18 must also be a hard validation check.  Codex also accepted the
non-veto request to make P18 carry-forward validation more than a presence scan.

| Finding | Claude summary | Codex classification | Control added |
|---|---|---|---|
| P20-V4 | The merge-aware lower bound could still be gamed by overestimating the replaced P18 tail; direct P20 > P18 checks were missing. | `ACCEPT` | Added hard-fail criteria: P20 TeX lines must exceed P18 lines; P20 PDF pages must be at least P18 pages; replacement subtraction may use only the named derivative/diagnostic/minimal-example/conclusion tail. |
| P20-N1 | P18 carry-forward validation needed to check order and substance, not only PDF text presence. | `ACCEPT` | Added Codex-side validation that the merge ledger preserves P18 block order and maps each block to a substantive carried section, not a summary placeholder. |

No disputed findings in iteration 2.

## Plan Review Iteration 3

Claude status: `ACCEPT`.

Codex audit decision: Codex agrees.  The plan now has direct hard gates for
P20 being longer than P18, merge-aware size bounds, exact P18 carry-forward and
P19 import checklists, duplicate-tag validation, bounded writes, and the
Codex-supervisor audit protocol.

No disputed findings in iteration 3.

## Execution Review Iteration 1

Claude status: `REJECT`.

Codex audit decision: Codex agrees with the rejection, but it is narrow.  The
review found that P20 is a real merge, P18's source-order reconstruction is
preserved, P19's accepted gradient material is imported, fixed-branch semantics
are correct, and no duplicate tags were found.  The blocking issue was that the
size ledger did not explicitly compute the merge-aware PDF page lower bound
required by the plan.

| Finding | Claude summary | Codex classification | Control added |
|---|---|---|---|
| F01 | The size ledger records P18/P19/P20 page counts but omits the replaced-tail page estimate, method, and required P20 page lower bound. | `ACCEPT` | Patched the size ledger to record a 5-page rendered-tail estimate, the method using P18 PDF page anchors plus line-proportional corroboration, and the inequality \(49 \ge 37+17-5=49\). |
| F02 | Chemistry persona could teach the same-scalar story, but wanted the fixed finite composition of ridge solves to be stated as a short differentiability lemma. | `PARTIAL` | Added a reader-facing lemma before Proposition 2 proving differentiability of a fixed ridge solve and a fixed finite sweep under nonsingular ridge systems. This was not treated as a veto because Claude explicitly said it would accept after F01, but Codex patched it because it improves chair readability. |

No disputed findings in iteration 1.

## Execution Review Iteration 2

Claude status: `ACCEPT`.

Codex audit decision: Codex independently agrees with the acceptance.  The
iteration-1 blocking ledger issue was patched, the chair-readability
differentiability point was strengthened, and no remaining substantive merge,
math, readability, tag, size, or ledger blocker was identified.

| Check | Claude summary | Codex classification | Evidence |
|---|---|---|---|
| F01 closure | The size ledger now records the 5-page replaced-tail estimate, page-estimate method, and merge-aware page inequality \(50 \ge 37+17-5=49\). | `ACCEPT` | Size ledger `Size Gate` table and inequalities. |
| Chair-readability patch | The fixed-ridge-sweep lemma materially improves the teachability of the finite-composition differentiability step. | `ACCEPT` | P20 note lemma `Fixed ridge sweeps are differentiable maps` before Proposition 2. |
| Merge integrity | P20 remains a real P18+P19 merge, not a supplement or compression. | `ACCEPT` | Merge ledger maps P18 spine and P19 gradient imports; P20 source is 4295 lines and PDF is 50 pages. |
| Same-scalar semantics | The note consistently freezes structural branch choices while recomputing fitted core values under the same fixed fitting rule. | `ACCEPT` | Bridge section, Proposition 2, and finite-difference protocol. |
| Tag hygiene | 288 equation tags and zero duplicate tags. | `ACCEPT` | Size ledger `Equation Tag Gate`; Codex validation repeated the duplicate-tag scan. |

No disputed findings in iteration 2.

Final review-loop status: `ACCEPTED_AFTER_EXECUTION_REVIEW_ITERATION_2`.
