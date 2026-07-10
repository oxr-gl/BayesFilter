# Review Bundle: Phase 2W Result And Phase 2X Subplan

Date: 2026-07-09

Review role: read-only reviewer. Codex remains supervisor and executor.

## Objective

Review whether Phase 2W is fairly closed as
`BLOCKED_FIXABLE_COMPACT_SCORE_PASS_FULL_RUNTIME_NO_ARTIFACT` and whether
Phase 2X is a safe next subplan before compact score kernel repair.

## Artifacts To Inspect

- Phase 2W result:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-phase2w-lgssm-score-fd-split-result-2026-07-09.md`
- Phase 2X subplan:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-phase2x-lgssm-compact-score-kernel-repair-subplan-2026-07-09.md`
- Ledger:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-visible-execution-ledger-2026-07-09.md`
- LGSSM runner:
  `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
- Transport JVP:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- Score validator:
  `bayesfilter/highdim/ledh_score_contract.py`

## Context Summary

Phase 2W split score-only and FD-only diagnostics. Local tests passed, trusted
GPU `N=256,T=3` score-only smoke passed, and trusted GPU `N=256,T=3` FD-only
smoke passed. The full trusted GPU score-only shard for seed `81120` at
`N=10000,T=50` initialized GPU and compiled XLA, but emitted no artifact after
about 6.75 minutes. This narrows the blocker to the full-scale compact
forward-sensitivity score pass itself.

The likely kernel surfaces are the transport JVP functions that stack tangent
blocks:

- `_filterflow_streaming_softmin_jvp`;
- `_filterflow_streaming_column_log_normalizer_jvp`;
- `_filterflow_streaming_transport_from_potentials_jvp`.

## Evidence Contract To Check

- Target scalar remains `observed_data_log_likelihood_estimator` /
  `log_likelihood`.
- Full admission still requires
  `validate_ledh_score_artifact(..., require_admitted=True)`.
- Phase 2X may repair tensor lifetime or add a reduced compact score path, but
  must match the current compact score on tiny deterministic cases before full
  use.
- No exact-Kalman substitution, target drift, `GradientTape`,
  `ForwardAccumulator`, stopped partials, or historical `manual_total_vjp*`
  evidence may be used.
- Score-only artifacts remain diagnostic, not admission.

## Review Questions

1. Does Phase 2W fairly close the score/FD split attempt without overclaiming?
2. Does Phase 2X include all required subplan fields?
3. Is compact score kernel/tensor-lifetime repair the correct next dependency?
4. Are there material missing tests, artifacts, or boundary risks before
   implementation?

Return concise findings and end with exactly one of:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
