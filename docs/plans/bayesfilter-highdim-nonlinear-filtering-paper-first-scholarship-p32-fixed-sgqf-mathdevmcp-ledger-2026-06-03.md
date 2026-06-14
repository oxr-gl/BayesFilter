# P32 FixedSGQF MathDevMCP Ledger

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- MathDevMCP checks in P32 are narrow algebra diagnostics only.
- They do not certify source fidelity, posterior accuracy, implementation correctness, or every equation in the note.

## Planned Checks

| id | obligation | status | result |
|---|---|---|---|
| P32-MCP-1 | derivative of scalar \(v^2/S\) analogue for innovation score | `MCP_TOOL_LIMIT` | function-derivative and simplified rational forms were not encodable by the current parser; human/project derivation remains in note |
| P32-MCP-2 | derivative of \(C/S\) scalar analogue for gain | `MCP_TOOL_LIMIT` | parser could not encode the rational identity; human/project derivation remains in note |
| P32-MCP-3 | derivative of posterior covariance scalar analogue \(P-K^2S\) | `MCP_TOOL_LIMIT` | parser could not encode the symbolic identity; human/project derivation remains in note |
| P32-MCP-4 | Cholesky fixed-branch identity in symbolic 2-by-2 or scalar analogue | `MCP_UNVERIFIED` | not completed in this pass |
| P32-MCP-5 | finite-difference toy derivative identity | `MCP_VERIFIED` | SymPy verified the scalar trace \(G=1/2\) arithmetic and cloud-sensitive bracket arithmetic |

## Notes

The failed parser checks are recorded as tool limits, not as mathematical
verification.  P32 must not claim broad machine certification.  The useful MCP
evidence is limited to arithmetic sub-identities in the finite-difference
examples.

## Status Taxonomy

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`
