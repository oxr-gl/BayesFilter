# BayesFilter NeuTra c603 Integration Visible Gated Execution Runbook

Date: 2026-07-06

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use `codex
exec`, `overnight_gated_launch.sh`, `setsid`, `nohup`, detached `tmux`
supervisors, backgrounded phase runners, or copied-workspace execution.

## Program

Master program:

- `docs/plans/bayesfilter-neutra-c603-integration-master-program-2026-07-06.md`

Reviewed plan artifacts:

- `docs/reviews/bayesfilter-neutra-c603-integration-launch-review-bundle-2026-07-06.md`

Execution ledger:

- `docs/plans/bayesfilter-neutra-c603-integration-visible-execution-ledger-2026-07-06.md`

Stop handoff:

- `docs/plans/bayesfilter-neutra-c603-integration-visible-stop-handoff-2026-07-06.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Launch Contract Freeze | `docs/plans/bayesfilter-neutra-c603-integration-phase0-launch-contract-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-c603-integration-phase0-launch-contract-result-2026-07-06.md` |
| 1 | Legacy Adapter | `docs/plans/bayesfilter-neutra-c603-integration-phase1-legacy-adapter-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-c603-integration-phase1-legacy-adapter-result-2026-07-06.md` |
| 2 | c603 Fixture Tests | `docs/plans/bayesfilter-neutra-c603-integration-phase2-c603-fixture-tests-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-c603-integration-phase2-c603-fixture-tests-result-2026-07-06.md` |
| 3 | Fixed-Transport Mechanics | `docs/plans/bayesfilter-neutra-c603-integration-phase3-fixed-transport-mechanics-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-c603-integration-phase3-fixed-transport-mechanics-result-2026-07-06.md` |
| 4 | Generic Interface Design | `docs/plans/bayesfilter-neutra-c603-integration-phase4-generic-interface-subplan-2026-07-06.md` | `docs/plans/bayesfilter-neutra-c603-integration-phase4-generic-interface-result-2026-07-06.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter convert the validated c603 import into reviewed adapter/tests/mechanics/design artifacts without overclaiming? |
| Baseline/comparator | Manual c603 import validation plus existing dense-IAF loader and fixed-transport mechanics tests. |
| Primary pass criterion | Phase 1/2 code tests pass CPU-only, Phase 3 mechanics remains mechanics-only, and Phase 4 design separates engineering from scientific claims. |
| Veto diagnostics | Hash/signature mismatch, nonfinite tensors, unsupported legacy semantics, orientation mismatch, GPU/training/long-HMC requirement, or unsupported claims. |
| Explanatory diagnostics | Stable hashes, artifact signatures, finite smoke values, local runtime, review comments. |
| Not concluded | Posterior convergence, HMC readiness, production readiness, sampler superiority, default-policy change. |
| Artifacts | Master program, subplans/results, ledger, review records, focused logs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Start from c603 | dsge_hmc follow-up and BayesFilter import validation | c603 has bridgeable payload and validated forward/logdet tie-out | Treating import as posterior evidence | Nonclaims in every artifact | reviewed evidence |
| CPU-only checks | Project policy allows CPU for smoke/import checks | Avoids GPU approval and sandbox ambiguity | Mistaking CPU pass for production GPU readiness | Record CPU-only status | reviewed boundary |
| `s_max=1.0` only for legacy dense IAF | c603 artifact and manual validation | BayesFilter/dsge_hmc formulas match for c603 | Incorrect generalization to other `s_max` values | Adapter rejection test | design constraint |
| Mixing matrix transpose | dsge_hmc and BayesFilter forward semantics | Required for `z @ W.T` vs `values @ matrix` | Orientation mismatch | Legacy tie-out test | checked assumption |

## Skeptical Plan Audit

Before executing each phase, Codex must record a skeptical audit in chat and in
the ledger for material phases. Check wrong baselines, proxy metric promotion,
missing stop conditions, unfair comparisons, hidden assumptions, stale context,
environment mismatch, and commands whose artifacts would not answer the phase
question.

Launch audit status: `PASS_WITH_BOUNDARIES`. The program is allowed to continue
only as CPU-only engineering integration until a later reviewed plan and human
approval changes that boundary.

## Quiet Visible Execution Pattern

For TensorFlow, pytest, or Claude review commands, predeclare log paths under:

- `docs/plans/logs/bayesfilter-neutra-c603-integration-2026-07-06/`

Redirect full stdout/stderr to logs for noisy commands. Print only bounded
summaries, exit status, and artifact paths in chat.

## Visible State Machine

For each phase:

1. `PRECHECK`: read the subplan, confirm prerequisites, restate evidence
   contract, append ledger entry.
2. `EXECUTE_MINIMAL`: run the smallest visible commands needed.
3. `ASSESS_GATE`: compare outputs to primary criterion and veto diagnostics.
4. `PASS_REVIEW`: use Claude read-only review for material gates when
   available.
5. `REPAIR_LOOP`: patch fixable blockers, rerun focused checks, stop after five
   review rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the current phase gate passes.

## Claude Review Protocol

Use Claude only as a reviewer. Start with one exact path. If Claude is
unresponsive, run a tiny probe. If probe succeeds, narrow the prompt. If probe
fails, record a fresh Codex-agent review substitute.

Default prompt shape:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <path>. Do not edit,
run commands, launch agents, or review the whole repo. Question: <question>.
End with VERDICT: AGREE or VERDICT: REVISE.
```

## Human-Required Stop Conditions

Stop if continuing would require package installation, GPU/CUDA work, training,
long HMC sampling, destructive git/filesystem action, git commit/push, default
policy change, broad public/scientific claims, or modifying unrelated dirty
user work.

## Final Visible Handoff

When execution completes or stops, write final phase reached, status, result
artifacts, review trail, tests actually run, unresolved blockers, nonclaims,
and safest next human decision if any.
