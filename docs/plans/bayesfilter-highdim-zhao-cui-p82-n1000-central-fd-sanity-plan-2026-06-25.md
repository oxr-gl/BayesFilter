# P82 N1000 Central FD Sanity Plan

Date: 2026-06-25
Status: PLANNED

## Question

For the exact P8R N1000 scalar route, do simple central FD slopes in the three
raw theta directions look closer to the stored manual/reverse-gradient
gradients or to the existing 13-point regression-FD slopes?

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Run an explanatory central FD sanity check for `log_kappa_scale`, `log_nu_scale`, and `log_obs_noise_scale` at N1000. |
| Baselines | Existing P8R manual-reverse N1000 gradient and existing P8R N1000 13-point regression-FD artifact. The older N1000 `reverse-gradient` diagnostic is reported as a diagnostic comparator only. |
| Primary output | For each raw theta direction, report central FD slope from offsets `-1,0,+1` with base step `0.001`, extracted from an accepted 7-point offset run, and compare against manual gradient, reverse-gradient diagnostic, and 13-point regression FD. |
| Veto diagnostics | GPU not visible, timeout/OOM, wrong theta/seeds/N/route/Sinkhorn/dtype/TF32 metadata, nonfinite values, missing plus/minus points, `transport_ad_mode=full`, or treating central FD as validation. |
| Explanatory diagnostics | Runtime, memory, central FD objective values, difference from manual gradient, difference from regression FD. |
| Not concluded | Central FD will not supersede the 13-point regression estimate, prove FD is an oracle, prove manual gradient wrong, certify posterior correctness, or use Zhao-Cui as a comparator. |
| Result artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p82-n1000-central-fd-sanity-result-2026-06-25.md`. |

## Skeptical Plan Audit

- Wrong baseline risk: avoided by comparing central FD to both manual/reverse
  gradients and the stronger regression-FD estimate.
- Proxy-promotion risk: central FD is noisy and explanatory only.
- Missing stop condition: stop on GPU placement failure, timeout/OOM, invalid
  metadata, missing raw theta rows, or nonfinite values.
- Hidden route drift: use the same N1000 theta, seeds, transport settings,
  Sinkhorn settings, dtype, TF32, value-trim mode, and raw-theta basis. Use
  accepted offsets `-3..3` because the harness rejects a 3-point offset list,
  but extract the central sanity slope only from the `-1,0,+1` points.
- Artifact adequacy: final JSON plus result note is enough for this sanity
  question.

Audit status: PASSED_FOR_EXPLANATORY_SANITY_CHECK.

## Planned Command

Run with trusted GPU permissions:

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 7200 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 1000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --fd-mode enabled \
  --basis-set raw \
  --phase-label "P82 N1000 central FD sanity raw theta GPU TF32" \
  --theta 0.02,-0.01,0.01 \
  --row-chunk-size 500 --col-chunk-size 500 --particle-chunk-size 512 \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --base-step-mode fixed \
  --base-step 0.001 \
  --regression-offsets=-3,-2,-1,0,1,2,3 \
  --trim-extreme-offsets 0 \
  --trim-extreme-mode value \
  --fd-evaluation-mode batched-theta \
  --theta-offset-batch-size 3 \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-n1000-central-fd-sanity-progress-2026-06-25.json \
  --memory-sample-output docs/plans/bayesfilter-highdim-zhao-cui-p82-n1000-central-fd-sanity-memory-samples-2026-06-25.json \
  --memory-sample-interval-seconds 1.0 \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-n1000-central-fd-sanity-2026-06-25.json
```
