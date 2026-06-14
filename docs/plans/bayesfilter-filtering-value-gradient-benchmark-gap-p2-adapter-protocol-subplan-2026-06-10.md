# P2 Subplan: Unified Filter Adapter Protocol

metadata_date: 2026-06-10
phase: FILTER_BENCH_P2
status: PLAN_DRAFT_PENDING_CLAUDE_REVIEW
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Define one adapter protocol for all filters so the benchmark runner does not
depend on one-off scripts and old result notes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can every filter expose value, gradient, diagnostics, runtime, and status through one benchmark interface? |
| Baseline/comparator | `bayesfilter.nonlinar`, `bayesfilter.highdim`, and `experiments/dpf_implementation` runner interfaces. |
| Primary criterion | Adapter protocol exists as a durable schema/interface artifact and at least one tiny exercised fixture row per algorithm family proves value, gradient/status, diagnostics, and reason-code payloads can be carried. |
| Veto diagnostics | Per-algorithm bespoke JSON shapes; missing status codes; no stable registry row id/target id; planned-but-unexercised smoke rows used as proof; no way to report invalid gradients; NumPy backend drift in BayesFilter-owned implementation. |
| Explanatory diagnostics | Import checks, adapter schema validation, and adapter smoke tests. |
| Not concluded | Adapter existence does not prove benchmark accuracy. |
| Artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p2-adapter-protocol-result-2026-06-10.md` plus a concrete schema/interface artifact, for example `docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json`. |

## Required Adapter Fields

- `algorithm_id`
- `target_id`
- `registry_row_id`
- `model_id`
- `dimension`
- `horizon`
- `theta_id`
- `observation_id`
- `value`
- `gradient`
- `value_status`
- `gradient_status`
- `reference_type`
- `diagnostics`
- `runtime_seconds`
- `random_seed`
- `artifact_path`

## Tasks

- Design a TensorFlow-first adapter protocol.
- Emit a durable schema/interface artifact with required fields, status enums,
  and allowed reason codes.
- Define result status enums for values and gradients.
- Define a diagnostic payload common enough for deterministic and particle
  filters.
- Plan import boundaries so experimental DPF code can be benchmarked without
  being promoted to default BayesFilter public API.
- Exercise at least one tiny fixture row per algorithm family: Kalman/linear,
  deterministic sigma-point/CUT/Zhao-Cui family, and DPF family.
- Verify the exercised fixture rows include at least one valid gradient/status
  payload and at least one invalid or unavailable gradient reason-code payload.

## Exit Criteria

Pass with `PASS_FILTER_BENCH_P2_ADAPTER_PROTOCOL` only if the protocol can
represent deterministic filters, particle filters, invalid gradients, and
historical-only rows, and this is demonstrated by exercised fixture rows rather
than planned smokes.  Block if any required algorithm family cannot be
represented without special cases.

## Validation

- Focused import, schema, and exercised-fixture tests once protocol code is
  added.
- Claude read-only review, max five iterations.
