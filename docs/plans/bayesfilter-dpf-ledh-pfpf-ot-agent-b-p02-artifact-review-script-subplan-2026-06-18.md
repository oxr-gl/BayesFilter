# Phase B2 Subplan: Independent Artifact Review Script

Date: 2026-06-18

## Phase Objective

Implement an Agent B-owned review script that inspects Agent A's Phase 11 JSON
and result note for manifest, schema, comparator, coverage, diagnostic-role,
source-route, and non-claim invariants.

## Entry Conditions Inherited From Previous Phase

- B1 independent unit tests passed or produced no blocker that prevents
  artifact-level review.
- B0 loaded and recorded the required parent context, including the reset memo,
  Phase 10 comparative decision, Agent A Phase 11 plan, Phase 4 Nystrom result,
  Phase 1 baseline fixture spec, and Phase 3 schema.
- Agent A JSON/result/Markdown files are read-only inputs.
- Agent B may create only Agent B-owned review script and output artifacts.

## Required Artifacts

- Review script:
  `docs/benchmarks/scalable_ot_p11_nystrom_independent_review.py`
- Phase B2 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p02-artifact-review-script-result-2026-06-18.md`
- Refreshed Phase B3 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p03-independent-review-execution-subplan-2026-06-18.md`

## Required Checks, Tests, And Reviews

The review script must check:

- Agent A JSON top-level manifest shape;
- exactly one direct Phase 3-valid record in top-level `candidate_records` per
  fixture/rank pair, using `diagnostics.fixture` and `diagnostics.rank_label`
  as the fixture/rank identity;
- all direct candidate record `baseline_comparator` values begin
  `phase1_dense_streaming`;
- all required fixtures are present:
  `tiny_manual`, `small_parity`, `high_dim_low_rank`, `high_dim_locality`,
  `ledh_specific_smoke`;
- all planned rank labels are present for each fixture;
- every direct candidate record emits
  `diagnostics.dense_reference_max_abs_particle_error` and
  `diagnostics.dense_reference_rms_particle_error`;
- `high_dim_locality` is explanatory-only for promotion;
- at least one viable reduced rank exists for every promotion fixture;
- non-claims include no speedup, no ranking, and no production default change;
- result text does not claim speedup, ranking, posterior correctness, HMC
  readiness, public API readiness, or production/default readiness;
- result text does not describe the JSON manifest shape as nested
  `candidate_record` objects when the artifact uses direct top-level
  `candidate_records` entries;
- source-route wording preserves `fixed_hmc_adaptation` for the whole route and
  does not promote the whole prototype to unqualified `source_faithful`.

Local commands:

```bash
python -m py_compile docs/benchmarks/scalable_ot_p11_nystrom_independent_review.py
```

Review:

- Run a compact local review of the script against this subplan.
- Claude review is material if the script omits a required invariant or if the
  invariant contract is ambiguous.  Do not send the whole script to Claude; send
  the check list and any disputed function/line snippets only.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can an independent review script check the Agent A Phase 11 artifact contract without executing Agent A diagnostics or editing Agent A files? |
| Baseline/comparator | Agent A JSON/result against Phase 3 schema and Agent B review contract. |
| Primary pass criterion | Script compiles and contains checks for all required manifest, schema, coverage, diagnostic-role, source-route, and non-claim invariants. |
| Veto diagnostics | Missing invariant, whole-file/source execution dependency, Agent A file mutation, external/GPU/network dependency, or broad claim interpretation. |
| Explanatory diagnostics | Check inventory, output schema, warning/finding severity mapping. |
| Not concluded | Script existence alone does not validate Agent A artifacts; execution occurs in B3. |
| Artifact preserving result | Review script, B2 result, ledger update, refreshed B3 subplan. |

## Forbidden Claims And Actions

- Do not edit Agent A files.
- Do not execute Agent A diagnostic script.
- Do not fetch packages, network, GPU, POT, or external backend resources.
- Do not treat script compile as artifact pass.

## Exact Next-Phase Handoff Conditions

Advance to B3 only if:

- B2 result status is `PHASE_B2_AGENT_B_ARTIFACT_REVIEW_SCRIPT_PASSED`;
- review script compiles;
- local script-coverage review confirms all required invariants are represented;
- B3 subplan is present and locally reviewed.

## Stop Conditions

Stop with `PHASE_B2_AGENT_B_ARTIFACT_REVIEW_SCRIPT_BLOCKED` if the script cannot
represent the manifest contract, requires editing Agent A files, or would need
external/GPU/network/package actions.

## End-Of-Phase Protocol

At phase end:

1. Run the required local checks.
2. Write the B2 phase result / close record.
3. Draft or refresh the B3 subplan.
4. Review the B3 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
