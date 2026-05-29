# P5 Self-Contained Exposition Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: Existing P1R/P1S/P1T/P1U/P2R/P3/P4 source-support and
claim-support ledgers, `ch33`--`ch37`, P5 plan, and scholarly literature audit
policy.

what_is_not_concluded: This ledger does not conclude production readiness,
NAWM readiness, posterior accuracy, HMC convergence, tensor validation,
transport validation, GPU/XLA readiness, machine-certified proof validity, or
exhaustive literature coverage.

## Source-Support Boundary

P5 inherits the existing high-dimensional nonlinear filtering source ledgers.
No new literature theorem claim was introduced.  No citation count, venue rank,
abstract, introduction, conclusion, blocked original, or quarantined source is
used as theorem support.  The Spantini et al. 2016 decomposable-transport
workshop paper remains quarantined and supports no claim.

## Self-Containedness Pass

| chapter | central object defined before method use | exact target / approximation / diagnostic role | industrial relevance sentence | status | residual risk |
|---|---|---|---|---|---|
| `ch33` | Conditional filtering law, normalizer, likelihood scalar, and likelihood-gradient sensitivity. | Exact Bayes recursion and exact likelihood are separated from approximate target and approximate gradient. | Diagnostics must identify whether they check law, likelihood scalar, or derivative. | `UPDATED` | Still compact relative to a full filtering textbook. |
| `ch34` | Gaussian projected moment pair and Gaussian-weighted expectations. | Moment closure is separated from exact conditional law; quadrature is expectation approximation, not posterior accuracy. | Gaussian scaffold exposes local curvature, factorization, innovation, and projection defects. | `UPDATED` | No new full quadrature theory; source-local boundary remains. |
| `ch35` | Empirical particle measure, transport/coupling object, and tensor representation. | Finite ensemble, fitted map, and low-rank representation are approximations to law/normalizer/covariance/map objects. | Methods stay diagnostic unless correction, support, rank, mass, positivity, PSD, and likelihood/score gates are visible. | `UPDATED` | The chapter still assumes some familiarity with SMC and tensor notation after the object paragraph. |
| `ch36` | Scalar HMC potential \(U(q)\). | Exact target uses \(\ell_T\); approximate target uses declared \(\widehat\ell_T\). | HMC is meaningful only after finite values, same-scalar gradients, support, Jacobians, divergences, and energy diagnostics. | `UPDATED` | HMC convergence remains explicitly unproved. |
| `ch37` | Defect-first decision procedure. | Methods are composed only through named approximations and exported diagnostics. | Industrial value is audited composition, not novelty or speed before validity. | `UPDATED` | The synthesis is still a monograph architecture, not production policy. |

## Operational Acceptance Test

- Each target chapter defines its central scalar or object before the method
  discussion becomes technical.
- Each target chapter now contains a sentence or paragraph separating exact
  target, approximation, diagnostic role, and industrial relevance.
- The reader can identify input and output objects for the major method family
  without relying solely on nonlinear-filtering jargon.

Decision: `SELF_CONTAINEDNESS_IMPROVED_WITH_RESIDUAL_COMPACTNESS`.
