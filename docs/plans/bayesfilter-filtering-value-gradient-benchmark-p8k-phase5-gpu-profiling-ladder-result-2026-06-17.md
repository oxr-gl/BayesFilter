# P8k Phase 5 Result: Generic GPU Profiling Ladder

metadata_date: 2026-06-18
status: STOP_AFTER_PHASE5_NO_EXPENSIVE_RUNG
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 5
executor: Codex
reviewer: Claude Opus max effort, read-only

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | The matched trusted-GPU `N=10000` actual-SIR full-history and value-only rungs both passed the finite/GPU/metadata/log-likelihood gate, but value-only did not produce a material runtime or memory benefit.  The Phase 5 stop condition is therefore engaged: do not run `N=50000`, and do not launch Phase 6 under the current entry conditions. |
| Primary criterion status | Passed for the executed cheap rungs.  Both artifacts are trusted-GPU outputs, finite, metadata-complete, and have identical log likelihoods. |
| Veto diagnostic status | No correctness veto for the executed rungs.  Continuation is vetoed by the predeclared stop condition because value-only gives no engineering reason to continue. |
| Main uncertainty | The result only profiles the history-mode knob under matched actual-SIR `N=10000`; it does not profile other generic fast-path candidates. |
| Next justified action | Stop this runbook lane with a visible handoff.  A future Phase 6 launch would need a revised, reviewed entry condition with independent bottleneck evidence. |
| What is not concluded | No particle-count adequacy, leaderboard completion, exact likelihood correctness, DPF gradient correctness, HMC/NUTS readiness, production/default readiness, or Zhao-Cui TT/SIRT parity. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which generic history-mode knob behavior materially affects trusted-GPU runtime or memory on the actual-SIR stress case? |
| Baseline/comparator | Phase 4-corrected actual-SIR benchmark harness under matched `N=10000`, five-seed, TF32/GPU settings. |
| Primary criterion | Executed rungs write finite trusted-GPU artifacts with exact configuration; matched full-history and value-only rungs have equal log likelihoods; the result identifies only engineering speed/memory candidates. |
| Veto diagnostics | CPU fallback, OOM, nonfinite output, missing configuration metadata, mismatched log likelihoods, legacy 5x speed field promoted to a Phase 5 criterion, or unreviewed `N=50000` escalation. |
| Explanatory diagnostics | Runtime, compile time, GPU memory, ESS if requested, log likelihood, speed ratio, chunk policy. |
| Not concluded | Particle-count adequacy, leaderboard completion, HMC readiness, exact nonlinear likelihood correctness, DPF gradient correctness, production/default readiness. |

## Trusted GPU Preflight

Command run in trusted/escalated context:

```bash
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
```

Observed device:

- NVIDIA GeForce RTX 4080 SUPER, 16376 MiB, driver 591.86.

## Commands Run

Full-history rung, trusted/escalated context:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --history-mode full --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-actual-sir-n10000-full-history-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-actual-sir-n10000-full-history-2026-06-18.md
```

Value-only rung, trusted/escalated context:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --history-mode value-only --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-actual-sir-n10000-value-only-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-actual-sir-n10000-value-only-2026-06-18.md
```

## Artifacts

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-actual-sir-n10000-full-history-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-actual-sir-n10000-full-history-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-actual-sir-n10000-value-only-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-actual-sir-n10000-value-only-2026-06-18.md`

## Result Comparison

| Diagnostic | Full History | Value Only | Gate Interpretation |
| --- | ---: | ---: | --- |
| finite output | true | true | passed |
| output device | `/device:GPU:0` | `/device:GPU:0` | passed |
| `history_mode` | `full` | `value-only` | expected difference |
| `return_history` | true | false | expected difference |
| ESS summary available | true | false | expected difference |
| log likelihoods equal | yes | yes | passed |
| compile + first call seconds | 19.849983 | 20.708217 | explanatory |
| warm call mean seconds | 6.898784 | 7.100296 | no value-only speed benefit |
| value/full warm ratio | N/A | 1.029210 | value-only was about 2.9 percent slower |
| peak GPU memory counter bytes | 210641920 | 210641920 | no memory benefit in this counter |

Log likelihood vector for both rungs:

```text
[-902.4534301757812, -902.7452392578125, -903.4571533203125, -903.2506713867188, -902.4193115234375]
```

Full-history ESS minima by seed:

```text
[6441.296875, 6432.78173828125, 6482.1669921875, 6511.61083984375, 6437.65673828125]
```

The ESS values are explanatory only.  They are not a Phase 5 promotion
criterion and do not establish particle-count adequacy.

## Gate Assessment

The cheap history-mode comparison answered the Phase 5 question for this knob:
value-only preserves the log likelihood but does not improve warm runtime or
the reported TensorFlow peak memory counter at `N=10000`.

The Phase 5 subplan says to stop before `N=50000` if the value-only rung does
not provide a real engineering reason to continue.  That stop condition is now
active.  The `N=50000` high-cost confirmation rung was not run.

The Phase 6 subplan entry condition also requires Phase 5 to identify a
generic bottleneck that the linear-observation or transition-cache design could
address.  This Phase 5 result does not provide that evidence.  Phase 6 is not
launched under the current runbook.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit recorded by artifacts | `b1f400d5cb7e88d6b10072a23344f1286542f492` |
| Host | `DESKTOP-RF1Q5IJ` |
| TensorFlow version | `2.19.1` |
| Python version | `3.11.14` |
| Device | `/GPU:0` |
| GPU status | Trusted/escalated GPU context; RTX 4080 SUPER visible |
| Shape | `B=5`, `T=20`, `D=18`, `M=9`, `N=10000` |
| Seeds | `81120,81121,81122,81123,81124` |
| dtype / TF32 | `float32`, TF32 enabled |
| Transport | active-all, Sinkhorn iterations 10, epsilon 1.0, row/col chunks 2048, particle chunk 1024 |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-gpu-profiling-ladder-subplan-2026-06-17.md` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-gpu-profiling-ladder-result-2026-06-17.md` |

## Boundary

The harness fields `speedup_vs_scalar_comparator_mean_warm_call` and
`primary_pass_5x_runtime_gate` remain explanatory legacy fields only.  They are
not used as Phase 5 pass criteria.

No default policy is changed.  Value-only mode remains an explicit
configuration path, not a production/default recommendation.

## Post-Run Red Team

Strongest alternative explanation:

- The overhead of history diagnostics is small relative to transport, so this
  knob can be semantically useful without being a runtime optimization.

What would overturn the continuation stop:

- A reviewed, cheaper profile showing history materialization dominates at a
  larger horizon, larger state dimension, or different downstream workload
  where value-only materially reduces runtime or memory while preserving
  values.

Weakest part of the evidence:

- TensorFlow memory counters may not capture all allocator behavior, and a
  single warm repeat is noisy.  However, the predeclared gate required a real
  engineering reason before high-cost escalation; the observed direction is not
  favorable.

## Handoff

Stop this P8k runbook lane here.  Do not run `N=50000` under this Phase 5
subplan, and do not launch Phase 6 without a revised, reviewed entry condition
or new independent bottleneck evidence.
