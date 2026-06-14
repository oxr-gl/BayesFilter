# P29 MathDevMCP Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," Annals of Mathematical Statistics 1952.
- Cui and Dolgov, squared inverse Rosenblatt transport / squared TT background used by Zhao and Cui.

audit_scope:
- Narrow MathDevMCP checks for P29 critical-equation audit.

what_is_not_concluded:
- MathDevMCP did not certify TT tensor contractions as full formal proofs.
- MathDevMCP did not certify all functional derivative notation.
- MathDevMCP did not visually compare Zhao--Cui equations.

## Checks

| obligation | status | evidence |
|---|---|---|
| quotient derivative algebra `(dn*c-n*dc)/c^2 = dn/c - n dc/c^2` | MCP_VERIFIED | SymPy simplified difference to zero under `c != 0`. |
| scalar fixed-solve derivative rearrangement `(dd-dN*g)/N = dd/N-dN*g/N` | MCP_VERIFIED | SymPy simplified difference to zero under `N != 0`. |
| conditional ratio cancellation `p1*(p12/p1)=p12` | MCP_VERIFIED | SymPy simplified difference to zero under `p1 != 0`. |
| preconditioning ratio associativity `(nu/eta)*rho = nu*(rho/eta)` | MCP_VERIFIED | SymPy simplified difference to zero under `eta != 0`. |
| residual ratio `q/rho*eta=q*eta/rho` | MCP_VERIFIED | SymPy simplified difference to zero under `rho != 0`. |
| triangular determinant commutativity `a*c=c*a` | MCP_VERIFIED | Supports 2D triangular determinant product only; not full matrix proof. |
| exponential shift derivative simplification | MCP_TOOL_LIMIT | Tool normalized `exp(-c)` oddly; not relied on as evidence. |

## Verdict

mathdevmcp_verdict: `NARROW_SUPPORT_ONLY`

The tool supports the scalar algebra used inside the derivations. It does not replace human review of dimensions, signs, source fidelity, or assumptions.

