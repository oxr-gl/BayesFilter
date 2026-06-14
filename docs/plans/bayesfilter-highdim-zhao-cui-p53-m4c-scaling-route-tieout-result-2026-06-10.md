# P53-M4C Result: Scaling Route Lower-Rung Tie-Out

metadata_date: 2026-06-10
phase: P53-M4C
status: PASS_P53_M4C_SCALING_ROUTE_TIEOUT

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does the selected `C_scale` route reproduce its declared lower-rung target on J=1/J=2/J=3 under predeclared tolerances? |
| Baseline/comparator | Dense retained-grid route on J=1/J=2/J=3 spatial SIR fixtures.  P53 `C_low` remains only a computational proxy because P53-M3 tied it to dense. |
| Primary criterion | Met locally after validation: assembled local coordinate factors match dense transition logs, predictive log densities, one-step log increments, current-point gradients, and route metadata on J=1/J=2/J=3. |
| Veto diagnostics | Not fired: M4B token exists in the execution ledger; tie-out target and tolerances were predeclared by M4A; failing dimensions are not hidden; the result does not emit admission or rank/dimension readiness tokens. |
| Nonclaims | No M4D admission, no rank-selection readiness, no d=18/d=50/d=100 readiness, no production retained-TT contraction readiness, no HMC or GPU readiness. |

## Implementation

Added lower-rung tie-out adapter symbols in
`bayesfilter/highdim/transition_route.py`:

- `LocalNeighborhoodPredictiveResult`;
- `spatial_sir_local_pairwise_transition_log_density`;
- `spatial_sir_local_predictive_log_density`.

The adapter assembles the M4B coordinate-local factors:

```text
log K_theta(x,z) = sum_a log Normal(x_a ; Phi_a(z_N_a), sigma_a^2)
```

and compares the resulting pairwise transition matrix and predictive
log-density against the dense retained-grid route on J=1/J=2/J=3.  This is a
lower-rung diagnostic adapter, not the production retained-TT contraction.

## Manifest

Persisted manifest:

- `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4c-scaling-route-tieout-manifest-2026-06-10.json`

Required token emitted:

`PASS_P53_M4C_SCALING_ROUTE_TIEOUT`

This phase does not emit `PASS_P53_M4D_SCALING_ROUTE_ADMISSION`.

Forbidden tokens:

- `PASS_P53_M4D_SCALING_ROUTE_ADMISSION`;
- `PASS_P53_M5_RANK_SELECTION_INTEGRATION`;
- `PASS_P53_M6_SPATIAL_SIR_D18`.

## Validation

Focused validation command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p53_m4c_scaling_route_tieout.py tests/highdim/test_p53_m4b_scaling_route_implementation.py tests/highdim/test_p53_m4a_scaling_route_derivation.py tests/highdim/test_p53_planning_failure_lock.py
```

Result:

```text
23 passed, 2 warnings in 3.72s
```

Additional checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall bayesfilter/highdim/transition_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p53_m4c_scaling_route_tieout.py
git diff --check
```

Result:

```text
compileall exited 0
git diff --check exited 0
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; P53 is uncommitted workspace work |
| Environment | local Python environment |
| CPU/GPU status | CPU-only planned with `CUDA_VISIBLE_DEVICES=-1`; no GPU conclusion |
| Random seeds | N/A |
| Wall time | pytest 3.72s; compile/check commands completed successfully |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4c-scaling-route-tieout-subplan-2026-06-10.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4c-scaling-route-tieout-result-2026-06-10.md` |
| Manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4c-scaling-route-tieout-manifest-2026-06-10.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass P53-M4C pending Claude review | Local factor assembly ties out to dense on J=1/J=2/J=3 under predeclared tolerances and focused validation passed | No admission/rank tokens emitted; no d=18 claim | Production retained-TT contraction/admission still belongs to M4D and later phases | Request Claude review, then advance to M4D if agreed | Admission, rank selection, d=18/d=50/d=100 readiness |

Required token:

`PASS_P53_M4C_SCALING_ROUTE_TIEOUT`
