# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09c-policy-r32-eps0p3-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P09C-POLICY-R32-EPS0P3`
- Shape: `{'batch_size': 5, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `24.04466551914811` | `1.0971721219830215` | `[]` |
| nystrom | `PASS` | `16.81944348081015` | `0.6479200138710439` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `1.51568603515625`
- log_likelihood_mean_abs_delta: `0.731591796875`
- warm_median_streaming_over_nystrom_descriptive: `1.6933758774140795`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
