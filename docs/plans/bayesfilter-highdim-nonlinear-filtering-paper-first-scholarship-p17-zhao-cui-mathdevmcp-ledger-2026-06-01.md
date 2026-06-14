# P17 Zhao-Cui MathDevMCP Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, JMLR 2024.
- P17 project derivations.

what_is_not_concluded:
- No broad machine certification of TT filtering.
- No certification of adaptive Zhao--Cui code.
- No certification of posterior accuracy.
- No certification of the full P17 note.

## Checks Attempted

| Obligation | Tool result | P17 status |
|---|---|---|
| Derivative of \(\log Z(\theta)\) is \(\dot Z/Z\) for \(Z>0\) | `MCP_INCONCLUSIVE`: functional derivative notation was not encodable by SymPy wrapper | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` |
| Differentiating \(N g=d\) gives \(N\dot g=\dot d-\dot N g\) | `MCP_UNVERIFIED`: simplifier could not certify from textual assumptions | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` |
| Quotient derivative algebra \((\dot a Z-a\dot Z)/Z^2=\dot a/Z-a\dot Z/Z^2\) | `MCP_VERIFIED`: SymPy simplified lhs-rhs to zero with \(Z\) nonzero | `MCP_VERIFIED_NARROW_ALGEBRA_ONLY` |
| Functional TT mass-contraction derivative | Not submitted as broad proof | `MCP_TOOL_LIMIT`; kept as human-reviewed index derivation |
| Triangular KR Jacobian identity | Not submitted as broad proof | `MCP_TOOL_LIMIT`; kept as human-reviewed determinant derivation |

## Decision

`MCP_NARROW_CHECKS_ONLY`

MathDevMCP supports only a narrow algebraic quotient identity here.  The
functional and matrix-calculus derivations remain project derivations reviewed
in the text and by Claude; no broad certification is claimed.

