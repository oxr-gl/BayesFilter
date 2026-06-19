# P8n Result: SIR d18 Full-Filter Chunk Comparison

metadata_date: 2026-06-18
status: PASS_CURRENT_MATCHED_EVIDENCE_FAVORS_1024
plan: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-full-filter-chunk-comparison-plan-2026-06-18.md
executor: Codex

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | In current matched actual-SIR d18 full-filter runs, `row/col=1024/1024` is faster than `2048/2048` at both `N=10000` and `N=50000`. |
| Primary criterion status | Passed for the local comparison.  All four trusted-GPU artifacts are finite, GPU-backed, and metadata-complete. |
| Veto diagnostic status | No CPU fallback, OOM, nonfinite output, missing metadata, or model/seed/history/Sinkhorn mismatch. |
| Main uncertainty | The `N=10000` `2048` warm timings were noisy, and this is still one SIR d18 fixture, not a cross-model default-policy proof. |
| Next justified action | Use `1024/1024` as the preferred SIR d18 benchmark setting for near-term full-filter runs; require cross-fixture validation before changing broad defaults. |
| What is not concluded | No particle-count adequacy, MC-SE adequacy, leaderboard completion, exact likelihood correctness, DPF gradient correctness, HMC/NUTS readiness, production readiness, or cross-model/default-policy readiness. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Compare actual SIR d18 full-filter wall time for `1024/1024` versus `2048/2048` chunks at `N=10000` and `N=50000`. |
| Baseline/comparator | Same harness, seeds, TF32/GPU, `transport-policy active-all`, `sinkhorn_iterations=10`, `sinkhorn_epsilon=1.0`, `particle_chunk_size=1024`, and `history-mode full`; only row/column chunk size changes. |
| Primary criterion | Trusted-GPU artifacts are finite and GPU-backed; candidate is faster only if its warm-call mean is lower under matched settings for the same `N`. |
| Veto diagnostics | CPU fallback, nonfinite output, OOM, missing metadata, changed model/seed/Sinkhorn/particle chunk/history settings, or unsupported broad default claims. |
| Explanatory diagnostics | Compile-plus-first-call time, warm-call timings, TensorFlow GPU memory counters, speedup versus legacy scalar comparator, output log likelihoods, ESS minima. |

## Checks

Local checks before GPU runs:

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-full-filter-chunk-comparison-plan-2026-06-18.md docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
```

Both passed.

Trusted GPU preflight:

```bash
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
```

Observed:

- NVIDIA GeForce RTX 4080 SUPER, 16376 MiB, driver 591.86.

Post-run JSON assertions passed:

- all four artifacts have `finite_output=true`;
- all expected outputs are on GPU;
- all preserve actual SIR d18 shape and metadata;
- `particle_chunk_size=1024`, TF32 enabled, `history-mode full`,
  `transport-policy active-all`, Sinkhorn 10, epsilon 1.0.

## Results

| N | Row/col chunk | Warm timings seconds | Warm mean seconds | Compile + first seconds | Peak GPU memory counter bytes | Legacy scalar speedup |
| ---: | ---: | --- | ---: | ---: | ---: | ---: |
| 10000 | 1024 | `[8.460080, 8.798238]` | 8.629159 | 21.798881 | 84075520 | 91.521744 |
| 10000 | 2048 | `[23.212110, 10.173980]` | 16.693045 | 50.452710 | 210641920 | 47.310462 |
| 50000 | 1024 | `[140.195284]` | 140.195284 | 157.426766 | 184149248 | 5.633254 |
| 50000 | 2048 | `[187.547440]` | 187.547440 | 180.395486 | 225041920 | 4.210965 |

Relative comparison:

| N | Runtime ratio `2048/1024` | `1024` speedup vs `2048` | Peak memory ratio `2048/1024` |
| ---: | ---: | ---: | ---: |
| 10000 | 1.934493 | 48.306861% | 2.505389 |
| 50000 | 1.337759 | 25.248095% | 1.222063 |

## Output Diagnostics

ESS minima matched exactly within each `N` pair:

- `N=10000`: `[6441.296875, 6432.78173828125, 6482.1669921875,
  6511.61083984375, 6437.65673828125]`
- `N=50000`: `[32286.685546875, 32056.00390625, 32381.6875,
  32084.078125, 31872.62109375]`

Log likelihoods differed slightly between chunk sizes, consistent with
different floating-point accumulation order under different tiling:

| N | Max absolute log-likelihood delta | Mean absolute log-likelihood delta |
| ---: | ---: | ---: |
| 10000 | 0.06512451171875 | 0.035009765625 |
| 50000 | 0.01629638671875 | 0.00570068359375 |

These deltas are explanatory diagnostics.  P8n does not establish exact
likelihood correctness or scientific adequacy.

## Artifacts

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n10000-chunk1024-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n10000-chunk1024-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n10000-chunk2048-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n10000-chunk2048-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n50000-chunk1024-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n50000-chunk1024-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n50000-chunk2048-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n50000-chunk2048-2026-06-18.md`

## Interpretation

The real full-filter SIR d18 test supports `1024/1024` as the better near-term
benchmark setting on this GPU.  This corrects the earlier ambiguity from the
synthetic transport-core microbenchmark: although `1024` and `2048` were nearly
tied in the synthetic core, the full model run favored `1024`.

The result should not be generalized into a repository-wide default yet.  It is
strong enough to use `1024/1024` for SIR d18 follow-up runs, including the
larger `N=50000` practical setting.

## Memory / Leak Boundary

The TensorFlow peak memory counter was lower for `1024/1024` in both matched
pairs.  The absolute difference is not important on a 16 GB card for these
value-only full-filter runs.  It is recorded as a headroom diagnostic.

This run does not prove or disprove a memory leak.  Each chunk setting ran in a
separate process, and the artifacts record only before/after counters per
process, not per-repeat allocator growth inside a long-lived process.

## Post-Run Red Team

Strongest alternative explanation:

- `N=10000` `2048/2048` had noisy repeats, so its exact mean may be overstated.

What would overturn the near-term decision:

- A replicated same-process or cross-fixture run where `2048/2048` is
  consistently faster or equally fast without worse memory behavior.

Weakest part of the evidence:

- `N=50000` used one warm repeat per chunk because of runtime cost.
