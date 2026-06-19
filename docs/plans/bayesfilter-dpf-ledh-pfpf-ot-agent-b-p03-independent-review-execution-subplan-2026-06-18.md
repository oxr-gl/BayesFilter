# Phase B3 Subplan: Independent Review Execution

Date: 2026-06-18

## Phase Objective

Run Agent B's independent review script against Agent A's Phase 11 artifacts,
write JSON/Markdown review artifacts, classify findings, and determine whether
Agent A's artifacts receive `AGREE`, `REVISE`, or `BLOCKED` from Agent B.

## Entry Conditions Inherited From Previous Phase

- B2 review script compiled and passed local coverage review.
- B1 independent tests passed or any remaining issue was classified as
  non-blocking for artifact review.
- Agent A artifacts remain read-only inputs.

## Required Artifacts

- Review JSON:
  `docs/benchmarks/scalable-ot-p11-nystrom-independent-review-2026-06-18.json`
- Review Markdown:
  `docs/benchmarks/scalable-ot-p11-nystrom-independent-review-2026-06-18.md`
- Phase B3 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p03-independent-review-execution-result-2026-06-18.md`
- Refreshed Phase B4 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-agent-b-p04-closeout-decision-subplan-2026-06-18.md`
- Parent-required final review note to be written in B4:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-nystrom-independent-review-result-2026-06-18.md`

## Required Checks, Tests, And Reviews

Local commands:

```bash
python docs/benchmarks/scalable_ot_p11_nystrom_independent_review.py \
  --agent-a-json docs/benchmarks/scalable-ot-p11-reduced-rank-nystrom-ladder-diagnostics-2026-06-18.json \
  --agent-a-result docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p11-reduced-rank-nystrom-ladder-result-2026-06-18.md \
  --output docs/benchmarks/scalable-ot-p11-nystrom-independent-review-2026-06-18.json \
  --markdown-output docs/benchmarks/scalable-ot-p11-nystrom-independent-review-2026-06-18.md
```

Then inspect the JSON/Markdown summary fields and classify findings by
severity.

Review:

- If B3 finds no material blockers, Claude read-only review should inspect a
  compact summary of the review result, not whole JSON.
- If B3 finds a material blocker in Agent B-owned artifacts, repair locally and
  rerun focused checks.
- If B3 finds a material blocker in Agent A-owned artifacts, write a revise
  result and stop or hand off.  Do not patch Agent A-owned files in this phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do Agent A's Phase 11 artifacts pass Agent B's independent artifact review? |
| Baseline/comparator | Agent A JSON/result against Phase 3 schema, Agent A plan, and Agent B plan. |
| Primary pass criterion | Review script exits successfully, writes JSON/Markdown artifacts, reports no blocker/high findings, and preserves non-claims. |
| Veto diagnostics | Script failure, unreadable Agent A artifacts, schema failure, missing fixtures/ranks, missing dense-reference fields, bad baseline prefix, unsupported claim, or Agent B mutation of Agent A files. |
| Explanatory diagnostics | Finding counts, warning counts, artifact coverage table, residual risks. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, or default readiness. |
| Artifact preserving result | Review JSON/Markdown, B3 result, ledger update, refreshed B4 subplan. |

## Forbidden Claims And Actions

- Do not edit Agent A files.
- Do not change Agent A pass/fail criteria after seeing results.
- Do not run GPU, network, package install, POT, external backend, or Agent A
  diagnostics.
- Do not claim default readiness, speedup, ranking, posterior correctness, HMC
  readiness, or public API readiness.

## Exact Next-Phase Handoff Conditions

Advance to B4 only if:

- B3 result status is one of:
  `PHASE_B3_AGENT_B_INDEPENDENT_REVIEW_AGREE` or
  `PHASE_B3_AGENT_B_INDEPENDENT_REVIEW_REVISE_AGENT_A`;
- review JSON and Markdown artifacts exist;
- B4 subplan is present and locally reviewed;
- B4 subplan preserves the parent-required final review note as a required
  closeout artifact.

## Stop Conditions

Stop with `PHASE_B3_AGENT_B_INDEPENDENT_REVIEW_BLOCKED` if review execution
cannot produce artifacts, requires Agent A mutation, or hits a human-required
boundary.

## End-Of-Phase Protocol

At phase end:

1. Run the required local checks.
2. Write the B3 phase result / close record.
3. Draft or refresh the B4 subplan.
4. Review the B4 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
