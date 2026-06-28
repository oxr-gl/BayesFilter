# Visible Gated Execution Plan: Low-Rank LEDH-PFPF-OT TF32 Scale Smoke

Date: 2026-06-20

## Status

`FINAL_TUNED_GPU_SCALE_PASSED_DIAGNOSTIC_ONLY`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only.  Claude may inspect bounded paths and
report findings.  Claude may not edit files, run experiments, launch agents,
authorize boundary crossings, or decide scientific/product readiness.

This runbook is visible and recoverable inside the current conversation.  It
does not launch detached agents, `codex exec`, `overnight_gated_launch.sh`,
`setsid`, `nohup`, detached `tmux`, background phase runners, or copied
workspaces.

## Quiet Visible Execution Pattern

Full stdout/stderr from TensorFlow, CUDA, GPU probes, long diagnostics, and
Claude review commands is preserved in logs.  The chat receives bounded
summaries only: exit status, artifact paths, pass/fail fields, and short
failure tails when needed.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-master-program-2026-06-20.md`

Claude review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-claude-review-ledger-2026-06-20.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-visible-execution-ledger-2026-06-20.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-visible-stop-handoff-2026-06-20.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| LR-TF32-0 | Governance, Evidence, And Review Gate | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p00-governance-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p00-governance-result-2026-06-20.md` |
| LR-TF32-1 | Harness And Small Invariants | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p01-harness-invariants-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p01-harness-invariants-result-2026-06-20.md` |
| LR-TF32-2 | Medium CPU No-Dense Smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02-medium-cpu-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02-medium-cpu-result-2026-06-20.md` |
| LR-TF32-2A | Coarse Low-Rank Solver-Route Tuning | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02a-tuning-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02a-tuning-result-2026-06-20.md` |
| LR-TF32-2B | Focused Low-Epsilon Tuning | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02b-focused-tuning-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02b-focused-tuning-result-2026-06-20.md` |
| LR-TF32-2C | Tuned Medium CPU No-Dense Validation | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02c-medium-cpu-tuned-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p02c-medium-cpu-tuned-result-2026-06-20.md` |
| LR-TF32-3 | Trusted GPU FP32/TF32 Scale Smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p03-trusted-gpu-scale-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p03-trusted-gpu-scale-result-2026-06-20.md` |
| LR-TF32-4 | Closeout And Stop | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-p04-closeout-subplan-2026-06-20.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-low-rank-tf32-scale-smoke-result-2026-06-20.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the low-rank coupling solver-route resampler run on LEDH/PFPF-shaped batched particle clouds at 50k and conditionally 100k particles without dense transport materialization, OOM, or invalid numerical artifacts? |
| Baseline/comparator | Exact weighted input estimates are the downstream reference; naive uniform no-transport is explanatory only; dense OT and positive-feature are not comparators. |
| Primary pass criterion | Governance review passes, small invariants pass, initial medium failure is amended as a missing-tuning planning/usage error, tuned medium no-dense validation passes, trusted GPU 50k scale smoke passes, conditional 100k runs only after 50k passes, and final closeout preserves all non-claims. |
| Veto diagnostics | Invalid factors/particles, dense materialization, residual/moment threshold failure, OOM/non-completion, missing manifest/artifact, unsupported claims, untrusted GPU evidence, or boundary edits. |
| Explanatory diagnostics | Runtime, memory, projection iterations, rank, factor minima, candidate-vs-naive deltas, device metadata. |
| Not concluded | No speedup, ranking, superiority, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, full solver fidelity, broad scalable-OT selection, or TF32-help claim. |
| Artifacts | Phase results, JSON/Markdown diagnostics with embedded run manifests, logs, Claude review ledger, visible ledger, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Low-rank factor route | Existing P12/Wave2 implementation | This is the algorithm under test, not a new candidate. | Small validity does not imply large feasibility. | P01 invariants and P02 medium smoke. | Reviewed in prior low-rank lane; rechecked here. |
| Exact weighted input moments as downstream reference | Resampling contract | Tests resampling preservation without dense OT. | Moment tolerance could be too loose or too strict. | Fixed thresholds before runs. | Predeclared. |
| 50k before 100k | User scale target and resource caution | Avoids jumping to 100k after a 50k failure. | 50k may pass while 100k fails. | Conditional 100k row. | Predeclared. |
| Runtime/memory explanatory only | Scientific evidence policy | Prevents speedup/default claims from one smoke. | User may overread time values. | Non-claims in artifacts. | Predeclared. |
| Frozen bounded fixture | Master fixture contract | Makes absolute moment thresholds interpretable. | Fixture scale drift could create false pass/fail. | Manifest fixture checks in P01-P03. | Predeclared. |
| Embedded run manifest | Scientific evidence policy | Preserves command, env, device, fixture, seed, and artifact provenance. | Missing provenance could make a pass unrecoverable. | JSON schema checks in P01-P04. | Predeclared. |

## Skeptical Plan Audit

Before executing each phase, Codex records a skeptical audit in the ledger:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run visible commands in the current conversation with
   quiet logs.
3. `ASSESS_GATE`: compare outputs to criteria and write phase result.
4. `PASS_REVIEW`: use Claude read-only review for material subplans/results.
5. `REPAIR_LOOP`: patch fixable lane-owned issues, rerun focused checks, stop
   after five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the phase gate passes.

## Claude Read-Only Review Prompt Rule

Prompts to Claude must provide paths and bounded questions only.  Do not paste
whole file bodies.  Claude must end with exactly `VERDICT: AGREE` or
`VERDICT: REVISE`.

Claude worker launches must use trusted/elevated execution through
`bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh`.  Any
non-elevated hang, missing output, auth error, or network error is sandbox
evidence only until a trusted minimal probe is rerun.

If Claude does not respond, Codex runs a tiny path-only probe.  If the probe
responds, Codex redesigns the prompt rather than treating Claude as unavailable.

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch,
credentials, destructive git/filesystem action, changing thresholds after
seeing results, default policy changes, unrelated dirty-work edits, untrusted
GPU evidence interpretation, or continuing after five nonconvergent Claude
review rounds on the same blocker.

## Approval Requests Anticipated

- Claude path-only read-only reviews through:
  `bash /home/ubuntu/python/claudecodex/scripts/claude_worker.sh` with
  trusted/elevated execution.
- Trusted GPU/TF32 scale command in Phase LR-TF32-3.
- GPU probe command, such as `nvidia-smi`.
- Long `timeout`-wrapped diagnostic commands writing logs under
  `docs/benchmarks/logs/`.

## Final Visible Handoff

When execution completes or stops, write final phase reached, final status,
result artifacts, Claude review trail, checks actually run, unresolved
blockers, non-claims, and safest next decision.
