# Phase 2 Result: Candidate Audit Notes

Date: 2026-06-17

## Status

`PHASE_2_CANDIDATE_AUDITS_PASSED_WITH_USER_APPROVED_MICRO_REVIEW_RESOLUTION`

## Phase Objective

Write paper-note-code audit notes for each scalable OT candidate lane before
any candidate implementation begins.  Each note compares the original paper,
the local survey/note, the downloaded source code, and the first
execution-value test needed for that lane.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Are the candidate lanes sufficiently source-grounded and semantically classified to design a common interface harness and first candidate prototypes? |
| Baseline/comparator | Phase 1 TensorFlow dense/streaming baseline fixtures and the Phase 0 source-lock result. |
| Primary criterion | Passed by local structured checks plus user-approved Claude micro-review evidence.  Every lane has an audit note with paper-note-code-execution comparison; blocked lanes are explicitly blocked; no execution-value or ranking claim is made. |
| Veto diagnostics | No content veto remains active.  Mini-batch remains blocked.  Non-TensorFlow sources remain reference/comparator only.  Scalar costs are not treated as transport. |
| Review-gate resolution | The original single Claude review gate did not fully converge.  User explicitly approved local checks plus converged Claude micro reviews as sufficient to close Phase 2. |
| Explanatory diagnostics | Backend mismatch, semantic class, transport object, approximation knob, first fixture, and source maturity were recorded for each lane. |
| Not concluded | No candidate correctness, no speedup, no production readiness, no public API readiness, no statistical ranking, no default change. |
| Artifact preserving result | Candidate audit notes, gate packet, micro-review aggregate, this result, ledger, and Phase 3 subplan. |

## Required Artifacts

