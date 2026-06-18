# Phase 9 Subplan: Sliced/Subspace/Minibatch Exploratory Lane

Date: 2026-06-17
Draft timestamp: 2026-06-18T04:02:30+08:00

## Phase Objective

Design and, if checks pass, run a bounded exploratory diagnostic for
projection-based sliced/subspace OT as a semantic-replacement resampling lane.

Phase 9 must preserve the distinction between:

- projected one-dimensional or low-dimensional transport objects; and
- a full-state BayesFilter resampling transform.

Mini-batch/BoMb remains blocked for decision-grade execution because the local
source audit records `source_partial_user_needed`.  Phase 9 may mention the
Mini-batch blocker and carry it forward, but it must not execute Mini-batch,
BoMb, POT, or partial source code without a new user-approved source-repair
plan.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result records `PHASE_1_BASELINE_FIXTURE_PASSED`.
- Phase 2 result records
  `PHASE_2_CANDIDATE_AUDITS_PASSED_WITH_USER_APPROVED_MICRO_REVIEW_RESOLUTION`.
- Phase 3 result records `PHASE_3_COMMON_INTERFACE_HARNESS_PASSED`.
- Phase 4 result records `PHASE_4_NYSTROM_PROTOTYPE_PASSED`.
- Phase 5 result records
  `PHASE_5_POSITIVE_FEATURE_PROTOTYPE_PASSED_SEMANTIC_REPLACEMENT`.
- Phase 6 result records
  `PHASE_6_LOW_RANK_COUPLING_TRANSPORT_OBJECT_FIXTURE_PASSED`.
- Phase 7 result records
  `PHASE_7_EXACT_ONLINE_GPU_REFERENCE_ONLY_PASSED`.
- Phase 8 result records
  `PHASE_8_SPARSE_LOCALITY_DIAGNOSTIC_COMPLETED_BLOCKS_SPARSE_IMPLEMENTATION_FOR_NOW`.
- Phase 8 blocks sparse implementation for now.  Phase 9 must not inherit or
  implement sparse/localized solver work.
- Sliced/subspace audit records `source_locked` and semantic replacement /
  exploratory surrogate.
- Mini-batch/BoMb audit records `source_partial_user_needed` and remains
  blocked.
- No sparse speedup, sliced/subspace equivalence, minibatch viability, ranking,
  posterior correctness, or default readiness has been claimed.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p09-sliced-subspace-minibatch-result-2026-06-17.md`
- If execution proceeds, diagnostic script:
  `docs/benchmarks/scalable_ot_p09_sliced_subspace_diagnostics.py`
- If execution proceeds, JSON result:
  `docs/benchmarks/scalable-ot-p09-sliced-subspace-diagnostics-2026-06-17.json`
- If execution proceeds, Markdown result:
  `docs/benchmarks/scalable-ot-p09-sliced-subspace-diagnostics-2026-06-17.md`
- Updated execution ledger and stop handoff.
- Phase 10 comparative decision subplan draft:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-subplan-2026-06-17.md`

## Source Anchors Required Before Execution

| Anchor | Required use |
| --- | --- |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-sliced-subspace-audit-2026-06-17.md` | Paper-note-code-execution matrix and semantic-replacement contract for projection methods. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-minibatch-bomb-audit-2026-06-17.md` | Mini-batch blocker that must be carried forward without execution. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` lines 892-973 | Monotone 1D transport, sliced Wasserstein, empirical projection average, max-sliced objective, and full-state warning. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-source-lock-result-2026-06-17.md` lines 83-84 and 96-97 | Sliced/subspace source-locked posture and Mini-batch source blocker. |
| `.localsource/scalable_ot_code_audit/MANIFEST.md` lines 109-110 and 176-212 | POT sliced plan source posture and Mini-batch/BoMb partial-source risk. |

## Required Checks, Tests, And Reviews

Before execution:

1. Re-read the sliced/subspace audit, Mini-batch/BoMb audit, Phase 8 result,
   Phase 3 schema, and source anchors above.
2. Record semantic posture before execution:
   - `semantic_replacement` for any projected/full-state heuristic output;
   - `reference_only` for source/library inspection;
   - never `exact_semantics` unless a full-state coupling and dense parity
     contract are separately reviewed.
3. Define the projection diagnostic before running:
   - fixed deterministic projection directions derived from fixture dimension;
   - one-dimensional monotone matching or quantile interpolation semantics;
   - explicit reconstruction rule for full-state particle output, if any;
   - projected transport residuals separate from full-state particle error;
   - projected reconstruction consistency tolerance no looser than `1.0e-8`
     when a full-state output is reconstructed from projection displacements;
   - dense-reference error treated as explanatory only.
4. Confirm Mini-batch/BoMb remains blocked and no partial-source code is run.
5. Confirm no package installation, network fetch, POT execution, GPU evidence,
   or non-TensorFlow BayesFilter default route is required.

If diagnostic proceeds:

1. Syntax/import check for the diagnostic script.
2. Small deterministic CPU-scoped run on Phase 1 fixtures.
3. JSON/Markdown artifacts that record projection directions, projected
   monotone matching diagnostics, full-state reconstruction rule, finite
   particles, dense-reference discrepancy, and non-claims.
