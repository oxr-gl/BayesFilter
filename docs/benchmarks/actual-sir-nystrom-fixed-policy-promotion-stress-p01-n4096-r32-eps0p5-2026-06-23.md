# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n4096-r32-eps0p5-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-FIXED-POLICY-PROMOTION-STRESS-P01-N4096`
- Shape: `{'batch_size': 3, 'time_steps': 20, 'num_particles': 4096, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `18.95432927296497` | `0.7456044470891356` | `[]` |
| nystrom | `PASS` | `14.898944437038153` | `0.22602915903553367` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `4.99755859375`
- log_likelihood_mean_abs_delta: `2.087646484375`
- warm_median_streaming_over_nystrom_descriptive: `3.298709114658611`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
