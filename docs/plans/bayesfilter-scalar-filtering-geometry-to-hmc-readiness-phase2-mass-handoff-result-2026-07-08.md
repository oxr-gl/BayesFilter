# Phase 2 Result: Geometry-To-Mass Handoff

Date: 2026-07-08
Status: `PASSED`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Subplan: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-subplan-2026-07-08.md`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Whitened mass handoff passes | Passed: Phase 1 artifact passed, `K_z` and `M_z` are finite SPD, condition number 35.99, reconstruction error 4.50e-15, no vetoes | No Phase 2 vetoes | This is a local mass handoff only; HMC dynamics are not tested | Draft and review Phase 3 mechanics canary | No HMC readiness, HMC convergence, posterior correctness, sampler superiority, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness |

## Key Diagnostics

| Diagnostic | Value | Role |
| --- | --- | --- |
| Coordinate system | `whitened_center_plus_scale_times_z` | Hard handoff contract |
| Center role | `truth_free_initial_center` | Boundary guard; not MAP |
| Refined center used | `false` | Hard boundary guard |
| `K_z` precision eigenvalues | `[0.1841, 0.1841, 4.0780, 6.6260]` | SPD/condition gate |
| `M_z` mass covariance eigenvalues | `[0.1509, 0.2452, 5.4317, 5.4317]` | SPD/condition gate |
| Condition number | 35.99 for both `K_z` and `M_z` | Hard gate against cap 1e5; magnitude otherwise descriptive |
| Eigen clipping | 0 clipped eigenvalues | Regularization diagnostic |
| Reconstruction error | `4.50e-15` for `K_z @ M_z ~= I` | Hard gate passed |

## Checks

- `python -m py_compile docs/benchmarks/prepare_scalar_ssl_lstm_filtering_mass_handoff_2026_07_08.py` passed.
- `pytest tests/test_scalar_ssl_lstm_filtering_mass_handoff.py -q` passed: 3 passed.
- `git diff --check` passed.
- `env CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/prepare_scalar_ssl_lstm_filtering_mass_handoff_2026_07_08.py ...` passed and wrote JSON/Markdown artifacts.

## Artifacts

- `docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json`
- `docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.md`
- `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase2-mass-handoff-subplan-2026-07-08.md`
- `docs/reviews/scalar-filtering-geometry-hmc-phase2-mass-handoff-review-bundle-2026-07-08.md`

## Post-Run Red Team

Strongest alternative explanation: a valid mass handoff can still fail HMC mechanics because the center is not stationary and the scalar horizon-30 target may not represent longer or higher-dimensional targets.

What would overturn the result: discovering that `M_z` is used with original-coordinate parameters without the declared `theta = center + scale * z` transform, or that an HMC API expects inverse mass while the artifact is passed as mass covariance.

Weakest evidence part: the artifact validates only matrix algebra and coordinate provenance; it does not test leapfrog dynamics.

## Next Handoff

Phase 3 may draft a mechanics canary that uses `M_z` only in the declared whitened coordinate system. Phase 3 must keep `L * epsilon` and acceptance diagnostics as mechanics evidence, not posterior or convergence evidence.
