# P8k Phase 5 Subplan: Generic GPU Profiling Ladder

metadata_date: 2026-06-17
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 5

## Phase Objective

Measure the generic configurable path on trusted GPU with cheap-to-expensive
rungs and decide whether further implementation work is justified.

## Entry Conditions Inherited From Previous Phase

- Phases 2 through 4 local checks passed.
- No GPU command is run outside trusted/escalated context.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-gpu-profiling-ladder-result-2026-06-17.md`
- JSON/markdown profile artifacts for each executed rung.

## Required Checks/Tests/Reviews

Trusted GPU preflight.  This command must be launched in trusted/escalated
context:

```bash
nvidia-smi
```

Cheap actual-SIR history-mode ladder first.  Both TensorFlow benchmark commands
must be launched in trusted/escalated context:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --history-mode full --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-actual-sir-n10000-full-history-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-actual-sir-n10000-full-history-2026-06-18.md
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --history-mode value-only --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-actual-sir-n10000-value-only-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-actual-sir-n10000-value-only-2026-06-18.md
```

Only if both cheap rungs are finite, GPU-backed, metadata-complete, and the
value-only rung shows a real engineering reason to continue, run reviewed
adjacent configuration rungs.  `N=50000` may be used only as a high-cost
confirmation rung after cheaper evidence justifies it.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which generic knobs materially affect runtime or memory on trusted GPU? |
| Baseline/comparator | Phase 4-corrected actual-SIR benchmark harness under matched `N=10000`, five-seed, TF32/GPU settings.  P8j `N=10000` and `N=50000` artifacts are reference stress evidence only, not promotion baselines or particle-adequacy evidence.  LGSSM is not a Phase 5 comparator unless a reviewed LGSSM rung is explicitly added. |
| Primary criterion | Each executed rung writes finite trusted-GPU artifacts with exact configuration; matched full-history and value-only rungs have equal log likelihoods; and the result identifies only engineering speed/memory candidates. |
| Veto diagnostics | CPU fallback, OOM, nonfinite output, missing configuration metadata, over-budget projection, or scientific adequacy claim. |
| Explanatory diagnostics | Runtime, compile time, GPU memory, ESS if requested, log likelihood, speed ratio, chunk policy. |
| Not concluded | Particle-count adequacy, leaderboard completion, HMC readiness, production default. |

The harness fields `speedup_vs_scalar_comparator_mean_warm_call` and
`primary_pass_5x_runtime_gate` are explanatory legacy fields only.  They are
not Phase 5 promotion criteria and do not establish particle adequacy,
leaderboard readiness, or production/default readiness.

## Forbidden Claims/Actions

- Do not run `N=50000` sweeps before cheaper rungs justify them.
- Do not change pass/fail criteria after seeing timings.
- Do not treat speedup as accuracy or adequacy.
- Do not treat the harness's built-in 5x runtime gate as a Phase 5 pass
  criterion.

## Exact Next-Phase Handoff Conditions

Phase 6 may proceed only if Phase 5 identifies a remaining bottleneck that is
generic enough to justify a design/implementation phase.  The Phase 5 result
must record whether full-history and value-only matched log likelihoods were
equal and whether value-only produced a material engineering benefit.

## Stop Conditions

Stop if GPU access is unavailable in trusted context, if a cheap rung is
nonfinite or falls back to CPU, if matched full-history and value-only log
likelihoods differ, if value-only does not provide an engineering reason to
continue, or if projected runtime exceeds the reviewed budget.  Do not proceed
to `N=50000` until the cheap history-mode comparison justifies that cost.
