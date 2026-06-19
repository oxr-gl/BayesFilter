# P66 Visible Gated Execution Runbook

Date: 2026-06-15

## Status

`P66_FIXED_BRANCH_VALIDATION_LADDER_REPLACEMENT_PASSED`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook must not launch a detached or nested agent. Do not use:

- `codex exec`;
- `overnight_gated_launch.sh`;
- `setsid`, `nohup`, or detached `tmux` supervisors;
- backgrounded phase runners;
- copied-workspace execution.

If detached overnight execution is needed later, stop and write a separate
detached-supervisor plan.  This runbook is for visible, recoverable execution
inside the current conversation.

## Program

Master program:

- `docs/plans/bayesfilter-highdim-zhao-cui-p66-fixed-branch-validation-ladder-master-program-2026-06-15.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p66-claude-review-ledger-2026-06-15.md`

Execution ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-p66-visible-execution-ledger-2026-06-15.md`

Stop handoff:

- `docs/plans/bayesfilter-highdim-zhao-cui-p66-visible-stop-handoff-2026-06-15.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance, baseline, and planning basis | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase0-governance-baseline-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase0-governance-baseline-result-2026-06-15.md` |
| 1 | Validation contract and API design | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase1-validation-contract-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase1-validation-contract-result-2026-06-15.md` |
| 2 | Implementation and focused tests | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase2-implementation-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase2-implementation-result-2026-06-15.md` |
| 3 | Closeout and handoff | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase3-closeout-subplan-2026-06-15.md` | `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase3-closeout-result-2026-06-15.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P66 replace the invalid old P60 low/high closeness primary gate with a source-invariant admissibility plus adjacent-ladder validation contract? |
| Baseline/comparator | P65 closeout: zero-TT repair passed, old P60 still blocks because crude low `(degree=0, rank=1)` and first nontrivial high `(degree=1, rank=2)` differ. |
| Primary pass criterion | The old low/high comparison is demoted to sentinel/explanatory status, admissibility/noncollapse becomes a fixed-branch precondition gate, adjacent rank/degree schema-only ladder rows are added with sample-adequacy permission-to-diagnose checks, and focused tests/reviews pass without correctness overclaim. |
| Veto diagnostics | Old thresholds weakened; sentinel gap hidden; source-route invariants changed; defensive `tau` changed; fixed-HMC adaptation called source-faithful Zhao--Cui; d=18 correctness claimed from admissibility. |
| Explanatory diagnostics | Old P60 deltas, square-root normalizers, core norms, condition numbers, ESS, correction ranges, sample adequacy ratios, adjacent-ladder deltas. |
| Not concluded | No d=18 correctness, no d=50/d=100 scaling, no adaptive Zhao--Cui parity, no HMC readiness. |
| Artifacts | P66 master program, phase subplans/results, Claude review ledger, visible execution ledger, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| CPU-only execution | AGENTS GPU/CUDA policy | P66 validates logic and source-route contracts, not GPU performance. | TensorFlow CUDA chatter could be misread. | Set `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`. | planned |
| P65 closeout as baseline | P65 Phase 3 result | It records the repaired zero-TT behavior and residual old P60 blockers. | Stale local state. | Phase 0 fresh JSON probe. | to verify |
| Old P60 gap as sentinel | User/Codex diagnosis and P65 evidence | `(0,1)` is too crude to be a convergence baseline for the 36D SIR target. | Sentinel evidence accidentally promoted or hidden. | Phase 0 planning-basis result and Phase 1 status taxonomy. | hypothesis pending review |
| Adjacent ladder as replacement | Numerical validation discipline | One-factor rank/degree changes are fairer than crude-vs-first-nontrivial comparison. | Sample adequacy missing or runtime too high. | Phase 1 sample adequacy rule before implementation. | planned |

## Interpretation Discipline

- Admissibility/noncollapse is a precondition and veto gate, not convergence
  evidence.
- Sample adequacy permits interpreting a convergence diagnostic; it is not a
  convergence pass.
- Adjacent rank/degree ladder stability is P66's intended convergence-style
  diagnostic, but Phase 2 records schema-only rows and does not claim stability.
  Even a future stability pass would not imply d=18 correctness.
- The old `(0,1)` versus `(1,2)` gap must remain visible as a neutral sentinel
  diagnostic.

## Skeptical Plan Audit

Before executing any phase, Codex must record a skeptical audit in chat and, for
material phases, in the execution ledger.

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
   - Send material phase results, repairs, implementation diffs, or final
     decisions to Claude as read-only review.
   - Continue only after `VERDICT: AGREE`, or revise and retry.
5. `REPAIR_LOOP`
   - For fixable blockers, write a blocker plan.
   - Get Claude review when material.
   - Apply the repair visibly.
   - Rerun focused checks.
   - Write a blocker result.
   - Stop after five Claude review rounds for the same blocker.
6. `ADVANCE_OR_STOP`
   - Advance only after the current phase gate passes.
   - Stop and write the handoff if a human-required blocker appears.

## Claude Read-Only Review Template

Use Claude only as a reviewer. The prompt must say:

```text
READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

Review:
- <phase result / blocker plan / implementation diff / final decision>

Check:
- wrong baseline;
- proxy metrics promoted to pass criteria;
- missing stop condition;
- unfair comparison;
- hidden assumption;
- stale context;
- environment mismatch;
- unsupported claim;
- artifact mismatch.

Findings first. End with exactly:
VERDICT: AGREE
or
VERDICT: REVISE
```

Codex must preserve the review artifact and inspect whether Claude actually
remained read-only.

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
