# Read-Only Review Bundle: LEDH Phase 1R Transport VJP Memory Repair

Review name:
`bayesfilter-ledh-memory-style-score-phase1r-transport-vjp-memory-repair`

## Role Contract

Claude is a read-only reviewer only. Claude must not edit files, run commands,
launch agents, approve policy/scientific boundaries, or authorize admission.
Codex remains supervisor and executor.

## Objective

Review whether the Phase 1R subplan is a correct, feasible, and boundary-safe
next step after the LGSSM memory-style score route was wired by default but the
trusted GPU `N=1000,T=10` score-only rung exceeded memory/no-artifact.

## Files To Review

Primary plan:

- `docs/plans/bayesfilter-ledh-memory-style-score-phase1r-transport-vjp-memory-repair-subplan-2026-07-09.md`

Context/result:

- `docs/plans/bayesfilter-ledh-memory-style-score-phase1-lgssm-default-wiring-result-2026-07-09.md`

Relevant code surfaces:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  - `_filterflow_streaming_softmin_vjp`
  - `_filterflow_streaming_transport_from_potentials_vjp`
  - `_scatter_axis1_add_2d`
  - `_scatter_axis1_add_3d`
  - `_filterflow_manual_streaming_finite_transport_total_pullback`
- `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
  - `_manual_value_and_score_from_components`
  - `_manual_transport_vjp_tf`
  - `_compact_value_and_score_from_components`

## Current Evidence Summary

- Focused CPU-hidden tests after Phase 1 default wiring:
  `57 passed, 2 warnings`.
- Broader CPU-hidden score/contract tests:
  `117 passed, 2 warnings`.
- Trusted GPU `N=256,T=3` score-only emitted:
  `docs/plans/artifacts/ledh-memory-style-score-phase1-lgssm-score-only-n256-t3-2026-07-09.json`
  with:
  - `score_derivative_provenance =
    memory_style_reverse_vjp_no_autodiff_same_scalar_lgssm_ledh_pfpf_ot`
  - `score_execution_style =
    memory_style_reverse_vjp_no_particle_param_axis`
- Trusted GPU `N=1000,T=10` score-only with the memory-style route exceeded
  the `14000 MiB` budget and emitted no artifact. The interrupted stack reached
  `_filterflow_streaming_softmin_vjp` / `_scatter_axis1_add_3d` from the total
  transport pullback.

## Review Questions

1. Does the Phase 1R subplan correctly distinguish the old compact
   forward-sensitivity issue from the remaining reverse/VJP transport-pullback
   memory issue?
2. Is targeting `_filterflow_streaming_softmin_vjp` and
   `_filterflow_streaming_transport_from_potentials_vjp` before LGSSM
   flow-history checkpointing a reasonable sequence given the interrupted
   stack?
3. Does the plan preserve the same finite-`N` LEDH scalar and avoid exact
   Kalman substitution, stopped partials, production autodiff, seed changes, or
   admission from score-only diagnostics?
4. Are the required tests, GPU rungs, evidence contract, stop conditions, and
   next-phase handoff conditions sufficient?
5. Is any material blocker missing that should be patched before
   implementation?

## Required Verdict

Return `VERDICT: AGREE` only if no material blocker remains. Return
`VERDICT: REVISE` if the plan must be patched before implementation.
