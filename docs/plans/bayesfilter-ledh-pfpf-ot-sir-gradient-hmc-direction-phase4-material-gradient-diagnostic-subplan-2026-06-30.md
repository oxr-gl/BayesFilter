# Phase 4 Subplan: Material SIR Gradient Diagnostic

Date: 2026-06-30

Status: `REPAIRED_AFTER_EXIT137_READY_FOR_REVIEW`

## Phase Objective

Run the first material SIR gradient diagnostic under GPU/XLA/TF32 using the
reviewed HMC-direction gate.  The run should classify whether the gradient
issue is absent, budget-related, finite-N-related, FD-window-related, or still
unexplained.

## Entry Conditions Inherited From Previous Phase

- Phase 3 GPU/XLA/TF32 smoke passed.
- Phase 2 diagnostic reporting fields are present.
- The Phase 1 gate is frozen before this material run.

## Required Artifacts

- Phase result: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-result-2026-06-30.md`
- JSON output: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-2026-06-30.json`
- Markdown output: `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-2026-06-30.md`
- Progress JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase4-material-gradient-diagnostic-progress-2026-06-30.json`
- Refreshed Phase 5 subplan if repair is needed.

## Required Checks, Tests, And Reviews

Escalated material command:

```bash
bash scripts/run_sir_gradient_phase4_material_diagnostic.sh
```

Review:

- Claude read-only review is required for the Phase 4 result before any
  pass/fail interpretation is promoted.

Local pre-run checks:

```bash
bash -n scripts/run_sir_gradient_phase4_material_diagnostic.sh
python -m py_compile docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py
```

Wrapper details:

- Uses `--regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6` so negative
  offsets are parsed as a value rather than as option-like tokens.
- Uses exact runtime chunking after the first material attempt was killed with
  exit code 137 during budget 100:
  - `--seed-microbatch-size 1`;
  - `--theta-offset-batch-size 2`.
- This chunking preserves the fixed seeds, theta offsets, budgets, route, and
  averaging contract.  It reduces peak memory by evaluating one seed group and
  at most two FD theta offsets at a time, then recombining by the existing
  seed-weighted mean and FD regression logic.
- Does not pass `--transport-plan-mode` or `--transport-ad-mode`; those are
  fixed internally by `diagnose_p8p_sir_sinkhorn_budget.py` as `streaming` and
  `stabilized`.
- Records progress JSON so a timeout or interruption preserves the last
  completed budget.

## Skeptical Pre-Run Audit

Status: `PASS_WITH_CONSTRAINTS`.

- Baseline/comparator is explicit: same fixed-randomness route and raw-theta
  regression FD, varying only Sinkhorn budget.
- The post-exit-137 chunking repair is an execution-shape change only.  It is
  allowed in Phase 4 because it preserves all seeds, theta offsets, budgets,
  route prerequisites, and regression/gate definitions.
- Proxy metrics are separated: row residual, relative error, R2, and runtime
  explain the result, but do not alone promote a pass.
- Promotion criterion is frozen by Phase 1; it is not changed after seeing
  Phase 4 output.
- Route mismatch is a veto: CPU, non-XLA, non-TF32, non-GPU outputs, or wrong
  score route cannot produce material evidence.
- The run is intentionally `N=64`, `T=3`, five seeds.  It can identify a
  discriminating failure pattern or a first material pass, but it cannot rule
  out finite-N effects globally.
- The artifact answers the current question because it reports route
  prerequisites, finite objective/gradient, row residual, regression FD slope
  SE, seed-gradient MCSE, combined SE, precision pass, and HMC-direction gate
  reason for every raw parameter and budget.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Under the default GPU/XLA/TF32 manual reverse route, does the SIR gradient pass the reviewed HMC-direction gate or identify a discriminating failure pattern? |
| Baseline/comparator | Same fixed-randomness 13-point regression FD across raw theta directions and Sinkhorn budgets. |
| Primary criterion | Route checks pass and each raw direction is classified by the Phase 1 gate, or a blocker/root-cause class is written. |
| Veto diagnostics | GPU/XLA/TF32 route failure, row residual violation for any claimed pass, nonfinite outputs, missing MCSE or FD SE, FD regression instability, unsupported exact-gradient claim. |
| Explanatory diagnostics | Budget trend, row residual trend, max absolute z, relative error, R2, per-seed MCSE, runtime/memory. |
| Not concluded | No posterior correctness, no HMC readiness, no global SIR production budget, no nonlinear-model generalization. |

## Forbidden Claims And Actions

- Do not revise the Phase 1 gate after seeing this run.
- Do not call a budget trend a root cause unless it discriminates the gradient
  gap as well as the residual.
- Do not treat N=64 as sufficient to rule out finite-N effects.
- Do not run CPU fallbacks as material evidence.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 if:

- Phase 4 passes but needs confirmation at higher N; or
- Phase 4 fails/blocks and the result identifies the smallest next
  discriminating ladder.

Advance directly to Phase 6 only if:

- Phase 4 cleanly passes all route and numerical gates and Claude agrees that
  no repair ladder is needed before closeout.

## Stop Conditions

- Material command fails due to environment or memory in a way requiring human
  runtime approval.
- Diagnostic output is insufficient to apply the gate.
- Claude finds a material interpretation flaw that does not converge within
  five rounds.

## End-Of-Phase Close Protocol

1. Run required material checks.
2. Write the Phase 4 result.
3. Draft or refresh Phase 5 or Phase 6 subplan.
4. Review the next subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
