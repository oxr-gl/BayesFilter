# P82 Phase 8R Subplan: Governed FD Consistency

status: READY_FOR_CLAUDE_REVIEW
date: 2026-06-24
phase: P8R-GOVERNED-FD-CONSISTENCY

## Phase Objective

Run the governed N1000 five-seed 13-point regression-FD comparison for the same
LEDH scalar and compare the raw-direction FD slopes against the P7R N10000
actual-gradient artifact.

## Entry Conditions Inherited From Previous Phase

- P7R passed and produced:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7r-actual-gradient-n10000-xla-chunk2500-gpu-tf32-2026-06-24.json`
- The P7R artifact records five fixed seeds, N10000, `manual-reverse`,
  `compiler.mode=xla`, `transport_plan_mode=streaming`,
  `transport_ad_mode=stabilized`, finite actual-gradient components, and finite
  seed MCSE.
- Before P8R interpretation, the P7R artifact must be explicitly checked
  against the P8R command for the same LEDH scalar contract:
  - theta equals `0.02,-0.01,0.01`;
  - transport policy is `active-all`;
  - transport plan mode is `streaming`;
  - transport gradient mode is
    `manual_streaming_finite_sinkhorn_stopped_scale_keys`;
  - transport AD mode is `stabilized`;
  - Sinkhorn settings are `iterations=10`, `epsilon=1.0`;
  - dtype is `float32` and TF32 is enabled.
- Zhao-Cui remains out of the comparator path.
- FD is diagnostic evidence, not an oracle.
- `transport_ad_mode=full` remains forbidden.

## Required Artifacts

- Governed FD JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-gpu-tf32-2026-06-24.json`
- Governed FD progress JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-progress-2026-06-24.json`
- Governed FD memory sidecar:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-memory-samples-2026-06-24.json`
- Phase 8R result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-consistency-result-2026-06-24.md`
- Updated P82 visible stop handoff.

## Required Checks / Tests / Reviews

Before GPU work:

```bash
CUDA_VISIBLE_DEVICES=-1 /home/chakwong/anaconda3/envs/tf-gpu/bin/python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
CUDA_VISIBLE_DEVICES=-1 /home/chakwong/anaconda3/envs/tf-gpu/bin/python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-*.md
```

Trusted/escalated GPU preflight:

```bash
nvidia-smi
MPLCONFIGDIR=/tmp /home/chakwong/anaconda3/envs/tf-gpu/bin/python -c "import tensorflow as tf; print(tf.__version__); print(tf.config.list_physical_devices()); print(tf.config.list_physical_devices('GPU'))"
```

Claude review:

- Use one exact path only: this subplan.
- Do not paste code or artifact packets.
- Ask whether the subplan safely performs P8R FD consistency against the P7R
  artifact without treating FD as an oracle or reopening forbidden routes.

## Governed FD Command

The FD run uses `N=1000`, five seeds, 13 offsets, batched theta-row value
evaluation, value-outlier trimming of one low and one high mean objective, and
OLS on the remaining 11 points.

Run with trusted GPU permissions:

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 7200 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 1000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --manual-reverse-warmups 0 \
  --manual-reverse-repeats 1 \
  --fd-mode enabled \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 Phase 8R governed manual-reverse XLA N1000 13-point regression FD GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 500 --col-chunk-size 500 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --base-step-mode fixed \
  --base-step 0.001 \
  --regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6 \
  --trim-extreme-offsets 1 \
  --trim-extreme-mode value \
  --fd-evaluation-mode batched-theta \
  --theta-offset-batch-size 13 \
  --basis-set raw \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-progress-2026-06-24.json \
  --memory-sample-output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-memory-samples-2026-06-24.json \
  --memory-sample-interval-seconds 30 \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8r-governed-fd-n1000-xla-chunk500-gpu-tf32-2026-06-24.json
```

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are the P7R N10000 actual-gradient components consistent with P8R N1000 13-point regression-FD slopes for the same LEDH scalar in raw theta directions? |
| Comparator | Same-scalar LEDH regression FD with 13 offsets, five seeds, N1000, value trimming of one low and one high mean objective point, and OLS on 11 retained points. FD is noisy diagnostic evidence, not an oracle. |
| Primary criterion | P7R comparator artifact matches the P8R same-scalar contract for theta, transport policy, transport route, Sinkhorn settings, dtype, and TF32 mode; P8R output metadata records `fd_mode=enabled`, `ad_evaluation_mode=manual-reverse`, `compiler.mode=xla`, `transport_plan_mode=streaming`, `gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, five seeds, N1000, 13 raw points, 11 fit points, and `trim_mode=value`; for every raw theta direction, P7R actual gradient, P7R seed MCSE, FD slope, FD slope SE, and combined SE are finite; each absolute combined-SE ratio is <= 2, or the row is explicitly downgraded for investigation rather than promoted. |
| Veto diagnostics | P7R/P8R theta, transport policy, transport route, Sinkhorn setting, dtype, or TF32 mismatch; wrong route metadata; `regression_fd.fd_mode` not explicitly enabled; wrong seed/particle counts; missing 13 raw points; missing 11 fit points; trim mode not `value`; nonfinite objective/gradient/slope/SE; timeout/OOM; GPU not visible; `transport_ad_mode=full`; Zhao-Cui comparator use; central-difference-only promotion; unsupported HMC/default/scientific-superiority claim. |
| Explanatory diagnostics | Regression R2, max residual, dropped value-extreme points, P8R internal N1000 AD-vs-FD residuals, runtime, chunks, compiler timings, TF32/device metadata, and TensorFlow allocator telemetry. |
| Not concluded | Exact correctness, posterior validity, HMC readiness, production readiness, scientific superiority, or calibrated hypothesis-test validity. |

## Forbidden Claims / Actions

- Do not use Zhao-Cui as comparator evidence.
- Do not treat FD as an oracle.
- Do not claim correctness from a row passing the 2 combined-SE triage rule.
- Do not use `transport_ad_mode=full`.
- Do not change theta, seeds, Sinkhorn settings, offsets, trim mode, or
  thresholds inside this phase.

## Exact Next-Phase Handoff Conditions

P9R closeout may start after P8R writes either a pass result or a clearly scoped
issue/blocker result.  P9R must preserve any rows exceeding 2 combined SE as
diagnostic issues rather than hiding them.

## Stop Conditions

Stop and write a blocker if local checks fail, Claude review returns
`VERDICT: REVISE` with an unresolved material issue, trusted GPU preflight
fails, the governed FD command fails/times out/OOMs, or output metadata violates
the protocol.

## End-Of-Phase Protocol

1. Run required local checks.
2. Run trusted GPU preflight.
3. Run the governed FD command.
4. Validate the JSON protocol.
5. Validate the P7R/P8R same-scalar metadata match.
6. Compare raw-direction FD slopes against the P7R actual-gradient artifact.
7. Write the P8R result.
8. Update the visible stop handoff.
