# P01 Result: Nystrom Implementation Harness

Date: 2026-06-22T01:04:25+08:00

Status: `P01_IMPLEMENTATION_HARNESS_PASSED`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Passed: a dedicated Nystrom LEDH/PFPF-OT diagnostic harness now exists. |
| Baseline/comparator | Dense TensorFlow `annealed_transport_resample_tf` is used only in `small-reference`; downstream and GPU modes test the Nystrom route self-consistency. |
| Primary criterion | Passed: harness and tests compile, focused tests pass, and the harness exposes `small-reference`, `downstream-smoke`, and `gpu-scale` modes with required schema/nonclaim/provenance fields. |
| Veto diagnostics | No P01 veto fired. Candidate route records sentinel `[0, 0]` transport matrix shapes and `transport_matrix_materialized: false`. |
| Explanatory diagnostics | Test runtime and dependency deprecation warnings only. No algorithm viability, speedup, or default readiness is inferred. |
| Not concluded | No Nystrom benefit, no speedup, no ranking, no posterior correctness, no HMC readiness, no dense Sinkhorn equivalence beyond later checked small fixtures, and no production/default readiness. |

## Files Created

- `docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py`
- `tests/test_nystrom_ledh_pfpf_algorithm_complete.py`

## Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Syntax | `PASS` | `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py docs/benchmarks/scalable_ot_nystrom_ledh_pfpf_algorithm_complete.py tests/test_nystrom_ledh_pfpf_algorithm_complete.py` |
| Focused tests | `PASS` | `pytest -q tests/test_nystrom_transport_tf.py tests/test_nystrom_ledh_pfpf_algorithm_complete.py`: `8 passed in 4.09s` |
| Local artifact coverage | `PASS` | Tests cover CLI modes, reviewed small-reference fixture counts/ranks, required top-level schema fields, nonclaims, dense-reference fields, downstream row metadata, and sentinel nonmaterialized transport shapes. |

Warnings: pytest emitted TensorFlow Probability and `gast`/Python 3.13 deprecation warnings. These are dependency warnings and did not affect the P01 gate.

## Harness Coverage

The harness supports:

- `small-reference`: reviewed P02 fixture counts and ranks, dense TensorFlow comparator, Nystrom candidate rows, dense-reference error fields, factor metadata, landmark indices, and sentinel candidate transport shape.
- `downstream-smoke`: deterministic LGSSM-shaped LEDH loop with Nystrom resampling rows matching the P03 plan by default.
- `gpu-scale`: P04 required GPU rows, optional row rule, TF32/device metadata fields, and GPU hard-veto checks.

Required top-level schema fields are present:

- `algorithm_family`
- `mode`
- `status`
- `hard_vetoes`
- `run_manifest`
- `source_route`
- `source_route_components`
- `semantic_class`
- `baseline_comparator`
- `transport_object_kind`
- `transport_matrix_materialized`
- `nonclaims`

## P02 Refresh

The P02 subplan was re-read during P01 implementation. The implemented
`small-reference` defaults preserve the reviewed fixture particle counts and
rank grids:

| Fixture | Particle count | Ranks |
| --- | ---: | --- |
| `tiny_manual` | 4 | `2,3,4` |
| `small_parity` | 8 | `2,4,8` |
| `high_dim_low_rank` | 32 | `2,4,8,16,32` |
| `ledh_specific_smoke` | 32 | `4,8,16,32` |

No P02 execution was run in P01.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Proceed to P02 | `PASS` | No P01 veto fired | P02 may still fail numeric dense-reference thresholds | Run P02 exact small-reference command after a fresh pre-run evidence contract/audit | No viability, speedup, ranking, posterior correctness, HMC readiness, or default readiness |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | Current working tree commit recorded by harness/tests when run; not separately frozen here. |
| Command | See checks table. |
| Environment | CPU-hidden local test path via test `CUDA_VISIBLE_DEVICES=-1`; no trusted GPU command used. |
| CPU/GPU status | CPU-only P01 checks. GPU phase not run. |
| Seeds | Harness default seed `20260621` for deterministic fixture generation. |
| Artifacts | This result note plus the two created P01 files. |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-p01-implementation-harness-subplan-2026-06-21.md` |

