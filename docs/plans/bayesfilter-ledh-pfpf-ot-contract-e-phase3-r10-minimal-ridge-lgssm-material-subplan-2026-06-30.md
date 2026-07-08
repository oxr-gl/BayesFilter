# Phase R10 Subplan: Minimal Stabilizing Ridge Material LGSSM Gate

Date: 2026-06-30

Status: `ACTIVE`

## Phase Objective

Test whether replacing the R9 forced fixed ridge `lambda=0.75` with a
minimal-stabilizing Cholesky ridge chart removes the obvious covariance
distortion in the LGSSM Contract E material route, while preserving the
no-autodiff manual reverse scan and same-scalar finite-difference parity.

The intended policy is numerical stabilization only: choose the smallest
per-batch ridge on a declared ladder that makes the Cholesky chart valid, then
replay that chosen ridge as a fixed local chart for derivative checks.

## Entry Conditions

- R9 showed that the material route is no-autodiff and matches central
  same-scalar FD to about `1e-10` on `D=1,2,T=10,N=64,seed_count=10`.
- R9 failed the material statistical gate because the forced fixed
  `lambda=0.75` produced large covariance residuals and Kalman value/score
  disagreement.
- `contract_e_minimal_stabilizing_cholesky_ridge` exists in
  `docs/benchmarks/contract_e_reset_tf.py` and has focused unit tests for base
  and per-batch escalation behavior.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does a minimal stabilizing ridge, replayed as a fixed local chart, remedy the R9 fixed-ridge distortion for the LGSSM material diagnostic? |
| Baseline/comparator | R9 forced fixed ridge `lambda=0.75`; exact Kalman value/score is only a material comparator after same-scalar FD passes. |
| Primary promotion criterion | Stage B must pass same-scalar FD for all three parameters, have no ridge replay instability, have max covariance residual at or below `5e-4`, and have value/score means within `2*MCSE` of exact Kalman for `D=1,2,T=10,N=64,seed_count=10`. |
| Veto diagnostics | Any outer `tf.GradientTape` in material route; branch/ridge replay instability under FD perturbations; nonfinite value/score; ridge failure; covariance residual above the gate; Kalman value/score failure; CPU-hidden/device manifest mismatch for this R10 run. |
| Explanatory diagnostics | Realized ridge ladder values, base ridge, attempts, covariance and mean residuals, cotangent norms, and Stage A route-scaling behavior. |
| Not concluded even if passed | No GPU/XLA/TF32 readiness, no SIR/SV/nonlinear correctness, no HMC readiness, no production readiness, and no claim that the branchy ridge-selection map itself is differentiable. |
| Artifact preserving result | JSON artifacts under `/tmp/contract_e_phase3_r10_*_material.json` and R10 result note under `docs/plans`. |

## Skeptical Plan Audit

- Wrong baseline risk: compare against R9 `lambda=0.75`, not against the old
  eigensystem route or a moving tuned run.
- Proxy metric risk: small realized ridge is explanatory only.  It cannot
  promote the route unless covariance and exact Kalman gates pass.
- Hidden branch risk: the selector is branchy.  Derivative evidence is valid
  only for the replayed fixed chart, and FD perturbations must confirm that
  reselecting would keep the same ridge branch.
- Stale-context risk: R9 already validated the manual reverse wiring.  R10
  should not reopen that path unless same-scalar FD fails.
- Environment risk: this run is CPU-hidden FP64 material evidence.  It must not
  be reported as GPU/XLA/TF32 evidence.
- Artifact risk: a run that writes only aggregate status is insufficient.  The
  artifact must include ridge policy, realized ridges, replay stability, and
  reset residuals.

Audit result: proceed after patching the diagnostic to select ridges once on
the center route and replay those fixed ridges for manual VJP and FD scalars.

## Required Artifacts

- Updated `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`
  material route supporting `minimal_stabilizing_replayed_fixed_chart`.
- Focused tests showing the material route accepts minimal-ridge policy and
  serializes replay diagnostics.
- Stage A JSON artifact:
  `/tmp/contract_e_phase3_r10_stage_a_material.json`.
- Stage B JSON artifact:
  `/tmp/contract_e_phase3_r10_stage_b_material.json`, if Stage A passes.
- R10 result note:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r10-minimal-ridge-lgssm-material-result-2026-06-30.md`.

## Required Checks

1. `python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py docs/benchmarks/contract_e_reset_tf.py tests/test_contract_e_phase3_material_manual_route.py`
2. `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_contract_e_phase3_material_manual_route.py tests/test_contract_e_phase3_r7_lgssm_manual_route.py tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py tests/test_contract_e_phase3_r5_manual_reverse_integration.py tests/test_contract_e_cholesky_ridge_reset.py tests/test_contract_e_phase3_gradient_route_audit.py -q`
3. Stage A material command with `--chol-ridge-abs 1e-10 --chol-ridge-rel 1e-8 --chol-ridge-escalation 10 --chol-ridge-max-attempts 12`.
4. Stage B material command with the same ridge policy, only if Stage A passes.

## Forbidden Claims And Actions

- Do not claim the branchy ridge selector itself is differentiable.
- Do not compare manual gradients to FD values generated with a different ridge
  branch or different scalar.
- Do not treat CPU-hidden FP64 results as GPU/XLA/TF32 evidence.
- Do not tune `lambda` against Kalman agreement.  The ridge rule is minimal
  numerical stabilization only.
- Do not remove the full Phase 3 blocker unless Stage B passes all material
  criteria.

## Handoff Conditions

- If Stage B passes: write a result note proposing removal or narrowing of
  `PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION` for the
  CPU-hidden FP64 LGSSM material route only.
- If Stage B fails after same-scalar FD passes: write a blocker result
  identifying whether failure is due to ridge replay, covariance restoration,
  or Kalman statistical disagreement.
- If Stage A fails: stop before Stage B and write a focused R10 blocker result.

## Stop Conditions

- Any material route use of outer autodiff.
- Any FD branch/ridge replay instability.
- Any ridge failure or nonfinite scalar.
- Any artifact missing ridge policy/replay diagnostics.
- Stage A failure.
