# LEDH-PFPF-OT Large-Particle Efficiency Visible Gated Execution Runbook

Date: 2026-06-21

Status: DRAFT_VISIBLE_EXECUTION_RUNBOOK

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only.

This visible runbook must not launch detached or nested execution. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, detached `tmux`, or backgrounded phase runners;
- copied-workspace execution.

## Quiet Visible Execution Pattern

Full TensorFlow/CUDA/benchmark output is an artifact, not chat content. The
large-particle wrapper must capture child stdout/stderr tails and preserve child
JSON/Markdown artifacts. The session should receive only compact summaries:
exit status, pass/fail fields, artifact paths, and bounded failure tails.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-master-program-2026-06-21.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-claude-review-ledger-2026-06-21.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-visible-execution-ledger-2026-06-21.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-visible-stop-handoff-2026-06-21.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| P00 | Governance and claim lock | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p00-governance-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p00-governance-result-2026-06-21.md` |
| P01 | Harness implementation and static checks | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p01-harness-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p01-harness-result-2026-06-21.md` |
| P02 | Trusted GPU selection preflight | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p02-gpu-selection-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p02-gpu-selection-result-2026-06-21.md` |
| P03 | Streaming large-`N` reach ladder | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-ladder-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-ladder-result-2026-06-21.md` |
| P04 | Same-route TF32-vs-FP32 runtime | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-runtime-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-runtime-result-2026-06-21.md` |
| P05 | Dense breakpoint context | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p05-dense-breakpoint-context-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p05-dense-breakpoint-context-result-2026-06-21.md` |
| P06 | Closeout and decision | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p06-closeout-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-result-2026-06-21.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can current GPU TF32 streaming LEDH-PFPF-OT make the LGSSM-shaped LEDH-PFPF-OT benchmark operational at large particle counts by avoiding dense storage, and does TF32 show descriptive same-route runtime benefit? |
| Baseline/comparator | Streaming FP32+TF32 default for reach; streaming FP32-no-TF32 same-route comparator for runtime; dense/non-streaming only small-`N` context. |
| Primary pass criterion | P03 mandatory large-`N` rungs pass hard finite/device/storage/default-metadata gates and P04 records a valid matched runtime comparison or justified blocker. |
| Veto diagnostics | Non-finite output, CPU fallback, OOM/timeout, missing artifacts, dense matrix materialized, full pre-flow storage, `return_history=True`, wrong precision metadata, untrusted GPU evidence, unrecorded GPU0 fallback, or selected-GPU contamination during timing/memory-sensitive phases. |
| Explanatory diagnostics | Runtime, compile time, memory metadata, dense small-`N` context, output previews, and stderr tails. |
| Not concluded | No posterior correctness, no HMC readiness, no statistical ranking, no dense Sinkhorn equivalence, no public API readiness. |
| Artifacts | Phase results, wrapper artifacts, JSON/Markdown benchmark outputs, review ledger, execution ledger, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| GPU1 preferred | User directive | Avoids GPU0 contention unless GPU1 is busy/unsuitable. | Silent GPU0 use. | Trusted `nvidia-smi`; GPU1 busy means at least 2048 MiB total memory used, at least 20% utilization, or any single non-display compute process using at least 2048 MiB. Light shared compute below threshold is a warning, not a veto; parent records physical GPU and reason. | Required |
| Callback proposal | Current streaming harness | Avoids full pre-flow tensor storage. | Accidental tensor proposal invalidates storage claim. | Check `stores_full_pre_flow_particles is False`. | Required |
| `return_history=False` | Efficiency question | Avoids history storage not required for value feasibility. | History storage confounds memory evidence. | Check child artifact field. | Required |
| Runtime descriptive | Scientific coding policy | Single run is not statistical evidence. | Overclaim speedup. | Nonclaim and inference-status table. | Required |

## Runtime Budget And Selection Rules

- P03 phase wall-clock budget: 4 hours; per-rung child timeout: 3600 seconds.
- P03 mandatory rungs: `1000`, `5000`, `10000`.
- P03 optional `20000` rung: run only if all mandatory rungs pass, elapsed P03
  time is at most 2 hours, the `10000` child elapsed time is at most 1200
  seconds, and no GPU-memory warning/OOM occurred.
- P04 phase wall-clock budget: 3 hours; per-arm child timeout: 3600 seconds.
- P04 downgrade rule: use the largest P03-passing rung with child elapsed time
  at most 1800 seconds if the `10000` rung failed or exceeded 1800 seconds.
- GPU fallback rule: use GPU0 only if GPU1 is absent, has at least 2048 MiB
  total memory used, has at least 20% utilization, or has any single
  non-display compute process using at least 2048 MiB, and GPU0 is usable by
  the same thresholds. Light shared compute below threshold is recorded as a
  warning, not a veto.
- P03/P04 just-in-time GPU lease rule: P02 selection does not reserve the GPU.
  Rerun trusted `nvidia-smi` immediately before timing/memory-sensitive launch;
  if the selected GPU has unrelated compute processes, defer or stop. During
  startup/rungs, if unrelated selected-GPU compute appears, stop only this
  lane's launched processes and mark completed artifacts contaminated
  diagnostic-only.

## Skeptical Plan Audit

Before each phase, Codex must check:

- wrong baselines;
- proxy metrics promoted to pass criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If a material flaw is found, patch the plan or write a blocker note before
running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run visible commands only, preserving unrelated dirty
   worktree changes.
3. `ASSESS_GATE`: compare outputs against primary criterion and veto
   diagnostics.
4. `PASS_REVIEW`: use Claude only as read-only reviewer for material phase
   plans/results or final interpretation.
5. `REPAIR_LOOP`: patch fixable blockers, rerun focused checks, and stop after
   five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the current gate passes; otherwise
   write the stop handoff.

## Claude Read-Only Review Template

Use Claude only as a reviewer:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the listed plan/result paths in the repo. Check wrong baseline, proxy
metrics promoted to pass criteria, missing stop condition, unfair comparison,
hidden assumption, stale context, environment mismatch, unsupported claim, and
artifact mismatch.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Human-Required Stop Conditions

Stop if continuing would require:

- changing the research question after results;
- changing default policy;
- installing packages, network fetches, credentials, or environment setup;
- destructive git/filesystem action;
- modifying unrelated dirty user work;
- interpreting GPU evidence without trusted context;
- continuing after five Claude/Codex review rounds for the same blocker.

## Final Visible Handoff

At completion or stop, write the final result and stop handoff with:

- largest passed LGSSM-shaped benchmark particle count and shape;
- whether streaming avoided dense transport storage and full pre-flow storage;
- whether TF32 had descriptive same-route runtime advantage;
- dense context status;
- unsupported claims;
- next recommended test.
