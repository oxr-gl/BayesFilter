# P81 Phase 5 Result: Full-History Score Surface Audit

status: PHASE5_AUDIT_PASSED_PHASE6_SUBPLAN_DRAFTED_REVIEW_PENDING
date: 2026-06-21
supervisor_executor: Codex
readonly_reviewer: Claude Opus

## Skeptical Audit Before Execution

Pass.  Phase 5 used only read-only local `rg`, `sed`, `git rev-parse`, and
`git status` audit commands.  It did not run LEDH-PFPF-OT, SIR d=18
full-history candidate diagnostics, TensorFlow framework execution, GPU/CUDA
commands, tests, package installs, network fetches, detached agents, default
changes, or destructive filesystem/git actions.

The plan answers the stated question: identify the exact missing implementation
surface before comparing the Zhao-Cui fixed-branch/JVP-backed candidate against
the full-history LEDH/P8p comparator.  It avoids the wrong baseline problem
because no full-history LEDH result is compared to the current horizon-0
candidate.

## Decision Table

| Field | Status |
|---|---|
| Decision | Proceed to reviewed Phase 6 implementation subplan. |
| Primary criterion | Passed: the missing surface is bounded and concrete. |
| Veto diagnostic status | No veto triggered: no horizon-0 overclaim, no LEDH run, no full-history candidate run, no GPU boundary crossed. |
| Main uncertainty | Multistate transition score propagation is unimplemented; Phase 6 may still fail tiny finite-difference regression. |
| Next justified action | Review and then execute Phase 6: implement multistate retained-predictive derivative propagation and looped score path, with tiny two-row FD regression first. |
| Not concluded | No implementation correctness, no SIR d=18 full likelihood correctness, no LEDH/P8p agreement, no HMC readiness, no posterior/scientific validity, no scaling/default readiness, no source-faithfulness claim. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `5ea363e594516be236ca7c78ab2067b28a5b6eb5` |
| Worktree status | Dirty; includes P81 code/docs/test changes plus unrelated modified/untracked files. |
| Commands | `rg` audit checks from the Phase 5 subplan; targeted `sed` reads of `bayesfilter/highdim/filtering.py`; `git rev-parse HEAD`; `git status --short`. |
| Environment | Local shell in `/home/chakwong/BayesFilter`. |
| CPU/GPU status | N/A: no TensorFlow execution and no GPU/CUDA command in Phase 5. |
| Random seeds | N/A: read-only source audit only. |
| Wall time | Short interactive audit. |
| Output artifact paths | This result; Phase 6 subplan; updated P81 master/runbook/ledgers/handoff. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase5-full-history-score-surface-subplan-2026-06-21.md` |
| Reviewer status | Phase 5 subplan Claude review converged with `VERDICT: AGREE` after one patch round. Result/Phase 6 review pending. |

## Audit Evidence

| Surface | Current status verified | Required next evidence |
|---|---|---|
| Scalar full-history score template | Exists in `scalar_nonlinear_fixed_design_tt_score_path(...)`, currently looped over exactly two observations. | Use only as a design template; do not cite as multistate correctness. |
| Scalar transition target derivative | Exists in `scalar_nonlinear_transition_adjacent_target_derivative_batch(...)`. | Mirror the retained-predictive derivative structure in multistate form. |
| Scalar retained predictive derivative | Exists in `_scalar_tt_predictive_log_density_and_derivative_from_retained(...)` and `_scalar_grid_predictive_log_density_and_derivative_from_retained(...)`. | Phase 6 needs the multistate counterpart. |
| Multistate value path | Exists in `multistate_nonlinear_fixed_design_tt_value_path(...)` and loops over arbitrary observation count. | Phase 6 can reuse its target/fit/retained sequencing. |
| Multistate score path | Exists in `multistate_nonlinear_fixed_design_tt_score_path(...)` but rejects more than one observation row with `multistate score path currently supports horizon-0 smoke only`. | Remove only after implementing transition derivative propagation and tiny regression. |
| Multistate transition value target | Exists in `multistate_nonlinear_transition_adjacent_target_batch(...)`. | Add a derivative builder that includes retained-filter derivative plus transition and observation JVPs. |
| Multistate transition pairwise log density | Exists in `_multistate_pairwise_transition_between_grids_log_density(...)`. | Add a pairwise directional derivative helper, preferably ForwardAccumulator/JVP-backed and single-parameter like current P81 route. |
| Multistate retained log-density derivative | Missing. | Add derivative values on retained multistate grid using normalized squared-TT density derivative helpers, with shape/storage gates. |
| Multistep branch compatibility hash | Horizon-0 helper exists as `_fixed_design_horizon0_compatibility_hash(...)`. | Add or generalize a multistep compatibility hash excluding theta but including observation shape/count, basis, ranks, seeds, target ids, fit config, coordinate maps, and step structure. |
| Tiny multistate transition regression | Missing. | Add d=2 or d=3 two-observation finite-difference regression in `tests/highdim/test_fixed_branch_derivatives.py`. |
| SIR d=18 full-history candidate smoke | Not authorized in Phase 5. | Only after tiny multistate transition regression passes in Phase 6. |
| LEDH/P8p comparator | Harness exists with seeds, particle count, per-seed gradient, MC noise, and GPU expectation options. | Phase 7 only, after candidate full-history score exists. |

## Implementation Surface Map For Phase 6

Bounded Phase 6 edits should stay inside:

- `bayesfilter/highdim/filtering.py`
- `tests/highdim/test_fixed_branch_derivatives.py`
- `tests/highdim/test_p81_analytical_sir_score.py`, only after the tiny
  multistate transition regression passes
- P81 `docs/plans` artifacts

Concrete code surfaces to add or modify:

- Add `_multistate_tt_predictive_log_density_and_derivative_from_retained(...)`
  beside the scalar helper.
- Add `_multistate_grid_predictive_log_density_and_derivative_from_retained(...)`
  beside the current multistate value-only predictive helper.
- Add `_multistate_transition_log_density_derivative_between_grids(...)` using
  the same fixed-branch/JVP-backed convention as Phase 3, not a closed-form
  analytical claim.
- Add `multistate_nonlinear_transition_adjacent_target_derivative_batch(...)`
  mirroring the scalar derivative builder, but preserving multistate shape and
  reference-measure conventions.
- Extend `multistate_nonlinear_fixed_design_tt_score_path(...)` from
  one-row/horizon-0 to loop over observation rows, using the multistate value
  path step structure and checking fit branch hashes against the value run.
- Add or generalize a multistep compatibility hash.  Use unambiguous diagnostic
  terms: `observation_count` and `last_time_index`; avoid using `horizon` for
  both one-row smoke and row count.

## Boundary Notes

- The current candidate is fixed-branch/JVP-backed, not closed-form analytical.
- The current candidate has not yet computed a full-history score for SIR d=18.
- A full-history LEDH/P8p value/gradient comparison would be misleading until
  the candidate has full-history score evidence under the same parameter
  convention.
- Source-faithfulness is not claimed by this phase.

## Next Handoff

Review
`docs/plans/bayesfilter-highdim-zhao-cui-p81-phase6-multistate-full-history-score-subplan-2026-06-21.md`
with Claude read-only.  If it converges, execute Phase 6.  If Phase 6 tiny
regression fails for a wiring reason, patch and rerun focused checks inside
the reviewed boundary.  If the failure shows the implementation surface is not
bounded, write a blocker result and stop.
