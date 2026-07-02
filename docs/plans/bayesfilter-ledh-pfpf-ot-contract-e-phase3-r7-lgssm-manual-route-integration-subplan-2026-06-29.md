# Phase R7 Subplan: LGSSM Manual Route Integration Handoff

Date: 2026-06-29

Status: `DRAFT_EXECUTION_PLAN_ITER2`

## Phase Objective

Wire the Contract E fixed-ridge manual reverse-scan route into the smallest
LGSSM diagnostic path that shares primitives with Phase 3, while preserving the
material blocker.  R7 is an integration and same-scalar route-validation gate;
a pass nominates the next material-script wiring phase only.

## Entry Conditions Inherited From R6

- R5 one-step local Contract E VJP composition passed same-scalar central
  finite-difference parity.
- R6 two-step fixed-branch time reverse scan passed same-scalar central
  finite-difference parity with frozen replayed charts.
- Static audits cover the local fixed-ridge reset VJP and manual finite
  stopped-scale/key transport helper family for hidden generic autodiff,
  `tf.linalg.eigh`, and `transport_ad_mode="full"`.
- The material blocker remains active:
  `PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN`.

## Required Artifacts

- Executable R7 subplan reviewed with Claude before implementation.
- A route inventory of
  `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`,
  identifying the exact forward state that must be recorded for manual reverse
  scan: particles, corrected log weights, residual noises, replayed charts,
  transport matrices, reset diagnostics, ridge selections, reset/escalation
  branch decisions, frozen seeds/noise draws, and model-specific LGSSM VJP
  auxiliaries.
- An explicit fixed-ridge smooth-chart policy for the first integrated manual
  route.  The branchy ridge-escalation reset may remain as a diagnostic/value
  route, but it must not be silently used as the same-scalar FD comparator for
  a fixed-ridge manual VJP.
- A distinct fixed-ridge route label/config/assertion, expected label:
  `contract_e_cholesky_fixed_ridge_manual_lgssm_tiny`.
- A smallest integrated LGSSM manual score route initially scoped to:
  `state_dim=1`, `time_steps=2`, `num_particles=4`, `batch_size=1`,
  `dtype=tf.float64`, CPU-hidden, deterministic initial particles,
  transition noises, residual noises, and observations.
- Same-scalar central-FD parity for the three LGSSM parameters on the tiny
  fixture with step `1.0e-5`, target `rtol=5.0e-4`, `atol=1.0e-5`, and
  fail-closed branch replay checks.
- Static audit proving the material route is no longer using outer
  `tf.GradientTape` if a later phase proposes blocker replacement.
- R7 result / close record and a fresh R8 handoff.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before implementation.
- Bounded Claude read-only plan review before edits.
- Focused CPU-hidden same-scalar FD tests for the integrated LGSSM route.
- Existing R5/R6/reset/blocker route audits.
- `py_compile` for touched Python.
- `git diff --check` for touched paths.
- Bounded Claude implementation/result review before any blocker change.

Exact local checks for R7:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest \
  tests/test_contract_e_phase3_r7_lgssm_manual_route.py \
  tests/test_contract_e_phase3_r6_tiny_time_loop_reverse_scan.py \
  tests/test_contract_e_phase3_r5_manual_reverse_integration.py \
  tests/test_contract_e_cholesky_ridge_reset.py \
  tests/test_contract_e_phase3_gradient_route_audit.py -q
python -m py_compile \
  tests/test_contract_e_phase3_r7_lgssm_manual_route.py \
  docs/benchmarks/contract_e_reset_tf.py \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py