4. If a Phase 3 candidate record is emitted, it must use transport object kind
   `projection_plan` or `projected_output` and semantic class
   `semantic_replacement`.
5. Hard-veto diagnostics must include finite projected outputs, finite
   reconstructed particles if computed, deterministic projection metadata,
   projected reconstruction consistency at tolerance `1.0e-8` if full-state
   reconstruction is computed, and no Mini-batch execution.

Review:

- Phase 9 is material because it may execute a semantic-replacement diagnostic.
  Run local checks first, then use Claude as read-only reviewer for the subplan
  or material repairs.
- Claude cannot authorize dense-equivalence, ranking, default-readiness, or
  Mini-batch unblocking.
- Stop after five review rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a deterministic projection-based transport diagnostic produce finite, explicitly semantic-replacement resampling outputs worth carrying into the final comparative decision? |
| Baseline/comparator | Phase 1 dense TensorFlow transported particles for descriptive semantic delta only, not dense-equivalence promotion. |
| Primary pass criterion | Either a reviewed result closes Phase 9 as exploratory-only, or a diagnostic artifact records fixed projection directions, projected transport semantics, finite outputs, dense-reference discrepancy, Mini-batch blocker preservation, and non-claims. |
| Promotion veto | Distance-only result treated as particles; missing reconstruction rule; random projection single-run ranking; dense entropic equivalence claim; Mini-batch partial source executed; scalar minibatch cost treated as resampling map; non-TensorFlow default route. |
| Continuation veto | Projection diagnostic requires package installation, network fetch, POT execution, GPU evidence, external code, or unblocking Mini-batch/BoMb; full-state reconstruction cannot be defined before execution; local checks fail outside a repair trigger. |
| Repair trigger | Projection direction determinism, sorting/tie convention, full-state reconstruction text, artifact-schema issue, fixture-selection issue, or non-claim wording gap. |
| Explanatory diagnostics | Projected sorting residuals, finite output checks, dense-reference particle error, projection count/dimension, runtime/memory proxy, and sensitivity notes. |
| Not concluded | No dense OT equivalence, no posterior correctness, no production/default readiness, no ranking, no HMC-readiness, and no Mini-batch viability. |
| Artifact preserving result | Phase 9 diagnostics if run, result note, ledger, stop handoff, and Phase 10 subplan. |

## Skeptical Plan Audit

- Wrong baseline: Phase 9 must compare only descriptively against Phase 1 dense
  TensorFlow particles; exact dense coupling parity is not the target.
- Proxy metric risk: projection count, runtime, and implementation simplicity
  are explanatory only.
- Missing stop conditions: stop if a full-state output rule cannot be stated or
  if Mini-batch unblocking would be needed.
- Unfair comparisons: sliced/subspace is a semantic replacement; do not rank it
  against exact/approximate-kernel lanes by dense-reference error alone.
- Hidden assumptions: projection directions, sorting ties, reconstruction
  mapping, output semantics, and random seed policy must be recorded.
- Stale context: Phase 8 sparse failure does not imply projection methods pass
  or fail; it only blocks sparse implementation in this runbook.
- Environment mismatch: no package install, no network, no POT execution, no
  GPU evidence, no non-TensorFlow default implementation.
- Artifact adequacy: a projected distance without particles is not a
  BayesFilter resampling artifact.

Skeptical audit status:
`PASSED_FOR_PHASE_9_SLICED_SUBSPACE_EXPLORATORY_PLAN`.

## Forbidden Claims And Actions

- Do not claim dense entropic OT equivalence, exact full-state coupling
  validity, posterior correctness, HMC-readiness, production/default readiness,
  statistical ranking, or general scalability.
- Do not execute Mini-batch/BoMb code or unblock that lane without clean source
  and a separate reviewed user-approved plan.
- Do not run POT, package installation, network fetches, external source code,
  or GPU evidence without approval.
- Do not treat a scalar distance or projected cost as transported particles.
- Do not treat dense-reference discrepancy as a promotion criterion.
- Do not modify unrelated dirty user work.

## Exact Next-Phase Handoff Conditions

Phase 10 may begin only after:

- Phase 9 result records a precise status: executed exploratory diagnostic,
  reference-only close, or blocker;
- if diagnostic execution proceeded, JSON/Markdown artifacts exist and local
  syntax/import/artifact checks pass;
- semantic class and transport-object semantics are recorded;
- Mini-batch/BoMb blocker is explicitly preserved or resolved by a separate
  approved source-repair result;
- Phase 10 comparative decision subplan exists and has been reviewed for
  consistency, correctness, feasibility, artifact coverage, and boundary
  safety;
- no human-required stop condition is active.

## Stop Conditions

Stop and write/update the stop handoff if:

- the projection diagnostic cannot define a full-state output rule before
  execution;
- execution would require package installation, network fetch, POT execution,
  GPU evidence, credentials, destructive action, external code, or Mini-batch
  unblocking;
- local checks reveal a hard veto not localized to a repair trigger;
- Claude and Codex do not converge after five focused review rounds for the
  same material blocker.

## End-Of-Phase Checklist

1. Run the required local checks.
2. Write the Phase 9 result/close record.
3. Draft or refresh the Phase 10 comparative decision subplan.
4. Review the Phase 10 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
