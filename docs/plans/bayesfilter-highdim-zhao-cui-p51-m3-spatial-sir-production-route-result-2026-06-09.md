# P51-M3 Result: Spatial SIR Production Route Preflight

metadata_date: 2026-06-09
phase: P51-M3
status: PASS_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT
supervisor: Codex
reviewer: Claude Code read-only

## Decision

P51-M3 passes the scoped route preflight for the same P47/P50 spatial SIR
production row by preserving and sharpening the route-architecture blocker.

Production spatial SIR filtering remains blocked by
`BLOCKED_M4B_ROUTE_ARCHITECTURE`.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | The current all-axes retained-grid route cannot avoid the production architecture blocker for the same P47/P50 target row. |
| Baseline/comparator | P47-M4b production-row manifest and P50-M6 spatial-SIR production blocker row. |
| Primary criterion | Passed as route preflight: the same target row is locked, complexity is machine-encoded, and the missing architecture is explicit. |
| Veto diagnostics | Passed: no lower-rung J=1 result is promoted to J=9 production; finite scores are not certified gradients; memory complexity is not ignored. |
| Not concluded | No production spatial SIR filtering readiness. No HMC readiness. |

## Preflight Finding

The current route materializes pairwise transition evaluations over an all-axes
retained grid.  For `sites = 9`, `state_dim = 18`, and `order = 3`, the
preflight count is:

```text
grid_points = 3^(2*9) = 387420489
pairwise_transition_evaluations = grid_points^2 = 150094635296999121
```

This exceeds the reviewed CPU cap by many orders of magnitude.  The required
architecture change is a streamed or factorized transition application that
does not materialize all `grid_points^2` pairs while preserving deterministic
replay, branch identity, TensorFlow/TFP differentiability, and production-row
metrics.

## Validation

Focused validation actually run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p51_spatial_sir_route_preflight.py tests/highdim/test_p50_spatial_sir_predator_prey_ladder.py tests/highdim/test_p47_m4b_m5b_production_repair.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q tests/highdim/test_p51_spatial_sir_route_preflight.py
git diff --check -- tests/highdim/test_p51_spatial_sir_route_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-manifest-2026-06-09.json docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-result-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p51-visible-execution-ledger-2026-06-09.md
```

Results:

- `14 passed, 2 warnings` for the focused pytest command.  The warnings were
  TensorFlow Probability deprecation warnings from the local environment.
- `compileall` passed.
- `git diff --check` passed.

## Nonclaims

- No production spatial SIR filtering readiness.
- No HMC readiness.
- No lower-rung J=1 to J=9 promotion.
- No certified nonlinear-model gradient correctness.
- No source-faithful adaptive TT/SIRT filtering.
- No S&P 500 reproduction.
