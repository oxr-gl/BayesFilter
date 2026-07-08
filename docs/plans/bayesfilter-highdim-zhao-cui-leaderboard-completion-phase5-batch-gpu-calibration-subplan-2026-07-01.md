# Phase 5 Subplan: Batched, GPU/XLA, And Score-At-True Calibration Ladder

Date: 2026-07-01

Status: `DRAFT_PENDING_PHASE4_REVIEW`

## Phase Objective

For admitted Zhao-Cui value/score rows, run the required batched parity,
trusted GPU/XLA capability, and score-at-true consistency ladder. Rows that are
still blocked must not be benchmark-ranked.

## Entry Conditions Inherited From Previous Phase

- Phases 1 to 4 closed every non-LGSSM Zhao-Cui row as admitted or precisely
  blocked.
- Any admitted score row has manual analytical provenance and theta
  coordinates.
- GPU/XLA evidence requires trusted/escalated execution.

## Required Artifacts

- Batched parity result for admitted rows.
- Trusted GPU/XLA probe and row-specific compile/run manifest, where
  applicable.
- Score-at-true calibration manifest for rows with simulator/truth support.
- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase5-batch-gpu-calibration-result-2026-07-01.md`
- Refreshed Phase 6 subplan.

## Required Checks, Tests, Reviews

- Single-vs-batched equality for admitted rows.
- Trusted GPU framework probe before GPU/XLA claims.
- Row-specific GPU/XLA smoke or precise not-applicable/blocker.
- Score-at-true multi-seed average within reviewed uncertainty rule when data
  generation and true parameter are available.
- Claude read-only review of result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do admitted Zhao-Cui rows have batched parity, trusted GPU/XLA capability where claimed, and score-at-true consistency where testable? |
| Baseline/comparator | Single-call admitted value/score row for each model. |
| Primary criterion | Every admitted row has batched/GPU/calibration status recorded as pass, not-applicable, or precise blocker without ranking invalid rows. |
| Veto diagnostics | GPU claim from sandbox context; batched mismatch; nonfinite score; score-at-true treated as exact proof; blocked row ranked by timing. |
| Explanatory diagnostics | Runtime, score norm, standard deviation, standard error, GPU speedup. |
| Not concluded | No universal GPU superiority, posterior correctness, HMC convergence, or exact likelihood correctness. |
| Artifact | Phase 5 result and calibration/benchmark manifests. |

## Forbidden Claims And Actions

- Do not run GPU/CUDA commands without trusted/escalated context.
- Do not rank rows whose correctness gate is open.
- Do not treat score-at-true as exact likelihood proof.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 if each admitted row has explicit batched/GPU/calibration
status and each blocked row remains unranked.

## Stop Conditions

Stop if trusted GPU access is unavailable for a required GPU claim, or if
batched parity fails for an admitted row and cannot be repaired.

## End-of-Subplan Protocol

1. Run the required local checks.
2. Write the Phase 5 result / close record.
3. Draft or refresh the Phase 6 subplan.
4. Review the Phase 6 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
