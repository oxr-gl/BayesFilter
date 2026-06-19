# W2-1 Subplan: Current-Agent Positive-Feature Execution

Date: 2026-06-19
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-coordinator-master-program-2026-06-19.md`

## Phase Objective

Execute the current-agent positive-feature Sinkhorn lane to closeout under the
Wave 2 algorithm-complete contract, using the existing TensorFlow
positive-feature implementation and a Wave-2-owned diagnostic wrapper.

## Entry Conditions Inherited From Previous Phase

- W2-0 launch review converged.
- The current agent owns positive-feature Sinkhorn.
- The peer agent owns low-rank coupling validation and is not an input to this
  lane except final closeout availability for later coordinator merge.
- Phase 1 baseline and Phase 3 schema remain read-only.

## Required Artifacts

- Current-agent master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-master-program-2026-06-19.md`
- Current-agent status:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-status-2026-06-19.md`
- Diagnostic wrapper:
  `docs/benchmarks/scalable_ot_wave2_positive_feature_diagnostics.py`
- Focused tests:
  `tests/test_wave2_positive_feature_diagnostics.py`
- Diagnostic JSON:
  `docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.json`
- Diagnostic Markdown:
  `docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.md`
- Current-agent final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-result-2026-06-19.md`
- W2-1 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p01-current-positive-feature-execution-result-2026-06-19.md`
- W2-2 subplan.

## Required Checks, Tests, And Reviews

Local checks:

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave2_positive_feature_diagnostics.py tests/test_wave2_positive_feature_diagnostics.py experiments/dpf_implementation/tf_tfp/resampling/positive_feature_transport_tf.py docs/benchmarks/scalable_ot_p05_positive_feature_prototype_diagnostics.py
pytest -q tests/test_positive_feature_transport_tf.py tests/test_wave2_positive_feature_diagnostics.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave2_positive_feature_diagnostics.py --output docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.json --markdown-output docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.md
```

Review:

- Codex skeptical audit before running diagnostics.
- Claude read-only review is required if the diagnostic wrapper or result
  wording changes evidence roles, boundaries, or final status interpretation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current-agent positive-feature Sinkhorn route replay as a Wave 2 algorithm-complete lane with finite feature factors, scalings, transported particles, residual checks, and Phase 3 schema-valid reporting? |
| Baseline/comparator | Phase 1 dense/streaming TensorFlow baseline only for descriptive semantic deltas; Phase 5 positive-feature result as entry context, not final Wave 2 evidence. |
| Primary pass criterion | Syntax checks pass; focused tests pass; Wave-2 diagnostic exits 0; JSON candidate record validates; hard vetoes are empty; final result preserves semantic-replacement and non-claim boundaries. |
| Veto diagnostics | Nonfinite particles/factors/scalings, nonpositive features, row/column residual above threshold, schema failure, scalar-cost-only output, missing transported particles, shared file edit need, or unsupported claim. |
| Explanatory diagnostics | Dense-reference particle error, RMS error, feature count, epsilon, runtime, TensorFlow environment logs, prior Phase 5 status. |
| Not concluded | No dense Gibbs equivalence, no speedup, no ranking, no posterior correctness, no HMC readiness, no public API readiness, no production/default readiness, no broad scalable-OT selection. |
| Artifact preserving result | JSON/Markdown diagnostics, W2-1 result, current-agent final result/status. |

## Forbidden Claims And Actions

- Do not edit peer-agent low-rank files.
- Do not edit Phase 1 baseline or Phase 3 schema.
- Do not change public exports/defaults.
- Do not treat dense-reference error as a promotion criterion.
- Do not claim algorithm ranking, speedup, posterior correctness, HMC/API
  readiness, production/default readiness, dense equivalence, or broad
  scalable-OT selection.

## Exact Next-Phase Handoff Conditions

W2-2 may begin only if:

- W2-1 checks pass;
- current-agent final result exists and records one final status;
- current-agent status file is updated;
- W2-2 final merge subplan exists and passes Codex consistency review;
- peer-agent final status/result artifacts are available or a true blocker is
  recorded.

## Stop Conditions

Stop and write a blocker result if:

- a hard veto fires and cannot be repaired within current-lane files;
- execution requires package install, network, GPU evidence, external solver,
  public API/default/export edits, or shared schema/baseline edits;
- interpreting the result requires a forbidden claim;
- Claude/Codex do not converge after five rounds for the same material blocker.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write W2-1 result and current-agent final result/status.
3. Draft or refresh W2-2 subplan.
4. Review W2-2 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
