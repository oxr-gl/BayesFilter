# P82 FD Contract Hypothesis Test Plan

Date: 2026-06-25

## Objective

Test why the P82 LEDH-PFPF-OT SIR d18 manual reverse gradient agrees with the
diagnostic autodiff route but disagrees with raw regression FD for
`log_kappa_scale` and `log_nu_scale`, while `log_obs_noise_scale` agrees.

## Entry Conditions

- Prior active-all N1000 13-point regression FD artifact exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-gpu-tf32-2026-06-24.json`.
- Prior route decomposition artifact exists:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-manual-score-route-decomposition-n1000-gpu-tf32-2026-06-25.json`.
- Claude bounded micro-review `p82-fd-contract-micro-review-iter1` returned
  `VERDICT: AGREE`: `_manual_forward_transport_tf` freezes transport center,
  scale, and epsilon0, while regression FD evaluates ordinary perturbed-theta
  values.
- Zhao-Cui is not a comparator in this plan.
- Autodiff remains diagnostic-only.
- `transport_ad_mode=full` is forbidden.

## Hypotheses

H1, most likely: active-all raw FD is not estimating the same derivative contract
as manual reverse.  Manual reverse follows the stopped transport branch
contract, while raw FD re-evaluates transport-derived primal quantities at each
perturbed theta.

H2: the mismatch exists before transport, in the coupled SIR LEDH flow and
log-weight correction chain.  This would survive no-resampling.

H3: the mismatch is a value-route/manual-route primal mismatch rather than a VJP
error.  This would show up as a manual-value versus ordinary-value discrepancy
at theta0 under the same transport policy.

H4: the regression FD protocol is producing a misleading slope despite the prior
N1000, N2500, and central FD evidence.  This is lower probability, but remains a
diagnostic caveat, not an oracle claim.

## Evidence Contract

Question: Does the kappa/nu discrepancy persist when active transport is removed
but the same SIR d18 LEDH value/score route, seeds, time horizon, N, XLA manual
reverse, and 13-point FD protocol are used?

Comparator: manual reverse directional gradient versus raw 13-point regression
FD slope under `transport_policy=no-resampling`.

Primary discriminator:

- First verify theta0 primal value consistency: the manual reverse value and the
  ordinary value route must agree under `transport_policy=no-resampling` before
  interpreting derivative residuals.  If theta0 values disagree, H3 is favored
  and the next test is a value-contract audit, not a derivative/VJP audit.
- If theta0 values agree, compare `log_kappa_scale`, `log_nu_scale`, and
  `log_obs_noise_scale` manual-minus-FD residuals against a combined uncertainty
  screen using the FD regression slope standard error and the manual-gradient
  seed MCSE when available.  Treat the screen as passed when
  `abs(residual) <= 2 * sqrt(fd_slope_se^2 + manual_gradient_mcse^2)`.
- If theta0 values agree and all three derivative residuals pass the combined
  two-SE screen, H1 is favored: active transport stopped-branch/raw-FD contract
  mismatch is the first issue.
- If theta0 values agree but kappa/nu remain outside the combined two-SE screen
  under no-resampling, H2 is favored and the next test is a tiny coupled LEDH
  flow/correction audit.

Veto diagnostics:

- nonfinite objective or gradient;
- disconnected manual score route;
- GPU run executed without trusted/escalated context;
- command does not use `transport_policy=no-resampling`;
- command uses `transport_ad_mode=full`;
- output artifact missing regression FD slope standard errors.

Explanatory diagnostics:

- slope residual magnitudes;
- regression residual SSE and max residual;
- MCSE of seed gradients;
- value agreement between manual reverse value and ordinary value at theta0.

Not concluded even if the run passes:

- no proof that active transport gradient is mathematically correct;
- no proof that raw FD is an oracle;
- no posterior correctness, HMC readiness, Zhao-Cui faithfulness, or production
  statistical-validity claim.

## Required Artifacts

- Plan: this file.
- Claude plan review result, if Claude responds.
- No-resampling diagnostic JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-noresampling-fd-contract-diagnostic-2026-06-25.json`.
- Optional progress artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-noresampling-fd-contract-diagnostic-progress-2026-06-25.json`.
- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-fd-contract-hypothesis-test-result-2026-06-25.md`.

## Command

Run with trusted GPU access:

```bash
MPLCONFIGDIR=/tmp /home/chakwong/anaconda3/envs/tf-gpu/bin/python \
  docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --phase-label "P82 no-resampling FD contract discriminator GPU TF32" \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --time-steps 3 \
  --num-particles 1000 \
  --theta 0.02,-0.01,0.01 \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --fd-mode enabled \
  --fd-evaluation-mode batched-theta \
  --theta-offset-batch-size 13 \
  --basis-set raw \
  --base-step 0.001 \
  --regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6 \
  --trim-extreme-offsets 1 \
  --trim-extreme-mode value \
  --transport-policy no-resampling \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --row-chunk-size 500 \
  --col-chunk-size 500 \
  --particle-chunk-size 512 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-noresampling-fd-contract-diagnostic-progress-2026-06-25.json \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-noresampling-fd-contract-diagnostic-2026-06-25.json
```

## Stop Conditions

- Stop after the no-resampling diagnostic and result note.
- Do not patch LEDH VJP from this run alone.
- Do not run `transport_ad_mode=full`.
- If no-resampling passes the two-SE screen, next plan must target
  frozen-branch active-transport FD/JVP rather than primitive LEDH VJP.
- If theta0 manual value and ordinary value disagree under no-resampling, next
  plan must target a value-contract audit before any derivative/VJP audit.
- If theta0 values agree but no-resampling fails the combined two-SE derivative
  screen, next plan must target a tiny coupled LEDH flow/correction audit before
  any broad primitive rewrite.

## Skeptical Plan Audit

- Wrong baseline: guarded by using no-resampling only as a discriminator, not as
  a production comparator.
- Proxy metric risk: guarded; FD agreement/disagreement is diagnostic only.
- Hidden assumption: guarded by recording that raw FD and stopped-branch VJP are
  different contracts under active transport.
- Environment mismatch: guarded by trusted GPU execution and artifact metadata.
- Artifact sufficiency: guarded by requiring slope SE, residuals, finite
  objective/gradient, and exact transport policy metadata.
