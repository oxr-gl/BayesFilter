# Meta OT-Aligned Fixed-Target Retained-Sinkhorn Refit Master Program

Date: 2026-06-27

## Status

`REVIEWED_PHASE_0_READY`

## Purpose

Refit BayesFilter's current fixed-target retained-Sinkhorn neural-OT lane so it more faithfully matches the chosen Meta OT donor-core contract.

This program is limited to the **fixed-target retained-Sinkhorn route**. It does not close the annealed LEDH four-potential branch, does not reopen broad neural-OT invention, and does not claim paper-level usefulness before donor-aligned refit checks pass.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can BayesFilter refit its fixed-target retained-Sinkhorn route from a full dual-pair BayesFilter-native student into a Meta OT-aligned route that predicts one donor-style dual half, recovers the complementary half teacher-consistently, preserves corrective retained Sinkhorn, and improves the route without breaking replay/residual contracts? |
| Mechanism under test | Replace or augment the current dual-pair retained-Sinkhorn student/training path with a Meta OT-style one-half prediction route plus donor-faithful objective-based training and existing BayesFilter heldout replay diagnostics. |
| Expected failure mode | Current local route predicts both `log_u` and `log_v` directly and trains by teacher-state regression, so it may preserve deployment semantics while still failing donor-faithfulness on learned-object and objective choice. |
| Promotion criterion | A one-half predictor with teacher-side complementary recovery, donor-faithful objective-based training path, corrected retained-Sinkhorn deployment, and heldout replay/residual checks that remain at least as strong as the current local route. |
| Promotion veto | Silent fallback to dual-pair prediction, no complementary recovery path, no donor-faithful objective route, replay/residual regression after correction, or mixing annealed-route semantics into the fixed-target refit. |
| Continuation veto | Exact one-half target cannot be made well-posed under BayesFilter conventions, donor-faithful objective route cannot be implemented coherently in the TF/TFP stack, or the refit breaks corrected retained-Sinkhorn deployment semantics. |
| Repair trigger | Fixable target encoding, loss, data-manifest, student-architecture, or replay-evaluation issues with a clear local cause. |
| Explanatory diagnostics | Latent loss, training speed, parameter count, budget ladders, per-example replay metrics, and teacher residual summaries. |
| Must not conclude | No full source-faithful closure yet unless the new route passes the donor-aligned audit; no posterior correctness; no HMC readiness; no annealed-route usefulness claim; no production default change. |

## Program Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can BayesFilter refit the current fixed-target retained-Sinkhorn implementation so its learned object and training objective become Meta OT-aligned without losing the current strong corrected deployment and heldout replay checks? |
| Baseline/comparator | Current `SinkhornWarmStartStudentTF` route, current teacher-data runner, current heldout-eval runner, and the Meta OT donor-core decomposition from the completed source-faithful closure program. |
| Primary pass criterion | Each phase lands a visible artifact that tightens one part of the donor-aligned refit: target-object contract, teacher-data contract, student refit, objective-based training, heldout replay evaluation, and closeout decision. |
| Veto diagnostics | Wrong donor baseline; silent regression to dual-pair prediction; proxy latent metrics treated as success; broken corrected Sinkhorn deployment; replay/residual regression; route drift into annealed transport; missing manifests. |
| Explanatory diagnostics | Train loss curves, heldout latent error, low-budget effects, runtime, model size, example counts, and gradient/FD checks if added later. |
| Not concluded | No public-distribution license conclusion, no paper effectiveness conclusion on all routes, no annealed donor-faithfulness, no broad neural-OT success claim. |
| Required artifacts | Master program, phase subplans/results, refit-specific manifests, local checks actually run, and closeout decision. |

## Baseline And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Stay on fixed-target retained Sinkhorn | Source-faithful closure P5/P6 verdict | It is the correct Meta OT adaptation substrate | Drift back to annealed route | P0 route-boundary lock | reviewed |
| One-half prediction target | Meta OT donor-core decomposition | Closer donor alignment than current dual-pair student | Ill-posed or unstable target representation | P1 target/recovery design | hypothesis |
| Teacher-side complementary recovery | Meta OT donor-core decomposition | Prevents arbitrary free prediction of both halves | Hidden fallback to predicting both halves | P1/P3 code audit | hypothesis |
| Objective-based donor-aligned training path | Meta OT donor-core decomposition | Restores donor training semantics instead of pure pair regression | Local objective route unstable or inconsistent | P3 focused training smoke | hypothesis |
| Preserve BayesFilter replay/residual heldout checks | Existing retained-teacher local route | Keeps strong local deployment discipline while refitting donor alignment | New route looks donor-faithful but loses corrected-route evidence | P4 heldout replay result | reviewed |

## Phase Index

