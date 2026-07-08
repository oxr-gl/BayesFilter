# Highdim Leaderboard Blocker-By-Blocker Master Program

Date: 2026-07-04

Status: `DRAFT_REVIEW_READY`

Program owner: Codex supervisor/executor in the current conversation.

Claude role: read-only reviewer only. Claude may flag plan, evidence, or
claim-safety defects, but Claude cannot authorize crossing human, runtime,
model-file, funding, product-capability, default-policy, or scientific-claim
boundaries.

## Objective

Repair the remaining leaderboard blockers one row family at a time, with each
phase proving either a finite value plus a same-target analytical/manual score
or a precise blocker that preserves the row honestly.

Candidate target families, in current repair-priority order and subject to
Phase 0 certification against the July 3 combined leaderboard plus the July 2
remaining-blockers ledger:

1. `benchmark_lgssm_exact_oracle_m3_T50` full-row LEDH LGSSM admission;
2. `zhao_cui_sv_actual_nongaussian_T1000` current LEDH actual-SV adapter;
3. `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` current LEDH KSC adapter;
4. `zhao_cui_generalized_sv_synthetic_from_estimated_values` exact source-row evaluator;
5. `zhao_cui_spatial_sir_austria_j9_T20` full observed-data/filtering route;
6. `zhao_cui_predator_prey_T20` source-scope adapter and analytical score;
7. remaining UKF analytical-score cleanup;
8. final regeneration and closeout.

This program is intentionally one-row-family-at-a-time. No phase may promote a
row from a sidecar, lower-rung, autodiff, or diagnostic-only artifact.

## Baseline

Authoritative baseline:

- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json`
- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.md`
- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-execution-ledger-2026-07-02.md`

Current blockers are summarized in the combined leaderboard JSON and the
remaining-blockers ledger. For every phase, the phase result must say plainly
whether the computed quantity is correct for the stated target, wrong relative
to the stated target, unsupported, not checked, or heuristic only.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining highdim leaderboard blockers be repaired into honest value plus analytical/manual score rows, or else preserved as precise blockers, without admitting autodiff/FD scores or lower-rung diagnostics as leaderboard evidence? |
| Baseline/comparator | `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json` and `.md`, plus the remaining-blockers ledger and phase-local target contracts. |
| Primary pass criterion | Each targeted cell either emits finite value and finite same-target analytical/manual score with declared theta coordinates and provenance free of autodiff/FD, or has a precise blocker that separates target, value evaluator, score derivative, and readiness gaps. |
| Veto diagnostics | Autodiff/FD/tape score admission; wrong target reported as row; local component or lower-rung evidence reported as full row; source-faithful claim without paper/source anchors; GPU/XLA claim from non-trusted context. |
| Explanatory diagnostics | FD consistency, score norm, runtime, score-at-true calibration, CPU-only smoke, trusted GPU/XLA compile/timing, and batch parity. |
| Not concluded | Exact nonlinear likelihood correctness, posterior correctness, HMC convergence, GPU superiority, release readiness, default-policy change. |
| Artifacts | Master program, visible runbook, phase subplans/results, review ledger, execution ledger, stop handoff, regenerated leaderboard artifacts `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-04.json` and `.md` if Phase 8 reaches regeneration, and final closeout/reset memo `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-reset-memo-2026-07-04.md` if reached. |

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Baseline freeze and launch gate | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase0-baseline-freeze-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase0-baseline-freeze-result-2026-07-04.md` |
| 1 | Full-row LGSSM GPU/XLA score gate | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase1-lgssm-full-row-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase1-lgssm-full-row-result-2026-07-04.md` |
| 2 | Actual-SV current LEDH adapter repair | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase2-actual-sv-ledh-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase2-actual-sv-ledh-result-2026-07-04.md` |
| 3 | KSC current LEDH adapter repair | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase3-ksc-ledh-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase3-ksc-ledh-result-2026-07-04.md` |
| 4 | Generalized-SV exact source-row evaluator | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase4-generalized-sv-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase4-generalized-sv-result-2026-07-04.md` |
| 5 | Spatial SIR full observed-data/filtering route | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase5-spatial-sir-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase5-spatial-sir-result-2026-07-04.md` |
| 6 | Predator-prey T20 source-scope adapter | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase6-predator-prey-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase6-predator-prey-result-2026-07-04.md` |
| 7 | UKF analytical-score cleanup | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase7-ukf-cleanup-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase7-ukf-cleanup-result-2026-07-04.md` |
| 8 | Final regeneration and closeout | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase8-final-regeneration-closeout-subplan-2026-07-04.md` | `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase8-final-regeneration-closeout-result-2026-07-04.md` |

## Repair Loop

For every phase:

1. run the required local checks;
2. write the phase result or blocker record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude only as read-only reviewer for material phases;
6. patch fixable review findings visibly and rerun focused checks;
7. if the same blocker reaches five review rounds, write a blocker result,
   update the stop handoff, and stop.

Claude cannot authorize human, runtime, model-file, funding, product,
scientific-claim, or default-policy boundaries.

## Artifact Ownership

- `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-visible-execution-ledger-2026-07-04.md`
  is appended at each phase start/end and records the phase state machine.
- `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-claude-review-ledger-2026-07-04.md`
  records every material Claude review round.
- `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-visible-stop-handoff-2026-07-04.md`
  is written if a phase blocks, the runbook stops, or the program closes early.
- `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase8-final-regeneration-closeout-result-2026-07-04.md`
  and the reset note are written only by the final phase.

## Human Approval Surface

The user has already approved Claude read-only review for this repo. The
following remain trusted or escalated actions under repository policy:

- GPU/CUDA/XLA runs;
- long-running benchmark commands;
- destructive filesystem or git actions;
- network/package/environment changes;
- release tagging or default-policy changes.

## Skeptical Audit

Initial audit status: `PASSED_FOR_PLANNING_ONLY`.

Risks encoded in the phases:

- a row can have a finite value while score admission remains blocked;
- autodiff score provenance must stay diagnostic only;
- sidecar, lower-rung, or local-component evidence must not be promoted to a
  full row;
- score-at-true or runtime can explain but not admit a row;
- trusted GPU/XLA evidence is separate from CPU-only local checks.

Phase 0 must certify, in its result artifact, that the candidate eight phases
are aligned to the current authoritative remaining-blockers ledger at
`docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-execution-ledger-2026-07-02.md`.

Execution begins only through:

- `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-visible-gated-execution-runbook-2026-07-04.md`
