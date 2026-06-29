# P91 Phase 6 Result: CPU/GPU/Batched Performance Benchmark

Date: 2026-06-29

Status: `PASS_P91_PHASE6_PERFORMANCE_BENCHMARK`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 6 ran the reviewed CPU-only and trusted GPU/XLA local complete-data Zhao-Cui SIR d18 single/batched benchmark harness and merged the split manifests into the final benchmark JSON. |
| Primary criterion status | Passed: CPU and trusted GPU/XLA single/batched timings completed with finite outputs/scores, no OOM, no retries, no post-warmup retracing, explicit compile/warmup versus steady timing, and no closed-rule pathology. |
| Veto diagnostic status | Passed: CPU run hid GPU; GPU run used trusted execution and recorded `actual_xla_status == true`, GPU output devices, finite values/scores, no retracing, no OOM, no retries, and no closed-rule pathology. |
| Main uncertainty | This is one deterministic local complete-data fixture. It detects obvious pathologies and gives model-specific timing evidence for this fixture only; it does not establish universal GPU speed superiority or scientific validity. |
| Next justified action | Review this Phase 6 result and the refreshed Phase 7 HMC smoke subplan. |
| What is not being concluded | No score identity proof, exact likelihood correctness, HMC posterior validity, universal GPU speed superiority, packaging/default readiness, or production readiness. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Are CPU/GPU single/batched Zhao-Cui performance profiles acceptable and model-specific recommendations evidence-backed? |
| Baseline/comparator | CPU single route, CPU batched route, trusted GPU/XLA single route, and trusted GPU/XLA batched route on the same deterministic local complete-data fixture. |
| Primary criterion | Passed: all reviewed benchmark cells completed with finite outputs and no closed-rule pathology. |
| Veto diagnostics | Passed: no universal GPU-speed claim, untrusted GPU evidence, missing XLA status, missing compile/steady separation, hidden OOM/retry, closed-rule pathology, or speed-as-scientific-validity claim. |
| Explanatory diagnostics | First-call/compile-warmup times, steady times, per-item timing, trace counts, device placement, TensorFlow/CUDA metadata, and CPU/GPU visibility. |
| Not concluded | No posterior correctness, exact likelihood correctness, score identity proof, release/default readiness, or production readiness. |
| Artifact | CPU manifest, GPU manifest, final combined benchmark JSON, this result, and refreshed Phase 7 subplan. |

## Commands

Implementation checks:

```bash
git diff --check -- scripts/p91_performance_benchmark.py docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/p91_performance_benchmark.py
```

CPU-only benchmark:

```bash
CUDA_VISIBLE_DEVICES=-1 python scripts/p91_performance_benchmark.py --target cpu --xla false --manifest docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-cpu-2026-06-29.json
```

Trusted GPU/XLA benchmark:

```bash
nvidia-smi
python scripts/p91_performance_benchmark.py --target gpu --xla true --manifest docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-gpu-2026-06-29.json
```

Finalization:

```bash
python scripts/p91_performance_benchmark.py --merge docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-cpu-2026-06-29.json docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-gpu-2026-06-29.json --manifest docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-2026-06-29.json
```

## Manifest Summary

Final manifest:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-2026-06-29.json`

Split manifests:

- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-cpu-2026-06-29.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-gpu-2026-06-29.json`

Final status:

```text
PASS_P91_PHASE6_PERFORMANCE_BENCHMARK
```

| Target | Cell | First call seconds | Steady mean seconds | Steady per item seconds | Trace counts | Output device | Pathology |
| --- | --- | ---: | ---: | ---: | --- | --- | --- |
| CPU | looped single | `0.7272` | `0.003419` | `0.003419` | `0 -> 1 -> 1` | CPU:0 | none |
| CPU | batched | `1.2589` | `0.003698` | `0.000924` | `0 -> 1 -> 1` | CPU:0 | none |
| GPU/XLA | looped single | `1.8099` | `0.000901` | `0.000901` | `0 -> 1 -> 1` | GPU:0 | none |
| GPU/XLA | batched | `5.6662` | `0.001779` | `0.000445` | `0 -> 1 -> 1` | GPU:0 | none |

Closed-rule pathology status:

- `pathology_detected = false`
- `pathology_reasons = []`

Interpretation:

- On this deterministic local complete-data fixture, GPU/XLA steady time is
  faster than CPU for both single and batched routes.
- Batched per-item steady time is better than looped single per-item time on
  both CPU and GPU/XLA.
- These timings are explanatory and model/fixture-specific; they do not prove
  GPU is universally faster.

## Runtime Notes

- CPU-only benchmark intentionally set `CUDA_VISIBLE_DEVICES=-1`.
- The CPU and finalization commands emitted TensorFlow CUDA initialization
  warnings in the sandboxed context. The CPU manifest records no TensorFlow
  visible GPU devices and is the authoritative CPU evidence.
- Trusted GPU evidence comes from the trusted `nvidia-smi` command and the
  trusted GPU/XLA benchmark manifest.
- The GPU/XLA benchmark recorded TensorFlow GPU output devices and
  `actual_xla_status == true`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Worktree status | Dirty research worktree; unrelated dirty changes preserved. |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| Conda environment | `tf-gpu` |
| Execution target | CPU-only and trusted GPU/XLA local complete-data value/autodiff-score benchmark. |
| CPU/GPU status | CPU benchmark hid GPU; GPU benchmark used trusted/escalated execution; final merge was JSON finalization only. |
| Data version | `N/A`; deterministic local complete-data fixture. |
| Random seeds | `N/A`; deterministic fixture. |
| Wall time | CPU benchmark shell run `7.45s`; trusted GPU/XLA benchmark shell run `14.20s`; finalization shell run `8.25s`; local diff and py_compile checks exited 0. |
| Phase 6 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-subplan-2026-06-29.md` |
| Harness | `scripts/p91_performance_benchmark.py` |
| CPU manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-cpu-2026-06-29.json` |
| GPU manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-gpu-2026-06-29.json` |
| Final manifest | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-2026-06-29.json` |
| Result | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-result-2026-06-29.md` |
| Refreshed Phase 7 subplan | `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-subplan-2026-06-29.md` |

## Phase 7 Handoff

Phase 7 may proceed only after Claude review agrees on this Phase 6 result and
the refreshed Phase 7 HMC smoke subplan. Phase 7 must preserve that Phase 6 is
a deterministic local fixture benchmark and not score identity, HMC posterior
validity, release/default readiness, or production readiness.
