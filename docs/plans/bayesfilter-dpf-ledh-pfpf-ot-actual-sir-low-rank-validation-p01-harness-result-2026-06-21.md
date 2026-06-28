# P01 Harness Integration Result

Date: 2026-06-21

Status: `PASS`

## Phase Objective

Create an owned actual-SIR route-validation harness that preserves the existing
P8j actual-SIR callback/tensor semantics and adds route selection for
`streaming` and `low_rank`.

## Artifacts Created

| Artifact | Path |
| --- | --- |
| Harness | `docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py` |
| Focused tests | `tests/test_actual_sir_low_rank_route_validation.py` |
| Tiny P01 JSON artifact | `docs/benchmarks/actual-sir-low-rank-route-validation-p01-harness-smoke-2026-06-21.json` |
| Tiny P01 Markdown artifact | `docs/benchmarks/actual-sir-low-rank-route-validation-p01-harness-smoke-2026-06-21.md` |

## Checks Run

| Command | Result |
| --- | --- |
| `python -m py_compile docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py` | `PASS` |
| `pytest tests/test_actual_sir_low_rank_route_validation.py -q` | `PASS`, 3 passed |
| `pytest tests/test_low_rank_coupling_solver_tf.py tests/test_low_rank_ledh_pfpf_integration_smoke.py -q` | `PASS`, 6 passed |
| CPU-hidden tiny both-route artifact command | `PASS`, no hard vetoes |

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Actual-SIR semantics | `PASS`; artifact records `zhao_cui_spatial_sir_austria_j9_T20`, `D=18`, `M=9`, and actual callback usage. |
| Route-fired evidence | `PASS` on tiny P01 artifact; streaming and low-rank each fired once for one active step. |
| Low-rank diagnostics | `PASS` on tiny P01 artifact; nonmaterialized `[1,0,0]` sentinel, finite nonnegative factors, positive `g`, and max factor residual below `5e-3`. |
| Shared/public boundaries | `PASS`; no public export, shared schema, existing benchmark, or low-rank solver file was edited. |

## Notes

The tiny P01 artifact was intentionally CPU-hidden and is not GPU evidence.
TensorFlow printed a CUDA initialization warning despite `CUDA_VISIBLE_DEVICES=-1`;
the artifact records CPU output devices, no logical GPUs, and selected physical
GPU status `cpu_hidden`.

## Nonclaims

- No actual-SIR speedup claim.
- No large-N feasibility claim.
- No posterior correctness claim.
- No HMC readiness claim.
- No public API/default readiness claim.

## Next Phase Handoff

Advance to P02 tiny actual-SIR route smoke. The next subplan is
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p02-smoke-subplan-2026-06-21.md`.

P02 should run bounded actual-SIR rows for both routes, preserve JSON/Markdown
artifacts, and treat tiny timing as explanatory only.
