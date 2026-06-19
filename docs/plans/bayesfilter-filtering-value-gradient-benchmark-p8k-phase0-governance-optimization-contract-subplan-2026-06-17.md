# P8k Phase 0 Subplan: Governance And Optimization Contract

metadata_date: 2026-06-17
status: DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 0

## Phase Objective

Lock the lane boundary for generic batched TF32/GPU DPF optimization and
preserve the current P8j evidence as motivation only.

## Entry Conditions Inherited From Previous Phase

- P8j actual-SIR d18 `N=10000` and `N=50000` runs are available as feasibility
  evidence.
- Current experimental streaming core already exposes chunk sizes, transport
  policy inputs through harnesses, TF32 mode, and `return_history`.
- The user requested generic/configurable improvements rather than SIR-specific
  shortcuts.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase0-governance-optimization-contract-result-2026-06-17.md`
- P8k visible execution ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-execution-ledger-2026-06-17.md`
- P8k Claude review ledger:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-claude-review-ledger-2026-06-17.md`
- P8k stop handoff:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-visible-stop-handoff-2026-06-17.md`

## Required Checks/Tests/Reviews

```bash
rg -n "P8k|generic|configurable|not concluded|N=10000|N=50000|all-pairs OT|trusted" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-*
rg -n "return_history|skip_transport_when_no_active|transport_plan_mode|row_chunk_size|col_chunk_size|particle_chunk_size|sinkhorn_iterations|transport-policy" experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-*
```

Claude read-only review of the P8k planning packet is required before Phase 0
is closed.  If Claude review must be split into smaller chunks, Phase 0 may
close only after the master/runbook chunk and the Phase 0/Phase 1 subplan chunk
both return `VERDICT: AGREE`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is P8k correctly scoped as generic/configurable batched DPF optimization? |
| Baseline/comparator | Current P8j actual-SIR and LGSSM streaming benchmark artifacts. |
| Primary criterion | Local text checks and Claude review agree that P8k preserves boundaries and does not claim particle adequacy. |
| Veto diagnostics | SIR-specific implementation target, changed default policy, missing GPU trust rule, or runtime proxy promoted to scientific adequacy. |
| Explanatory diagnostics | Code-surface search hits showing existing knobs and unused optimization hooks. |
| Not concluded | No implementation success, no runtime improvement, no particle adequacy, no leaderboard completion. |

## Forbidden Claims/Actions

- Do not edit implementation code in Phase 0.
- Do not launch GPU benchmarks in Phase 0.
- Do not claim any runtime improvement from this planning phase.
- Do not stage, commit, merge, or push.

## Exact Next-Phase Handoff Conditions

Phase 1 may proceed only if Phase 0 result records:

- P8k scope is generic and configurable;
- P8j actual-SIR evidence is motivation only;
- all GPU commands remain trusted/escalated;
- Claude review converged on both the master/runbook chunk and the
  Phase 0/Phase 1 subplan chunk, or a blocker is written.

## Stop Conditions

Stop if the local artifacts contradict the P8j runtime evidence, if the
optimization scope cannot be separated from SIR-specific implementation, or if
Claude review does not converge within five rounds.

## Skeptical Plan Audit

The main risk is treating high-particle runtime as a scientific metric.  Phase
0 explicitly blocks that promotion and keeps Phase 5 profiling explanatory
unless paired with later particle-adequacy evidence outside P8k.
