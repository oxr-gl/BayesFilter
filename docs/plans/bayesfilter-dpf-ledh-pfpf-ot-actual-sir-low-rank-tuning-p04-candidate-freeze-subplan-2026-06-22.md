# P04 Candidate Freeze Subplan

Status: `DRAFT_AFTER_P03`

## Phase Objective

Freeze one or more tuned low-rank candidates before any held-out support rows
are run, preserving the boundary between tuning and promotion evidence.

## Entry Conditions Inherited From Previous Phase

P03 must nominate at least one candidate with exact parameters, tuning artifacts,
and no unresolved hard-veto/schema issue.

## Required Artifacts

- Frozen candidate record:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p04-frozen-candidates-2026-06-22.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p04-candidate-freeze-result-2026-06-22.md`
- Required Claude review:
  recorded in `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-claude-review-ledger-2026-06-22.md`

## Required Checks/Tests/Reviews

- Confirm frozen parameters are exactly reproducible from P03 artifacts.
- Confirm freeze eligibility follows the P03 deterministic rule and records the
  aggregate log-likelihood mean absolute delta, max absolute delta, rank, warm
  median, and parameter tuple used for tie-breaking.
- Confirm the number of frozen candidates follows the P03 deterministic rule:
  exactly two if the fastest-candidate key selects a candidate different from
  the first selected candidate; otherwise exactly one.
- Confirm held-out support seeds/shapes are not the sole tuning selection rows.
- Confirm no threshold changes or post-hoc criteria edits were introduced.
- Claude read-only review of the freeze record and P05 handoff, recorded in the
  review ledger with `VERDICT: AGREE`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the candidate frozen before held-out evidence, with enough provenance to prevent tuning/promotion leakage? |
| Baseline/comparator | P03 tuning aggregate and master fixed gates. |
| Primary pass criterion | Frozen candidate record states exact parameters, tuning evidence role, held-out row plan, nonclaims, no post-hoc gate changes, and Claude review recorded in the review ledger with `VERDICT: AGREE`. |
| Veto diagnostics | Missing exact parameter, selection basis inconsistent with the P03 deterministic rule, missing Claude review ledger entry, missing `VERDICT: AGREE`, held-out leakage, criteria changes after seeing P03, or unsupported claim language. |
| Explanatory diagnostics | Tuning row metrics that motivated freeze. |
| Not concluded | No held-out support, speedup, posterior correctness, HMC readiness, default readiness, or statistical ranking. |
| Artifact | Frozen candidate record, P04 result, and Claude review ledger entry. |

## Forbidden Claims/Actions

- Do not use freeze as promotion.
- Do not change gates after P03 results.
- Do not add route-repair changes in P04.
- Do not run held-out support before the freeze record exists and is reviewed.

## Exact Next-Phase Handoff Conditions

Advance to P05 only if the frozen candidate record is complete and
Claude-reviewed with `VERDICT: AGREE` recorded in the review ledger, and P05
lists exact held-out rows, seeds, GPU policy, commands, logs, and pass/fail
criteria.

## Stop Conditions

- Stop as `NO_FREEZE_CANDIDATE` if P03 did not nominate a candidate.
- Stop if selection depends on post-hoc threshold changes.
- Stop after five unresolved Claude review rounds for the same freeze blocker.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the P04 phase result.
3. Draft or refresh P05 with frozen parameters and held-out commands.
4. Review P05 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
