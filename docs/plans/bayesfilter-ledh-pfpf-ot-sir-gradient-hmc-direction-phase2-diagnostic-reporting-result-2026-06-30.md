# Phase 2 Result: Diagnostic Reporting And Test Hooks

Date: 2026-06-30

Status: `PASS`

## Decision

Phase 2 passes.  The SIR Sinkhorn budget diagnostic now emits the
machine-readable HMC-direction gate fields required by the Phase 1 contract,
including route prerequisites, combined uncertainty, precision vetoes,
supportive labels, numeric-vs-route-gated pass status, and pass/veto reasons.

## Implementation Summary

Changed:

- `docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py`
  - Added `_sir_hmc_direction_gate`.
  - Added `_route_prerequisite_gate`.
  - Added `combined_se`, `direction_scale`, `precision_pass`,
    `direction_gate_reason`, `near_equal_supportive`, `near_zero_direction`,
    sign status, and `max_abs_combined_z_finite_or_inf`.
  - Preserved `numeric_direction_pass` separately from route-gated
    `direction_pass`.
  - Made `direction_pass` and `all_raw_directions_hmc_direction_pass` require
    route prerequisites, so CPU/non-XLA/wrong-route runs cannot pass the HMC
    direction gate.
  - Added route prerequisite reporting in JSON/Markdown summaries.
- `tests/test_p8p_sir_hmc_direction_gate.py`
  - Added focused CPU-hidden tests for the SIR gate helper.
  - Covered precise 2-SE pass, precision veto, relative-error supportive-only,
    4-SE ladder certificate, row-residual veto, and route-prerequisite veto.

## Checks Run

Passed:

```bash
python -m py_compile docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
```

Passed:

```bash
python -m pytest tests/test_p8p_sir_hmc_direction_gate.py tests/test_ledh_pfpf_ot_p7_manual_score.py -q
```

Result: `11 passed, 2 warnings in 33.91s`.

Focused field check passed:

```bash
rg -n "route_prerequisite|numeric_direction_pass|route_prerequisite_veto|all_raw_directions_hmc_direction_pass|compiler_jit_compile|outputs_on_gpu" docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py tests/test_p8p_sir_hmc_direction_gate.py
```

## Claude Review

Phase 2 implementation review converged after two rounds.

- Round 1 found a material blocker: numeric direction gates could pass without
  route prerequisites.
- Codex added route prerequisites, route vetoes, and focused test coverage.
- Round 2 returned `VERDICT: AGREE`.

Review ledger:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-claude-review-ledger-2026-06-30.md`

## Gate Status

Phase 2 gate: `PASSED`.

Exact next-phase handoff conditions:

- Local checks passed.
- Code diff was reviewed by Claude.
- Phase 3 must validate the route prerequisite gate under trusted GPU/XLA/TF32
  execution.

## Nonclaims

- No material SIR gradient validation yet.
- No HMC/NUTS readiness.
- No exact SIR gradient proof.
- No posterior correctness.
- CPU-hidden tests are wiring checks only.

## Next Action

Run Phase 3 trusted GPU/XLA/TF32 route smoke and require
`route_prerequisites.route_prerequisite_pass == true` in the output artifact.
