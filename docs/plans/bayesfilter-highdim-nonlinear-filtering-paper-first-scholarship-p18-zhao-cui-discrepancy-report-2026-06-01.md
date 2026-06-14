# P18 Zhao--Cui Discrepancy Report

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao--Cui code audit and paper-code crosswalk ledgers.
- P15 fixed-branch implementation contract.
- P17 full-equation reconstruction note and ledgers.

what_is_not_concluded:
- No production BayesFilter implementation claim.
- No posterior accuracy claim for BayesFilter target models.
- No claim that adaptive Zhao--Cui branches are globally differentiable.
- No default-method recommendation.

## Discrepancy Status

Decision: `NO_OPEN_CODEX_CLAUDE_DISCREPANCY`.

Claude rejected the plan once and execution twice.  Codex accepted or partially
accepted every finding and patched the relevant files.  Claude execution review
iteration 3 returned `ACCEPT` with no surviving veto findings.  Therefore there
is no unresolved Codex--Claude disagreement requiring a human override.

## Closed Discrepancies

| Iteration | Issue | Codex classification | Resolution |
|---|---|---|---|
| Plan 1 | Missing scholarly ledgers, weak traceability, gameable equation count, subjective chemistry standard. | `ACCEPT` | Hardened P18 plan with literature ledgers, source-unit markers, count rules, veto controls, and chemistry rubric. |
| Exec 1 | Fixed-branch bleed, Section 5.4 teach-back gap, aggregated source units, weak equation-count ledger, Algorithm 5 dataflow gap, soft theorem assumptions. | `ACCEPT`/`PARTIAL` | Added reconciliation block, expanded Algorithm 5, row-wise count table, boxed dataflow, and local assumption boxes. |
| Exec 2 | Algorithm 5 inventory too coarse, Section 4 count contamination, P16c conditional pushforward gap. | `ACCEPT` | Split inventory rows, excluded Section 4 `E1`, recomputed count to 135, and added P16b.1--P16b.4. |

## Residual Non-Discrepancy Risks

- External theorem proofs are intentionally delegated and boxed.
- Empirical validation on BayesFilter models remains a separate workstream.
- The P18 note is an annotated mathematical companion and fixed-branch
  derivative specification, not production software.
