# P91 Phase 6 Subplan: CPU/GPU/Batched Performance Benchmark

Date: 2026-06-29

Status: `REFRESHED_PENDING_PHASE5_RESULT_REVIEW`

## Phase Objective

Benchmark Zhao-Cui value/score performance by model and execution target:
CPU single, CPU batched, GPU/XLA single, and GPU/XLA batched. The goal is to
detect serious performance pathologies and produce model-specific target
recommendations, not to assert universal GPU superiority.

## Entry Conditions Inherited From Previous Phase

- Phase 5 GPU/XLA JIT capability reviewed pass.
- Phase 2 batched API reviewed pass.
- This Phase 6 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- Benchmark manifest/results:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-2026-06-29.json`
- CPU manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-cpu-2026-06-29.json`
- GPU manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-gpu-2026-06-29.json`
- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-result-2026-06-29.md`
- Refreshed Phase 7 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase7-hmc-smoke-subplan-2026-06-29.md`
- Benchmark harness:
  `scripts/p91_performance_benchmark.py`

## Required Checks/Tests/Reviews

CPU benchmark commands must hide GPU before TensorFlow import. GPU benchmark
commands require escalated/trusted permissions. Claude review is required for
this refreshed subplan, Phase 6 result, and Phase 7 subplan.

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

Finalization command:

```bash
python scripts/p91_performance_benchmark.py --merge docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-cpu-2026-06-29.json docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-gpu-2026-06-29.json --manifest docs/plans/bayesfilter-highdim-zhao-cui-p91-phase6-performance-benchmark-2026-06-29.json
```

`--target gpu --xla true` is the only trusted GPU benchmark mode authorized by
this subplan. The harness must record actual XLA status, first-call
compile/warmup timing, steady timing, fixed input signatures or equivalent
shape/dtype stability, trace counts when available, explicit post-warmup
retrace status such as `post_warmup_retrace_detected`, retry count, OOM
status, trusted/escalated context, device details, exact command, git commit,
Python environment, CPU/GPU visibility, artifact paths, and pass/veto flags.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are CPU/GPU single/batched Zhao-Cui performance profiles acceptable and model-specific recommendations evidence-backed? |
| Baseline/comparator | CPU single route and looped/batched parity from Phase 2. |
| Primary criterion | CPU and trusted GPU/XLA single/batched timings complete with finite outputs, no OOM, no retracing after warmup, explicit compile/warmup versus steady timing, and no closed-rule pathology in any evaluated target/model cell. |
| Veto diagnostics | Universal GPU-speed claim, untrusted GPU evidence, missing XLA status for GPU, missing compile/steady separation, hidden OOM/retry, closed-rule pathology, or benchmark treated as scientific validity. |
| Explanatory diagnostics | Timing table, memory table, batch scaling, model-specific target notes. |
| Not concluded | No score identity proof, exact likelihood correctness, HMC posterior validity, packaging/default readiness, or universal speed claim. |
| Artifact | Benchmark JSON/MD, Phase 6 result, refreshed Phase 7 subplan. |

Closed-rule pathology vetoes:

- any benchmark cell has nonfinite output value or score;
- any benchmark cell records OOM or retry count greater than zero;
- any compiled cell records post-warmup retracing;
- any single/batched route missing steady timing;
- any batched route has steady per-item time more than `10x` its corresponding
  looped-single per-item steady time on the same target;
- GPU command does not record `actual_xla_status == true`;
- trusted GPU command does not record GPU output devices for benchmark outputs.

## Forbidden Claims/Actions

- Do not claim GPU is always faster.
- Do not use benchmark speed as score/scientific validity.
- Do not use one deterministic fixture benchmark as a universal performance
  result for all Zhao-Cui models.
- Do not run package/release/CI/default commands.
- Do not change defaults based solely on benchmark without final decision.

## Exact Next-Phase Handoff Conditions

Phase 7 may start only if:

- Phase 6 result receives Claude `VERDICT: AGREE`;
- Phase 7 subplan receives Claude `VERDICT: AGREE`;
- performance pathologies are absent or Phase 7 is blocker-only.

## Stop Conditions

- GPU/CPU benchmark evidence is untrusted or incomplete.
- Serious performance pathology requires product-direction decision.
- Local checks fail and cannot be repaired.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run required benchmark commands authorized by reviewed Phase 6 refresh.
2. Run the exact finalization command to merge CPU/GPU manifests into the named
   final benchmark JSON.
3. Write Phase 6 result / close record.
4. Draft or refresh Phase 7 subplan.
5. Review Phase 6 result and Phase 7 subplan.
