# Phase 2 Result: BayesFilter Central Policy Implementation

Date: 2026-07-07
Status: `PASSED_WITH_REPAIR`

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does BayesFilter expose and use one central geometry-scaled budget/timing policy? |
| Primary criterion | Met for the BayesFilter serious/default tuning path: `HMCGeometryScaledBudgetTimingPolicy` centralizes attempt budgets, bootstrap screen sizing, and emergency stage caps. |
| Veto diagnostics | No active NUTS/No-U-Turn path was introduced. Public passed-artifact leakage was found by read-only review and repaired before closeout. |
| Explanatory diagnostics | Policy uses dimension, condition number, effective dimension/anisotropy, and regularization pressure. Emergency caps are machine-protection only. |
| Not concluded | No CCMA tuned kernel, posterior convergence, sampler superiority, scientific validity, GPU readiness, or production/default-readiness claim. |

## Implementation Summary

- Added/exported `HMCGeometryScaledBudgetTimingPolicy` in BayesFilter.
- Routed serious attempt budgets through the central policy.
- Routed serious bootstrap screen counts through the central policy.
- Made `HMCStagedTimeoutPolicy` defaults emergency safety caps, not progress gates.
- Preserved fixed-trajectory HMC: mass from covariance, SPD/diagonal regularization, grid over `L`, tune epsilon for each `L`, repair edge grids, final local grid, freeze `(L, epsilon)`, then windowed mass update while progress exists.
- Did not add or use NUTS.

## Review And Repair

Claude Code review was not available through the approval path, so a fresh Codex read-only review was used as the replacement reviewer.  The review returned `VERDICT: REVISE` with one high-severity issue: a passed public final handoff still copied private mechanics (`step_size`, `num_leapfrog_steps`, `trajectory_length`, and mass payload arrays) from the private final kernel.

Repair performed:

- Added a public final-kernel summary path that is non-replayable.
- Public final handoffs now expose hashes, signatures, target dimension, verification status, acceptance summary, and nonclaims only.
- Private BayesFilter replay still uses the private loop payload with mass arrays and fixed-kernel mechanics.
- `HMCTuneVerifyRepairLoopResult.payload(include_final_mass_arrays=False)` now honors the redaction flag for the final kernel payload.
- Added regression tests for passed public artifacts and public loop summaries.

## MacroFinance Integration Status

- CCMA launcher now requires BayesFilter `HMCGeometryScaledBudgetTimingPolicy` for `--ccma-phase7-staged-timeout-policy phase4y`; it no longer constructs a MacroFinance-local fallback staged-timeout policy.
- CCMA progress-aware supervisor keeps a large safety cap (`86400s`) and separate no-progress monitor (`3600s`).
- A separate generated-data K1 public artifact leak was repaired by hiding literal fixed HMC mechanics in `tiny_budget`.
- Residual issue: `one_country_zlb_ns_estimation.py` still has local staged HMC timing constants. This is outside the CCMA/BayesFilter promoted-default repair and should get a dedicated plan before changing that lane.

## Checks Run

- `PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider tests/test_hmc_kernel_tuning_public_api.py tests/test_hmc_kernel_tuning_outer_loop.py tests/test_hmc_kernel_tuning_bootstrap.py tests/test_hmc_budget_ladder.py -q`
  Result: `157 passed`.
- `PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider tests/test_run_ccma_phase3e_serious_tuning.py -q -k "staged_timeout_policy or progress_aware_joint_tuning_supervisor or bootstrap_diagnostic or windowed_mass_timeout_closeout"`
  Result: `6 passed, 18 deselected`.
- `PYTHONPATH=/home/ubuntu/python/BayesFilter PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider tests/test_mixed_frequency_tfp_generated_data_hmc_authority_bridge.py::test_k1_full_chain_xla_probe_runs_non_xla_control_then_fails_closed -q`
  Result: `1 passed`.
- AST parse check for changed BayesFilter and MacroFinance Python files.
  Result: passed.
- No-NUTS scan: no active `tfp.mcmc.NoUTurnSampler`/`NoUTurn` use in changed tuning path; remaining `NUTS` hits are docs/reference/test-only.

## Decision Table

| Decision | Status |
| --- | --- |
| Central BayesFilter policy implemented | Passed focused tests. |
| Public redaction for passed final handoff | Repaired after review and regression-tested. |
| NUTS exclusion | Passed active-path scan. |
| CCMA local fallback timing policy | Removed for promoted `phase4y` path. |
| Default-readiness | Not claimed. |
| Next justified action | Phase 5 closeout/reset memo, then a small CCMA public-path smoke before any long actual-target tuning run. |

## Inference Status

| Evidence Class | Status |
| --- | --- |
| Hard veto screen | No NUTS introduced; public leak repaired; focused tests pass. |
| Statistically supported ranking | None. No stochastic ranking was attempted. |
| Descriptive-only differences | CCMA-like policy smoke gave larger bootstrap counts for ill-conditioned geometry, but this is policy behavior only. |
| Default-readiness | Not established. |
| Next evidence needed | Actual CCMA public-path smoke using the promoted BayesFilter policy, followed by a reviewed long tuning run only if smoke artifacts are public-safe. |

## Post-Run Red Team

Strongest alternative explanation: tests prove payload shape and routing, not that the resulting HMC kernel is good for CCMA.  The weakest evidence is still end-to-end actual-target behavior; no long CCMA tuning run was launched here.  A future result that shows public progress stalls despite the new policy would invalidate the current runtime policy, not the posterior model.
