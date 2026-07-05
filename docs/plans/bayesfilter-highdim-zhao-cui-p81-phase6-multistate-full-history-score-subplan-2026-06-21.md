# P81 Phase 6 Subplan: Multistate Full-History Score Propagation

status: DRAFT_REVIEW_PENDING
date: 2026-06-21

## Phase Objective

Implement and test the bounded multistate full-history fixed-branch/JVP-backed
score path required before any SIR d=18 value/gradient comparison against
LEDH-PFPF-OT.  Phase 6 must first pass a tiny d=2 or d=3 two-observation
finite-difference regression; only then may it run a bounded SIR d=18 two-row
candidate smoke.

## Entry Conditions Inherited From Phase 5

- Phase 3 established only one-row horizon-0 observation-term engineering
  wiring under same-branch finite-difference stability.
- Phase 4 established only trusted GPU-visible backend feasibility for that
  one-row candidate path.
- Phase 5 found a bounded missing surface: multistate retained-predictive
  derivative propagation and a looped multistate score path.
- The current LEDH/P8p harness can do full-history diagnostics, but is not a
  valid comparator until the Zhao-Cui candidate score path can process
  full-history observations.
- The current candidate is fixed-branch/JVP-backed, not closed-form analytical,
  and no source-faithfulness claim is authorized.

## Required Artifacts

- This Phase 6 subplan.
- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase6-multistate-full-history-score-result-2026-06-21.md`.
- Updated P81 master, runbook, execution ledger, Claude review ledger, and stop
  handoff.
- Focused code/test edits, if the reviewed plan converges:
  `bayesfilter/highdim/filtering.py`,
  `tests/highdim/test_fixed_branch_derivatives.py`, and optionally
  `tests/highdim/test_p81_analytical_sir_score.py` after the tiny regression
  passes.

The Phase 6 result must include a skeptical-audit note, decision table, run
manifest, command outputs summarized as pass/fail, and an explicit list of
claims not established.

## Required Checks, Tests, And Reviews

Pre-implementation source checks:

```bash
rg -n "def scalar_nonlinear_fixed_design_tt_score_path|def scalar_nonlinear_transition_adjacent_target_derivative_batch|def _scalar_tt_predictive_log_density_and_derivative_from_retained|def _scalar_grid_predictive_log_density_and_derivative_from_retained" bayesfilter/highdim/filtering.py
rg -n "def multistate_nonlinear_fixed_design_tt_score_path|multistate score path currently supports horizon-0|def multistate_nonlinear_fixed_design_tt_value_path|def multistate_nonlinear_transition_adjacent_target_batch|def _multistate_grid_predictive_log_density_from_retained|def _multistate_pairwise_transition_between_grids_log_density" bayesfilter/highdim/filtering.py
rg -n "test_multistate_fixed_design_tt_score_path_matches_same_branch_fd_for_tiny_horizon0_fixture|test_multistate_fixed_design_tt_score_path_runs_on_sir_d18_horizon0_observation_term" tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p81_analytical_sir_score.py
```

Implementation targets:

- Add `_multistate_transition_log_density_derivative_between_grids(...)`.
- Add `_multistate_grid_predictive_log_density_and_derivative_from_retained(...)`.
- Add `_multistate_tt_predictive_log_density_and_derivative_from_retained(...)`.
- Add `multistate_nonlinear_transition_adjacent_target_derivative_batch(...)`.
- Extend `multistate_nonlinear_fixed_design_tt_score_path(...)` to loop over
  observation rows, while preserving the existing one-row behavior.
- Add a multistep compatibility hash that excludes theta and records
  observation shape/count, last time index, basis/ranks/sweeps/ridge, coordinate
  maps, seeds, target ids, and value-path step structure.

Required local checks after implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/highdim/filtering.py tests/highdim/test_fixed_branch_derivatives.py tests/highdim/test_p81_analytical_sir_score.py
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_fixed_branch_derivatives.py -k "multistate_fixed_design_tt_score_path"
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/highdim/test_p81_analytical_sir_score.py -k "horizon0 or two_row"
```

