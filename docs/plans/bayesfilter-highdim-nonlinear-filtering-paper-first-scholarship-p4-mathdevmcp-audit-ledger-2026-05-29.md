# P4 MathDevMCP Audit Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P4 derivation obligations in `ch33`--`ch37`, especially small
algebraic identities split from broad propositions.

what_is_not_concluded: MathDevMCP diagnostics do not certify the chapters as
machine-verified proofs, do not prove PDE filtering theorems, do not establish
posterior accuracy, and do not validate any industrial method.

## Protocol

Broad industrial propositions were not submitted as certification targets.
They were split into bounded algebraic or typed diagnostics where feasible.
The allowed status vocabulary is:

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

## Results

| audit_id | obligation | tool | input | status | interpretation |
|---|---|---|---|---|---|
| `P4-MCP-1` | lognormal variance factor used in particle-collapse derivations | `check_equality` / SymPy | `exp(2*mu + 2*v)/(exp(mu + v/2)**2) = exp(v)` | `MCP_VERIFIED` | Certifies only the displayed algebraic ratio.  It does not certify high-dimensional particle-filter asymptotics. |
| `P4-MCP-2` | PSD counterexample eigenvalue algebra | `check_equality` / SymPy | `1 - (1 + eps)**2 = -eps*(2 + eps)` | `MCP_VERIFIED` | Certifies the determinant/product algebra behind the two-by-two indefinite perturbation.  It does not certify finite-precision covariance analysis. |
| `P4-MCP-3` | scalar simplification of Gaussian residual covariance terms | `check_equality` / SymPy | `P - 2*C**2/S + C**2/S = P - C**2/S` | `MCP_VERIFIED` | Certifies a scalar analogue of the residual covariance simplification.  The matrix derivation remains human-reviewed. |
| `P4-MCP-4` | log of product equals sum | `check_equality` / SymPy | `log(exp(a)*exp(b)) = a + b` under real assumptions | `MCP_UNVERIFIED` | SymPy left `log(exp(a+b))`; the likelihood factorization remains human-reviewed under positive-density assumptions. |
| `P4-MCP-5` | predictive score identity label | `derive_label_step` | `prop:bf-hd-score` comparing integral identity | `MCP_UNVERIFIED` | Tool reported symbolic mismatch because integral notation was not formalized.  Context supported the label, but certification failed. |
| `P4-MCP-6` | affine projection label | `typed_obligation_label` | `prop:bf-hd-affine-projection` | `MCP_UNVERIFIED` / `needs_assumptions` | Tool requested missing matrix constraints due parser limitations.  Text now states nonsingular `S`; dimensions remain human-reviewed. |
| `P4-MCP-7` | transport Jacobian target label | `typed_obligation_label` | `prop:bf-hd-jacobian-target` | `MCP_INCONCLUSIVE` / `consistent` | Tool found metadata ready for bounded routing but did not certify the change-of-variables theorem.  Text remains project derivation. |
| `P4-MCP-8` | performance-after-veto proposition | `typed_obligation_label` | `prop:bf-hd-performance-after-veto` | `MCP_INCONCLUSIVE` / `consistent` | Tool extracted a proposition but it is an industrial contract, not a symbolic equality.  It remains human-reviewed. |

## Status Summary

MathDevMCP certified three small algebraic equalities.  It did not certify any
broad proposition, PDE derivation, HMC convergence statement, tensor-rank
claim, transport-map correctness theorem, or industrial synthesis contract.

The chapter text and P4 result must therefore describe the math as
source-grounded and human-reviewed, with small algebraic MCP checks, not as
machine-certified.
