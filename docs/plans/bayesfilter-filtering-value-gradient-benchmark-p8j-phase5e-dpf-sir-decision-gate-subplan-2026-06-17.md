# P8j Phase 5e Subplan: DPF SIR Decision Gate

metadata_date: 2026-06-17
status: REVIEWED_READY_TO_EXECUTE
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 5e
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Close the current P8j DPF SIR d18 tuning lane with a decision artifact:

- either preserve DPF SIR cells as blocked for the leaderboard until a separate
  variance-reduction program is approved;
- or request explicit human direction for a new variance-reduction/resampling
  program;
- or, only with explicit human approval, narrow the leaderboard scope.

This phase must not run another blind particle-count ladder.

## Entry Conditions Inherited From Previous Phase

- Bootstrap DPF remains MC-SE-blocked through `N=256`.
- LEDH OT fixed-epsilon nonfinite blocker was repaired by explicit adaptive
  Sinkhorn.
- LEDH OT adaptive `N=16,32,64` is finite and transport-valid but MC-SE-blocked:
  `38.680160007903105`, `41.269063039967556`, `39.529955624675594`.
- LEDH OT adaptive runtime is high: `N=64` took `789.755664` seconds.
- No SIR d18 DPF particle count has been selected.
- Phase 6 leaderboard refresh remains unauthorized.

## Required Artifacts

- Phase 5e result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5e-dpf-sir-decision-gate-result-2026-06-17.md`
- Updated execution ledger, Claude review ledger, and stop handoff.
- Optional new master program only if user explicitly approves a variance-
  reduction program.

## Required Checks/Tests/Reviews

Local checks:

```bash
python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8j or sir_dpf"
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-result-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5e-dpf-sir-decision-gate-subplan-2026-06-17.md
```

Claude review:

- Required before declaring the P8j DPF SIR tuning lane closed or blocked.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Given bootstrap and LEDH OT DPF SIR d18 evidence, what is the safe next decision? |
| Baseline/comparator | Phase 5 through Phase 5d artifacts: bootstrap MC-SE blockers, LEDH OT fixed-epsilon nonfinite repair, adaptive LEDH OT MC-SE/runtime blockers. |
| Primary criterion | Produce a decision record that does not overclaim and states whether the lane is blocked pending human-approved variance reduction or scope change. |
| Veto diagnostics | Launching more blind particle ladders; Phase 6 refresh without selected counts; hidden model/data/default changes; unreviewed leaderboard narrowing; gradient/HMC/source-faithfulness claims. |
| Explanatory diagnostics | MC SE table, runtime table, transport repair status, remaining options. |
| Not concluded | Leaderboard completion; DPF adequacy; gradient/HMC/NUTS readiness; Zhao-Cui TT/SIRT or MATLAB parity; production readiness. |

## Forbidden Claims/Actions

- Do not proceed to Phase 6.
- Do not run additional GPU ladders in this phase.
- Do not change SIR model/data definitions.
- Do not select `N=8`.
- Do not silently change default Sinkhorn behavior.
- Do not claim gradient/HMC/NUTS readiness.
- Do not claim Zhao-Cui TT/SIRT source-faithfulness or MATLAB parity.
- Do not stage, commit, merge, or push.

## Exact Next-Phase Handoff Conditions

The lane may close as blocked if:

- Phase 5e result summarizes the blockers and options;
- local checks pass;
- Claude returns `VERDICT: AGREE`.

Any new execution program requires explicit human approval, especially if it
changes resampling policy, variance reduction, leaderboard scope, or scientific
claims.

## Stop Conditions

Stop and ask for human direction if:

- the decision requires narrowing the leaderboard;
- the decision requires a new variance-reduction/resampling research program;
- Claude review does not converge after five rounds for the same blocker.

## Skeptical Plan Audit

The risk is treating "finite after repair" as "leaderboard-ready."  The
evidence says the opposite: execution is fixed, but estimator variance and
runtime block particle-count selection.  This phase therefore records a
decision instead of launching more runs.
