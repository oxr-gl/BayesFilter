# P53-M4A Result: Scaling Route Choice And Derivation

metadata_date: 2026-06-10
phase: P53-M4A
status: PASS_P53_M4A_SCALING_ROUTE_DERIVATION

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Which concrete scaling route should be implemented next, and what equations, approximation status, replay identity, route-width metadata, memory model, and tie-out criteria define it? |
| Baseline/comparator | P53-M1 route design, P53-M2 `C_low` implementation, P53-M3 dense tie-out, historical P53-M4 blocker, P30 spatial SIR equations, and current dense route. |
| Primary criterion | Met for derivation: exactly one `C_scale` route is selected, with equations, exactness scope, replay identity, route-width metadata, memory model, gradient variables, and lower-rung tie-out criteria. |
| Veto diagnostics | Not fired: route choice is not deferred to M4B; `C_low` is not relabeled as `C_scale`; approximation scope is explicit; route-width and tie-out criteria are declared. |
| Nonclaims | No scaling-route implementation, no scaling-route tie-out, no M4D admission, no rank-selection readiness, no d=18/d=50/d=100 readiness, no HMC or GPU readiness. |

## Selected Route

P53-M4A selects:

```text
route_id: p53_spatial_sir_local_neighborhood_contraction
route_class: scaling_route
selected_design: local-neighborhood sparse transition contraction
```

The TT-MPO operator route is not selected for this immediate repair.  It remains
a plausible later end state, but it requires a separate operator-compression
design before implementation.

## Mathematical Derivation

Let the spatial SIR state be

```text
z = (S_1, I_1, ..., S_J, I_J)
```

and let the one-step RK4 transition mean be

```text
Phi(z) = transition_mean(z).
```

For diagonal process covariance

```text
Q = diag(sigma_1^2, ..., sigma_d^2),
```

the transition log-density factorizes over current coordinates:

```text
log K_theta(x, z)
  = sum_{a=1}^d log Normal(x_a ; Phi_a(z_{N_a}), sigma_a^2),
```

where `N_a` is the previous-coordinate dependency neighborhood for the `a`th
transition-mean coordinate.  `N_a` is computed by composing the SpatialSIRSSM
one-step RK4 dependency graph for the model's `rk4_substeps`.

This is a scaling route because the local factors depend on bounded dependency
neighborhoods rather than on full current/previous global pairs.  The
implementation target is a local contraction against the retained TT density,
not a block-streaming all-pairs matrix.

## Exactness Scope

The selected route is exact under these conditions:

- process covariance is diagonal;
- each `N_a` contains every previous-state coordinate on which `Phi_a` depends;
- no neighborhood truncation is used.

The route must block rather than pass if:

- process covariance is non-diagonal and no separate reviewed
  covariance-factorization route is supplied;
- a dependency neighborhood is truncated for memory without declaring a new
  approximation plan;
- the route-width bound exceeds the configured memory cap.

## Replay And Metadata

The replay identity for M4B must include:

```text
(route_id,
 route_class,
 selected_design,
 rk4_substeps,
 dependency_neighborhoods,
 basis_order,
 TT rank metadata,
 R_eff,
 memory_forecast_bytes,
 covariance_scope,
 dtype,
 branch id)
```

The conservative route-width bound is:

```text
R_eff = max_a q^{|N_a|} times local TT-rank contraction factors,
```

where `q` is the per-coordinate basis/grid order and `|N_a|` is the number of
previous coordinates in the largest dependency neighborhood.  The memory model
for local workspace is:

```text
O(d * q^w * r_left * r_right)
```

where `w = max_a |N_a|` and `r_left,r_right` are the adjacent retained TT ranks
seen by the local contraction.

## Tie-Out Contract For P53-M4C

P53-M4C must test Spatial SIR:

- J=1 / state dimension 2;
- J=2 / state dimension 4;
- J=3 / state dimension 6.

The baseline is the dense retained-grid route.  P53 `C_low` predictive update
may be used as a computational proxy only because P53-M3 already tied `C_low`
to the dense route on the same lower-rung family.  Tolerances are:

- predictive log-density absolute tolerance: `1e-8`;
- one-step log-increment absolute tolerance: `1e-8`;
- gradient absolute tolerance: `1e-6`.

M4C must also check:

- `route_class == scaling_route`;
- `R_eff` is finite and positive;
- memory forecast is finite and below the configured cap for the tie-out
  fixture;
- the implementation does not enumerate global current/previous dense pairs.

## Manifest

Persisted manifest:

- `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-manifest-2026-06-10.json`

Required token emitted:

`PASS_P53_M4A_SCALING_ROUTE_DERIVATION`

Forbidden tokens:

- `PASS_P53_M4B_SCALING_ROUTE_IMPLEMENTATION`;
- `PASS_P53_M4C_SCALING_ROUTE_TIEOUT`;
- `PASS_P53_M4D_SCALING_ROUTE_ADMISSION`;
- `PASS_P53_M5_RANK_SELECTION_INTEGRATION`.

## Validation

Focused validation command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p53_m4a_scaling_route_derivation.py tests/highdim/test_p53_planning_failure_lock.py
```

Result:

```text
12 passed in 0.04s
```

Additional check:

```bash
git diff --check
```

Result:

```text
exited 0
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; P53 is uncommitted workspace work |
| Environment | local Python environment |
| CPU/GPU status | CPU-only planned with `CUDA_VISIBLE_DEVICES=-1`; no GPU conclusion |
| Random seeds | N/A |
| Wall time | 0.04s for focused pytest; diff check exited immediately |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-subplan-2026-06-10.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-result-2026-06-10.md` |
| Manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-manifest-2026-06-10.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass P53-M4A pending Claude review | Local-neighborhood sparse contraction selected with exactness scope, metadata, and tie-out contract; focused tests passed | No `C_low` relabel; no route choice deferral | M4B implementation may reveal practical contraction complexity | Request Claude review, then advance to M4B if agreed | Implementation, tie-out, admission, rank/dimension readiness |

Required token:

`PASS_P53_M4A_SCALING_ROUTE_DERIVATION`