| Phase | Name | Objective | Subplan | Result |
| ---: | --- | --- | --- | --- |
| 0 | Scope Lock And Baseline Freeze | Freeze donor, route, baseline, and out-of-scope branches for the refit program. | `docs/plans/bayesfilter-neural-ot-metaot-refit-p0-scope-lock-subplan-2026-06-27.md` | `docs/plans/bayesfilter-neural-ot-metaot-refit-p0-scope-lock-result-2026-06-27.md` |
| 1 | One-Half Target And Recovery Contract | Define the exact one-half target, gauge/canonicalization rule, and teacher-side complementary recovery path. | `docs/plans/bayesfilter-neural-ot-metaot-refit-p1-target-recovery-subplan-2026-06-27.md` | `docs/plans/bayesfilter-neural-ot-metaot-refit-p1-target-recovery-result-2026-06-27.md` |
| 2 | Teacher-Data And Manifest Refit | Update the retained-Sinkhorn teacher-data contract so it supports donor-aligned one-half training and keeps BayesFilter manifests/replay artifacts. | `docs/plans/bayesfilter-neural-ot-metaot-refit-p2-teacher-data-subplan-2026-06-27.md` | `docs/plans/bayesfilter-neural-ot-metaot-refit-p2-teacher-data-result-2026-06-27.md` |
| 3 | Student And Objective Refit | Refit the student path toward one-half prediction and add the donor-faithful objective-based training path. | `docs/plans/bayesfilter-neural-ot-metaot-refit-p3-student-objective-subplan-2026-06-27.md` | `docs/plans/bayesfilter-neural-ot-metaot-refit-p3-student-objective-result-2026-06-27.md` |
| 4 | Heldout Replay And Residual Evaluation | Re-evaluate corrected retained-Sinkhorn replay/residual behavior under the refit route. | `docs/plans/bayesfilter-neural-ot-metaot-refit-p4-heldout-replay-subplan-2026-06-27.md` | `docs/plans/bayesfilter-neural-ot-metaot-refit-p4-heldout-replay-result-2026-06-27.md` |
| 5 | Closeout And Next Boundary | Decide whether the refit is donor-faithful enough to replace the current route, and what remains blocked or deferred. | `docs/plans/bayesfilter-neural-ot-metaot-refit-p5-closeout-subplan-2026-06-27.md` | `docs/plans/bayesfilter-neural-ot-metaot-refit-p5-closeout-result-2026-06-27.md` |
| 6 | Range-Bearing Discriminating-Rung Recovery | Recover a governed discriminating range-bearing rung after the current donor-aligned result showed saturated zero-init budgets on the candidate rung. | `docs/plans/bayesfilter-neural-ot-metaot-refit-p6-range-bearing-discriminating-rung-subplan-2026-06-29.md` | `docs/plans/bayesfilter-neural-ot-metaot-refit-p6-range-bearing-discriminating-rung-result-2026-06-29.md` |

## Repair Loop

For each material phase:
1. Run the skeptical audit before execution.
2. Execute the smallest visible change/check that answers the phase.
3. Write the phase result.
4. Refresh the next subplan if the implementation changed the boundary.
5. Keep the route boundary explicit: fixed-target retained Sinkhorn only.
6. Treat the annealed route as deferred extension work, not as a fallback target.

## Phase-6 Amendment Boundary

P5 closed the original refit program by showing that the donor-aligned route was
implemented but not promoted under the then-current heldout rule. Subsequent
better-contract runs changed that boundary:

- broader LGSSM and calibrated SV now show local usefulness on discriminating
  budgets;
- the range-bearing donor-aligned rung instead showed `saturated_zero_init` at
  budgets `10` and `20`, which means the current range-bearing rung is not a
  valid promotion/non-promotion comparator.

Therefore future range-bearing execution is governed by P6, not by ad hoc reruns
of the old range-bearing command pair. P6 requires a zero-init ladder probe on
this artifact first, then either:
- governed reuse of newly identified discriminating budgets on the same artifact,
  or
- a narrow harder-artifact amendment if the current artifact has no usable
  discriminating rung.

## Forbidden Claims And Actions

- Do not call the refit source-faithful merely because corrected deployment still works.
- Do not silently keep full dual-pair prediction while claiming Meta OT alignment.
- Do not treat latent loss alone as success.
- Do not drift into annealed-route target design inside this program.
- Do not use this program to justify public redistribution of donor-derived code.
- Do not overclaim usefulness, posterior correctness, or HMC readiness.

## Final Handoff Requirements

The final handoff for this program must state:
- whether the fixed-target route reached donor-faithful one-half semantics,
- whether the donor-style objective-based path is actually implemented and tested,
- how the corrected replay/residual contract changed versus the pre-refit baseline,
- what remains deferred (including annealed-route work),
- and the exact next human decision required.
