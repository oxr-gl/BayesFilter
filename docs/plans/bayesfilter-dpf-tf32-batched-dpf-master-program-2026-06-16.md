# BayesFilter DPF TF32 Batched DPF Master Program - 2026-06-16

## Status

`PHASE_6_CLOSEOUT_GUARDRAILS_PASSED`

## Final Execution Note

The visible program closed through Phase 6 on 2026-06-17. The final closeout
artifact is:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p6-closeout-guardrails-result-2026-06-17.md`

The score path is now finite on the scoped tiny active-odd score/JIT fixture,
but this remains bounded engineering evidence. The program still makes no HMC
readiness, posterior correctness, production readiness, public API readiness,
TF32 superiority, or 100k-particle score-scalability claim.

## Purpose

Create and execute a visible gated program for the experimental TF32 batched
LEDH-PFPF-OT DPF lane over independent rows, chains, or seeds.

This program deliberately excludes distributed sharding of one particle cloud
across multiple GPUs. Multi-GPU work in this program means row splitting for
independent filters only.

## Active Context

Primary reset memo:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-reset-memo-2026-06-16.md`

Supporting DPF reset memo:

- `docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-reset-memo-2026-06-15.md`

Key prior evidence:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-pf-mc-error-vs-precision-result-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-tf32-default-policy-result-2026-06-15.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-t120-tf32-capacity-result-2026-06-15.md`

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can the experimental streaming LEDH-PFPF-OT DPF be made batch-native for independent rows while preserving correctness guardrails and using TF32 as the scoped performance default? |
| Candidate or mechanism | TensorFlow/TFP batched value path over independent parameter rows, chains, or seeds, with `float32` tensors and TensorFlow TF32 execution enabled for the performance lane. |
| Expected failure mode | The current path is compute-bound for active-all exact OT and the score path is not yet JIT-safe; careless batching could hide row cross-talk, precision-policy drift, or unsupported HMC claims. |
| Promotion criterion | Each phase meets its own evidence contract, writes result artifacts, and passes local plus read-only Claude review gates where material. |
| Promotion veto | Wrong baseline, missing precision/reference lane, row cross-talk, non-finite values, failed JIT smoke in phases that require JIT, score path promoted before JIT-safety, or unsupported HMC/default-readiness claim. |
| Continuation veto | TensorFlow cannot import in the chosen environment, the reviewed phase plan is inconsistent with the reset memo, required artifacts cannot be written, or Claude/Codex review fails to converge after five rounds for the same blocker. |
| Repair trigger | Fixable plan inconsistency, missing artifact coverage, failed local check, stale path, row locality issue, or precision metadata gap. |
| Explanatory diagnostics | Runtime, compile time, memory, GPU placement, TF32 metadata, precision drift versus FP64/FP32-no-TF32, and HMC-facing diagnostics after the score path is JIT-safe. |
| Must not conclude | No production default, no public API readiness, no posterior correctness, no HMC readiness, no single-filter multi-GPU particle sharding, and no broad GPU speedup claim. |

## Program Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can a visible, recoverable master program advance TF32 batched DPF work without mixing filtering, score/HMC, and distributed-sharding claims? |
| Baseline/comparator | Current streaming LEDH-PFPF-OT TF32 artifacts and FP64/FP32-no-TF32 reference lanes from the June 15 result files. |
| Primary pass criterion | All phases that are executed pass their subplan checks, write a close/result artifact, refresh the next subplan, and pass material read-only review. |
| Veto diagnostics | Detached execution, Claude used as executor, missing stop condition, missing evidence contract, proxy timing treated as correctness, HMC readiness before score JIT repair, or failure to preserve FP64/FP32-no-TF32 reference lanes. |
| Explanatory diagnostics | Wall time, compile time, GPU memory, capacity shapes, precision drift, and code complexity. |
| Not concluded | Passing this program does not prove scientific correctness, production readiness, public API readiness, or HMC posterior validity. |
| Required artifacts | Master program, visible runbook, execution ledger, phase subplans, phase results, Claude review artifacts, benchmark/result artifacts for later phases, and final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| TF32 performance default is scoped | TF32 default policy result from 2026-06-15 | Prior PF MC noise comparison made TF32 a serious performance candidate | User or code treats TF32 as global BayesFilter policy | Phase 1 precision inventory must list explicit reference lanes | reviewed |
| Batched rows are independent filters | T120 capacity result and reset memo | Multi-GPU row splitting is feasible without designing distributed OT | Claims accidentally imply one particle cloud is sharded across GPUs | Phase 0 and Phase 3 forbidden-claim checks | reviewed |
| Score/HMC is delayed | Reset memo and prior result notes | JIT-safe score path is unresolved | HMC readiness is claimed from value-only evidence | Phase 4 gate before Phase 5 | reviewed |
| TensorFlow/TFP backend | Project AGENTS policy | BayesFilter-owned algorithmic code defaults to TensorFlow/TFP | NumPy prototype leaks into implementation path | Phase 1 code inventory | reviewed |
| Visible foreground execution | Visible runbook template | Keeps recovery and user supervision simple after stream instability | Detached process or nested supervisor creates opaque state | Runbook and ledger checks | reviewed |

## Phase Index

| Phase | Name | Objective | Subplan | Result |
| ---: | --- | --- | --- | --- |
| 0 | Governance And Runbook Lock | Create and review the clean master program, visible runbook, ledger, stop handoff, and Phase 1 subplan. | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p0-governance-runbook-lock-subplan-2026-06-16.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p0-governance-runbook-lock-result-2026-06-16.md` |
| 1 | Implementation And Precision Inventory | Inventory current implementation paths, precision knobs, JIT boundaries, and reference lanes. | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p1-implementation-precision-inventory-subplan-2026-06-16.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p1-implementation-precision-inventory-result-2026-06-16.md` |
| 2 | Single-GPU Batched Value Runner | Implement or verify independent-row batching on one GPU using the current streaming TF32 value path. | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p2-single-gpu-batched-value-subplan-2026-06-16.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p2-single-gpu-batched-value-result-2026-06-16.md` |
| 3 | Two-GPU Row Splitting | Add a launcher that splits independent rows, chains, or seeds across GPU 0 and GPU 1. | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p3-two-gpu-row-splitting-subplan-2026-06-16.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p3-two-gpu-row-splitting-result-2026-06-16.md` |
| 4 | JIT-Safe Score Path | Plan and repair score-gradient execution so HMC-facing diagnostics can be meaningful. | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-streaming-gradient-nan-repair-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-streaming-gradient-nan-repair-result-2026-06-17.md` |
| 5 | HMC-Facing Diagnostics | After score JIT-safety, compare value/gradient precision and HMC energy/acceptance diagnostics. | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p5-hmc-facing-diagnostics-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p5-hmc-facing-diagnostics-result-2026-06-17.md` |
| 6 | Closeout And Guardrails | Close the program with default-policy guardrails, nonclaims, blockers, and next research tasks. | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p6-closeout-guardrails-subplan-2026-06-17.md` | `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p6-closeout-guardrails-result-2026-06-17.md` |

