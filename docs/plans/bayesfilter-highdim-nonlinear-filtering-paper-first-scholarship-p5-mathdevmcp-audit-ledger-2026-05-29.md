# P5 MathDevMCP Audit Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P5 analytical-gradient obligations in `ch33` and `ch36`.

what_is_not_concluded: MathDevMCP diagnostics do not certify the chapters as
machine-verified proofs, do not prove integral differentiation conditions, do
not prove continuous-time/PDE adjoint formulas, do not establish posterior
accuracy, and do not validate HMC convergence.

## Protocol

P5 submitted only narrow algebraic or typed obligations:

- derivative of a log-normalizer as \(\nabla Z/Z\);
- quotient-rule form for normalized density sensitivity;
- scalar Gaussian HMC-gradient sign simplification;
- typed diagnostics for broad propositions.

Statuses:

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

## Results

| audit_id | obligation | tool | input | status | interpretation |
|---|---|---|---|---|---|
| `P5-MCP-1` | log-normalizer derivative algebra | `check_equality` | `dZ / Z = dZ / Z` under `Z > 0` | `MCP_VERIFIED` | Certifies only the displayed scalar algebra behind \(\nabla\log Z=\nabla Z/Z\). |
| `P5-MCP-2` | normalized density quotient-rule algebra | `check_equality` | `(dn*Z - n*dZ)/Z**2 = dn/Z - (n/Z)*(dZ/Z)` | `MCP_VERIFIED` | Certifies the scalar quotient identity used in the update sensitivity formula. |
| `P5-MCP-3` | one-observation scalar Gaussian HMC-gradient sign | `check_equality` | `-(y-q)/S + (q-mu0)/sig0**2 = (q-y)/S + (q-mu0)/sig0**2` | `MCP_VERIFIED` | Certifies only the algebraic sign simplification. |
| `P5-MCP-4` | two-observation scalar Gaussian gradient extension | `check_equality` | `-((y1-q)/S + (y2-q)/S) + (q-mu0)/sig0**2 = (q-y1)/S + (q-y2)/S + (q-mu0)/sig0**2` | `MCP_VERIFIED` | Certifies repeated-sum sign algebra for the toy example. |
| `P5-MCP-5` | broad likelihood sensitivity proposition | `typed_obligation_label` | `prop:bf-hd-likelihood-sensitivity` | `MCP_UNVERIFIED` / `typed_review` | Tool extracted context but could not certify integral sensitivity recursion.  Main text is human-reviewed under Assumption `ass:bf-hd-dominated`. |
| `P5-MCP-6` | broad HMC gradient contract proposition | `typed_obligation_label` | `prop:bf-hd-hmc-gradient-contract` | `MCP_UNVERIFIED` / `typed_review` | Tool could not certify the posterior/change-of-variables contract.  Main text is human-reviewed and source-grounded by HMC/change-of-variables logic. |

Decision: `SMALL_ALGEBRA_VERIFIED_BROAD_PROPOSITIONS_HUMAN_REVIEWED`.
