# P03 Result: Downstream LEDH Smoke

Date: 2026-06-22T02:04:12+08:00

Status: `P03_DOWNSTREAM_SMOKE_PASSED`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Passed: Nystrom resampling ran through the deterministic LEDH/PFPF-OT filtering loop without hard smoke failures. |
| Baseline/comparator | Same-harness streaming context remains explanatory only; P03 checked Nystrom route self-consistency. |
| Primary criterion | Passed: both predeclared CPU rows produced finite outputs, normalized final log weights, ESS fraction above threshold, residuals below threshold, and sentinel nonmaterialized transport shapes. |
| Veto diagnostics | No hard veto fired. |
| Explanatory diagnostics | Runtime, memory proxy, state summary magnitudes, and step diagnostics. |
| Not concluded | No posterior correctness, speedup, ranking, default readiness, GPU readiness, HMC readiness, or public API readiness. |

## Commands And Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Exact P03 run | `PASS` | `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py --mode downstream-smoke --device-scope cpu --output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.md > docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.log 2>&1` |
| JSON parse | `PASS` | `python -m json.tool docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.json` |

CPU-hidden TensorFlow emitted no phase-veto evidence. GPU evidence was not
requested or used for P03.

## Diagnostic Summary

| Metric | Value |
| --- | ---: |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Passed rows | `2 / 2` |
| Max row residual | `2.8744214464193618e-05` |
| Max column residual | `1.1102230246251565e-16` |
| Max output log-weight residual | `0.0` |
| Min ESS fraction | `0.9999939940500705` |
| Wall time | `0.32868878194130957` seconds in the recorded JSON |

## Rows

| Fixture id | N | Rank | Status | ESS fraction | Row residual | Column residual | Transport shapes |
| --- | ---: | ---: | --- | ---: | ---: | ---: | --- |
| `nystrom_ledh_smoke_n64_rank8` | 64 | 8 | `PASS` | `0.9999941345181469` | `2.8744214464193618e-05` | `1.1102230246251565e-16` | `[[1, 0, 0], [1, 0, 0]]` |
| `nystrom_ledh_smoke_n128_rank16` | 128 | 16 | `PASS` | `0.9999939940500705` | `2.7929399874171423e-05` | `1.1102230246251565e-16` | `[[1, 0, 0], [1, 0, 0]]` |

## Artifacts

- `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.json`
- `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.md`
- `docs/benchmarks/logs/scalable-ot-nystrom-ledh-pfpf-algorithm-complete-p03-downstream-smoke-2026-06-21.log`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p03-downstream-smoke-result-2026-06-21.md`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Proceed to P04 GPU preflight | `PASS` | No P03 veto fired | Trusted GPU availability and scale rows are still untested | Run trusted `nvidia-smi` preflight and then P04 if a usable GPU exists | No GPU readiness, speedup, posterior correctness, HMC readiness, default readiness, or ranking |
