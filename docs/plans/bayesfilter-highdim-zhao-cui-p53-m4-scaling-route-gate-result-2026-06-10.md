# P53-M4 Result: Scaling Route Gate

metadata_date: 2026-06-10
phase: P53-M4
status: BLOCK_P53_M4_SCALING_ROUTE_GATE
amendment_status: historical_blocker_superseded_by_P53_M4A_M4D_phase_split

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does BayesFilter have a real scaling route, distinct from lower-rung streaming dense-equivalent tie-out infrastructure, that can support rank/scaling phases? |
| Baseline/comparator | P53-M1 route design, P53-M2 lower-rung implementation, P53-M3 dense tie-out, P52-M4 blocker, and current dense route. |
| Primary criterion | Not met: no `scaling_route` implementation exists yet. |
| Veto diagnostics | Fired: P53-M1 through P53-M3 passed only for `lower_rung_dense_equivalent`; no local-neighborhood or TT-MPO route is implemented or tied out. |
| Nonclaims | No scaling-route readiness, no rank-selection readiness, no d=18/d=50/d=100 readiness, no production filtering correctness, no HMC readiness, no GPU readiness. |

## Decision

P53-M4 blocks.

The correct token is:

`BLOCK_P53_M4_SCALING_ROUTE_GATE`

This is a successful gated behavior, not a runbook failure.  It prevents the
P52 logical error from recurring: a lower-rung dense-equivalent route cannot be
promoted into rank selection or spatial SIR dimension scaling.

After review with the user, this result is also treated as evidence of a second
planning error: the original P53-M4 phase combined route choice, derivation,
implementation, tie-out, and admission into one overloaded phase.  The active
resume target is therefore P53-M4A, and the active unlock token is
`PASS_P53_M4D_SCALING_ROUTE_ADMISSION`.

## Why It Blocks

P53-M1 through P53-M3 established:

- route design and P30 notation for `C_low` versus `C_scale`;
- a TensorFlow `C_low` implementation;
- a lower-rung dense tie-out for Spatial SIR J=1/J=2/J=3.

They did not establish:

- local-neighborhood sparse transition contraction;
- TT-MPO transition operator;
- scaling-route replay identity;
- `R_eff` or conservative route-width metadata for `C_scale`;
- scaling-route lower-rung tie-out.

The P53-M2 route remains dense-equivalent: every current point still sums over
every previous retained point.  Its block streaming reduces peak memory for
lower rungs, but it does not remove dense pair semantics from the production
transition application.

## Manifest

Persisted manifest:

- `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4-scaling-route-gate-manifest-2026-06-10.json`

Emitted token:

- `BLOCK_P53_M4_SCALING_ROUTE_GATE`

Forbidden tokens:

- `PASS_P53_M4_SCALING_ROUTE_GATE` for the historical overloaded M4 gate;
- `PASS_P53_M5_RANK_SELECTION_INTEGRATION`;
- `PASS_P53_M6_SPATIAL_SIR_D18`;
- `PASS_P53_M7_SPATIAL_SIR_D50_D100`.

## Smallest Next Repair

The amended P53 program splits this repair into P53-M4A through P53-M4D.  P53-M4A
should choose one `C_scale` route:

- local-neighborhood sparse transition contraction; or
- TT-MPO factorized transition contraction.

It should then derive the TensorFlow contraction, implement it separately from
`C_low`, emit replay/memory/route-width metadata, and tie it out on J=1/J=2/J=3
before attempting rank selection.

## Validation

Focused validation command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p53_scaling_route_gate.py tests/highdim/test_p53_planning_failure_lock.py
```

Result:

```text
11 passed in 0.03s
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
| Wall time | 0.03s for focused pytest; diff check exited immediately |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4-scaling-route-gate-subplan-2026-06-10.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4-scaling-route-gate-result-2026-06-10.md` |
| Manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m4-scaling-route-gate-manifest-2026-06-10.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Block P53-M4 pending Claude review | Not met: no scaling-route implementation exists | Veto fired: only lower-rung dense-equivalent route passed | Which `C_scale` design to implement next | Send blocker to Claude, then stop before M5-M8 unless user authorizes a new C_scale repair plan | Scaling readiness, rank selection, d=18/d=50/d=100 readiness, HMC readiness |

Required token:

`BLOCK_P53_M4_SCALING_ROUTE_GATE`
