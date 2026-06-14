# P18 Zhao--Cui Claude Review Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao--Cui code audit and paper-code crosswalk ledgers.
- P15 fixed-branch implementation contract.
- P17 full-equation reconstruction note and ledgers.

what_is_not_concluded:
- No claim that the adaptive Zhao--Cui implementation is globally differentiable.
- No claim that fixed-branch differentiation proves exact posterior accuracy.
- No claim that BayesFilter has production tensor-train filtering code.
- No claim that Zhao--Cui has been validated on BayesFilter target models.
- No default-method recommendation.

## Plan Review Iteration 1

Claude status: `REJECT`.

Codex audit decision: Claude's rejection is materially correct.  P18 needs
stronger scholarly traceability, stricter equation-count rules, explicit
source-unit markers, implementation contracts, non-waivable veto handling, and a
testable chemistry-reader rubric.

| Finding | Claude summary | Codex classification | Control added |
|---|---|---|---|
| P18-PLAN-1 | Missing required literature ledgers and quarantine checks. | `ACCEPT` | Added six literature ledgers, source/version/quarantine checks, and blocker rule. |
| P18-PLAN-2 | Equation-count gate can be gamed. | `ACCEPT` | Added counting rules: one mathematical claim per display; cosmetic splits do not count; each added equation must serve a source-unit derivation step. |
| P18-PLAN-3 | Source-unit granularity still allows collapsed reconstruction. | `ACCEPT` | Added mandatory explicit source-unit marker for every material source unit, with cross-reference only after its own derivation/explanation. |
| P18-PLAN-4 | Implementability without original paper not fully enforced. | `ACCEPT` | Added mini implementation contract for each algorithmic math line: inputs, outputs, persisted state, operation, dependencies. |
| P18-PLAN-5 | Claude veto power can be weakened procedurally. | `ACCEPT` | Added non-waivable veto block: any Claude veto item blocks final acceptance until patched and no longer flagged, unless human overrides. |
| P18-PLAN-6 | Original technical text inspection and claim mapping not explicit enough. | `ACCEPT` | Added rule mapping every important claim to Zhao--Cui identifiers or fresh project derivation in claim-support ledger. |
| P18-PLAN-7 | Chemistry-reader requirement subjective. | `ACCEPT` | Added binary chemistry persona rubric. |
| P18-PLAN-8 | Fixed-branch separation not structurally enforced. | `ACCEPT` | Added hard section boundary, frozen equation-count point, and prohibition on anticipatory adaptive differentiability claims. |
| P18-PLAN-9 | Validation too structure-oriented. | `ACCEPT` | Added ledger-level reconciliation and hostile spot-audit sampling rows from each section. |

No disputed findings.

## Execution Review Iteration 1

Claude status: `REJECT`.

Codex audit decision: Claude's rejection is materially correct.  The P18 draft
is substantially better than P17, but the plan gave Claude non-waivable veto
power for true annotation, chemistry teach-back, and fixed-branch separation.
Those bars were not fully met.

| Finding | Claude summary | Codex classification | Control to add |
|---|---|---|---|
| P18-EXEC1-F1 | Fixed-branch separation has conceptual bleed between learned parameter lane and external \(\beta\) lane. | `ACCEPT` | Add post-boundary reconciliation block mapping pre-boundary \((x_t,\theta,x_{t-1})\) objects to fixed-branch \((x_t,x_{t-1};\beta)\) objects. |
| P18-EXEC1-F2 | Chemistry persona cannot teach back Section 5.4 composite preconditioning map. | `ACCEPT` | Add step-by-step derivation from \(T_t^\ell,S_t^\ell\) composition through marginalizing \(u_{t-1}\) to retained physical density. |
| P18-EXEC1-F3 | Some material source units are still aggregated. | `ACCEPT` | Split Remark 3 and Algorithm 5 into per-source-line submarkers with local question/implementation/failure checks. |
| P18-EXEC1-F4 | Equation-count ledger bucket total is not auditable. | `ACCEPT` | Replace with row-wise count table: tag, source anchor, category, justification. |
| P18-EXEC1-F5 | Implementation engineer needs explicit Algorithm 5 dataflow and evaluator signatures. | `ACCEPT` | Add boxed Algorithm 5 pipeline with persisted objects and evaluator signatures. |
| P18-EXEC1-F6 | Delegated theorem assumptions are too soft. | `PARTIAL` | Add local assumption boxes for Lemma 1, Proposition 2, and KR exactness; do not attempt to reprove external Cui--Dolgov theorems. |

