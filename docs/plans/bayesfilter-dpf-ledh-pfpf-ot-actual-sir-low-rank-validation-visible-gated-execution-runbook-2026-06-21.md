# Actual-SIR Low-Rank Validation Visible Gated Execution Runbook

Date: 2026-06-21

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use `codex
exec`, `overnight_gated_launch.sh`, `setsid`, `nohup`, detached `tmux`, or
copied-workspace execution.

## Quiet Visible Execution Pattern

Large TensorFlow/GPU/Claude commands must write full stdout/stderr to bounded
log files under `/tmp` or structured JSON/Markdown artifacts under
`docs/benchmarks`. Chat output should summarize status, artifact paths, and
bounded failure tails only.

## Program

Master program:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-master-program-2026-06-21.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-claude-review-ledger-2026-06-21.md`

Execution ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-visible-execution-ledger-2026-06-21.md`

Stop handoff:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-visible-stop-handoff-2026-06-21.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| ---: | --- | --- | --- |
| 0 | Governance and skeptical audit | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p00-governance-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p00-governance-result-2026-06-21.md` |
| 1 | Harness integration | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p01-harness-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p01-harness-result-2026-06-21.md` |
| 2 | Tiny actual-SIR route smoke | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p02-smoke-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p02-smoke-result-2026-06-21.md` |
| 3 | Paired actual-SIR ladder | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p03-paired-ladder-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p03-paired-ladder-result-2026-06-21.md` |
| 4 | Large-N actual-SIR envelope | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p04-large-n-envelope-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p04-large-n-envelope-result-2026-06-21.md` |
| 5 | Closeout | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p05-closeout-subplan-2026-06-21.md` | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-result-2026-06-21.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can low-rank make actual-SIR d18 LEDH/PFPF-OT more efficient on paired feasible rows, and can it extend the executable envelope toward `N=50000` to `N=100000` without validity vetoes? |
| Baseline/comparator | Existing streaming actual-SIR TF32/GPU route. |
| Primary pass criterion | Valid route-fired artifacts, predeclared paired engineering-comparability on feasible rows, exact P03 `warmups=1`, `repeats=3` warm-median speed on the same physical GPU UUID, and physical GPU provenance for GPU claims. Exact `3600s` same-row timeout-boundary evidence is resource-boundary evidence only unless paired comparability evidence is also present. Low-rank-only large-N rows are executable-envelope evidence only. |
| Veto diagnostics | Nonfinite outputs, GPU/TF32 mismatch, missing actual-SIR semantics, route fallback, dense low-rank materialization, invalid factors, or paired comparability failure for support rows. |
| Explanatory diagnostics | Runtime, memory, compile time, warm-call time, ESS, log-likelihood/filtered-summary deltas, projection iterations. |
| Not concluded | No posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or statistical ranking. |
| Artifacts | Master program, ledgers, phase results, benchmark JSON/Markdown row artifacts, final result, stop handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Actual-SIR d18 as workload | Existing P8j/P8n artifacts | Real repo-native high-dimensional nonlinear workload | Synthetic proxy claim | P00 source checks | planned |
| Streaming route as comparator | Existing actual-SIR benchmark | Direct current route | Wrong baseline | P00/P03 checks | planned |
| GPU1 preferred | User instruction in this execution thread: "for GPU usage, use GPU1 unless it is busy than use GPU0" | Avoid busy GPU0 when possible | Logical `/GPU:0` can hide physical index under CUDA remapping, and cross-GPU paired rows would be unfair | `nvidia-smi` plus manifest fields: requested `CUDA_VISIBLE_DEVICES`, selected physical index/name/UUID when available, fallback status; paired support rows must use one physical GPU UUID for both routes | planned |
| Low-rank route as diagnostic semantic replacement | Existing solver diagnostics | Honest source classification | Unsupported source-faithful claim | P01/P05 review | planned |

## Skeptical Plan Audit

Before each material phase, Codex must record a skeptical audit in the ledger
checking wrong baselines, proxy metric promotion, missing stop conditions,
unfair comparisons, hidden assumptions, stale context, environment mismatch,
and artifact mismatch. If the audit finds a material flaw, revise the plan or
write a blocker before executing.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only commands needed for the phase.
3. `ASSESS_GATE`: compare outputs to criteria and write phase result.
4. `PASS_REVIEW`: use Claude read-only review for material plan/result claims.
5. `REPAIR_LOOP`: patch fixable issues, rerun focused checks, stop after five
   Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after phase gate passes.

## Claude Read-Only Review Template

Prompt Claude with paths only:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review this path:
<path>

You may read only the same-prefix docs/plans paths named inside that file.

Check wrong baseline, proxy metrics promoted to pass criteria, missing stop
condition, unfair comparison, hidden assumption, stale context, environment
mismatch, unsupported claim, and artifact mismatch.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetch,
credentials, destructive filesystem/git action, public API/default change,
shared contract/schema change, unapproved resource expansion, or changing
pass/fail criteria after seeing results.

## Final Visible Handoff

Final handoff must report final phase reached, final status, result artifacts,
Claude review trail, tests/benchmarks actually run, unresolved blockers,
nonclaims, and safest next human decision.
