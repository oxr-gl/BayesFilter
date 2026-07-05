# P82 Phase 8 Subplan: Governed FD Consistency

status: REVIEWED_CLAUDE_R4_AGREE_WAITING_FOR_P7
date: 2026-06-23
phase: P8-GOVERNED-FD-CONSISTENCY

## Phase Objective

Run the governed N1000 five-seed 13-point regression-FD comparison for the same
LEDH scalar and compare the raw-direction FD slopes against the P7 N10000
actual-gradient artifact.

## Entry Conditions

- P7 passed and produced:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-gpu-tf32-2026-06-23.json`
- The P7 artifact records five fixed seeds, N10000, manual streaming gradient
  mode, `transport_plan_mode=streaming`, `transport_ad_mode=stabilized`,
  finite actual-gradient components, and finite seed MCSE.
- Zhao-Cui remains out of the comparator path.

## Required Artifacts

- Governed FD JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-governed-fd-n1000-gpu-tf32-2026-06-23.json`
- Governed FD progress JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-governed-fd-n1000-progress-2026-06-23.json`
- Phase 8 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-governed-fd-consistency-result-2026-06-23.md`
- Updated P82 execution ledger, Claude review ledger if P8 is reviewed, and
  stop handoff.

## Required Checks / Tests / Reviews

Before GPU work:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-*.md
```

Trusted/escalated GPU preflight:

```bash
nvidia-smi
MPLCONFIGDIR=/tmp python -c "import tensorflow as tf; print(tf.__version__); print(tf.config.list_physical_devices()); print(tf.config.list_physical_devices('GPU'))"
```

Governed FD command:

```bash
MPLCONFIGDIR=/tmp timeout 7200 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 1000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode reverse-gradient \
  --fd-mode enabled \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 Phase 8 governed manual streaming N1000 13-point regression FD GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --base-step-mode fixed \
  --base-step 0.001 \
  --regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6 \
  --trim-extreme-offsets 1 \
  --trim-extreme-mode value \
  --fd-evaluation-mode batched-theta \
  --theta-offset-batch-size 13 \
  --basis-set raw \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-governed-fd-n1000-progress-2026-06-23.json \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-governed-fd-n1000-gpu-tf32-2026-06-23.json
```

After the command, compute a comparison table in the result markdown:

- P7 N10000 actual-gradient component;
- P7 seed-MCSE for that component;
- P8 FD slope;
- P8 FD slope SE;
- difference and `difference / sqrt(actual_mcse^2 + slope_se^2)`.

The combined-SE ratio is a triage diagnostic only.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are the P7 N10000 actual-gradient components consistent with P8 N1000 13-point regression-FD slopes for the same LEDH scalar in raw theta directions? |
| Comparator | Same-scalar LEDH regression FD with 13 offsets, five seeds, N1000, value trimming of one low and one high mean objective point, and OLS on 11 retained points. |
| Primary criterion | Output metadata records `transport_plan_mode=streaming`, `gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, and `regression_fd.fd_mode=enabled`; for every raw theta direction, actual gradient, FD slope, actual MCSE, FD slope SE, and combined SE are finite; each absolute combined-SE ratio is <= 2, or the row is explicitly downgraded for investigation rather than promoted. |
| Veto diagnostics | Wrong route metadata; `regression_fd.fd_mode` not explicitly enabled; wrong seed/particle counts; missing 13 raw points; missing 11 fit points; trim mode not `value`; nonfinite objective/gradient/slope/SE; timeout/OOM; GPU not visible; `transport_ad_mode=full`; Zhao-Cui comparator use; central-difference-only promotion; unsupported HMC/default/scientific-superiority claim. |
| Explanatory diagnostics | Regression R2, max residual, dropped value-extreme points, P8 internal N1000 AD-vs-FD residuals, runtime, chunks, TF32/device metadata. |
| Not concluded | Exact correctness, posterior validity, HMC readiness, production readiness, scientific superiority, or calibrated hypothesis-test validity. |

## Stop Conditions

Stop and write a blocker if the governed FD command fails, times out, OOMs, or
emits invalid protocol metadata.  If any row exceeds 2 combined SE, write an
issue result rather than claiming validation.

## Next-Phase Handoff Conditions

P9 closeout may start after P8 writes either a pass result or a clearly scoped
issue/blocker result.
