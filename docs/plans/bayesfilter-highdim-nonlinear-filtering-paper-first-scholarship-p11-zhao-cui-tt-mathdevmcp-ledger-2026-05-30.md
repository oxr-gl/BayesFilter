# P11 Zhao-Cui TT MathDevMCP Ledger

metadata_date: 2026-05-30

seed_papers:
- Zhao and Cui JMLR 2024.
- P11 fixed-branch analytical derivative note.

what_is_not_concluded:
- No broad machine certification.
- No certification of TT-cross, SIRT, or companion code.
- No certification of adaptive-branch differentiability.
- No HMC readiness.

## Checks Attempted

| Obligation | Status | Result |
|---|---|---|
| \(\partial_i(\log Z-c)=\dot Z/Z-\dot c\) as an algebraic score form | `MCP_VERIFIED` | SymPy simplified the checked expression to zero under \(Z\ne0\). |
| Product-rule form \(d(ABC)=\dot A BC+A\dot B C+AB\dot C\) in scalar symbolic notation | `MCP_VERIFIED` | MathDevMCP exact normalization matched both sides. |
| Normalized-density derivative \(\dot(q/Z)=(\dot q Z-q\dot Z)/Z^2\) | `MCP_VERIFIED` | SymPy simplified the checked expression to zero under \(Z\ne0\). |
| Function-valued squared-density normalizer derivative \(\dot{\int \phi^2+\tau}=2\int\phi\dot\phi+\dot\tau\) | `MCP_INCONCLUSIVE` | SymPy backend could not encode the function-valued obligation with callable \(\phi(\epsilon)\). |

## Interpretation

MathDevMCP supports only narrow algebraic obligations in this pass.  It does
not certify the Zhao-Cui TT derivative, TT-core sensitivity equations, QR/SVD
branch behavior, or implementation correctness.  The note may describe the
unchecked function-valued identities as human-reviewed calculus under stated
regularity assumptions, not as machine-certified.

Decision:
`HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`
