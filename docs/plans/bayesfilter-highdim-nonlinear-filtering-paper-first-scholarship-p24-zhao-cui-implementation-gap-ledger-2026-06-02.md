# P24 Zhao--Cui Implementation Gap Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.

what_is_not_concluded:
- No executable code is produced.
- No production numerical default is validated.
- No empirical finite-difference success is claimed.

## Implementation Gaps

| Gap | Control added in P24 | Status |
|---|---|---|
| Single boxed algorithm. | Added "End-To-End Fixed-Branch Squared-TT Filter" with inputs, initialization, loop, outputs, invariants, and failure exits. | `DONE` |
| Derivative recursions through sweep environments. | Preserved and normalized explicit \(\dot y,\dot H,\dot L,\dot R,\dot A,\dot N,\dot d,\dot g\) equations in derivative pass. | `DONE` |
| Deterministic rank ladder. | Added rank ladder with residual, conditioning, defensive-fraction pass criteria and branch failure. | `DONE` |
| Stabilization defaults table. | Added default table for floors, ridge, rank/fit constants, root inversion, defensive fraction, and conditioning veto. | `DONE` |
| Two-time-step numerical trace. | Added scalar trace with numerical parameters, target values, square-root values, normalizer, retained filter, second target, derivative term, and finite-difference check. | `DONE` |

