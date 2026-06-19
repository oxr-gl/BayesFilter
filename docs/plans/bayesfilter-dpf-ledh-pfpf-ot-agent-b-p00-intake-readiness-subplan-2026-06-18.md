# Phase B0 Subplan: Intake And Readiness Gate

Date: 2026-06-18

## Phase Objective

Verify that Agent A's Phase 11 handoff artifacts exist, are readable, and are
sufficiently complete to begin Agent B independent testing and artifact review.

## Entry Conditions Inherited From Previous Phase

- Agent A Phase 11 has reported completion.
- Agent B master program exists.
- Current lane owns Agent B planning and execution.
- Agent B must remain read-only on Agent A-owned implementation, diagnostic,
  JSON/Markdown, and result-note files during the initial independent review
  pass.

## Required Artifacts

- Phase B0 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p00-intake-readiness-result-2026-06-18.md`
- Refreshed Phase B1 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p01-independent-unit-test-harness-subplan-2026-06-18.md`
- Visible execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-visible-execution-ledger-2026-06-18.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-visible-stop-handoff-2026-06-18.md`

## Required Checks, Tests, And Reviews

Local checks:

- `git status --short`
- load and record the required parent context before any independent tests or
  artifact judgments:
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-reboot-reset-memo-2026-06-18.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p10-comparative-decision-result-2026-06-17.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-a-reduced-rank-nystrom-ladder-plan-2026-06-18.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p04-nystrom-prototype-result-2026-06-17.md`
  - `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p01-baseline-fixture-spec-2026-06-17.md`
  - `docs/benchmarks/scalable_ot_candidate_result_schema.py`
  - `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
  - `tests/test_nystrom_transport_tf.py`
- existence checks for Agent A result, JSON, Markdown, diagnostic script,
  implementation, and test file;
- parse Agent A JSON and report top-level keys, number of direct
  `candidate_records`, fixture names from `diagnostics.fixture`,
  `phase11_status`, and first `baseline_comparator`;
- validate every direct Phase 3 record in `candidate_records` with
  `docs.benchmarks.scalable_ot_candidate_result_schema.validate_candidate_result`;
- confirm every direct candidate record's `baseline_comparator` begins
  `phase1_dense_streaming`;
- confirm `diagnostics.dense_reference_max_abs_particle_error` and
  `diagnostics.dense_reference_rms_particle_error` exist for every direct
  candidate record.

Review:

- Claude review is optional for B0 unless local checks reveal a material
  readiness ambiguity.  If used, Claude must be read-only and receive a compact
  finding summary, not whole files.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are Agent A's Phase 11 artifacts complete enough to start independent Agent B checks? |
| Baseline/comparator | Agent A Phase 11 result and JSON must preserve the Phase 1 dense/streaming comparator convention. |
| Primary pass criterion | Required parent context is loaded and recorded; all required Agent A artifacts exist; JSON is readable; all direct `candidate_records` schema-validate; baseline prefixes pass; dense-reference fields exist; and the Agent A result says Agent B can begin. |
| Veto diagnostics | Missing context file, missing Agent A artifact, unreadable JSON, zero candidate records, schema validation failure, bad baseline prefix, missing dense-reference fields, or Agent A result not granting Agent B handoff. |
| Explanatory diagnostics | Context paths, artifact paths, candidate-record count, fixture set, status strings, git status snapshot. |
| Not concluded | No independent correctness review yet; no speedup, ranking, posterior, HMC, or default-readiness claim. |
| Artifact preserving result | B0 result, ledger entry, and refreshed B1 subplan note. |

## Forbidden Claims And Actions

- Do not edit Agent A-owned files.
- Do not run Agent A diagnostics.
- Do not interpret Agent A pass as independent validation.
- Do not use GPU, network, package install, POT, or external backend evidence.
- Do not claim speedup, ranking, posterior correctness, HMC readiness, or
  default readiness.

## Exact Next-Phase Handoff Conditions

Advance to B1 only if:

- B0 result status is `PHASE_B0_AGENT_B_INTAKE_READINESS_PASSED`;
- required parent context files were loaded and recorded in the B0 result;
- required Agent A artifacts exist and validate under B0 checks;
- B1 subplan is present and locally reviewed for consistency, feasibility,
  artifact coverage, and boundary safety.

## Stop Conditions

Stop with `PHASE_B0_AGENT_B_INTAKE_READINESS_BLOCKED` if any primary artifact is
missing, JSON/schema checks fail, the handoff is not granted, or independent
review would require editing Agent A-owned files before the first verdict.

## End-Of-Phase Protocol

At phase end:

1. Run the required local checks.
2. Write the B0 phase result / close record.
3. Draft or refresh the B1 subplan.
4. Review the B1 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