If the tiny multistate two-row regression passes and the SIR d=18 two-row test
exists, a trusted/escalated GPU-visible run may be used only for the bounded
candidate smoke, per local GPU policy.  Do not run GPU commands
non-escalated.

Review this subplan with Claude read-only before implementation.  Review the
Phase 6 execution result with Claude read-only after local checks.  Loop until
convergence or five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the current multistate Zhao-Cui fixed-branch/JVP-backed score path be extended from one-row horizon-0 to a bounded full-history/two-row score path with same-branch finite-difference agreement? |
| Exact baseline/comparator | Same codebase value path and same-branch finite differences on the tiny fixture.  LEDH/P8p is not a Phase 6 comparator. |
| Primary criterion | Tiny d=2 or d=3 two-observation multistate regression returns finite score and valid finite-difference rows with matching branch hashes and acceptable residual. |
| Veto diagnostics | Nonfinite value/score; branch-hash mismatch; retained derivative shape mismatch; storage/complexity budget failure; global default change required; SIR d=18 run attempted before tiny regression passes; LEDH/P8p comparator run. |
| Explanatory diagnostics | Runtime, FD residual size, condition warnings, retained storage bytes, target/fit/retained hashes, TensorFlow warnings. |
| Not concluded | No LEDH agreement, no SIR d=18 full likelihood correctness beyond the bounded smoke, no HMC readiness, no posterior/scientific validity, no performance scaling, no default readiness, no source-faithfulness. |
| Artifact preserving result | Phase 6 result markdown and updated P81 ledgers. |

## Required Phase 6 Test Design

1. Extend the tiny multistate fixture in
   `tests/highdim/test_fixed_branch_derivatives.py` so
   `transition_log_density(...)` is implemented and parameter-sensitive.
2. Add a two-observation test that calls
   `multistate_nonlinear_fixed_design_tt_score_path(...)` with the existing
   small multistate config.
3. Require:
   - `result.status is HighDimStatus.OK`;
   - `result.score.shape == (1,)`;
   - finite log likelihood and score;
   - valid finite-difference rows;
   - plus/minus/base compatibility hashes match;
   - `diagnostics["observation_count"] == 2`;
   - `diagnostics["last_time_index"] == 1`;
   - max finite-difference error below a predeclared loose engineering smoke
     tolerance.
4. Only after that passes, add a bounded SIR d=18 two-row smoke in
   `tests/highdim/test_p81_analytical_sir_score.py` using a small observation
   pair and the existing P81 local dense budget.  This smoke may check finite
   values and branch-stable FD rows, but it must not claim full scientific
   validation.

## Forbidden Claims And Actions

- Do not run LEDH/P8p comparator diagnostics in Phase 6.
- Do not claim agreement with LEDH/P8p.
- Do not claim full likelihood correctness from a tiny fixture or a two-row
  smoke.
- Do not claim closed-form analytical derivatives; use fixed-branch/JVP-backed
  wording.
- Do not claim Zhao-Cui source-faithfulness without paper/source anchors.
- Do not install/fetch packages, change defaults, launch detached agents, or
  take destructive git/filesystem actions.
- Do not use NumPy as the BayesFilter algorithmic implementation backend.

## Exact Next-Phase Handoff Conditions

Phase 7 may be drafted only if Phase 6 records:

- tiny multistate two-row FD regression passing;
- no branch-hash drift;
- no nonfinite score/value;
- a bounded SIR d=18 candidate smoke result or a precise reason to defer it;
- Claude execution review convergence.

If these conditions pass, Phase 7 should define the LEDH/P8p comparator using
the agreed convention: batched TF32 LEDH default, GPU-visible trusted execution,
10 seeds with `N=2000` particles unless revised by reviewed evidence, and value
plus gradient comparison under explicit Monte Carlo uncertainty.

## Stop Conditions

Stop with a blocker if multistate transition derivative propagation cannot be
implemented without broad refactor/default changes, if same-branch hashes drift
on the tiny regression, if the score/value is nonfinite, if the implementation
requires an unreviewed backend change, or if Claude review does not converge
after five rounds.
