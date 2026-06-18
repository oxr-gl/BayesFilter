# Phase 10 Subplan: Comparative Decision

Date: 2026-06-17
Draft timestamp: 2026-06-18T04:12:20+08:00

## Phase Objective

Produce the final comparative decision table for the scalable OT master
program.  Phase 10 should synthesize Phases 0-9 into an evidence-class-aware
recommendation about which routes are ready for deeper LEDH-PFPF-OT testing,
which are reference-only, and which remain blocked.

Phase 10 is a decision and documentation phase.  It must not implement new
algorithms, run new candidate diagnostics, change BayesFilter defaults, or
rank stochastic/scientific candidates beyond the evidence already recorded.

## Entry Conditions Inherited From Previous Phase

- Phase 0 records governance/source-lock/runbook pass.
- Phase 1 records `PHASE_1_BASELINE_FIXTURE_PASSED`.
- Phase 2 records
  `PHASE_2_CANDIDATE_AUDITS_PASSED_WITH_USER_APPROVED_MICRO_REVIEW_RESOLUTION`.
- Phase 3 records `PHASE_3_COMMON_INTERFACE_HARNESS_PASSED`.
- Phase 4 records `PHASE_4_NYSTROM_PROTOTYPE_PASSED`.
- Phase 5 records
  `PHASE_5_POSITIVE_FEATURE_PROTOTYPE_PASSED_SEMANTIC_REPLACEMENT`.
- Phase 6 records
  `PHASE_6_LOW_RANK_COUPLING_TRANSPORT_OBJECT_FIXTURE_PASSED`.
- Phase 7 records
  `PHASE_7_EXACT_ONLINE_GPU_REFERENCE_ONLY_PASSED`.
- Phase 8 records
  `PHASE_8_SPARSE_LOCALITY_DIAGNOSTIC_COMPLETED_BLOCKS_SPARSE_IMPLEMENTATION_FOR_NOW`.
- Phase 9 records
  `PHASE_9_SLICED_SUBSPACE_EXPLORATORY_DIAGNOSTIC_PASSED_SEMANTIC_REPLACEMENT`.
- Mini-batch/BoMb remains `source_partial_user_needed` and blocked.
- No speedup, posterior correctness, production/default readiness, HMC
  readiness, or statistically supported ranking has been established.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-result-2026-06-17.md`
- Reset memo:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-reset-memo-2026-06-17.md`
- Updated execution ledger and stop handoff.

## Source Anchors Required Before Execution

| Anchor | Required use |
| --- | --- |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-code-master-program-2026-06-17.md` | Master program phase index and candidate-evidence roles. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-source-lock-result-2026-06-17.md` | Source-lock and Mini-batch blocker summary. |
| Phase 1-9 result notes | Evidence-class status and non-claims for every lane. |
| Phase 2 candidate audit notes | Paper-note-code classification and first execution-value contracts. |
| `docs/benchmarks/scalable-ot-p04-nystrom-prototype-diagnostics-2026-06-17.json` | Nystrom fixture diagnostics. |
| `docs/benchmarks/scalable-ot-p05-positive-feature-prototype-diagnostics-2026-06-17.json` | Positive-feature semantic-replacement diagnostics. |
| `docs/benchmarks/scalable-ot-p06-low-rank-coupling-prototype-diagnostics-2026-06-17.json` | Low-rank coupling transport-object diagnostics. |
| `docs/benchmarks/scalable-ot-p08-sparse-locality-diagnostics-2026-06-17.json` | Sparse/locality screen decision. |
| `docs/benchmarks/scalable-ot-p09-sliced-subspace-diagnostics-2026-06-17.json` | Sliced/subspace semantic-replacement diagnostics. |

## Required Checks, Tests, And Reviews

Before writing the decision:

1. Re-read Phase 1-9 result notes and the candidate audit notes.
2. Classify each lane by evidence class before comparing:
   - approximate-kernel diagnostic;
   - semantic-replacement diagnostic;
   - reference-only;
   - blocked/source-needed;
   - sparse implementation blocked by locality diagnostic.
3. Build a decision table with, at minimum:
   - candidate lane;
   - source status;
   - semantic class;
   - transport object;
   - execution artifact;
   - hard veto status;
   - promotion/readiness status;
   - implementation risk;
   - recommended next action;
   - explicit non-claims.
4. Include a separate inference-status table:
   - hard veto screen;
   - statistically supported ranking;
   - descriptive-only differences;
   - default-readiness;
   - next evidence needed.
5. Confirm no evidence class is silently upgraded into a ranking or default
   decision.
6. Confirm Mini-batch remains blocked unless a separate source-repair result
   exists.

Review:

