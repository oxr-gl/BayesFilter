# P71 Phase 4d Subplan: Post-Stability-Repair Rank/Degree Ladder Rerun

metadata_date: 2026-06-16
status: DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 4d
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Rerun the previously blocked P71 Phase 4 same-route rank/degree structural
ladder after the Phase 4c objective-preserving scaled ALS implementation was
locally checked and accepted by Claude R2.  This phase tests whether the
engineering stabilization allows the predeclared d18 structural ladder to
execute under the same rank, degree, fit-budget, threshold, source-route, and
claim-boundary rules.

Phase 4d is a structural gate only.  It is not a filtering accuracy gate and
cannot launch Phase 5 unless the exact handoff conditions below are met.

## Entry Conditions Inherited From Previous Phase

- P71 Phase 4 result status is `BLOCKED_CLAUDE_REVIEW_AGREE` because every
  predeclared row hit `CONDITION_NUMBER_VETO` and no d18 configuration was
  admitted.
- P71 Phase 4b repair design was accepted by Claude and selected
  objective-preserving column-scaled weighted ridge ALS.
- P71 Phase 4c implementation passed focused local checks and Claude R2
  returned `VERDICT: AGREE`.
- Phase 4c did not rerun the full structural ladder and made no d18 accuracy,
  rank/degree convergence, scaling, HMC readiness, or Zhao-Cui
  source-faithfulness claim for the numerical stabilization.
- Phase 5 remains blocked until Phase 4d admits exactly one d18 configuration
  and writes/reviews the Phase 4d result.

## Required Artifacts

- Machine-readable rerun artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-2026-06-16.json`
- Phase 4d result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-result-2026-06-16.md`
- Updated visible execution ledger and Claude review ledger.
- If, and only if, Phase 4d admits exactly one d18 configuration, a refreshed
  Phase 5 filtering-accuracy/reference-gate subplan.
- If Phase 4d blocks or admits zero/multiple configurations, a blocker result
  and no Phase 5 refresh except a blocked handoff note.

## Required Checks/Tests/Reviews

Before execution:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-runbook-claude-review-ledger-2026-06-16.md
rg -n "base_candidate_1_2_fit16|rank_candidate_1_2_fit36|rank_stronger_1_3_fit36|degree_candidate_1_2_fit24|degree_stronger_2_2_fit24|condition-number veto|exactly one d18 configuration|Phase 5 remains blocked|CUDA_VISIBLE_DEVICES=-1" docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-subplan-2026-06-16.md scripts/p67_author_sir_adjacent_ladder_diagnostics.py
```

Execution command, CPU-only by design:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p67_author_sir_adjacent_ladder_diagnostics.py --output docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-2026-06-16.json
```

