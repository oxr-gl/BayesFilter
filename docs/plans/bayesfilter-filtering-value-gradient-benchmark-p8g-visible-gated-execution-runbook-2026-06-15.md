# P8g Visible Gated Execution Runbook

Date: 2026-06-15

## Status

`REVIEWED_VISIBLE_EXECUTION_RUNBOOK_READY_FOR_G0_LAUNCH_APPROVAL`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only. Claude must not edit files, run
experiments, launch agents, authorize GPU execution, or change state.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- overnight launcher scripts;
- `setsid`, `nohup`, detached `tmux`, or background supervisors;
- copied-workspace execution.

This is a visible, recoverable execution runbook. Any long, GPU, or overnight
run requires an explicit launch approval checkpoint before execution.

## Program

Master program:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-gated-master-program-2026-06-15.md`

Reviewed source plan:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-gpu-ledh-gradient-dpf-program-2026-06-15.md`

Execution ledger:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-execution-ledger-2026-06-15.md`

Canonical review loop ledger:

- section `Review Loop Ledger` in `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-execution-ledger-2026-06-15.md`

Stop handoff:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-stop-handoff-2026-06-15.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
|---|---|---|---|
| G0 | GPU device and backend gate | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md` |
| G1 | Current bottleneck profile | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-result-2026-06-15.md` |
| G2 | Vectorized GPU Algorithm 1 core | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-result-2026-06-15.md` |
| G3 | Fixed-randomness LEDH gradient objective | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-result-2026-06-15.md` |
| G4 | GPU particle-count tuning | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-result-2026-06-15.md` |
| G5 | KSC and Spatial SIR callback closure | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase5-callback-closure-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase5-callback-closure-result-2026-06-15.md` |
| G6 | HMC diagnostic tiers | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tiers-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tiers-result-2026-06-15.md` |
| G7 | P8d/P8g artifact refresh | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase7-artifact-refresh-subplan-2026-06-15.md` | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase7-artifact-refresh-result-2026-06-15.md` |

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can P8g run as a visible, repair-loop-governed, GPU-first LEDH/DPF value-and-gradient program? |
| Baseline/comparator | Reviewed P8g source plan, P8e repaired runner, and P8f tuning component. |
| Primary pass criterion | Each phase passes its subplan gate or writes a blocker result and visible stop handoff. |
| Veto diagnostics | Detached launch; GPU execution without trusted probe/approval; Claude used as executor; missing phase result; blocked rows dropped; HMC overclaim. |
| Explanatory diagnostics | Ledger entries, local checks, Claude reviews, profile/tuning/gradient/HMC diagnostics. |
| Not concluded | Any algorithmic result before its phase result artifact; production HMC; stochastic PF target HMC; Zhao-Cui source faithfulness. |
| Artifacts | Master program, phase subplans/results, execution ledger including its `Review Loop Ledger` section, stop handoff, refreshed outputs. |

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run visible commands only, starting with smallest
   diagnostic.
3. `ASSESS_GATE`: compare against primary and veto diagnostics, write result.
4. `PASS_REVIEW`: use Claude read-only review for material phase results or
   next subplans.
5. `REPAIR_LOOP`: patch fixable issues visibly, rerun focused checks, stop
   after five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after phase gate passes; otherwise write
   stop handoff.

## Command And Artifact Rule

Each phase is launchable only from its subplan's `Planned Command And Artifact
Contract`. That section must name:

- repository and environment assumptions;
- the exact planned command entry points;
- which commands are CPU-only and which require trusted GPU escalation;
- phase-local output paths;
- the required phase result artifact path;
- the approval boundary for GPU, long, overnight, network, or destructive work.

If a command entry point does not exist yet, the phase may implement it only
within the phase scope, then must rerun focused local checks and refresh the
subplan/result before claiming the gate passed.

## Claude Read-Only Review Prompt Shape

Use bounded local-file prompts:

```text
READ-ONLY REVIEW ONLY.
Do not edit files, run experiments, launch agents, or change state.
Read these local repo files only as needed:
- <subplan/result/diff paths>
Review for consistency, correctness, feasibility, artifact coverage, boundary
safety, unsupported claims, and missing stop conditions.
Return exactly one verdict line: VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, run a small liveness probe. If probe succeeds,
redesign the prompt. If probe fails, write a tooling blocker.

## Human-Required Stop Conditions

Stop if continuing would require:

- GPU/CUDA/NVIDIA execution without approval;
- long or overnight run without approval;
- package installation, network fetch, credentials, or environment setup;
- destructive git/filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU results without trusted G0 evidence;
- continuing after Claude/Codex do not converge after five review rounds.

## Launch Boundary

This runbook is created now. It is not launched automatically. Before G0
execution, Codex must request approval for the exact GPU probe commands and any
Claude wrapper use not already approved in the active session.
