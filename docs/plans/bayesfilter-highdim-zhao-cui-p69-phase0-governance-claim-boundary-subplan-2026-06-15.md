# P69 Phase 0 Subplan: Governance And Claim-Boundary Baseline

metadata_date: 2026-06-15
status: DRAFT_PENDING_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
phase: 0
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Confirm the launch baseline for P69: the current work is the Zhao--Cui
fixed-HMC adaptation, not adaptive Zhao--Cui parity; P67/P68 remain
inconclusive; the next actionable phase is holdout/replay diagnostic design;
rank/degree structural diagnosis remains a later gated phase; and every later
phase must preserve source-anchor governance.

## Entry Conditions Inherited From Previous Work

- P50 contains a mathematical fixed-branch construction and explicitly states
  that fixed-branch derivatives condition on branch choices.
- P65 repaired the defensive-only high-rank collapse.
- P66 demoted the invalid old low/high closeness gate and created a
  validation-ladder contract.
- P67 ran adjacent fixed-budget ladders and remained inconclusive.
- P68 exposed fit-quality diagnostics but still remained inconclusive because
  holdout/replay evidence was unavailable and degree-ladder thresholds failed.
- The source-governance charter and AGENTS source-anchor gate remain binding.

## Required Input Artifacts

- P69 master program.
- P69 visible gated execution runbook.
- P69 visible execution ledger.
- P69 Claude review ledger.
- P69 visible stop handoff.
- Draft Phase 1 holdout/replay diagnostic design subplan.

## Required Phase 0 Output Artifacts

- Phase 0 result/close record.
- Reviewed or refreshed Phase 1 holdout/replay diagnostic design subplan.

## Required Checks, Tests, And Reviews

- Local text/source checks:
  - verify required P69 input artifacts exist;
  - verify no P69 artifact claims adaptive parity, d18 correctness, d50/d100
    scaling, or HMC readiness;
  - verify P69 artifacts mention the P68 holdout/replay gap and degree-ladder
    instability;
  - verify the runbook forbids detached/background execution.
- Skeptical plan audit before launch:
  - wrong baselines;
  - proxy metrics promoted to pass criteria;
  - missing stop conditions;
  - unfair comparisons;
  - hidden assumptions;
  - stale context;
  - environment mismatch;
  - artifacts that would not answer the phase question.
- Claude Opus max effort read-only review of the planning set to convergence
  or max five rounds.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is P69 logically ready to launch the remaining Zhao--Cui fixed-HMC adaptation work, with source-governance and claim boundaries strong enough to prevent overclaim? |
| Baseline/comparator | P50 document, P65/P66/P67/P68 result artifacts, source-governance charter, Zhao--Cui paper/source anchors. |
| Primary pass criterion | P69 master/runbook/Phase 0 result and Phase 1 subplan converge under local skeptical audit and Claude review, with all current gaps listed and no forbidden claim emitted. |
| Veto diagnostics | Missing holdout/replay gap; missing degree-ladder failure; adaptive parity language without anchors; d18 correctness claim; scaling or HMC readiness claim; detached execution; later phase allowed without subplan/review. |
| Explanatory diagnostics | File-existence checks, text checks, P68 status, review findings, dirty-worktree scope. |
| Not concluded | No code repair, no validation pass, no paper-scale reproduction, no HMC readiness, no formal proof certification. |
| Artifact preserving result | `docs/plans/bayesfilter-highdim-zhao-cui-p69-phase0-governance-claim-boundary-result-2026-06-15.md`. |

## Forbidden Claims And Actions

- Do not implement code in Phase 0.
- Do not run adjacent ladders in Phase 0.
- Do not run HMC, GPU, or long experiments in Phase 0.
- Do not claim d18 correctness or HMC readiness.
- Do not call the fixed branch source-faithful adaptive Zhao--Cui.
- Do not treat Claude as an execution authority.
- Do not launch detached or background supervisors.

## Exact Next-Phase Handoff Conditions

Phase 0 may hand off to Phase 1 only if:

- P69 planning artifacts exist and pass local text checks;
- local skeptical audit finds no material launch blocker, or all blockers are
  visibly patched;
- Claude review returns `VERDICT: AGREE`;
- Phase 0 result records the claim boundary and remaining gaps;
- Phase 1 subplan is drafted or refreshed and reviewed for consistency.

## Stop Conditions

Stop and write a blocker result if:

- the master program cannot consistently separate fixed-HMC adaptation from
  adaptive source-faithful reproduction;
- the P68 holdout/replay gap or degree-ladder failure is missing from the plan;
- Claude review does not converge after five rounds for the same blocker;
- a required source artifact is missing and cannot be replaced by a reviewed
  blocker;
- continuing would require GPU/HMC/long-run approval not covered by Phase 0.

## Planned Local Commands

These are read-only or document-only checks:

```bash
test -f docs/plans/bayesfilter-highdim-zhao-cui-p69-remaining-gaps-master-program-2026-06-15.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p69-visible-gated-execution-runbook-2026-06-15.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p69-visible-execution-ledger-2026-06-15.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p69-claude-review-ledger-2026-06-15.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p69-visible-stop-handoff-2026-06-15.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p69-phase0-governance-claim-boundary-subplan-2026-06-15.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p69-phase1-holdout-replay-design-subplan-2026-06-15.md
rg -n "holdout|degree-ladder|fixed_hmc_adaptation|adaptive Zhao|HMC readiness|d18 correctness|detached" docs/plans/bayesfilter-highdim-zhao-cui-p69-*.md
```

No GPU or long-running command is planned for Phase 0.
