# P8g-G1 Subplan: Current Bottleneck Profile

Date: 2026-06-15

Status: `READY_FOR_G1_PROFILE_LAUNCH`

## Phase Objective

Profile the current repaired P8d LEDH path to identify whether a GPU
vectorization route is admissible and where the Python particle/time loops
dominate.

## Entry Conditions

- G0 trusted GPU probe passed and its manifest path is cited:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md`.
- G0 result has read-only Claude review recorded in the canonical
  `Review Loop Ledger`.
- P8e repaired adapter code is present.
- No serious GPU tuning or gradient run has started.

## Required Artifacts

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-result-2026-06-15.md`
- CPU/GPU profile summary.
- First vectorization-target list.
- Decision: `PASS_PROFILE_VECTOR_TARGET_IDENTIFIED` or
  `BLOCK_P8G_GPU_PROFILE_NO_ADMISSIBLE_VECTOR_TARGET`.

## Required Checks/Tests/Reviews

- Short CPU reference profile on LEDH SV-style row.
- Short trusted GPU profile on the same row.
- Explicit device placement/no-silent-CPU-fallback diagnostics.
- `python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `git diff --check`
- Claude read-only review of the profile result before G2.

## Planned Command And Artifact Contract

Repository root: `/home/chakwong/BayesFilter`.

Environment assumptions:

- G0 result artifact is passed by path and cited in the profile result;
- CPU reference profile hides GPU with `CUDA_VISIBLE_DEVICES=-1`;
- trusted GPU profile uses the same row, horizon prefix, seed set, and particle
  count as the CPU profile unless the result explains a reviewed exception.

Exact planned commands:

- compile check, non-GPU:
  `python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- formatting check, non-GPU:
  `git diff --check`
- CPU profiling entry point, to be implemented or confirmed in G1 before use:
  `python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8g-ledh-prefix --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --horizon 50 --particles 32 --seeds 81120,81121,81122,81123,81124 --device cpu --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-cpu-2026-06-15.json`
- trusted GPU profiling entry point, same shape:
  `python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --profile-p8g-ledh-prefix --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --horizon 50 --particles 32 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-gpu-2026-06-15.json`

If the profile CLI flags do not exist, G1 must first add a focused profiling
entry point within the P8d/P8g runner lane, rerun compile and focused tests, and
record that implementation in the result.

Phase-local output paths:

- required phase result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-result-2026-06-15.md`;
- CPU profile JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-cpu-2026-06-15.json`;
- GPU profile JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-gpu-2026-06-15.json`.

Approval boundary:

- trusted GPU profile requires explicit launch approval after G0 passes;
- no full-horizon tuning or implementation rewrite is authorized in G1.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is there a concrete batched TensorFlow rewrite target that can plausibly make P8g GPU execution useful? |
| Baseline/comparator | Current CPU reference and trusted GPU profile of the existing implementation. |
| Primary criterion | Identify vectorizable hotspots and project feasibility for at least five-seed full-horizon `N=32` LEDH SV-style gate within a recorded budget. |
| Veto diagnostics | Serious route still dominated by unvectorizable Python loops; silent CPU fallback; profile does not cite G0 manifest; profile commands do not answer bottleneck question. |
| Explanatory diagnostics | Time by phase, device placement, loop counts, op placement, memory observations. |
| Not concluded | GPU implementation correctness or speedup after rewrite. |

## Forbidden Claims/Actions

- Do not start vectorized implementation without a vectorization target.
- Do not claim speedup from existing GPU execution if kernels fall back to CPU.

## Next-Phase Handoff Conditions

Advance to G2 only if G1 records a concrete batched-kernel implementation target
and a feasible runtime projection.

## Stop Conditions

- No admissible vectorization target.
- Trusted GPU path silently falls back to CPU.
- Profiling requires unapproved long runs.
