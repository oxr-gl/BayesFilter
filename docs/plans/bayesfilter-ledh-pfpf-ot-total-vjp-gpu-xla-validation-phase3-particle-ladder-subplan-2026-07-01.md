# Phase 3 Subplan: Material Particle Ladder

Date: 2026-07-01

Status: `READY_FOR_CLAUDE_REVIEW`

## Phase Objective

Measure whether the corrected full total-derivative route remains GPU/XLA
viable as particle count increases.

## Entry Conditions Inherited From Previous Phase

- Phase 1 tiny GPU/XLA full-route smoke passed.
- Phase 2 was skipped because no harness repair was needed.
- Phase 0 static dispatch proof remains binding: the legacy gradient-mode
  selector paired with `transport_ad_mode="full"` reaches
  `_filterflow_manual_streaming_finite_transport_total_vjp`.

## Required Artifacts

- Phase 3 rung JSON files under
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-*.json`.
- Phase 3 memory sample JSON files for rungs above `N=16`.
- Phase 3 result markdown:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-particle-ladder-result-2026-07-01.md`.
- Updated Phase 4 subplan if ladder passes.

## Required Checks, Tests, Reviews

Candidate rungs:

- `N=16`, `T=1`, seeds `81120,81121`;
- `N=64`, `T=3`, seeds `81120,81121,81122,81123,81124`;
- `N=256`, `T=3`, same seeds if N=64 passes;
- `N=1000`, `T=3`, same seeds only if memory/runtime is sane.

Each rung must use:

- GPU visible trusted execution;
- float32, TF32 enabled;
- manual-reverse XLA;
- streaming transport;
- `transport_ad_mode="full"`.

Phase 3 skeptical audit before execution:

- The stopped partial derivative is not a baseline.
- Phase 3 tests GPU/XLA viability and scaling only; it does not test HMC
  direction quality.
- Advancement from one rung to the next depends on the previous rung passing
  the exact JSON gate below.
- The `N=1000` rung is conditional, not mandatory; do not run it if earlier
  memory/runtime indicates likely OOM or an unreasonable overnight stall.

Exact rung commands:

```bash
python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --fd-mode ad-only \
  --batch-seeds 81120,81121 \
  --time-steps 1 \
  --num-particles 16 \
  --theta 0.02,-0.01,0.01 \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode full \
  --row-chunk-size 16 \
  --col-chunk-size 16 \
  --particle-chunk-size 16 \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n16-t1-2026-07-01.json
```

```bash
python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --fd-mode ad-only \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --time-steps 3 \
  --num-particles 64 \
  --theta 0.02,-0.01,0.01 \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode full \
  --row-chunk-size 32 \
  --col-chunk-size 32 \
  --particle-chunk-size 32 \
  --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n64-t3-memory-2026-07-01.json \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n64-t3-2026-07-01.json
```

```bash
python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --fd-mode ad-only \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --time-steps 3 \
  --num-particles 256 \
  --theta 0.02,-0.01,0.01 \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode full \
  --row-chunk-size 64 \
  --col-chunk-size 64 \
  --particle-chunk-size 64 \
  --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n256-t3-memory-2026-07-01.json \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n256-t3-2026-07-01.json
```

```bash
python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --fd-mode ad-only \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --time-steps 3 \
  --num-particles 1000 \
  --theta 0.02,-0.01,0.01 \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode full \
  --row-chunk-size 128 \
  --col-chunk-size 128 \
  --particle-chunk-size 128 \
  --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n1000-t3-memory-2026-07-01.json \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase3-rung-n1000-t3-2026-07-01.json
```

Rung JSON gate:

- `status == "pass"`;
- `primary_pass is true`;
- all `output_devices` contain `GPU`;
- `compiler.mode == "xla"` and `compiler.jit_compile is true`;
- `transport.transport_ad_mode == "full"`;
- objective is finite;
- all gradient components are finite;
- seed-gradient MCSE is finite;
- `gradients_connected is true`;
- memory sample artifact exists when requested.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | At what particle count does the corrected full route remain finite and operational under GPU/XLA? |
| Baseline/comparator | Previous rung in the same route. |
| Primary criterion | Rung passes finite value/gradient/MCSE and route metadata gates without OOM or CPU fallback. |
| Veto diagnostics | OOM, XLA failure, CPU fallback, nonfinite output, route metadata not full, runtime beyond planned budget. |
| Explanatory diagnostics | Runtime, compile timing, memory, gradient norm, MCSE trend. |
| Not concluded | No HMC direction validity unless Phase 4 passes. |
| Artifact preserving result | Phase 3 JSON/markdown and ledger. |

## Forbidden Claims And Actions

- Do not interpret ladder pass as HMC readiness.
- Do not run `N=1000` if earlier memory/runtime suggests unsafe continuation.
- Do not compare against stopped route as a correctness baseline.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if at least the `N=64`, `T=3`, five-seed rung passes.
If only the tiny rung passes, write a limited-viability result and stop or
return to implementation planning.

## Stop Conditions

- Trusted GPU memory pressure or OOM.
- Repeated XLA failure.
- Nonfinite gradient or objective.
- Same blocker fails five Claude review rounds.
