# P5 Analytical-Gradient Derivation Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: `ch33`, `ch36`, P4 derivation ledger, P5 plan, and existing
source-support ledgers.

what_is_not_concluded: This ledger does not conclude exact posterior accuracy
for any approximate filter, HMC convergence, production readiness, or
continuous-time/PDE score-adjoint validity.

## Gradient Obligation Table

| obligation_id | location | claim | support_status | derivation_status | mcp_status | residual gap |
|---|---|---|---|---|---|---|
| `P5-GRAD-1` | `ch33`, `eq:bf-hd-likelihood-factor` | \(\ell_T(\theta)=\sum_t\log Z_t(\theta)\). | `PROJECT_DERIVATION` inherited from P4 | already expanded in P4 and reused | broad factorization human-reviewed | No measure-theoretic machine certification. |
| `P5-GRAD-2` | `ch33`, `eq:bf-hd-prediction-sensitivity` | \(s_t^-\) satisfies the differentiated prediction recursion. | `PROJECT_DERIVATION` | added in P5 under dominated differentiation | broad integral derivative not machine-certified | Requires dominated differentiation and fixed support assumptions. |
| `P5-GRAD-3` | `ch33`, `eq:bf-hd-normalizer-gradient` | \(\nabla_\theta Z_t\) is the differentiated observation normalizer. | `PROJECT_DERIVATION` | added in P5 | broad integral derivative not machine-certified | Requires differentiable \(g_\theta\), \(p_t^-\), and dominated differentiation. |
| `P5-GRAD-4` | `ch33`, `eq:bf-hd-likelihood-gradient` | \(\nabla_\theta\ell_T=\sum_t\nabla_\theta Z_t/Z_t\). | `PROJECT_DERIVATION` | added in P5 | small \(\nabla\log Z=\nabla Z/Z\) algebra `MCP_VERIFIED` | Broad sequence likelihood remains human-reviewed. |
| `P5-GRAD-5` | `ch33`, `eq:bf-hd-update-sensitivity` | normalized filtering sensitivity follows from quotient rule. | `PROJECT_DERIVATION` | added in P5 | scalar quotient algebra `MCP_VERIFIED` | Integral normalization remains human-reviewed. |
| `P5-GRAD-6` | `ch36`, `eq:bf-hd-analytical-hmc-gradient` | transformed HMC gradient is chain rule plus Jacobian term. | `PROJECT_DERIVATION` | added in P5 | broad vector chain rule not machine-certified | Human-reviewed; no broad formal proof. |
| `P5-GRAD-7` | `ch36`, `ex:bf-hd-scalar-gaussian-gradient` | scalar Gaussian likelihood/HMC gradient can be computed by hand. | `PROJECT_DERIVATION` | added in P5 | scalar sign/simplification `MCP_VERIFIED` | Toy example only; no nonlinear-filter validation. |
| `P5-GRAD-8` | `ch36`, `eq:bf-hd-approx-hmc-gradient`; `ch37`, HMC defect section | approximate-filter gradient targets only declared approximate scalar unless exact correction is present. | `PROJECT_DERIVATION` | strengthened in P5 | not machine-checkable policy/target contract | No exactness claim for approximate filters. |
| `P5-GRAD-9` | `ch33`, PDE boundary paragraph | continuous-time/PDE gradient or adjoint analogues are not derived here. | `SOURCE_GAP_BLOCKER` / `SURVEY_CONTEXT_ONLY` | made explicit in P5 | not attempted | Requires separate source-supported adjoint/sensitivity theory. |

## Human-Review Notes

The main text contains step-by-step derivations for the discrete-time
sensitivity recursion and HMC target gradient.  MathDevMCP verified small
algebraic pieces only.  Any broad proposition with tool-inconclusive status is
therefore `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`, not machine-certified.

Decision: `ANALYTICAL_GRADIENT_PASS_READY_FOR_HOSTILE_REVIEW`.
