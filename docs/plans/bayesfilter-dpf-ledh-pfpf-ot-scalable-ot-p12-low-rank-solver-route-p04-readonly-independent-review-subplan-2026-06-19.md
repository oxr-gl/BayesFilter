# P12-4 Subplan: Read-Only Independent Review

Date: 2026-06-19

## Status

`DRAFT_PENDING_PHASE_P12_3_GATE_AND_CLAUDE_APPROVAL`

## Phase Objective

Run a bounded read-only review of the P12 lane artifacts for consistency,
source-route boundaries, artifact coverage, and claim safety.  Claude Opus may
act as read-only reviewer only after user approval; Codex remains supervisor
and execution authority.

## Entry Conditions Inherited From Previous Phase

- P12-3 closeout/status sync passed.
- All P12 artifacts are current.
- Claude Code review approval has been granted or the phase stops.

## Required Artifacts

- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-claude-review-ledger-2026-06-19.md`
- Independent review result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p04-readonly-independent-review-result-2026-06-19.md`

## Required Checks, Tests, And Reviews

- Codex read-only review of P12 implementation, tests, diagnostic script,
  JSON/Markdown, result, status, and source-route classifications.
- Claude read-only review using `claude_worker.sh --model opus --effort max`.
- Maximum five Claude rounds for the same material blocker.
- If Claude fails to respond, run a tiny read-only probe.  If the probe
  responds, redesign the prompt rather than treating Claude as unavailable.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do P12 artifacts support the final diagnostic-only status without unsupported source, claim, schema, or boundary drift? |
| Baseline/comparator | P12 master, Wave 1 coordinator, P12 replay artifacts, and source anchors by path/line. |
| Primary pass criterion | Codex and Claude converge on no material blockers, or all fixable P12-owned blockers are repaired and focused checks rerun. |
| Veto diagnostics | Unsupported source-faithfulness claim, missing anchor, schema drift, wrong baseline, proxy metric promoted, missing stop condition, write-boundary violation, or Claude review not read-only. |
| Explanatory diagnostics | Nonblocking wording findings, residual risks, review round count. |
| Not concluded | Claude agreement is not execution authority and does not authorize crossing shared-contract or scientific-claim boundaries. |

## Forbidden Claims And Actions

- Do not let Claude edit files, launch agents, run experiments, or authorize
  boundary crossings.
- Do not send whole files in the prompt; send bounded instructions and file
  paths for read-only inspection.
- Do not continue after five failed review rounds for the same blocker.

## Exact Next-Phase Handoff Conditions

Advance to P12-5 only if:

- read-only review ends in `VERDICT: AGREE`; or
- only nonblocking findings remain and Codex records why they do not block;
- all material P12-owned repairs have focused local checks.

## Stop Conditions

Stop if:

- Claude approval is absent;
- Claude review repeatedly fails and a small probe shows prompt/design failure
  that cannot be repaired;
- a material blocker requires shared contract changes or forbidden actions;
- five review rounds fail to converge on the same blocker.

## End-Of-Phase Protocol

At phase end:

1. run required local checks;
2. write the P12-4 result/close record;
3. draft or refresh the P12-5 subplan;
4. review the P12-5 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
