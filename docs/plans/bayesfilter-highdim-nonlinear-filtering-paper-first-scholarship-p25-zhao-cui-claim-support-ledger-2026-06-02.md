# P25 Zhao--Cui Claim-Support Ledger

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
- No exact posterior accuracy claim.
- No adaptive global differentiability claim.
- No production implementation claim.
- No empirical validation claim.

## Claim Mapping

| P25 claim | Support class | Anchor |
|---|---|---|
| Bayesian filtering requires representation and marginalization of the adjacent-state target. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eqs. (9)--(12); P25 `p25-bridge-1`--`p25-bridge-4`. |
| TT rank is a controlled relaxation of independence across coordinate splits. | `PROJECT_DERIVATION` + `PRIMARY_TECHNICAL_SUPPORT` | Oseledets TT background; P25 `p25-bridge-9`--`p25-bridge-13`. |
| Moderate rank is plausible under local interactions and good ordering, but can fail under global constraints. | `PROJECT_DERIVATION` | P25 `p25-bridge-14`--`p25-bridge-18`. |
| Coordinate transformations preserve mass through Jacobian factors. | `PROJECT_DERIVATION` + `PRIMARY_TECHNICAL_SUPPORT` | Rosenblatt transformation background; P25 `p25-walk-2`--`p25-walk-4`. |
| The fixed-branch derivative differentiates \(\widehat\ell_T(\beta;B)\), not the adaptive scalar. | `PROJECT_DERIVATION` | P25 `p25-gradteach-2`--`p25-gradteach-11`; P24 Proposition 2. |
| The implementable lane is fixed ridge least squares, not adaptive TT-cross. | `PROJECT_DERIVATION` | P25 `p25-ls-1`--`p25-ls-23`. |
| The less-toy trace is pedagogical and not validation. | `PROJECT_DERIVATION` | P25 `p25-trace2-1`--`p25-trace2-20`; P25 result caveats. |

Decision: `CLAIM_SUPPORT_READY_FOR_P25_REVIEW`.
