# P8 Ch34 MathDevMCP Ledger

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: Rewritten `ch34`, P8 gradient-obligation ledger,
`ch18_svd_sigma_point.tex`, MathDevMCP diagnostics, and the scholarly
literature audit policy.

what_is_not_concluded: MathDevMCP diagnostics do not certify the chapter, HMC
correctness, posterior accuracy, or broad derivation validity.

## Planned Narrow Checks

| Obligation | Status | Evidence |
|---|---|---|
| \(\partial_i\log\det S=\tr(S^{-1}\dot S_i)\). | `MCP_TOOL_LIMIT` / `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | Direct derivative syntax was not encodable by the SymPy backend (`'Symbol' object is not callable`).  The chapter proof remains a human-reviewed matrix-calculus derivation. |
| Scalar quadratic-form algebra \(d(v^2/S)=2v\,dv/S-v^2dS/S^2\). | `MCP_VERIFIED` | `check_equality`: `2*v*dv/S - v**2*dS/S**2 == 2*dv*(v/S) - (v/S)**2*dS`, assumption `S != 0`; SymPy simplified lhs-rhs to zero. |
| Substitution \(w=v/S\) in the scalar score. | `MCP_UNVERIFIED_DIAGNOSTIC` | The backend did not use the assumption `w = v/S` as a rewrite rule.  Human review supplies the substitution. |
| UT weight sum \(k/(n+k)+2n/[2(n+k)]=1\). | `MCP_VERIFIED` | SymPy simplified lhs-rhs to zero under `n+k != 0`. |
| Fifth-degree rule weight sum. | `MCP_VERIFIED` | SymPy verified \(2/(n+2)+2n(n-1)/(n+2)^2+n(4-n)/(n+2)^2=1\). |
| Fifth-degree second-moment identity. | `MCP_VERIFIED` | SymPy verified \((4-n)/(n+2)+2(n-1)/(n+2)=1\). |
| Fifth-degree cross fourth-moment identity. | `MCP_VERIFIED` | SymPy verified \((n+2)^2/(n+2)^2=1\). |

## Broad Certification Status

`HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`: no broad chapter proof is certified.