git diff --check -- \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r7-lgssm-manual-route-integration-subplan-2026-06-29.md \
  tests/test_contract_e_phase3_r7_lgssm_manual_route.py
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the Contract E manual reverse-scan route be wired into a tiny LGSSM score route without generic autodiff and with same-scalar FD parity? |
| Baseline/comparator | Central finite differences of the exact same fixed-ridge LGSSM scalar under frozen seeds/noise, replayed charts, fixed ridge, and fixed branch records; later exact Kalman gradient only after same-scalar FD passes. |
| Primary pass criterion | Integrated manual score matches same-scalar FD for all three LGSSM parameters on the scoped tiny fixture with `rtol=5.0e-4`, `atol=1.0e-5`. |
| Veto diagnostics | Hidden outer tape in the integrated score path, missing forward replay state, branch changes, nonfinite values/cotangents, missing reset/transport diagnostics, missing blocker while the material script still has outer tape, stale route labels, or any fallback from fixed-ridge route to branchy ridge escalation. |
| Explanatory diagnostics | Per-time cotangent norms, incremental log-likelihood components, reset covariance residuals, ridge diagnostics, Sinkhorn residuals, and Kalman value/gradient deltas. |
| Not concluded | Material Phase 3 correctness, broad LGSSM correctness, nonlinear SIR/SV correctness, HMC readiness, production readiness, or GPU/XLA/TF32 readiness. |
| Artifact preserving result | R7 result note plus focused test/diagnostic output. |

## Forbidden Claims And Actions

- Do not remove the material blocker until a reviewed route proves that the
  material score no longer uses the outer `tf.GradientTape` path and passes
  same-scalar FD.
- A tiny R7 integrated diagnostic pass may only nominate R8 material-script
  integration.  It must not replace the blocker by itself.
- Do not use exact Kalman agreement as a substitute for same-scalar FD route
  validation.
- Do not compare a fixed-ridge manual VJP against a finite-difference scalar
  that reruns branchy ridge escalation or changes ridge selection.
- Do not run full Phase 3, SIR/SV, GPU, or XLA jobs unless a reviewed R7 plan
  explicitly authorizes that scope.
- Do not claim production readiness or scientific validity from a tiny
  integration fixture.

## Exact Next-Phase Handoff Conditions

Advance beyond R7 only if:

- the executable R7 subplan converges under review;
- the integrated route inventory identifies all required forward and reverse
  state;
- the fixed-ridge forward scalar and manual VJP use the same ridge values and
  replayed charts;
- same-scalar FD parity passes on the scoped LGSSM fixture;
- route audits show no hidden generic autodiff in the R7 integrated score path;
- focused local checks pass;
- Claude implementation/result review converges; and
- the material Phase 3 blocker remains active unless R8 or later proves the
  verified route is the actual material Phase 3 score path or a shared
  implementation used by it, and a no-outer-tape audit passes.

## Stop Conditions

Stop and write an R7 blocker result if:

- required LGSSM forward state cannot be replayed without changing the scalar;
- the branchy ridge-escalation scalar cannot be separated from the fixed-ridge
  smooth-chart manual VJP;
- the integrated route requires generic autodiff to pass;
- same-scalar FD parity fails after one focused repair attempt;
- branch replay changes appear;
- the blocker would need to be removed without material route evidence; or
- Claude review does not converge after five rounds for the same blocker.

## Skeptical Plan Audit

- Wrong-baseline risk: FD could accidentally evaluate branchy
  `contract_e_cholesky_ridge_reset` while the manual VJP evaluates
  `contract_e_cholesky_ridge_reset_fixed_ridge`.  Mitigation: the R7 fixture
  must expose and assert the route label
  `contract_e_cholesky_fixed_ridge_manual_lgssm_tiny`, call the fixed-ridge
  forward helper for both manual and FD scalars, and keep branchy escalation
  only as an optional diagnostic record.
- Proxy-promotion risk: a tiny LGSSM parity pass could be overread as Phase 3
  material evidence.  Mitigation: R7 explicitly preserves the material blocker
  and only hands off to R8.
- Hidden-autodiff risk: reusing the Phase 3 script could accidentally retain
  `_make_compiled_value_and_gradient` and its outer tape.  Mitigation: static
  audits must target the integrated R7 score helper and keep the existing
  blocker audit active.
- Environment risk: R7 is CPU-hidden and tiny; no GPU/XLA/TF32 claims are
  permitted.
- Artifact adequacy: the planned test and result note answer the R7 question by
  preserving same-scalar FD parity, deterministic fixture details, branch
  replay diagnostics, and route-label evidence.

This revised plan is executable because it fixes the tiny fixture scope,
commands, tolerances, route label, and blocker handoff rule before any code is
changed.
