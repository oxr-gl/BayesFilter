# P70 Phase 4 Subplan: Nondegenerate Initialization And Fitting Design

metadata_date: 2026-06-16
status: READY_AFTER_PHASE3_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 4
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Design the fixed fitting rule \(\mathcal A_t\) for the Phase 3 branch builder.
The design must give declared rank channels a mathematical opportunity to
activate, define multi-sweep fitting behavior, and freeze channel-activity,
normalizer, holdout, replay, and conditioning predicates before any
implementation or repaired diagnostic run.

Phase 4 is a design phase.  It does not edit algorithmic code, edit p50, or run
P69/P70 diagnostics.

## Entry Conditions Inherited From Phase 3

Phase 4 may begin only after Phase 3 produces:

- Phase 3 design result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase3-ukf-guided-branch-builder-design-result-2026-06-16.md`;
- a reviewed definition of \(G_t\) for
  \((\mu_t,L_t,\Omega_t,\mathcal D_t,c_t)\);
- branch identity payload requirements;
- source-governance classification for every branch-builder operation;
- exact branch-builder coverage predicate and branch-builder thresholds;
- initialization and sweep-design obligations for Phase 4;
- channel-activity, normalizer, holdout, replay, condition-number, and
  row-adequacy predicate inputs and obligations;
- Claude `VERDICT: AGREE`.

## Required Artifacts

- Phase 4 design result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase4-nondegenerate-fitting-design-result-2026-06-16.md`.
- Updated P70 visible execution ledger.
- Updated P70 Claude review ledger.
- Refreshed Phase 5 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase5-focused-implementation-tests-subplan-2026-06-16.md`.

## Required Checks/Tests/Reviews

Local read-only checks:

```bash
rg -n "FixedTTFitter|FixedTTFitConfig|_source_route_constant_path_initial_cores|max_sweeps|sweep_order|condition_number|holdout_tolerance" bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py
rg -n "zero-environment|constant-path|channel|normalizer|holdout|replay" docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex docs/plans/bayesfilter-highdim-zhao-cui-p70-*.md
rg -n "test_fixed_branch_fit|FixedTTFitter|holdout_residual_veto|rank_changed|sweep_order" tests/highdim
```

MathDevMCP should be used if Phase 4 states a proposition-like mathematical
claim about nonzero channels, gauge behavior, or normalizer predicates.  Any
MathDevMCP result is diagnostic-only unless a separate formal proof artifact is
produced.

Claude review:

- Review the Phase 4 design result and refreshed Phase 5 subplan.
- Check that the proposed fitting rule is mathematically coherent and feasible.
- Check that thresholds are frozen before implementation and diagnostics.
- Check that fit residual is not promoted to correctness.
- Check that Phase 5 is authorized to edit only exact named implementation and
  test surfaces.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What fixed initialization, sweep policy, and admissibility predicates should replace the current constant-path one-sweep source-route fit before implementation? |
| Baseline/comparator | Phase 3 branch-builder design; current constant-path initialization and one-sweep P59/P69 source-route helper; generic `FixedTTFitter` capabilities. |
| Primary criterion | Produce a design contract for \(\mathcal A_t\) with nondegenerate initialization, multi-sweep policy, row-adequacy predicates, channel-activity predicates, normalizer/holdout/replay predicates, frozen thresholds, and exact Phase 5 implementation/test scope. |
| Veto diagnostics | In-sample residual as promotion criterion; threshold chosen after repaired output; low/high closeness gate; UKF promoted to truth; source-faithful overclaim; hidden implementation; missing Phase 5 handoff. |
| Explanatory diagnostics | p50 zero-environment/constant-path propositions, current fitter anchors, P69 diagnostic findings, generic fitter tests. |
| Not concluded | No implementation, no repaired diagnostic, no validation, no scaling, no HMC readiness, no adaptive Zhao--Cui parity. |
| Artifact preserving result | Phase 4 design result and refreshed Phase 5 subplan. |

## Required Design Content

The Phase 4 result must define:

- initialization rule, including how declared nonfirst rank channels enter the
  initial cores;
- sweep count, sweep order, stopping rule, and deterministic replay identity;
- row-adequacy thresholds for the weighted raw pushed rows selected by the
  Phase 3 branch-builder coverage gate;
- ridge and condition-number policies;
- channel-activity predicates and thresholds;
- normalizer finite/bounded predicates and thresholds;
- holdout and replay predicate roles and thresholds;
- exact implementation surfaces Phase 5 may edit;
- exact focused tests Phase 5 must add or update;
- forbidden implementation shortcuts.

## Forbidden Claims/Actions

- Do not edit algorithmic code.
- Do not edit p50.
- Do not run P69 Phase 5c or any repaired diagnostic.
- Do not run validation ladders.
- Do not claim the design fixes the bug until Phase 5/6 evidence exists.
- Do not make a `source_faithful` claim without direct paper and author-source
  anchors.
- Do not make low/high branch closeness a gate.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only if Phase 4 produces:

- reviewed initialization and fitting design;
- all thresholds needed before implementation and Phase 6 diagnostics;
- exact implementation-surface list;
- exact focused test list;
- refreshed Phase 5 implementation subplan;
- Claude `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- no nondegenerate initialization can be stated without an unreviewed
  invention decision;
- channel-activity predicates cannot be made meaningful under the chosen gauge;
- threshold choices would require observing repaired diagnostic output;
- Phase 5 would need broader code edits than Phase 4 can justify;
- Claude and Codex do not converge after five material review rounds.

## Skeptical Plan Audit

The known Phase 4 risk is choosing a fitting rule because it improves the
training residual while leaving rank channels inactive or normalizers unstable.
The design must make structural channel activity and normalizer/holdout/replay
predicates primary gates for later diagnostics.
