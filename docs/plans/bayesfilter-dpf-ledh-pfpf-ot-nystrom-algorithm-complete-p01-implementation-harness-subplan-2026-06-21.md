# P01 Subplan: Implementation And Harness

Date: 2026-06-21

Status: `DRAFT_DEPENDS_ON_P00`

## Phase Objective

Implement a dedicated Nystrom algorithm-complete harness and focused tests that
exercise the fixed-rank Nystrom transport inside an LEDH/PFPF-OT resampling
loop, without changing the repository default route.

## Entry Conditions Inherited From Previous Phase

- P00 governance passed.
- Nystrom lane boundaries and nonclaims are locked.
- Existing `nystrom_transport_tf.py` is the candidate transport implementation.

## Required Artifacts

- Harness:
  `docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py`
- Tests:
  `tests/test_nystrom_ledh_pfpf_algorithm_complete.py`
- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p01-implementation-harness-result-2026-06-21.md`
- Refreshed P02 subplan.

## Required Checks, Tests, Reviews

- Exact syntax command:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py tests/test_nystrom_ledh_pfpf_algorithm_complete.py
```

- Exact focused test command:

```bash
pytest -q tests/test_nystrom_transport_tf.py tests/test_nystrom_ledh_pfpf_algorithm_complete.py
```

- Local artifact coverage check for CLI modes and nonclaims.
- Claude review only if harness changes introduce material claim or boundary
  changes beyond this subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does a dedicated harness exist that can test Nystrom as an end-to-end LEDH/PFPF-OT candidate? |
| Baseline/comparator | Existing Nystrom transport implementation and streaming/default harness patterns. |
| Primary criterion | Harness and tests compile; focused tests pass; harness exposes small-reference, downstream-smoke, and GPU-scale modes; output schema records hard vetoes, source-route/provenance fields, transport-object fields, baseline comparator, and nonclaims. |
| Veto diagnostics | Missing mode, missing nonclaims, missing source-route/provenance fields, missing transport-object fields, missing dense-reference fields, missing GPU/device fields, tests fail, dense matrix materialized in candidate route, or default route changed. |
| Explanatory diagnostics | Test runtime, harness schema details, fixture metadata. |
| Not concluded | No algorithm viability, speedup, posterior correctness, dense equivalence, default readiness, or leaderboard rank. |
| Artifact | P01 result file. |

## Forbidden Claims And Actions

- Do not claim the Nystrom algorithm helps LEDH yet.
- Do not change default route metadata.
- Do not commit/push.
- Do not use NumPy as algorithm backend except for fixture construction,
  reporting, and independent reference inspection.

## Exact Next-Phase Handoff Conditions

P02 may begin only after:

- P01 required checks pass;
- P01 result records commands and status;
- harness schema includes `algorithm_family`, `mode`, `status`, `hard_vetoes`,
  `run_manifest`, `source_route`, `source_route_components`, `semantic_class`,
  `baseline_comparator`, `transport_object_kind`,
  `transport_matrix_materialized`, and `nonclaims`;
- P02 subplan is refreshed and locally reviewed.

## Stop Conditions

- Harness cannot be implemented without changing default route or public API.
- Focused tests fail for a nontrivial algorithm issue.
- Required artifacts cannot be written.
