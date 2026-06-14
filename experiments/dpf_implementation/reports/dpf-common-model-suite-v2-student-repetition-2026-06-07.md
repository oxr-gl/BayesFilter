# DPF Common Model Suite V2 Student Repetition Result

metadata_date: 2026-06-07
decision: PASS_STUDENT_REPETITION_TERMINALLY_CLASSIFIED

## Question

Can the two quarantined student repositories be applied to the same frozen V2 density/path/fixed-ancestor/gradient contracts with every cell terminally classified and no oracle claim?

## Evidence Contract

Primary criterion: every implementation/model/surface cell is terminally classified as `MATCHED`, `EXPLAINED_MISMATCH`, `INTERFACE_BLOCKED`, or `OUT_OF_SCOPE` under the frozen V2 contracts.

Veto diagnostics: missing closed V2 artifacts, oracle misuse, unreviewed contract/tolerance changes, FD used as a gate, unclassified executed discrepancy, proxy student panel substitution, or CPU-only TensorFlow without pre-import `CUDA_VISIBLE_DEVICES=-1`.

FD diagnostics are diagnostic-only and were not used as a gate.

## Summary

| Status | Count |
|---|---:|
| `EXPLAINED_MISMATCH` | 2 |
| `INTERFACE_BLOCKED` | 46 |

Executed cells:

- `advanced_particle_filter::lgssm_2d_h25_rich::density`
- `advanced_particle_filter::lgssm_2d_h25_rich::noresampling_path`

## Cells

