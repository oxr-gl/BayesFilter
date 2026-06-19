# P74 Subplan: Fresh-Audit Holdout Root-Cause Discriminator

metadata_date: 2026-06-17
status: DRAFT_FROM_P73_PHASE6_NOT_LAUNCHED
previous_program: docs/plans/bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p73-phase6-result-decision-result-2026-06-17.md
diagnostic_json: docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Identify the smallest discriminating root cause for the P73 Phase 5
fresh-audit holdout and audit-line failure before any validation, HMC,
scaling, GPU, rank promotion, threshold change, or default-policy change.

This subplan is drafted as the P73 Phase 6 handoff.  It is not launched by
P73.  Launching P74 requires a reviewed P74 runbook or explicit human
direction.

## Entry Conditions Inherited From P73

P74 may begin only if:

- P73 Phase 5 JSON exists and is a real Phase 5 artifact;
- P73 Phase 5 result records `P73_PHASE5_DENSITY_AWARE_RENEWAL_BLOCKED`;
- Phase 5 Claude micro-reviews agree that the runner, \(F_1\) construction,
  audit exclusion, post-fit gates, and bounded interpretation are valid;
- P73 Phase 6 result exists and selects this root-cause lane;
- the run is governed by a reviewed P74 runbook or explicit human direction.

## Required Artifacts

P74 should first produce:

- a constructor/provenance audit result under `docs/plans`;
- an exact ledger of the code paths and artifact fields used to construct
  \(F_0,E_0,N_1,F_1,G_1,A_1\), guard-line probes, and audit-line probes;
- a classification table for each candidate root cause:
  `runner_or_constructor_mismatch`, `target_frame_shift_or_scale_mismatch`,
  `finite_cloud_geometry_or_clipping`, `rank_degree_capacity`,
  `missing_density_aware_optimizer`, or `unresolved`;
- a next subplan only if the first audit does not identify a repairable bug.

## Required Checks/Tests/Reviews

Initial local checks should be artifact and source checks only:

```bash
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json
test -s docs/plans/bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-result-2026-06-17.md
rg -n "fresh_audit_holdout|audit_line|F1_hash|A1_hashes|shift_constant|frame_hash|line_block|residual_rms_veto|residual_max_veto|NO_AUDIT_COEFFICIENT_SELECTION" docs/plans/bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json scripts/p73_density_aware_renewal_diagnostic.py
git diff --check -- docs/plans
```

Review:

- Claude read-only review of the constructor/provenance audit plan and result;
- loop to convergence or max 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Why did P73-A fit \(F_1\) well while fresh audit holdout and audit-line gates failed catastrophically? |
| Exact baseline/comparator | P73 Phase 5 blocked JSON/result for `rank_candidate_1_2_fit36`, plus the P72 blocked context. |
| Primary criterion | Classify whether the first root cause is a runner/constructor bug, target-frame/shift/scale mismatch, cloud-geometry/clipping failure, capacity failure, missing objective failure, or unresolved. |
| Diagnostics that can veto | Any new fit, validation, HMC, scaling, GPU run, rank promotion, threshold change, or downstream readiness claim before the constructor/provenance audit is complete. |
| Explanatory only | Existing residuals, line residuals, nearest-fit distances, clipping fractions, support warnings, condition spectra, and cross-entropy values. |
| What will not be concluded | No lower-gate repair, no validation readiness, no adaptive Zhao--Cui failure, no proof that P73-B would fix the issue. |
| Artifact preserving result | P74 root-cause audit result and updated ledgers. |

## Root-Cause Hypotheses To Test In Order

1. `runner_or_constructor_mismatch`: fresh audit holdout or audit-line targets
   are generated with a different frame, shift, previous retained object, time
   index, seed semantics, or endpoint convention than the fit/guard/replay
   channels.
2. `target_frame_shift_or_scale_mismatch`: the residual scale used for gates
   is inappropriate for the fresh-audit target channel, or the source shift
   differs from the fitted branch target definition.
3. `finite_cloud_geometry_or_clipping`: the fresh audit holdout and audit-line
   clouds lie far from \(F_1\) in the finite support diagnostic and are
   saturated/clipped, so the rank-2 degree-1 square-root regression
   extrapolates badly.
4. `rank_degree_capacity`: the fixed rank/degree row fits \(F_1\) but lacks
   enough representational capacity to generalize across the audit channel.
5. `missing_density_aware_optimizer`: P73-A is only renewal plus least-squares
   square-root regression; it does not optimize the proposed density-aware
   objective.

## Forbidden Claims/Actions

- Do not rerun P73, fit a new branch, or execute new random diagnostics in the
  initial constructor/provenance audit.
- Do not run validation, HMC, scaling, GPU, or rank promotion.
- Do not change thresholds after seeing Phase 5 outputs.
- Do not treat nearest-fit distance, clipping, or cross-entropy as proof by
  itself.
- Do not call P73 renewal or P74 diagnostics source-faithful Zhao--Cui without
  paper and author-source anchors.

## Exact Next-Phase Handoff Conditions

If the constructor/provenance audit identifies a concrete implementation bug,
the next subplan must be a focused repair plan with:

- exact file/function anchors;
- a before/after artifact that would fail before repair and pass after repair;
- focused tests;
- no validation/HMC/scaling launch.

If the audit does not identify a bug, the next subplan must be a bounded
diagnostic design that separately tests cloud geometry, target scale,
rank/degree capacity, and the missing P73-B optimizer.  That diagnostic must
freeze thresholds before execution and treat short-run results as
root-cause evidence only.

## Stop Conditions

Stop and ask for human direction if:

- P73 Phase 5 artifacts cannot be parsed or appear schema/smoke-only;
- the code/artifact anchors are insufficient to audit constructor provenance;
- a proposed next action requires validation, HMC, scaling, GPU, rank
  promotion, threshold changes, package/network setup, or default-policy
  changes;
- Claude and Codex do not converge after five rounds for the same blocker.

## Skeptical Plan Audit

This handoff subplan passes an initial skeptical audit as a next step because
it targets the actual Phase 5 blocker, starts with an artifact/source audit
rather than another fit, keeps proxy metrics explanatory, forbids downstream
promotion, and separates runner bugs from scientific or numerical
limitations.