## Cross-Agent Review Contract

Codex is supervisor and executor in the current visible conversation.

Claude Opus max effort is a read-only reviewer only. Claude may inspect named
local files and report findings. Claude must not edit files, run experiments,
launch agents, approve boundary crossings, change pass/fail criteria, or
authorize production/scientific claims.

Claude prompts must be concise and path-based. Do not paste whole large files.
If Claude does not respond, run a small read-only probe. If the probe responds,
redesign the review prompt and retry. Stop after five rounds for the same
blocker.

## Repair Loop

For each material phase:

1. Read the current subplan.
2. Record a skeptical audit before execution.
3. Execute the smallest visible step that answers the phase question.
4. Run required local checks.
5. Write a phase result or blocker result.
6. Draft or refresh the next subplan.
7. Review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
8. Send material plans, results, or repairs to Claude as read-only review.
9. Patch fixable problems visibly and rerun focused checks.
10. Stop after five Claude rounds for the same blocker.

## Quiet Execution Requirement

Commands that may emit large stdout/stderr must preserve full output in log
files and keep the session window to bounded summaries only.

This applies to TensorFlow, CUDA, benchmark, sampler, long test, and Claude
review commands. Phase subplans must predeclare log paths and structured
artifact paths before such commands run. Full logs should live under
`docs/benchmarks/logs/` unless a phase subplan states a more specific location.

Do not mirror full benchmark JSON or TensorFlow/CUDA logs into the chat stream
with `tee`. Use file redirection and summarize pass/fail metadata from the
result artifacts.

## Anticipated Trusted Commands

- Claude read-only review through
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh`.
- GPU/CUDA diagnostics or benchmarks in later phases, only after a phase
  subplan states the evidence contract and artifact paths.

Package installation, network fetches, credentials, destructive filesystem or
git operations, detached execution, and production default changes require
separate human approval.

## Forbidden Claims And Actions

- Do not claim HMC readiness before Phase 5 passes.
- Do not claim production default or public API readiness.
- Do not claim one filter's particles are sharded across GPUs.
- Do not treat runtime or memory diagnostics as correctness evidence.
- Do not remove FP64 and FP32-no-TF32 reference/comparison lanes.
- Do not run detached supervisors or hidden background phase runners.
- Do not modify unrelated dirty worktree files.

## Final Handoff Requirements

The final handoff must list the final phase reached, final status, result
artifacts, Claude review trail, local checks and benchmarks actually run,
unresolved blockers, what was not concluded, and the safest next human
decision if one remains.
