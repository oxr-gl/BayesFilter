# Visible Gated Execution Runbook: LEDH Highdim Row Score Admission

Date: 2026-07-05

## Status

`DRAFT_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook is visible execution inside the current conversation. It does not
launch detached supervisors or nested agents.

## Quiet Visible Execution Pattern

Use bounded logs and bounded chat summaries for large-output commands, GPU
commands, long tests, and Claude review commands.

Principle: full stdout/stderr goes to artifacts when needed; chat gets the
phase question, the bounded result, and the gate decision.

## Program

Master program:

- `docs/plans/bayesfilter-ledh-highdim-row-score-admission-master-program-2026-07-05.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-highdim-row-score-admission-visible-execution-ledger-2026-07-05.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-highdim-row-score-admission-visible-stop-handoff-2026-07-05.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Launch and blocker freeze | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase0-launch-blocker-freeze-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase0-launch-blocker-freeze-result-2026-07-05.md` |
| 1 | Fixed spatial SIR full-row score promotion | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase1-fixed-spatial-sir-full-row-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase1-fixed-spatial-sir-full-row-result-2026-07-05.md` |
| 2 | Actual SV same-target adapter and score | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase2-actual-sv-same-target-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase2-actual-sv-same-target-result-2026-07-05.md` |
| 3 | KSC SV same-target adapter and score | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase3-ksc-sv-same-target-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase3-ksc-sv-same-target-result-2026-07-05.md` |
| 4 | Predator-prey same-target adapter and score | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase4-predator-prey-same-target-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase4-predator-prey-same-target-result-2026-07-05.md` |
| 5 | Generalized SV same-target adapter and score | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase5-generalized-sv-same-target-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase5-generalized-sv-same-target-result-2026-07-05.md` |
| 6 | Leaderboard reassembly and row test expansion | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase6-leaderboard-reassembly-subplan-2026-07-05.md` | `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase6-leaderboard-reassembly-result-2026-07-05.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the remaining LEDH highdim rows be repaired in an order that respects target identity first and derivative identity second? |
| Baseline/comparator | The July 3 row ledger, July 3 closeout result, the actual-SV corrected derivation note, and the July 5 `N=10000` LEDH score-memory suite. |
| Primary pass criterion | Each phase writes a direct pass/block result, runs the required local checks, refreshes the next subplan, and clears read-only review before the next material phase begins. |
| Veto diagnostics | Wrong-target evidence being treated as correct, scoped rows being treated as full rows, autodiff being treated as admitted score evidence, or silent change of phase criteria. |
| Explanatory diagnostics | Runtime notes, memory notes, legacy callback traces, and historical blocked evidence. |
| Not concluded | No admitted score claim for blocked rows, no HMC claim, no runtime cross-ranking claim, and no scientific superiority claim. |
| Artifacts | Master program, phase subplans, visible execution ledger, stop handoff, review bundle, review logs, phase results, and later code/test artifacts. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Fixed spatial SIR first | July 3 ledger and July 5 score suite | It has the shortest path from existing value route and scoped manual score to full-row repair. | Scoped diagnostic might still be a different scalar. | Phase 1 target freeze and bridge check. | reviewed baseline |
| Actual SV before KSC | Actual-SV corrected derivation note | KSC should reuse a settled transformed-SV target discipline. | KSC work could accidentally copy a wrong actual-SV target pattern. | Phase 2 target trace. | reviewed baseline |
| Predator-prey before generalized SV | July 2 blocker inventory | Predator-prey has a concrete current-adapter blocker; generalized SV has a more ambiguous target-family blocker. | Predator-prey could still turn out more ambiguous than expected. | Phase 4 target note. | hypothesis |
| Final leaderboard phase only after row repairs | July 3 closeout result | Prevents false all-model score promotion. | Pressure to publish a partial rerun early. | Phase 6 gate text. | reviewed baseline |

## Skeptical Plan Audit

Before each phase:

- check that the phase still answers one narrow blocker question;
- check that the phase does not promote a score before the value target;
- check that diagnostics are not being promoted to pass criteria;
- check that the next artifact would directly answer the phase question.

If any of those fail, revise the subplan before running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`
   - read the subplan;
   - restate the evidence contract in chat;
   - append a ledger entry.
2. `EXECUTE_MINIMAL`
   - run only the smallest local checks or edits needed for that phase.
3. `ASSESS_GATE`
   - compare outputs to the phase criterion and stop conditions;
   - write the phase result.
4. `PASS_REVIEW`
   - review the phase result and the next subplan with Claude read-only if the
     phase is material;
   - if Claude is unavailable, use a fresh Codex review packet and record that
     substitution.
5. `REPAIR_LOOP`
   - patch fixable issues visibly;
   - rerun focused checks;
   - stop after five review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - advance only when the current phase gate passes.

## Plain-Language Gate

Every result must:

- state the exact scalar target;
- state the exact differentiated quantity;
- use direct verdicts such as `correct`, `wrong relative to the stated target`,
  `unsupported`, or `not checked`;
- avoid soft language that hides unsupported claims.

## Claude Read-Only Review Procedure

Use project-local review bundles and the Claude review gate script.

If Claude does not respond:

1. run the tiny probe in trusted execution;
2. if the probe passes, narrow the prompt surface and retry;
3. if the probe fails, replace the review with a fresh Codex review and record
   that Claude was unavailable.

Claude cannot authorize scientific claims, runtime boundary crossings, or
default-policy changes.

## Human-Required Stop Conditions

Stop if continuing would require:

- a change to pass/fail criteria after results are seen;
- package installation or new environment setup;
- destructive git action;
- publishing a new claim not already scoped in the phase plan;
- more than five review rounds for the same blocker.
