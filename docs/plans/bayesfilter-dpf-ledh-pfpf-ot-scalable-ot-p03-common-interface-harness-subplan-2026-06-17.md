# Phase 3 Subplan: Common Interface Harness

Date: 2026-06-17

## Phase Objective

Implement the experimental candidate transport interface and JSON/Markdown
result schema without adding a new scalable OT algorithm yet.  Phase 3 should
create the harness that later candidate prototypes use to report transported
particles, transport objects, diagnostics, source routes, and execution
manifests against the Phase 1 dense/streaming baseline fixtures.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result records `PHASE_1_BASELINE_FIXTURE_PASSED`.
- Phase 2 result records
  `PHASE_2_CANDIDATE_AUDITS_PASSED_WITH_USER_APPROVED_MICRO_REVIEW_RESOLUTION`.
- Seven candidate audit notes and the Phase 2 gate packet exist.
- Mini-batch/BoMb remains `source_partial_user_needed` and blocked for
  decision-grade implementation.
- No candidate execution value, ranking, or default change has been claimed.
- No human-required stop condition is active for a documentation/schema-only
  harness phase.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p03-common-interface-harness-result-2026-06-17.md`
- Harness/schema implementation artifact, to be chosen after inventory:
  - preferred location under `docs/benchmarks` for experiment/reporting schema
    if no reusable package API is needed; or
  - a narrowly scoped TensorFlow-compatible experimental helper under
    `experiments/dpf_implementation/tf_tfp/resampling/` only if the existing
    code patterns clearly support it.
- JSON schema or schema-checking helper for candidate transport results.
- One schema-only smoke/check artifact under `docs/benchmarks`.
- Updated ledger and stop handoff.
- Phase 4 Nystrom prototype subplan draft:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-subplan-2026-06-17.md`

## Required Checks, Tests, And Reviews

Local checks:

1. Inventory existing Phase 1 diagnostic script/result shapes and current
   `AnnealedTransportTFResult` fields before implementation.
2. Verify the new schema can represent:
   dense matrix, streaming non-materialized transport, low-rank factors,
   sparse plan, projection plan, blocked lane, and semantic-replacement output.
3. Verify the schema records:
   source status, semantic class, source route, baseline comparator,
   transport-object kind, diagnostics roles, and non-claims.
4. Run a schema smoke check using Phase 1 baseline diagnostics or synthetic
   in-memory examples; do not run candidate algorithms.
5. Run targeted syntax/import checks for any new Python artifact.

Review:

- Claude review is optional for Phase 3 planning unless the schema changes
  implementation boundaries, because the user approved the Phase 2 review-gate
  resolution and Phase 3 is schema/harness only.
- If Claude is used, use the atomized micro-review style, not a broad file
  traversal prompt.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we create a common result schema and harness that will let later scalable OT candidates be compared fairly against the Phase 1 dense/streaming baseline? |
| Baseline/comparator | Phase 1 baseline fixture outputs and current `annealed_transport_tf.py` result semantics. |
| Primary pass criterion | A schema/harness artifact exists and passes smoke checks for all required transport-object kinds without implementing a new candidate algorithm. |
| Veto diagnostics | Candidate algorithm implemented early; schema cannot represent semantic replacements or blocked lanes; no field for source route/source status; no field for Phase 1 comparator; no non-claims field; non-TF backend promoted as default; Mini-batch unblocked. |
| Explanatory diagnostics | Ease of adapting Phase 4 Nystrom, field completeness, JSON/Markdown readability, and compatibility with Phase 1 artifacts. |
| Not concluded | No candidate correctness, no execution value, no speedup, no ranking, no production API readiness, no default change. |
| Artifact preserving result | Schema/harness files, smoke-check output, Phase 3 result, ledger entry, and Phase 4 subplan. |

## Skeptical Plan Audit

- Wrong baseline: Phase 3 must use Phase 1 dense/streaming fixture outputs as
  comparator examples, not external library outputs.
- Proxy metric risk: schema completeness and smoke checks do not prove any
  candidate works.
- Missing stop conditions: stop if implementation of Nystrom/feature/low-rank
  algorithm becomes necessary to test the schema.
- Unfair comparisons: exact, approximate-kernel, and semantic-replacement
  lanes require different diagnostic roles in the schema.
- Hidden assumptions: schema must record orientation, transport-object kind,
  source route, semantic class, and whether dense-reference error is a
  promotion criterion or explanatory only.
- Stale context: use the Phase 2 audit notes and gate packet as the source of
  required transport-object kinds.
- Environment mismatch: no package installation, no network fetch, no GPU
  evidence, and no non-TF default implementation.
- Artifact adequacy: a schema smoke check answers this phase; candidate
  numerical results do not belong here.

Skeptical audit status: `PASSED_FOR_PHASE_3_COMMON_INTERFACE_HARNESS_PLAN`.

## Forbidden Claims And Actions

- Do not implement Nystrom, positive-feature, low-rank, sparse, sliced, or
  Mini-batch algorithms in Phase 3.
- Do not install packages or fetch network sources.
- Do not run external library tests.
- Do not claim execution value, speedup, ranking, posterior correctness, or
  production/default readiness.
- Do not unblock Mini-batch/BoMb.
- Do not change the BayesFilter default backend.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only after:

- Phase 3 result records `PHASE_3_COMMON_INTERFACE_HARNESS_PASSED`;
- schema/harness artifacts exist;
- smoke checks and syntax/import checks pass;
- the schema can represent all required transport-object kinds and semantic
  classes;
- Phase 4 Nystrom prototype subplan exists and has been reviewed for
  consistency, correctness, feasibility, artifact coverage, and boundary
  safety;
- no human-required stop condition is active.

## Stop Conditions

Stop and write/update the stop handoff if:

- a candidate algorithm must be implemented to continue;
- schema fields cannot represent one of the Phase 2 lane requirements;
- Phase 1 baseline diagnostics are missing or inconsistent;
- continuing would require package installation, network, GPU evidence,
  credentials, or destructive action;
- review uncovers a mismatch that would make candidate comparisons unfair;
- user direction is needed to choose between a docs/benchmarks-only schema and
  a reusable Python helper in experiment code.

## End-Of-Phase Checklist

1. Run the required local checks.
2. Write the Phase 3 result/close record.
3. Draft or refresh the Phase 4 Nystrom prototype subplan.
4. Review the Phase 4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
