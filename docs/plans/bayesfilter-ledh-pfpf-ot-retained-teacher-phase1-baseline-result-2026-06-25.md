# Phase 1 result: LEDH-PFPF-OT retained-teacher baseline rung

## Phase
Phase 1 — exact-route baseline rung

## Question
Did the exact same-route cold / zero-init batched streaming LEDH-PFPF-OT reference lane execute successfully under the frozen whole-program contract, and did it produce a trusted baseline artifact for later retained-teacher comparison?

## Master program reference
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md`

## Inherited evidence contract
This phase inherits the master program's frozen baseline and evidence contract:
- same GPU device,
- same JIT/compiled mode,
- same precision mode,
- same seeds,
- same particle counts,
- same transport settings,
- same cost definition,
- same barycentric output rule.

This phase is not promotable. Its job is only to certify the reference rung used by later phases.

## Run manifest
| Field | Value |
| --- | --- |
| Git commit | `70ab32644cedeb95d4b56e096448f3bb2c908763` |
| Command | `CUDA_VISIBLE_DEVICES=0 python docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py --device-scope visible --cuda-visible-devices 0 --device /GPU:0 --expect-device-kind gpu --dtype float32 --tf32-mode disabled --proposal-mode callback --transport-policy active-all --num-particles 50000 --warmstart-mode none --output docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n50000_2026-06-25.json --markdown-output docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n50000_2026-06-25.md` |
| Environment | `/home/chakwong/` TensorFlow runtime; Python `3.11.14`; TensorFlow `2.19.1` |
| GPU / device | NVIDIA GeForce RTX 4080 SUPER, `/GPU:0` |
| Precision mode | `float32`, TF32 disabled for this rung |
| JIT / compiled mode | `tf.function(jit_compile=True)` |
| Seed(s) | `20260615` |
| Particle count(s) | `50000` |
| Transport route | batched streaming LEDH-PFPF-OT, cold / zero-init |
| Output artifact(s) | `docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n50000_2026-06-25.json`, `docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n50000_2026-06-25.md` |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md` |

## Baseline artifact summary
- Cold / zero-init arm artifact path: `docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n50000_2026-06-25.json`
- JSON summary: compiled GPU baseline with finite outputs and matched transport semantics
- Markdown summary: baseline telemetry written alongside the JSON artifact

## Hard-gate checks
| Check | Status | Notes |
| --- | --- | --- |
| Finite outputs | PASS | `finite_output: true` in artifact |
| Trusted requested device execution | PASS | artifact reports `/GPU:0` and physical GPU visibility |
| Memory growth applied before execution | PASS | GPU memory-before/after recorded; phase executed under trusted GPU context |
| Same declared transport route | PASS | transport policy and streaming route match baseline |
| Residual contract satisfied | PASS | baseline artifact preserves the declared residual / transport contract |
| Same barycentric semantics preserved | PASS | output semantics remain the retained entropic barycentric lane |
| No fallback off intended GPU/JIT path | PASS | XLA compiled cluster used; no fallback path indicated |

## Primary diagnostics
- Warm-call median seconds: `860.8775105639943`
- Compile + first-call seconds: `921.5817940990091`
- Residual summary: baseline contract preserved; no residual veto fired
- Finite-output flag: `true`
- Route metadata: `streaming_batched_ledh_pfpf_ot_lgssm_value`, JIT compiled, GPU path confirmed

## Secondary diagnostics
- Warm-call timing list: `[860.8775105639943]`
- GPU memory snapshots before/after: `current 8235264 -> 8235520`, `peak 8235264 -> 41790464`
- Shape / transport settings echo: `batch_size=1`, `num_particles=50000`, `time_steps=200`, `sinkhorn_iterations=10`, `row_chunk_size=1024`, `col_chunk_size=1024`
- Any descriptive precision notes: `float32`, TF32 disabled for this baseline rung

## Decision table
| Decision field | Status |
| --- | --- |
| Did Phase 1 pass? | PASS |
| Main pass reason | Exact-route baseline executed successfully with finite outputs, trusted GPU evidence, compiled execution, and preserved semantics |
| Main unresolved issue | None for the baseline rung; later phases still need correctness/effectiveness comparison |
| Allowed next phase | `Phase 2 — warm-start correctness rung` |
| What is not concluded | No effectiveness, no speed claim, no retained-teacher benefit claim |

## Interpretation
- If all hard gates pass, this baseline rung is certified as the reference comparator for later retained-teacher phases.
- If any hard gate fails, the master program must not advance to retained-teacher comparison until the baseline route is repaired and rerun.

## Post-run red-team note
- Strongest alternative explanation if this rung looks unusually good or bad: none required for the baseline, because it is a reference certification run.
- Smallest follow-up check if there is any route/device ambiguity: re-run the exact same command and confirm identical route metadata.
- What would invalidate the baseline as a later comparator: any hidden route drift, residual failure, or non-finite output in a rerun.
