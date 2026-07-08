# P85 Phase 1 Subplan: Author Basis/Domain Semantics Inventory

Date: 2026-06-23

Status: `DRAFT_BLOCKED_PENDING_PHASE0`

## Phase Objective

Inventory the exact author and local basis/domain semantics needed to design a
setup-configurable BayesFilter basis/domain surface.

## Entry Conditions Inherited From Previous Phase

- Phase 0 has frozen P85 scope, role contract, XLA/static boundaries, and
  approval gates.
- P84 Phase 2 fitting remains blocked.
- No code implementation is authorized in Phase 1.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase1-author-basis-domain-inventory-result-2026-06-23.md`
- Updated execution ledger.
- Refreshed Phase 2 subplan.
- Optional Claude review entry for the Phase 1 result or Phase 2 subplan.

## Required Checks / Tests / Reviews

Run source/code scans over the exact anchors:

```bash
rg -n "Lagrangep\\(4, ?8\\)|AlgebraicMapping\\(1\\)|ApproxBases|BoundedDomain|user can switch|freedom of the polynomials" third_party/audit/zhao_cui_tensor_ssm_p10/source -S
```

```bash
rg -n "LegendreBasis1D|ProductBasis|BoundedInterval|no AlgebraicMapping\\(1\\) parity claim|fit_degree" bayesfilter/highdim tests/highdim docs/plans -S
```

Run documentation hygiene checks for P85 artifacts and send the Phase 1 result
to Claude as a bounded one-path read-only review if it affects the Phase 2
interface.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What author operations and local gaps must a configurable basis/domain setup represent? |
| Baseline/comparator | Author README, SIR script, `ApproxBases`, `Lagrangep`, `AlgebraicMapping`, and local Legendre-only code. |
| Primary criterion | A reviewed inventory classifies each basis/domain operation as `source_faithful`, `fixed_hmc_adaptation`, `extension_or_invention`, or `local_gap`. |
| Veto diagnostics | Missing paper/source/code anchors; claiming Legendre equals author parity; copying third-party code; using README alone for algorithmic correctness. |
| Explanatory diagnostics | Cardinality formulas, domain-map formulas, replication semantics, current manifest nonclaims. |
| Not concluded | No implementation, fit quality, correctness, XLA performance, or production readiness. |
| Artifact | Phase 1 result and refreshed Phase 2 subplan. |

## Forbidden Claims / Actions

- Do not implement code in Phase 1.
- Do not claim parity is repaired.
- Do not use source anchors to claim statistical correctness.
- Do not copy MATLAB source into BayesFilter production modules.
- Do not run fitting, GPU, HMC, LEDH, d=50/d=100, or long commands.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if Phase 1 records:

- exact author setup fields to represent;
- exact local gap fields to repair;
- classification labels for each operation;
- unresolved source uncertainties, if any;
- a refreshed Phase 2 design subplan that can consume the inventory.

## Stop Conditions

Stop if:

- `Lagrangep(4,8)` or `AlgebraicMapping(1)` semantics cannot be anchored;
- local code has already changed in a way that invalidates the P84 blocker and
  requires a new inventory;
- Claude review finds a material source-grounding flaw that cannot be patched
  within five rounds.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 1 result / close record;
3. draft or refresh the Phase 2 subplan;
4. review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
