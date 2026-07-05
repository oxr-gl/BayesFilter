# P84 Phase 1 Subplan: Author Basis And Domain Parity

Date: 2026-06-23

Status: `DRAFT_BLOCKED_PENDING_PHASE0`

## Phase Objective

Close or precisely block the gap between the author SIR basis/domain route
(`Lagrangep(4,8)` on `AlgebraicMapping(1)`) and the current local Legendre
diagnostic fitter.

## Entry Conditions Inherited From Previous Phase

- Phase 0 target freeze passed.
- Author source anchors are available.
- No Phase 1 implementation or run has been approved yet.

## Required Artifacts

- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase1-author-basis-domain-parity-result-2026-06-23.md`
- Optional implementation diff if a reviewed adaptation is approved.
- Updated execution ledger and Phase 2 subplan.

## Required Checks / Tests / Reviews

At minimum:

```bash
rg -n "Lagrangep\\(4,8\\)|AlgebraicMapping\\(1\\)|LegendreBasis1D|basis_dim|author_basis_dim|source_faithful|fixed_hmc_adaptation" \
  docs/plans \
  bayesfilter/highdim \
  third_party/audit/zhao_cui_tensor_ssm_p10/source -S
```

Claude read-only review is required for any parity/adaptation decision.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is there a source-backed author-basis/domain parity path, or must local Legendre remain diagnostic-only? |
| Baseline/comparator | Zhao-Cui author SIR source and P83/P84 basis documentation. |
| Primary criterion | A reviewed parity/adaptation decision with source anchors and tests, or a blocker. |
| Veto diagnostics | Claiming Legendre diagnostics equal author parity without review; missing author anchors. |
| Explanatory diagnostics | Basis cardinality, mapping semantics, local fitter compatibility. |
| Not concluded | No fit quality, correctness, rank convergence, production readiness. |
| Artifact | Phase 1 result. |

## Forbidden Claims / Actions

- Do not call local Legendre basis source-faithful author parity unless reviewed.
- Do not run long fitting or validation.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if the basis/domain route for fitting is classified as
`source_faithful`, `fixed_hmc_adaptation`, or blocked with explicit scope.

## Stop Conditions

Stop if author-basis/domain semantics cannot be anchored or classified.