- Run local artifact/content checks over the Phase 10 result and reset memo.
- Use Claude as read-only reviewer for the comparative decision if the result
  makes a recommendation among lanes.  Prefer bounded micro-review over a
  whole-file review if broad review stalls.
- Claude cannot authorize default changes, scientific claims, Mini-batch
  unblocking, GPU/external-code use, or phase completion without local checks.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Given the source audit and Phase 1-9 diagnostics, which scalable OT routes are justified for deeper LEDH-PFPF-OT testing, and which remain reference-only or blocked? |
| Baseline/comparator | Phase 1 dense/streaming TensorFlow baseline and each lane's declared semantic comparator. |
| Primary pass criterion | A comparative result and reset memo exist, correctly classify evidence classes, preserve non-claims, avoid unsupported ranking/default claims, and identify next justified testing routes. |
| Promotion veto | Treating semantic replacements as dense approximations; treating sparse locality failure as broad sparse-OT rejection; treating source maturity or runtime proxy as promotion evidence; Mini-batch unblocked; one-fixture or one-seed descriptive metrics ranked as statistically supported. |
| Continuation veto | Missing Phase 1-9 result artifact; missing benchmark JSON needed for a lane; unresolved contradiction between result and audit; local checks fail outside a repair trigger; review cannot converge after five bounded rounds for a material recommendation. |
| Repair trigger | Table omission, non-claim wording gap, evidence-class mismatch, stale handoff, missing reset-memo item, or review finding about overclaiming. |
| Explanatory diagnostics | Dense-reference discrepancies, residual magnitudes, source maturity, implementation effort, runtime/memory proxies, and fixture-specific behavior. |
| Not concluded | No production default, no posterior correctness, no HMC readiness, no public API readiness, no statistically supported ranking, and no speedup claim. |
| Artifact preserving result | Phase 10 result, reset memo, ledger, and stop handoff. |

## Skeptical Plan Audit

- Wrong baseline: final comparison must use Phase 1 and each lane's declared
  semantic comparator, not an ad hoc metric.
- Proxy metric risk: runtime, source maturity, dense-reference discrepancy, and
  ease of coding are explanatory unless the lane's own subplan declared them
  as promotion criteria.
- Missing stop conditions: stop if any required result artifact is missing or
  if a recommendation cannot be stated without crossing a forbidden claim.
- Unfair comparisons: do not rank exact/reference-only, approximate-kernel,
  and semantic-replacement lanes as if they share a single metric.
- Hidden assumptions: note that the fixtures are deterministic smoke/diagnostic
  fixtures, not downstream filtering evidence.
- Stale context: Phase 8 blocks sparse implementation for now but not sparse OT
  in general; Phase 9 is viable only as semantic replacement.
- Environment mismatch: no package install, network, GPU, POT, external code,
  or non-TensorFlow default action in Phase 10.
- Artifact adequacy: a final recommendation must cite artifacts, not memory.

Skeptical audit status:
`PASSED_FOR_PHASE_10_COMPARATIVE_DECISION_PLAN`.

## Forbidden Claims And Actions

- Do not claim speedup, production/default readiness, posterior correctness,
  HMC-readiness, public API readiness, or statistically supported ranking.
- Do not treat semantic-replacement diagnostics as dense OT equivalence.
- Do not treat sparse Phase 8 failure as proof that sparse OT cannot help in
  LEDH-specific future fixtures.
- Do not unblock or execute Mini-batch/BoMb.
- Do not run new candidate experiments unless a separate reviewed subplan is
  written.
- Do not install packages, fetch network sources, use GPU evidence, run POT, or
  execute external source code.
- Do not modify unrelated dirty user work.

## Exact Next-Phase Handoff Conditions

The master program may close when:

- Phase 10 comparative result exists and passes local checks;
- reset memo exists and preserves current status, decisions, non-claims, and
  next justified actions;
- read-only review of material recommendations converges or a blocker result
  records nonconvergence after the allowed bounded rounds;
- ledger and stop handoff are updated;
- no human-required stop condition remains active.

## Stop Conditions

Stop and write/update the stop handoff if:

- any required Phase 1-9 result or benchmark JSON artifact is missing;
- final recommendation would require an unsupported ranking/default/scientific
  claim;
- Mini-batch source repair is required to complete the decision;
- review finds a material issue that cannot be repaired in five bounded rounds;
- local checks reveal a hard contradiction between artifacts and the proposed
  decision.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write the Phase 10 comparative result.
3. Write the reset memo.
4. Run local artifact/content checks.
5. Run bounded read-only Claude review for material recommendations.
6. Patch fixable issues and rerun focused checks/review.
7. Update ledger and stop handoff.
