# Visible Gated Execution Runbook: SR-UKF Actual-SV Analytical Score

Date: 2026-07-01

Status: DRAFT_VISIBLE_EXECUTION_RUNBOOK

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

This runbook is visible and recoverable inside the current conversation. It must
not launch a detached or nested supervisor. Do not use `codex exec`, detached
overnight launch scripts, `setsid`, `nohup`, background phase runners, or copied
workspace execution. This is an overnight-style gated plan, not a detached
agent.

## Program

Master program:

- `docs/plans/bayesfilter-srukf-actual-sv-score-master-program-2026-07-01.md`

Reviewed plan artifacts:

- `docs/plans/bayesfilter-srukf-actual-sv-score-claude-review-ledger-2026-07-01.md`

Execution ledger:

- `docs/plans/bayesfilter-srukf-actual-sv-score-visible-execution-ledger-2026-07-01.md`

Stop handoff:

- `docs/plans/bayesfilter-srukf-actual-sv-score-visible-stop-handoff-2026-07-01.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Governance And Drift Inventory | `docs/plans/bayesfilter-srukf-actual-sv-score-phase0-governance-inventory-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase0-governance-inventory-result-2026-07-01.md` |
| 1 | Generic SR-UKF Derivation | `docs/plans/bayesfilter-srukf-actual-sv-score-phase1-generic-derivation-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase1-generic-derivation-result-2026-07-01.md` |
| 2 | Generic Derivation Audit | `docs/plans/bayesfilter-srukf-actual-sv-score-phase2-generic-audit-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase2-generic-audit-result-2026-07-01.md` |
| 3 | Augmented-Noise Adapter Derivation | `docs/plans/bayesfilter-srukf-actual-sv-score-phase3-augmented-adapter-derivation-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase3-augmented-adapter-derivation-result-2026-07-01.md` |
| 4 | Adapter Derivation Audit | `docs/plans/bayesfilter-srukf-actual-sv-score-phase4-adapter-audit-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase4-adapter-audit-result-2026-07-01.md` |
| 5 | Generic Backend Implementation | `docs/plans/bayesfilter-srukf-actual-sv-score-phase5-generic-implementation-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase5-generic-implementation-result-2026-07-01.md` |
| 6 | Actual-SV Adapter Implementation | `docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-result-2026-07-01.md` |
| 7 | Thorough Test Ladder | `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-test-ladder-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-test-ladder-result-2026-07-01.md` |
| 8 | Leaderboard Admission And Release Note | `docs/plans/bayesfilter-srukf-actual-sv-score-phase8-leaderboard-release-subplan-2026-07-01.md` | `docs/plans/bayesfilter-srukf-actual-sv-score-phase8-leaderboard-release-result-2026-07-01.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter produce an audited, implemented, analytical factor-propagating SR-UKF score for actual-SV without route drift? |
| Baseline/comparator | Current actual-SV value-only UKF diagnostic, current KSC strict-SPD principal-root route, and Kalman affine fixtures. |
| Primary pass criterion | All phase gates pass with derivation audit, implementation tests, and leaderboard provenance guards. |
| Veto diagnostics | Autodiff admitted score, historical SVD/eigenderivative admitted score, strict-SPD principal-root derivative substitution, wrong actual-SV sigma-point law, failed formal/local audit, failed reconstruction, failed FD consistency, failed score-at-true-parameter check, or unsupported release claim. |
| Explanatory diagnostics | Runtime, CPU/GPU performance, UKF approximation gaps, FD sensitivity, and branch telemetry. |
| Not concluded | Exact likelihood correctness, HMC convergence, posterior validity, or method superiority. |
| Artifacts | Master, subplans, ledgers, result notes, LaTeX diffs, MathDevMCP audits, Claude reviews, code/tests, leaderboard files if admitted. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Two-product split | User directive | Separates numerical backend drift from model-law drift | Adapter bug hides backend bug | Phase 0/1/3 artifact checks | reviewed hypothesis |
| Visible execution | Template | Recoverable current-conversation execution | Detached agent loses governance | Runbook forbids detached launch | required |
| Claude read-only | AGENTS.md | Prevents reviewer becoming executor | Claude edits/runs commands | Bounded prompt and ledger | required |
| MathDevMCP label audits | Local tool policy | Equation-level audit before implementation | Labels too broad/missing | Phase 2/4 lookup checks | planned |
| CPU-only for non-GPU checks | AGENTS.md | Avoid false GPU sandbox failures | TensorFlow imports accidentally use GPU | Set `CUDA_VISIBLE_DEVICES=-1` when needed | planned |

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

If the audit finds a material flaw, revise the plan or write a blocker note
before running the phase.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract,
   append ledger entry.
2. `EXECUTE_MINIMAL`: run only visible commands in the current conversation.
3. `ASSESS_GATE`: compare outputs against criteria and veto diagnostics.
4. `PASS_REVIEW`: use Claude read-only review for material phases.
5. `REPAIR_LOOP`: patch fixable issues visibly, rerun focused checks, stop
   after five Claude rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after gate passes, otherwise write handoff.

## Claude Read-Only Review Template

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, run a tiny probe. If the probe responds, narrow the
material prompt. If the probe fails in trusted execution, write a blocker.

## Human-Required Stop Conditions

Stop if continuing would require:

- changing the scientific target;
- changing pass/fail criteria after seeing results;
- package installation, network fetch, credentials, or environment setup;
- destructive git/filesystem actions;
- model-file mutation;
- default-policy change;
- detached or nested agent launch;
- GPU/HMC/long runtime outside a reviewed subplan;
- continuing after five failed Claude convergence rounds.

## Launch Instruction

Launch means begin Phase 0 visibly in this conversation: run local artifact
checks, get bounded Claude review of launch artifacts, write the Phase 0 result,
and refresh the Phase 1 handoff. It does not mean detached overnight execution.
