# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-fixed-policy-promotion-stress-p01-n2048-r32-eps0p5-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-FIXED-POLICY-PROMOTION-STRESS-P01-N2048`
- Shape: `{'batch_size': 3, 'time_steps': 20, 'num_particles': 2048, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `both`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `18.510332682868466` | `0.2672716311644763` | `[]` |
| nystrom | `PASS` | `14.760027736891061` | `0.15417952905409038` | `[]` |

## Paired Comparability

- log_likelihood_max_abs_delta: `3.092529296875`
- log_likelihood_mean_abs_delta: `2.1047770182291665`
- warm_median_streaming_over_nystrom_descriptive: `1.7335091941467151`

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
