# P13 Zhao-Cui TT MathDevMCP Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- P11/P12 MathDevMCP ledgers.

what_is_not_concluded:
- No broad machine certification of the full TT proof.
- No certification of adaptive-code differentiability.
- No numerical accuracy or implementation readiness claim.

## Scope

P13 mainly changes exposition.  It preserves the P12 proposition substance.
P11/P12 already checked narrow identities for log-normalizer differentiation,
normalized-density derivative algebra, scalar product-rule analogues, fixed
interpolation sensitivity, and fixed weighted least-squares normal-equation
sensitivity.

New P13 algebra includes the scalar example normalizer and the same displayed
fixed-branch score in a human-readable structure.

## Status Before Additional P13 Checks

| Obligation | Status | Reason |
|---|---|---|
| \(\partial_i(\log z-c)=\dot z/z-\dot c\) | `MCP_VERIFIED_INHERITED_FROM_P12` | Same identity as P12. |
| Normalized-density derivative \(\partial(q/z)\) | `MCP_VERIFIED_INHERITED_FROM_P11` | Same identity as P11. |
| TT product rule and mass-contraction derivative | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | P12 human proof; broad TT contraction is beyond narrow symbolic check. |
| Scalar example \(\widehat Z=\iint\phi^2+\tau\lambda=\iint\phi^2+\tau\) for normalized \(\lambda\) | `PENDING_P13_CHECK_OR_HUMAN_REVIEW` | Added in P13. |
| Fixed interpolation and weighted least-squares sensitivity equations | `MCP_VERIFIED_OR_PARTIAL_INHERITED_FROM_P12` | Same equations as P12. |

Decision:
`P13_MATHDEV_SCOPE_DECLARED_PENDING_TARGETED_CHECKS`

## P13 Targeted Checks Run

| Obligation | Tool result | P13 status |
|---|---|---|
| Scalar example normalization: if \(A=\iint\phi^2\) and \(\int\lambda=1\), then \(A+\tau\int\lambda=A+\tau\). | MathDevMCP `check_equality`, SymPy simplified `A + tau*1` and `A + tau` to equality. | `MCP_VERIFIED` |
| Log-shift score algebra: \(\partial(\log Z-c)=\dot Z/Z-\dot c\). | MathDevMCP `check_equality`, normalized match. | `MCP_VERIFIED` |
| Normalized-density derivative algebra: \((\dot q z-q\dot z)/z^2=\dot q/z-q\dot z/z^2\). | MathDevMCP `check_equality`, SymPy simplified difference to zero. | `MCP_VERIFIED` |
| Direct fixed-branch score expression: \((\dot R+\dot\tau)/(R+\tau)-\dot c\). | MathDevMCP `check_equality`, normalized match. | `MCP_VERIFIED_AS_DISPLAY_CONSISTENCY` |

## Limits

MathDevMCP did not and cannot certify the full function-valued TT filtering
proof from these scalar checks.  The TT product rule, mass-contraction
derivative, previous-filter sensitivity recursion, and fixed interpolation or
least-squares derivative remain project derivations inherited from P12 and
human-reviewed in P13.

Final decision:
`NARROW_IDENTITIES_MCP_VERIFIED_FULL_TT_PROOF_HUMAN_REVIEWED`
