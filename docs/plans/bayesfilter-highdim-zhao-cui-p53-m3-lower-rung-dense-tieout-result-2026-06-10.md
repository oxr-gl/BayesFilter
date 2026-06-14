# P53-M3 Result: Lower-Rung Dense Tie-Out

metadata_date: 2026-06-10
phase: P53-M3
status: PASS_P53_M3_LOWER_RUNG_DENSE_TIEOUT

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does the P53-M2 route reproduce the dense lower-rung spatial SIR transition/predictive update on tiny grids within declared tolerances? |
| Baseline/comparator | Existing dense retained-grid spatial SIR transition route, P53-M2 streaming route, and P30 route equations. |
| Primary criterion | Spatial SIR J=1, J=2, and J=3 predictive log densities, one-step likelihood increments, and current-point gradients match the dense route under predeclared tolerances. |
| Veto diagnostics | Dense reference not changed; tolerances declared before execution; tie-out not skipped; result remains lower-rung only. |
| Nonclaims | This does not prove d=18/d=50/d=100 correctness or scaling-route readiness; does not establish HMC readiness or GPU readiness. |

## Declared Tolerances

The tolerances were declared before running the phase validation:

- predictive log-density absolute tolerance: `1e-10`;
- one-step log-increment absolute tolerance: `1e-10`;
- current-point gradient absolute tolerance: `1e-8`.

## Checks

Focused test file:

- `tests/highdim/test_p53_lower_rung_dense_tieout.py`

The test covers:

- Spatial SIR `J=1`, `J=2`, and `J=3`, corresponding to state dimensions
  `2`, `4`, and `6`;
- predictive log density from the P53 streaming route versus
  `bayesfilter.highdim.filtering._multistate_pairwise_transition_between_grids_log_density`;
- one-step likelihood increment as a downstream assembly check using the same
  observation density and quadrature weights after the predictive tie-out;
- TensorFlow gradient with respect to current physical grid points;
- route metadata and nonpromotion of the scaling-route gate.

## Manifest

Persisted manifest:

- `docs/plans/bayesfilter-highdim-zhao-cui-p53-m3-lower-rung-dense-tieout-manifest-2026-06-10.json`

Route class:

- `lower_rung_dense_equivalent`

Claim class:

- `interface_tieout_only_not_scaling`

Phase evidence class:

- `lower_rung_dense_tieout_not_scaling`

Scaling gate status:

- P53-M3 does not emit `PASS_P53_M4D_SCALING_ROUTE_ADMISSION`.
- P53-M5 through P53-M8 remain blocked until P53-M4D admits the scaling route.

## Validation

Focused validation command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p53_lower_rung_dense_tieout.py tests/highdim/test_p53_lower_rung_streaming_route.py tests/highdim/test_p53_planning_failure_lock.py
```

Result:

```text
15 passed, 2 warnings in 7.12s
```

The warnings were TensorFlow Probability `distutils` deprecation warnings and
did not affect the tie-out checks.

Additional checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall tests/highdim/test_p53_lower_rung_dense_tieout.py
git diff --check
```

Result:

```text
both commands exited 0
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; P53 is uncommitted workspace work |
| Environment | local Python environment |
| CPU/GPU status | CPU-only planned with `CUDA_VISIBLE_DEVICES=-1`; no GPU conclusion |
| Random seeds | N/A |
| Wall time | 7.12s for focused pytest; compile/diff checks exited immediately |
| Plan | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m3-lower-rung-dense-tieout-subplan-2026-06-10.md` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m3-lower-rung-dense-tieout-result-2026-06-10.md` |
| Manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p53-m3-lower-rung-dense-tieout-manifest-2026-06-10.json` |

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass P53-M3 pending Claude review | Spatial SIR J=1/J=2/J=3 dense tie-out passed with predeclared tolerances | Scaling-route admission token not emitted | Only lower-rung dense-equivalent route is tested | Send to Claude, then advance to P53-M4A if agreed | Scaling-route readiness, d=18/d=50/d=100 readiness, HMC readiness |

Required token:

`PASS_P53_M3_LOWER_RUNG_DENSE_TIEOUT`
