# Manual Reverse XLA Default Result

date: 2026-06-24
status: COMPLETE

## Decision Table

| Field | Result |
|---|---|
| Decision | The P8p regression harness now defaults the `manual-reverse` seed-microbatch value/score route to XLA compilation. |
| Primary criterion status | PASS: a trusted GPU smoke omitted `--manual-reverse-compiler` and produced `compiler.mode=xla`, `jit_compile=true`, finite objective, finite score, and GPU output devices. |
| Veto diagnostic status | PASS: no FD, no diagnostic autodiff route, no `transport_ad_mode=full`, and no CPU placement. |
| Main uncertainty | This changes the harness default, not every BayesFilter algorithm entry point. |
| Next justified action | Future manual-reverse GPU timing/gradient diagnostics should omit the compiler flag or explicitly keep `xla`; use `--manual-reverse-compiler eager` only for scoped debugging. |
| Not concluded | FD agreement, HMC readiness, posterior correctness, five-seed feasibility, scientific validity, or production readiness. |

## Default Change

`docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py` now defaults:

```text
--manual-reverse-compiler xla
```

This is scoped to the `manual-reverse` seed-microbatch value/score route. It does not make the diagnostic autodiff modes default, and it does not make `transport_ad_mode=full` valid.

The override remains available:

```text
--manual-reverse-compiler eager
--manual-reverse-compiler tf-function
```

Those overrides should be treated as debugging routes because non-XLA manual-reverse was measured as misleadingly slow for N10000.

## Evidence

Trusted GPU smoke command intentionally omitted `--manual-reverse-compiler`:

```bash
MPLCONFIGDIR=/tmp /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 1 --num-particles 8 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --manual-reverse-warmups 0 --manual-reverse-repeats 1 --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "manual reverse default XLA GPU smoke" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 2 --sinkhorn-epsilon 1.0 --row-chunk-size 4 --col-chunk-size 4 --particle-chunk-size 4 --dtype float32 --tf32-mode enabled --basis-set raw --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-manual-reverse-default-xla-gpu-smoke-2026-06-24.json
```

Observed:

- TensorFlow logged XLA cluster compilation.
- `compiler.mode`: `xla`.
- `compiler.jit_compile`: `true`.
- Compile plus first call: `21.54825826799788` seconds.
- Warm call: `0.08603397299884818` seconds.
- Status: `pass`.
- Primary pass: `true`.

Artifact:

- `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-manual-reverse-default-xla-gpu-smoke-2026-06-24.json`
