# Phase 5 Result: Per-Budget Process-Isolation Repair

Date: 2026-07-01

Status: `BLOCKED_BUDGET100_EXIT137`

## Decision

Phase 5 sharpened the Phase 4 blocker.

Budget 10 can complete as a standalone GPU/XLA/TF32 material artifact under the
frozen Phase 1 gate.  Budget 100 still exits with code 137 even when isolated
into its own Python process and preserving the reviewed chunking knobs.

The next blocker is therefore not cross-budget accumulation alone.  It is the
budget-100 material diagnostic shape at `N=64`, `T=3`, five seeds, 13 FD
offsets, XLA manual reverse, and the current diagnostic implementation.

## Budget 10 Complete Artifact

Command:

```bash
bash scripts/run_sir_gradient_phase5_budget10.sh
```

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-progress-2026-06-30.json`

Route and transport facts:

- `route_prerequisite_pass`: `true`
- `route_prerequisite_failed_checks`: `[]`
- GPU outputs observed for objective and gradient tensors.
- `tf32_execution_enabled`: `true`
- XLA JIT compiler: `true`
- score route: `manual_reverse_scan_no_autodiff`
- row residual: `1.4722347259521484e-05`
- row residual pass: `true`
- elapsed seconds: `1611.4168632070068`

Direction gate summary:

| Parameter | Manual | FD slope | Combined SE | Combined z | Precision pass | Direction pass | Reason |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| `log_kappa_scale` | -143.369888 | -263.185455 | 48.951077 | 2.447659 | false | false | `inconclusive_precision_veto` |
| `log_nu_scale` | 68.266624 | 105.052803 | 13.006940 | -2.828196 | true | false | `within_4_combined_se_requires_ladder_certificate` |
| `log_obs_noise_scale` | 46.060081 | 46.766800 | 0.546964 | -1.292074 | true | true | `within_2_combined_se` |

Interpretation:

- Budget 10 is a valid completed material artifact.
- Row residual convergence alone does not certify gradient agreement at budget
  10.
- `log_obs_noise_scale` passes the direction gate at budget 10.
- `log_kappa_scale` is precision-vetoed due to large seed-gradient MCSE.
- `log_nu_scale` is within 4 combined SE but needs a ladder certificate before
  it can pass under the frozen Phase 1 gate.

## Budget 100 Blocker

Command:

```bash
bash scripts/run_sir_gradient_phase5_budget100.sh
```

Artifact status:

- Progress artifact exists:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget100-progress-2026-06-30.json`
- Final JSON artifact was not written.
- Final Markdown artifact was not written.

Progress artifact:

```json
{
  "completed": [],
  "elapsed_seconds": 5.887642582063563,
  "stage": "budget_started",
  "steps": 100
}
```

Runtime outcome:

- TensorFlow created the GPU device.
- XLA service initialized for CUDA.
- Process exited with code 137 before completing budget 100.

Classification:

- `BLOCKED_SINGLE_BUDGET100_EXIT137`

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Partially answered. Budget 10 completed; budget 100 remains memory-blocked. |
| Baseline/comparator | Preserved for attempted budgets: same seeds, theta, offsets, exact chunking knobs, route, and gate. |
| Primary criterion | Failed to obtain budgets 10 and 100 complete artifacts; budget 100 exit-137 is the active blocker. |
| Veto diagnostics | Budget 100 exit 137 vetoes further budget-ladder promotion. |
| Explanatory diagnostics | Budget 10 gate details are valid; budget 100 has no completed direction diagnostics. |
| Not concluded | No HMC readiness, posterior correctness, production budget, nonlinear generalization, or finite-N conclusion. |

## Root-Cause Interpretation

The current material diagnostic implementation is too memory-heavy for budget
100 under the full `N=64`, `T=3`, five-seed, 13-offset, XLA manual reverse
configuration.  Per-budget process isolation removes cross-budget accumulation
but does not make budget 100 feasible.

The next engineering target should split the diagnostic more finely than the
budget level, most likely by seed group and/or FD direction/offset process, and
then aggregate scalar outputs into the same Phase 1 gate.  This is different
from changing the scientific criterion; it is an artifact-construction repair.

## Forbidden Conclusions

- Do not claim SIR gradient correctness.
- Do not claim Sinkhorn budget is or is not the root cause from budget 10
  alone.
- Do not claim HMC readiness.
- Do not run budget 200 or 400 before repairing budget 100 feasibility.
- Do not downgrade GPU/XLA/TF32 policy because the blocker is diagnostic memory
  shape, not a CPU/GPU correctness comparison.

## Next Handoff

Advance to Phase 6 closeout/handoff with the recommendation to create a new
reviewed subplan for finer-grained artifact construction:

- one process per seed group and budget for manual score;
- one process per FD direction, offset chunk, seed group, and budget for
  objective values;
- deterministic aggregation of per-seed gradients and per-offset objective
  means into the existing regression and Phase 1 gate.
