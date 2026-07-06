# P00 Program Review And Launch Gate Subplan

Date: 2026-06-23

Status: `READY_FOR_LOCAL_CHECKS_AND_CLAUDE_REVIEW`

## Phase Objective

Validate that the master program, visible gated execution runbook, ledgers, and
P01 subplan are internally consistent, feasible, artifact-complete, and safe to
launch.

## Entry Conditions Inherited From Previous Phase

No previous phase.  Required inherited state:

- P09D result exists and shows `SVD_CORE_REPAIR_DID_NOT_RESCUE`.
- Promotion runbook remains blocked before P10 under broad policy.
- Codex is supervisor/executor; Claude is read-only reviewer.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-master-program-2026-06-23.md`
- Visible execution runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-visible-gated-execution-runbook-2026-06-23.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-claude-review-ledger-2026-06-23.md`
- Visible execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-visible-execution-ledger-2026-06-23.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-visible-stop-handoff-2026-06-23.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p00-program-review-result-2026-06-23.md`

## Required Checks, Tests, Reviews

- Local file-existence and required-section check using `rg`.
- Claude Opus max read-only review of path list and review targets, not whole
  file pasted into the prompt.
- If Claude does not respond, run a small Claude probe.  If the probe responds,
  redesign the review prompt.  If the probe fails, write a blocker record.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the repair program safe and complete enough to launch visible gated execution? |
| Baseline/comparator | Project AGENTS policy, visible-gated template, P09D result, and promotion runbook blocker. |
| Primary pass criterion | Local checks pass and Claude review ends with `VERDICT: AGREE` within five rounds. |
| Veto diagnostics | Missing required sections, detached execution authority, Claude treated as execution authority, missing stop conditions, or unsupported default/scientific claims. |
| Explanatory diagnostics | Review comments, local check output, dirty worktree context. |
| Not concluded | No algorithm repair, no default readiness, no scientific validity. |
| Artifacts | P00 result plus Claude review ledger/log. |

## Forbidden Claims And Actions

- Do not claim Nystrom is repaired.
- Do not launch GPU diagnostics in P00.
- Do not use detached `overnight_gated_launch.sh`.
- Do not ask Claude to edit files or run experiments.
- Do not proceed if review convergence fails.

## Exact Next-Phase Handoff Conditions

Advance to P01 only if:

- P00 result records local checks passed.
- Claude review converged with `VERDICT: AGREE`.
- P01 subplan exists and has been refreshed after review.
- Visible execution ledger records `P00 PASSED`.

## Stop Conditions

- Any required file missing after one repair attempt.
- Claude/Codex review non-convergence after five rounds for same blocker.
- Claude unavailable and small probe fails.
- Human approval required for a boundary not anticipated by the master program.

## End-Of-Subplan Required Actions

1. Run required local checks.
2. Write P00 result/close record.
3. Draft or refresh P01 subplan.
4. Review P01 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
