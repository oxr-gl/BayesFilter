# Wave 2 Current-Agent Master Program: Positive-Feature Sinkhorn

Date: 2026-06-19
Owner: current agent
Supervisor/executor: Codex in the current conversation
Read-only reviewer: Claude Opus max effort for material issues

## Status

`POSITIVE_FEATURE_SINKHORN_VISIBLE_EXECUTION_COMPLETE`

## Purpose

Govern the current-agent Wave 2 positive-feature Sinkhorn lane from reviewed
launch packet through deterministic replay, diagnostics, repair loop, and lane
closeout.

This program owns the positive-feature lane only.  The peer-agent low-rank
coupling lane is independent and is not an input during current-lane execution.

## Entry Context

- Positive-feature source audit:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-audit-2026-06-17.md`
- Phase 5 positive-feature result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p05-positive-feature-prototype-result-2026-06-17.md`
- Existing TensorFlow implementation:
  `experiments/dpf_implementation/tf_tfp/resampling/positive_feature_transport_tf.py`
- Existing tests:
  `tests/test_positive_feature_transport_tf.py`

## Owned Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-*-2026-06-19.md`
- `docs/benchmarks/scalable_ot_wave2_positive_feature_diagnostics.py`
- `docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.json`
- `docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.md`
- `tests/test_wave2_positive_feature_diagnostics.py`

Existing Phase 5 positive-feature files are read-only unless a focused repair
is required by the Wave 2 diagnostic and can be made without changing shared
contracts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the positive-feature Sinkhorn route close as a Wave 2 algorithm-complete current-agent lane with finite transported particles, feature factors, scalings, residual checks, and schema-valid artifacts? |
| Baseline/comparator | Phase 1 dense/streaming baseline only for descriptive semantic deltas; Phase 5 artifacts as entry context. |
| Primary pass criterion | Wave-2 diagnostic wrapper, focused tests, official JSON/Markdown diagnostics, current-agent result, and status record all pass with empty hard vetoes and explicit semantic-replacement boundaries. |
| Veto diagnostics | Nonfinite particles/factors/scalings, nonpositive features, residual threshold failure, schema validation failure, scalar-cost-only output, missing transported particles, or unsupported claim. |
| Explanatory diagnostics | Dense-reference errors, feature count, epsilon, runtime, Phase 5 replay status. |
| Not concluded | No dense Gibbs equivalence, speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, or broad scalable-OT selection. |

## Phase Index

This current-agent lane is executed inside coordinator phase W2-1:

| Lane phase | Name | Subplan | Result |
| --- | --- | --- | --- |
| PF-0 | Launch Packet Review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p00-coordinator-launch-packet-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p00-coordinator-launch-packet-result-2026-06-19.md` |
| PF-1 | Diagnostic Replay And Closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p01-current-positive-feature-execution-subplan-2026-06-19.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-result-2026-06-19.md` |

## Stop Conditions

Stop if execution requires package installation, network fetch, GPU evidence,
external solver, public API/default/export change, Phase 1/Phase 3 edit,
peer-lane edit, changing thresholds after seeing results, or making a
forbidden claim.
