# P6 Running Example Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P6 plan, P5 result/ledgers, `ch33`--`ch37`, and existing P1--P5
source-support artifacts.

what_is_not_concluded: The running example is not NAWM validation, production
evidence, posterior-accuracy evidence, tensor-method validation, transport
validation, HMC validation, or evidence that the macro-finance stress cell has
the same severity as the scalar cell.

## Running Cell

\[
  x_t=\rho x_{t-1}+\eta_t,\qquad
  \eta_t\sim\calN(0,Q),\qquad
  y_t=x_t^2+\epsilon_t,\qquad
  \epsilon_t\sim\calN(0,R).
\]

For a one-step Gaussian prediction \(X\sim\calN(0,P^-)\), the pedagogical
filtering density is proportional to
\[
  \exp\{-x^2/(2P^-)-(y-x^2)^2/(2R)\}.
\]

When \(R\) is small and \(y>0\), this cell can put mass near both
\(+\sqrt y\) and \(-\sqrt y\).

## Chapter Use

| chapter | use of running cell |
|---|---|
| `ch33` | explains conditional law, normalizer, likelihood scalar, and why a nonlinear observation can create two lobes |
| `ch34` | explains why Gaussian projection can preserve moments while losing shape |
| `ch35` | explains particles as lobe coverage, transports as support/Jacobian/correction, and tensors as semantic compression |
| `ch36` | explains that HMC starts only after a scalar likelihood or declared approximate scalar and gradient are named |
| `ch37` | connects the scalar mechanism to the existing stylized macro-finance stress cell while preserving nonvalidation language |

## Non-Overgeneralization Boundary

The scalar cell is used only to teach mechanisms.  It cannot establish
macro-finance severity, rank tractability, transport behavior, HMC behavior, or
industrial adequacy except by analogy.

Decision: `RUNNING_EXAMPLE_INTEGRATED_WITH_NONVALIDATION_BOUNDARY`.
