# Phase B1 Subplan: Independent Unit-Test Harness

Date: 2026-06-18

## Phase Objective

Create and run an Agent B-owned independent unit-test harness for
`nystrom_transport_resample_tf` that checks core invariants without editing
Agent A-owned files.

## Entry Conditions Inherited From Previous Phase

- B0 passed and recorded that Agent A artifacts are present and readable.
- B0 loaded and recorded the required parent context before independent test
  work begins.
- Agent A implementation file is treated as read-only for this phase.
- Agent B may create `tests/test_nystrom_transport_tf_independent.py`.

## Required Artifacts

- Independent test file:
  `tests/test_nystrom_transport_tf_independent.py`
- Phase B1 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p01-independent-unit-test-harness-result-2026-06-18.md`
- Refreshed Phase B2 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p02-artifact-review-script-subplan-2026-06-18.md`
- Optional test log:
  `docs/benchmarks/scalable-ot-p11-nystrom-independent-unit-tests-2026-06-18.log`

## Required Checks, Tests, And Reviews

Required independent tests:

- import and basic shape test for `nystrom_transport_resample_tf`;
- reduced-rank factor shape test with `rank < N`;
- full-rank replay guard against the Phase 4-style full-rank path;
- batch-shape test with `B > 1`;
- orientation/materialized-plan reconstruction test using
  `diag(u) V A^{-1} V^T diag(v)` and the declared
  `source_rows_target_columns` convention;
- invalid-input/nonfinite guard checks that invalid rank/epsilon/shape inputs do
  not silently produce valid-looking results.

Local commands:

```bash
python -m py_compile tests/test_nystrom_transport_tf_independent.py
pytest -q tests/test_nystrom_transport_tf_independent.py
```

Review:

- Claude review is material if the independent test design changes the planned
  evidence contract or if local tests expose an ambiguous implementation issue.
  Use a compact prompt with only test names, invariant summaries, and findings.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does an independently written test harness confirm the Nystrom implementation's basic shape, rank, orientation, batch, and invalid-input invariants? |
| Baseline/comparator | Function-level invariants and Phase 3 orientation convention; not dense-reference ranking. |
| Primary pass criterion | Independent tests compile and pass in CPU-only mode without modifying Agent A files. |
| Veto diagnostics | Import failure, nonfinite result, wrong reduced-rank factor shape, full-rank replay mislabeling, invalid orientation reconstruction, invalid inputs silently accepted, or Agent B editing Agent A files. |
| Explanatory diagnostics | Test durations, reconstructed row/column residuals, shape inventory, TensorFlow CPU/GPU warning notes. |
| Not concluded | No artifact-level Agent A review yet; no speedup, ranking, posterior correctness, HMC readiness, or default readiness. |
| Artifact preserving result | Independent test file, pytest output/log, B1 result, ledger update, refreshed B2 subplan. |

## Forbidden Claims And Actions

- Do not edit Agent A implementation or result files.
- Do not treat passing unit tests as artifact-level validation.
- Do not run GPU, network, package install, POT, or external backend actions.
- Do not claim speedup, ranking, posterior correctness, HMC readiness, or
  default readiness.

## Exact Next-Phase Handoff Conditions

Advance to B2 only if:

- B1 result status is `PHASE_B1_AGENT_B_INDEPENDENT_UNIT_TESTS_PASSED`;
- independent tests compile and pass;
- B2 subplan is present and locally reviewed.

## Stop Conditions

Stop with `PHASE_B1_AGENT_B_INDEPENDENT_UNIT_TESTS_BLOCKED` if TensorFlow import
fails, tests cannot run, or any failure points to an Agent A-owned artifact that
Agent B cannot repair under the read-only boundary.

## End-Of-Phase Protocol

At phase end:

1. Run the required local checks.
2. Write the B1 phase result / close record.
3. Draft or refresh the B2 subplan.
4. Review the B2 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
