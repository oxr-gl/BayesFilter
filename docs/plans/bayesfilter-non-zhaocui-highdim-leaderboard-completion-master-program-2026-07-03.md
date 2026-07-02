# Non-Zhao-Cui Highdim Leaderboard Completion Master Program

Date: 2026-07-03

## Status

`DRAFT_REVIEW_READY`

Program owner: Codex supervisor/executor in the current conversation.

Claude role: read-only reviewer only. Claude may identify internal
consistency, evidence, or claim-safety defects, but Claude is not an execution
authority and cannot authorize human, runtime, product-capability,
default-policy, release, or scientific-claim boundary crossings.

## Objective

Finish the **non-Zhao-Cui** side of the high-dimensional leaderboard comparison
so that, for the current tested model rows, the SGQF and UKF algorithms are
reported honestly in value and analytical-gradient terms, or precisely blocked.

This program excludes all `zhao_cui_scalar_or_multistate` row-completion work.
It treats the already-complete SGQF/UKF baselines as preserved and focuses only
on the remaining non-Zhao-Cui blockers for:

- `zhao_cui_spatial_sir_austria_j9_T20`
- `zhao_cui_predator_prey_T20`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`

Rows already complete and preserved as baselines:

- `benchmark_lgssm_exact_oracle_m3_T50`
- `zhao_cui_sv_actual_nongaussian_T1000`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`

This program is focused and anti-drift. It does not ask the user to choose row
semantics or approximation categories that are already fixed by reviewed row
contracts and prior artifacts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining non-Zhao-Cui leaderboard gaps be repaired into honest value plus analytical/manual score rows, or else preserved as precise blockers, without promoting autodiff, wrong-target, or sidecar evidence into leaderboard admission? |
| Baseline/comparator | Authoritative current leaderboard artifacts `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json` and `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md`; preserved baseline rows for LGSSM / actual SV / KSC surrogate SV; existing SGQF and UKF row contracts / result artifacts for SIR, predator-prey, and generalized SV. |
| Primary pass criterion | Each remaining non-Zhao-Cui cell is either `executed_value_score` with finite value, finite analytical/manual score, declared theta coordinates, same-scalar provenance, and scoped nonclaims, or is blocked/value-only with a precise reason. The final regenerated leaderboard must report SGQF and UKF honestly for every tested row. |
| Veto diagnostics | autodiff/`GradientTape`/finite differences admitted as analytical score; value-only row promoted as gradient evidence; sidecar/local-complete-data evidence promoted as full observed-data leaderboard evidence; wrong-target scalar promotion; unexplained approximation gap at the reviewed claim level; blocked row silently upgraded during regeneration. |
| Explanatory diagnostics | FD consistency, score norm, branch/failure labels, score-at-true calibration where meaningful, runtime, and row-specific gap explanation explain behavior but do not by themselves prove exact likelihood correctness, posterior correctness, HMC readiness, or production readiness. Approximate rows are acceptable if the difference is measured and honestly explained. |
| Not concluded | No HMC readiness, no top-level API promotion, no production/default-policy change, no broad generic direct-likelihood SGQF claim, and no broad UKF readiness beyond the reviewed row scopes. |
| Artifacts | Master program, visible runbook, execution ledger, Claude review ledger, stop handoff, row-family subplans/results, regenerated leaderboard JSON/Markdown, and final closeout artifact. |

## Current Non-Zhao-Cui State

Authoritative current artifact pair:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md`

Already complete non-Zhao-Cui rows:

- `benchmark_lgssm_exact_oracle_m3_T50` — SGQF and UKF both `executed_value_score`
- `zhao_cui_sv_actual_nongaussian_T1000` — SGQF and UKF both `executed_value_score`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` — SGQF and UKF both `executed_value_score`

Remaining non-Zhao-Cui blockers:

- `zhao_cui_spatial_sir_austria_j9_T20`
  - SGQF blocked
  - UKF value exists, score not admitted under current full-row contract
