# Experimental Batched LEDH-PFPF-OT LGSSM Scale Benchmark

- JSON artifact: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-fixed-lgssm-gpu0-b1-t100-np1000-d10-m10-activeall-dense-2026-06-15.json`
- Mode: `compiled-value`
- Shape: B=1, T=100, N=1000, state_dim=10, obs_dim=10
- Device request: `/GPU:0`
- Output devices: `['/job:localhost/replica:0/task:0/device:GPU:0']`
- Transport plan mode: `dense`
- JIT compiled: `True`
- Compile plus first call seconds: `113.004068905022`
- Warm-call timing summary seconds: `{'min': 0.7239098988939077, 'median': 0.7239098988939077, 'max': 0.7239098988939077}`
- Finite output: `True`

## Nonclaims

- single synthetic LGSSM-shaped fixture only
- no production default readiness claim
- no CPU/GPU ranking claim
- no scalar parity claim
- no active transport gradient validation claim
