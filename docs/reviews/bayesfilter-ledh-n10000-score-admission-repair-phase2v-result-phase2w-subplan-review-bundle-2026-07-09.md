# Review Bundle: Phase 2V Result And Phase 2W Subplan

Date: 2026-07-09

Review role: read-only reviewer. Codex remains supervisor and executor.

## Objective

Review whether Phase 2V is fairly closed as
`BLOCKED_FIXABLE_SINGLE_SHARD_FULL_RUNTIME_NO_ARTIFACT` and whether Phase 2W is
a safe next subplan before implementation.

## Artifacts To Inspect

- Phase 2V result:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-phase2v-lgssm-sharded-admission-result-2026-07-09.md`
- Phase 2W subplan:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-phase2w-lgssm-score-fd-split-subplan-2026-07-09.md`
- Ledger:
  `docs/plans/bayesfilter-ledh-n10000-score-admission-repair-visible-execution-ledger-2026-07-09.md`
- LGSSM runner:
  `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
- Score validator:
  `bayesfilter/highdim/ledh_score_contract.py`

## Context Summary

Phase 2V implemented exact seed-sharded aggregation and passed local tests,
synthetic aggregation smoke, and trusted GPU `N=256,T=3` shard smoke. The first
full trusted GPU shard for seed `81120` at `N=10000,T=50` initialized GPU and
compiled XLA, but emitted no raw shard artifact after about six minutes. It was
stopped and GPU memory was released.

Phase 2W proposes splitting full-shard score computation from finite-difference
correctness so a score-only artifact can be emitted immediately after compact
score completion. FD-only correctness remains separate. No score-only or FD-only
artifact may be admitted.

## Evidence Contract To Check

- Target scalar remains `observed_data_log_likelihood_estimator` /
  `log_likelihood`.
- Full admission still requires
  `validate_ledh_score_artifact(..., require_admitted=True)`.
- Score-only emission is diagnostic only and cannot be admitted.
- FD-only must use the value-only scalar route and must not call compact
  score/JVP.
- No `GradientTape`, `ForwardAccumulator`, stopped partials, or historical
  `manual_total_vjp*` evidence can be used for admission.
- Phase 2W must not silently authorize moving to fixed-SIR.

## Review Questions

1. Does Phase 2V fairly close the sharded attempt without overclaiming?
2. Does Phase 2W include all required subplan fields?
3. Is score/FD splitting the smallest logical next diagnostic after one full
   shard failed to emit?
4. Are there material missing tests or boundary risks before implementation?

Return concise findings and end with exactly one of:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
