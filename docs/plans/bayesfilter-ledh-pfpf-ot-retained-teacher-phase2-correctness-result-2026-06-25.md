# Phase 2 result: LEDH-PFPF-OT retained-teacher correctness rung

## Phase
Phase 2 — warm-start correctness rung

## Question
Under the frozen whole-program contract, do the `cold`, `heuristic`, and `learned` retained-teacher arms preserve the exact same transport semantics, teacher-preservation envelope, and residual contract before any runtime comparison is interpreted?

## Master program reference
- `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md`

## Inherited evidence contract
This phase inherits the same frozen baseline and exact-route contract. The only allowed comparison is between same-route arms under matched device, precision, seed, particle count, and corrective budget.

## Run manifest
| Field | Value |
| --- | --- |
| Git commit | `70ab32644cedeb95d4b56e096448f3bb2c908763` |
| Commands | same benchmark family as Phase 1, varying only `--warmstart-mode none|heuristic|learned` |
| Environment | Python `3.11.14`, TensorFlow `2.19.1` |
| GPU / device | NVIDIA GeForce RTX 4080 SUPER, `/GPU:0` |
| Precision mode | `float32`, TF32 disabled |
| JIT / compiled mode | `tf.function(jit_compile=True)` |
| Seed(s) | `20260615` |
| Particle count(s) | `50000` |
| Corrective budget / transport settings | same as baseline: `sinkhorn_iterations=10`, `annealed_scaling=0.9`, `annealed_convergence_threshold=0.001`, row/col chunk `1024/1024`, `transport-policy active-all`, `proposal-mode callback` |
| Arms run | `cold`, `heuristic`, `learned` |
| Output artifact(s) | `docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase1_cold_gpu0_tf32off_n50000_2026-06-25.json`; `docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase2_heuristic_gpu0_tf32off_n50000_2026-06-25.json`; `docs/benchmarks/ledh_pfpf_ot_retained_teacher_phase2_learned_gpu0_tf32off_n50000_2026-06-25.json` |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md` |

## Hard-gate checks by arm
| Arm | Finite outputs | Same route metadata | Same transport settings | Trusted GPU/JIT path | Paired replay metric emitted | Pass? |
| --- | --- | --- | --- | --- | --- | --- |
| cold | PASS | PASS | PASS | PASS | baseline | PASS |
| heuristic | PASS | PASS | PASS | PASS | PASS | PASS |
| learned | PASS | PASS | PASS | PASS | PASS | CONDITIONAL |

## Primary correctness diagnostics
- Finite outputs: all three arms reported `finite_output: true`.
- Device / route preservation: all three arms reported `/GPU:0`, `jit_compile: true`, `compiled_unit: streaming_batched_ledh_pfpf_ot_lgssm_value`, `plan_mode: streaming`, `transport_policy: active-all`, and identical shape metadata.
- Visible scalar agreement:
  - cold: `820.1132202148438`
  - heuristic: `820.11328125`
  - learned: `820.113037109375`
- Paired teacher-replay discrepancy against the frozen cold reference:
  - heuristic `teacher_replay_rmse = 4.488008016778622e-06`
  - heuristic `teacher_replay_max_abs = 2.7567148208618164e-05`
  - learned `teacher_replay_rmse = 1.5392147179227322e-04`
  - learned `teacher_replay_max_abs = 6.644055247306824e-04`
- Row residual summaries:
  - cold `max_row_residual = 0.007936239242553711`
  - heuristic `max_row_residual = 0.00780797004699707`
  - learned `max_row_residual = 0.010607004165649414`
- Column residual summaries:
  - cold `max_column_residual = 0.0`
  - heuristic `max_column_residual = 0.0`
  - learned `max_column_residual = 0.0`

## Secondary diagnostics
- Compile + first-call seconds:
  - cold: `921.5817940990091`
  - heuristic: `4541.726593509025`
  - learned: `5090.462801736023`
- Warm-call median seconds:
  - cold: `860.8775105639943`
  - heuristic: `4348.624285814993`
  - learned: `4199.515477239038`
- GPU memory snapshots remain finite and consistent with successful execution on the requested GPU.
- These timing values are secondary in Phase 2; they are not interpreted as effectiveness evidence here.

## Decision table
| Decision field | Status |
| --- | --- |
| Did Phase 2 pass? | `PASS for heuristic; CONDITIONAL / NON-PROMOTED for learned` |
| Which arms preserved visible route semantics? | `cold`, `heuristic`, and `learned` all passed finite-output, device, and route-metadata checks |
| Which arm cleared the stronger paired replay check best? | `heuristic` |
| Main concern | `learned` shows materially larger replay discrepancy and a larger row residual than both `cold` and `heuristic` |
| Allowed next phase | `Phase 3` may proceed for the heuristic arm; the learned arm should not be promoted to effectiveness reading without further repair/tuning |
| What is not concluded | no learned-arm effectiveness claim; no claim that all warm-start arms preserve the teacher object equally well |

## Interpretation
- The repaired harness now emits the stronger paired replay metrics that Phase 2 originally needed.
- Under those stronger metrics, the heuristic arm looks teacher-preserving enough to advance descriptively to Phase 3.
- The learned arm remains finite and route-consistent, but it is clearly farther from the cold reference than the heuristic arm and also shows the largest row residual. That is not yet a clean correctness win.
- Therefore the correct Phase 2 reading is split: the correctness rung passes for the heuristic arm, while the learned arm remains non-promoted until its replay discrepancy is reduced or otherwise justified.

## Post-run red-team note
- Strongest alternative explanation: the learned warm-start path may be preserving the same broad route while still perturbing the corrected transport object too much for a retained-teacher claim.
- Smallest discriminating follow-up check: inspect whether the learned arm's discrepancy is systematic across repeated seeds or mainly this single fixture/seed, and whether a tighter or better-targeted warm-start state improves replay parity.
- What would force a return to Phase 1: evidence that the route, output interpretation, or benchmark settings changed across arms. No such evidence appeared here.
