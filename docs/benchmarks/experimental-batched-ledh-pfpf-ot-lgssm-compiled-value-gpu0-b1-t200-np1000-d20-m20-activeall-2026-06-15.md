# Experimental Batched LEDH-PFPF-OT LGSSM Scale Benchmark

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-lgssm-compiled-value-gpu0-b1-t200-np1000-d20-m20-activeall-2026-06-15.json`
- Mode: `compiled-value`
- Shape: B=1, T=200, N=1000, state_dim=20, obs_dim=20
- Device request: `/GPU:0`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- JIT compiled: `True`
- Compile plus first call seconds: `363.3586277551949`
- Warm-call timing summary seconds: `{'min': 8.290091150905937, 'median': 8.290091150905937, 'max': 8.290091150905937}`
- Finite output: `True`

## Nonclaims

- single synthetic LGSSM-shaped fixture only
- no production default readiness claim
- no CPU/GPU ranking claim
- no scalar parity claim
- no active transport gradient validation claim