| Implementation | Model | Surface | Status | Reason |
|---|---|---|---|---|
| `advanced_particle_filter` | `lgssm_2d_h25_rich` | `density` | `EXPLAINED_MISMATCH` | APF LGSSM density values differ under the frozen V2 density probes; APF adds covariance jitter and uses its own density helpers. |
| `advanced_particle_filter` | `lgssm_2d_h25_rich` | `noresampling_path` | `EXPLAINED_MISMATCH` | APF bootstrap PF loop was executable under replay, but the frozen V2 noresampling_path primary values or branch semantics differ; see per-field metrics. |
| `advanced_particle_filter` | `lgssm_2d_h25_rich` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | advanced_particle_filter BootstrapParticleFilter resamples after the measurement update, while the frozen V2 fixed-ancestor contract branches at the start of the step before propagation.  No exact same-branch-timing replay surface is exposed without writing a new adapter and reviewed amendment. |
| `advanced_particle_filter` | `lgssm_2d_h25_rich` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | advanced_particle_filter does not expose the V2 fixed-noise fixed-ancestor physical-knob AD scalar; its differentiable PF uses different SV/HMC resampling contracts. |
| `advanced_particle_filter` | `sv_1d_h18_rich` | `density` | `INTERFACE_BLOCKED` | advanced_particle_filter SVSSM/DPF surfaces target a batched HMC/DPF contract and do not expose the V2 fixed finite particle path scalar. |
| `advanced_particle_filter` | `sv_1d_h18_rich` | `noresampling_path` | `INTERFACE_BLOCKED` | advanced_particle_filter SVSSM/DPF surfaces target a batched HMC/DPF contract and do not expose the V2 fixed finite particle path scalar. |
| `advanced_particle_filter` | `sv_1d_h18_rich` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | advanced_particle_filter SVSSM/DPF surfaces target a batched HMC/DPF contract and do not expose the V2 fixed finite particle path scalar. |
| `advanced_particle_filter` | `sv_1d_h18_rich` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | advanced_particle_filter SVSSM/DPF surfaces target a batched HMC/DPF contract and do not expose the V2 fixed finite particle path scalar. |
| `advanced_particle_filter` | `range_bearing_4d_h20_rich` | `density` | `INTERFACE_BLOCKED` | advanced_particle_filter exposes a range-bearing model, but its public range-bearing density uses Student-t observation noise while V2 uses Gaussian range/bearing noise with the frozen covariance. |
| `advanced_particle_filter` | `range_bearing_4d_h20_rich` | `noresampling_path` | `INTERFACE_BLOCKED` | advanced_particle_filter exposes a range-bearing model, but its public range-bearing density uses Student-t observation noise while V2 uses Gaussian range/bearing noise with the frozen covariance. |
| `advanced_particle_filter` | `range_bearing_4d_h20_rich` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | advanced_particle_filter exposes a range-bearing model, but its public range-bearing density uses Student-t observation noise while V2 uses Gaussian range/bearing noise with the frozen covariance. |
| `advanced_particle_filter` | `range_bearing_4d_h20_rich` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | advanced_particle_filter exposes a range-bearing model, but its public range-bearing density uses Student-t observation noise while V2 uses Gaussian range/bearing noise with the frozen covariance. |
| `advanced_particle_filter` | `structural_ar1_quadratic_h16` | `density` | `INTERFACE_BLOCKED` | advanced_particle_filter has no exposed V2-compatible structural_ar1_quadratic_h16 model surface. |
| `advanced_particle_filter` | `structural_ar1_quadratic_h16` | `noresampling_path` | `INTERFACE_BLOCKED` | advanced_particle_filter has no exposed V2-compatible structural_ar1_quadratic_h16 model surface. |
| `advanced_particle_filter` | `structural_ar1_quadratic_h16` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | advanced_particle_filter has no exposed V2-compatible structural_ar1_quadratic_h16 model surface. |
| `advanced_particle_filter` | `structural_ar1_quadratic_h16` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | advanced_particle_filter has no exposed V2-compatible structural_ar1_quadratic_h16 model surface. |
| `advanced_particle_filter` | `spatial_sir_j3_rk4` | `density` | `INTERFACE_BLOCKED` | advanced_particle_filter has no exposed V2-compatible spatial_sir_j3_rk4 model surface. |
| `advanced_particle_filter` | `spatial_sir_j3_rk4` | `noresampling_path` | `INTERFACE_BLOCKED` | advanced_particle_filter has no exposed V2-compatible spatial_sir_j3_rk4 model surface. |
| `advanced_particle_filter` | `spatial_sir_j3_rk4` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | advanced_particle_filter has no exposed V2-compatible spatial_sir_j3_rk4 model surface. |
| `advanced_particle_filter` | `spatial_sir_j3_rk4` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | advanced_particle_filter has no exposed V2-compatible spatial_sir_j3_rk4 model surface. |
| `advanced_particle_filter` | `predator_prey_rk4` | `density` | `INTERFACE_BLOCKED` | advanced_particle_filter has no exposed V2-compatible predator_prey_rk4 model surface. |
| `advanced_particle_filter` | `predator_prey_rk4` | `noresampling_path` | `INTERFACE_BLOCKED` | advanced_particle_filter has no exposed V2-compatible predator_prey_rk4 model surface. |
| `advanced_particle_filter` | `predator_prey_rk4` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | advanced_particle_filter has no exposed V2-compatible predator_prey_rk4 model surface. |
| `advanced_particle_filter` | `predator_prey_rk4` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | advanced_particle_filter has no exposed V2-compatible predator_prey_rk4 model surface. |
| `2026MLCOE` | `lgssm_2d_h25_rich` | `density` | `INTERFACE_BLOCKED` | 2026MLCOE current adapters do not expose initial/transition/observation density components with V2 scalar constants and checksums. |
| `2026MLCOE` | `lgssm_2d_h25_rich` | `noresampling_path` | `INTERFACE_BLOCKED` | 2026MLCOE BPF samples internally and exposes particle summaries, not fixed initial particles, fixed innovations, and fixed ancestor replay under the V2 scalar contract. |
| `2026MLCOE` | `lgssm_2d_h25_rich` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | 2026MLCOE BPF samples internally and exposes particle summaries, not fixed initial particles, fixed innovations, and fixed ancestor replay under the V2 scalar contract. |
| `2026MLCOE` | `lgssm_2d_h25_rich` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | 2026MLCOE has no exposed V2 fixed-branch physical-knob AD gradient surface. |
| `2026MLCOE` | `sv_1d_h18_rich` | `density` | `INTERFACE_BLOCKED` | 2026MLCOE current adapters do not expose initial/transition/observation density components with V2 scalar constants and checksums. |
| `2026MLCOE` | `sv_1d_h18_rich` | `noresampling_path` | `INTERFACE_BLOCKED` | 2026MLCOE BPF samples internally and exposes particle summaries, not fixed initial particles, fixed innovations, and fixed ancestor replay under the V2 scalar contract. |
| `2026MLCOE` | `sv_1d_h18_rich` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | 2026MLCOE BPF samples internally and exposes particle summaries, not fixed initial particles, fixed innovations, and fixed ancestor replay under the V2 scalar contract. |
| `2026MLCOE` | `sv_1d_h18_rich` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | 2026MLCOE has no exposed V2 fixed-branch physical-knob AD gradient surface. |
| `2026MLCOE` | `range_bearing_4d_h20_rich` | `density` | `INTERFACE_BLOCKED` | 2026MLCOE current adapters do not expose initial/transition/observation density components with V2 scalar constants and checksums. |
| `2026MLCOE` | `range_bearing_4d_h20_rich` | `noresampling_path` | `INTERFACE_BLOCKED` | 2026MLCOE BPF samples internally and exposes particle summaries, not fixed initial particles, fixed innovations, and fixed ancestor replay under the V2 scalar contract. |
| `2026MLCOE` | `range_bearing_4d_h20_rich` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | 2026MLCOE BPF samples internally and exposes particle summaries, not fixed initial particles, fixed innovations, and fixed ancestor replay under the V2 scalar contract. |
| `2026MLCOE` | `range_bearing_4d_h20_rich` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | 2026MLCOE has no exposed V2 fixed-branch physical-knob AD gradient surface. |
| `2026MLCOE` | `structural_ar1_quadratic_h16` | `density` | `INTERFACE_BLOCKED` | 2026MLCOE current adapters do not expose initial/transition/observation density components with V2 scalar constants and checksums. |
| `2026MLCOE` | `structural_ar1_quadratic_h16` | `noresampling_path` | `INTERFACE_BLOCKED` | 2026MLCOE BPF samples internally and exposes particle summaries, not fixed initial particles, fixed innovations, and fixed ancestor replay under the V2 scalar contract. |
| `2026MLCOE` | `structural_ar1_quadratic_h16` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | 2026MLCOE BPF samples internally and exposes particle summaries, not fixed initial particles, fixed innovations, and fixed ancestor replay under the V2 scalar contract. |
| `2026MLCOE` | `structural_ar1_quadratic_h16` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | 2026MLCOE has no exposed V2 fixed-branch physical-knob AD gradient surface. |
| `2026MLCOE` | `spatial_sir_j3_rk4` | `density` | `INTERFACE_BLOCKED` | 2026MLCOE current adapters do not expose initial/transition/observation density components with V2 scalar constants and checksums. |
| `2026MLCOE` | `spatial_sir_j3_rk4` | `noresampling_path` | `INTERFACE_BLOCKED` | 2026MLCOE BPF samples internally and exposes particle summaries, not fixed initial particles, fixed innovations, and fixed ancestor replay under the V2 scalar contract. |
| `2026MLCOE` | `spatial_sir_j3_rk4` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | 2026MLCOE BPF samples internally and exposes particle summaries, not fixed initial particles, fixed innovations, and fixed ancestor replay under the V2 scalar contract. |
| `2026MLCOE` | `spatial_sir_j3_rk4` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | 2026MLCOE has no exposed V2 fixed-branch physical-knob AD gradient surface. |
| `2026MLCOE` | `predator_prey_rk4` | `density` | `INTERFACE_BLOCKED` | 2026MLCOE current adapters do not expose initial/transition/observation density components with V2 scalar constants and checksums. |
| `2026MLCOE` | `predator_prey_rk4` | `noresampling_path` | `INTERFACE_BLOCKED` | 2026MLCOE BPF samples internally and exposes particle summaries, not fixed initial particles, fixed innovations, and fixed ancestor replay under the V2 scalar contract. |
| `2026MLCOE` | `predator_prey_rk4` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | 2026MLCOE BPF samples internally and exposes particle summaries, not fixed initial particles, fixed innovations, and fixed ancestor replay under the V2 scalar contract. |
| `2026MLCOE` | `predator_prey_rk4` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | 2026MLCOE has no exposed V2 fixed-branch physical-knob AD gradient surface. |

