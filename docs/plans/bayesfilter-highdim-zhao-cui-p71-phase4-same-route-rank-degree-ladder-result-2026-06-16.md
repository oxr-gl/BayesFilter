# P71 Phase 4 Result: Same-Route Rank And Degree Ladder

metadata_date: 2026-06-16
status: BLOCKED_CLAUDE_REVIEW_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 4

## Objective

Run the predeclared same-route rank/degree structural ladder for SIR d=18
without treating finite values, execution-only evidence, or same-route replay
as filtering accuracy.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the same source-route branch remain stable under adjacent rank and degree changes without hidden source-route drift? |
| Baseline/comparator | Phase 3 admitted finite-value candidate branch, the Phase 2 execution-only JSON row-adequacy boundary, the known P60 condition-veto boundary, adjacent rank candidate, and adjacent degree candidate; authorized differences are `fit_rank` or `fit_degree` only. |
| Primary criterion | Predeclared rank/degree ladder passes source invariants, finite normalizers, frozen bounded-delta thresholds, non-defensive-only transport, channel activity, and condition diagnostics. |
| Veto diagnostics | Source-route invariant drift, unauthorized branch drift, defensive-only transport, rank-channel collapse, nonfinite normalizers, condition-number warning/veto, row-adequacy boundary misuse, or thresholds changed after output. |
| Explanatory diagnostics | Log-marginal deltas, normalizer increments, ESS, condition numbers, channel norms, holdout/replay residuals, and P60 sentinel status. |
| Not concluded | No filtering accuracy, no d50/d100 scaling, no HMC readiness, no adaptive Zhao-Cui parity, and no author-code failure claim. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-2026-06-16.json` |

## Frozen Thresholds

These were copied from the Phase 4 subplan before interpretation.

| Quantity | Threshold |
| --- | ---: |
| log marginal absolute delta | 5.0 |
| normalizer increment absolute delta | 5.0 |
| probe log-density median absolute delta | 10.0 |
| retained log-density median absolute delta | 10.0 |
| condition-number warning | 1e10 |
| condition-number veto | 1e14 |
| channel activity absolute tolerance | 1e-12 |
| channel activity relative tolerance | 1e-8 |
| defensive-only sqrt-normalizer tolerance | 1e-14 |
| fit mass fraction minimum | 1e-6 |
| log increment absolute bound | 1e6 |
| holdout/replay normalized residual veto | 10.0 |

## Command

CPU-only by design:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p67_author_sir_adjacent_ladder_diagnostics.py --output docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-2026-06-16.json
```

The repaired artifact records `cpu_only_intent: CUDA_VISIBLE_DEVICES=-1`,
`sample_count: 1`, fit budgets `{base_candidate: 16, rank_pair: 36,
degree_pair: 24}`, and elapsed time `11.943` seconds.

## Result Summary

Phase 4 is blocked.

- Top-level status:
  `P67_ADJACENT_FIXED_BUDGET_SCREEN_BLOCKED`.
- Every predeclared row blocked on
  `fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO`.
- The rank ladder was not executed:
  `P67_ROW_NOT_EXECUTED`.
- The degree ladder was not executed:
  `P67_ROW_NOT_EXECUTED`.
- The P60 sentinel remains blocked:
  `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE`.
- The P60 sentinel is explanatory only and still carries stale
  `branch_fit_row_adequacy_failed` blockers; it is not the Phase 4 primary
  gate.
- The repaired P67 artifact now preserves structured
  `failed_fit_diagnostics`, `budget_limitation_diagnostics`,
  `core_update_statuses`, `condition_number_veto`, `transport_returned:
  false`, and `success_payload_emitted: false`.

The five blocked rows are:

| Row | Rank | Degree | Fit sample count | Status | Fit status | Transport returned |
| --- | ---: | ---: | ---: | --- | --- | --- |
| `base_candidate_1_2_fit16` | 2 | 1 | 16 | `P67_ROW_BLOCKED_ON_FAILED_FIT` | `CONDITION_NUMBER_VETO` | false |
| `rank_candidate_1_2_fit36` | 2 | 1 | 36 | `P67_ROW_BLOCKED_ON_FAILED_FIT` | `CONDITION_NUMBER_VETO` | false |
| `rank_stronger_1_3_fit36` | 3 | 1 | 36 | `P67_ROW_BLOCKED_ON_FAILED_FIT` | `CONDITION_NUMBER_VETO` | false |
| `degree_candidate_1_2_fit24` | 2 | 1 | 24 | `P67_ROW_BLOCKED_ON_FAILED_FIT` | `CONDITION_NUMBER_VETO` | false |
| `degree_stronger_2_2_fit24` | 2 | 2 | 24 | `P67_ROW_BLOCKED_ON_FAILED_FIT` | `CONDITION_NUMBER_VETO` | false |

