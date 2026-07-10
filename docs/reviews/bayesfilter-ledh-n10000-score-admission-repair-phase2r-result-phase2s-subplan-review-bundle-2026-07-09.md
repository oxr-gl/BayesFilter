# Review Bundle: Phase 2R Result And Phase 2S LGSSM Score Procedure Repair

Date: 2026-07-09

Reviewer role: read-only. Codex remains supervisor and executor.

## Objective

Review whether Phase 2R is fairly closed as a fixable no-artifact runtime
blocker, and whether Phase 2S is the right next repair before code edits or
another full `N=10000,T=50` LGSSM run.

## Artifacts Under Review

- Phase 2R result:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-phase2r-lgssm-memory-repair-result-2026-07-09.md`
- Phase 2S subplan:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-phase2s-lgssm-score-procedure-repair-subplan-2026-07-09.md`
- Runner source anchors:
  `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
  - `_compact_forward_transport_jvp_tf`
  - `_compact_value_and_score_from_components`
  - `_manual_score_diagnostic`
  - `_lgssm_score_artifact_from_result`
- Transport source anchors:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  - `_filterflow_streaming_softmin_jvp`
  - `_filterflow_streaming_column_log_normalizer_jvp`
  - `_filterflow_streaming_transport_from_potentials_jvp`
  - `_filterflow_manual_streaming_finite_transport_value_and_jvp_total`

## Key Evidence

Phase 2R smaller chunks:

- trusted GPU/XLA log exists at
  `docs/plans/logs/bayesfilter-ledh-n10000-score-admission-repair-phase2r-lgssm-smaller-chunks-2026-07-09.log`;
- log confirms RTX 4080 SUPER GPU device, CUDA XLA, cuDNN, and XLA compile;
- intended JSON artifact is absent;
- no score was admitted.

Code inspection findings motivating Phase 2S:

- `_manual_score_diagnostic` computes compact score, then coordinate-wise FD.
- Its `value_at` currently calls `_compact_value_and_score_from_components`,
  so each plus/minus FD recomputes the full score/JVP route rather than a
  value-only scalar.
- `_lgssm_score_artifact_from_result` uses `gpu_memory_info_after`, which the
  runner measures around the value route before score diagnostic execution.
  That is not a score-specific memory gate.

## Review Questions

1. Does Phase 2R correctly stop without admitting LGSSM score?
2. Is Phase 2S scoped to the smallest procedural fixes before another full
   `N=10000,T=50` run?
3. Does Phase 2S preserve the target scalar, admitted value artifact, row id,
   seeds, `N`, `T`, theta coordinate system, and parameter order?
4. Are the required checks enough to catch the two identified procedural bugs:
   FD using the score route, and score memory measured only around value?
5. Is there any boundary violation, unsupported claim, or missing stop
   condition?

## Pass/Block Criteria

Return `VERDICT: AGREE` only if the Phase 2S subplan is safe and sufficient as
the next repair phase.

Return `VERDICT: REVISE` if the plan should be patched before code edits.

## Forbidden Nonclaims

Do not claim:

- LGSSM score is admitted;
- compact score mathematics is proven wrong;
- full leaderboard score computation is complete;
- HMC readiness, posterior correctness, exact Kalman score equality, runtime
  ranking, scientific superiority, or non-LGSSM score admission.

End with exactly one verdict line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
