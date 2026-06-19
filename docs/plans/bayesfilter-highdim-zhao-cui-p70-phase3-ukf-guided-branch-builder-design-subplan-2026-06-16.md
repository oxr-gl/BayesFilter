# P70 Phase 3 Subplan: UKF-Guided Branch-Builder Design

metadata_date: 2026-06-16
status: READY_AFTER_PHASE2_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Design the fixed branch construction \(G_t\) that maps scout and source-route
inputs to frozen branch objects
\[
  G_t \mapsto
  (\mu_t,L_t,\Omega_t,\mathcal D_t,c_t,\text{branch identity fields}).
\]

The UKF may guide the center, covariance orientation, scale bounds, and design
measure proposal.  It remains scout evidence only.  Phase 3 writes a design
contract; it does not implement the branch builder and does not run
diagnostics.

## Entry Conditions Inherited From Phase 2

Phase 3 may begin only after Phase 2 produces:

- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase2-current-code-gap-audit-result-2026-06-16.md`;
- gap ledger for \(\mu_t,L_t,\Omega_t,\mathcal D_t,c_t\);
- gap ledger for nondegenerate initialization, sweep policy, and
  channel-activity predicates;
- gap ledger for normalizer, holdout, and replay predicates;
- list of exact code surfaces Phase 3 may design against;
- list of surfaces Phase 3 must not touch;
- Claude `VERDICT: AGREE` for Phase 2 and this Phase 3 subplan.

## Required Artifacts

- Phase 3 design result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase3-ukf-guided-branch-builder-design-result-2026-06-16.md`.
- Updated P70 visible execution ledger.
- Updated P70 Claude review ledger.
- Refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase4-nondegenerate-fitting-design-subplan-2026-06-16.md`.

## Required Checks/Tests/Reviews

Local read-only checks:

```bash
rg -n "P52_UKF_SCOUT_CLAIM|scout_not_truth|UKF scout cannot promote stronger claims|UKF is diagnostic only" bayesfilter/highdim/ukf_scout.py bayesfilter/highdim/rank_budget.py
rg -n "SourceRouteCoordinateFrame|source_route_recenter|_p59_author_sir_source_fit_data_for_step|_p59_fixed_ttsirt_transport_from_values|SourceRouteNormalizerContribution|source_route_log_normalizer_update" bayesfilter/highdim/source_route.py
rg -n "source_faithful|fixed_hmc_adaptation|extension_or_invention|UKF-guided|branch-builder|channel-activity" docs/plans/bayesfilter-highdim-zhao-cui-p70-*.md
```

Optional MathDevMCP checks are allowed only for equations or proposition-style
claims introduced in the Phase 3 design result.  They are diagnostic-only
unless a separate formal proof artifact is produced.

The `rg` checks above are smoke checks for anchor and boundary presence.  They
do not certify that the design contract is correct or adequate.

Claude review:

- Review the Phase 3 design result and refreshed Phase 4 subplan.
- Check source-governance classifications.
- Check that UKF scout metadata is not promoted to correctness, rank, or HMC
  readiness.
- Check that the design produces exact Phase 4 entry conditions.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What fixed branch-builder design should replace the current implicit source-route construction before nondegenerate fitting is designed? |
| Baseline/comparator | Phase 2 gap ledger; current empirical source-route localization and one-sweep constant-path fixed-TTSIRT route; UKF scout nonclaims. |
| Primary criterion | Produce a human-readable mathematical/design contract for \(G_t\) that freezes \(\mu_t,L_t,\Omega_t,\mathcal D_t,c_t\), records branch identity fields, classifies every operation under source governance, and hands exact initialization/fitting requirements to Phase 4. |
| Veto diagnostics | UKF promoted to truth; source-faithful claim without paper and author-source anchors; low/high closeness gate; design depends on repaired diagnostic output not yet produced; hidden implementation; missing Phase 4 handoff; threshold chosen after observing repaired diagnostics. |
| Explanatory diagnostics | Code anchors from Phase 2, UKF scout manifest fields, source-route localization anchors, branch-identity payload requirements, threshold-provenance notes. |
| Not concluded | No implementation, no repaired diagnostic, no validation, no scaling, no HMC readiness, no adaptive Zhao--Cui parity. |
| Artifact preserving result | Phase 3 design result and refreshed Phase 4 subplan. |

## Required Design Content

The Phase 3 result must define:

1. A branch-builder map \(G_t\) with inputs:
   - model and observation prefix;
   - optional previous retained object;
   - UKF scout result;
   - source-route sample/push information, if retained in the design;
   - deterministic seeds and branch-builder thresholds.
2. Outputs:
   - \(\mu_t\);
   - \(L_t\), including covariance/eigenvalue/jitter policy;
   - \(\Omega_t\), including local cube or alternative bounded domain;
   - \(\mathcal D_t\), including local design points and weights;
   - \(c_t\), including whether it is the fit-row minimum of the local
     negative log target or another frozen scalar;
   - branch identity fields sufficient for replay.
3. Classification of each operation:
   - `source_faithful`;
   - `fixed_hmc_adaptation`;
   - `extension_or_invention`;
   with paper/source anchors where required.
   Any `source_faithful` row must repeat the direct Zhao--Cui paper
   section/equation/algorithm anchors inline, not only references to project
   ledgers.
4. Nonclaims:
   - UKF is not truth;
   - branch construction is not adaptive Zhao--Cui parity;
   - no rank/degree/normalizer validation is established.
5. Exact requirements handed to Phase 4:
   - whether initialization must be channel-seeded;
   - whether fitting must use more than one sweep;
   - channel-activity predicate inputs;
   - normalizer/holdout/replay predicate dependencies;
   - thresholds that must be frozen before Phase 5 implementation or Phase 6
     diagnostics.

## Forbidden Claims/Actions

- Do not edit algorithmic code.
- Do not edit p50.
- Do not run P69 Phase 5c or any repaired diagnostic.
- Do not choose thresholds after looking at repaired output.
- Do not claim UKF-guided branch construction is source-faithful unless the
  exact operation has both Zhao--Cui paper and author-source anchors.
- Do not claim the Phase 3 design fixes the rank-channel or normalizer bug.
- Do not require low and high branch outputs to be close.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only if Phase 3 produces:

- a reviewed mathematical/design definition of \(G_t\);
- a branch identity payload specification;
- a source-governance table for every branch-builder operation;
- frozen branch-builder thresholds or a blocker explaining why they cannot yet
  be frozen;
- exact initialization and sweep-design obligations for Phase 4;
- exact channel-activity, normalizer, holdout, and replay predicate inputs that
  Phase 4 must design around;
- a refreshed Phase 4 subplan;
- Claude `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- the UKF-guided design cannot be classified without a new human decision about
  `extension_or_invention`;
- required paper/source anchors for a claimed source-faithful operation are
  missing;
- branch-builder thresholds cannot be stated without observing repaired
  diagnostics;
- Phase 4 would require implementation evidence Phase 3 does not produce;
- Claude and Codex do not converge after five material review rounds.

## Skeptical Plan Audit

The known Phase 3 risk is turning a useful UKF scout into a correctness oracle.
The design must keep the UKF as a deterministic proposal mechanism for a fixed
branch, not as evidence that the branch is correct, stable, source-faithful, or
HMC-ready.
