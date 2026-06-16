# P71 Phase 4 Subplan: Same-Route Rank And Degree Ladder

metadata_date: 2026-06-16
status: DRAFT_PENDING_PHASE3_RESULT
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 4

## Phase Objective

Run a predeclared same-route rank/degree ladder that tests whether the d18
fixed branch is structurally stable enough to be considered for accuracy
validation.

## Entry Conditions Inherited From Previous Phase

- Phase 3 passed finite numeric evaluator/value checks.
- Phase 3 preserved branch identity and nonclaims.

## Required Artifacts

- Phase 4 result note.
- Machine-readable rank/degree ladder artifact.
- Comparison-invariant ledger showing only authorized rank or degree changes.
- Frozen-threshold table copied into the result before execution.
- Refreshed Phase 5 accuracy/reference subplan.

## Required Checks/Tests/Reviews

- Run or extend existing P60/P66/P67/P69/P70 rank/degree diagnostics only under
  a frozen evidence contract.
- Run focused pytest for rank comparator and validation-ladder schema if code
  changes are made.
- `git diff --check` over artifacts.
- Claude read-only review of ladder thresholds and result interpretation.

## Frozen Thresholds

These thresholds are hypotheses for the first reviewed P71 ladder and must be
recorded before execution.  A later phase may revise them only by writing a new
reviewed subplan before seeing new ladder output.

| Quantity | Threshold | Source |
| --- | ---: | --- |
| log marginal absolute delta | 5.0 | `scripts/p67_author_sir_adjacent_ladder_diagnostics.py` |
| normalizer increment absolute delta | 5.0 | `scripts/p67_author_sir_adjacent_ladder_diagnostics.py` |
| probe log-density median absolute delta | 10.0 | `scripts/p67_author_sir_adjacent_ladder_diagnostics.py` |
| retained log-density median absolute delta | 10.0 | `scripts/p67_author_sir_adjacent_ladder_diagnostics.py` |
| condition-number warning | 1e10 | `bayesfilter/highdim/source_route.py` `P70_CONDITION_NUMBER_WARNING` |
| condition-number veto | 1e14 | `bayesfilter/highdim/source_route.py` `P70_CONDITION_NUMBER_VETO` |
| channel activity absolute tolerance | 1e-12 | `bayesfilter/highdim/source_route.py` `P70_CHANNEL_ACTIVITY_ABS_TOL` |
| channel activity relative tolerance | 1e-8 | `bayesfilter/highdim/source_route.py` `P70_CHANNEL_ACTIVITY_REL_TOL` |
| defensive-only sqrt-normalizer tolerance | 1e-14 | `bayesfilter/highdim/source_route.py` `P70_DEFENSIVE_ONLY_SQRT_NORMALIZER_TOL` |
| fit mass fraction minimum | 1e-6 | `bayesfilter/highdim/source_route.py` `P70_FIT_MASS_FRACTION_MIN` |
| log increment absolute bound | 1e6 | `bayesfilter/highdim/source_route.py` `P70_LOG_INCREMENT_ABS_BOUND` |
| holdout/replay normalized residual veto | 10.0 | `bayesfilter/highdim/source_route.py` `P70_HOLDOUT_REPLAY_NORMALIZED_RESIDUAL_VETO` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the same source-route branch remain stable under adjacent rank and degree changes without hidden source-route drift? |
| Baseline/comparator | Phase 3 admitted candidate branch, adjacent rank candidate, and adjacent degree candidate; authorized differences are `fit_rank` or `fit_degree` only. |
| Primary criterion | Predeclared rank/degree ladder passes source invariants, finite normalizers, the frozen bounded-delta thresholds above, non-defensive-only transport, channel activity, and condition diagnostics. |
| Veto diagnostics | Source-route invariant drift, branch identity drift outside authorized field, defensive-only transport, rank-channel collapse, nonfinite normalizers, or thresholds changed after output. |
| Explanatory diagnostics | Log-marginal deltas, normalizer increments, ESS, condition numbers, channel norms, holdout/replay residuals. |
| Not concluded | No filtering accuracy, no d50/d100 scaling, no HMC readiness. |
| Artifact | Phase 4 result note and ladder artifact. |

## Forbidden Claims/Actions

- Do not use low/high closeness alone as correctness.
- Do not promote degree/rank by in-sample fit residual alone.
- Do not hide condition-number vetoes.
- Do not run accuracy gates until the structural gate passes.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if the ladder passes all veto diagnostics and records a
single admitted d18 configuration for reference comparison.

## Stop Conditions

Stop if adjacent ladders are unstable under the frozen thresholds,
condition-vetoed, defensive-only, or source-route drifting.
