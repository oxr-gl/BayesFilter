# SGQF Highdim Leaderboard Completion Master Program

Date: 2026-07-01

## Status

`DRAFT_REVIEW_READY`

Program owner: Codex supervisor/executor in the current conversation.

Claude role: read-only reviewer only. Claude may find internal consistency
problems or agree that a plan/result is safe, but Claude is not an execution
authority and cannot authorize human, runtime, product-capability,
default-policy, release, or scientific-claim boundary crossings.

## Objective

Finish the SGQF side of the high-dimensional leaderboard comparison so that, for
all currently tested highdim source-scope model rows, SGQF is either:

- `executed_value_score` with finite value, analytical/manual score provenance,
  declared theta coordinates, and honest scoped nonclaims; or
- explicitly blocked with a precise missing evaluator / missing analytical-
  derivative / wrong-target / no-free-theta reason.

This program is focused on the remaining SGQF leaderboard gaps for:

- `zhao_cui_spatial_sir_austria_j9_T20`
- `zhao_cui_predator_prey_T20`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`

The already-complete SGQF rows remain preserved as baselines and are **not** to
be reopened unless a later phase finds a true contradiction:

- `benchmark_lgssm_exact_oracle_m3_T50`
- `zhao_cui_sv_actual_nongaussian_T1000`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`

This program treats the task as a **leaderboard-completion program first** and
an implementation program second. The user wants minimal interruption and no
false mathematical “choices.” Therefore the row identities, claim levels,
approximate-vs-exact semantics, and analytical-only score rule are fixed by the
reviewed program artifacts rather than by interactive preference prompts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining SGQF leaderboard gaps be repaired into honest value plus analytical-score cells, or else blocked with exact evaluator/derivative gaps, so that the highdim leaderboard contains a proper SGQF comparison across all currently tested models? |
| Baseline/comparator | Current authoritative artifacts `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json` and `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`; the completed SGQF rows for affine LGSSM, actual SV, and KSC surrogate SV; the generic nonlinear-SSM governed program closed on 2026-07-01; and current source-scope evaluator/score adapters. |
| Primary pass criterion | Every remaining SGQF row is either `executed_value_score` with finite value, finite analytical/manual score, explicit theta coordinates, same-scalar provenance, and scoped nonclaims, or is blocked with a precise next implementation gap. The final regenerated leaderboard must show SGQF/UKF/Zhao-Cui status honestly for every tested row. |
| Veto diagnostics | Autodiff/`GradientTape`/finite-difference provenance admitted as an analytical score; value-only row treated as gradient evidence; wrong-target Gaussian-closure surrogate promoted as same-target evidence; source-row evaluator missing but row emitted as executed; no-free-theta row emitted with score; auxiliary/native-oracle/precursor evidence promoted as source-row admission; GPU/XLA status treated as row admission; unexplained gap after a claimed exact/same-target route. |
| Explanatory diagnostics | FD consistency, score-at-true calibration where meaningful, runtime, score norms, branch/failure labels, and model-specific gap tables explain behavior but do not alone prove exact likelihood correctness, posterior correctness, HMC readiness, or production readiness. It is acceptable for SGQF to remain approximate if the difference is measured, expected, and honestly explained at the reviewed claim level. |
| Not concluded | No HMC readiness, no production/default-policy change, no top-level API promotion, no universal exact-target claim for all models, and no broad generic direct-likelihood SGQF claim unless separately gated and reviewed. |
| Artifacts | This master program; phase subplans/results; visible runbook; visible execution ledger; Claude review ledger; visible stop handoff; regenerated highdim leaderboard JSON/Markdown; and final closeout artifact. |

## Current SGQF Leaderboard State

Authoritative current artifact:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`

Current authoritative paired leaderboard artifacts:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`

Current full three-way SGQF/UKF/Zhao-Cui rows:

- `benchmark_lgssm_exact_oracle_m3_T50`
- `zhao_cui_sv_actual_nongaussian_T1000`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`

Current rows still missing SGQF completion:

- `zhao_cui_spatial_sir_austria_j9_T20`
- `zhao_cui_predator_prey_T20`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`

