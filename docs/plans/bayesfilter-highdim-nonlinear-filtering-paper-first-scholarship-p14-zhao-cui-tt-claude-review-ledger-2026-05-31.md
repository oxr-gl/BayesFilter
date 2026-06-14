# P14 Zhao-Cui TT Claude Review Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- P10/P11/P12/P13 BayesFilter Zhao-Cui artifacts.

what_is_not_concluded:
- No posterior accuracy.
- No HMC readiness.
- No global derivative of adaptive TT-cross/rank-changing code.
- No production BayesFilter implementation.

## Finding Register

| Round | ID | Finding summary | Codex classification | Action taken | Evidence path | Status |
|---|---|---|---|---|---|---|
| Plan iter1 | P14-PLAN-1 | Missing source-discipline execution requirements for new pedagogical claims. | `ACCEPT` | Added source-discipline execution rule requiring claim labels `PAPER_EXPLICIT`, `DERIVED_IN_NOTE`, or `IMPLEMENTATION_INTERPRETATION`. | P14 plan `Source-Discipline Execution Rule` | `resolved` |
| Plan iter1 | P14-PLAN-2 | Pass criteria too subjective for chemistry/physics audience target. | `ACCEPT` | Added reader-panel ledger pass criteria for each section. | P14 plan `Evidence Contract` | `resolved` |
| Plan iter1 | P14-PLAN-3 | Veto diagnostics did not guard against more equations that still do not teach. | `ACCEPT` | Added veto for equations without intermediate derivation or explanation. | P14 plan `Veto diagnostics` | `resolved` |
| Plan iter1 | P14-PLAN-4 | MathDevMCP boundary too vague. | `ACCEPT` | Added layer-by-layer MCP boundary. | P14 plan `MathDevMCP Protocol` | `resolved` |
| Plan iter1 | P14-PLAN-5 | Review classification protocol lacked no-silent-drop closure discipline. | `ACCEPT` | Added finding register requirements with open/resolved/disputed/carried-forward statuses. | P14 plan `Claude Review Loop` | `resolved` |
| Plan iter1 | P14-PLAN-6 | Validation did not check Proposition 2 layers or failure-mode markers. | `ACCEPT` | Added `pdftotext` check for Layer A--F, why-this-matters, and failure-mode markers. | P14 plan `Validation` | `resolved` |
| Plan iter1 | P14-PLAN-7 | Missing explicit skeptical plan audit. | `ACCEPT` | Added skeptical plan audit section. | P14 plan `Skeptical Plan Audit` | `resolved` |
| Plan iter2 | P14-PLAN-8 | Residual risk: audience-fit remains indirect. | `ACCEPT` | Record as nonblocking limitation; reader-panel ledger and hostile review are proxies, not actual reader validation. | This ledger and result artifact | `resolved` |
| Plan iter2 | P14-PLAN-9 | Residual risk: heading grep cannot prove pedagogical quality. | `ACCEPT` | Record as nonblocking limitation; validation is structural, not sufficient by itself. | This ledger and result artifact | `resolved` |

Plan review history:
- Iteration 1: `REJECT`.
- Iteration 2: `ACCEPT`.

## Execution Review

| Round | ID | Finding summary | Codex classification | Action taken | Evidence path | Status |
|---|---|---|---|---|---|---|
| Exec iter1 | P14-EXEC-1 | Broken equation numbering/cross-references: labels inside unnumbered displays resolved to section numbers. | `ACCEPT` | Added note-local display numbering so cited displays resolve to unique equation numbers; rebuilt PDF and inspected `.aux`. | P14 note preamble; `.aux` labels now show unique equation numbers. | `resolved` |
| Exec iter1 | P14-EXEC-2 | Section 10 recipe cited collapsed references like "Solve either (7) or (7)" and "store \(a_t\) from (7)". | `ACCEPT` | Same numbering fix makes interpolation, least-squares, and marginal numerator references distinct. | PDF now shows interpolation `(52)`, least squares `(53)`, numerator `(56)`. | `resolved` |
| Exec iter1 | P14-EXEC-3 | Proposition 2 layer navigation undermined by broken numbering. | `ACCEPT` | Same numbering fix makes Layer A--F formulas and final score uniquely navigable. | `.aux` shows `eq:p14-layerA` as `(65)`, `eq:p14-lambda-extra` as `(68)`, final score as `(85)`. | `resolved` |

Execution review history:
- Iteration 1: `REJECT`.
- Iteration 2: `ACCEPT`.

Codex classification of iteration 2 residual risks:
- Audience-fit remains proxy-validated: `ACCEPT`, nonblocking limitation.
- Proposition 2 remains dense but navigable: `ACCEPT`, nonblocking limitation.
- Note proves fixed-branch filtering/gradient, not accuracy or adaptive
  differentiability: `ACCEPT`, intended scope.

Execution review conclusion:
`EXECUTION_ACCEPTED_ITER2`
