# P25 Zhao--Cui Discrepancy Report

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- P24 Zhao--Cui human-facing companion note.

what_is_not_concluded:
- No unresolved discrepancy has been accepted as harmless.
- No full-file Claude execution-review certification is recorded.
- No exact posterior, adaptive-gradient, production-implementation, or
  empirical-validation claim is made.

## Status

status: `BOUNDED_EXECUTION_REVIEW_ACCEPTED_WITH_PATCHED_MINOR_RESIDUALS`

No substantive Codex/Claude disagreements are recorded.

Claude plan review accepted the P25 plan in iteration 1.  Two full-file or
file-inspection execution-review attempts stalled and were stopped.  A separate
Claude health check succeeded, and a bounded excerpt execution review completed
with decision `ACCEPT_WITH_MINOR_RESIDUALS`.

Codex accepted all four minor residuals and patched them:

- anti-overclaim sentence for the TT-rank locality heuristic;
- reference/physical measure-bookkeeping display;
- shape, flattening, and mass-contraction ledger for the fixed least-squares
  lane;
- explicit verification equations for the two-point numeric trace.

Residual discrepancy:

- The bounded excerpt review is not full-document machine certification.

Decision:

`P25_LOCAL_VALIDATION_PASS_BOUNDED_CLAUDE_REVIEW_ACCEPTED_PATCHED`.
