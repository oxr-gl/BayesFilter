# P33 Basis-Choice Confidence MathDevMCP Ledger

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.

what_is_not_concluded:
- MathDevMCP does not certify the full 100-plus-page note.
- MathDevMCP does not prove basis optimality.
- MathDevMCP checks only narrow algebraic identities.

## Checks

| identity | status | evidence | what_is_not_certified |
|---|---|---|---|
| \(\frac{d}{d\beta}\log Z=\dot Z/Z\) | `MCP_VERIFIED` after scalarization | MathDevMCP certified the normalized scalar identity `dZ/Z = dZ/Z` under \(Z\ne0\). Direct functional notation `Z(beta)` was `MCP_TOOL_LIMIT` because the SymPy wrapper treated the function name as a symbol. | Does not certify the full TT normalizer derivation. |
| Scalar square-mass derivative | `MCP_VERIFIED` for scalar constant mass | MathDevMCP/SymPy simplified `dC*m*C + C*m*dC - 2*C*m*dC` to zero under scalar constant-mass assumptions. | Matrix/tensor contraction derivative is supported by project derivation in the note, not machine certified in full tensor notation. |
| Scalar quotient/linear-solve derivative form | `MCP_VERIFIED` for scalar quotient algebra | MathDevMCP/SymPy simplified `(dd*N - d*dN)/(N**2)` and `dd/N - dN*d/(N**2)` to the same expression under \(N\ne0\). | Fixed-matrix/vector solve derivative in full matrix notation remains project-derived, not broadly certified. |
| Functional notation checks for \(Z(\beta)\), \(c(\beta)\), \(N(\beta)\) | `MCP_TOOL_LIMIT` | Wrapper reported `'Symbol' object is not callable` for direct function notation. | No negative mathematical evidence; only a tooling limitation. |
| Projection monotonicity for nested spaces | `MCP_UNVERIFIED` | Symbolic backend could not certify set/infinite-dimensional infimum statement. | The note's proof remains a human/project derivation. |
