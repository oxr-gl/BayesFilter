# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-fixed-policy-stress-p01a-r32-eps0p5-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-FIXED-POLICY-STRESS-P01A-R32-EPS0P5`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `19.812803614884615` | `0.10082777799107134` | `[]` |
| nystrom | `PASS` | `16.040742113953456` | `0.10266691586002707` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.5533447265625`
- log_likelihood_mean_abs_delta: `2.08074951171875`
- warm_median_streaming_over_nystrom_descriptive: `0.9820863629383476`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
