# P82 Visible Stop Handoff

Date: 2026-06-22

Status: P82_CLOSED_WITH_P8R_DIAGNOSTIC_ISSUE_AFTER_P7R_REMEDIATION

## Current State

P82 reached the Zhao-Cui analytical-comparator gate and stopped under the
original scope.  The human owner then removed Zhao-Cui as comparator for now,
so P82 is reopened under an FD-only LEDH same-scalar consistency scope.

## Latest Completed Phase

P3:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase3-zhaocui-analytical-route-result-2026-06-22.md`

## Active Phase

P4-FD-ONLY:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase4-fd-only-ledh-consistency-subplan-2026-06-22.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase4-fd-only-ledh-consistency-result-2026-06-22.md`

## Preserved Corrections

- Zhao-Cui was the original approximate comparator, not an oracle.
- Zhao-Cui is removed from the active P82 pass/fail path for now by human
  amendment.
- LEDH-PFPF-OT is an approximate method, not an oracle.
- Zhao-Cui analytical derivative route was the intended comparator under the
  original P82 scope; this is superseded for now by the FD-only amendment.
- Autodiff/JVP is diagnostic-only unless explicitly reviewed otherwise.
- Two-point central finite difference is not promotion evidence.
- Regression FD uses 13 line points, five seeds, N=1000, value-outlier trim,
  OLS on 11 retained means, and slope SE.
- LEDH actual estimate uses N=10000 and five fixed seeds by default.

## Not Concluded

No gradient validation, no GPU evidence, no posterior correctness, no HMC
readiness, no default-gradient readiness, no scientific superiority, no
manual-adjoint correctness, and no streaming memory improvement.

## Superseded Blocker

`BLOCK_P82_P3_ANALYTICAL_COMPARATOR_ROUTE_NOT_READY`

The current runnable multistate SIR d=18 score path still uses TensorFlow
ForwardAccumulator/JVP for target derivatives.  P12/P15/P16 provide a
fixed-branch same-scalar analytical derivative contract, and `source_route.py`
preserves author SIR fixed-TTSIRT source-route anchors, but P3 did not find an
already-implemented, source-backed analytical multistate comparator route.

This blocker remains valid for the original Zhao-Cui-comparator scope.  It no
longer blocks the amended FD-only LEDH consistency check.

## Active Next Step

P4 FD-only local checks and tiny GPU mechanics smoke passed.  The N=10000
five-seed `transport_ad_mode=full` AD-only gate did not produce an artifact in
the bounded window and was interrupted.

Human correction: the `transport_ad_mode=full` N=10000 route had already been
established as infeasible by the prior P8p Phase 3j runtime blocker, so retrying
it was not a valid next discriminating test.

Active correction:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-full-ad-route-correction-2026-06-22.md`

Do not launch the full N=1000 regression-FD comparison until the actual-gradient
side is supplied by a reviewed memory-disciplined route.  The next active plan
is the LEDH-PFPF-OT manual-adjoint/custom-gradient program:

- `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-master-program-2026-06-22.md`

The manual-adjoint program has produced a local route and P5 has now wired the
manual streaming transport-gradient mode through the P82 benchmark path.  P5
local CPU-hidden checks passed and one-path Claude review returned
`VERDICT: AGREE`.  No P82 validation has resumed.

P5 artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase5-manual-streaming-gradient-wiring-subplan-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase5-manual-streaming-gradient-wiring-result-2026-06-23.md`

P5 local checks:

- `py_compile`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q`:
  `10 passed, 2 warnings in 6.91s` on the post-crash rerun.
- `git diff --check`: passed.
- One-path Claude review: `VERDICT: AGREE`.

P6 artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-subplan-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-result-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-2026-06-23.json`

P6 status:

- local checks passed;
- trusted GPU preflight passed;
- tiny GPU smoke exited 0 with route metadata
  `transport_plan_mode=streaming`,
  `gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`,
  `transport_ad_mode=stabilized`, and `regression_fd.fd_mode=ad-only`;
- one-path Claude execution review returned `VERDICT: AGREE`.

P7 artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n1000-gpu-tf32-2026-06-23.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-result-2026-06-23.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase9-closeout-result-2026-06-23.md`

P7 status:

- N1000 feasibility rung passed with five seeds and finite GPU-visible
  gradients/MCSE.
- N10000 rung failed with TensorFlow `ResourceExhaustedError: failed to
  allocate memory`.
- No N10000 output JSON or progress JSON exists.

Closeout:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase9-closeout-result-2026-06-23.md`
- Claude R2 review returned `VERDICT: AGREE`.

## 2026-06-24 Resume / Final State

The old P7 memory blocker was remediated by a reviewed P7R subplan using the
manual-reverse XLA route and the N10000 chunk-sizing rule (`2500 x 2500`).

P7R artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-xla-chunk2500-actual-gradient-remediation-subplan-2026-06-24.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-xla-chunk2500-actual-gradient-remediation-result-2026-06-24.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-gpu-tf32-2026-06-24.json`

P7R status:

- Passed.
- Produced a valid five-seed N10000 actual-gradient artifact.
- Used `ad_evaluation_mode=manual-reverse`, `compiler.mode=xla`,
  `transport_plan_mode=streaming`,
  `gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`,
  `transport_ad_mode=stabilized`, and chunks `2500/2500/512`.
- Did not run FD and did not claim FD agreement.

P8R artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-consistency-subplan-2026-06-24.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-consistency-result-2026-06-24.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-gpu-tf32-2026-06-24.json`

P8R status:

- Governed FD protocol ran successfully.
- Same-scalar metadata check against P7R passed.
- FD protocol metadata passed: 13 raw points, value trimming, 11 fit points,
  five seeds, N1000, GPU-visible output, and `fd_mode=enabled`.
- FD consistency did not pass: `log_kappa_scale` and `log_nu_scale` exceeded
  the 2 combined-SE triage threshold; `log_obs_noise_scale` was within 2
  combined SE.

P9R closeout:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase9r-closeout-result-2026-06-24.md`

Current final state:

- Stop.  P82 is closed with a P8R diagnostic issue, not a validation pass.
- The active blocker is no longer N10000 memory.  The blocker is
  rate-parameter FD disagreement.
- Further GPU experiments require a new reviewed remediation plan focused on
  the kappa/nu mismatch.