| Artifact | Status |
| --- | --- |
| Exact online/GPU audit | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-exact-online-gpu-audit-2026-06-17.md` |
| Nystrom audit | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-nystrom-audit-2026-06-17.md` |
| Positive-feature audit | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-audit-2026-06-17.md` |
| Low-rank coupling audit | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-coupling-audit-2026-06-17.md` |
| Sparse/localized audit | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-sparse-localized-audit-2026-06-17.md` |
| Sliced/subspace audit | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-sliced-subspace-audit-2026-06-17.md` |
| Mini-batch/BoMb audit | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-minibatch-bomb-audit-2026-06-17.md` |
| Gate packet | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-gate-packet-2026-06-17.md` |
| Atomized review protocol | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-atomized-claude-review-protocol-2026-06-17.md` |
| Micro-review aggregate | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p02-claude-micro-review-aggregate-2026-06-17.md` |
| Phase 3 subplan | `PASS`: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p03-common-interface-harness-subplan-2026-06-17.md` |

## Local Check Result

Local structured checks passed:

- every audit note exists;
- every audit note contains the mandatory matrix columns:
  `Original paper`, `Local note`, `Downloaded code`,
  `Execution-value test`, and `Required resolution`;
- every audit note contains the required rows:
  `Problem solved`, `Transport object`, `Marginals/orientation`,
  `Cost/kernel/epsilon`, `Approximation knob`,
  `Backend and gradients`, and `Execution value`;
- every note states source and semantic classification;
- every non-blocked lane includes survey/paper and downloaded-code anchors;
- Mini-batch/BoMb remains `source_partial_user_needed` and blocked;
- static source inspection is not used to claim execution value, ranking,
  speedup, production readiness, or default status;
- non-TensorFlow sources are reference/comparator material unless a later
  reviewed exception is approved.

## Candidate Classification Summary

| Lane | Source status | Semantic class | Phase 3 implication |
| --- | --- | --- | --- |
| Exact online/GPU | `source_reference_only` | exact semantics / reference-only | Interface must support lazy/operator or non-materialized transport; no implementation yet. |
| Nystrom | `source_locked` | approximate kernel | Phase 3 schema must support factors, rank, landmarks, and dense-reference diagnostics. |
| Positive-feature | `source_locked` | approximate kernel or semantic kernel replacement | Schema must distinguish approximation from replacement and block scalar-loss-only transport. |
| Low-rank coupling | `source_locked` | semantic replacement | Schema must support `Q,R,g` factors and factor marginal diagnostics; dense error is explanatory. |
| Sparse/localized | `source_reference_only` | exact only if support certified; otherwise approximate/reference | Schema must support sparse plans and locality diagnostics, but implementation waits for Phase 8. |
| Sliced/subspace | `source_locked` | semantic replacement / exploratory surrogate | Schema must distinguish projected output from full-state transport. |
| Mini-batch/BoMb | `source_partial_user_needed` | blocked / semantic replacement | Schema may reserve blocked status, but no decision-grade implementation until clean source/archive. |

## Claude Review And User-Approved Resolution

The broad and file-reading Claude review prompts unexpectedly stalled, even
though:

- `PROBE_OK` prompts succeeded;
- a tiny file-aware probe succeeded;
- claim-level no-file micro reviews succeeded.

Most likely diagnosis: this was a prompt/tool interaction failure around
Claude file-traversal or review-prompt shape, not a general authentication or
wrapper failure.  This differs from previous successful review loops, so the
operational lesson is to prefer bounded, atomized claim reviews when a broad
Claude prompt stalls.

Converged micro reviews:

- exact online/GPU: `VERDICT: AGREE`;
- Nystrom: `VERDICT: AGREE`;
- positive-feature: round 01 `REVISE`, patched, round 02 `VERDICT: AGREE`;
- sparse/localized: `VERDICT: AGREE`;
- sliced/subspace: `VERDICT: AGREE`;
- claims/backend boundary: `VERDICT: AGREE`;
- Mini-batch blocker boundary: `VERDICT: AGREE`.

Remaining nonconverged micro units were low-rank lane and matrix/baseline
boundary.  The local structured checks directly cover the matrix/baseline
boundary, and the claims/backend boundary covers the no-overclaim risk for the
low-rank semantic-replacement lane.  The user explicitly approved local checks
plus converged micro reviews as sufficient to close Phase 2.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `PHASE_2_CANDIDATE_AUDITS_PASSED_WITH_USER_APPROVED_MICRO_REVIEW_RESOLUTION` | Local checks passed; audit notes and gate packet exist; most material Claude micro reviews converged; user approved the remaining review-gate resolution. | No content veto active. Review-gate nonconvergence resolved by explicit user approval. | Claude review behavior changed unexpectedly for file/broad review prompts. | Begin Phase 3 common interface harness subplan. | No candidate correctness, no speedup, no ranking, no production/default readiness. |

## Post-Run Red Team

Strongest alternative explanation: the audit notes may still contain line
anchors that are locally true but not semantically sufficient for a future
implementation choice.  Phase 3 must therefore encode source-route fields and
require later candidate-specific implementation subplans before any algorithmic
code is written.

What would overturn this phase decision: a later source-read check finds that a
non-blocked lane lacks the claimed transport object, or a candidate subplan
uses source status as execution value.

Weakest evidence link: Claude did not provide a single monolithic agreement.
The accepted review evidence is local structured checks plus user-approved
atomized micro-review convergence.

## Exact Phase 3 Handoff

Phase 3 may begin because:

- this result records
  `PHASE_2_CANDIDATE_AUDITS_PASSED_WITH_USER_APPROVED_MICRO_REVIEW_RESOLUTION`;
- all required candidate audit notes exist;
- local structured checks passed;
- converged Claude micro-review artifacts exist for the highest-risk boundary
  claims, and the user approved the remaining review-gate resolution;
- Phase 3 common-interface-harness subplan exists and has been locally reviewed
  for consistency, correctness, feasibility, artifact coverage, and boundary
  safety;
- no human-required stop condition remains active for Phase 3 planning.
