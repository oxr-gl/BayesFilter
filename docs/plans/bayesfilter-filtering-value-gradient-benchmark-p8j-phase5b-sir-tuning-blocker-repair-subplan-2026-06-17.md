# P8j Phase 5b Subplan: SIR Tuning Blocker Repair

metadata_date: 2026-06-17
status: EXECUTED_PENDING_PHASE5B_RESULT_AND_PHASE5C_SUBPLAN_REVIEW
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 5b
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Repair or classify the Phase 5 SIR d18 particle-tuning blockers:

- bootstrap DPF: `BLOCK_P8J_SIR_PARTICLE_TUNING_MC_SE`;
- LEDH OT: `BLOCK_P8J_SIR_PARTICLE_TUNING_NONFINITE` from
  `Sinkhorn row residual exceeded tolerance envelope`.

This phase may run focused diagnostics and implement narrowly reviewed harness
repairs.  It may not refresh the leaderboard.  It may not change SIR model/data
definitions.

## Entry Conditions Inherited From Previous Phase

- Phase 5 produced `executed_p8j_sir_particle_tuning_stage0_with_blockers`.
- No SIR DPF particle count was selected.
- Phase 6 leaderboard refresh is blocked.
- This Phase 5b subplan has Claude `VERDICT: AGREE`.

## Required Artifacts

- Phase 5b result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-result-2026-06-17.md`
- Optional repair diagnostic JSON/CSV if commands are run:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-2026-06-17.json`
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-2026-06-17.csv`
- Updated P8j execution ledger and Claude review ledger.
- A refreshed Phase 5 subplan or Phase 6 subplan only if the repair is reviewed
  and Phase 5 can be rerun safely.

## Required Checks/Tests/Reviews

Local checks before any diagnostic:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8j or sir_dpf"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-subplan-2026-06-17.md
```

Bootstrap repair diagnostics:

- Run higher bootstrap-only candidate counts above `64`, for example
  `128,256`, with the same five seeds and trusted GPU.
- Select bootstrap only if the same MC SE and adjacent-rung gates pass.
- If runtime projection exceeds budget or MC SE remains above threshold, keep
  the blocker.

LEDH OT repair diagnostics:

- Diagnose the Sinkhorn row residual failure without changing the SIR model:
  record state scale/cost scale at the failing first resampling event, source
  weights, effective sample size, and solver residuals when possible.
- Test only reviewed command-level or harness-level OT solver repairs, such as
  scale-adaptive cost normalization, larger epsilon, more iterations, or looser
  but explicit residual tolerance.
- Any repair must preserve route identifiers and record that it is a P8j SIR
  OT numerical-stability repair, not Zhao-Cui source-faithfulness evidence.

Claude review is required before rerunning a repaired Phase 5 tuning ladder.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the Phase 5 blockers fixable by a reviewed tuning range or OT numerical-stability repair without changing SIR model/data or crossing claim boundaries? |
| Baseline/comparator | Phase 5 blocker artifact, Phase 4 finite N=4 OT smoke, and P8h reviewed OT covariance-carry route. |
| Primary criterion | Either a reviewed repair plan enables rerunning Phase 5 safely, or the blocker is preserved with exact failure cause and next human decision point. |
| Veto diagnostics | Model/data mutation; selecting N=8; accepting one-seed smoke; fewer than five seeds for value evidence; untrusted GPU evidence; silent tolerance relaxation; claiming leaderboard, gradient/HMC, or source-faithful TT/SIRT evidence. |
| Explanatory diagnostics | Bootstrap MC SE by count, adjacent-rung deltas, Sinkhorn residuals, cost/state scale, ESS, runtime, route identifiers. |
| Not concluded | Particle adequacy, leaderboard completion, DPF gradient correctness, HMC/NUTS readiness, source-faithful TT/SIRT parity, MATLAB parity, production readiness. |

## Forbidden Claims/Actions

- Do not proceed to Phase 6.
- Do not change SIR model/data definitions.
- Do not select `N=8`.
- Do not treat one-seed or failed-rung diagnostics as tuning evidence.
- Do not silently relax Sinkhorn tolerances after seeing failures; any tolerance
  change must be explicit, justified, and reviewed.
- Do not claim score/Hessian/theta-gradient/HMC/NUTS evidence.
- Do not claim Zhao-Cui TT/SIRT source-faithfulness or MATLAB parity.
- Do not stage, commit, merge, or push.

## Exact Next-Phase Handoff Conditions

Phase 5 may be rerun only if:

- Phase 5b result identifies a bounded repair or higher-count ladder;
- focused local tests pass;
- Claude returns `VERDICT: AGREE` on the repair result/subplan;
- GPU commands remain trusted/escalated.

Phase 6 may begin only after a rerun Phase 5 selects reviewed particle counts or
the user explicitly narrows Phase 6 to a reviewed subset.

## Stop Conditions

Stop and preserve the blocker if:

- higher bootstrap counts still fail MC SE or runtime budget;
- LEDH OT remains nonfinite after one reviewed numerical-stability repair
  attempt;
- repair would require model/data changes;
- repair would require untrusted GPU execution;
- Claude review does not converge after five rounds for the same blocker.

## Skeptical Plan Audit

This phase could mislead us by converting a real tuning failure into an
unreviewed solver relaxation.  The plan therefore separates bootstrap
tuning-range failure from LEDH OT numerical-stability failure and requires
review before any rerun can be promoted back into Phase 5.
