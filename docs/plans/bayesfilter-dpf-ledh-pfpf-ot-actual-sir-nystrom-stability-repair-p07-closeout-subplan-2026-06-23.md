# P07 Closeout Handoff Subplan

Date: 2026-06-23

Status: `READY_FOR_CLOSEOUT`

## Phase Objective

Close the stability repair program with a clear decision, artifacts, nonclaims,
and next human or automated action.

## Entry Conditions Inherited From Previous Phase

- P06 failed with `FAIL_PAIRED_THRESHOLD_AFTER_FINITE_RESCUE`.
- The first required P06 row, `rank=32,epsilon=0.25`, was finite and
  residual-valid under `positive_projected`, but failed paired max
  log-likelihood threshold.
- P09/P10 must not be reopened from this repair result.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p07-closeout-result-2026-06-23.md`
- Updated visible stop handoff.
- Updated stop handoff stating `REPAIR_FAILED_OR_BLOCKED`.
- Promotion runbook update only if needed to preserve the blocked P09/P10
  status; do not mark P09/P10 reopened.

## Required Checks, Tests, Reviews

- Local artifact-existence check.
- Claude read-only review of final decision only if the closeout attempts to
  reopen P09/P10 or change default/promotion status.  This closeout keeps the
  blocked status, so local review is sufficient unless a consistency check
  fails.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What did the repair program establish, and what remains blocked? |
| Baseline/comparator | All completed phase results and promotion runbook. |
| Primary pass criterion | Final handoff accurately separates finite numerical rescue from paired-comparability repair failure and preserves blocked P09/P10 status. |
| Veto diagnostics | Unsupported default claim, missing artifact, stale status, or failure to distinguish candidate failure from research-direction failure. |
| Explanatory diagnostics | Phase summaries and review trail. |
| Not concluded | No claims beyond completed evidence. |
| Artifacts | P07 result, handoff, runbook update, review ledger. |

## Forbidden Claims And Actions

- Do not promote default policy.
- Do not reopen P09/P10.
- Do not present `FIXED_POLICY_ONLY_RECOMMENDED` as default readiness, broad
  robustness, or promotion evidence; it is only a blocked-region handoff unless
  a later reviewed promotion gate passes.
- Do not hide failed rows.
- Do not start a new experimental phase without a new subplan.

## Exact Next-Phase Handoff Conditions

No next phase in this master program.  Handoff must state one of:

- `REPAIR_PASSED_READY_FOR_REVIEWED_P09_RERUN`
- `FIXED_POLICY_ONLY_RECOMMENDED`
- `REPAIR_FAILED_OR_BLOCKED`
- `HUMAN_DECISION_REQUIRED`

The expected outcome for this program is `REPAIR_FAILED_OR_BLOCKED`.

## Stop Conditions

- Artifact mismatch.
- Claude/Codex final-decision non-convergence after five rounds.

## End-Of-Subplan Required Actions

1. Run required local checks.
2. Write P07 result/close record.
3. Refresh visible stop handoff.
4. Review final handoff for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
