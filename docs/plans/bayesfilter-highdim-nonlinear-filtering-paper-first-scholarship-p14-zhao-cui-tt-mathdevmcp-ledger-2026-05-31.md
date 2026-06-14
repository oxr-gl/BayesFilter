# P14 Zhao-Cui TT MathDevMCP Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- P11/P12/P13 MathDevMCP ledgers.

what_is_not_concluded:
- No broad machine certification of the full TT proof.
- No certification of adaptive-code differentiability.
- No numerical implementation validation.

## Planned Narrow Checks

| Identity | Planned status |
|---|---|
| \(\partial(\log z-c)=\dot z/z-\dot c\) | `MCP_VERIFIED` |
| \((\dot q z-q\dot z)/z^2=\dot q/z-q\dot z/z^2\) | `MCP_VERIFIED` |
| \(A+\tau\cdot1=A+\tau\) for normalized defensive density | `MCP_VERIFIED` |
| Fixed interpolation derivative \(A\dot g=\dot b-\dot A g\) as product-rule algebra | `MCP_UNVERIFIED`; human derivation retained |
| Least-squares normal-equation derivative | Pending or human-reviewed if backend unsuitable |

Layer boundary:
Layers A and B may use MCP for scalar checks.  Layer D may use MCP only for
local product-rule sanity checks.  Layers C, E, F, and final proposition
linkage remain human-readable project derivations with MCP auxiliary at most.

Decision:
`P14_NARROW_SCALAR_IDENTITIES_VERIFIED_TT_AND_SOLVE_DERIVATIONS_HUMAN_REVIEWED`

## Check Details

- MathDevMCP certified the displayed log-shift score identity by normalized
  match.
- MathDevMCP certified the normalized-density derivative algebra by SymPy
  simplification.
- MathDevMCP certified the normalized defensive-density scalar
  \(A+\tau\cdot1=A+\tau\).
- MathDevMCP did not certify the symbolic interpolation product-rule check in
  the generic form submitted.  The note keeps the human derivation:
  differentiating \(Ag=b\) gives \(\dot A g+A\dot g=\dot b\), hence
  \(A\dot g=\dot b-\dot A g\) when the fixed solve branch is declared.
