# P83 Phase 5 Subplan: Tiny Source-Route Mechanics Smoke

Date: 2026-06-22

Status: `READY_AFTER_PHASE4_BLOCKER_REVIEW`

## Phase Objective

Run or preserve the smallest CPU-only source-route mechanics smoke that checks
retained-object carry across at least two steps after Phase 4 blocked
derivative readiness.

This phase is mechanics-only.  It must not claim analytical derivative
readiness, d=18 correctness, LEDH agreement, HMC readiness, posterior
correctness, production KR closure, or scaling.

## Entry Conditions Inherited From Previous Phase

Phase 5 may begin only after Phase 4 blocker review agrees that a mechanics-only
handoff is safe.

Inherited boundaries:

- `BLOCK_P83_PHASE4_ANALYTICAL_DERIVATIVE_READINESS` is active;
- FD/JVP/ForwardAccumulator are diagnostic-only and out of scope;
- current numerical CDF-grid route is not production KR closure;
- positive defensive mass and `eval_pdf` proposal semantics remain required;
- no GPU, d=18, LEDH, HMC, fitting ladder, or validation job is authorized.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase5-mechanics-smoke-result-2026-06-22.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md`
- Updated Claude review ledger if material:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md`
- Draft/refreshed Phase 6 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-subplan-2026-06-22.md`

## Required Checks / Tests / Reviews

Skeptical audit before execution.

Focused CPU-only checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p83_minimal_source_route_transport_slice.py \
  tests/highdim/test_p57_m6_sequential_fixed_hmc_source_loop.py \
  -k "two_step or sequential_loop_carries_previous_retained_marginal"

git diff --check -- \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase5-mechanics-smoke-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase5-mechanics-smoke-result-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-phase6-fitting-budget-design-subplan-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-execution-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-claude-review-ledger-2026-06-22.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p83-visible-stop-handoff-2026-06-22.md
```

Review:

- Claude read-only review is required if the result attempts to advance beyond
  mechanics-only interpretation.
- If the test fails because Phase 4 derivative readiness is blocked, revise the
  test selection or result wording; do not patch derivative code in Phase 5.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the tiny source-route mechanics fixture still demonstrate retained-object carry, previous marginal use, finite normalizer increments, `eval_pdf` proposal correction, and honest metadata after Phase 4 blocked derivative readiness? |
| Baseline/comparator | P83-3 tests, P57-M6 sequential fixed-HMC source loop, P83 Phase 4 blocker result. |
| Primary pass criterion | Focused smoke passes and result records derivative readiness as blocked/out of scope. |
| Veto diagnostics | Any analytical derivative, d=18, LEDH, HMC, posterior, production KR, or scaling claim; zero defensive mass accepted for P83 fixture; base-density proposal substitution. |
| Explanatory diagnostics | Focused pytest output and manifest/nonclaim assertions. |
| Not concluded | No derivative readiness, no d=18 correctness, no source-route production correctness, no LEDH readiness, no HMC readiness. |
| Artifact preserving result | Phase 5 result and Phase 6 budget-design subplan. |

## Forbidden Claims / Actions

- Do not edit derivative code.
- Do not run GPU, LEDH, d=18, HMC, fitting ladders, or validation jobs.
- Do not promote the smoke to correctness, scaling, posterior, or production
  readiness.
- Do not claim production KR closure from current grid-CDF metadata.
- Do not use FD/JVP/ForwardAccumulator evidence in this phase.

## Exact Next-Phase Handoff Conditions

P83-6 may begin only if:

- Phase 5 focused mechanics smoke passes;
- Phase 5 result preserves the Phase 4 derivative blocker;
- Phase 6 subplan exists and is fitting-budget design only;
- Phase 6 computes parameter counts and training-sample minimums before any
  fitting run;
- no d=18 validation, LEDH comparison, HMC claim, or production claim appears.

## Stop Conditions

Stop with a Phase 5 blocker result if:

- retained-object carry or previous marginal evidence fails;
- proposal correction can only pass through base/reference density;
- metadata drops `production_kr_closure=False` or P83 nonclaims;
- the mechanics fixture requires derivative readiness;
- a fix would require code edits outside the mechanics smoke scope.
