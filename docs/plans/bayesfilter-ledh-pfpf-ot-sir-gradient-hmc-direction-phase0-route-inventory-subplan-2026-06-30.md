# Phase 0 Subplan: SIR Route Inventory And Governance Freeze

Date: 2026-06-30

Status: `DRAFT_PENDING_REVIEW`

## Phase Objective

Inventory the current P8p SIR gradient diagnostic route and freeze the
governance boundary before numerical debugging.  This phase must identify the
active scripts, tests, route defaults, material GPU/XLA/TF32 requirements, and
known comparators without making scientific gradient claims.

## Entry Conditions Inherited From Previous Phase

- Master program and visible runbook exist.
- No previous phase result exists.
- Worktree may be dirty; unrelated changes must be preserved.
- Material LEDH evidence must use GPU/XLA/TF32 with escalated execution, but
  Phase 0 is inventory and local wiring only.

## Required Artifacts

- Phase result: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase0-route-inventory-result-2026-06-30.md`
- Updated execution ledger: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-visible-execution-ledger-2026-06-30.md`
- Refreshed Phase 1 subplan if inventory changes the intended gate.

## Required Checks, Tests, And Reviews

Local checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
python -m pytest tests/test_ledh_pfpf_ot_p7_manual_score.py -q
```

The pytest command is a tiny CPU-hidden wiring test because the test itself
sets `CUDA_VISIBLE_DEVICES=-1`; it is not material LEDH GPU evidence.

Review:

- Claude read-only review is required for the master/runbook before launching
  this phase.
- Claude review of the Phase 0 result is optional unless the inventory changes
  a material phase boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact SIR route and diagnostics are available for the SIR gradient program? |
| Baseline/comparator | Local source inventory of P8p scripts and tests. |
| Primary criterion | Active route, default flags, route vetoes, existing checks, and output artifacts are identified accurately. |
| Veto diagnostics | Missing scripts, syntax failure, manual score unit failure, or discovery that the intended material route is not GPU/XLA/TF32 capable. |
| Explanatory diagnostics | Dirty worktree list, existing prior SIR artifacts, route metadata field names. |
| Not concluded | No gradient correctness, FD correctness, HMC readiness, posterior validity, or production budget promotion. |

## Forbidden Claims And Actions

- Do not claim SIR gradient correctness.
- Do not run material GPU diagnostics in Phase 0.
- Do not modify benchmark code.
- Do not treat CPU-hidden tests as production LEDH evidence.
- Do not revert unrelated dirty worktree changes.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- py_compile passes for the three active SIR diagnostics;
- the manual-score unit test passes or any failure is classified as a Phase 0
  blocker;
- the Phase 0 result identifies the comparator limitations for SIR;
- the Phase 1 subplan remains consistent with the route inventory.

## Stop Conditions

- A required active script is missing.
- The route inventory shows no viable GPU/XLA/TF32 manual reverse path.
- Local checks fail in a way that requires code changes before defining the
  gate.
- Claude review of master/runbook does not converge after five rounds.

## End-Of-Phase Close Protocol

1. Run required local checks.
2. Write the Phase 0 result.
3. Refresh Phase 1 subplan if needed.
4. Review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