No disputed findings.

## Execution Review Iteration 2

Claude status: `REJECT`.

Codex audit decision: Claude's rejection is materially correct.  The remaining
issues are narrow but true vetoes under the P18 plan: Algorithm 5 inventory
granularity, a count-ledger equation from Section 4 that should not be counted
under the Sections 1--3 and 5 gate, and one conditional pushforward step that
was still too compressed for the chemistry-reader standard.

| Finding | Claude summary | Codex classification | Control added |
|---|---|---|---|
| P18-EXEC2-F1 | Inventory collapses Algorithm 5 into one row although the note has per-line markers. | `ACCEPT` | Split the inventory into separate Algorithm 5(b.1), (b.2), (b.3), (c.1), and (c.2) rows with exact P18 equation tags. |
| P18-EXEC2-F2 | Equation-count ledger includes out-of-scope Section 4 equation `E1`. | `ACCEPT` | Removed `E1` from the counted table, added section subtotals, and changed the gate result from `132_GE_39` to `135_GE_39` after adding P16b.1--P16b.4. |
| P18-EXEC2-F3 | Chemistry reader cannot fully teach back the conditional pushforward step behind P16c. | `ACCEPT` | Added P16b.1--P16b.4 deriving the conditional pushforward identity from the bridge map before multiplying by the bridge marginal. |

No disputed findings.

## Execution Review Iteration 3

Claude status: `ACCEPT`.

Codex audit decision: Codex independently agrees with acceptance.  Claude
verified that the iteration-2 veto fixes are present and sufficient: Algorithm
5 is now row-wise traceable in the inventory, the equation-count gate excludes
the Section 4 context equation and reports `135 >= 39`, and the chemistry-reader
gap at the P16c bridge decomposition is closed by P16b.1--P16b.4.

| Control | Claude verdict | Codex classification | Evidence |
|---|---|---|---|
| Algorithm 5 inventory granularity | Pass | `ACCEPT` | Separate rows for Algorithm 5(b.1)--(c.2), mapped to P7l, P8--P11c, P12--P13a, P14--P15, and P16--P18. |
| Equation-count gate | Pass | `ACCEPT` | Section subtotals 16/26/57/36, total 135, Section 4 `E1` excluded. |
| Chemistry-reader P16c derivation | Pass | `ACCEPT` | P16b.1--P16b.4 derive the conditional pushforward identity before P16c--P17. |
| Eight P18 controls | Pass | `ACCEPT` | No remaining veto across source order, display math, symbols/measures, derivation, implementation objects, diagnostics, chemistry reader, fixed-branch separation. |

Persona summary:

- Hostile numerical analyst: no remaining veto; count gate is auditable and
  scope-clean.
- Implementation engineer: no remaining veto; Algorithm 5 inputs, outputs,
  persisted objects, and diagnostics are traceable.
- Educated former chemistry academic: no remaining veto; can teach back the
  bridge argument from conditional pushforward through P17.  The method is
  plausible as a high-dimensional TT/transport approximation strategy, subject
  to rank, conditioning, and model diagnostics.

Residual minor risks:

- External theorem proofs remain delegated and boxed as assumptions.
- Plausibility is not empirical validation on BayesFilter target models.
- Equation count remains a process/readability gate, not correctness evidence.

No disputed findings.