## Artifact-Coverage Repair During Phase 4

The first Phase 4 diagnostic artifact showed only exception strings for failed
fits.  That was insufficient artifact coverage for a gated blocker because it
did not preserve the P70 failed-fit payload.

Repair:

- `scripts/p67_author_sir_adjacent_ladder_diagnostics.py` now catches
  `P70FixedFitDiagnosticError` separately.
- Failed rows now preserve the structured P70 payload rather than emitting
  only the exception string.
- `tests/highdim/test_p59_author_sir_step_spec_assembly.py` now covers the
  failed-fit row payload and uses the current P70 condition threshold
  constants in relevant assertions and fixtures.

This repair improves blocker observability only.  It does not weaken the
condition-number veto, does not admit failed fits, and does not change rank,
degree, thresholds, source-route semantics, or Phase 4 pass criteria.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Stop before Phase 5 | Failed: no rank/degree ladder could execute | Condition-number veto triggered on all five rows | Whether the fixed branch fit can be stabilized without retuning thresholds or changing the source-route contract | Write/review a separate condition-veto or fit-stability repair plan before any accuracy gate | No d18 accuracy, no same-route rank convergence, no robustness, no scaling, no HMC readiness |

## Handoff

Phase 5 must not launch from this artifact.  Its entry condition requires a
single admitted d18 configuration from Phase 4, and Phase 4 admitted none.

The next work item is a separate reviewed repair/design plan for the fixed-fit
condition-veto blocker.  That plan must preserve the P70 veto thresholds unless
the user explicitly approves changing them, and it must separate numerical
stabilization, rank/degree/sample-budget decisions, and scientific claims.

## Claude Read-Only Review

Claude Opus max effort reviewed the Phase 4 blocker packet with worker
`p71-phase4-blocker-result-review-iter1` and returned `VERDICT: AGREE`.

Findings summary:

- Blocking Phase 5 is correct because all five rows are
  `CONDITION_NUMBER_VETO`, rank/degree ladders are `P67_ROW_NOT_EXECUTED`, and
  no d18 configuration was admitted.
- Claude found no wrong-baseline or proxy-promotion error in the Phase 4
  decision.
- The failed-fit artifact-coverage repair is sufficient: structured P70
  failed-fit diagnostics are preserved and failed fits remain inadmissible.
- Stop conditions, feasibility, boundary safety, and CPU-only environment
  interpretation are coherent.
- Claude noted a non-material artifact nuance: the subplan names a
  comparison-invariant ledger and refreshed Phase 5 subplan, but since the
  ladders never executed and Phase 5 is explicitly blocked, this does not
  affect the blocker decision.

## Local Checks

Passed:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-2026-06-16.json
python -m compileall -q scripts/p67_author_sir_adjacent_ladder_diagnostics.py tests/highdim/test_p59_author_sir_step_spec_assembly.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_step_spec_assembly.py::test_p59_9b_assembles_two_author_sir_36d_step_specs tests/highdim/test_p59_author_sir_step_spec_assembly.py::test_p67_failed_fit_row_payload_preserves_p70_diagnostics
git diff --check -- scripts/p67_author_sir_adjacent_ladder_diagnostics.py tests/highdim/test_p59_author_sir_step_spec_assembly.py docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-result-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-phase4-same-route-rank-degree-ladder-2026-06-16.json docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-stop-handoff-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-gated-overnight-execution-runbook-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p71-runbook-claude-review-ledger-2026-06-16.md
```

Focused pytest output:

- `2 passed, 2 warnings in 178.83s`

## Nonclaims

- No d18 filtering accuracy claim.
- No same-route rank/degree convergence claim.
- No d50 or d100 scaling claim.
- No HMC readiness claim.
- No adaptive Zhao-Cui parity claim.
- No author-code failure claim.
