# P9 Ch34 MathDevMCP Ledger

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: Rewritten `ch34`, P9 plan, fixed-SGQF gradient ledger,
MathDevMCP diagnostics, and the scholarly literature audit policy.

what_is_not_concluded: MathDevMCP diagnostics do not certify the chapter, the
fixed-SGQF algorithm, HMC correctness, posterior accuracy, or broad derivation
validity.

## Narrow Checks

| Obligation | Status | Evidence |
|---|---|---|
| Scalar Gaussian innovation score algebra after substituting \(w=v/S\). | `MCP_VERIFIED` | `check_equality` verified `-0.5*(dS/S + 2*dv*v/S - v*v*dS/(S*S)) == -0.5*(dS/S + 2*dv*(v/S) - (v/S)*(v/S)*dS)`. |
| Fixed-weight derivative linearity for a three-point weighted sum. | `MCP_VERIFIED` | Normalizer verified identical weighted derivative expression. |
| One-dimensional three-point GHQ affine mean identity. | `MCP_VERIFIED` | SymPy simplified \((1/6)(m-C\sqrt3)+(2/3)m+(1/6)(m+C\sqrt3)-m\) to zero. |
| One-dimensional three-point GHQ affine variance identity. | `MCP_VERIFIED` | SymPy verified \((1/6)(-C\sqrt3)^2+(2/3)0^2+(1/6)(C\sqrt3)^2=C^2\). |
| Sparse-grid linear-combination distributivity. | `MCP_VERIFIED` | SymPy verified `c1*(a1+b1)+c2*(a2+b2) == (c1*a1+c2*a2)+(c1*b1+c2*b2)`. |
| Cholesky derivative identity \(L(B+B^\top)L^\top=\dot P\) when \(B+B^\top=L^{-1}\dot P L^{-\top}\). | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | Matrix identity is derived in the chapter; not encoded in MathDevMCP. |
| Matrix log-det derivative. | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | Same limitation as P8: broad matrix calculus identity is used by project derivation, not certified here. |
| Full fixed-SGQF recursion. | `MCP_TOOL_LIMIT` / `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | Too broad for the symbolic backend; checked by human derivation and Claude review only. |

## Broad Certification Status

`HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`: no broad chapter or algorithm proof is
machine-certified.
