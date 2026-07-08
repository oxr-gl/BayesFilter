# Phase 0 Result: Governance, Inventory, And Baseline Lock

Date: 2026-07-07

Status: `PASSED_WITH_REPAIR_TARGETS`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 1 design | Met: active paths and material constants are classified below | No active NUTS path found; no MacroFinance-local HMC tuning authority found in checked CCMA path | Exact final numeric formulas remain Phase 1 design items | Draft central policy design subplan | No tuning readiness, posterior convergence, sampler superiority, GPU readiness, or scientific validity |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What exact constants and active paths must later repair centralize or preserve? |
| Baseline/comparator | Current active `bayesfilter/inference/hmc_kernel_tuning.py`, BayesFilter HMC budget ladder, focused HMC tests, and CCMA launcher/watcher path. |
| Primary pass criterion | Met. This note classifies active sample/time/attempt/progress constants and names repair targets. |
| Veto diagnostics | No active CCMA NUTS path found. No active MacroFinance-local HMC tuning authority found in checked path. |
| Explanatory diagnostics | BayesFilter and MacroFinance worktrees are dirty; unrelated changes must be preserved. |
| Not concluded | No implementation correctness, no tuning readiness, no posterior convergence, no sampler superiority, no runtime performance claim. |

## Active Path Inventory

| Area | Active file/function | Classification |
| --- | --- | --- |
| One-call public tuner | `bayesfilter/inference/hmc_kernel_tuning.py::tune_hmc_kernel` and `HMCKernelTuningConfig` | Active BayesFilter authority |
| Attempt budgets | `_HMCAttemptBudgetPolicy`, `_default_attempt_budget_policy`, `_public_budget_policy_factory` | Active policy, currently split between serious and public presets |
| Bootstrap sizing | `_public_bootstrap_config` | Active policy, currently hard-coded by preset plus overrides |
| Staged timeout | `HMCStagedTimeoutPolicy`, `_default_staged_timeout_policy_stage_budgets` | Active policy, currently literal stage budgets |
| CCMA wrapper | `cross_country_multi_asset_macro_mixed_frequency_hmc_kernel_tuning.py` | Active MacroFinance target adapter and BayesFilter caller |
| CCMA launcher | `scripts/run_ccma_phase3e_serious_tuning.py` | Active MacroFinance launcher; currently owns CCMA staged timeout numbers |
| CCMA watcher | `scripts/watch_ccma_tuning_progress.py` and progress-aware supervisor shell | Active public progress monitor |
| Generic docs | BayesFilter LaTeX HMC chapters | Correct documentation target |

## Magic-Number Classification

| Constant family | Current location | Current role | Phase 1/2 repair target |
| --- | --- | --- | --- |
| Bootstrap `4/1`, `16/4`, `32/8` | `_public_bootstrap_config` | Active preset defaults; small diagnostic counts | Move behind central sample-budget policy with explicit `smoke`, `diagnostic`, and `tuning-evidence` roles |
| Serious budget constants | `_default_attempt_budget_policy` payload references `_SERIOUS_TUNING_*` and floors `32/8`, `64/16` | Active serious policy | Extend to geometry-scaled policy using dimension plus covariance/mass condition/effective dimension/regularization pressure |
| Public preset budget formulas | `_public_budget_policy_factory` uses caps/floors like `64`, `256`, dimension multipliers, `25*d` | Active non-serious policy | Centralize with same policy object and role-specific caps/rationales |
| Attempt defaults `1/2/3/5` and cap 10 | `HMCKernelTuningConfig` presets and cap | Active attempt policy | Preserve min 5 and allow up to 10 only with meaningful progress; expose rationale in policy payload |
| Terminal extra attempt `0/1` | `terminal_phase6_repair_extra_attempts` | Active repair-slot edge case | Keep only if Phase 1 proves it is still needed after progress-based attempt policy |
| Trajectory window `0.3..3.0` | `HMCKernelTuningConfig` | Active acceptance/trajectory screen | Keep as reviewed broad default unless Phase 1 changes it with evidence; include provenance |
| BayesFilter staged budgets `750/300/900/600/900/600`, global `3600`, reserve `60` | `HMCStagedTimeoutPolicy` defaults | Active timeout defaults | Replace or relabel as derived emergency/progress policy; no bare `900` active default |
| CCMA staged budgets `3600`, `900`, cap `21600`, reserve `60` | `scripts/run_ccma_phase3e_serious_tuning.py` | Active CCMA override | Move derivation into BayesFilter or make launcher request BayesFilter policy by name without local numeric table |
| Supervisor `21600`, `3600`, poll `60`, attempts `10`, `n_steps=8` | progress-aware supervisor shell | Active wrapper defaults | Derive or import public policy metadata; preserve only emergency and poll constants with explicit policy provenance |
| Watcher safety/no-progress thresholds | `watch_ccma_tuning_progress.py` args | Active monitor inputs | Keep watcher as mechanism, but thresholds must come from central policy or launcher policy payload |
| Test constants | focused tests | Test fixtures | Keep when labeled fixtures; update expectations to assert policy derivation/rationale, not literal magic defaults |

## BayesFilter Usage Audit

Checked CCMA wrapper and launcher import `HMCKernelTuningConfig`,
`HMCStagedTimeoutPolicy`, and `tune_hmc_kernel` from `bayesfilter.inference`.
No active import from MacroFinance-local `filters.*`, `inference.hmc*`,
`inference.mass_matrix`, or `inference.posterior_adapter` appeared in the
checked CCMA tuning path.  MacroFinance contains public redaction checks for
private tuning mechanics, but does not own HMC transition, mass adaptation,
step-size tuning, or L-grid mechanics in the checked path.

## No-NUTS Audit

Search found no active NUTS/NoUTurn use in the checked CCMA path or
`hmc_kernel_tuning.py`.  BayesFilter has a separate
`fixed_trajectory_hmc_tuning_v2.py` guard that rejects NUTS labels as
reference/diagnostic only.  Active sampler calls in the inspected path use
`tfp.mcmc.HamiltonianMonteCarlo`.

## Phase 1 Handoff

Phase 1 must design a single central policy that provides:

- geometry summary inputs: dimension, mass/covariance condition number,
  effective dimension, and regularization pressure;
- role-aware sample budgets for bootstrap, Phase 5 tuning/screening, Phase 6
  screening, and final verification;
- acceptance-uncertainty logic so ambiguous estimates get more draws or are
  marked insufficient evidence;
- attempt policy with at least 5 attempts and up to 10 only while repair
  progress is meaningful;
- progress-aware timing policy that separates sample budget, stall detection,
  and emergency cap;
- public-safe rationale payloads that do not leak private mass arrays, raw
  samples, candidate grids, or step sizes;
- tests proving high dimension and bad geometry increase budgets and
  slow-but-progressing runs are not killed by a hard timeout.

## Review Status

Claude review was attempted and rejected by the approval system as an external
workspace data-risk.  A fresh Codex substitute read-only review was recorded at
`docs/reviews/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-p00-codex-substitute-review-2026-07-07.md` with `VERDICT: AGREE`.

## Inference Status

| Row | Status |
| --- | --- |
| Hard veto screen | No active NUTS or MacroFinance-local HMC tuning authority found in checked active path |
| Statistically supported ranking | None; no stochastic comparison was run |
| Descriptive-only differences | Current constants are descriptive inventory only |
| Default-readiness | Not established |
| Next evidence needed | Phase 1 design and Phase 2 tests for derived policy behavior |
