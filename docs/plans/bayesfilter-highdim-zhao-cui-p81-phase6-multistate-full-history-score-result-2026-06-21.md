# P81 Phase 6 Result: Multistate Full-History Score Propagation

status: PHASE6_TINY_MULTISTATE_SCORE_PASSED_D18_ALL_GRID_BLOCKED_PHASE7_SUBPLAN_DRAFTED_REVIEW_PENDING
date: 2026-06-21
supervisor_executor: Codex
readonly_reviewer: Claude Opus

## Skeptical Audit Before Execution

Pass with boundary.  The reviewed Phase 6 subplan authorized local code/test
edits for multistate full-history score propagation, CPU-hidden focused checks,
and a bounded SIR d=18 candidate smoke only after the tiny multistate
two-observation regression passed.  The execution did not run LEDH/P8p,
GPU/CUDA commands, package installs, network fetches, detached agents, default
policy changes, or destructive git/filesystem actions.

During execution, the SIR d=18 two-row candidate smoke attempted to form an
all-pairs transition tensor with shape proportional to
`262144 x 262144 x 18`, which is not a bounded smoke.  The implementation was
patched to fail fast with `COMPLEXITY_GATE` before such allocation.

## Decision Table

| Field | Status |
|---|---|
| Decision | Tiny multistate full-history score propagation passed; SIR d=18 all-grid two-row route is blocked by quadratic transition scaling. |
| Primary criterion | Partially passed: tiny d=2 two-observation FD regression passed with valid same-branch finite-difference rows. |
| Veto diagnostic status | Veto for SIR d=18 candidate full-history smoke: all-grid transition pairwise tensor exceeds the complexity gate. |
| Main uncertainty | Whether a chunked/streamed all-pairs logsumexp derivative is enough for d=18, or whether a different retained transition representation is required. |
| Next justified action | Draft/review Phase 7 as a scaling-blocker resolution phase, not an LEDH comparator phase. |
| Not concluded | No LEDH/P8p agreement, no SIR d=18 full-history score correctness, no HMC readiness, no posterior/scientific validity, no source-faithfulness, no scaling/default readiness. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `5ea363e594516be236ca7c78ab2067b28a5b6eb5` |
| Worktree status | Dirty; includes P81 edits plus unrelated/non-P81 modified and untracked files already present in the workspace. |
| CPU/GPU status | CPU-hidden for checks with `CUDA_VISIBLE_DEVICES=-1`. No GPU/CUDA command was run in Phase 6. |
| Random seeds | Deterministic branch seed strings in tests: `p81-score-multistate-two-row`, `p81-score-sir-d18-two-row`, and existing P81 seeds. |
| Commands | `python -m py_compile ...`; focused pytest checks listed below. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase6-multistate-full-history-score-subplan-2026-06-21.md` |
| Result file | This file. |
| Reviewer status | Phase 6 subplan Claude review returned `VERDICT: AGREE`; execution review pending. |

## Implementation Summary

Implemented in `bayesfilter/highdim/filtering.py`:

- multistate transition target derivative builder:
  `multistate_nonlinear_transition_adjacent_target_derivative_batch(...)`;
- multistate retained-predictive derivative helpers:
  `_multistate_tt_predictive_log_density_and_derivative_from_retained(...)`
  and `_multistate_grid_predictive_log_density_and_derivative_from_retained(...)`;
- multistate pairwise transition JVP helper:
  `_multistate_transition_log_density_derivative_between_grids(...)`;
- looped `multistate_nonlinear_fixed_design_tt_score_path(...)` over
  observation rows, preserving the one-row path and adding
  `observation_count`/`last_time_index` diagnostics;
- multistep compatibility hash excluding theta;
- pairwise transition tensor complexity gate to prevent OOM.

Test changes:

- extended the tiny multistate fixture with parameter-sensitive transition
  density;
- added a d=2 two-observation same-branch FD regression;
- added a SIR d=18 two-row complexity-gate regression showing the all-grid
  transition route is not bounded.

Incidental import/regression blockers fixed because they prevented focused
checks from running:

- restored the missing `tf_svd_cut4_score(...)` function header and
  `_matvec_points(...)` helper in
  `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`;
- restored missing `mahalanobis = tf.reduce_sum(innovation * solve_innovation)`
  in `bayesfilter/nonlinear/sigma_points_tf.py`.

## Checks

| Check | Result |
|---|---|
| `CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/filtering.py bayesfilter/highdim/__init__.py bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py bayesfilter/nonlinear/sigma_points_tf.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p81_analytical_sir_score.py` | passed |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_fixed_branch_derivatives.py -k "multistate_fixed_design_tt_score_path"` | 2 passed, 18 deselected, 2 warnings |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "horizon0 or two_row"` | 2 passed, 2 deselected, 2 warnings |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p46_multistate_zhaocui_adapter.py tests/highdim/test_p47_spatial_sir_filtering.py` | 10 passed, 2 warnings |

Warnings were TensorFlow Probability `distutils` deprecation warnings.  CPU-only
runs emitted framework CUDA registration/cuInit messages despite
`CUDA_VISIBLE_DEVICES=-1`; those are not GPU evidence and no GPU command was
run.

## Interpretation

The multistate score formula is now wired for a small full-history path:

1. initial target derivative;
2. retained log-density derivative propagation;
3. transition predictive log-density derivative;
4. observation derivative;
5. fixed-design TT coefficient derivative;
6. score accumulation through log normalizer plus log-scale-shift terms;
7. same-branch finite-difference validation.

This is enough to validate the local multistate score mechanism on a tiny
two-observation fixture.  It is not enough for the SIR d=18 full-history
candidate, because the current retained all-grid transition route requires an
all-pairs transition matrix between current and previous tensor grids.  With a
degree-0 d=18 grid, that is `2^18` current points times `2^18` previous points,
which is quadratic in grid size and not a bounded candidate smoke.

## Next Handoff

Review and then execute Phase 7 only as a scaling-blocker resolution phase:
`docs/plans/bayesfilter-highdim-zhao-cui-p81-phase7-d18-transition-scaling-blocker-subplan-2026-06-21.md`.

Do not run LEDH/P8p comparison until a d=18 candidate full-history score route
exists under an explicit memory/runtime contract.
