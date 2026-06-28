# BayesFilter DPF LEDH-PFPF-OT Default Impact Test Visible Gated Execution Runbook

Date: 2026-06-20

## Status

`COMPLETED_P06_OPERATIONAL_VIABILITY_SUPPORTED_WITH_NONCLAIMS`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only.  Claude must not edit files, run
experiments, launch agents, authorize phase crossing, or change state.

This runbook is visible foreground execution in the current conversation.  It
must not launch a detached or nested agent.  Do not use `codex exec`,
`overnight_gated_launch.sh`, `setsid`, `nohup`, detached `tmux`, backgrounded
phase runners, or copied-workspace execution.

## Quiet Visible Execution Pattern

Commands expected to produce large TensorFlow/CUDA/Claude output should write
structured JSON/Markdown artifacts directly and keep chat output bounded.  If a
command fails, inspect at most bounded failure output and preserve the artifact
or result note.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-master-program-2026-06-20.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-claude-review-ledger-2026-06-20.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-execution-ledger-2026-06-20.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-visible-stop-handoff-2026-06-20.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance, runbook, and review lock | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p00-governance-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p00-governance-result-2026-06-20.md` |
| P01 | Small deterministic correctness gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p01-correctness-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p01-correctness-result-2026-06-20.md` |
| P02 | Trusted GPU precision drift screen | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p02-precision-gpu-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p02-precision-gpu-result-2026-06-20.md` |
| P03 | Target-shape trusted GPU smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p03-target-gpu-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p03-target-gpu-result-2026-06-20.md` |
| P04 | Performance and memory interpretation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p04-performance-memory-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p04-performance-memory-result-2026-06-20.md` |
| P05 | Tiny HMC mechanics smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p05-hmc-mechanics-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p05-hmc-mechanics-result-2026-06-20.md` |
| P06 | Final synthesis and handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-p06-closeout-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-impact-test-result-2026-06-20.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the promoted GPU TF32 LEDH-PFPF-OT default help the LEDH filter engineering route enough to remain viable for follow-on validation? |
| Baseline/comparator | FP64/reference arms, FP32-no-TF32 arms, previous/default smoke artifacts, and phase-local previous rungs. |
| Primary pass criterion | All executed phase hard screens pass and each phase writes result, next subplan, and review record without overclaiming. |
| Veto diagnostics | Nonfinite outputs, trusted GPU placement mismatch, missing artifacts, stale metadata, failed correctness gate, or unsupported scientific/default-policy claim. |
| Explanatory diagnostics | Runtime, memory, drift magnitudes, compile time, warm-call timing, HMC acceptance/log-accept values. |
| Not concluded | Posterior correctness, HMC readiness, convergence, statistical superiority, dense Sinkhorn equivalence, public API readiness, or low-rank lane rejection. |
| Artifacts | Phase subplans/results, benchmark JSON/MD artifacts, execution ledger, Claude review ledger, stop handoff. |

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands needed to answer the phase.
3. `ASSESS_GATE`: compare outputs against hard screens and write result.
4. `PASS_REVIEW`: use Claude as read-only reviewer for material subplans or
   material phase results.
5. `REPAIR_LOOP`: patch fixable blockers visibly, rerun focused checks, and
   retry read-only review, stopping after five rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after gate pass and reviewed next subplan.

## Human-Required Stop Conditions

Stop if continuing would cross or require human, runtime, model-file, funding,
product-capability, default-policy, or scientific-claim authority not already
granted in this program.  Also stop for package installation, network fetch,
credentials, destructive git/filesystem action, modifying unrelated dirty work,
changing criteria after seeing results, using untrusted GPU evidence as GPU
evidence, or continuing after Claude/Codex do not converge after five review
rounds for the same blocker.

## Final Visible Handoff

When execution completes or stops, write final phase reached, final status,
result artifacts, Claude review trail, tests/benchmarks actually run, unresolved
blockers, what was not concluded, and safest next human decision if any.
