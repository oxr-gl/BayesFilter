# P7 Gaussian/Transport/Tensor MathDevMCP Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P7 plan, `ch34`, `ch35`, `ch18_svd_sigma_point.tex`,
MathDevMCP diagnostics, and the scholarly literature audit policy.

what_is_not_concluded: MathDevMCP was used only for narrow algebraic
diagnostics.  This ledger does not conclude broad theorem certification,
chapter certification, HMC convergence, exact posterior accuracy, or production
readiness.

## Checks

| Obligation | Tool call summary | Status | Interpretation |
|---|---|---|---|
| Gaussian innovation score after substituting \(w=v/S\) in the scalar case. |
Checked equality between
\(-\frac12(dS/S+2\,dv\,v/S-v^2dS/S^2)\) and
\(-\frac12(dS/S+2\,dv\,(v/S)-(v/S)^2dS)\). | `MCP_VERIFIED` | Confirms the
scalar solve-form score algebra after explicit substitution. |
| Gaussian innovation score with symbolic assumption \(w=v/S\). | Checked
same equality using assumption string `w = v/S`. | `MCP_INCONCLUSIVE` |
SymPy did not use the textual assumption; recorded as tool limitation, not a
mathematical refutation. |
| Corrected proposal identity. | Checked
\((\phi\gamma/q)/(\gamma/q)=\phi\) under \(q\ne0\), \(\gamma\ne0\). |
`MCP_VERIFIED` | Confirms the algebraic cancellation behind corrected proposal
expectations, not integrability/support conditions. |
| PSD toy perturbation off-diagonal cancellation. | Checked
\((1+\epsilon)-(1+\epsilon)=0\). | `MCP_VERIFIED` | Supports the eigenvector
calculation context. |
| PSD toy negative eigenvalue expression. | Checked \(1-(1+\epsilon)=-\epsilon\).
| `MCP_VERIFIED` | Supports the two-by-two covariance caution. |

## Limits

MathDevMCP did not certify:

- matrix-calculus identities in full generality;
- differentiability of covariance factors;
- sparse-grid or TT branch smoothness;
- source theorems;
- HMC validity, convergence, or posterior accuracy;
- PDF correctness or readability.

Those remain human-reviewed project derivations and source-supported
exposition.
