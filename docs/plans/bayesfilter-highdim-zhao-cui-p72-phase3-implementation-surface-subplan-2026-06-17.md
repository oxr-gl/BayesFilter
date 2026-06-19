# P72 Phase 3 Subplan: Implementation Surface Audit And Focused Test Plan

metadata_date: 2026-06-17
status: READY_FOR_PHASE3_EXECUTION_CLAUDE_R3_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Map the Phase 2 support-certified design contract to exact implementation
surfaces and tests before code edits.  Phase 3 is a design and audit phase
only.  It does not edit production code, does not run repaired diagnostics,
and does not authorize downstream validation.

## Entry Conditions Inherited From Phase 2

Phase 3 may begin only if:

- Phase 2 result exists and contains the frozen design contract:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-result-2026-06-17.md`;
- every Phase 2 design element has a Phase 1-compatible classification label;
- every imported P70/P71 observable is mapped to a Phase 1 classification row;
- thresholds and observables are frozen before implementation;
- Claude returns `VERDICT: AGREE` for the Phase 2 result and this Phase 3
  subplan;
- no production code edit or repaired diagnostic has occurred in P72.

## Required Artifacts

Phase 3 must produce:

- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-result-2026-06-17.md`;
- implementation-surface map listing exact files, functions, dataclasses, and
  tests Phase 4 may edit;
- no-edit audit of current code surfaces for:
  `FixedTTFitSampleBatch`, `FixedTTFitConfig`, `FixedTTFitter.fit`,
  `_p59_fixed_ttsirt_transport_from_values`,
  `_p69_author_sir_source_diagnostic_data_for_step`,
  `_p69_post_fit_holdout_replay_diagnostics`,
  `_p70_channel_activity_diagnostics`,
  `_p70_fixed_fitting_policy_payload`, and the P70/P71 diagnostic scripts;
- focused test plan for cloud construction, guard augmentation, audit
  separation, residual gates, line gates, normalizer gates, conditioning gates,
  effective-rank convention, and rank-channel activity;
- updated execution and review ledgers;
- refreshed Phase 4 implementation subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-subplan-2026-06-17.md`.

## Required Checks, Tests, And Reviews

Local read-only checks before writing the Phase 3 result:

```bash
test -f docs/plans/bayesfilter-highdim-zhao-cui-p72-phase2-support-certified-design-result-2026-06-17.md
rg -n "FixedTTFitSampleBatch|FixedTTFitConfig|FixedTTFitter|_p59_fixed_ttsirt_transport_from_values|_p69_author_sir_source_diagnostic_data_for_step|_p69_post_fit_holdout_replay_diagnostics|_p70_channel_activity_diagnostics" bayesfilter/highdim/fitting.py bayesfilter/highdim/source_route.py
rg -n "holdout_replay|line_stability|condition|normalizer|rank_channel|effective_rank|scaled_augmented" scripts/p70_phase6h_root_cause_probes.py scripts/p70_phase6_rank_channel_normalizer_diagnostic.py tests/highdim/test_p70_phase6_diagnostic_script.py
```

Local checks after writing Phase 3 result and Phase 4 subplan:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-claude-review-ledger-2026-06-17.md
rg -n "bayesfilter/highdim/fitting.py|bayesfilter/highdim/source_route.py|scripts/|tests/|forbidden|not concluded|TensorFlow|extension_or_invention|fixed_hmc_adaptation" docs/plans/bayesfilter-highdim-zhao-cui-p72-phase3-implementation-surface-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-subplan-2026-06-17.md
```

Reviews:

- Codex skeptical plan audit before Phase 3 execution.
- Claude read-only review of the Phase 3 result and Phase 4 subplan.
- If Claude returns `VERDICT: REVISE`, patch visibly and rerun focused checks.
  Stop after five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which exact code surfaces and focused tests are necessary and sufficient to implement the Phase 2 support-certified lower gate? |
| Baseline/comparator | Phase 2 design contract and current TensorFlow fixed-branch implementation surfaces. |
| Primary criterion | Produce a complete no-edit surface map and Phase 4 implementation/test subplan that covers every mandatory Phase 2 design element and excludes quarantined candidates. |
| Veto diagnostics | Missing implementation surface for a mandatory gate; code edits in Phase 3; unaudited shape/stable-LS/Christoffel candidate entering Phase 4; NumPy used for BayesFilter algorithmic implementation; audit clouds accidentally allowed into coefficient selection; downstream validation authorized. |
| Explanatory only | Estimated edit size, possible helper names, optional future refactors, and runtime estimates. |
| Not concluded | No implementation, no repaired diagnostic, no pass/fail evidence, no d18 validation, no HMC readiness, no source-faithfulness closure for guard/stability additions. |
| Artifact preserving result | Phase 3 result, execution ledger, review ledger, and Phase 4 subplan. |

## Expected Surface Categories

Phase 3 must decide whether Phase 4 needs:

- a support-certified sample-batch or fitting wrapper that can concatenate
  `Z_fit` and `Z_guard` without mixing `Z_audit`;
- target-evaluation helpers for arbitrary local guard/audit/line points in the
  fixed source-route frame;
- diagnostic payload fields for cloud hashes, seed manifests, residual gates,
  line gates, normalizer gates, singular spectra, effective rank, and
  activity gates;
- a bounded P72 diagnostic script or a reviewed extension of the P70/P71
  diagnostic scripts;
- focused unit tests for the gate schema and for synthetic pass/fail cases.

## Forbidden Claims And Actions

- Do not edit production code in Phase 3.
- Do not run repaired diagnostics, validation ladders, d18 validation, HMC, or
  GPU diagnostics.
- Do not authorize shape penalties, derivative penalties, line-growth
  objective penalties, Christoffel/leverage/oversampling rules, or stable-LS
  theorem claims.
- Do not weaken or move Phase 2 thresholds.
- Do not represent extension gates as source-faithful Zhao--Cui behavior.
- Do not use NumPy as the implementation backend for BayesFilter-owned
  algorithmic paths.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- Phase 3 result exists and covers every mandatory Phase 2 design element;
- Phase 4 subplan exists and lists exact files/functions/tests authorized for
  edit;
- Phase 4 subplan preserves TensorFlow/TensorFlow Probability backend policy;
- Phase 4 subplan forbids downstream validation and repaired full validation
  ladders;
- local checks pass;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- a mandatory Phase 2 gate has no feasible implementation surface without a
  broader redesign;
- audit and guard data cannot be separated cleanly;
- target evaluation for arbitrary guard/audit/line points would require an
  unreviewed route change;
- implementation would require package installation, network access, or
  changing default backend policy;
- Claude and Codex do not converge after five review rounds for the same
  blocker;
- the user redirects the lane.

## Skeptical Plan Audit

This phase is justified because Phase 2 froze the design contract.  The main
risk is editing too early or letting old P70/P71 diagnostic vocabulary drag in
unclassified behavior.  Phase 3 controls that risk by requiring a no-edit
surface map and a reviewed Phase 4 subplan before implementation begins.
