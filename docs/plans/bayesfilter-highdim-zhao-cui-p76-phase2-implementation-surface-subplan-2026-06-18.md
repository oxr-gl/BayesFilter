# P76 Phase 2 Subplan: Implementation Surface And Test Plan

metadata_date: 2026-06-18
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE2
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase1-mathematical-ukf-initializer-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Translate the Phase 1 mathematical contract for
`ukf_whitened_gaussian_sqrt_projection_v1` into a concrete, scoped
implementation and test surface.  Phase 2 is still a planning phase: it names
the implementation edits for Phase 3 but does not edit implementation code.

## Entry Conditions Inherited From Phase 1

Phase 2 may begin only if:

- Phase 1 result exists;
- Phase 1 defines \(m_U,P_U\), the local map, \(h_0\), covariance floors, and
  mini-batch handoff;
- Phase 1 forbids source-route prefit as a substitute initializer target;
- Phase 1 excludes audit samples from initialization, mini-batch training,
  stopping, and selection;
- Phase 1 local checks pass;
- Claude agrees Phase 1 and this subplan are consistent, or repairable issues
  are patched and re-reviewed.

## Required Artifacts

Phase 2 must produce:

- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase2-implementation-surface-result-2026-06-18.md`;
- reviewed Phase 3 implementation subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase3-optin-ukf-initializer-implementation-subplan-2026-06-18.md`;
- updated execution and Claude review ledgers;
- updated runbook Phase Index, if Phase 3 artifact paths are finalized.

## Required Checks/Tests/Reviews

Local checks:

```bash
rg -n "m_U|P_U|h_0|ukf_whitened_gaussian_sqrt_projection_v1|scout_not_truth|source-route prefit|mini-batch|audit|TensorFlow|TrainableFunctionalTT" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase2-implementation-surface-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase3-optin-ukf-initializer-implementation-subplan-2026-06-18.md
rg -n "class UKFScoutResult|mean_path|covariance_path|P52_UKF_SCOUT_CLAIM|spatial_sir_ukf_scout" bayesfilter/highdim/ukf_scout.py
rg -n "class P75TrainableTTConfig|class TrainableFunctionalTT|class P75ObjectiveBatch|def train_step|def snapshot_density" bayesfilter/highdim/stochastic_density_training.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p76-phase2-implementation-surface-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase3-optin-ukf-initializer-implementation-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
```

Review:

- Claude read-only review of the Phase 2 result and Phase 3 subplan;
- MathDevMCP may be used if a labeled derivation is introduced;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What exact implementation and test surface should realize the Phase 1 UKF initializer? |
| Exact baseline/comparator | Phase 1 design, current `ukf_scout.py`, and current `stochastic_density_training.py`. |
| Primary criterion | Phase 2 names concrete functions/classes, file edits, focused tests, manifests, CPU-only checks, and stop conditions for Phase 3. |
| Diagnostics that can veto | Implementation surface substitutes source-route prefit; uses NumPy as BayesFilter implementation backend; lacks audit separation; lacks covariance validity tests; lacks degree >= 2 guard for curvature tests; changes defaults; authorizes large mini-batch pilot. |
| Explanatory only | Estimated test runtime, helper naming, expected core shapes, candidate manifest keys. |
| What will not be concluded | No implementation, no empirical initializer success, no lower-gate repair, no validation/HMC readiness. |
| Artifact preserving result | Phase 2 result, Phase 3 subplan, ledgers, Claude review. |

## Required Surface Decisions

The Phase 2 result must decide:

- whether to create a new opt-in module, for example
  `bayesfilter/highdim/ukf_initializer.py`, or extend the P75 experimental
  training module;
- exact dataclass names for config/result payloads;
- exact helper names for adjacent moment extraction, covariance stabilization,
  local-frame construction, one-dimensional Gaussian square-root projection,
  TT-core construction, rank embedding, and trainable-TT initialization;
- exact manifest fields preserving `scout_not_truth`, \(m_U,P_U\), \(h_0\),
  degree/rank, covariance floors, \(\gamma\), projection quadrature, and
  nonclaims;
- exact focused tests for finite moments, covariance flooring, degree guard,
  rank-one/product core shape, rank embedding, audit exclusion, and
  no source-route prefit use;
- exact CPU-only commands for Phase 3.

## Forbidden Claims/Actions

- Do not edit implementation code in Phase 2.
- Do not run training diagnostics in Phase 2.
- Do not use GPU/CUDA.
- Do not use NumPy as the BayesFilter implementation backend.
- Do not change package exports or defaults unless Phase 2 explicitly defers
  that decision to a later human-approved phase.
- Do not authorize a large mini-batch pilot.
- Do not claim source-faithful Zhao--Cui behavior.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- Phase 2 result exists;
- Phase 3 implementation subplan exists;
- the Phase 3 subplan names exact files that may be edited;
- the Phase 3 subplan names exact tests and CPU-only commands;
- the implementation route preserves TensorFlow/TensorFlow Probability as the
  BayesFilter implementation backend;
- source-route prefit remains forbidden as \(h_0\);
- Claude agrees, or a blocker is escalated.

## Stop Conditions

Stop if:

- current code lacks enough UKF moment information to implement the Phase 1
  \(m_U,P_U\) route;
- ProductBasis cannot support deterministic projection without an unreviewed
  backend exception;
- the only implementable warm start is source-route prefit;
- audit separation cannot be checked in focused tests;
- Phase 3 would require GPU/CUDA, package installation, network fetch, default
  behavior changes, or a large mini-batch pilot;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

Phase 2 is intentionally a surface-planning phase.  It blocks if the concrete
implementation path would answer a different question than Phase 1, especially
if it drifts back into the P75 source-route prefit route.