## Owner Decisions Incorporated

- The highdim leaderboard comparison must use **analytical/manual score routes only** for admitted SGQF score cells. Autodiff is diagnostic only.
- An SGQF row may be approximate; that is acceptable if the approximation is
  the reviewed lane, the difference is measured, and the difference is honestly
  explained.
- It is not acceptable for an executed SGQF row to have an unexplained gap, a
  wrong-target scalar, or a silently mismatched value/score branch.
- Value-before-gradient remains a hard gate.
- Score-at-true consistency, FD consistency, and runtime explain behavior but do
  not by themselves prove exact likelihood correctness, posterior correctness,
  HMC readiness, or production readiness.
- The already-complete affine LGSSM / actual SV / KSC rows are baselines to
  preserve, not lanes to reopen casually.

## Governing Authority Order

When artifacts disagree, use the following authority order for SGQF leaderboard
completion semantics:

1. newest reviewed SGQF leaderboard row contract or blocker/result produced by
   this program for the exact row/claim in question;
2. newest reviewed final decision or closeout from this program;
3. current authoritative leaderboard artifact
   `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
   plus its paired Markdown summary;
4. reviewed target-and-authority / branch / structural-admission contracts from
   the generic nonlinear-SSM program where they apply;
5. live code seams and emitted row logic in leaderboard/benchmark harnesses;
6. older SGQF repair programs and older two-lane artifacts as historical context
   only.

No lower-ranked artifact may silently override a higher-ranked target statement
or row-status statement.

## Anti-Drift Hard Gates And Vetoes

### Hard gates

1. **Row-contract-before-implementation gate**
   - No SGQF code/test mutation for a blocked row may begin until that row's
     target / evaluator / score contract is frozen in a reviewed phase artifact.

2. **Value-before-gradient gate**
   - No SGQF analytical-score claim may advance until the SGQF value row for the
     same target/row has passed the value gate.

3. **Analytical-only score gate**
   - No SGQF score row may be admitted if its provenance uses autodiff,
     `GradientTape`, `ForwardAccumulator`, or finite-difference approximation as
     the admitted score route.

4. **Approximate-but-explained gate**
   - An SGQF row may remain approximate and still be admitted if:
     - the reviewed lane semantics say it is approximate,
     - the difference is measured against the right comparator,
     - and the difference is explained honestly.
   - If the difference cannot be explained at the reviewed claim level, the row
     blocks.

5. **Same-row / same-scalar gate**
   - Native-oracle, precursor, auxiliary, actual-SV, or KSC evidence may not be
     promoted as source-row admission evidence for SIR / predator-prey /
     generalized-SV rows unless a reviewed artifact explicitly says so.

6. **Review-before-advance gate**
   - No phase may advance without a reviewed subplan, reviewed result/blocker,
     and refreshed next-phase subplan.

7. **Blocked-closeout gate**
   - If a row remains blocked, the phase must write a blocker closeout at the
     declared result path and the program may continue only if downstream
     artifacts can still represent that blocked status honestly.

8. **Status-preservation gate**
   - Historical blocked/value-only/diagnostic statuses may not be silently
     upgraded by tests, benchmark emitters, or regenerated tables.

### Explicit veto conditions

- `AUTODIFF_SCORE_PROMOTED_AS_ANALYTICAL`
- `VALUE_ONLY_ROW_PROMOTED_AS_GRADIENT_EVIDENCE`
- `WRONG_TARGET_SCALAR_PROMOTED`
- `SOURCE_SCOPE_EVALUATOR_MISSING`
- `NO_FREE_THETA_BUT_SCORE_EMITTED`
- `UNEXPLAINED_APPROXIMATION_GAP`
- `PHASE_ADVANCE_WITHOUT_REVIEWED_HANDOFF`

## Phase Index

| Phase | Name | Objective | Subplan | Required result artifact |
| ---: | --- | --- | --- | --- |
| 0 | Launch inventory and SGQF row freeze | Freeze the remaining blocked SGQF row identities, governing comparators, and no-choice execution discipline before code work. | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase0-launch-subplan-2026-07-01.md` | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase0-launch-result-2026-07-01.md` |
| 1 | SIR full-row SGQF contract and evaluator status | Freeze the exact SGQF row contract for spatial SIR and either implement or precisely block its value/score path. | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase1-sir-subplan-2026-07-01.md` | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase1-sir-result-2026-07-01.md` |
| 2 | Predator-prey T20 SGQF row completion | Freeze the T20 SGQF row contract and implement or block the source-scope predator-prey value/analytical-score pair honestly. | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-subplan-2026-07-01.md` | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-result-2026-07-01.md` |
| 3 | Generalized-SV SGQF source-row completion | Freeze the exact generalized-SV SGQF row contract and implement or block the value/analytical-score pair honestly. | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase3-generalized-sv-subplan-2026-07-01.md` | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase3-generalized-sv-result-2026-07-01.md` |
| 4 | Cross-row SGQF analytical score gate | Validate analytical/manual score provenance, same-scalar support, and row-specific gap explanation for every SGQF row newly executed in Phases 1-3. | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase4-score-gate-subplan-2026-07-01.md` | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase4-score-gate-result-2026-07-01.md` |
| 5 | Final leaderboard regeneration and closeout | Regenerate the authoritative highdim leaderboard artifacts and close with the final SGQF row-status decision table. | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase5-final-regeneration-subplan-2026-07-01.md` | `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase5-final-regeneration-result-2026-07-01.md` |

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

