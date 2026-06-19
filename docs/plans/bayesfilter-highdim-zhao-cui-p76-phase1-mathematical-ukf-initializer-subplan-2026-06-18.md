# P76 Phase 1 Subplan: Mathematical UKF Initializer Contract

metadata_date: 2026-06-18
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE1
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase0-closeout-boundary-reset-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Define the actual UKF-informed warm-start initializer mathematically before any
implementation edits.  The result must specify the route from UKF scout moments
\((m_U,P_U)\) to a trainable TT square-root initializer \(h_0\), and how
mini-batch stochastic density training will start from that initializer.

## Entry Conditions Inherited From Phase 0

Phase 1 may begin only if:

- Phase 0 result exists;
- P75 erratum remains active;
- P76 master program and runbook exist;
- Phase 0 preserves UKF as `scout_not_truth`;
- Phase 0 forbids source-route prefit as a substitute target;
- Phase 0 local checks pass;
- Claude agrees Phase 0 and this subplan are consistent, or fixable issues are
  patched and re-reviewed.

## Required Artifacts

Phase 1 must produce:

- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase1-mathematical-ukf-initializer-result-2026-06-18.md`;
- reviewed Phase 2 implementation-surface subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase2-implementation-surface-subplan-2026-06-18.md`;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Local checks:

```bash
rg -n "m_U|P_U|h_0|scout_not_truth|source-route prefit|mini-batch|audit" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase1-mathematical-ukf-initializer-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase2-implementation-surface-subplan-2026-06-18.md
rg -n "P52_UKF_SCOUT_CLAIM|scout_not_truth|UKF scout cannot promote stronger claims|spatial_sir_ukf_scout" bayesfilter/highdim/ukf_scout.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p76-phase1-mathematical-ukf-initializer-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase2-implementation-surface-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md
```

Review:

- Claude read-only review of the Phase 1 result and Phase 2 subplan;
- MathDevMCP checks may be used for labeled derivations if the result adds
  LaTeX labels;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What exact UKF-moment initializer should P76 implement before mini-batch density training? |
| Exact baseline/comparator | P75 historical failures and p50/P70 UKF scout contracts. |
| Primary criterion | The result must define \(m_U,P_U\), their map to fixed local coordinates, the initializer target \(h_0\), projection/fitting objective, finite/flooring rules, mini-batch handoff, and audit separation. |
| Diagnostics that can veto | Source-route prefit renamed as UKF; missing coordinate map; missing covariance validity/flooring; UKF promoted to truth; audit leakage; no implementable projection/fitting objective; large-pilot authorization. |
| Explanatory only | UKF moment spectra, covariance conditioning, proposed projection residuals, expected optimizer losses, historical P75 diagnostics. |
| What will not be concluded | No implementation, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy, no source-faithfulness. |
| Artifact preserving result | Phase 1 result, Phase 2 subplan, ledgers, Claude review. |

## Required Mathematical Content

The Phase 1 result must define:

- the source of \(m_U,P_U\) and the exact time/adjacent-state convention;
- the map from physical UKF moments to fixed local coordinate moments;
- covariance symmetrization, eigenvalue floors, truncation/domain handling, and
  failure conditions;
- the initial square-root target \(h_0\);
- whether \(h_0\) is represented by direct TT projection, supervised fitting to
  UKF-generated points, quadrature, or another reviewed finite objective;
- how the mini-batch density objective starts from the initialized parameters;
- why the design is not source-route prefit;
- what audit data are excluded from initialization/training/stopping/selection.

## Forbidden Claims/Actions

- Do not edit implementation code in Phase 1.
- Do not run training diagnostics in Phase 1.
- Do not claim UKF initialization works.
- Do not use source-route prefit as the initializer target.
- Do not use audit samples for design selection.
- Do not authorize the large mini-batch pilot.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- Phase 1 result exists;
- Phase 2 subplan exists;
- the UKF initializer is mathematically defined in terms of \(m_U,P_U\);
- the projection/fitting route for \(h_0\) is implementable in the current
  TensorFlow/TensorFlow Probability default backend, or an explicit blocker is
  written;
- source-route prefit is not used as a substitute target;
- Claude agrees, or a blocker is escalated.

## Stop Conditions

Stop if:

- no current code or documented route can provide finite UKF moments for the
  target setting;
- the local-coordinate moment map cannot be defined without changing the
  scientific target;
- the only feasible design is source-route prefit under another name;
- the initializer objective cannot be separated from audit data;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

This subplan is the guardrail against the P75 failure mode.  It forces the
UKF moment map and \(h_0\) target to exist on paper before implementation, and
it blocks if the design collapses back into source-route square-root prefit.
