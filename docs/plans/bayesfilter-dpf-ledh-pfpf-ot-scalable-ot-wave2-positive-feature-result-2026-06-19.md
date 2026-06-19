# Wave 2 Result: Current-Agent Positive-Feature Sinkhorn

Date: 2026-06-19
Owner: current agent
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-master-program-2026-06-19.md`

## Status

`POSITIVE_FEATURE_SINKHORN_PASSED_DIAGNOSTIC_ONLY`

## Result Summary

The current-agent positive-feature Sinkhorn lane closed as a Wave 2
algorithm-complete diagnostic-only lane.  It replayed the existing TensorFlow
positive-feature transport route through a Wave-2-owned diagnostic wrapper and
wrote schema-valid JSON/Markdown artifacts.

This is a semantic-replacement diagnostic.  Dense-reference particle deltas are
explanatory only.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the positive-feature Sinkhorn route close as a Wave 2 algorithm-complete current-agent lane with finite transported particles, feature factors, scalings, residual checks, and schema-valid artifacts? |
| Baseline/comparator | Phase 1 dense/streaming baseline was used only for descriptive semantic deltas; Phase 5 artifacts were entry context. |
| Primary criterion | Passed. Syntax checks passed, focused tests passed, official Wave 2 diagnostic exited 0, JSON candidate record validates, hard vetoes are empty, and semantic-replacement boundaries are preserved. |
| Veto diagnostics | None fired. |
| Explanatory diagnostics | Dense-reference particle error, RMS error, feature count, epsilon, runtime, TensorFlow environment warning, and Phase 5 replay status. |
| Not concluded | No dense Gibbs equivalence, speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, or broad scalable-OT selection. |
| Preserving artifacts | Wave 2 positive-feature JSON/Markdown diagnostics, this result note, W2-1 phase result, and current-agent status. |

## Checks Run

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave2_positive_feature_diagnostics.py tests/test_wave2_positive_feature_diagnostics.py experiments/dpf_implementation/tf_tfp/resampling/positive_feature_transport_tf.py docs/benchmarks/scalable_ot_p05_positive_feature_prototype_diagnostics.py
pytest -q tests/test_positive_feature_transport_tf.py tests/test_wave2_positive_feature_diagnostics.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_wave2_positive_feature_diagnostics.py --output docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.json --markdown-output docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.md
```

Results:

- `py_compile`: passed.
- focused pytest: `3 passed`.
- official diagnostic: exited 0.
- TensorFlow emitted a CUDA no-device warning despite CPU-scoped
  `CUDA_VISIBLE_DEVICES=-1`; recorded as environment noise, not GPU evidence.

## Diagnostic Summary

| Metric | Value |
| --- | ---: |
| status | `PASS` |
| wave2 status | `POSITIVE_FEATURE_SINKHORN_PASSED_DIAGNOSTIC_ONLY` |
| validity pass | `True` |
| hard vetoes | `[]` |
| max row residual | `3.221883e-05` |
| max column residual | `2.220446e-16` |
| max dense-reference particle error, explanatory | `1.487610e-01` |
| max dense-reference RMS error, explanatory | `8.104504e-02` |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `b4156c4b0cbfdc443440fc6df4b6044e09040abb` |
| Python | `3.13.13` |
| Device scope | CPU-scoped TensorFlow with `CUDA_VISIBLE_DEVICES=-1` |
| Diagnostic script | `docs/benchmarks/scalable_ot_wave2_positive_feature_diagnostics.py` |
| Diagnostic JSON | `docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.json` |
| Diagnostic Markdown | `docs/benchmarks/scalable-ot-wave2-positive-feature-diagnostics-2026-06-19.md` |
| Focused tests | `tests/test_positive_feature_transport_tf.py`, `tests/test_wave2_positive_feature_diagnostics.py` |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for finite feature factors, positive features, finite scalings, finite transported particles, residual thresholds, and schema-valid reporting. |
| Statistically supported ranking | None. No stochastic comparative uncertainty analysis was run. |
| Descriptive-only differences | Dense-reference particle deltas and runtime-like fields are descriptive only. |
| Default-readiness | Not assessed and not claimed. |
| Next evidence needed | Any comparative decision or default/public path would require a new reviewed comparative evidence contract. |

## Close Record

The current-agent positive-feature lane is complete and stops.  Coordinator
synthesis may begin because the peer-agent low-rank lane also has final
closeout artifacts.
