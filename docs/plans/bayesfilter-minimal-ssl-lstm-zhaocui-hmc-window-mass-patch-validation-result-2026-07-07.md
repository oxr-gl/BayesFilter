# Minimal SSL-LSTM Zhao-Cui HMC Window-Mass Patch Validation Result

Date: 2026-07-07

Status: `PATCH_DID_NOT_CLEAR_PHASE8_BLOCKER`

## Question

Does the current worktree repair to the window-mass / fixed-mass tuning route
help the previously blocked minimal scalar `zhaocui_fixed` HMC terminal
repair-slot case?

## Decision

Decision: `NO_PUBLIC_LEVEL_IMPROVEMENT_ON_THIS_SMOKE_CASE`.

The fresh CPU-hidden diagnostic ran successfully and produced a valid
structured artifact, but it reproduced the same public outcome as the prior
Phase 8 terminal repair-slot artifact:

- final status: `budget_exhausted`
- diagnostic role: `budget_exhausted_non_promoting`
- hard vetoes: `[]`
- final kernel hash: `None`
- active fixed-mass blocker:
  - `screen_acceptance_above_repair_band`
  - `joint_l_epsilon_no_viable_pair`
  - `phase5_fixed_mass_step_status:repair_or_retry`

## Baseline Versus Candidate

| Field | Phase 8 baseline | Patch validation |
| --- | --- | --- |
| Wrapper status | `passed` | `passed` |
| Phase decision | `structured_non_promoting_tuning_result_recorded` | `structured_non_promoting_tuning_result_recorded` |
| Tuning final status | `budget_exhausted` | `budget_exhausted` |
| Diagnostic role | `budget_exhausted_non_promoting` | `budget_exhausted_non_promoting` |
| Hard vetoes | `[]` | `[]` |
| Attempt count | `2` | `2` |
| Windowed stage | `passed` | `passed` |
| Fixed-mass step stage | `repair_or_retry` | `repair_or_retry` |
| Fixed-mass triggers | `screen_acceptance_above_repair_band`, `joint_l_epsilon_no_viable_pair` | `screen_acceptance_above_repair_band`, `joint_l_epsilon_no_viable_pair` |
| Frozen trajectory stage | not reached in latest attempt | not reached in latest attempt |
| Final kernel hash | `None` | `None` |

## Patch Validation Artifact

- JSON:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_window_mass_patch_validation_cpu_hidden_2026-07-07.json`
- Markdown:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_window_mass_patch_validation_cpu_hidden_2026-07-07.md`
- Public tuning artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_window_mass_patch_validation_public_artifacts_2026-07-07/hmc_kernel_tuning_result.json`
- Public progress artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_window_mass_patch_validation_public_artifacts_2026-07-07/hmc_kernel_tuning_progress.json`

## Checks

| Check | Status |
| --- | --- |
| Skeptical plan audit | passed with boundaries |
| `py_compile` for touched tuning/harness/test files | passed |
| Focused tests | `19 passed, 59 deselected` |
| `git diff --check` before runtime | passed |
| Runtime command | exited `0`; CPU-hidden |
| Output JSON validation | passed |
| Public tuning JSON validation | passed |
| Public progress JSON validation | passed |
| Private event count | `22`; count only, private mechanics not exposed |

## Interpretation

The patch appears compatible with the focused contracts and does not introduce
a runtime or artifact validity failure in this diagnostic. However, on the
minimal `zhaocui_fixed` Phase 8-style smoke case, it does not clear or move the
public blocker. The fixed-mass joint L/epsilon search still completes four
candidates with zero selected pairs and no candidate hard vetoes in the public
summary.

This is evidence that the current blocker is not resolved by the tested
window-mass repair alone. It is not evidence against the broader tuning idea,
because this run is smoke-scale, CPU-hidden, and uses one seed/target/settings
contract.

## Decision Table

| Field | Decision |
| --- | --- |
| Primary criterion status | `PASSED`: fresh artifact answers the patch-validation question. |
| Veto diagnostic status | No hard vetoes; no runtime exception; valid JSON artifacts. |
| Main uncertainty | Whether changing the fixed-mass acceptance/repair band, L/epsilon neighborhood, candidate budget, diagnostic scale, or GPU/XLA route would produce a viable pair. |
| Next justified action | Start a reviewed fixed-mass tuning-design program that inspects the no-viable-pair behavior directly instead of continuing ad hoc retries. |
| What is not being concluded | No posterior correctness, HMC convergence, zero-divergence, ranking, superiority, default readiness, production readiness, source-faithful Zhao-Cui parity, dimensional generality, or LEDH claim. |

## Next Step

The next program should focus on why all public-safe fixed-mass candidates miss
the repair band in this target. Candidate design questions:

- Is the repair band too narrow for this smoke diagnostic?
- Is the joint L/epsilon neighborhood centered on the wrong anchor?
- Does the candidate budget need a staged expansion before declaring
  `joint_l_epsilon_no_viable_pair`?
- Is the mass-window seed suitable after a Phase 6 handoff, or should the next
  mass window use a different reviewed seed route?
- Should the next discriminating run be CPU-hidden smoke, larger CPU diagnostic,
  or trusted GPU/XLA?
