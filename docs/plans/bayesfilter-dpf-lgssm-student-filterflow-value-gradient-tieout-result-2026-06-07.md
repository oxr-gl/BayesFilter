# DPF LGSSM Student/FilterFlow Value and Gradient Tie-Out Result

metadata_date: 2026-06-07
decision: PASS_LGSSM_STUDENT_FILTERFLOW_TERMINALLY_CLASSIFIED

## Question

For LGSSM only, can APF and MLCOE expose value and gradient surfaces that match the closed FilterFlow V2 contracts?

## Evidence Contract

Primary criterion: every LGSSM student/surface cell is terminally classified under the frozen FilterFlow V2 value/gradient contracts.

FD, Kalman checks, APF jitter mirrors, and MLCOE missing-constant mirrors are diagnostic-only and cannot create strict `MATCHED` status.

## Summary

- strict cells: `8`
- status counts: `{'EXPLAINED_MISMATCH': 2, 'INTERFACE_BLOCKED': 6}`
- diagnostic mirrors: `['apf_jittered_density_mirror:EXPLAINS_STRICT_DELTA', 'apf_jittered_noresampling_mirror:EXPLAINS_STRICT_DELTA', 'mlcoe_weight_only_likelihood_mirror:NOT_RUN']`

## Strict Cells

| Implementation | Surface | Status | Reason |
|---|---|---|---|
| `advanced_particle_filter` | `density_components` | `EXPLAINED_MISMATCH` | APF LGSSM density values differ from the strict FilterFlow V2 density probes because APF adds +1e-8 I covariance jitter before Gaussian Cholesky/log-density evaluation. |
| `advanced_particle_filter` | `noresampling_path` | `EXPLAINED_MISMATCH` | APF no-resampling replay matches the frozen particles but differs from strict FilterFlow V2 weights/log-normalizers at the APF +1e-8 I observation-covariance jitter scale. |
| `advanced_particle_filter` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | APF BootstrapParticleFilter resamples after the measurement update, while the V2 fixed-ancestor LGSSM contract branches before propagation.  No exact strict-V2 branch-timing surface is exposed without a reviewed adapter amendment. |
| `advanced_particle_filter` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | APF TF LGSSM builders convert inputs through tf.constant and APF's differentiable PF surface is SV/HMC-oriented; no exposed LGSSM fixed-branch scalar with V2 knobs transition_matrix_scale and observation_noise_scale is available. |
| `2026MLCOE` | `density_components` | `INTERFACE_BLOCKED` | MLCOE current LGSSM/BPF adapters do not expose initial, transition, observation, and scalar Gaussian density components with the frozen V2 constants and checksums. |
| `2026MLCOE` | `noresampling_path` | `INTERFACE_BLOCKED` | MLCOE BPF samples internally through TensorFlow Probability and exposes particle summaries, not fixed initial particles, fixed transition innovations, fixed ancestor indices, and the V2 log-normalizer scalar. |
| `2026MLCOE` | `fixed_ancestor_path` | `INTERFACE_BLOCKED` | MLCOE BPF samples internally through TensorFlow Probability and exposes particle summaries, not fixed initial particles, fixed transition innovations, fixed ancestor indices, and the V2 log-normalizer scalar. |
| `2026MLCOE` | `fixed_branch_gradient` | `INTERFACE_BLOCKED` | MLCOE DPF/PHMC surfaces do not expose the frozen LGSSM fixed-branch log-normalizer scalar with V2 knobs transition_matrix_scale and observation_noise_scale. |

## Diagnostic-Only Localization

| Diagnostic | Status | Max delta | Note |
|---|---|---:|---|
| `apf_jittered_density_mirror` | `EXPLAINS_STRICT_DELTA` | `4.440892098500626e-16` | none; diagnostic-only |
| `apf_jittered_noresampling_mirror` | `EXPLAINS_STRICT_DELTA` | `5.551115123125783e-17` | none; diagnostic-only |
| `mlcoe_weight_only_likelihood_mirror` | `NOT_RUN` | `N/A` | MLCOE exposes no strict V2 fixed-particle/fixed-innovation PF log-normalizer scalar in the current adapter, so the mirror is not applicable until a strict value cell executes. |

## Command Manifest

- command: `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_student_filterflow_value_gradient_tieout_tf`
- commit: `7ccb9c39883471c2d5ec2891cbf33b9ed436bada`
- branch: `main`
- CPU-only: `True`
- `CUDA_VISIBLE_DEVICES`: `-1`
- output JSON: `experiments/dpf_implementation/reports/outputs/dpf_lgssm_student_filterflow_value_gradient_tieout_2026-06-07.json`

## Review State

Claude result/governance review: `PASS`.

Review summary:

- all eight strict cells are terminally classified;
- APF jitter mirrors remain diagnostic-only and do not create strict
  `MATCHED` status;
- no oracle claim, FD gate, proxy student panel, unreviewed contract weakening,
  or vendored student edit was found;
- CPU-only pre-import CUDA hiding is enforced and recorded;
- interface blocks are not treated as student failures.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next action | Not concluded |
|---|---|---|---|---|---|
| PASS_LGSSM_STUDENT_FILTERFLOW_TERMINALLY_CLASSIFIED | EXPLAINED_MISMATCH=2, INTERFACE_BLOCKED=6 | no veto fired | current student surfaces expose few strict V2 LGSSM cells | Claude result/governance review | no correctness, oracle, stochastic-resampling, differentiable-resampling, or production claim |

## Post-Run Red Team

Strongest alternative explanation: a future reviewed adapter could expose additional exact LGSSM surfaces without vendored-code edits; current interface blocking is not a proof that no such adapter can ever exist.

Result that would overturn this decision: discovery of an existing student surface that already accepts the frozen V2 particles, innovations, ancestor schedule, scalar, and knobs exactly but was missed.

Weakest evidence link: APF executable strict cells are narrow, and MLCOE remains classified by interface evidence rather than executable strict V2 values.

## Non-Claims

- no student correctness or failure claim
- no FilterFlow, BayesFilter, APF, or MLCOE oracle claim
- no filter correctness proof
- no stochastic-resampling distribution claim
- no differentiable-resampling claim
- no TT/SIRT or paper-scale reproduction claim
- no GPU, HMC, DSGE, scalability, deployment, or production-readiness claim
