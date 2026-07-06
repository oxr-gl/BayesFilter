# Actual-SIR Nystrom Compiled Redo Benchmark

- JSON artifact: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p08-nystrom-only-n32768-2026-06-23.json`
- Status: `PASS`
- Phase: `ACTUAL-SIR-NYSTROM-COMPILED-REDO-P08-NYSTROM-ONLY-N32768`
- Shape: `{'batch_size': 1, 'time_steps': 20, 'num_particles': 32768, 'state_dim': 18, 'obs_dim': 9}`
- Route request: `nystrom`
- JIT compile: `True`
- Hard vetoes: `[]`

## Routes

| Route | Status | Compile+first seconds | Warm median seconds | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| nystrom | `PASS` | `13.484218016965315` | `0.8095715930685401` | `[]` |

## Paired Comparability

- Not applicable.

## Nonclaims

- redo benchmark after prior runtime protocol quarantine
- no default readiness claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no statistical ranking claim without replicated uncertainty analysis
