# Phase 3 Result: GPU/XLA/TF32 Route Smoke

Date: 2026-06-30

Status: `PASS`

## Decision

Phase 3 passed after the user approved retrying the bounded repaired GPU
diagnostic through a short wrapper script.  The successful artifact exercises
the Phase 2 `route_prerequisites` field in the SIR Sinkhorn budget diagnostic
itself, not only the older regression-FD route smoke.

## Supporting Evidence Completed

Escalated GPU probe:

```bash
nvidia-smi
```

Result:

- GPU visible: NVIDIA GeForce RTX 4080 SUPER.
- Driver/CUDA visible through trusted execution.

Escalated route smoke:

```bash
python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --cuda-visible-devices 0 --expect-device-kind gpu --dtype float32 --tf32-mode enabled --ad-evaluation-mode manual-reverse --manual-reverse-compiler xla --fd-mode ad-only --batch-seeds 81120,81121 --time-steps 1 --num-particles 16 --theta 0.02,-0.01,0.01 --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --row-chunk-size 16 --col-chunk-size 16 --particle-chunk-size 16 --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.json
```

Result artifact:

- `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.json`

Supporting route facts from the JSON:

- `output_devices`: GPU:0 for objective and gradient tensors.
- `precision.tf32_execution_enabled`: `true`.
- `compiler.mode`: `xla`.
- `compiler.jit_compile`: `true`.
- `transport.gradient_mode`: `manual_streaming_finite_sinkhorn_stopped_scale_keys`.
- `transport.transport_plan_mode`: `streaming`.
- `transport.transport_ad_mode`: `stabilized`.
- `gradient_finite`: `true`.
- `monte_carlo_gradient_noise_mcse_finite`: `true`.

This is useful route evidence, but it is not sufficient for the repaired Phase
3 gate because it does not emit the Phase 2 `route_prerequisites` field.

## Historical Blocker And Repair

The repaired Phase 3 command was initially attempted twice with escalation:

```bash
python docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py --device-scope visible --cuda-visible-devices 0 --expect-device-kind gpu --dtype float32 --tf32-mode enabled --manual-reverse-compiler xla --num-particles 16 --time-steps 1 --batch-seeds 81120,81121 --candidate-steps 10 --theta 0.02,-0.01,0.01 --base-step 0.001 --regression-offsets -3,-2,-1,0,1,2,3 --trim-extreme-values 0 --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --row-chunk-size 16 --col-chunk-size 16 --particle-chunk-size 16 --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.json --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.md
```

Both direct long-command attempts returned:

```text
Rejected("The automatic permission approval review did not finish before its deadline. Do not assume the action is unsafe based on the timeout alone. You may retry once, or ask the user for guidance or explicit approval.")
```

After explicit user approval, the command was moved into:

- `scripts/run_sir_gradient_phase3_gpu_smoke.sh`

The first wrapper launch exposed two CLI wiring issues:

- negative regression offsets must be passed as
  `--regression-offsets=-3,-2,-1,0,1,2,3`;
- `--transport-plan-mode` and `--transport-ad-mode` are fixed internally by
  `diagnose_p8p_sir_sinkhorn_budget.py` and are not exposed CLI flags.

The wrapper was patched and rerun successfully with trusted GPU execution.

Successful command:

```bash
bash scripts/run_sir_gradient_phase3_gpu_smoke.sh
```

Successful artifacts:

- JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.json`
- Markdown:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.md`

Focused JSON gate check:

```bash
python - <<'PY'
import json, math
from pathlib import Path
p = Path('docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.json')
data = json.loads(p.read_text())
r = data['records'][0]
route = r['route_prerequisites']
checks = route['checks']
required = [
    'device_scope_visible',
    'expect_device_kind_gpu',
    'outputs_on_gpu',
    'dtype_float32',
    'tf32_enabled',
    'manual_reverse_compiler_xla',
    'compiler_jit_compile',
    'manual_score_route',
    'streaming_transport_plan',
    'stabilized_transport_ad',
    'manual_streaming_transport_gradient',
    'finite_objective',
    'finite_gradient',
]
missing = [k for k in required if not checks.get(k)]
assert route['route_prerequisite_pass'] is True
assert not route['failed_checks']
assert not missing
assert math.isfinite(r['transport']['objective'])
assert r['transport']['row_residual_pass'] is True
print('PHASE3_ROUTE_GATE_PASS')
PY
```

Focused check result:

- `PHASE3_ROUTE_GATE_PASS`
- `sinkhorn_steps`: `10`
- `max_row_residual`: `3.933906555175781e-06`
- `objective`: `-36.1715087890625`
- `compiler.mode`: `xla`
- `compiler.jit_compile`: `true`
- `score_route`: `manual_reverse_scan_no_autodiff`
- `output_devices`:
  `['/job:localhost/replica:0/task:0/device:GPU:0', '/job:localhost/replica:0/task:0/device:GPU:0']`
- `precision.tf32_execution_enabled`: `true`

## Gate Status

Phase 3 gate: `PASSED`.

Reason:

- `route_prerequisites.route_prerequisite_pass == true`
- `route_prerequisites.failed_checks == []`
- GPU-visible route, float32 dtype, TF32 enabled, XLA JIT compiler, manual
  reverse score route, streaming stabilized transport, finite objective, finite
  gradient, and row residual pass were all observed in the repaired diagnostic.

## Nonclaims

- The Phase 3 run is a tiny route smoke only.
- The small `N=16`, `T=1`, two-seed numerical direction outcomes are not
  material SIR validation evidence.
- No material SIR gradient diagnostic has run in Phase 3.
- No HMC/NUTS readiness or posterior correctness is claimed.

## Next Action

Proceed to Phase 4 material SIR gradient diagnostic with the frozen Phase 1
gate, refreshed wrapper-based command, and Claude read-only review before
promoting any pass/fail interpretation.
