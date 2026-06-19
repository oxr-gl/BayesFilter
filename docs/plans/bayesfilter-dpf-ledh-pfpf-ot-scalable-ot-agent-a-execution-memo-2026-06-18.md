# Agent A Execution Memo: Reduced-Rank Nystrom Ladder

Date: 2026-06-18
Timestamp: 2026-06-18T16:52:46+08:00

## Assignment

Agent A should execute only the reduced-rank Nystrom ladder implementation and
primary diagnostics.

This thread will keep Agent B's independent test/review plan local.  Agent A
must not begin Agent B work, create Agent B review artifacts, or modify Agent
B-owned files.

## Start Here

Read, in order:

1. `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-a-reduced-rank-nystrom-ladder-plan-2026-06-18.md`
2. `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-agent-plans-claude-review-convergence-2026-06-18.md`
3. `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-reboot-reset-memo-2026-06-18.md`

The Agent A plan has already passed Claude review:

`AGENT_A_B_REDUCED_RANK_NYSTROM_PLANS_CLAUDE_REVIEW_CONVERGED`

## Required Boundaries

- Do not change BayesFilter defaults.
- Do not create public API surface.
- Do not run GPU, network, package-install, POT, or external-backend actions.
- Do not edit Agent B-owned independent test/review artifacts.
- Preserve unrelated dirty worktree files, especially HMC/linear/test changes
  outside this scalable OT Nystrom scope.
- Runtime and memory fields are explanatory only until validity gates pass.
- No speedup, ranking, posterior-correctness, HMC-readiness, or production
  readiness claim is allowed.

## Critical Schema Requirements

- Phase 11 JSON must be a manifest containing one Phase 3-valid
  `candidate_record` per fixture/rank record plus a summary section.
- Every nested `candidate_record.baseline_comparator` must begin with
  `phase1_dense_streaming`.
- Every fixture/rank record must emit dense-reference max and RMS
  transported-particle error fields, including `high_dim_locality`.
- The `ledh_specific_smoke` fixture construction must be deterministic, pinned
  in the diagnostic script, and summarized in the result artifact.

## Expected Agent A Artifacts

- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
- `tests/test_nystrom_transport_tf.py`
- `docs/benchmarks/scalable_ot_p11_reduced_rank_nystrom_ladder_diagnostics.py`
- `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.json`
- `docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-reduced-rank-nystrom-ladder-result-2026-06-18.md`

Update the scalable OT ledger and stop handoff only if the Agent A plan's
conditions for doing so are met.

## Completion Handoff Back To This Thread

When Agent A finishes, report:

- final status;
- exact commands run;
- implementation diff summary;
- diagnostic JSON/Markdown paths;
- result-note path;
- hard veto list;
- viable reduced-rank list;
- unresolved uncertainties and non-claims;
- whether Agent B can begin independent review.

Allowed final statuses are only:

- `PHASE_11_REDUCED_RANK_NYSTROM_LADDER_PASSED_DIAGNOSTIC_ONLY`
- `PHASE_11_REDUCED_RANK_NYSTROM_LADDER_COMPLETED_CANDIDATE_NOT_PROMOTED`
- `PHASE_11_REDUCED_RANK_NYSTROM_LADDER_BLOCKED`

