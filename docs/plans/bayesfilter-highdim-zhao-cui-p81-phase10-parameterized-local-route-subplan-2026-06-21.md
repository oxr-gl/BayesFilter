# P81 Phase 10 Subplan: Parameterized Local-Route Tie-Out

status: EXECUTED_PENDING_REVIEW
date: 2026-06-21

## Phase Objective

Repair the P53 local-neighborhood transition route so it respects the P81
`ParameterizedZhaoCuiSIRSSM` theta convention, then verify on tiny fixtures
that local-route transition values and theta derivatives match the dense
transition reference.

Phase 10 is a parameterized semantics and derivative tie-out phase.  It is not
a d=18 full-history run, not an LEDH-PFPF-OT comparator phase, and not a
source-faithfulness phase.

## Entry Conditions Inherited From Phase 9

- Phase 8 proved only tiny dense-vs-streaming parity and integration coverage.
- SIR d=18 full-grid two-row propagation remains blocked by transition scaling.
- Phase 9 selected the P53 local-neighborhood route as the smallest
  implementable deterministic fixed-gradient diagnostic route.
- P53 local route is `extension_or_invention` for source-faithfulness claims.
- P53-M5 blocks exact d=18 local-route rank selection under the active 8 GiB
  memory contract.
- The concrete code gap is that the current local-route primitive discards
  `theta` and calls the unparameterized `transition_mean(previous)` signature.

## Required Artifacts

- This Phase 10 subplan.
- Phase 10 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase10-parameterized-local-route-result-2026-06-21.md`.
- Focused tests in `tests/highdim/test_p53_m4b_scaling_route_implementation.py`
  and/or `tests/highdim/test_p53_m4c_scaling_route_tieout.py`.
- Minimal implementation edits in `bayesfilter/highdim/transition_route.py`.
- Updated P81 master, runbook, execution ledger, Claude review ledger, and stop
  handoff.

## Required Checks, Tests, And Reviews

Review this subplan with Claude read-only before implementation.  Claude is a
reviewer only and cannot authorize boundary crossings.

Allowed implementation edits:

- add a narrow route-accessor/helper layer in `transition_route.py` that handles
  both direct `SpatialSIRSSM` models and `ParameterizedZhaoCuiSIRSSM` wrappers;
- route metadata, covariance checks, reachability neighborhoods, and variance
  access may use a normalized structural model such as `model.base_model` when
  the wrapper exposes one, because these quantities are theta-independent for
  the P81 SIR parameterization;
- transition means must still use the theta-dependent model path, e.g.
  `model.transition_mean(theta, previous)` or an equivalent `scaled_model(theta)`
  route, not the base-model transition mean;
- remove the unconditional `del theta` from the local-route primitive;
- keep TensorFlow operations on the differentiable path;
- add focused tests proving the parameterized value and theta-gradient
  semantics.

Required local checks after implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/transition_route.py tests/highdim/test_p53_m4b_scaling_route_implementation.py tests/highdim/test_p53_m4c_scaling_route_tieout.py
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p53_m4b_scaling_route_implementation.py tests/highdim/test_p53_m4c_scaling_route_tieout.py
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "horizon0 or two_row"
```

Review the execution result with Claude read-only after checks complete.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the local-neighborhood transition factor route obey the same theta convention as `ParameterizedZhaoCuiSIRSSM` and match dense transition value/theta derivatives on tiny fixtures? |
| Exact baseline/comparator | Dense transition reference from `_multistate_pairwise_transition_between_grids_log_density` or `model.transition_log_density(theta, previous, current, t)` on tiny retained grids. |
| Primary pass criterion | Tiny `ParameterizedZhaoCuiSIRSSM` local-route transition log-density and predictive log-density match dense reference within existing P53 tolerances, and theta-gradient/JVP through transition parameters matches dense reference. |
| Veto diagnostics | Any local-route theta derivative is `None` when dense derivative is nonzero; local value differs from dense value beyond tolerance; current-gradient tie-out regresses; P81 horizon/two-row gates regress; code uses NumPy on differentiable path; d=18 full-grid run is attempted; source-faithfulness is claimed. |
| Explanatory diagnostics | Magnitudes of theta gradients, existing current-gradient tie-out, metadata/replay identity, and P53-M5 memory blocker status. |
| Not concluded | No d=18 full-history correctness, no LEDH-PFPF-OT agreement, no HMC readiness, no posterior validity, no source-faithfulness, no default readiness. |
| Artifact preserving result | Phase 10 result markdown and updated focused tests. |

## Implementation Sketch

1. Add private helpers such as `_local_route_structural_model(model)` and
   `_transition_mean_for_local_route(model, theta, previous)` in
   `transition_route.py`.
2. Use the structural helper for theta-independent route metadata:
   `process_covariance`, `neighbor_sets`, `_rk4_substeps`, `state_dim()`, and
   `observation_dim()`.
3. If the model has a positive `parameter_dim()`, call
   `model.transition_mean(theta, previous)`.
4. Otherwise call `model.transition_mean(previous)`, preserving the existing
   `SpatialSIRSSM` behavior.
5. Use those helpers inside metadata construction, covariance validation,
   reachability-neighborhood construction, and
   `spatial_sir_local_coordinate_log_factor`.
6. Add a parameterized test fixture using `highdim.parameterized_zhao_cui_sir_austria_model()`
   or a small `ParameterizedZhaoCuiSIRSSM` wrapper around a small
   `p30_spatial_sir_fixture_model`.
7. Test tiny local-vs-dense transition value parity for theta values with
   nonzero log-kappa/log-nu scales.
8. Test theta-gradient or JVP parity for a scalar local-vs-dense objective.  The
   derivative for `log_obs_noise_scale` is expected to be zero for transition
   density; `log_kappa_scale` and `log_nu_scale` should be finite and nonzero
   for the selected fixture.
9. Add a test that parameterized route metadata can be constructed without
   requiring the wrapper to directly expose `process_covariance`,
   `neighbor_sets`, or `_rk4_substeps`.
10. Rerun existing P53 current-gradient and P81 horizon/blocker checks.

## Forbidden Claims And Actions

- Do not run LEDH-PFPF-OT diagnostics.
- Do not run d=18 full-grid transition propagation.
- Do not run GPU/CUDA commands in Phase 10.
- Do not install/fetch packages, use network, launch detached agents, change
  defaults, or take destructive git/filesystem actions.
- Do not claim source-faithfulness; this local/operator route remains
  `extension_or_invention` for source-faithful Zhao-Cui claims.
- Do not claim HMC readiness, posterior validity, production/default readiness,
  or scientific validity.

## Exact Next-Phase Handoff Conditions

If Phase 10 passes, the next phase may draft a memory/rank/compression policy
phase for making the parameterized local route meaningful beyond lower-rung
tie-out.  It may not jump directly to LEDH-PFPF-OT comparison unless a reviewed
subplan establishes a d=18 candidate full-history score route under a memory
and runtime contract.

If Phase 10 fails because the parameterized local route cannot match dense
value/theta derivatives on tiny fixtures, write a blocker result and do not
advance.

## Stop Conditions

Stop if Claude review does not converge after five rounds, if tiny
parameterized value or theta-derivative tie-out fails, if the implementation
requires a non-TensorFlow differentiable path, if current-gradient or P81 gate
tests regress, if a d=18 full-grid run is required, or if the route cannot be
kept within the deterministic diagnostic claim boundary.
