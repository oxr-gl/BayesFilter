# Review Bundle: LEDH Memory-Style Score Root-Cause And Repair Plan

Date: 2026-07-09

Role: Claude is read-only reviewer only.  Codex remains supervisor and
executor.  Do not edit files, run commands, launch agents, or authorize
scientific/product boundaries.

## Objective

Review the plan:

`docs/plans/bayesfilter-ledh-memory-style-score-root-cause-and-repair-plan-2026-07-09.md`

The plan responds to a full-scale LEDH score memory blocker.  A previous
shared transport contraction patch removed avoidable 5D temporaries but
`N=10000,T=50` LGSSM score-only still failed the memory gate and emitted no
artifact.  The plan proposes to demote the full forward-sensitivity tangent
score route as historical/diagnostic and use memory-style reverse/VJP score
routes by default where those routes compute the same finite-`N` scalar.

## Key Code Anchors

- LGSSM forward-sensitivity route:
  `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
  `_compact_value_and_score_from_components`.
- LGSSM reverse/VJP route:
  same file, `_manual_value_and_score_from_components` and
  `_manual_transport_vjp_tf`.
- Shared transport JVP still returning full tangents:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  `_filterflow_streaming_transport_from_potentials_jvp`.
- Score contract:
  `bayesfilter/highdim/ledh_score_contract.py`.
- Similar score scripts:
  `docs/benchmarks/benchmark_ledh_same_target_fixed_sir_score.py`,
  `benchmark_ledh_same_target_actual_sv_score.py`,
  `benchmark_ledh_same_target_predator_prey_score.py`,
  `benchmark_ledh_same_target_generalized_sv_score.py`,
  `benchmark_ledh_same_target_ksc_sv_score.py`.

## Evidence Already Observed

- Current compact forward-sensitivity route carries
  `[batch,N,state_dim,param_dim]` particle tangents and
  `[batch,N,param_dim]` weight/potential tangents.
- Trusted GPU `N=10000,T=50` LGSSM score-only attempt exceeded the
  `14000 MiB` reviewed memory budget and emitted no artifact.
- Tiny LGSSM test currently shows compact and reverse/VJP routes match.
- Fixed-SIR already has a prior `N=10000` memory-style score artifact with
  peak about `3166.77 MiB`, but its old route string is historical.

## Review Questions

1. Is the root-cause diagnosis materially correct, or does the plan miss
   another full-tangent score path that must be repaired first?
2. Is the phase ordering sound: contract taxonomy, LGSSM default wiring,
   fixed-SIR reclassification, predator-prey/actual-SV wiring, then
   generalized-SV/KSC derivation gate?
3. Does the plan preserve the same finite-`N` LEDH scalar and avoid exact
   Kalman substitution?
4. Are the evidence contract, vetoes, and stop conditions sufficient to avoid
   claiming score admission from score-only or tiny diagnostics?

Return a concise review ending with exactly one of:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
