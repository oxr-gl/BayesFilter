# P8k Master Program: Generic Batched TF32/GPU DPF Optimization

metadata_date: 2026-06-18
status: STOPPED_AFTER_PHASE5_NO_ENGINEERING_REASON_FOR_HIGH_COST_RUNG
executor: Codex
reviewer: Claude Opus max effort, read-only

## Scope

P8k is the generic optimization lane for the experimental batched
TF32/GPU LEDH-PFPF-OT streaming engine.

The immediate motivation is the P8j actual-SIR d18 evidence:

- `N=10000`, `B=5`, `T=20` is finite and practical;
- `N=50000`, `B=5`, `T=20` is finite but expensive;
- all-pairs OT scaling is the dominant cost at high particle counts.

P8k must keep the improvements generic and configurable.  Actual-SIR d18 is a
stress case and downstream benchmark, not the source of model-specific hacks.

## Out Of Scope

- Zhao-Cui fixed-branch TT/SIRT source-faithfulness or monograph work.
- Declaring a SIR d18 particle count adequate.
- Leaderboard completion.
- HMC/NUTS readiness.
- Exact likelihood, score, Hessian, or scientific validity claims.
- Changing default BayesFilter numerical policy without a reviewed result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the batched TF32/GPU DPF engine expose generic opt-in controls and fast paths that reduce runtime or memory pressure without changing scientific claim boundaries? |
| Baseline/comparator | Current P8j experimental streaming adapter and LGSSM streaming benchmark with `active-all`, `sinkhorn_iterations=10`, TF32 enabled, and current chunk controls.  The P8j `N=10000` and `N=50000` actual-SIR artifacts are reference evidence, not promotion baselines. |
| Primary pass criterion | Each phase either passes its declared local checks and writes a result artifact, or writes a blocker that preserves exact boundary state.  Final P8k pass requires generic opt-in configuration and benchmark artifacts, plus no regression in focused CPU tests. |
| Veto diagnostics | SIR-specific optimization hidden in the engine; runtime proxy treated as particle adequacy; GPU result outside trusted context; changed defaults without evidence; missing artifact for a material claim; Phase 5/6 benchmarks run before local correctness checks; Claude used as execution authority. |
| Explanatory diagnostics | Runtime, compile time, GPU memory info, ESS when requested, log likelihood finiteness, chunk-size scaling, Sinkhorn iteration scaling, transport policy scaling, and XLA compile behavior. |
| Not concluded | Particle-count adequacy, MC-SE adequacy, leaderboard readiness, exact nonlinear likelihood correctness, DPF gradient correctness, HMC/NUTS readiness, production/default readiness, or Zhao-Cui TT/SIRT source-faithfulness. |

## Skeptical Plan Audit

This lane could mislead us in four ways:

1. runtime wins could be confused with statistical adequacy;
2. SIR-specific shortcuts could be mislabeled as generic engine work;
3. cheap benchmark fixtures could be promoted over actual downstream behavior;
4. GPU failures or successes could be misread if not run in trusted context.

The program therefore requires opt-in configuration, focused CPU correctness
tests before GPU profiling, explicit nonclaims in every result, and trusted
GPU context for all CUDA/TensorFlow GPU commands.

Audit status: `PASS_FOR_PLANNING_REVIEW`.  The phase order starts with the
configuration contract and local checks before spending GPU time.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and optimization contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase0-governance-optimization-contract-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase0-governance-optimization-contract-result-2026-06-17.md` |
| 1 | Generic configuration surface contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase1-config-surface-contract-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase1-config-surface-contract-result-2026-06-17.md` |
| 2 | Benchmark harness plumbing | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-benchmark-harness-plumbing-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase2-benchmark-harness-plumbing-result-2026-06-17.md` |
| 3 | Value-only diagnostics fast path | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-value-only-diagnostics-fastpath-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase3-value-only-diagnostics-fastpath-result-2026-06-17.md` |
| 4 | Inactive-transport skip path | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase4-inactive-transport-skip-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase4-inactive-transport-skip-result-2026-06-17.md` |
| 5 | Generic GPU profiling ladder | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-gpu-profiling-ladder-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase5-gpu-profiling-ladder-result-2026-06-17.md` |
| 6 | Generic linear-observation and transition-cache design | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase6-linear-observation-transition-cache-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase6-linear-observation-transition-cache-result-2026-06-17.md` |
| 7 | Closeout and next-lane boundary | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase7-closeout-boundary-subplan-2026-06-17.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase7-closeout-boundary-result-2026-06-17.md` |

## Required Phase Protocol

For every phase:

1. read the phase subplan before execution;
2. state the evidence contract and skeptical audit;
3. run only required local checks or reviewed commands;
4. write the phase result or blocker record;
5. draft or refresh the next subplan;
6. review the next material subplan or result with Claude until convergence or
   five rounds for the same blocker.

## Review And Repair Protocol

Claude is a read-only reviewer only.  Claude may inspect local repo paths and
return findings, but cannot edit files, run experiments, authorize GPU usage,
change pass criteria, cross funding/product/model-file boundaries, or make
scientific claims authoritative.

If Claude finds a fixable issue, Codex patches the same artifact visibly,
reruns focused local checks, and repeats bounded review.  If review does not
converge after five rounds for the same blocker, Codex writes a blocker result
and stops for human direction.

## Global Stop Conditions

- The plan would require package installation, network fetch, credentials, or
  destructive git/filesystem operations.
- A GPU/CUDA command would run without trusted/escalated context.
- A change would mutate unrelated Zhao-Cui, monograph, or user work.
- A result would require changing pass/fail criteria after seeing outcomes.
- A benchmark would exceed the reviewed runtime budget.
- Claude and Codex fail to converge after five review rounds.
- A phase would make a particle-adequacy, leaderboard, HMC, exact-likelihood,
  or production-default claim not authorized by the evidence contract.
