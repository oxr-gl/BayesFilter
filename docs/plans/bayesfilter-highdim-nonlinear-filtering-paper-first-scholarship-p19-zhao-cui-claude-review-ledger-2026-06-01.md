# P19 Zhao--Cui Claude Review Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao--Cui filtering-scalar and gradient-feasibility ledgers.
- P15 implementable fixed-branch squared-TT specification.
- P18 true annotated Zhao--Cui companion and review ledgers.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross/rank/pivot/domain
  choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No empirical validation on BayesFilter target models.

## Plan Review Iteration 1

Claude status: `REJECT`.

Codex audit decision: Claude's rejection is materially correct.  The plan
needed stronger controls against reverting into an audit artifact, a substantive
finite-difference ledger requirement, explicit trusted Claude execution, and a
narrower allowed-write list.

| Finding | Claude summary | Codex classification | Control added |
|---|---|---|---|
| P19-PLAN1-F1 | No hard veto/validation against the note becoming a governance artifact. | `ACCEPT` | Added governance-artifact veto and banned-term validation scan for the main note/PDF. |
| P19-PLAN1-F2 | Finite-difference guard was presence-checked rather than substance-checked. | `ACCEPT` | Added finite-difference ledger requirements: branch manifest, branch identity, centered formula, epsilon schedule, error/tolerance, pass/fail interpretation. |
| P19-PLAN1-F3 | Claude review loops did not state trusted/elevated execution requirement. | `ACCEPT` | Added trusted/elevated Claude wrapper requirement to plan and execution review loops. |
| P19-PLAN1-F4 | Allowed writes broader than needed. | `ACCEPT` | Narrowed allowed writes to exact P19 outputs plus note PDF and same-basename latexmk auxiliaries. |

No disputed findings.

## Execution Review Iteration 1

Claude status: `REJECT`.

Codex audit decision: Codex agrees that the two high-severity findings are
material vetoes under the P19 plan.  The note was mathematically honest on the
fixed-branch distinction, but still too compressed at the bridge from warmups
to full TT core fitting and at the carried-marginal derivative.

| Finding | Claude summary | Codex classification | Control added |
|---|---|---|---|
| P19-EXEC-F1 | The design-row derivation jumped too quickly to \(A_{j,k}=R^\top\otimes b^\top\otimes L\); the chair could not teach back why the Kronecker row is correct. | `ACCEPT` | Added a decompressed single-row derivation in the main note before Eq. (54): entrywise environments \(L_{j,k}[a]\), \(R_{j,k}[b]\), local core expansion, the triple sum showing linearity in \(C_k[a,\ell,b]\), the row coefficient \(A_{j,k}[a,\ell,b]\), and entrywise \(\dot A_{j,k}\). |
| P19-EXEC-F2 | The carried-filter derivative stated \(\dot a_t=\int\dot q_t\) but did not show how to assemble it from core derivatives. | `ACCEPT` | Added explicit left-to-right marginal contraction formulas for \(M_{<j}\), \(\dot M_{<j}\), \(a_t(z_D)\), and \(\dot a_t(z_D)\), with coordinate-ordering caveat. |
| P19-EXEC-F3 | The mass-contraction section needed a sentence-to-equation bridge from the rank-\(R\) warmup to the full indexed contraction. | `ACCEPT` | Added explanatory bridge identifying \(M_{>j}\) as the right factor, \(B_j\) as one-coordinate basis mass, and the two copies of \(C_j\) as the two squared-TT factors. |
| P19-EXEC-F4 | Positivity floors were mentioned without saying whether they alter the scalar being differentiated. | `ACCEPT` | Added Eq. (53a) and explanation that a floor becomes part of the declared scalar and must be differentiated as that floored scalar. |
| P19-EXEC-F5 | Discrepancy report and result note were absent at the time of review. | `ACCEPT` | Deferred until after execution review convergence; these are required final outputs and will be created before closeout. |

No disputed findings in iteration 1.

## Execution Review Iteration 2

Claude status: `ACCEPT`.

Codex audit decision: Codex agrees with the acceptance.  The prior vetoes were
closed by concrete mathematical additions:

- the note now derives the local design row entrywise before using Kronecker
  notation;
- the note now gives an explicit carried-marginal contraction and derivative
  recipe;
- the note now bridges the rank-\(R\) warmup to the full mass recursion;
- the note now states that a positivity floor changes the declared scalar and
  must be differentiated as that floored scalar.

Claude reported no remaining findings in the scoped re-review.  Codex also
independently checked that the main note continues to avoid the banned
process/governance terms and that the fixed-branch semantics freeze structural
choices rather than fitted core values.

No disputed findings in iteration 2.

## Plan Review Iteration 2

Claude status: `ACCEPT`.

Codex audit decision: Codex agrees with acceptance.  The plan now includes the
governance-artifact veto and banned-term validation scan, substantive
finite-difference ledger requirements, trusted/elevated Claude wrapper
requirements, and narrowed allowed writes.  No material plan blocker remains.

Residual minor risks accepted for execution:

- The final result must explicitly separate new P19 changes from unrelated
  dirty files already present in the repository.
- The banned-term scan is necessary but not sufficient; the persona-based
  execution review remains the real readability gate.
- Chair satisfaction remains judgment-based, so Codex must not treat formal
  structure alone as sufficient.

No disputed findings.
