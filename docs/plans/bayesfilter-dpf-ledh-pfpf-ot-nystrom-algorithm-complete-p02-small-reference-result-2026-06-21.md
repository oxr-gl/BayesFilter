# P02 Result: Small Dense-Reference Validation

Date: 2026-06-22T02:02:38+08:00

Status: `P02_SMALL_REFERENCE_PASSED`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Passed: each required fixture had at least one predeclared Nystrom rank meeting the small dense-reference screen. |
| Baseline/comparator | Dense TensorFlow `annealed_transport_resample_tf` on the same small fixtures. |
| Primary criterion | Passed: top-level hard vetoes are empty; all required fixtures have at least one viable rank; candidate rows remain nonmaterialized with sentinel `[0, 0]` transport shapes. |
| Veto diagnostics | No phase-level veto fired. One non-promoted row (`high_dim_low_rank`, rank `2`) missed the dense max-error threshold and remains a row-level diagnostic only. |
| Explanatory diagnostics | Runtime, memory proxy, row-level dense-reference errors, and landmark indices. |
| Not concluded | No large-N scalability, GPU readiness, speedup, posterior correctness, default readiness, HMC readiness, public API readiness, or ranking. |

## Commands And Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Exact P02 run | `PASS` | `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py --mode small-reference --device-scope cpu --output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.md > docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.log 2>&1` |
| JSON parse | `PASS` | `python -m json.tool docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.json` |
| Repair syntax check | `PASS` | `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py tests/test_nystrom_ledh_pfpf_algorithm_complete.py` |
| Focused tests after repair | `PASS` | `pytest -q tests/test_nystrom_transport_tf.py tests/test_nystrom_ledh_pfpf_algorithm_complete.py`: `8 passed in 4.08s` |

CPU-hidden TensorFlow emitted a `cuInit` no-device warning in the log. This is
sandbox/environment noise and not GPU evidence.

## Diagnostic Summary

| Metric | Value |
| --- | ---: |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Passed rows | `14 / 15` |
| Max row residual | `9.902792837324093e-05` |
| Max column residual | `2.220446049250313e-16` |
| Max dense-reference particle error | `0.08564275772586204` |
| Max dense-reference RMS error | `0.026235230425731913` |
| Wall time | `2.0806500411126763` seconds in the recorded JSON |

The maximum dense-reference particle error comes from `high_dim_low_rank` rank
`2`, which did not pass the row screen. The P02 promotion gate is fixture-level:
at least one predeclared rank per required fixture must pass.

## Viable Ranks

| Fixture | Viable ranks |
| --- | --- |
| `tiny_manual` | `2, 3, 4` |
| `small_parity` | `2, 4, 8` |
| `high_dim_low_rank` | `4, 8, 16, 32` |
| `ledh_specific_smoke` | `4, 8, 16, 32` |

## Artifacts

- `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.json`
- `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.md`
- `docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p02-small-reference-2026-06-21.log`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p02-small-reference-result-2026-06-21.md`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Proceed to P03 | `PASS` | No phase-level veto fired | Downstream LEDH loop may still fail smoke thresholds | Run P03 exact downstream-smoke command after fresh audit/evidence contract | No GPU readiness, speedup, posterior correctness, HMC readiness, default readiness, or ranking |

