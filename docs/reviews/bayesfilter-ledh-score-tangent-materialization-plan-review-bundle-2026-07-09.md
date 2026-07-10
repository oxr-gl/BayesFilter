# Claude Review Bundle: LEDH Score Tangent-Materialization Repair Plan

Date: 2026-07-09

## Role Contract

Claude is read-only reviewer only. Codex remains supervisor and executor.
Claude must not edit files, run commands, authorize boundaries, or make
scientific/admission claims.

## Objective

Review this plan for consistency, correctness, feasibility, artifact coverage,
and boundary safety:

`docs/plans/bayesfilter-ledh-score-tangent-materialization-root-cause-repair-plan-2026-07-09.md`

## Packet Summary

The remaining blocker is not the old 5D broadcast temporary pattern alone.
Source tests already reject the old `d_weighted`/`d_diff` broadcast patterns in
`tests/test_ledh_compact_transport_jvp.py`. The remaining compact route issue is
that `_filterflow_streaming_transport_from_potentials_jvp` in
`experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
returns `d_transported` with shape roughly `[batch,N,state_dim,param_dim]`, and
compact score loops carry this full tangent state.

The proposed plan:

- treats compact forward-sensitivity routes as historical/diagnostic for full
  score admission;
- preserves same finite-`N` LEDH `observed_data_log_likelihood_estimator`;
- makes memory-style reverse/VJP route IDs admissible only when model-specific
  code exists and correctness/memory gates pass;
- wires predator-prey and actual-SV default wrappers to their existing manual
  reverse/VJP routes;
- reclassifies fixed-SIR via a new memory-style route ID rather than promoting
  old `manual_total_vjp*` artifacts;
- keeps generalized-SV and KSC blocked from full admission until reviewed
  memory-style derivations exist;
- does not claim full leaderboard admission from unit tests or score-only rungs.

## Key Anchors

- Shared contract:
  `bayesfilter/highdim/ledh_score_contract.py`
- Shared transport JVP:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- LGSSM runner:
  `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
- Fixed-SIR runner:
  `docs/benchmarks/benchmark_ledh_same_target_fixed_sir_score.py`
- Predator-prey runner:
  `docs/benchmarks/benchmark_ledh_same_target_predator_prey_score.py`
- Actual-SV runner:
  `docs/benchmarks/benchmark_ledh_same_target_actual_sv_score.py`
- Generalized-SV runner:
  `docs/benchmarks/benchmark_ledh_same_target_generalized_sv_score.py`
- KSC-SV runner:
  `docs/benchmarks/benchmark_ledh_same_target_ksc_sv_score.py`

## Review Questions

1. Does the plan correctly distinguish the already-repaired old 5D broadcast
   temporaries from the remaining full `[B,N,D,P]` tangent carry?
2. Does the phase sequence avoid admitting compact forward-sensitivity or old
   historical `manual_total_vjp*` route strings as production score evidence?
3. Is it feasible and boundary-safe to first wire predator-prey and actual-SV
   wrappers to existing manual reverse/VJP routes, while leaving
   generalized-SV/KSC blocked?
4. Are the evidence contract, forbidden claims/actions, and stop conditions
   sufficient to avoid another planning/procedural false pass?

## Required Verdict

End with exactly one of:

`VERDICT: AGREE`

or

`VERDICT: REVISE`

If revising, list only material blockers that must be fixed before execution.
