# Phase 5 Result: Batch/GPU/XLA Readiness And Score-At-True Calibration

Date: 2026-07-02

Status: `PASS_PHASE5_READINESS_CLASSIFIED_NO_ADMISSION_CHANGE`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 5 as readiness classification, not row promotion | Passed: readiness artifacts are keyed per admitted Zhao-Cui row and preserve deferred statuses | Passed: no Phase 3/4 blocker promoted, no untrusted GPU claim, no score-at-true proof claim | Exact batch-parity and multi-seed score-at-true harnesses are not yet wired for the two admitted rows | Refresh Phase 6 final regeneration subplan and regenerate/close only if artifacts match phase results | GPU/XLA readiness, HMC readiness, posterior correctness, exact likelihood correctness, batch throughput superiority |

## Evidence Contract Outcome

Phase 5 asked which admitted rows have batch/GPU/XLA readiness and
score-at-true consistency evidence, and which readiness checks are not
applicable or deferred. The answer is:

- `zhao_cui_predator_prey_T20` / `zhao_cui_scalar_or_multistate`: local
  value/manual-score row admitted from Phase 1; batch parity deferred with
  `deferred_exact_harness_missing`; score-at-true calibration deferred with
  `deferred_exact_multiseed_harness_missing`; GPU/XLA not run.
- `zhao_cui_generalized_sv_synthetic_from_estimated_values` /
  `zhao_cui_scalar_or_multistate`: local value/manual-score row admitted from
  Phase 2; batch parity deferred with `deferred_exact_harness_missing`;
  score-at-true calibration deferred with
  `deferred_exact_multiseed_harness_missing`; GPU/XLA not run.
- Phase 3 SIR and Phase 4 UKF blockers remain non-admitted readiness targets.

## Artifacts

- Readiness manifest:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-readiness-manifest-2026-07-02.json`
- Batch parity artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-batch-parity-2026-07-02.json`
- GPU/XLA readiness artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-gpu-xla-readiness-2026-07-02.json`
- Score-at-true artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-score-at-true-2026-07-02.json`

## Checks Run

- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m json.tool docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase1-predator-prey-zhaocui-row-2026-07-02.json`: passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m json.tool docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-zhaocui-row-2026-07-02.json`: passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m json.tool docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-route-bindings-2026-07-02.json`: passed.
- CPU-only admitted-row inventory command from the subplan: passed; normalized
  Phase 1 as a single object and Phase 2 as a one-row list.
- Broad readiness discovery `rg`: passed with many adjacent matches, including
  P91 batched score API, FD batch diagnostics, and experimental SVD/UKF batch
  code; these were not exact row-local readiness harnesses.
- Narrow exact-row discovery over admitted row IDs and score-at-true/batch
  terms: passed; found exact row value/score tests and truth bindings but no
  exact batch-parity or multi-seed score-at-true harness for either admitted
  Zhao-Cui row.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | not recorded in Phase 5 artifact; worktree is dirty |
| Environment | local repo; CPU-only checks used `CUDA_VISIBLE_DEVICES=-1` and `MPLCONFIGDIR=/tmp` |
| GPU status | not probed; trusted GPU/XLA commands were not approved or run |
| Data version | Phase 1/2 row-local artifacts from 2026-07-02; July 1 baseline for context |
| Seeds | no new stochastic numerical run |
| Output artifacts | Phase 5 JSON artifacts listed above |
| Plan file | `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase5-readiness-calibration-subplan-2026-07-02.md` |

## Boundary Notes

- Score-at-true consistency remains a useful sanity diagnostic, but Phase 5 did
  not run it and would not treat it as exact likelihood proof.
- Single-dataset score norms in the admitted rows are not multi-seed
  calibration evidence.
- GPU/XLA readiness requires a future trusted-context command approval with an
  exact command, runtime expectation, row target, artifact path, and device
  precheck.
- Phase 5 does not regenerate the full leaderboard and does not change
  admission criteria.

## Handoff

Proceed to Phase 6 only after refreshing and reviewing the final regeneration
subplan. Phase 6 must preserve Phase 5 readiness statuses separately from
value/score row admission.
