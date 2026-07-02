# Phase R12 Plan: GPU XLA TF32 Contract E Manual Score Route

Date: 2026-06-30

Status: `ACTIVE`

## Objective

Replace the R11 GPU/XLA/TF32 LGSSM Contract E score diagnostic's generic
outer-`GradientTape` route with a batched manual reverse-scan route.  The new
route must compute the transition-first log marginal likelihood value and the
three-parameter LGSSM score directly under TensorFlow XLA, using explicit VJPs
for transport, normalization, log-density corrections, LEDH flow, and Contract
E fixed-ridge reset.

## Problem Statement

R11 showed finite values on the production-default route
(`GPU`, `float32`, TF32 enabled, XLA, batched seeds, `N=1000`, `T=10`) but all
three score components were `NaN`.  The `skip-reset-computation` probe also
returned all-`NaN` scores, while direct one-step GPU/XLA probes gave finite
gradients.  Therefore the immediate blocker is score-route wiring, not evidence
that the Contract E mathematical repair or LGSSM estimator score is wrong.

The broken R11 score route is the nested compiled forward plus generic
outer-`GradientTape` wrapper in
`docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`.  The
known good structural template is the existing LGSSM statistical harness manual
reverse scan in `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`.

## Evidence Contract

- Scientific/engineering question: can the Contract E LGSSM production-default
  GPU/XLA/TF32 branch produce finite, auditable manual scores, and do those
  seed-mean scores match exact Kalman within the stated Monte Carlo uncertainty
  gate?
- Baseline/comparator: exact FP64 Kalman value and score for the same LGSSM
  fixture, parameter convention, observations, and transition-first likelihood
  scalar.
- Candidate route: batched TensorFlow `float32`, TF32 enabled, visible GPU,
  XLA `jit_compile=True`, no CPU LEDH evidence, no seed loop, no Python loop
  inside the compiled score route, and no generic outer `GradientTape` for the
  score.  The route uses `tf.while_loop` forward and reverse scans.
- Primary criterion: for `D=2,N=1000,T=10,seed_count=10`, the seed-mean value
  and all three score components are within `2*MCSE` of exact FP64 Kalman.
- Secondary fixture: `D=1,N=1000,T=10,seed_count=10` should also satisfy the
  same value and score gate.
- Veto diagnostics:
  - no visible logical GPU under trusted/escalated execution;
  - XLA disabled or no XLA compile evidence;
  - TF32 disabled;
  - any nonfinite value or score;
  - route source contains `tf.GradientTape` in the manual score path;
  - route source lacks `tf.while_loop` forward and reverse scans;
  - route source lacks the Contract E fixed-ridge reset VJP;
  - ridge failure;
  - covariance restoration residual above `5e-4`;
  - condition proxy above `1e8`.
- Explanatory diagnostics: seed SDs, MCSEs, z-scores, Sinkhorn row/column
  residuals, realized ridge, ridge attempts, covariance and mean residuals.
- Not concluded even if this passes: no same-scalar FD certificate at `N=1000`,
  no SIR/SV/nonlinear correctness, no HMC readiness, no production readiness,
  no proof that the ridge selector is differentiable, and no claim that the
  value bias is eliminated at finite `N`.
- Artifact: R12 JSON and markdown result under `docs/plans`, plus route-guard
  tests under `tests/` and implementation changes in the existing Contract E
  diagnostic files.

## Skeptical Plan Audit

- Wrong baseline risk: CPU material replay would not answer the production
  LEDH question.  R12 must use visible GPU/XLA/TF32 for evidence.
- Proxy metric risk: the old `2*seed_sd` pytest gate is not the scientific
  criterion for the seed average.  R12 uses `2*MCSE`.
- Hidden route mismatch risk: a route can be XLA and still use the wrong
  reverse path.  R12 must add route guards that reject generic score
  `GradientTape` and require explicit manual VJPs.
- False success risk: finite gradients alone do not prove correctness.  The
  score must be compared to exact Kalman under the fixed evidence gate.
- Over-tuning risk: do not change `N`, Sinkhorn budget, epsilon, ridge policy,
  or Kalman comparator while repairing score wiring.  R12 isolates route
  correctness from estimator tuning.
- Runtime risk: the `N=1000` dense transport route is compile-heavy.  Execute a
  small route-guard/static test first, then `D=2,T=1` finite-score smoke, then
  the full `D=2,T=10`/`D=1,T=10` gate.

Audit status: `PASS`.

## Implementation Plan

1. Add a manual Contract E LGSSM value-and-score function to
   `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`.
   The function must:
   - use a forward `tf.while_loop`;
   - write forward checkpoints to `TensorArray`;
   - save ancestors, transition noise, post-flow particles, corrected log
     weights, transport log weights, transport matrix, residual noise, selected
     fixed ridge, weights, and all LEDH flow auxiliary tensors needed by
     `_batched_ledh_linearized_flow_vjp`;
   - apply Contract E fixed-ridge reset using the minimal-ridge selected chart
     replayed with stopped ridge;
   - collect reset diagnostics.
2. Add a reverse `tf.while_loop` in the same compiled function.  The reverse
   scan must:
   - call `contract_e_cholesky_ridge_reset_fixed_ridge_vjp`;
   - call `_filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys`;
   - call `_normalize_log_weights_vjp` or the fixed-floor equivalent;
   - call `_log_weight_correction_vjp`;
   - call transition and observation Gaussian log-density VJPs;
   - call `_batched_ledh_linearized_flow_vjp`;
   - accumulate score components for `ar_coefficient`,
     `log_transition_variance`, and `log_observation_variance`;
   - propagate the previous-particle cotangent through the transition matrix.
3. Wire `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py`
   to use the new manual route by default, and update its manifest to label
   the route as manual reverse scan rather than outer tape.
4. Add route-guard tests that fail if the manual score route contains
   `GradientTape`, lacks `tf.while_loop`, lacks the reset VJP, or lacks the
   dense finite transport VJP.
5. Add or update `scripts/run_contract_e_r12_gpu_manual_score.sh` for the full
   R12 GPU/XLA/TF32 run.

## Planned Checks

Non-GPU local checks:

```bash
python -m py_compile \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py \
  docs/benchmarks/contract_e_reset_tf.py
python -m pytest tests/test_contract_e_cholesky_ridge_reset.py -q
python -m pytest tests/test_contract_e_phase3_gradient_route_audit.py -q
```

Trusted GPU/XLA checks:

```bash
bash scripts/run_contract_e_r12_gpu_manual_score.sh
```

The GPU command must be run with escalated/trusted sandbox permissions.

## Stop Conditions

- Stop if Claude review identifies a material plan flaw that cannot be fixed
  locally.
- Stop if route guards show the new route still uses generic score autodiff.
- Stop if `T=1` manual score is nonfinite; debug the specific primitive VJP
  before running full `T=10`.
- Stop if GPU is not visible under escalated execution, XLA is disabled, or TF32
  is disabled.
- Stop if the full run OOMs; record the blocker and propose a memory-specific
  subplan rather than silently switching to CPU.
- Stop if the full run is finite but fails the `2*MCSE` Kalman gate; record it
  as a real estimator or tuning failure, not as score-route success.

## Claude Review Contract

Claude is a read-only reviewer.  The review should check the plan for route
correctness, missing artifacts, hidden CPU/default-route drift, proxy metric
misuse, stop-condition gaps, and whether the manual route implementation plan
is specific enough to execute.  Claude cannot authorize scientific claims,
default-policy changes, or boundary crossing.
