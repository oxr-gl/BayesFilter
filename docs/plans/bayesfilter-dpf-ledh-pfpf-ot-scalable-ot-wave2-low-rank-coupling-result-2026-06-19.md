# Wave 2 Result: Peer-Agent Low-Rank Coupling Validation

Date: 2026-06-19
Owner: peer agent

## Status

`LOW_RANK_COUPLING_VALIDATION_PASSED_DIAGNOSTIC_ONLY`

## Decision Table

| Decision field | Status |
| --- | --- |
| Decision | Close the Wave 2 peer-agent low-rank coupling validation lane as diagnostic-only passed under its own hard-veto screen. |
| Primary criterion status | Passed: CPU-only validation JSON status is `PASS`, hard vetoes are `[]`, candidate record validates under Phase 3 schema, factors/particles are finite, `Q,R` are nonnegative, `g` is positive, residuals pass thresholds, and materialized tiny apply parity passes. |
| Veto diagnostic status | No hard vetoes or continuation vetoes fired. |
| Main uncertainty | This remains a diagnostic solver-route validation.  The simplified update and cost-nudged assignment kernel are `extension_or_invention`, so full low-rank Sinkhorn solver fidelity is not established. |
| Next justified action | Coordinator may consume this lane-local result after the current-agent lane also closes or blocks, preserving the diagnostic-only evidence contract. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or full solver fidelity. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | The low-rank coupling solver-route candidate passed a Wave 2 lane-local hard-veto validation screen for finite nonnegative `Q,R,g` factors, finite transported particles, valid lazy/materialized apply parity, Phase 3 candidate-record validity, and preserved source/boundary classifications. |
| Baseline/comparator | P12 diagnostic result is entry context. Phase 1 dense/streaming baseline is not a promotion comparator in this Wave 2 lane. Runtime, memory, and any dense-reference deltas are explanatory only. |
| Primary pass criterion | Passed. |
| Veto diagnostics | No missing/invalid `Q,R,g`, sign/finite failure, residual threshold failure, apply-parity failure, schema failure, source-route overclaim, positive-feature artifact dependency, external solver execution, package/network/GPU requirement, public export/default edit, or shared contract change occurred. |
| Explanatory diagnostics | Projection iterations, projection error, floor hits, factor minima, fixture shapes, rank, and wall time. |
| Preserving artifacts | Wave 2 peer-lane plan/result/status files, validation script, tests, JSON, and Markdown diagnostics. |

## Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-master-program-2026-06-19.md`
- Status:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-status-2026-06-19.md`
- P00 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-p00-governance-intake-result-2026-06-19.md`
- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-p01-validation-replay-result-2026-06-19.md`
- Validation script:
  `docs/benchmarks/scalable_ot_wave2_low_rank_coupling_validation.py`
- Focused tests:
  `tests/test_wave2_low_rank_coupling_validation.py`
- Diagnostic JSON:
  `docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.json`
- Diagnostic Markdown:
  `docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.md`

## Checks

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile \
  docs/benchmarks/scalable_ot_wave2_low_rank_coupling_validation.py \
  tests/test_wave2_low_rank_coupling_validation.py

CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_low_rank_coupling_solver_tf.py \
  tests/test_wave2_low_rank_coupling_validation.py

CUDA_VISIBLE_DEVICES=-1 python \
  docs/benchmarks/scalable_ot_wave2_low_rank_coupling_validation.py \
  --output docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.json \
  --markdown-output docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.md
```

Observed:

- focused pytest: `5 passed`;
- diagnostic JSON status: `PASS`;
- wave2 status: `LOW_RANK_COUPLING_VALIDATION_PASSED_DIAGNOSTIC_ONLY`;
- validity pass: `True`;
- hard vetoes: `[]`;
- candidate record schema validation: passed.

## Diagnostic Summary

| Metric | Value | Role |
| --- | ---: | --- |
| max factor marginal residual | `1.1449623765757977e-07` | hard veto |
| max induced row residual | `5.267489473492759e-07` | hard veto |
| max induced column residual | `5.724811882323877e-07` | hard veto |
| max materialized tiny apply parity | `1.1102230246251565e-16` | hard veto |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for finite factors, positive `g`, finite transported particles, residual thresholds, apply parity, source-route boundary preservation, and schema validation. |
| Statistically supported ranking | None.  No comparative uncertainty analysis was run. |
| Descriptive-only differences | Projection iteration counts, wall time, factor minima, and projection diagnostics are descriptive/explanatory. |
| Default-readiness | Not established. |
| Next evidence needed | Separate coordinator synthesis after both Wave 2 lanes close or block; any stronger solver-fidelity claim would require source-anchored algorithmic review beyond this diagnostic validation. |

## Boundary Record

- Did not edit positive-feature lane files.
- Did not use positive-feature intermediate artifacts as evidence.
- Did not edit Phase 1 baseline, Phase 3 schema, public exports/defaults, or
  coordinator synthesis files.
- Did not use package installs, network, external POT/OTT solver execution, or
  GPU evidence.

## Post-Run Red-Team Note

Strongest alternative explanation: the validation fixtures may exercise a
well-conditioned deterministic route that preserves factor constraints without
establishing full low-rank Sinkhorn solver fidelity or downstream filtering
value.

Result that would overturn this closeout: a focused source or schema review
showing the recorded `Q,R,g` convention, orientation, lazy apply, residuals,
or source-route classification are inconsistent with the Wave 2 contract.

Weakest evidence point: the cost-nudged assignment kernel and simplified update
remain `extension_or_invention`.

## Close Record

The peer-agent Wave 2 low-rank coupling validation lane is complete and stops
here.  Coordinator merge/synthesis is deferred until the current-agent lane
also closes or blocks, and must preserve the non-comparative evidence contract.
