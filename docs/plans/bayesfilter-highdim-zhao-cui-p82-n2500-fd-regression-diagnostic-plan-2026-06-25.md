# P82 N2500 FD Regression Diagnostic Plan

Date: 2026-06-25
Status: PLANNED

## Question

Does the P8R FD regression result materially change when the same governed
13-point regression-FD protocol is rerun with `N=2500` particles instead of
`N=1000`?

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are the three FD slopes from the P8R N1000 run stable under an N2500 rerun with the same theta, seeds, offsets, base step, trim rule, XLA/manual-reverse value route, dtype, TF32 mode, transport policy, and Sinkhorn settings? |
| Baseline/comparator | Existing P8R N1000 FD artifact: `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-gpu-tf32-2026-06-24.json`. |
| Primary criterion | N2500 run completes with valid protocol metadata and finite slopes/SEs. For each of `log_kappa_scale`, `log_nu_scale`, and `log_obs_noise_scale`, report N2500 slope, slope SE, N1000 slope, N1000 slope SE, difference, combined SE, and difference / combined SE. |
| Veto diagnostics | GPU not visible; timeout/OOM; missing JSON; wrong theta/seeds/offsets/base step/trim mode/route/dtype/TF32/Sinkhorn metadata; `transport_ad_mode=full`; nonfinite objective/slope/SE; fewer than 13 raw points or 11 retained fit points. |
| Explanatory diagnostics | Runtime, compile timings, memory samples, regression R2, max residual, chunk sizes. |
| Not concluded | This run will not prove FD is an oracle, prove manual gradient correctness or incorrectness, certify posterior validity, or use Zhao-Cui as a comparator. |
| Result artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p82-n2500-fd-regression-diagnostic-result-2026-06-25.md`. |

## Skeptical Plan Audit

- Wrong baseline: avoided by comparing only to the existing P8R N1000 FD
  artifact, not to Zhao-Cui and not to a central-difference shortcut.
- Proxy metric drift: slope stability is a diagnostic only; it is not a
  correctness or scientific-validity claim.
- Hidden assumption: chunk size should not change the scalar, but N2500 will
  use exact `2500 x 2500` transport chunks following the current chunk-sizing
  reset memo. Any result is therefore an N-plus-chunk-policy diagnostic, not a
  pure mathematical chunk-invariance proof.
- Missing stop condition: stop on timeout/OOM, invalid metadata, nonfinite
  regression quantities, or `transport_ad_mode=full`.
- Artifact adequacy: the JSON plus result note are sufficient to answer whether
  the N1000 FD slopes persist at N2500.

Audit status: PASSED_FOR_NARROW_DIAGNOSTIC.

## Planned Command

Run with trusted GPU permissions:

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 14400 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --time-steps 3 --num-particles 2500 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --fd-mode enabled \
  --phase-label "P82 N2500 governed manual-reverse XLA 13-point regression FD GPU TF32 diagnostic" \
  --theta 0.02,-0.01,0.01 \
  --row-chunk-size 2500 --col-chunk-size 2500 --particle-chunk-size 512 \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --base-step-mode fixed \
  --base-step 0.001 \
  --regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6 \
  --trim-extreme-offsets 1 \
  --trim-extreme-mode value \
  --fd-evaluation-mode batched-theta \
  --theta-offset-batch-size 13 \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-n2500-fd-regression-diagnostic-progress-2026-06-25.json \
  --memory-sample-output docs/plans/bayesfilter-highdim-zhao-cui-p82-n2500-fd-regression-diagnostic-memory-samples-2026-06-25.json \
  --memory-sample-interval-seconds 1.0 \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-n2500-fd-regression-diagnostic-2026-06-25.json
```
