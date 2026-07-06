# BayesFilter DPF LEDH-PFPF-OT Default Quality Validation Visible Gated Execution Runbook

Date: 2026-06-20

## Status

`COMPLETED_P03_MEDIUM_GPU_QUALITY_SCREEN_PASSED_WITH_NONCLAIMS`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only. Claude must not edit files, run
experiments, launch agents, authorize phase crossing, or change state.

This runbook is visible foreground execution in the current conversation. It
must not launch a detached or nested agent. Do not use `codex exec`,
`overnight_gated_launch.sh`, `setsid`, `nohup`, detached `tmux`, backgrounded
phase runners, or copied-workspace execution.

## Quiet Visible Execution Pattern

Commands expected to produce large TensorFlow/CUDA/Claude output should write
structured JSON/Markdown artifacts directly and keep chat output bounded. If a
command fails, inspect bounded failure output and preserve the artifact or
result note.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-master-program-2026-06-20.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-claude-review-ledger-2026-06-20.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-visible-execution-ledger-2026-06-20.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-visible-stop-handoff-2026-06-20.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance, evidence contract, and Claude review | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p00-governance-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p00-governance-result-2026-06-20.md` |
| P01 | Paired quality harness implementation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p01-harness-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p01-harness-result-2026-06-20.md` |
| P02 | Trusted GPU paired medium quality screen | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p02-medium-gpu-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p02-medium-gpu-result-2026-06-20.md` |
| P03 | Closeout and next-rung handoff | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-p03-closeout-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-default-quality-validation-result-2026-06-20.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the promoted GPU TF32 streaming LEDH-PFPF-OT route preserve downstream LEDH filter outputs in a paired medium quality rung? |
| Baseline/comparator | Paired FP64 TF32-disabled streaming arm; FP32 TF32-disabled is diagnostic. |
| Primary pass criterion | P00-P03 gates pass, and P02 preserves paired seeds plus per-seed/per-output drift records showing default-arm max-relative drift to FP64 `<= 1.0e-2` for each downstream output across paired seeds. |
| Drift formula | `max(abs(candidate - reference) / max(1.0, abs(reference)))` per output array and paired seed; `1.0e-2` is an engineering sanity threshold only. |
| Veto diagnostics | Child failure, nonfinite output, GPU placement mismatch, missing output arrays, config mismatch, paired seed count mismatch, missing per-seed/per-output drift fields, precision metadata mismatch, stale artifacts, unsupported claim, or drift above tolerance. |
| Explanatory diagnostics | Runtime, memory, compile time, warm timing, FP32-no-TF32 drift, and TF32-vs-no-TF32 extra drift. |
| Not concluded | No posterior correctness, HMC readiness, sampler convergence, speedup, statistical superiority, dense Sinkhorn equivalence, public API readiness, or target-shape scientific validity. |
| Artifacts | Phase subplans/results, benchmark JSON/MD artifacts, child artifacts, execution ledger, Claude review ledger, and stop handoff. |

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   and append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands needed to answer the phase.
3. `ASSESS_GATE`: compare outputs against hard screens and write result.
4. `PASS_REVIEW`: use Claude as read-only reviewer for material plans or
   interpretations.
5. `REPAIR_LOOP`: patch fixable blockers visibly, rerun focused checks, and
   retry read-only review, stopping after five rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after gate pass and reviewed next artifact.

## Human-Required Stop Conditions

Stop if continuing would cross or require human, runtime, model-file, funding,
product-capability, default-policy, or scientific-claim authority not already
granted in this program. Also stop for package installation, network fetch,
credentials, destructive git/filesystem action, modifying unrelated dirty work,
changing criteria after seeing results, using untrusted GPU evidence as GPU
evidence, or continuing after Claude/Codex do not converge after five review
rounds for the same blocker.
