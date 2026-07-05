# Phase 1 Result: Spatial SIR SGQF Row Contract And Evaluator Status

Date: 2026-07-01

Status: `SGQF_LEADERBOARD_PHASE1_REVIEWED_BLOCKED_CLOSED`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Do not promote the SGQF spatial SIR row to `executed_value_score` or even `executed_value_only` in this phase. Preserve the row as blocked. The reviewed row contract confirms that the current SGQF state lacks a full observed-data source-scope evaluator and also lacks an admitted free-theta / analytical-manual score route for the row. |
| Primary criterion status | Passed by precise blocker: no reviewed SGQF full observed-data spatial SIR evaluator exists for the source-scope row, and the row still has no admissible SGQF analytical/manual score route. |
| Veto diagnostic status | Passed: no local complete-data or sidecar evidence was promoted as full filtering row admission, no no-free-theta score row was emitted, no autodiff score was admitted as analytical, and no wrong-target scalar promotion was made. |
| Main uncertainty | A future SGQF spatial SIR row may be possible, but only after a reviewed row-level evaluator contract and, if score admission is sought, a reviewed free-theta / derivative-ownership contract. |
| Next justified action | Advance to Phase 2 and freeze the predator-prey T20 SGQF row contract while preserving this SIR row as blocked. |
| What is not being concluded | No SGQF spatial SIR value row, no SGQF spatial SIR score row, no HMC readiness, no production/default claim, and no broad source-faithful SGQF claim for this row. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the spatial SIR SGQF row be tied to a real full observed-data value/analytical-score route, or must it remain blocked with a precise missing-evaluator / no-free-theta reason? |
| Baseline/comparator | `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`, `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`, `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-result-2026-06-30.md`, `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`, and `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md`. |
| Primary criterion | Passed by blocker: the row remains blocked because no reviewed full observed-data SGQF evaluator exists, and no SGQF analytical/manual score route tied to an admitted free-theta row contract exists. |
| Veto diagnostics | Passed: no local complete-data evidence promoted as full filtering, no no-free-theta score row emitted, no autodiff admitted as analytical, and no wrong-target scalar promoted. |
| Explanatory diagnostics | Row-contract inventory, existing leaderboard status, and preserved blocker notes. FD and score-at-true evidence remain inapplicable until the row contract admits a score route. |
| Not concluded | No SGQF SIR row admission, no HMC readiness, no production/default claim, and no broad source-faithful SGQF claim. |
| Artifact | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase1-sir-result-2026-07-01.md` and refreshed `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-subplan-2026-07-01.md`. |

## Reviewed Row Contract Summary

Current reviewed row identity:

```text
zhao_cui_spatial_sir_austria_j9_T20
```

Current reviewed SGQF row status:

- `comparison_status = blocked`
- `numeric_execution_status = blocked_by_two_lane_contract_or_missing_source_scope_evaluator`
- `score_status = blocked_no_free_theta`
- reason: `no reviewed SGQF source-scope spatial SIR route is wired`

Reviewed row-contract conclusions:

- this row is a source-scope observed-data leaderboard row;
- it is **not** the P91 local complete-data sidecar;
- it is **not** a score row unless a reviewed artifact first declares the
  required free-theta / derivative ownership for the same row target;
- blocked is the only honest current SGQF leaderboard status for this row.

## Local Checks

Commands:

```bash
test -f docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json
test -f docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md
test -f docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-result-2026-06-30.md
test -f docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json
test -f docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md
rg -n "zhao_cui_spatial_sir_austria_j9_T20|blocked_no_free_theta|blocked_by_two_lane_contract_or_missing_source_scope_evaluator|local complete-data|full observed-data" docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-result-2026-06-30.md docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase1-sir-row-contract-2026-07-01.md
git diff --check -- docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase1-sir-*.md
```

Outcome:

- All required row-authority inputs existed locally.
- Grep coverage confirmed the preserved blocked SGQF row state, the no-free-theta score blocker, and the distinction between the P91 local component and the full observed-data row.
- Phase 1 row-contract diff hygiene passed.

## Bounded Claude Reviews

Reviewed artifacts and final outcomes:

- Phase 1 SIR subplan: `VERDICT: AGREE` after closing review-gate, exact-authority, provenance-definition, and derivative-evidence wording issues
- Phase 1 SIR row contract: prepared for use in this result and local checks
- refreshed Phase 2 subplan: to be reviewed in the next phase package

## Skeptical Plan Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided: the row is anchored to the authoritative July 1 leaderboard artifact and the June 30 SIR blocker closeout. |
| Proxy metric promoted | Avoided: no sidecar/local complete-data evidence was treated as full-row admission. |
| Missing stop condition | Avoided: the row remains blocked because no SGQF full-row evaluator and no admissible score route exist. |
| Unfair comparison | Avoided: no score route is admitted for a row still lacking a reviewed free-theta / derivative contract. |
| Hidden assumption | Avoided: the result does not assume UKF or Zhao-Cui execution implies SGQF near-readiness. |
| Stale context | Avoided: the row contract is tied to explicit authority inputs rather than older generic memory. |
| Environment mismatch | Avoided: Phase 1 remained document-only. |
| Artifact-answer mismatch | Avoided: the result closes with a precise blocker and an exact next implementation gap rather than a vague “pending” state. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745` |
| Worktree status | Dirty pre-existing research/doc worktree; unrelated dirty changes preserved. |
| Execution target | Document-only SGQF spatial SIR row-contract phase. |
| CPU/GPU status | No TensorFlow numerical command and no GPU/CUDA command were run in Phase 1. |
| Runtime status | No implementation, runtime, leaderboard regeneration, HMC, GPU/XLA, release, CI, or default-policy command was run. |
| Plan | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase1-sir-subplan-2026-07-01.md` |
| Row contract | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase1-sir-row-contract-2026-07-01.md` |
| Result | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase1-sir-result-2026-07-01.md` |
| Refreshed Phase 2 subplan | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-subplan-2026-07-01.md` |

## Phase 2 Handoff

Phase 2 may start only after the ledgers record that:

- the spatial SIR SGQF row remains blocked with exact reason
  `blocked_by_two_lane_contract_or_missing_source_scope_evaluator` and
  `blocked_no_free_theta` for score;
- the Phase 1 result is reviewed `AGREE`;
- the refreshed Phase 2 subplan is reviewed `AGREE`;
- and no SGQF code/test mutation was performed for SIR under an unfrozen row contract.

Phase 2 must now freeze the predator-prey T20 SGQF row contract and either
implement or block that row honestly.