## Command Manifest

- command: `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_student_repetition_tf`
- commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`
- branch: `main`
- CPU-only: `True`
- `CUDA_VISIBLE_DEVICES`: `-1`
- output JSON: `experiments/dpf_implementation/reports/outputs/dpf_common_model_suite_v2_student_repetition_2026-06-07.json`

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next action | Not concluded |
|---|---|---|---|---|---|
| PASS_STUDENT_REPETITION_TERMINALLY_CLASSIFIED | all 48 cells terminally classified | no veto fired | future adapter work could expose more exact V2 student surfaces | Claude result/governance review, then close | no student correctness, failure, or filter correctness claim |

## Post-Run Red Team

Strongest alternative explanation: additional lower-level student code might be adaptable to more V2 surfaces with new reviewed adapters, but those surfaces are not exposed by the current adapters without changing the execution contract.

Result that would overturn this decision: discovery of an existing student command or adapter that already accepts the frozen V2 density/path/fixed-ancestor/gradient fixtures exactly and was missed by this inventory.

Weakest evidence link: the executed evidence is narrow, mainly APF LGSSM replay; blocked cells are interface classifications, not exhaustive proofs about all possible future adapters.

## Non-Claims

- no student correctness or failure claim
- no BayesFilter or FilterFlow oracle claim
- no filter correctness proof
- no stochastic-resampling distribution claim
- no differentiable-resampling claim
- no TT/SIRT or paper-scale reproduction claim
- no GPU, HMC, DSGE, scalability, deployment, or production-readiness claim
