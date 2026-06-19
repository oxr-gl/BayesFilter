# P70 Phase 2 Subplan: Current-Code Gap Audit

metadata_date: 2026-06-16
status: READY_AFTER_PHASE1_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Audit the current BayesFilter code against the Phase 1 mathematical
fixed-branch contract.  Phase 2 must classify each required object as present,
partial, missing, or blocked, with code/file anchors.  Phase 2 does not
implement repairs and does not run repaired diagnostics.

## Entry Conditions Inherited From Phase 1

Phase 2 may begin only after Phase 1 produces:

- the Phase 1 mathematical fixed-branch contract result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase1-mathematical-fixed-branch-contract-result-2026-06-16.md`;
- source/fixed-adaptation classification for UKF-guided branch construction;
- constant-path reconciliation;
- Zhao--Cui paper-anchor additions or quarantine for every operation claimed as
  `source_faithful`;
- mathematical diagnostic predicates with threshold-provenance responsibilities;
- a boundary note stating that Phase 1 defines predicates but does not
  authorize diagnostic execution or empirical ladders;
- implementation-surface list;
- local document checks and diagnostic-only MathDevMCP notes recorded in the
  visible execution ledger;
- Claude `VERDICT: AGREE`.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase2-current-code-gap-audit-result-2026-06-16.md`.
- Updated P70 visible execution ledger.
- Updated P70 Claude review ledger.
- Refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase3-ukf-guided-branch-builder-design-subplan-2026-06-16.md`.

## Required Checks/Tests/Reviews

Local read-only checks:

```bash
rg -n "max_sweeps|_source_route_constant_path_initial_cores|FixedTTFitConfig|FixedTTFitter|holdout|replay" bayesfilter/highdim/source_route.py bayesfilter/highdim/fitting.py
rg -n "scout_not_truth|UKF is diagnostic only|P57_ALLOWED_UKF_CLAIM_CLASS" bayesfilter/highdim/ukf_scout.py bayesfilter/highdim/rank_budget.py
rg -n "p69_phase5c|rank_activity|channel|normalizer" scripts tests docs/plans
```

Optional focused Python import checks are allowed only if the Phase 2 result
needs to verify exported names.  They must be CPU-only and must not run
diagnostics.

Claude review:

- Review the gap map and Phase 3 subplan.
- Check that no code repair is hidden in the audit.
- Check that every `source_faithful`, `fixed_hmc_adaptation`, or
  `extension_or_invention` classification has the required anchors.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which current code surfaces already implement the Phase 1 fixed-branch contract, which are partial, and which are missing before a UKF-guided branch-builder design can be written? |
| Baseline/comparator | Phase 1 mathematical contract, current `source_route.py`, `fitting.py`, `ukf_scout.py`, `rank_budget.py`, P69 Phase 5c diagnostics, and existing tests/scripts. |
| Primary criterion | Produce a code-gap ledger mapping each Phase 1 mathematical object and predicate to present/partial/missing/blocked code surfaces with exact anchors and no repair implementation. |
| Veto diagnostics | Code edits; diagnostic rerun; source-faithful claim without paper/source anchors; UKF promoted to truth; low/high closeness gate; Phase 3 requires implementation evidence not produced by Phase 2. |
| Explanatory diagnostics | `rg` outputs, code anchors, test/script anchors, existing manifest fields, dirty-worktree scope. |
| Not concluded | No repaired branch, no validation, no scaling, no HMC readiness, no Phase 6/7 authorization. |
| Artifact preserving result | Phase 2 result and refreshed Phase 3 subplan. |

## Forbidden Claims/Actions

- Do not edit algorithmic code.
- Do not edit p50.
- Do not run P69 Phase 5c or any repaired diagnostic.
- Do not write Phase 3 implementation code.
- Do not claim the current code satisfies the full Phase 1 contract.
- Do not convert UKF scout metadata into correctness evidence.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only if Phase 2 produces:

- a gap ledger for \(\mu_t,L_t,\Omega_t,\mathcal D_t,c_t\);
- a gap ledger for nondegenerate initialization, sweep policy, and
  channel-activity predicates;
- a gap ledger for normalizer, holdout, and replay predicates;
- a list of exact code surfaces Phase 3 may design against;
- a list of surfaces Phase 3 must not touch without a later implementation
  phase;
- a refreshed Phase 3 design subplan;
- Claude `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- a required code surface cannot be inspected;
- current dirty worktree changes make code anchors ambiguous;
- source-governance classification cannot be made without new paper/source
  evidence;
- a Phase 3 design would require implementation evidence Phase 2 did not
  produce;
- Claude and Codex do not converge after five material review rounds.

## Skeptical Plan Audit

Known risk: silently implementing while auditing.  Phase 2 is read-only except
for result/subplan/ledger artifacts.  Any repair belongs to Phase 5 or a later
reviewed implementation phase.
