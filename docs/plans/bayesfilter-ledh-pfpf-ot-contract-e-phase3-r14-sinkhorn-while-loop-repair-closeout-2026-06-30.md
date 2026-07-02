# Phase R14 Closeout: Manual Dense Sinkhorn `tf.while_loop` Repair

Date: 2026-06-30

Status: `ENGINEERING_REPAIR_PASS__KALMAN_GATE_STILL_FAILS`

## Decision Table

| Decision | Primary criterion status | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Keep the `tf.while_loop` Sinkhorn repair; do not claim LGSSM gradient correctness yet. | Static audit and targeted primitive/manual-route tests pass. GPU/XLA/TF32 `steps20` and `steps50` run complete after repair. | GPU route valid; XLA true; TF32 true; manual score route true; finite values/scores; covariance/conditioning/ridge diagnostics clean. Kalman `2*MCSE` score gate still fails. | Remaining failure may be finite-N finite-seed bias, a score estimator bias, or a parameter-specific VJP/score convention issue; pure Sinkhorn nonconvergence is no longer sufficient. | Run the next discriminating phase: increase `N`/seed evidence or isolate same-particle manual score against finite differences after converged row residual. | No production budget promotion; no SIR/SV correctness; no HMC readiness; no proof that `steps50` is globally adequate. |

## What Changed

- Replaced Python-unrolled Sinkhorn loops in
  `_filterflow_manual_dense_finite_sinkhorn_outputs` with `tf.while_loop`.
- Replaced the VJP forward replay and reverse replay loops in
  `_filterflow_manual_dense_finite_sinkhorn_vjp` with TensorArray-backed
  `tf.while_loop` recursions.
- Added a static route guard requiring those two helpers to contain
  `tf.while_loop` and not contain `range(steps)`.
- Added bounded R14 GPU runner scripts for `steps2/8/20` and `steps50`.

## Local Checks

The static route audit is only a wiring guard.  The semantic preservation claim
comes from the primitive/manual-route tests below, especially the dense
manual-adjoint oracle coverage.

Passed:

```bash
python -m py_compile \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py
python -m pytest \
  tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py \
  tests/test_contract_e_phase3_gradient_route_audit.py \
  tests/test_contract_e_cholesky_ridge_reset.py \
  -q
```

Result: `41 passed`.

Also passed:

```bash
git diff --check -- \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py \
  tests/test_contract_e_phase3_gradient_route_audit.py \
  scripts/run_contract_e_r14_gpu_sinkhorn_while_loop_ladder.sh \
  scripts/run_contract_e_r14_gpu_sinkhorn_while_loop_steps50.sh \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r13-gpu-xla-sinkhorn-budget-ladder-blocker-2026-06-30.md \
  docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r14-sinkhorn-while-loop-repair-plan-2026-06-30.md
```

## GPU Evidence

Route:

- visible GPU: yes;
- XLA: true;
- TF32 execution: true;
- score route: `manual-reverse-scan`;
- reset: Contract E Cholesky-ridge;
- `N=1000`, `T=10`, `seed_count=10`.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r14-gpu-xla-tf32-sinkhorn-while-loop-ladder-2026-06-30.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r14-gpu-xla-tf32-sinkhorn-while-loop-ladder-result-2026-06-30.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r14-gpu-xla-tf32-sinkhorn-while-loop-steps50-2026-06-30.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r14-gpu-xla-tf32-sinkhorn-while-loop-steps50-result-2026-06-30.md`

Trend:

| dim | steps | row residual | value z | gradient z values | gate |
| ---: | ---: | ---: | ---: | --- | --- |
| 2 | 2 | `0.956566` | `-2.053` | `[-3.768, -1.973, -3.052]` | fail |
| 2 | 8 | `0.946542` | `-2.054` | `[-3.748, -2.023, -3.139]` | fail |
| 2 | 20 | `0.143895` | `-1.273` | `[-0.717, 1.049, 2.533]` | fail |
| 2 | 50 | `7.87e-05` | `-1.216` | `[-0.517, 1.201, 2.930]` | fail |
| 1 | 2 | `0.995968` | `-1.466` | `[-4.547, 0.588, -3.859]` | fail |
| 1 | 8 | `0.994946` | `-1.599` | `[-5.054, 0.194, -4.354]` | fail |
| 1 | 20 | `0.624706` | `-0.679` | `[-4.327, -0.009, -2.466]` | fail |
| 1 | 50 | `0.010923` | `1.608` | `[2.115, 4.142, 4.339]` | fail |

## Interpretation

R14 fixed the R13 execution blocker.  The `steps20` ladder completed in about
73 seconds, and the separate `steps50` rung completed in about 30 seconds.  The
previous giant-graph compile problem is therefore not the current blocker after
the `tf.while_loop` repair.

The numerical evidence weakens the hypothesis that the remaining LGSSM gradient
failure is simply unresolved Sinkhorn marginal error.  Row residuals decrease
substantially with more Sinkhorn steps and are tiny for D=2 at `steps50`, but
the Kalman gradient gate still fails.  D=1 is especially informative: increasing
budget moves the score past the Kalman reference for some parameters, producing
positive z-scores above the `2*MCSE` gate at `steps50`.

The next target should not be another blind Sinkhorn-budget increase.  The next
discriminating test should separate finite-N/seed bias from a score/VJP
implementation or convention error.  The smallest useful follow-up is either:

1. rerun the converged-budget fixture with larger `N` and/or more seeds on the
   same GPU/XLA/TF32/manual route; or
2. isolate the same scalar objective at `steps50` and compare the manual
   reverse score to finite differences for D=1 and D=2 on fixed random numbers.

## Claude Review

Claude reviewed the R14 plan before implementation and returned
`VERDICT: AGREE`, with the caution that a helper-specific static guard should
be made explicit.  That guard was added.

A second read-only Claude patch/result review returned `VERDICT: AGREE`.  It
confirmed that the TensorArray VJP replay stores pre-update states and that the
GPU artifacts support the limited claim "compile blocker fixed, Kalman gradient
gate still fails."  It also cautioned that the static audit is a wiring guard,
not the semantic proof; this closeout records the primitive/manual-route tests
as the semantic evidence.
