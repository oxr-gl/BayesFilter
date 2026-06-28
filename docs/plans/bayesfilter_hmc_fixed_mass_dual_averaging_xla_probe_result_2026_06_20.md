# BayesFilter HMC Fixed-Mass Dual-Averaging XLA Probe Result

Date: 2026-06-20

Status: `PASSED_HOST_XLA_GAUSSIAN_WRAPPER_PROBE`

Subplan:
`docs/plans/bayesfilter_hmc_fixed_mass_dual_averaging_xla_probe_subplan_2026_06_20.md`

Review ledger:
`docs/plans/bayesfilter_hmc_fixed_mass_dual_averaging_xla_probe_review_ledger_2026_06_20.md`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Narrowed the BayesFilter full-chain HMC guard so `use_xla=True` is allowed only for reviewed `fixed_mass_dual_averaging`; generic dual averaging remains fail-closed. |
| Primary criterion status | Passed: focused tests showed the exact BayesFilter Gaussian full-chain wrapper compiles/runs under Host-XLA with fixed-mass dual averaging and required adaptive telemetry. |
| Veto diagnostic status | No phase veto fired. Full-chain XLA authority gates, raw-string adaptation rejection, and reviewed-but-generic dual-averaging rejection remained in force. |
| Main uncertainty | This is a tiny Gaussian wrapper probe under CPU-hidden Host-XLA. It does not test the CCMA 314D target, GPU execution, convergence, or posterior validity. |
| Next justified action | Draft/review a MacroFinance CCMA exact-target fixed-mass dual-averaging Host-XLA canary subplan before any CCMA adaptive run. |
| Not concluded | No CCMA readiness, GPU readiness, posterior convergence, posterior correctness, empirical validity, mass adaptation, default-readiness, or sampler superiority. |

## Run Manifest

| Field | Value |
| --- | --- |
| BayesFilter git commit | `43bcb2015127712705d7ac77d3f0c9b01d349733` |
| Repo dirty state | Dirty before this phase from unrelated HMC telemetry and DPF/OT work; unrelated changes preserved. This phase touched `bayesfilter/inference/hmc.py`, `tests/test_hmc_fixed_mass_step_tuning.py`, `tests/test_nonlinear_ssm_phase4_full_chain_hmc.py`, and BayesFilter HMC plan artifacts. |
| Environment | Python `3.13.13`; TensorFlow `2.20.0`; TensorFlow Probability `0.25.0`. |
| Device context | `CUDA_VISIBLE_DEVICES=-1`; TensorFlow listed `gpus=[]`. This is Host-XLA / CPU-hidden evidence only. |
| Syntax command | `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache python -m py_compile bayesfilter/inference/hmc.py tests/test_hmc_fixed_mass_step_tuning.py tests/test_nonlinear_ssm_phase4_full_chain_hmc.py` |
| Config smoke command | `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 python - <<'PY' ... FullChainHMCConfig(... use_xla=True, tuning_policy=fixed_mass_dual_averaging ...) ... PY` |
| Focused pytest command | `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 python -m pytest -q -p no:cacheprovider tests/test_nonlinear_ssm_phase4_full_chain_hmc.py::test_phase4_tiny_full_chain_hmc_jit_returns_finite_samples_and_metadata tests/test_nonlinear_ssm_phase4_full_chain_hmc.py::test_phase4_reviewed_dual_averaging_policy_records_diagnostic_telemetry tests/test_nonlinear_ssm_phase4_full_chain_hmc.py::test_phase4_reviewed_dual_averaging_policy_compiles_with_xla tests/test_nonlinear_ssm_phase4_full_chain_hmc.py::test_phase4_xla_full_chain_hmc_fails_closed_without_reviewed_authority tests/test_nonlinear_ssm_phase4_full_chain_hmc.py::test_phase4_target_only_xla_readiness_does_not_authorize_full_chain_xla tests/test_nonlinear_ssm_phase4_full_chain_hmc.py::test_phase4_rejects_unreviewed_adaptation_policy tests/test_hmc_fixed_mass_step_tuning.py::test_xla_generic_dual_averaging_remains_blocked_for_phase3 tests/test_hmc_fixed_mass_step_tuning.py::test_full_chain_hmc_rejects_generic_dual_averaging_policy_in_phase3 tests/test_hmc_fixed_mass_step_tuning.py::test_fixed_mass_step_tuning_records_frozen_mass_and_required_telemetry` |
| Focused pytest result | `9 passed, 47 warnings in 10.76s`. |
| Config smoke output | `True fixed_mass_dual_averaging`. |
| Plan file | Subplan above. |
| Result file | This file. |

## Evidence Summary

| Diagnostic | Role | Result |
| --- | --- | --- |
| Skeptical plan audit | Required pre-run gate | Passed after explicit baseline, veto, nonclaim, stop-condition, and artifact checks. |
| Claude review | Material plan review | Round 1 `REVISE`; Round 2 `AGREE` after focused patch. |
| Fixed-kernel XLA Gaussian smoke | Baseline comparator | Passed in focused pytest set. |
| Non-XLA fixed-mass dual-averaging telemetry | Baseline comparator | Passed in focused pytest set. |
| New fixed-mass dual-averaging XLA Gaussian exact-path probe | Primary criterion | Passed; test asserts `jit_compile=True`, finite samples, finite final step size, `step_size`, `target_accept_prob`, `num_adaptation_steps`, full-chain XLA authority metadata, and nonclaims. |
| Full-chain XLA authority boundaries | Veto diagnostic | Passed; unreviewed authority and target-only XLA readiness remain rejected. |
| Raw-string adaptive policy | Veto diagnostic | Passed; `adaptation_policy="dual_averaging"` remains fail-closed. |
| Reviewed-but-generic dual-averaging policy | Veto diagnostic | Passed; `HMCTuningPolicy.dual_averaging_step_size` remains rejected for full-chain HMC. |
| GPU readiness | Forbidden claim | Not tested; GPU hidden. |

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | No hard veto fired in the scoped BayesFilter Host-XLA Gaussian wrapper probe. |
| Statistically supported ranking | None; no stochastic method comparison or ranking was run. |
| Descriptive-only differences | Timing, acceptance, and adapted step-size values are explanatory only. |
| Default-readiness | Not established. |
| Next evidence needed | CCMA exact-target fixed-mass dual-averaging Host-XLA canary under a reviewed MacroFinance subplan. |

## Post-Run Red Team

| Question | Answer |
| --- | --- |
| Strongest alternative explanation | The BayesFilter wrapper and Gaussian fixture are XLA-compatible, but the CCMA 314D target may still fail under adaptive full-chain XLA due to target-specific graph shape, telemetry, runtime, or numerical behavior. |
| What would overturn this decision | A failure of the new focused BayesFilter XLA test, authority-boundary regression, or a broader TFP/XLA incompatibility discovered in the exact CCMA target canary. |
| Weakest part of evidence | It is a tiny Host-XLA Gaussian fixture, not the CCMA target and not GPU execution. |

## Handoff

MacroFinance may revise its prior Phase 5 architecture-blocked status only for
the narrow statement that BayesFilter no longer blocks reviewed
`fixed_mass_dual_averaging` at configuration time under `use_xla=True`.

The next authorized step is a reviewed CCMA exact-target fixed-mass
dual-averaging Host-XLA canary. A full CCMA HMC run, posterior diagnostics,
GPU-readiness claim, or non-XLA fallback remains unauthorized.
