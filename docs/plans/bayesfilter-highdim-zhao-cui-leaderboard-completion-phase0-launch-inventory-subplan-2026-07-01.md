# Phase 0 Subplan: Launch Inventory And Fail-Closed Zhao-Cui Contract

Date: 2026-07-01

Status: `DRAFT_REVIEW_READY`

## Phase Objective

Freeze the Zhao-Cui-only leaderboard completion contract, inventory current row
statuses, and verify that the program can represent analytical-score,
value-only, and precise-blocker outcomes without using SGQF or autodiff
shortcuts.

## Entry Conditions Inherited From Previous Phase

- User requested a master program, phase subplans, Claude review to convergence
  or max five rounds, a visible gated overnight runbook, and launch.
- SGQF repair is explicitly out of this program because another agent owns it.
- Current leaderboard artifacts are expected at
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
  and `.md`.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-master-program-2026-07-01.md`.
- Visible overnight runbook:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-visible-gated-overnight-execution-runbook-2026-07-01.md`.
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-claude-review-ledger-2026-07-01.md`.
- Visible execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-visible-execution-ledger-2026-07-01.md`.
- Stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-visible-stop-handoff-2026-07-01.md`.
- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase0-launch-inventory-result-2026-07-01.md`
- Refreshed Phase 1 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase1-sv-ksc-score-subplan-2026-07-01.md`.

## Required Checks, Tests, Reviews

- Local structural check that required plan/runbook/subplan files exist.
- Current leaderboard Zhao-Cui row inventory.
- Scan new artifacts for required subplan sections.
- Schema/state representability check that the current leaderboard and planned
  artifacts can distinguish `executed_value_score`, `executed_value_only`,
  and precise `blocked_or_status_only` Zhao-Cui outcomes without using SGQF or
  autodiff as an analytical-score shortcut.
- Exact artifact-path check for the baseline:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`,
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`,
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase1-route-protocol-inventory-result-2026-06-22.md`,
  and `docs/plans/bayesfilter-highdim-zhao-cui-p91-reset-memo-2026-06-29.md`.
- Check that the master/runbook encode trusted-context GPU/XLA rules before
  any later GPU/XLA phase can launch.
- Source-anchor gate check: master/runbook/phase contracts must fail closed on
  any source-faithfulness claim without exact Zhao-Cui paper/source anchors.
- Claude read-only review of master program, runbook, and this Phase 0
  subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the Zhao-Cui-only completion program safe to launch without mixing SGQF work, admitting autodiff as analytical score, or hiding real evaluator gaps? |
| Baseline/comparator | Exact artifacts `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`, `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`, `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase1-route-protocol-inventory-result-2026-06-22.md`, and `docs/plans/bayesfilter-highdim-zhao-cui-p91-reset-memo-2026-06-29.md`. |
| Primary criterion | Program files exist, phase gates are explicit, Zhao-Cui gaps are inventoried, and schema/state checks prove admitted, value-only, and blocked Zhao-Cui outcomes are representable without SGQF or autodiff shortcuts. Claude review may veto or request repairs, but it is not itself evidence of correctness. |
| Veto diagnostics | Missing stop conditions, SGQF phase work inside Zhao-Cui program, autodiff admitted as analytical, no source-anchor gate for source-faithfulness, no GPU trusted-context rule, no per-phase result/handoff protocol. |
| Explanatory diagnostics | Counts of admitted/value-only/blocked Zhao-Cui cells, dirty worktree status. |
| Not concluded | No code correctness, score correctness, full leaderboard completion, GPU readiness, HMC readiness, or production readiness. |
| Artifact | Phase 0 result and updated ledgers. |

## Forbidden Claims And Actions

- Do not claim any remaining Zhao-Cui row is fixed in Phase 0.
- Do not edit implementation code in Phase 0.
- Do not run GPU, HMC, package, network, or long benchmark commands.
- Do not claim source-faithfulness without cited paper/source anchors.
- Do not treat Claude agreement as authority to cross product/scientific
  boundaries.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 if:

- master/runbook/Phase 0 subplan converge under Claude review or require only
  non-material notes;
- local structural checks pass;
- source-faithfulness claims are gated by exact paper/source anchors or are
  classified as non-source-faithful manual adapters/extensions/blockers;
- Phase 0 result records current Zhao-Cui row statuses and precise Phase 1
  entry conditions.

## Stop Conditions

Stop if:

- Claude and Codex do not converge after five total Phase 0 launch-review
  rounds, regardless of whether the blockers differ;
- any required launch artifact, baseline artifact, or required subplan section
  is missing, unreadable, or section-incomplete;
- the program cannot isolate Zhao-Cui work from SGQF work;
- the leaderboard/result schema cannot represent admitted, value-only, and
  precise-blocker Zhao-Cui outcomes without admitting autodiff;
- the master/runbook do not encode trusted-context GPU/XLA rules;
- source-faithfulness is not fail-closed on missing/partial/conflicting
  Zhao-Cui paper/source anchors;
- required human approval is needed for a boundary not already authorized.

## End-of-Subplan Protocol

1. Run the required local checks.
2. Write the Phase 0 result / close record.
3. Draft or refresh the Phase 1 subplan.
4. Review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
