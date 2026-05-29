# P7 Gaussian/Transport/Tensor Self-Contained Gradient Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P7 plan, P6 result, `ch34`, `ch35`, `ch36`, `ch37`,
`ch18_svd_sigma_point.tex`, P1R/P1S/P1T/P1U/P2R/P3/P4/P5/P6 artifacts,
`docs/references.bib`, `docs/source_map.yml`, and the scholarly literature
audit policy.

what_is_not_concluded: This ledger does not conclude production readiness, NAWM
readiness, posterior accuracy, HMC convergence, tensor-method validation,
transport-method validation, GPU/XLA readiness, default readiness, exhaustive
literature coverage, or machine-certified chapter proof validity.

## Decision

`P7_EXECUTED_WITH_CLAUDE_ACCEPT_AND_PDF_BUILD`.

## Scope

P7 rewrote the two chapters identified by the user as still too compact:

- `ch34`: Gaussian projection, derivative filters, UKF/CKF, high-degree CKF,
  tensor-product Gauss--Hermite quadrature, sparse-grid Gauss--Hermite/SGQF,
  and the approximate Gaussian innovation likelihood score.
- `ch35`: empirical particle measures, SIR/bootstrap mechanics, weight
  collapse, guided proposal correction, transport-map correction, triangular
  ensemble transports, TT density/PDE filters, TT/KR transport bridge, and
  tensor-network covariance caution.

Narrow coordination edits were added to:

- `ch36`: cross-reference the concrete P7 approximate Gaussian innovation
  likelihood and score.
- `ch37`: import the new approximate-score parity and HMC-admissibility gates
  into the synthesis table.

## Readability Actions

| Chapter | P7 action | Panel-facing purpose |
|---|---|---|
| `ch34` | Replaced short sections with method-local teaching blocks. | A physics,
chemistry, or numerical-analysis reader sees the object, construction, scalar,
gradient, failure mode, diagnostic, and source anchor before tables. |
| `ch34` | Added tensor-product GHQ before sparse-grid use. | The reader now
understands sparse grids as a truncation/combination of tensor-product
interaction rules rather than as an acronym. |
| `ch34` | Added exact approximate Gaussian innovation score derivation. | HMC
can only use the approximate scalar if the score differentiates that same
scalar. |
| `ch35` | Split particles, guided proposals, transports, TT densities, TT/KR
maps, and TN covariance filters into separate object sections. | Avoids asking
readers to infer semantic differences from method names. |
| `ch35` | Added HMC boundary language for resampling, map Jacobians, TT ranks,
TT-cross pivots, and TN covariance branches. | Prevents smooth-gradient claims
from being smuggled through adaptive or discrete algorithmic choices. |

## HMC Labels Added

| Family | P7 label |
|---|---|
| EKF fixed smooth scalar | `HMC_ADMISSIBLE_APPROXIMATE_TARGET` |
| IEKF convergence branch | `HMC_BRANCH_LOCAL_ONLY` |
| Second-order EKF | `DIAGNOSTIC_ONLY` or branch-local for small smooth blocks |
| UKF/CKF fixed rule | `HMC_ADMISSIBLE_APPROXIMATE_TARGET` |
| High-degree CKF fixed rule | `HMC_ADMISSIBLE_APPROXIMATE_TARGET` for declared
small blocks |
| Tensor-product GHQ | `DIAGNOSTIC_ONLY` globally; admissible only on tiny fixed
blocks |
| Sparse-grid fixed index set | `HMC_BRANCH_LOCAL_ONLY` unless all branches are
fixed and smooth |
| Adaptive sparse-grid filter | `HMC_NOT_ADMISSIBLE_UNTIL_SMOOTHED` |
| Bootstrap/SIR with resampling | `HMC_NOT_ADMISSIBLE_UNTIL_SMOOTHED` |
| No-resampling fixed-random-number particle diagnostic | `HMC_BRANCH_LOCAL_ONLY` |
| Transport-preconditioned HMC with finite corrected scalar/Jacobian |
`HMC_ADMISSIBLE_APPROXIMATE_TARGET` |
| TT density/operator with declared scalar and fixed differentiable branch |
`HMC_ADMISSIBLE_APPROXIMATE_TARGET` |
| Frozen TT ranks/pivots | `HMC_BRANCH_LOCAL_ONLY` |
| Adaptive TT ranks/pivots/truncation | `HMC_NOT_ADMISSIBLE_UNTIL_SMOOTHED` |
| TN covariance filters | `DIAGNOSTIC_ONLY` unless embedded in a fixed smooth
Gaussian likelihood branch |

## Human-Reader Test

P7 explicitly asks the reader to track:

1. the object being approximated;
2. the exact target or approximate scalar;
3. the construction in equations;
4. the failure mode;
5. the diagnostic/veto;
6. the industrial role;
7. the source anchor or project derivation.

Residual risk: the chapters are more teachable but remain dense monograph
chapters rather than textbook-length lecture notes.

## Validation Status

- Claude plan review: `ACCEPT` on iteration 1.
- Claude execution review: `REJECT` on iteration 1, repaired, then `ACCEPT` on
  iteration 2.
- PDF build: succeeded with `latexmk -cd -pdf -interaction=nonstopmode
  -halt-on-error docs/main.tex`.
- Citation/reference scan: no undefined citation, undefined reference, or rerun
  blockers found.
- Layout warnings: underfull/overfull boxes remain, including in dense P7
  tables.  These are editorial/layout warnings, not source-support or PDF-build
  blockers.
