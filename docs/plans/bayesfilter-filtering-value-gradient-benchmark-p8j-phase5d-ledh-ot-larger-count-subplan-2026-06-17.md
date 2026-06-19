# P8j Phase 5d Subplan: LEDH OT Larger-Count Feasibility

metadata_date: 2026-06-17
status: EXECUTED_PENDING_PHASE5D_RESULT_AND_PHASE5E_SUBPLAN_REVIEW
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 5d
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Determine whether the Phase 5c explicit scale-adaptive Sinkhorn repair can
produce a usable LEDH OT SIR d18 particle-count ladder at larger counts without
exceeding runtime budget or claim boundaries.

## Entry Conditions Inherited From Previous Phase

- Phase 5 selected no SIR d18 particle count.
- Phase 5b preserved bootstrap MC-SE blocker at `N=128,256`.
- Phase 5c repaired the LEDH OT Sinkhorn nonfinite blocker for `N=16,32`.
- Phase 5c LEDH OT `N=16,32` remained blocked by MC SE:
  `38.680160007903105` and `41.269063039967556`.
- Phase 6 leaderboard refresh remains unauthorized.

## Required Artifacts

- Phase 5d result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-result-2026-06-17.md`
- Optional larger-count JSON/CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-2026-06-17.json`
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-2026-06-17.csv`
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-selected-blocked-2026-06-17.csv`
- Updated execution ledger, Claude review ledger, and stop handoff.
- A refreshed Phase 5 rerun subplan only if Phase 5d identifies a safe ladder.

## Required Checks/Tests/Reviews

Before GPU diagnostics:

```bash
python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "p8j or sir_dpf"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5c-scale-adaptive-sinkhorn-repair-result-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5d-ledh-ot-larger-count-subplan-2026-06-17.md
```

GPU diagnostics:

- Use trusted/escalated GPU.
- Use exactly the five fixed seeds `81120,81121,81122,81123,81124`.
- Use explicit `--p8j-sinkhorn-epsilon-policy cost_mean_max_nominal`.
- Start with `N=64,128` only if runtime projection is acceptable; otherwise
  run a narrower one-rung runtime probe and preserve a runtime blocker.

Claude review:

- Required before any Phase 5 rerun or Phase 6 draft.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can larger adaptive LEDH OT particle counts pass MC SE and adjacent-rung gates for SIR d18 within runtime budget? |
| Baseline/comparator | Phase 5c adaptive `N=16,32` finite but MC-SE-blocked rungs; Phase 5 fixed-epsilon nonfinite rungs. |
| Primary criterion | Either select no count and preserve exact blocker, or identify a reviewed larger-count ladder suitable for Phase 5 rerun. |
| Veto diagnostics | Nonfinite trajectory; invalid transport metadata; untrusted GPU; fewer than five seeds; `N=8`; runtime budget excess; hidden model/data/default changes; leaderboard/gradient/HMC/source-faithfulness claims. |
| Explanatory diagnostics | MC SE, adjacent-rung deltas, runtime, ESS, effective epsilon/cost scale, Sinkhorn residuals. |
| Not concluded | Particle adequacy until Phase 5 rerun passes; leaderboard completion; DPF gradients; HMC/NUTS; Zhao-Cui TT/SIRT or MATLAB parity; production readiness. |

## Forbidden Claims/Actions

- Do not proceed to Phase 6.
- Do not change SIR model/data definitions.
- Do not select `N=8`.
- Do not silently change default Sinkhorn behavior.
- Do not claim gradient/HMC/NUTS readiness.
- Do not claim Zhao-Cui TT/SIRT source-faithfulness or MATLAB parity.
- Do not stage, commit, merge, or push.

## Exact Next-Phase Handoff Conditions

Phase 5 rerun may be drafted only if:

- Phase 5d result has reviewed larger-count evidence or a clear narrowed
  blocker;
- local checks pass;
- Claude returns `VERDICT: AGREE`.

Phase 6 remains blocked until a reviewed Phase 5 rerun selects particle counts
or the user explicitly narrows the leaderboard scope.

## Stop Conditions

Stop and preserve a blocker if:

- larger counts remain MC-SE-blocked;
- runtime exceeds or clearly projects beyond budget;
- transport diagnostics fail;
- trusted GPU execution is unavailable;
- Claude review does not converge after five rounds for the same blocker.

## Skeptical Plan Audit

The risk is spending GPU time chasing MC SE without evidence that variance is
falling.  This phase should therefore start with the smallest larger adjacent
ladder that can discriminate MC-SE trend and runtime feasibility.
