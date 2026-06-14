# P19 Zhao--Cui Discrepancy Report

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao--Cui filtering-scalar and gradient-feasibility ledgers.
- P15 implementable fixed-branch squared-TT specification.
- P18 true annotated Zhao--Cui companion and review ledgers.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross, rank selection,
  pivot selection, changing domains, changing shifts, or changing fitting
  points.
- No HMC convergence claim.
- No production BayesFilter implementation claim.
- No empirical validation on BayesFilter target models.
- No default-method recommendation.

## Disagreement Status

Decision: `NO_OPEN_CODEX_CLAUDE_DISAGREEMENT`.

Claude execution review iteration 1 rejected the note with two veto findings
and three non-veto findings.  Codex accepted all five findings and patched the
P19 note and ledgers.  Claude execution review iteration 2 accepted the patched
note and reported no remaining findings.

## Resolved Findings

| Finding | Claude status | Codex classification | Resolution |
|---|---|---|---|
| P19-EXEC-F1 | `REJECT` veto in iter1; resolved in iter2 | `ACCEPT` | Added entrywise design-row derivation leading to Kronecker shorthand and \(\dot A\). |
| P19-EXEC-F2 | `REJECT` veto in iter1; resolved in iter2 | `ACCEPT` | Added explicit carried-marginal contraction and derivative formulas. |
| P19-EXEC-F3 | Non-veto in iter1; resolved in iter2 | `ACCEPT` | Added bridge from rank-\(R\) warmup to full indexed mass recursion. |
| P19-EXEC-F4 | Non-veto in iter1; resolved in iter2 | `ACCEPT` | Added positivity-floor same-scalar clarification. |
| P19-EXEC-F5 | Bundle-completeness gap in iter1 | `ACCEPT` | This discrepancy report and the P19 result note close the required-output gap. |

## Residual Discrepancies

None between Codex and Claude.

## Residual Non-Disagreement Risks

- MathDevMCP did not broadly certify calculus identities involving
  \(Z(\beta)\); it only checked narrow algebraic identities that the tool could
  encode.
- P19 is a derivation and review note, not an implementation run.  The
  finite-difference protocol is specified but not executed.
- The chair-readable judgment is supported by Claude's persona review and
  Codex audit, but still ultimately depends on the real panel chair's reading.
