# P12 Zhao-Cui TT MathDevMCP Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- P12 self-contained proof-expansion note.

what_is_not_concluded:
- No broad machine certification of Zhao-Cui.
- No certification of TT-cross, SIRT, adaptive branches, or companion code.
- No certification of posterior accuracy or HMC readiness.

## Checks Attempted

| Obligation | Status | Result |
|---|---|---|
| \(\partial(\log Z-c)=\dot Z/Z-\dot c\), represented as \(dZ/Z-dc=(dZ-Zdc)/Z\) | `MCP_VERIFIED` | SymPy simplified the difference to zero under \(Z\ne0\). |
| Normalized-density derivative algebra \(\dot(q/Z)=(\dot q Z-q\dot Z)/Z^2\) | `MCP_VERIFIED` | SymPy simplified the equivalent form to zero under \(Z\ne0\). |
| Finite product rule in scalar notation \(d(ABC)=\dot A BC+A\dot B C+AB\dot C\) | `MCP_VERIFIED` | MathDevMCP exact normalization matched both sides. |
| Fixed scalar interpolation sensitivity from \(Ag=b\): \(A((db-dA g)/A)+dA g=db\) | `MCP_VERIFIED` | SymPy simplified to zero under \(A\ne0\). |
| Scalar weighted least-squares normal-equation sensitivity form | `MCP_VERIFIED` | SymPy verified that the proposed solution satisfies the scalar normal-equation derivative under \(A\ne0,w\ne0\). |
| Function-valued identity \(\partial\int\phi^2=2\int\phi\partial\phi\) | `MCP_TOOL_LIMIT` | Not encoded as a certifying callable-integral obligation; treated as human-reviewed calculus under regularity assumptions. |
| Full TT mass-contraction derivative | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | Product-rule structure is explicit, but full tensor/matrix contraction was not machine-certified. |

## Interpretation

MathDevMCP supports narrow algebraic pieces used in Proposition 2.  It does
not certify the Zhao-Cui algorithm, SIRT construction, adaptive TT-cross/rank
behavior, source claims, or implementation correctness.

Decision:
`NARROW_IDENTITIES_VERIFIED_BROAD_PROOF_HUMAN_REVIEWED`
