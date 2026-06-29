# P81 Phase 10 Result: Parameterized Local-Route Tie-Out

status: PASS_PHASE10_PARAMETERIZED_LOCAL_ROUTE_TIEOUT
date: 2026-06-21

## Phase Objective

Repair the P53 local-neighborhood transition route so it respects the
`ParameterizedZhaoCuiSIRSSM` theta convention, then verify on tiny fixtures
that local-route transition values and theta derivatives match the dense
transition reference.

## Skeptical Plan Audit

The plan passed after Claude Round 1 found a material scope issue.  The original
draft only named the `transition_mean` signature mismatch, but the local route
also needed wrapper-safe access to theta-independent structure:
`process_covariance`, `neighbor_sets`, and `_rk4_substeps`.  The subplan was
patched and Claude Round 2 agreed.

Phase 10 stayed inside its boundary:

- no LEDH-PFPF-OT diagnostics;
- no GPU/CUDA commands;
- no package installs or network;
- no d=18 full-grid transition propagation;
- no source-faithfulness, HMC-readiness, posterior-validity, production, or
  default-readiness claims.

## Implementation

Changed `bayesfilter/highdim/transition_route.py`:

- added `_local_route_structural_model(...)` to normalize direct
  `SpatialSIRSSM` models and `ParameterizedZhaoCuiSIRSSM`-compatible wrappers;
- added `_is_spatial_sir_structural_model(...)` as the structural route check;
- added `_transition_mean_for_local_route(...)` so direct SIR uses
  `model.transition_mean(previous)` and parameterized wrappers use
  `model.transition_mean(theta, previous)`;
- changed local-route metadata and covariance/neighborhood construction to use
  the theta-independent structural model;
- removed the unconditional theta discard from
  `spatial_sir_local_coordinate_log_factor`.

Changed focused tests:

- `tests/highdim/test_p53_m4b_scaling_route_implementation.py`
  - parameterized metadata uses base-model structure;
  - parameterized coordinate factor matches dense coordinate density under
    nonzero theta.
- `tests/highdim/test_p53_m4c_scaling_route_tieout.py`
  - parameterized local transition matrix and predictive log-density match a
    dense theta-aware reference;
  - parameterized theta gradients match the dense theta-gradient reference.

## Checks Run

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/transition_route.py tests/highdim/test_p53_m4b_scaling_route_implementation.py tests/highdim/test_p53_m4c_scaling_route_tieout.py
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p53_m4b_scaling_route_implementation.py tests/highdim/test_p53_m4c_scaling_route_tieout.py
```

Result:

```text
15 passed, 2 warnings in 7.94s
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "horizon0 or two_row"
```

Result:

```text
2 passed, 2 deselected, 2 warnings in 64.74s
```

```bash
git diff --check -- bayesfilter/highdim/transition_route.py tests/highdim/test_p53_m4b_scaling_route_implementation.py tests/highdim/test_p53_m4c_scaling_route_tieout.py
```

Result: passed.

## Evidence Contract Result

| Field | Result |
|---|---|
| Question | Does the local route obey `ParameterizedZhaoCuiSIRSSM` theta semantics on tiny fixtures? |
| Baseline/comparator | Dense theta-aware transition reference from `model.transition_log_density(theta, previous, current, t)`. |
| Primary criterion | Met on tiny fixtures: local transition/predictive values and theta gradients match dense references. |
| Veto diagnostics | Not fired: no `None` theta gradient, no value mismatch, no P81 gate regression, no non-TensorFlow differentiable path, no d=18 full-grid run. |
| Explanatory diagnostics | Existing P53 current-gradient tests still pass; P81 horizon/blocker tests still pass. |
| Not concluded | No d=18 full-history correctness, no LEDH-PFPF-OT agreement, no HMC readiness, no posterior validity, no source-faithfulness, no default readiness. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Pass Phase 10 pending Claude execution review | Tiny parameterized local-vs-dense value and theta-gradient tie-out passed | No regression in focused P53/P81 checks | d=18 memory/rank scaling remains unresolved; P53-M5 still blocks exact local route rank selection | Draft Phase 11 memory/rank/compression policy phase | d=18 full-history score route, LEDH comparator readiness, source-faithfulness, HMC/posterior/default readiness |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | Dirty worktree; no commit made |
| Commands | `py_compile`, focused P53 pytest, focused P81 pytest, `git diff --check` |
| Environment | Local Python environment |
| CPU/GPU status | CPU-hidden with `CUDA_VISIBLE_DEVICES=-1`; no GPU conclusion |
| Data version | N/A |
| Random seeds | N/A |
| Wall time | P53 pytest 7.94s; P81 pytest 64.74s |
| Output artifacts | This result file and Phase 11 subplan |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase10-parameterized-local-route-subplan-2026-06-21.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase10-parameterized-local-route-result-2026-06-21.md` |

## Nonclaims

Phase 10 does not establish d=18 full-history likelihood correctness, complete
fixed-branch score correctness, LEDH-PFPF-OT agreement, HMC or NUTS readiness,
posterior validity, source-faithfulness, production readiness, or default
readiness.  The local/operator route remains `extension_or_invention` for
source-faithful Zhao-Cui claims.

## Next Handoff

Proceed only after Claude reviews this execution result and the Phase 11
subplan.  Phase 11 should resolve the memory/rank/compression policy before any
d=18 candidate full-history score route or LEDH-PFPF-OT comparison.
