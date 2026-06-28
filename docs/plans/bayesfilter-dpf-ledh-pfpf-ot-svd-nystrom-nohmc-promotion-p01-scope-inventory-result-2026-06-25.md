# P01 Result: Scope, Inventory, And Harness Readiness

Date: 2026-06-25

Status: `P01_PASS_TO_P02_LGSSM_REFERENCE`

## Phase Objective

Verify the current code/artifact/test surface can support the SVD-Nystrom
no-HMC promotion program before material model-suite GPU phases.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the local harness surface ready for no-HMC SVD-Nystrom promotion testing? |
| Baseline/comparator | P06/P07 evidence plus existing test/harness inventory. |
| Primary criterion | Inventory identifies executable next paths and focused local tests pass. |
| Veto diagnostics | Missing P06/P07 artifacts, missing SVD metadata tests, local test failure, active-path NumPy evidence, or inability to define executable next phase. |
| Explanatory diagnostics | File lists, test names, existing artifact provenance. |
| Not concluded | No model-suite validity, no GPU readiness, no promotion, no statistical ranking. |
| Artifact | `docs/benchmarks/svd-nystrom-nohmc-promotion-p01-scope-inventory-2026-06-25.json` |

## Required Checks

| Check | Status |
| --- | --- |
| Parse P06 summary | PASS: `P06_PASS_TO_P07_EVIDENCE_PACKAGE`, `14/14` deterministic-valid, `0/14` exceedances, CP upper `0.1926361756501353 <= 0.20` |
| Parse P07 closeout | PASS: status and nonclaim boundaries present |
| Inventory SVD-Nystrom surfaces | PASS: compiled-redo harness and transport implementation expose SVD metadata |
| Verify focused metadata tests | PASS: `tests/test_actual_sir_nystrom_compiled_redo.py` covers `svd_truncated`, `core_rcond`, kernel mode, and scaling metadata |
| Run focused local tests | PASS: `16 passed` in `30.86s` with `CUDA_VISIBLE_DEVICES=-1` |
| Review P02 subplan | PASS WITH KNOWN GAP: P02 must establish a fair SVD-Nystrom LGSSM exact-reference path or write a blocker |

## Test Manifest

Command:

```bash
timeout 300 env CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_actual_sir_nystrom_compiled_redo.py tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_default_promotion.py
```

Log:

- `docs/plans/logs/svd-nystrom-nohmc-promotion-2026-06-25/p01-focused-local-tests.log`

Result:

- `16 passed, 15109 warnings in 30.86s`

Warning classification: TensorFlow/TFP/gast deprecation warnings only; no test
failure.

## Inventory Summary

| Surface | Status |
| --- | --- |
| `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py` | Present; supports `svd_truncated` and `core_rcond` |
| `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` | Present; exposes SVD policy metadata and command flags |
| `docs/benchmarks/run_actual_sir_nystrom_threshold_calibration_p06.py` | Present; locks P06 SVD policy |
| `tests/test_nystrom_transport_tf.py` | Present; covers truncated SVD solver |
| `tests/test_actual_sir_nystrom_compiled_redo.py` | Present; covers compiled-redo SVD metadata |
| LGSSM exact-reference surface | Low-rank LGSSM reference surface exists; dedicated SVD-Nystrom LGSSM harness is not yet established |

## Inference Status

| Row | Status |
| --- | --- |
| Hard veto screen | PASS for P01 inventory/local tests |
| Statistically supported ranking | NO |
| Descriptive-only differences | N/A in P01 |
| Default-readiness | NO |
| Next evidence needed | P02 exact-reference LGSSM gate or blocker if no fair executable SVD-Nystrom LGSSM harness exists |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass to P02 | PASS | No P01 veto fired | P02 may need harness work or an honest blocker for fair SVD-Nystrom LGSSM exact-reference execution | Launch P02 preflight and exact-reference harness assessment | No promotion, no model-suite validity, no GPU readiness, no HMC readiness, no statistical ranking |

## Next-Phase Handoff

`P01_PASS_TO_P02_LGSSM_REFERENCE`

P02 must first perform trusted GPU preflight and determine whether a fair
SVD-Nystrom LGSSM exact-reference harness exists or can be created within the
bounded docs/benchmark/test edit scope. If not, P02 must write
`P02_BLOCKED` rather than substituting a low-rank-only result.