- `zhao_cui_predator_prey_T20`
  - SGQF has reviewed same-row candidate evidence, but final authoritative leaderboard regeneration remains incomplete
  - UKF value exists, score blocked as autodiff-not-admitted
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`
  - SGQF blocked by missing same-row evaluator
  - UKF value exists, score blocked as autodiff-not-admitted

## Owner Decisions Incorporated

- Analytical/manual score only. Autodiff is diagnostic only.
- Approximate rows are acceptable if the approximation is the reviewed lane,
  the difference is measured, and the difference is honestly explained.
- It is not acceptable to leave an unexplained gap or to promote a wrong-target
  or sidecar route as leaderboard admission.
- Value-before-gradient remains a hard gate.
- Already-complete baseline rows are preserved and must not be reopened unless a
  reviewed contradiction is found.

## Anti-Drift Hard Gates And Vetoes

### Hard gates

1. **Row-contract-before-implementation gate**
   - No code/test mutation for a remaining row may begin until that row's
     contract is frozen in a reviewed artifact.

2. **Value-before-gradient gate**
   - No analytical-score claim may advance until the row's value gate passes for
     the same reviewed row/target.

3. **Analytical-only score gate**
   - No row may be admitted as `executed_value_score` if its admitted score
     provenance uses autodiff, `GradientTape`, `ForwardAccumulator`, or finite
     differences as the admitted route.

4. **Approximate-but-explained gate**
   - A row may remain approximate and still be admitted if the reviewed lane
     semantics say it is approximate, the difference is measured against the
     right comparator, and the difference is honestly explained.
   - If the difference cannot be explained at the reviewed claim level, the row
     blocks.

5. **Sidecar-is-not-main-row gate**
   - No local complete-data sidecar, lower-rung fixture, native oracle, or
     auxiliary evidence may be promoted as full leaderboard row admission unless
     a reviewed artifact explicitly says so.

6. **Review-before-advance gate**
   - No phase may advance without a reviewed subplan, reviewed result/blocker,
     and refreshed next-phase subplan.

7. **Blocked-closeout gate**
   - If a row remains blocked, the phase must write a blocker closeout at the
     declared result path and the program may continue only if downstream
     artifacts can still represent that blocked status honestly.

8. **Status-preservation gate**
   - Historical blocked/value-only/diagnostic statuses may not be silently
     upgraded by tests, emitters, or regenerated tables.

### Explicit veto conditions

- `AUTODIFF_SCORE_PROMOTED_AS_ANALYTICAL`
- `VALUE_ONLY_ROW_PROMOTED_AS_GRADIENT_EVIDENCE`
- `SIDECAR_PROMOTED_AS_MAIN_ROW`
- `WRONG_TARGET_SCALAR_PROMOTED`
- `UNEXPLAINED_APPROXIMATION_GAP`
- `PHASE_ADVANCE_WITHOUT_REVIEWED_HANDOFF`

## Phase Index

| Phase | Name | Objective | Subplan | Required result artifact |
| ---: | --- | --- | --- | --- |
| 0 | Baseline freeze and launch gate | Freeze the July 3 authoritative leaderboard pair and the preserved baseline row states before any new row work. | `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase0-baseline-freeze-subplan-2026-07-03.md` | `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase0-baseline-freeze-result-2026-07-03.md` |
| 1 | Spatial SIR row contract and status | Decide whether the main non-Zhao-Cui spatial SIR row remains blocked/value-only or can be advanced under a reviewed row contract. | `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase1-spatial-sir-subplan-2026-07-03.md` | `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase1-spatial-sir-result-2026-07-03.md` |
| 2 | Predator-prey T20 row completion | Finalize SGQF predator-prey row status and resolve UKF analytical-score admission for the exact T20 row. | `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase2-predator-prey-subplan-2026-07-03.md` | `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase2-predator-prey-result-2026-07-03.md` |
| 3 | Generalized-SV row contract and status | Decide whether SGQF generalized-SV remains blocked and whether UKF analytical-score admission can be closed honestly for the exact source row. | `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase3-generalized-sv-subplan-2026-07-03.md` | `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase3-generalized-sv-result-2026-07-03.md` |
| 4 | Final non-Zhao-Cui regeneration and closeout | Regenerate the authoritative highdim leaderboard pair and close with the final SGQF/UKF row-status decision table for all non-Zhao-Cui rows. | `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase4-final-regeneration-subplan-2026-07-03.md` | `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase4-final-regeneration-result-2026-07-03.md` |

## Required Review Loop

1. Review this master program with Claude in read-only mode, bounded to this
   exact file first.
2. Review the visible runbook and Phase 0 subplan before Phase 0 execution.
3. Review every material subplan before execution.
4. At phase end, run local checks, write the phase result or blocker, refresh
   the next subplan, and review the next subplan for consistency, correctness,
   feasibility, artifact coverage, and boundary safety.
5. If Claude finds a fixable issue, patch the same artifact visibly and rerun
   focused local checks.
6. Stop after five Claude review rounds for the same blocker and write a blocker
   result.

## No-Choice Execution Discipline

This program must not confuse the user with false mathematical choices.
Therefore:

- do not ask the user to choose row semantics already fixed by the reviewed row
  contract;
- do not ask whether autodiff is “good enough” when the contract requires
  analytical/manual provenance;
- do not ask for preferences when the next step is determined by science,
  reviewed evidence, or the hard gates;
- ask only at true human-boundary points: changing row target semantics,
  changing leaderboard admission criteria, destructive actions, or crossing an
  authority boundary explicitly marked human-required.

## Approval And Trusted-Context Needs

No extra human approval is anticipated for:

- document edits under `docs/plans`;
- CPU-only local checks with GPU hidden before TensorFlow import;
- bounded Claude read-only review;
- non-destructive source/test/emitter edits explicitly authorized by a reviewed
  phase subplan.

Human or explicit approval is still required for:

- package installation, network fetches, credentials, release tagging,
  CI-service mutation, or default-policy changes;
- destructive git/filesystem actions;
- treating a GPU/XLA result as evidence without trusted GPU execution;
- changing pass/fail criteria after seeing results.

## Final Required Output Artifacts

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json`,
  or a later dated file only if the final regeneration phase explicitly records
  the supersession.
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md`,
  or a later dated file only if the final regeneration phase explicitly records
  the supersession.
- `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-claude-review-ledger-2026-07-03.md`
- `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-visible-execution-ledger-2026-07-03.md`
- `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-visible-gated-execution-runbook-2026-07-03.md`
- `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase4-final-regeneration-result-2026-07-03.md`
- `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-visible-stop-handoff-2026-07-03.md`
