# P31 Fixed-SGQF MathDevMCP Ledger

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- MathDevMCP does not certify the whole FixedSGQF note.
- MathDevMCP does not certify source fidelity to Jia--Xin--Cheng or Singh et al.
- MathDevMCP does not certify numerical stability, posterior accuracy, or HMC convergence.

## Planned Narrow Checks

| obligation | status | evidence |
|---|---|---|
| derivative of \(v^\top S^{-1}v\) with respect to \(S,v\), scalar check | `MCP_VERIFIED` | SymPy verified `2*dv*u - u*dS*u = 2*dv*u - u*u*dS`. |
| Gaussian innovation score sign and terms, scalar check | `MCP_VERIFIED` | SymPy verified the expanded scalar score with \(u=v/S\). |
| Cholesky sensitivity identity \(\dot L L^\top+L\dot L^\top=\dot P\) for \(B+B^\top=A\) | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | P31 proves it by substitution in Eq. `p31-chol-check`; no matrix backend proof claimed. |
| covariance derivative product rule | `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` | P31 derives by product rule; no broad matrix proof claimed. |
| Kalman gain derivative \(d(CS^{-1})\), scalar check | `MCP_VERIFIED` | SymPy verified `dC/S - C*dS/S**2 = dC/S - (C/S)*dS/S`. |
| toy finite-difference gradient simplification | `MCP_VERIFIED` | SymPy verified \(\theta[y^2/(1+\theta^2)^2-1/(1+\theta^2)] = \theta[y^2-(1+\theta^2)]/(1+\theta^2)^2\). |
| cloud-sensitive nonlinear trace score at \(\theta=1\) | `MCP_VERIFIED` | SymPy verified the displayed score expression equals \(4/9\). |
| symbolic substitution form for cloud-sensitive trace | `MCP_UNVERIFIED` | SymPy did not consume the textual substitution assumptions; this is a tool limitation, not a refutation. |

## Status Labels

- `MCP_VERIFIED`: narrow algebra equality checked by a backend.
- `MCP_UNVERIFIED`: attempted but not verified.
- `MCP_TOOL_LIMIT`: not suitable for the tool.
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`: reviewed in text but not machine certified.

mathdevmcp_status: `NARROW_SUPPORT_ONLY`
