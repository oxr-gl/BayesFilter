# P20 Zhao--Cui Discrepancy Report

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

## Decision

Decision: `NO_UNRESOLVED_CLAUDE_CODEX_DISCREPANCY`.

The P20 execution review loop closed after two iterations.  Claude rejected
iteration 1 for one ledger-audit gap and accepted iteration 2 after Codex
patched that gap.  Codex independently audited every finding and did not leave
any disputed item unresolved.

## Closed Items

| Item | Claude position | Codex audit | Resolution |
|---|---|---|---|
| Page lower-bound ledger missing | Reject until the replaced-tail page estimate and required P20 page lower bound are explicit. | `ACCEPT` | Size ledger now records a 5-page replaced-tail estimate, method, required page lower bound 49, and actual 50-page PDF result. |
| Fixed-solve differentiability teachability | Not a veto, but chemistry persona wanted the finite-composition differentiability step made easier to teach back. | `PARTIAL` in iteration 1, `ACCEPT` after patch | Added a lemma proving differentiability of fixed ridge-sweep core updates before Proposition 2. |

## Remaining Risks

- P20 is still a long mathematical companion, so a nontechnical reader may need
  time rather than only local clarification.
- The fixed-branch derivative is a derivative of the declared fixed-branch
  approximate scalar.  It is not a derivative of the fully adaptive
  rank-changing Zhao--Cui research algorithm.
- The note has not been validated by implementing a new production filter from
  scratch.

No downstream execution is blocked by a Codex-Claude disagreement.
