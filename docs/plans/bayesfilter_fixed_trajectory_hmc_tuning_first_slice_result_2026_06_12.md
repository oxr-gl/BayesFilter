# BayesFilter Fixed-Trajectory HMC Tuning First Slice Result

Date: 2026-06-12

Plan: `docs/plans/bayesfilter_fixed_trajectory_hmc_tuning_master_plan_2026_06_12.md`

Review: `docs/plans/bayesfilter_fixed_trajectory_hmc_tuning_master_plan_review_round_01_2026_06_12.md`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Implemented first slice as an explicit v2 module: tiny Gaussian fixed-trajectory HMC tuning schema/result/helper/tests. |
| Primary criterion status | Passed focused checks for explicit step size, leapfrog count/trajectory length, identity mass policy, closed `[0.65, 0.75]` tuning band, artifact nonclaims, and NUTS fail-closed behavior. |
| Veto diagnostic status | No NUTS tuning/default remedy, empirical/windowed mass adaptation, convergence claim, superiority claim, default-readiness claim, or legacy fixed-kernel screen rewrite was introduced. |
| Main uncertainty | Tiny Gaussian TFP HMC fixture only; acceptance is a promotion screen for tuning plumbing, not sampler validity. |
| Next justified action | Later reviewed slices may add richer target/mass validation and broader candidate ladders. |
| What is not concluded | No posterior convergence, sampler superiority, production/default readiness, GPU/XLA readiness, MacroFinance readiness, or large-scale model readiness. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `4df30ec31f30d880a1e1ed83b0b6a449442ec293` |
| Workspace | `/home/ubuntu/python/BayesFilter` |
| Environment | Python `3.13.13`; TensorFlow/TFP imported by focused pytest. |
| CPU/GPU status | Focused pytest run used `CUDA_VISIBLE_DEVICES=-1`; no GPU readiness claim. |
| Random seed | Tiny fixture test/helper seed `(20260612, 7)`. |
| Output artifacts | This result note plus new tests and in-memory `FixedTrajectoryHMCV2TuningResult.payload()`. |
| Plan file | `docs/plans/bayesfilter_fixed_trajectory_hmc_tuning_master_plan_2026_06_12.md` |
| Result file | `docs/plans/bayesfilter_fixed_trajectory_hmc_tuning_first_slice_result_2026_06_12.md` |

## Checks Run

| Command | Outcome |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python -m py_compile bayesfilter/inference/hmc_tuning.py bayesfilter/inference/__init__.py bayesfilter/__init__.py tests/test_fixed_trajectory_hmc_tuning.py` | Failed because Python attempted to write `bayesfilter/inference/__pycache__/...` on a read-only filesystem despite `PYTHONDONTWRITEBYTECODE=1`. Treated as environment/cache-path issue, then rerun with cache redirected. |
| `PYTHONPYCACHEPREFIX=/tmp/bayesfilter_pycache PYTHONDONTWRITEBYTECODE=1 python -m py_compile bayesfilter/inference/hmc_tuning.py bayesfilter/inference/__init__.py bayesfilter/__init__.py tests/test_fixed_trajectory_hmc_tuning.py` | Passed. |
| `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_fixed_trajectory_hmc_tuning.py -q` | Passed: `5 passed, 3 warnings in 3.20s`. Warnings were TensorFlow Probability `distutils` deprecations and pytest cache inability to write under the read-only workspace cache. |
| `PYTHONPYCACHEPREFIX=/tmp/bayesfilter_pycache PYTHONDONTWRITEBYTECODE=1 python -m py_compile bayesfilter/inference/hmc_tuning.py bayesfilter/inference/fixed_trajectory_hmc_tuning_v2.py bayesfilter/inference/__init__.py bayesfilter/__init__.py tests/test_fixed_trajectory_hmc_tuning.py` | Passed after the v2 isolation repair. |
| `CUDA_VISIBLE_DEVICES=-1 PYTHONPYCACHEPREFIX=/tmp/bayesfilter_pycache PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_fixed_trajectory_hmc_tuning.py -q -p no:cacheprovider` | Passed after the v2 isolation repair and final non-export assertion tightening: `5 passed, 2 warnings in 3.27s`. Warnings were TensorFlow Probability `distutils` deprecations. |

## Implementation Notes

- Skeptical audit repair: the first implementation slice initially touched the
  shared `bayesfilter.inference.hmc_tuning` export surface. That was a material
  integration flaw because another agent may depend on the legacy API.
- Added explicit v2-only symbols in
  `bayesfilter.inference.fixed_trajectory_hmc_tuning_v2`:
  `FixedTrajectoryHMCV2CandidateResult`, `FixedTrajectoryHMCV2TuningResult`,
  `FIXED_TRAJECTORY_HMC_V2_ACCEPTANCE_BAND`, and
  `run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2`.
- The v2 helper is not re-exported from `bayesfilter.inference` or top-level
  `bayesfilter`.
- The helper uses `tfp.mcmc.HamiltonianMonteCarlo`, not NUTS, over explicit
  finite candidate grids.
- First slice accepts only `mass_policy="identity"` and fails closed for
  empirical/windowed mass adaptation requests.
- The closed `[0.65, 0.75]` acceptance band is recorded as a tuning promotion
  screen. The legacy `(0.05, 0.99)` fixed-kernel screen remains separate.
- Result payloads include policy label, selected step size, leapfrog count,
  trajectory length, mass policy, acceptance band, diagnostics, vetoes, and
  nonclaims.

## Post-Run Red-Team Note

Strongest alternative explanation: the tiny Gaussian seed/candidate grid proves
only that the artifact and policy plumbing can select a candidate under TFP HMC.
It does not establish that this tuning strategy will work on larger targets.

Weakest part of the evidence: acceptance rates are short-run descriptive probe
outputs. They are used only for the predeclared closed-band tuning screen.

Result that would overturn the implementation decision: a focused test showing
NUTS can be selected as a remedy/default, non-identity mass adaptation executes
in this first slice, artifact payloads omit nonclaims/veto metadata, or the
legacy broad fixed-kernel screen is silently replaced by the tuning band.
