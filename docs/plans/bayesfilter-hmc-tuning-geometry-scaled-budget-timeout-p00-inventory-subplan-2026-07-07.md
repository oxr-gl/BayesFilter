# Phase 0 Subplan: Governance, Inventory, And Baseline Lock

Date: 2026-07-07

Status: `DRAFT_PHASE_SUBPLAN`

## Phase Objective

Lock the active baseline before implementation: identify the HMC tuning files,
CCMA call path, existing hard-coded sample/time/attempt constants, NUTS
references, public/private diagnostic boundaries, and the exact artifacts that
must change in later phases.

## Entry Conditions

- User approved executing the master prompt.
- BayesFilter is the implementation authority.
- MacroFinance is only an integration caller.
- No implementation edits have been made under this program yet.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-p00-inventory-result-2026-07-07.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-visible-execution-ledger-2026-07-07.md`
- Compact review bundle if Claude gate is used:
  `docs/reviews/bayesfilter-hmc-tuning-geometry-scaled-budget-timeout-p00-review-bundle-2026-07-07.md`

## Required Checks

Run focused read-only inspections:

- active BayesFilter tuner:
  `bayesfilter/inference/hmc_kernel_tuning.py`
- BayesFilter HMC budget ladder:
  `bayesfilter/inference/hmc_budget_ladder.py`
- BayesFilter focused HMC tests:
  `tests/test_hmc_kernel_tuning_*.py`,
  `tests/test_hmc_budget_ladder.py`
- MacroFinance CCMA wrapper and launchers:
  `cross_country_multi_asset_macro_mixed_frequency_hmc_kernel_tuning.py`,
  `scripts/run_ccma_phase3e_serious_tuning.py`,
  `scripts/run_ccma_phase3e_phase7_progress_aware_joint_tuning_supervisor.sh`,
  `scripts/watch_ccma_tuning_progress.py`
- BayesFilter LaTeX HMC docs:
  `docs/chapters/ch21_hmc_for_state_space.tex`,
  `docs/chapters/ch22_mass_matrices.tex`,
  `docs/chapters/ch25_diagnostics.tex`,
  `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact constants and active paths must the later repair centralize or preserve? |
| Baseline/comparator | Current active files before this program's implementation edits. |
| Primary pass criterion | Result note classifies each material sample/time/attempt/progress constant as active default, test fixture, diagnostic override, emergency cap, or historical doc; and identifies exact later-phase repair targets. |
| Veto diagnostics | Inventory misses active CCMA path; NUTS active path found and not blocked; MacroFinance-local tuning authority found and not blocked; magic constants treated as acceptable without provenance. |
| Explanatory diagnostics | Dirty worktree status, existing docs chapters, existing tests, current public-private redaction behavior. |
| Not concluded | No implementation correctness, no tuning readiness, no posterior convergence, no sampler superiority, no runtime performance claim. |

## Forbidden Claims And Actions

- Do not edit implementation code in Phase 0.
- Do not run long HMC tuning.
- Do not claim a constant is correct merely because a test expects it.
- Do not treat short diagnostic sample counts as tuning evidence.
- Do not authorize NUTS.

## Skeptical Plan Audit

- Wrong baseline risk: using stale MacroFinance result docs instead of active
  BayesFilter source.  Mitigation: inspect active source paths directly.
- Proxy metric risk: treating presence of progress JSON as sufficient tuning
  progress.  Mitigation: classify event semantics, not only file modification.
- Missing stop condition risk: inventory could expand indefinitely across old
  plans.  Mitigation: restrict Phase 0 to active tuner, focused tests, CCMA
  launcher/watcher, and relevant LaTeX docs.
- Environment mismatch risk: BayesFilter is outside MacroFinance writable root.
  Mitigation: write BayesFilter artifacts only with approved write path.
- Artifact mismatch risk: a search output alone would not answer the policy
  question.  Mitigation: produce classified result table.

## BayesFilter Usage Audit

Phase 0 must confirm that the active CCMA path imports/calls
`bayesfilter.inference.tune_hmc_kernel` or its public BayesFilter wrapper and
does not implement local mass, step-size, L-grid, or HMC transition mechanics in
MacroFinance.

## No-NUTS Audit

Phase 0 must distinguish LaTeX/reference discussion of NUTS from active CCMA or
BayesFilter tuning code.  Active use is a blocker.

## Magic-Number Audit

Classify:

- sample counts and burn-in counts;
- max attempts and extension rules;
- acceptance windows and trajectory windows;
- timeout/stall/safety caps;
- progress polling intervals;
- test-only constants.

## Next-Phase Handoff Conditions

Advance to Phase 1 only if the result note names:

- the active functions/classes to modify;
- the constants to centralize;
- the tests to add or update;
- the LaTeX location to update;
- any boundary that must remain private/public-safe.

## Stop Conditions

Stop if active NUTS use is found, active MacroFinance-local HMC tuning authority
is found, the active path cannot be identified, or BayesFilter docs/code cannot
be written with approved permissions.
