# P8k Phase 7 Subplan: Closeout And Next-Lane Boundary

metadata_date: 2026-06-17
status: DRAFT
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-generic-batched-dpf-optimization-master-program-2026-06-17.md
phase: 7

## Phase Objective

Close the generic optimization lane with a clear artifact index, result
summary, unresolved gaps, and boundary to the later particle-adequacy or
leaderboard lane.

## Entry Conditions Inherited From Previous Phase

- All prior phases either passed or wrote blockers.
- No unresolved implementation diff lacks local checks.

## Required Artifacts

- Phase 7 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-phase7-closeout-boundary-result-2026-06-17.md`
- Optional artifact index:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-artifact-index-2026-06-17.json`
- Updated stop handoff.

## Required Checks/Tests/Reviews

```bash
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8k-* experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py
git status --short
```

Claude read-only review is required for the final closeout.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What did P8k actually improve, what remains experimental, and what is the safest next lane? |
| Baseline/comparator | P8k phase results and P8j feasibility artifacts. |
| Primary criterion | Closeout lists changed files, checks run, result artifacts, unresolved blockers, and nonclaims. |
| Veto diagnostics | Missing artifact, unsupported speed/adequacy claim, unreviewed material diff, or dirty-worktree confusion. |
| Explanatory diagnostics | Git status, artifact index, final benchmark summary. |
| Not concluded | Particle adequacy, leaderboard completion, HMC/NUTS readiness, production default. |

## Forbidden Claims/Actions

- Do not commit or push unless the user separately asks.
- Do not call the experimental path a production default.
- Do not use P8k speed evidence as SIR particle adequacy.

## Exact Next-Phase Handoff Conditions

There is no next P8k phase.  The closeout may recommend a separate
particle-tuning or leaderboard lane if evidence supports it.

## Stop Conditions

Stop if final review does not converge, if artifacts are missing, or if the
worktree contains unrelated changes that make a clean boundary impossible.
