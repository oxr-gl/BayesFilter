# Review Bundle: Phase 2U Result And Phase 2V Subplan

Date: 2026-07-09

Review role: read-only reviewer. Codex remains supervisor and executor.

## Objective

Review whether Phase 2U is fairly closed as a fixable no-artifact blocker and
whether Phase 2V is a safe, correct next subplan before implementation.

## Artifacts To Inspect

- Phase 2U result:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-phase2u-lgssm-full-run-result-2026-07-09.md`
- Phase 2V subplan:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-phase2v-lgssm-sharded-admission-subplan-2026-07-09.md`
- Master:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-master-program-2026-07-09.md`
- Ledger tail:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-visible-execution-ledger-2026-07-09.md`
- Score validator:
  `bayesfilter/highdim/ledh_score_contract.py`
- LGSSM score runner:
  `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`

## Context Summary

Phase 2S repaired same-scalar FD so FD uses the value-only scalar route instead
of reusing the compact score/JVP route. Phase 2T established a disclosed
precision policy: production TF32 remains enabled, but the FD correctness arm
uses TF32 disabled and records that split. Phase 2U launched the reviewed full
`N=10000,T=50`, five-seed trusted GPU command. It initialized GPU and compiled
XLA, but no JSON score artifact was emitted during the bounded window. The
process was killed and post-kill GPU checks showed no remaining compute app.

The proposed Phase 2V repair is to run exact fixed-seed shards, write durable
raw shard artifacts, then aggregate by the same full-row batch-mean contract.
The aggregate score artifact must still validate with
`validate_ledh_score_artifact(..., require_admitted=True)` against the admitted
LGSSM value artifact.

## Evidence Contract To Check

- The target scalar remains `observed_data_log_likelihood_estimator`, reported
  as `log_likelihood`.
- Full score admission requires compact no-tape provenance and validator
  admission.
- Per-seed sharding is acceptable only if the aggregate score and FD are exactly
  the arithmetic mean over the fixed full-row seeds.
- Segmented execution must be disclosed and must not claim monolithic five-seed
  memory or runtime.
- Partial shards must not be admitted.

## Forbidden Claims Or Actions

- Do not treat Phase 2U as score admission.
- Do not approve changing `N`, `T`, seeds, row id, target scalar, parameter
  order, transport policy, Sinkhorn settings, source value artifact, or
  production precision policy.
- Do not admit historical `manual_total_vjp*`, stopped partials,
  `GradientTape`, or `ForwardAccumulator` evidence.
- Do not proceed to fixed-SIR before LGSSM is admitted or a reviewed LGSSM
  blocker is written.

## Review Questions

1. Does the Phase 2U result accurately close the full-run attempt as
   `BLOCKED_FIXABLE_FULL_RUNTIME_NO_ARTIFACT` without overclaiming?
2. Does Phase 2V include the required subplan fields: objective, entry
   conditions, required artifacts, checks/tests/reviews, evidence contract,
   forbidden claims/actions, exact next-phase handoff conditions, and stop
   conditions?
3. Is seed-sharded aggregation a logically valid next repair, provided the
   implementation proves small-case direct-batch parity and validates the final
   aggregate artifact?
4. Are there material missing tests or boundary risks that must be added before
   Phase 2V implementation?

Return a concise finding list and end with exactly one of:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
