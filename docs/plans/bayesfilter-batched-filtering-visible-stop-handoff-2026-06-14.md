# Batched Filtering Visible Stop Handoff

Date: 2026-06-14

## Final Phase Reached

Phase 6: Default-readiness decision.

## Final Status

`FILTERING_PRODUCTION_CANDIDATE_READY_FOR_FILTER_LANE_REVIEW`

The batched filtering value+score work is ready to promote from experimental
evidence to filtering production-candidate review for the tested Kalman and
SVD-UKF scopes.  It is not yet an unconditional default across all filtering
workloads.

## Main Decision

- Correction: the earlier HMC/static-unroll downstream test was a consumer test,
  not a filtering test.  It is removed from the filtering promotion gate.
- Kalman batched value+score is a filtering production candidate for the tested
  dense fixtures.
- SVD-UKF batched value+score is a filtering production candidate for the tested
  parity/nonlinear/JIT benchmark fixtures.
- No unconditional default, public export change, HMC/NeuTra readiness,
  posterior-validity, broad model-coverage, speed-ranking, or CUT4 readiness
  claim is made.

## Result Artifacts

- Master program:
  `docs/plans/bayesfilter-batched-filtering-production-default-master-program-2026-06-14.md`
- Visible runbook:
  `docs/plans/bayesfilter-batched-filtering-visible-gated-execution-runbook-2026-06-14.md`
- Execution ledger:
  `docs/plans/bayesfilter-batched-filtering-visible-execution-ledger-2026-06-14.md`
- Phase 6 subplan:
  `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-subplan-2026-06-14.md`
- Phase 6 result:
  `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-result-2026-06-14.md`

## Claude Review Trail

- Master/Phase 0 review:
  `docs/plans/bayesfilter-batched-filtering-claude-review-round-01-2026-06-14.md`
  and `docs/plans/bayesfilter-batched-filtering-claude-review-round-02-2026-06-14.md`
- Phase 1 review:
  `docs/plans/bayesfilter-batched-filtering-phase-1-claude-review-round-01-2026-06-14.md`
  and `docs/plans/bayesfilter-batched-filtering-phase-1-claude-review-round-02-2026-06-14.md`
- Phase 2 review:
  `docs/plans/bayesfilter-batched-filtering-phase-2-claude-review-round-01-2026-06-14.md`
  through `docs/plans/bayesfilter-batched-filtering-phase-2-claude-review-round-03-2026-06-14.md`
- Phase 3 review:
  `docs/plans/bayesfilter-batched-filtering-phase-3-claude-review-round-01-2026-06-14.md`
  and `docs/plans/bayesfilter-batched-filtering-phase-3-claude-review-round-02-2026-06-14.md`
- Phase 4 review:
  `docs/plans/bayesfilter-batched-filtering-phase-4-claude-review-round-01-2026-06-14.md`
  and `docs/plans/bayesfilter-batched-filtering-phase-4-claude-review-round-02-2026-06-14.md`
- Phase 5 review, now treated as historical consumer-boundary evidence and not
  as a filtering promotion gate:
  `docs/plans/bayesfilter-batched-filtering-phase-5-claude-review-round-01-2026-06-14.md`
  and `docs/plans/bayesfilter-batched-filtering-phase-5-claude-review-round-02-2026-06-14.md`
- Phase 6 subplan review:
  `docs/plans/bayesfilter-batched-filtering-phase-6-claude-review-round-01-2026-06-14.md`
  and `docs/plans/bayesfilter-batched-filtering-phase-6-claude-review-round-02-2026-06-14.md`
- Phase 6 result review:
  `docs/plans/bayesfilter-batched-filtering-phase-6-result-claude-review-round-01-2026-06-14.md`
  and `docs/plans/bayesfilter-batched-filtering-phase-6-result-claude-review-round-02-2026-06-14.md`

The earlier Phase 6 result review agreed with the over-scoped downstream/HMC
framing.  That framing is superseded by the filtering-lane correction in the
Phase 6 result.

## Tests And Checks Actually Run In Final Phase

Passed:

- Batched implementation/interface subset:
  `40 passed` for
  `tests/test_experimental_batched_value_score_interface.py`,
  `tests/test_experimental_batched_benchmark_harness.py`,
  `tests/test_experimental_batched_linear_kalman_tf.py`,
  `tests/test_experimental_batched_svd_sigma_point_tf.py`, and
  `tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py`.
- Experimental export scan:
  empty output for experimental batched module names in
  `bayesfilter/__init__.py`, `bayesfilter/linear/__init__.py`, and
  `bayesfilter/nonlinear/__init__.py`.
- GPU JSON validation:
  six batched GPU artifacts record `jit_compile: true`, finite outputs, and
  value/score placement on `GPU:0`.

Excluded from filtering gate:

- `tests/test_experimental_batched_downstream_value_score_harness.py` was an
  HMC/static-unroll consumer-boundary test.  It was removed from this filtering
  work and should not be used to promote or block filtering.
- Public package/HMC import checks are not filtering correctness checks.

## Benchmark Headlines

All GPU timing evidence below is descriptive, JIT/XLA compiled, and
trusted-context device-placed.  It is not a statistical ranking.

| Kernel | B | GPU warm median seconds | Per-filter GPU warm median seconds |
| --- | ---: | ---: | ---: |
| Kalman | 20 | 0.04977 | 0.002489 |
| Kalman | 256 | 0.1388 | 0.000542 |
| Kalman | 4096 | 1.6320 | 0.000398 |
| SVD-UKF | 20 | 0.3735 | 0.01868 |
| SVD-UKF | 256 | 0.7836 | 0.003061 |
| SVD-UKF | 4096 | 7.7604 | 0.001895 |

## Unresolved Blockers And Gaps

- No human approval for filtering public export or production default change.
- Current evidence is working-tree-scoped and not release-snapshot reproducible.
- Scalar SVD compiled-loop comparator remains XLA TraceType-infeasible at the
  current wrapper boundary.
- Broader model coverage, production docs, CI-sized benchmarks, and maintenance
  policy remain missing.

## Next Human Decision Required

Decide whether to authorize a filtering productionization program: public
API/export shape, default policy, CI coverage, docs, broader filtering fixtures,
and release-snapshot cleanup.  HMC/NeuTra validation should stay in separate
consumer-lane plans.
