# P28 MathDevMCP Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

audit_scope:
- Narrow algebra checks for selected proof obligations.
- Tool-limit recording where functional or matrix expressions are not encodable.

what_is_not_concluded:
- MathDevMCP did not certify the whole document.
- MathDevMCP did not certify all 754 equation environments.
- Inconclusive checks are not failures of the math, but they are not machine verification.

## Checks

| obligation | expression checked | status | evidence summary |
|---|---|---|---|
| quotient derivative algebra | `(dn*c - n*dc)/c**2 == dn/c - n*dc/c**2` | MCP_VERIFIED | SymPy simplified lhs-rhs to zero under `c != 0`. |
| squared term differential algebra | `2*a*da == da*a + a*da` | MCP_VERIFIED | SymPy simplified lhs-rhs to zero. |
| log-normalizer scalar form | `dc/c == dc*(1/c)` | MCP_VERIFIED | SymPy simplified lhs-rhs to zero under `c != 0`. |
| Bayes normalizer cancellation | `(f*g*p)/(f*g*p) == 1` | MCP_VERIFIED | SymPy simplified lhs-rhs to zero under nonzero denominator. |
| squared-density normalization cancellation | `(a**2 + tau)/(a**2 + tau) == 1` | MCP_VERIFIED | SymPy simplified lhs-rhs to zero under nonzero denominator. |
| derivative of shifted squared mass | `dtau + 2*a*da*m == dtau + (da*a+a*da)*m` | MCP_VERIFIED | SymPy simplified lhs-rhs to zero. |
| functional derivative of `log(c(theta))` | callable notation | MCP_TOOL_LIMIT | Backend could not encode callable functional notation. |
| quotient derivative in callable notation | callable notation | MCP_TOOL_LIMIT | Backend could not encode callable functional notation. |
| derivative of `a(theta)^2` in callable notation | callable notation | MCP_TOOL_LIMIT | Backend could not encode callable functional notation. |
| fixed matrix/linear solve derivative | symbolic assumption form | MCP_UNVERIFIED | Backend could not use equation assumption to simplify matrix-like scalar expression. |
| triangular Jacobian determinant | `det(Matrix(...))` form | MCP_TOOL_LIMIT | Tool grammar rejected matrix constructor syntax. |

## Verdict

mathdevmcp_status: `NARROW_SUPPORT_ONLY`

The checks support local scalar algebra used by the fixed-branch derivative and normalization discussions. They do not certify the functional analysis, TT contractions, KR map construction, or all displayed equations.
