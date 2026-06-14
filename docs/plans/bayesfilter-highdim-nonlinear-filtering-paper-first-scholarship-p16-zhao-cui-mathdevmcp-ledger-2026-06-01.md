# P16 Zhao-Cui MathDevMCP Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui JMLR 2024.
- P16 project derivations.

what_is_not_concluded:
- No broad machine certification of TT filtering.
- No certification of the adaptive Zhao--Cui implementation.
- No certification of posterior accuracy.

## Checks Attempted

| Obligation | Tool result | P16 status |
|---|---|---|
| \(d\log Z=dZ/Z\) for \(Z>0\) | `MCP_INCONCLUSIVE`: symbolic encoding failed for functional notation | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` |
| Differentiating \(N g=d\) gives \(N\dot g=\dot d-\dot N g\) | `MCP_UNVERIFIED`: simplifier could not certify from textual assumptions | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` |
| \(\int(\phi^2+\tau\lambda)=\int\phi^2+\tau\) when \(\int\lambda=1\) | `MCP_INCONCLUSIVE`: symbolic encoding failed | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` |
| \(d(R+\tau)=dR\) for frozen \(\tau\) | `MCP_INCONCLUSIVE`: symbolic encoding failed | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` |

## Decision

`MCP_TOOL_LIMIT_FOR_FUNCTIONAL_TT_IDENTITIES`

The identities remain elementary project derivations in the P16 note.  No broad
MCP certification is claimed.
