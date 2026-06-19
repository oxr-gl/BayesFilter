# P8j Phase 5c Subplan: Scale-Adaptive Sinkhorn Repair Gate

metadata_date: 2026-06-17
status: EXECUTED_PENDING_PHASE5C_RESULT_AND_PHASE5D_SUBPLAN_REVIEW
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 5c
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement and test a bounded P8j SIR d18 LEDH OT numerical-stability repair
candidate: scale-adaptive Sinkhorn epsilon based on the current OT cost scale,
with enough diagnostics to decide whether Phase 5 can be rerun safely.

This phase also records that bootstrap remains blocked at `N=128,256` under the
current MC SE gate and must not be silently promoted.

## Entry Conditions Inherited From Previous Phase

- Phase 5 selected no SIR d18 particle count.
- Phase 5b local checks passed.
- Bootstrap higher-count diagnostic at `N=128,256` remained blocked by
  `BLOCK_P8J_SIR_PARTICLE_TUNING_MC_SE`.
- LEDH OT first-failure diagnostic found nominal Sinkhorn cost scale:
  cost mean `116.56402657134574`, cost max `237.97475859459587`,
  nominal epsilon `1.0`.
- A diagnostic-only probe with epsilon equal to cost mean and `500` iterations
  produced finite residuals at the first event.
- Phase 6 leaderboard refresh remains unauthorized.

## Required Artifacts

- Phase 5c result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-sinkhorn-repair-result-2026-06-17.md`
- Optional LEDH OT repair diagnostic JSON/CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-ledh-ot-2026-06-17.json`
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-ledh-ot-2026-06-17.csv`
- Updated P8j execution ledger, Claude review ledger, and stop handoff.
- A refreshed Phase 5 rerun subplan only if Phase 5c passes and Claude review
  returns `VERDICT: AGREE`.

## Required Checks/Tests/Reviews

Before implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8j or sir_dpf"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-result-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-sinkhorn-repair-subplan-2026-06-17.md
```

Implementation checks:

- Add tests proving the scale-adaptive mode is opt-in and records the adapted
  epsilon, cost scale, iterations, tolerance, and nonclaim boundary.
- Run the focused P8j/SIR tests again.
- Run `python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`.
- Run `git diff --check` on touched files.

Trusted GPU diagnostics:

- Run a LEDH-only diagnostic ladder, initially `N=16,32` and the five fixed
  seeds, with the scale-adaptive Sinkhorn settings.
- The run may use the existing P8j tuning payload only if the repair is wired
  into the profile path with explicit route metadata and no hidden default
  change.
- If `N=16,32` passes finite/transport but fails MC SE or adjacent stability,
  draft a reviewed Phase 5 rerun plan with larger LEDH counts rather than
  claiming a selected count.

Claude review:

- Required before any Phase 5 rerun or Phase 6 draft.
- Review must verify no SIR model/data mutation, no default silent relaxation,
  no leaderboard claim, and no gradient/HMC/source-faithfulness claim.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does a bounded scale-adaptive Sinkhorn epsilon repair the P8j SIR d18 LEDH OT solver failure without changing model/data or silently relaxing claim boundaries? |
| Baseline/comparator | Phase 5 LEDH OT failure at `N=16,32,64`; Phase 5b first-event diagnostic and scale-adaptive probe; Phase 4 finite `N=4` OT smoke. |
| Primary criterion | A five-seed LEDH OT diagnostic ladder produces finite full trajectories, trusted-GPU evidence, valid transport diagnostics, and explicit repair metadata, or the LEDH OT blocker is preserved with cause. |
| Veto diagnostics | Model/data mutation; hidden default change; untrusted GPU; fewer than five fixed seeds for value evidence; selecting `N=8`; nonfinite trajectories; invalid transport diagnostics; treating a diagnostic as leaderboard, gradient/HMC, or source-faithful TT/SIRT evidence. |
| Explanatory diagnostics | Cost scale, adapted epsilon, Sinkhorn iterations/residuals, ESS, runtime, log likelihood, adjacent-rung deltas, route identifiers. |
| Not concluded | Particle adequacy until Phase 5 rerun passes; leaderboard completion; DPF gradient correctness; HMC/NUTS readiness; Zhao-Cui TT/SIRT or MATLAB parity; production readiness. |

## Forbidden Claims/Actions

- Do not proceed to Phase 6.
- Do not change SIR model/data definitions.
- Do not select `N=8`.
- Do not make scale-adaptive Sinkhorn a silent global default.
- Do not relax tolerance without recording it as a reviewed repair parameter.
- Do not claim score/Hessian/theta-gradient/HMC/NUTS evidence.
- Do not claim Zhao-Cui TT/SIRT source-faithfulness or MATLAB parity.
- Do not stage, commit, merge, or push.

## Exact Next-Phase Handoff Conditions

Phase 5 may be rerun only if:

- Phase 5c result identifies a bounded implementation repair;
- focused local tests pass;
- trusted GPU LEDH diagnostics pass or preserve a clear blocker;
- Claude returns `VERDICT: AGREE` on Phase 5c result and the Phase 5 rerun
  subplan.

Phase 6 may begin only after a reviewed Phase 5 rerun selects particle counts,
or the user explicitly narrows the leaderboard to a reviewed subset.

## Stop Conditions

Stop and preserve the blocker if:

- scale-adaptive Sinkhorn fails any full-trajectory LEDH OT smoke;
- the repair requires changing SIR model/data;
- the repair would be a hidden default change rather than an explicit P8j
  repair parameter;
- trusted GPU execution is unavailable;
- Claude review does not converge after five rounds for the same blocker.

## Skeptical Plan Audit

The main risk is converting a one-event scale diagnostic into an algorithmic
success claim.  This plan permits only an explicit, reviewed numerical-stability
repair attempt and requires five-seed full-trajectory evidence before the work
can re-enter Phase 5 tuning.
