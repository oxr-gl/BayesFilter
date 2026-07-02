# Manual Reverse XLA Compile Result

date: 2026-06-24
status: COMPLETE

## Decision Table

| Field | Result |
|---|---|
| Decision | The manual-reverse LEDH-PFPF-OT seed-microbatch value/score route now has an opt-in XLA compiled entry point and passes a small trusted GPU compile smoke. |
| Primary criterion status | PASS: `tf.function(jit_compile=True)` executed the manual-reverse route on GPU and TensorFlow logged XLA cluster compilation. |
| Veto diagnostic status | PASS: smoke used `manual-reverse`, `transport_plan_mode=streaming`, `transport_ad_mode=stabilized`, `manual_streaming_finite_sinkhorn_stopped_scale_keys`, no FD sweep, no Zhao-Cui comparator, no `transport_ad_mode=full`. |
| Main uncertainty | This is not yet an N10000 timing result; it proves compiler feasibility on a small fixed shape. |
| Next justified action | Run a bounded compiled timing ladder before rerunning single-seed N10000: e.g. N100, N1000, then N10000 with warm-call timings and allocator telemetry. |
| Not concluded | FD agreement, HMC readiness, posterior correctness, scientific validity, five-seed N10000 feasibility, or production readiness. |

## What Changed

The regression FD harness now supports an opt-in manual-reverse compiler mode:

- `--manual-reverse-compiler eager`
- `--manual-reverse-compiler tf-function`
- `--manual-reverse-compiler xla`

For compiled modes, the compiled unit is the seed-microbatch manual value/score:

```text
manual_reverse_seed_microbatch_value_score
```

The harness also records compile-and-first-call timings plus optional warm-call timings:

- `--manual-reverse-warmups`
- `--manual-reverse-repeats`

To make the manual score graph-compilable, fixed Zhao-Cui SIR model constants were hoisted out of the compiled body, and the manual process-noise push was made batch-aware for batched transition Cholesky tensors.

## Evidence

Small trusted GPU XLA smoke:

```bash
MPLCONFIGDIR=/tmp /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 1 --num-particles 8 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --manual-reverse-compiler xla --manual-reverse-warmups 1 --manual-reverse-repeats 2 --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "manual reverse XLA GPU warm timing smoke" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 2 --sinkhorn-epsilon 1.0 --row-chunk-size 4 --col-chunk-size 4 --particle-chunk-size 4 --dtype float32 --tf32-mode enabled --basis-set raw --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-manual-reverse-xla-gpu-warm-smoke-2026-06-24.json
```

Observed:

- TensorFlow logged: `Compiled cluster using XLA!`
- Compile plus first call: `22.600756562998868` seconds.
- Warm-call timings: `0.04668212099932134`, `0.04479685401020106` seconds.
- Device: `/GPU:0`.
- TF32: enabled.
- Final status: `pass`.

Artifacts:

- `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-manual-reverse-xla-gpu-smoke-2026-06-24.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-manual-reverse-xla-gpu-warm-smoke-2026-06-24.json`

## Pre-run Audit Outcome

The plan asked only whether the manual-reverse seed-microbatch route could be compiled as the relevant unit. It did not use N10000 wall time, FD agreement, or scientific validity as promotion criteria. The smoke would have been invalid if it changed transport route, used diagnostic autodiff, used `transport_ad_mode=full`, used CPU placement for the GPU gate, or compiled only JSON/reporting code outside the manual score. Those veto conditions did not occur.