After execution:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-2026-06-16.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p71_phase4d_validate_ladder_artifact.py --artifact docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-2026-06-16.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p67_author_sir_adjacent_ladder_diagnostics.py scripts/p71_phase4d_validate_ladder_artifact.py bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_p59_author_sir_step_spec_assembly.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_fit.py tests/highdim/test_p59_author_sir_step_spec_assembly.py::test_p67_failed_fit_row_payload_preserves_p70_diagnostics
git diff --check -- scripts/p67_author_sir_adjacent_ladder_diagnostics.py scripts/p71_phase4d_validate_ladder_artifact.py bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_p59_author_sir_step_spec_assembly.py docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-result-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4d-post-stability-repair-rank-degree-ladder-rerun-2026-06-16.json docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-runbook-claude-review-ledger-2026-06-16.md
```

Claude read-only review is required after the Phase 4d result note is written.
Do not start Phase 5 until Claude review agrees with the Phase 4d result and
the exact handoff conditions are satisfied.

## Frozen Row Specs

Phase 4d must use the existing row specs from
`scripts/p67_author_sir_adjacent_ladder_diagnostics.py`:

| Row | Degree | Rank | Fit sample count |
| --- | ---: | ---: | ---: |
| `base_candidate_1_2_fit16` | 1 | 2 | 16 |
| `rank_candidate_1_2_fit36` | 1 | 2 | 36 |
| `rank_stronger_1_3_fit36` | 1 | 3 | 36 |
| `degree_candidate_1_2_fit24` | 1 | 2 | 24 |
| `degree_stronger_2_2_fit24` | 2 | 2 | 24 |

## Frozen Thresholds

These thresholds are carried from the original Phase 4 subplan and must not be
changed in Phase 4d:

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
| Question | After the objective-preserving scaled ALS implementation, does the same source-route d18 branch remain stable under the predeclared adjacent rank and degree ladder without hidden source-route drift? |
| Baseline/comparator | Original blocked Phase 4 artifact, Phase 3 finite-value candidate branch, Phase 2 execution-only row-adequacy boundary, and the same five P67 row specs. Authorized row differences remain `fit_rank`, `fit_degree`, and predeclared `fit_sample_count` only. |
| Primary criterion | The rerun artifact passes source invariants, finite normalizers, frozen bounded-delta thresholds, non-defensive-only transport, channel activity, transformed condition diagnostics under unchanged warning/veto thresholds, holdout/replay diagnostics, and records exactly one admitted d18 configuration. |
| Veto diagnostics | Source-route invariant drift, unauthorized rank/degree/row/sweep/initializer/threshold change, defensive-only transport, rank-channel collapse, nonfinite normalizers, condition-number warning/veto, failed fit, multiple/no admitted configurations, row-adequacy misuse, or thresholds changed after output. |
| Explanatory diagnostics | Log-marginal deltas, normalizer increments, ESS, transformed and original condition summaries, column-scale summaries, ridge-metric summaries, channel norms, holdout/replay residuals, and P60 sentinel status. |
| Not concluded | No filtering accuracy, no same-route rank/degree convergence beyond this structural gate, no d50/d100 scaling, no HMC readiness, no adaptive Zhao-Cui parity, and no author-code failure claim. |
| Artifact | Phase 4d JSON artifact and Phase 4d result note. |

## Exact Next-Phase Handoff Conditions

Phase 5 may be drafted and reviewed only if all are true:

- Phase 4d execution artifact is valid JSON and records the frozen row specs.
- The Phase 4d artifact validation passes and records exactly one admitted d18
  configuration.
- The admitted configuration passes all Phase 4d veto diagnostics.
- Failed or non-admitted rows are preserved as diagnostics, not hidden.
- Claude read-only review of the Phase 4d result returns `VERDICT: AGREE`.

If any condition fails, write a Phase 4d blocker result and stop.  Phase 5
remains blocked.

## Forbidden Claims/Actions

- Do not launch Phase 5 from this subplan.
- Do not change thresholds, fit row counts, rank specs, degree specs, sweep
  order, initializer, target, or source-route semantics.
- Do not treat same-route closeness as filtering accuracy.
- Do not treat in-sample fit residuals as rank/degree promotion evidence.
- Do not hide condition-number vetoes or failed fits.
- Do not claim d18 accuracy, five-seed robustness, scaling, HMC readiness, or
  Zhao-Cui source-faithfulness for the numerical stabilization.

## Stop Conditions

Stop and write a blocker result if:

- the rerun command fails or emits invalid JSON;
- any row changes outside the frozen row specs;
- all rows remain condition-vetoed or failed;
- no configuration is admitted;
- multiple configurations are admitted;
- the ladder passes only by threshold drift, route drift, defensive-only
  transport, or row-adequacy misuse;
- Claude review returns `VERDICT: REVISE` and the blocker cannot be patched
  within five rounds.

## Skeptical Plan Audit

This rerun can pass while misleading us if the scaled solve only suppresses the
old condition veto but produces defensive-only transports, rank-channel
collapse, source-route drift, or same-route closeness without independent
accuracy.  The plan therefore keeps Phase 4d structural-only, preserves the
original P67 row specs and thresholds, requires failed rows to stay visible,
and blocks Phase 5 unless exactly one d18 configuration is admitted and
reviewed.  Proxy metrics such as fit residuals, same-route replay, or
normalizer closeness do not by themselves establish filtering accuracy.
