# Phase B4 Subplan: Closeout And Decision

Date: 2026-06-18

## Phase Objective

Synthesize B0-B3 results into a final Agent B independent-review decision and
write the program handoff.

## Entry Conditions Inherited From Previous Phase

- B3 produced review JSON/Markdown artifacts and a phase result.
- Any material findings have been classified as Agent B-owned repair,
  Agent A-owned revise, or blocker.
- Claude read-only review has converged for material review-result questions,
  or a blocker has been recorded after the allowed loop budget.

## Required Artifacts

- Phase B4 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p04-closeout-decision-result-2026-06-18.md`
- Parent-required standalone Agent B review result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-nystrom-independent-review-result-2026-06-18.md`
- Updated visible execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-visible-execution-ledger-2026-06-18.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-visible-stop-handoff-2026-06-18.md`

## Required Checks, Tests, And Reviews

Local checks:

- confirm B0-B3 result artifacts exist;
- confirm review JSON/Markdown exist;
- confirm the standalone parent-required review result exists and is consistent
  with the B4 closeout status;
- confirm final status is consistent with B3 finding severities;
- confirm no forbidden claims appear in B4 result text.

Review:

- Claude read-only review is required for the final B4 decision if the result
  is `AGREE` or if it asks Agent A to revise.  Use a compact summary with
  status, finding counts, artifact paths, and non-claims.  Do not send whole
  files.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is Agent B's final independent-review decision on Agent A Phase 11 artifacts? |
| Baseline/comparator | B0-B3 results and Agent A Phase 11 artifacts. |
| Primary pass criterion | B4 decision accurately reflects prior phase evidence, preserves non-claims, and provides a safe next handoff. |
| Veto diagnostics | Missing prior result, final status inconsistent with findings, unsupported claim, or unresolved material blocker. |
| Explanatory diagnostics | Finding severities, residual risks, Claude review status, commands run, artifacts produced. |
| Not concluded | No speedup, no production/default readiness, no posterior correctness, no HMC readiness, no ranking, and no broad scalable-OT decision. |
| Artifact preserving result | B4 result, standalone parent-required review result, ledger, stop handoff, Claude review note if used. |

## Forbidden Claims And Actions

- Do not choose a BayesFilter default.
- Do not claim Nystrom is best, fastest, posterior-correct, HMC-ready, or
  production-ready.
- Do not edit Agent A-owned artifacts in the initial independent review pass.
- Do not change thresholds after seeing B3 results.

## Exact Next-Phase Handoff Conditions

There is no next Agent B phase in this program.  Final handoff must state one
of:

- Agent A artifacts receive Agent B `AGREE`;
- Agent A artifacts need Agent A revision with specific findings;
- Agent B review is blocked and needs human direction.

The standalone parent-required review result must use one of:

- `PHASE_11_NYSTROM_INDEPENDENT_REVIEW_AGREE`;
- `PHASE_11_NYSTROM_INDEPENDENT_REVIEW_REVISE`;
- `PHASE_11_NYSTROM_INDEPENDENT_REVIEW_BLOCKED_WAITING_FOR_AGENT_A_ARTIFACTS`.

## Stop Conditions

Stop with `PHASE_B4_AGENT_B_CLOSEOUT_BLOCKED` if final status cannot be made
consistent with the phase evidence or if Claude/Codex do not converge after
five review rounds on the same material final-decision blocker.

## End-Of-Phase Protocol

At phase end:

1. Run the required local checks.
2. Write the B4 phase result / close record.
3. Refresh the stop handoff.
4. Review the final handoff for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
