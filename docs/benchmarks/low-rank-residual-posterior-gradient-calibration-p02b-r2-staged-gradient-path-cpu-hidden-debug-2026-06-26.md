# P02B-R2 Compact Staged Gradient Path Diagnostic

- Status: `PASS`
- Phase: `LOW_RANK_STAGED_GRADIENT_PATH_P02B_R2`
- Evidence class: `cpu_hidden_debug_only`
- Artifact vetoes: `[]`
- Diagnostic findings: `[]`
- Interpretation scope: `staged whole-sum gradient localization only`
- JSON artifact: `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-cpu-hidden-debug-2026-06-26.json`

## Rows

| Seed | Probe | Same loglik grad | Same final-particle grad | Separated loglik grad | First expected break | H1 tape artifact |
| ---: | --- | --- | --- | --- | --- | --- |
| 91001 | `center` | `{'connected': True, 'finite': True, 'finite_components': [True, True], 'gradient': [0.4512544870376587, 0.13440996408462524], 'norm': 0.4708467378211839}` | `{'connected': True, 'finite': True, 'finite_components': [True, True], 'gradient': [1.1228382587432861, -3.0942726135253906], 'norm': 3.291699980574005}` | `{'connected': True, 'finite': True, 'finite_components': [True, True], 'gradient': [0.45125409960746765, 0.1344095766544342], 'norm': 0.4708462559147843}` | `None:no_observed_expected_connected_break` | `False` |

## H6 SIR Inventory

- Answer: No. They exercise a forward route or a different gradient target/path.

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Device scope: `cpu`
- CUDA_VISIBLE_DEVICES: `-1`
- TF32 recorded: `False`
- JIT compile: `False`
- GPU trust basis: `None`

## Non-Claims

- P02B-R2 compact staged gradient-path localization diagnostic only
- no low-rank solver repair claim
- no residual-threshold calibration claim
- no P03 handoff claim
- no posterior correctness claim
- no HMC readiness claim
- no default/package/public API readiness claim
- no statistical superiority claim
- no scientific validity claim
