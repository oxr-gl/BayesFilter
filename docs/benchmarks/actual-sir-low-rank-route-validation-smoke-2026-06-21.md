# Actual-SIR Low-Rank Route Smoke Aggregate

- Status: `PASS`
- Evidence role: tiny smoke only; no promotion or speedup claim.

| Row | Status | Stream Invocations | Low-Rank Invocations | Factor Residual | ESS Fraction Min | Variance Gate | Warm Ratio Explanatory |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: |
| `B=1,T=3,N=128` | `PASS` | `3` | `3` | `2.2398307919502258e-07` | `0.6771839261054993` | `True` | `2.490910313095381` |
| `B=1,T=20,N=256` | `PASS` | `20` | `20` | `4.6868808567523956e-07` | `0.23121842741966248` | `True` | `1.8547515193146573` |

## Row Artifacts

- `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t3-n128.json`
- `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t3-n128.md`
- `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t20-n256.json`
- `docs/benchmarks/actual-sir-low-rank-route-validation-smoke-2026-06-21-row-b1-t20-n256.md`

## Nonclaims

- No large-N performance claim.
- No posterior correctness claim.
- No public API/default/production readiness claim.
- CPU-hidden timing is explanatory only.
