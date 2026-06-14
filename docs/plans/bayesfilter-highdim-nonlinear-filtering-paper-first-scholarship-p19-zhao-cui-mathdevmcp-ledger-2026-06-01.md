# P19 Zhao--Cui MathDevMCP Ledger

metadata_date: 2026-06-01

seed_papers:
- P15 fixed-branch implementation specification.
- P18 annotated companion.

what_is_not_concluded:
- No broad machine certification is claimed.
- MathDevMCP checks are narrow algebra/proof diagnostics only.

## Checks Attempted

| Check | Status | Notes |
|---|---|---|
| derivative of \(\log Z\) | `MCP_TOOL_LIMIT`; `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | Tool could not encode expressions like `diff(log(Z(beta)), beta)` and returned `Symbol object is not callable`; the note proves the identity manually in Sec. 2. |
| derivative of squared integral | `MCP_VERIFIED` for algebraic product skeleton; `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` for differentiation-under-integral step | Exact-normalization check verified the encoded algebraic identity \(2x\,dx=2x\,dx\); the integral interchange is a stated mathematical assumption in the note. |
| fixed linear-solve derivative | `MCP_VERIFIED` for scalar encoded solve rearrangement | Verified \(N((dd-dN\,g)/N)=dd-dN\,g\) under \(N\ne0\), matching the scalar version of \(N\dot g=\dot d-\dot N g\). |
| quotient derivative for carried filter | `MCP_VERIFIED` | Verified \((da\,Z-a\,dZ)/Z^2=da/Z-a\,dZ/Z^2\) under \(Z\ne0\). |
| two-coordinate mass contraction derivative | `MCP_VERIFIED` for product-rule skeleton; `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` for integral notation | Exact-normalization check verified the encoded product-rule skeleton \(dM_1M_2+M_1dM_2\). |

## Tool Limit Details

The broad derivative obligations were intentionally not machine-certified.  In
particular, the functional derivative syntax for \(Z(\beta)\) was not accepted
by the current MathDevMCP symbolic backend in this session.  P19 therefore uses
MathDevMCP as a narrow algebra checker only.  The calculus identities remain
human-reviewed derivations in the LaTeX note.

Decision: `MIXED_MCP_VERIFIED_AND_TOOL_LIMIT_NO_BROAD_CERTIFICATION`.
