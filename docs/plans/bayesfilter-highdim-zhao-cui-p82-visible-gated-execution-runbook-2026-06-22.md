# P82 Visible Gated Execution Runbook

Date: 2026-06-22

## Status

`P6_P8_COMPLETION_PLAN_DRAFTED_PENDING_REVIEW`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus is a read-only reviewer only.

This runbook must not launch a detached or nested agent.  Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

Visible execution stays in the current conversation.  If detached overnight
execution is desired later, write a separate detached-supervisor plan and stop.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-ledh-pfpf-ot-sir-d18-regression-gradient-master-program-2026-06-22.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-claude-review-ledger-2026-06-22.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-visible-execution-ledger-2026-06-22.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-visible-stop-handoff-2026-06-22.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
|---|---|---|---|
| 0 | Governance bootstrap | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase0-governance-bootstrap-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase0-governance-bootstrap-result-2026-06-22.md` |
| 1 | Route/protocol inventory | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase1-route-protocol-inventory-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase1-route-protocol-inventory-result-2026-06-22.md` |
| 2 | Regression-FD harness | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase2-regression-fd-harness-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase2-regression-fd-harness-result-2026-06-22.md` |
| 3 | Zhao-Cui analytical route | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase3-zhaocui-analytical-route-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase3-zhaocui-analytical-route-result-2026-06-22.md` |
| 4 | FD-only LEDH consistency | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase4-fd-only-ledh-consistency-subplan-2026-06-22.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase4-fd-only-ledh-consistency-result-2026-06-22.md` |
| 5 | Manual streaming wiring | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase5-manual-streaming-gradient-wiring-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase5-manual-streaming-gradient-wiring-result-2026-06-23.md` |
| 6 | Tiny manual streaming GPU smoke | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-result-2026-06-23.md` |
| 7 | Actual-gradient feasibility | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-result-2026-06-23.md` |
| 8 | Governed FD consistency | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-governed-fd-consistency-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-governed-fd-consistency-result-2026-06-23.md` |
| 9 | Closeout | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase9-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase9-closeout-result-2026-06-23.md` |

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can LEDH-PFPF-OT SIR d=18 gradient diagnostics pass a five-seed, standard-error-aware regression-FD comparison protocol without oracle, central-difference, or HMC/default overclaims? |
| Baseline/comparator | LEDH regression FD for its own scalar.  Zhao-Cui is removed from the pass/fail path by human amendment. |
| Primary pass criterion | Every phase produces required artifacts, passes local checks/reviews, and preserves the corrected comparator and regression-FD protocol. |
| Veto diagnostics | Reintroducing Zhao-Cui as comparator evidence, treating FD as oracle, central-difference promotion, missing SE, missing trusted GPU evidence before GPU phases, hidden route mismatch, unsupported claims, or unreviewed code/GPU phase launch. |
| Explanatory diagnostics | Runtime, device placement, TF32 mode, seed variance, slope SE, regression residuals, transport residuals, memory/chunk metadata. |
| Not concluded | Posterior correctness, HMC readiness, default readiness, scientific superiority, exact likelihood correctness, manual-adjoint correctness, or streaming memory improvement. |
| Artifacts | P82 master, runbook, ledgers, subplans, results, JSON outputs, and final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
|---|---|---|---|---|---|
| Zhao-Cui removed for now | Human P82 amendment on 2026-06-22 | Allows same-scalar LEDH-vs-FD consistency despite P3 route blocker | Accidentally using Zhao-Cui evidence in P4 | P4 FD-only subplan | active amendment |
| Regression FD replaces central FD | User correction and P81 protocol correction | Central FD is too noisy | False gradient bug from two-point noise | P2 harness audit/patch | reviewed input |
| Five fixed seeds | User correction | Reduces seed-specific conclusions | Hidden seed luck | P2/P5/P6 seed manifest checks | reviewed input |
| FD N=1000, LEDH actual N=10000 | User correction | Separates line diagnostic budget from actual estimate budget | Unfair particle budget or hidden MC noise | P5/P6 run manifests | reviewed input |
| 2-SE discrepancy rule | User correction plus P0 Claude review caution | Triage likely issues in uncertainty units | Misread as calibrated test or certification | P7 variance-assumption statement | heuristic only |
| GPU default | Repository AGENTS policy | BayesFilter default execution target is GPU | Sandbox hides GPU or CPU result overclaimed | Trusted GPU preflight in P4 | governance |

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and,
for material phases, in the execution ledger.

Check:

- wrong baselines;
- proxy metrics being treated as promotion criteria;
- missing stop conditions;
- unfair comparisons;
- hidden assumptions;
- stale context;
- environment mismatch;
- commands whose artifacts would not answer the phase question.

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

## Visible State Machine

For every governed P82 regression-FD command, explicitly pass
`--trim-extreme-mode value`.  The result artifact must record
`raw_point_count = 13`, `fit_point_count = 11`, and that the dropped points were
chosen by highest/lowest mean-over-seed objective value, not by offset
magnitude.  If this flag or metadata is missing, the run is not P82
protocol-compliant.

For each phase:

1. `PRECHECK`
   - Read the phase subplan.
   - Confirm prerequisites.
   - Restate the phase evidence contract in chat.
   - Append a ledger entry.
2. `EXECUTE_MINIMAL`
   - Run only visible commands in the current conversation.
   - Prefer the smallest diagnostic or implementation needed to answer the
     phase question.
   - Preserve unrelated dirty worktree changes.
3. `ASSESS_GATE`
   - Compare outputs against the primary criterion and veto diagnostics.
   - Write or update the required phase result artifact.
4. `PASS_REVIEW`
   - Send material phase fact packets to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, patch visibly.
   - Rerun focused checks.
   - Review again when material.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Claude Read-Only Review Protocol

Use Claude only as a reviewer.  Do not send whole files.  Send compact
path-anchored fact packets and one focused question.

Required prompt shape:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review the P82 fact packet below for:
- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- unfair comparison;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch.

Findings first. End with exactly one final line:
VERDICT: AGREE
or
VERDICT: REVISE
```

If Claude stalls, probe:

```text
READ-ONLY PROBE. Reply exactly PROBE_OK.
```

If the probe works, redesign the prompt.

## Human-Required Stop Conditions

Stop if continuing would require:

- a project-direction decision not already in the reviewed plan;
- package installation, network fetch, credentials, or environment setup;
- destructive git or filesystem action;
- changing pass/fail criteria after seeing results;
- changing default policy;
- modifying unrelated dirty user work;
- interpreting GPU/special hardware results without trusted-context evidence;
- continuing after Claude and Codex do not converge after five review rounds.

## Final Visible Handoff

When execution completes or stops, write:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests/benchmarks actually run;
- unresolved blockers;
- what was not concluded;
- safest next human decision, if any.
