# P8m Master Program: Generic Transport-Core Optimization

metadata_date: 2026-06-18
status: DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW
executor: Codex
reviewer: Claude Opus max effort, read-only

## Scope

P8m is the generic optimization lane for the TensorFlow batched DPF
transport core used by the experimental LEDH-PFPF-OT streaming engine.

The P8l profile found that active OT/Sinkhorn transport explains most of the
trusted-GPU warm-call time for the actual-SIR d18 stress harness.  P8m must
turn that evidence into generic transport-core instrumentation, profiling, and
safe optimization candidates.

SIR d18 is only a stress fixture.  P8m must not hard-code SIR state layout,
observation structure, seed lists, or disease dynamics into the transport
engine.

## Out Of Scope

- SIR-specific shortcuts or disease-model-specialized transport code.
- Zhao-Cui fixed-branch TT/SIRT source-faithfulness or monograph work.
- Declaring any SIR d18 particle count adequate.
- Leaderboard completion.
- HMC/NUTS readiness.
- Exact nonlinear likelihood, score, Hessian, or scientific validity claims.
- Changing BayesFilter default numerical policy without a reviewed result.
- Promoting fewer Sinkhorn iterations or changed epsilon as scientifically
  acceptable without a separate validation contract.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the batched TensorFlow DPF transport core be made faster or more configurable through generic exact implementation work, while keeping algorithmic and scientific claim boundaries explicit? |
| Baseline/comparator | Current streaming entropic OT route used by `batched_annealed_transport_core_tf` / `_filterflow_streaming_transport`, with P8l active-all `N=10000`, Sinkhorn-10 trusted-GPU artifacts as stress evidence only. |
| Primary pass criterion | Every phase either passes its declared local checks and writes a result artifact, or writes a blocker.  Final P8m pass requires generic transport instrumentation/profiling artifacts and, if implementation occurs, focused tests showing no value regression under matched exact settings. |
| Veto diagnostics | SIR-specific optimization hidden in generic code; runtime proxy promoted to particle adequacy; untrusted GPU result; changed default policy; lower Sinkhorn iteration or epsilon promoted without validation; missing artifact for a material claim; Claude used as execution authority. |
| Explanatory diagnostics | Runtime, compile time, memory counters, finite values, log-likelihood sensitivity, chunk sizes, Sinkhorn iterations, epsilon, transport mode, row/column residual diagnostics if available. |
| Not concluded | Particle-count adequacy, MC-SE adequacy, leaderboard readiness, exact nonlinear likelihood correctness, DPF gradient correctness, HMC/NUTS readiness, production/default readiness, or Zhao-Cui TT/SIRT source-faithfulness. |

## Skeptical Plan Audit

This lane can mislead us if:

1. a SIR stress-case result is treated as a SIR-specific implementation target;
2. a timing improvement changes numerical behavior but is described as exact
   optimization;
3. lower Sinkhorn iterations are promoted as a default from runtime alone;
4. whole-call timing is mistaken for kernel-level attribution;
5. GPU command results are interpreted without trusted execution context.

Controls:

- every phase states whether it is exact implementation, tuning validation, or
  extension;
- SIR d18 remains a stress fixture only;
- exact implementation changes require matched-value checks;
- lower-iteration/epsilon changes require a separate validation phase;
- all GPU/CUDA/TensorFlow GPU commands run in trusted/escalated context.

Audit status: `PASS_FOR_PLANNING_REVIEW`.

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance and generic boundary contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase0-governance-boundary-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase0-governance-boundary-result-2026-06-18.md` |
| 1 | Transport instrumentation design | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase1-instrumentation-design-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase1-instrumentation-design-result-2026-06-18.md` |
| 2 | Generic microbenchmark implementation | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-microbenchmark-implementation-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase2-microbenchmark-implementation-result-2026-06-18.md` |
| 3 | Trusted GPU chunk ladder | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-gpu-chunk-ladder-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase3-gpu-chunk-ladder-result-2026-06-18.md` |
| 4 | Exact implementation optimization decision | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase4-exact-optimization-decision-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase4-exact-optimization-decision-result-2026-06-18.md` |
| 5 | Exact implementation repair, if justified | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase5-exact-implementation-repair-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase5-exact-implementation-repair-result-2026-06-18.md` |
| 6 | Sinkhorn/epsilon validation contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase6-sinkhorn-validation-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase6-sinkhorn-validation-result-2026-06-18.md` |
| 7 | Administrative boundary closeout | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase7-cross-fixture-closeout-subplan-2026-06-18.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8m-phase7-administrative-boundary-closeout-result-2026-06-18.md` |

## Required Phase Protocol

For every phase:

1. read the phase subplan before execution;
2. state the evidence contract and skeptical audit;
3. run only required checks or reviewed commands;
4. write the phase result or blocker record;
5. draft or refresh the next subplan if needed;
6. review the next material subplan/result/diff with Claude until convergence
   or five rounds for the same blocker.

## Review And Repair Protocol

Claude is a read-only reviewer only.  Claude may inspect local repo paths and
return findings, but cannot edit files, run experiments, authorize GPU usage,
change pass criteria, cross funding/product/model-file boundaries, or make
scientific claims authoritative.

If Claude finds a fixable issue, Codex patches the same artifact visibly,
reruns focused local checks, and repeats bounded review.  If review does not
converge after five rounds for the same blocker, Codex writes a blocker result
and stops for human direction.

Use small review prompts.  If Claude does not respond, run a small probe.  If
the probe responds, redesign the review prompt into smaller chunks.

## Global Stop Conditions

- The plan would require package installation, network fetch, credentials, or
  destructive git/filesystem operations.
- A GPU/CUDA/TensorFlow GPU command would run without trusted/escalated context.
- A change would mutate unrelated Zhao-Cui, monograph, or user work.
- A result would require changing pass/fail criteria after seeing outcomes.
- A benchmark would exceed the reviewed runtime budget.
- Claude and Codex fail to converge after five review rounds for the same
  blocker.
- A phase would make a particle-adequacy, leaderboard, HMC, exact-likelihood,
  production-default, or SIR-specific generality claim not authorized by the
  evidence contract.
