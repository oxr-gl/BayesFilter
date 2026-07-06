# P02B-R2 Compact Staged Gradient Path Diagnostic

- Status: `PASS`
- Phase: `LOW_RANK_STAGED_GRADIENT_PATH_P02B_R2`
- Evidence class: `owner_designated_managed_session_visible_gpu_trusted`
- Artifact vetoes: `[]`
- Diagnostic findings: `[]`
- Interpretation scope: `staged whole-sum gradient localization only`
- JSON artifact: `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02b-r2-staged-gradient-path-small-visible-gpu-2026-06-26.json`

## Rows

| Seed | Probe | Same loglik grad | Same final-particle grad | Separated loglik grad | First expected break | H1 tape artifact |
| ---: | --- | --- | --- | --- | --- | --- |
| 91003 | `center` | `{'connected': True, 'finite': True, 'finite_components': [True, True], 'gradient': [-0.5048569440841675, -2.3420207500457764], 'norm': 2.395817548903711}` | `{'connected': True, 'finite': True, 'finite_components': [True, True], 'gradient': [2.6538991928100586, 5.184882164001465], 'norm': 5.82461878410754}` | `{'connected': True, 'finite': True, 'finite_components': [True, True], 'gradient': [-0.5048569440841675, -2.3420207500457764], 'norm': 2.395817548903711}` | `None:no_observed_expected_connected_break` | `False` |
| 91002 | `qr_plus` | `{'connected': True, 'finite': True, 'finite_components': [True, True], 'gradient': [-0.1264142245054245, -0.5369585752487183], 'norm': 0.5516385299183164}` | `{'connected': True, 'finite': True, 'finite_components': [True, True], 'gradient': [-32.67249298095703, 49.05421447753906], 'norm': 58.93901726020794}` | `{'connected': True, 'finite': True, 'finite_components': [True, True], 'gradient': [-0.12641428411006927, -0.5369595289230347], 'norm': 0.5516394718729876}` | `None:no_observed_expected_connected_break` | `False` |

## H6 SIR Inventory

- Answer: No. They exercise a forward route or a different gradient target/path.

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `1`
- TF32 recorded: `True`
- JIT compile: `False`
- GPU trust basis: `owner_designated_managed_session_visible_gpu_trusted`

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
