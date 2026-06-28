# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p03b-while-loop-repair-b1-t20-n1024-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P03B-WHILE-LOOP-REPAIR-B1-T20-N1024`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 1024, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `16.429368857992813` | `0.06890799989923835` | `[]` |
| nystrom | `PASS` | `12.189794685924426` | `0.02689056284725666` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `2.957275390625`
- log_likelihood_mean_abs_delta: `2.957275390625`
- warm_median_streaming_over_nystrom_descriptive: `2.5625346814288883`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