- do not ask the user to choose target semantics already fixed by the reviewed
  row contract;
- do not ask the user whether an autodiff route is “good enough” when the row
  contract requires analytical/manual score provenance;
- do not ask for preferences when the next step is determined by science,
  reviewed evidence, or the hard gates;
- ask only at true human-boundary points: changing the row target, changing
  leaderboard admission criteria, destructive actions, or crossing an authority
  boundary explicitly marked human-required.

## Approval And Trusted-Context Needs

No extra human approval is anticipated for:

- document edits under `docs/plans`;
- CPU-only local checks with GPU hidden before TensorFlow import;
- bounded Claude read-only review;
- non-destructive source/test edits explicitly authorized by a reviewed phase
  subplan.

Human or explicit approval is still required for:

- package installation, network fetches, credentials, release tagging,
  CI-service mutation, or default-policy changes;
- destructive git/filesystem actions;
- treating a GPU/XLA result as evidence without trusted GPU execution;
- changing pass/fail criteria after seeing results.

## Skeptical Audit

Initial audit status: `PASSED_FOR_PLANNING_ONLY`.

Material risks incorporated into the plan:

- a row can look “complete” when value exists but analytical/manual score does
  not;
- approximate SGQF rows are acceptable only when the difference is measured and
  explained honestly;
- SIR, predator-prey, and generalized-SV blockers are evaluator/contract gaps,
  not formatting gaps;
- the already-admitted rows should be preserved as baselines rather than
  reopened casually;
- GPU/XLA and batch status may explain readiness but must not silently decide
  row admission.

If a phase cannot establish same-row value validity or analytical-score validity,
the row must close as blocked or value-only with a precise reason. The program
may continue only if downstream artifacts can represent that status without
ambiguity.

## Final Required Output Artifacts

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`,
  or a later dated file only if the final regeneration phase explicitly records
  the supersession.
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`,
  or a later dated file only if the final regeneration phase explicitly records
  the supersession.
- `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-claude-review-ledger-2026-07-01.md`
- `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-visible-execution-ledger-2026-07-01.md`
- `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-visible-gated-execution-runbook-2026-07-01.md`
- `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase5-final-regeneration-result-2026-07-01.md`
- `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-visible-stop-handoff-2026-07-01.md`

Execution begins only through
`docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-visible-gated-execution-runbook-2026-07-01.md`.
