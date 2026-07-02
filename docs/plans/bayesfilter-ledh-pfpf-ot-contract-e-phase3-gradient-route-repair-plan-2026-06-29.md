# Contract E Phase 3 Gradient Route Repair Plan

Date: 2026-06-29

Status: `R0_CONTAINMENT_EXECUTED`

## Problem Statement

The Phase 3 Contract E LGSSM gradient diagnostic was wired to a generic
`tf.GradientTape` over the full Contract E scalar.  The route name
`manual-custom-vjp` was misleading: it selected a manual/custom VJP only for
the Sinkhorn transport matrix, not for the full LEDH likelihood score.

This invalidates the Phase 3 reverse-gradient evidence path.  The existing
finite-difference values remain useful as forward-scalar diagnostics, but the
current reverse route must not be used as material gradient evidence.

## Objective

Repair the Phase 3 gradient program so that a material Contract E LGSSM
gradient gate cannot run unless the score route is a full manual likelihood
reverse scan with each derivative boundary accounted for.

## Entry Conditions

- Phase 2 Contract E LGSSM value gate is closed as passed.
- Phase 3 precheck is blocked because finite 13-point FD slopes coexist with
  `NaN` reverse gradients.
- Claude bounded review agreed that the leading issue is the current taped
  reverse route, not proved Contract E mathematics.
- Existing manual LGSSM score pattern is available in
  `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`.

## Repair Phases

### Phase R0: Containment And Route Naming

Objective:
Make the current bad wiring impossible to promote.

Implementation details:

- Rename the route semantics in the Phase 3 diagnostic from
  `manual-custom-vjp` to `manual-transport-vjp-only`.
- Keep the old spelling only as a rejected compatibility alias if needed for
  already-written artifacts; do not use it in new material commands.
- Add a hard material-mode guard:
  `--gate-mode material` must fail unless the score route is a future
  `manual-likelihood-reverse-scan`.
- Record the blocker code:
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.

Required artifacts:

- Patched `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`.
- Static route audit test under `tests/`.

Checks:

- `python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`
- focused pytest for the new route-audit test.

Evidence contract:

- Question: can the current Phase 3 script accidentally run a material
  gradient gate through generic `GradientTape`?
- Pass criterion: no; material mode is blocked and the source-level audit
  detects that the only current gradient function is diagnostic/taped.
- Nonclaim: no Contract E gradient has been repaired yet.

Stop conditions:

- The script can still run material mode with a taped score route.
- The test relies only on prose and does not inspect the relevant source.

### Phase R1: Manual Likelihood Reverse-Scan Design

Objective:
Design the full Contract E score route before implementation.

Implementation details:

- Start from the old LGSSM manual score pattern:
  `_lgssm_manual_value_and_score`, `_transport_forward`, `_transport_vjp`,
  `_normalize_log_weights_with_floor_vjp`, `_log_weight_correction_vjp`,
  `_batched_ledh_linearized_flow_vjp`.
- Add a derivative-boundary table for:
  transition noise, LEDH flow, transition/observation log densities,
  normalization/floor, transport, Contract E reset, and time recursion.
- Contract E reset must be explicitly classified as one of:
  `manual_vjp_implemented`, `stop_gradient_by_design`, or `blocked`.
- No `tf.GradientTape`, `ForwardAccumulator`, or `transport_ad_mode=full` may
  appear in the material score route.

Required artifacts:

- Phase R1 subplan/result.
- Route manifest or source audit record binding the exact score entrypoint.

Checks:

- AST/source audit proving no generic score autodiff in the selected route.
- Claude bounded read-only review with exact path anchors.

Stop conditions:

- Any derivative boundary is implicit.
- Contract E reset derivative status is unstated.

### Phase R2: Local Contract E Reset VJP Decision

Objective:
Determine whether Contract E reset can be differentiated manually and safely.

Implementation details:

- Isolate the reset map
  `(post_flow, weights, matrix, residual_noise) -> y_star`.
- Test local VJP candidates against 13-point FD on tiny 1d/2d fixtures.
- Treat eigensystem/sqrt/pinv-sqrt derivatives as a separate risk; do not
  silently use TensorFlow autodiff through them.
- If a robust manual VJP cannot be produced, close Phase 3 as blocked or use a
  deliberately stopped reset only with a clear bias/nonclaim ledger.

Required artifacts:

- Local reset VJP derivation note or blocker.
- Tiny local reset parity diagnostic.

Stop conditions:

- Local reset VJP is nonfinite.
- Reset derivative silently falls back to generic autodiff.

### Phase R3: Integrate Manual Contract E LGSSM Score

Objective:
Wire the manual likelihood reverse scan into the Phase 3 LGSSM diagnostic.

Implementation details:

- Use `tf.while_loop` for forward and reverse scans.
- Preserve batched seeds, XLA compilation, TF32 default, and the frozen Phase 3
  FD protocol.
- Emit route metadata:
  `score_route=manual_likelihood_reverse_scan_no_autodiff`.
- Keep FD as an independent comparator, not as a replacement for the score
  route.

Checks:

- CPU-hidden small-N smoke with route audit.
- Trusted GPU/XLA/TF32 material run only after the route audit passes.

Stop conditions:

- Nonfinite manual gradients.
- Route audit fails.
- FD protocol mismatch.

### Phase R4: Resume Material Phase 3 Gate

Objective:
Run the original Phase 3 material LGSSM gradient gate with the repaired route.

Implementation details:

- `N=1000`, 10 seeds, 1d/2d LGSSM, exact Kalman comparator.
- Same 13-point FD regression: drop highest and lowest objective values and
  regress the remaining 11 points with explicit slope SE.
- Compare manual reverse to exact Kalman and same-scalar FD within the stated
  uncertainty contract.

Stop conditions:

- More than 2 standard-error disagreement without reviewed explanation.
- Missing MCSE/FD SE.
- Any GPU/XLA/TF32 metadata mismatch.

## Reviewer Contract

Claude may review exact paths read-only.  Claude is not an execution authority.
For this repair, Claude review must cite exact paths or line anchors for:

- whether material mode is blocked for the taped route;
- whether the route naming distinguishes transport-only VJP from full
  likelihood reverse scan;
- whether the next implementation phase accounts for each derivative boundary;
- whether any unsupported scientific or product claim is being made.

## Immediate Execution Slice

Execute Phase R0 only in this turn:

1. Patch the diagnostic route naming and material-mode guard.
2. Add the static route-audit test.
3. Run py_compile and focused pytest.
4. Write a concise result note if checks pass or a blocker note if they fail.

No GPU run, FD run, material gradient run, or Contract E gradient claim is
authorized by this repair slice.
