# W4-1 Subplan: Peer Low-Rank Lane Handoff

Date: 2026-06-20
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-master-program-2026-06-20.md`

## Phase Objective

Write a durable Markdown task note for the peer agent to execute the independent
low-rank coupling solver-route Wave 4 lane to completion before final merge.
This phase runs immediately after W4-0 so the peer lane can proceed in parallel
with the current-agent positive-feature lane.

## Entry Conditions Inherited From Previous Phase

- W4-0 launch review has passed local checks and Claude compact review.
- The peer lane is independent and must not consume current-lane intermediate
  artifacts as evidence.
- The final Wave 4 merge is not authorized until the peer lane writes its lane
  result and diagnostic artifacts.

## Required Artifacts

- Peer task note:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-peer-low-rank-task-note-2026-06-20.md`
- W4-1 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p01-peer-low-rank-handoff-result-2026-06-20.md`
- Current-lane subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p02-current-positive-feature-validation-subplan-2026-06-20.md`
- Draft/refreshed W4-3 final merge subplan.
- Updated execution ledger and stop handoff if peer artifacts are absent.

Expected peer artifacts:

- `docs/benchmarks/scalable_ot_wave4_low_rank_coupling_validation.py`
- `tests/test_wave4_low_rank_coupling_validation.py`
- `docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.json`
- `docs/benchmarks/scalable-ot-wave4-low-rank-coupling-validation-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-low-rank-coupling-result-2026-06-20.md`

## Required Checks, Tests, And Reviews

Local checks:

```bash
rg -n "current agent|peer agent|low-rank|forbidden|no ranking|no speedup claim|same fixture/seed grid|manifest" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-peer-low-rank-task-note-2026-06-20.md
test -f docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p02-current-positive-feature-validation-subplan-2026-06-20.md
test -f docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p03-final-merge-subplan-2026-06-20.md
```

Review:

- Codex consistency review of the peer note and final-merge entry conditions.
- Claude review only if the peer note changes evidence boundaries materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the peer-agent low-rank Wave 4 task note clear enough to let the peer execute independently and produce merge-ready artifacts on the same fixture/seed grid and artifact contract? |
| Baseline/comparator | Wave 4 master program, Wave 2 low-rank result, Wave 3 result, and the lane artifact contract. |
| Primary pass criterion | Peer note exists, states the exact ownership/write set/artifact contract/checks/nonclaims, requires the same fixture/seed grid as the current lane, requires run-manifest fields, and final merge subplan blocks until peer artifacts exist. |
| Veto diagnostics | Note tells peer to edit current-lane artifacts, uses new agent labels, permits ranking/default claims, omits hard vetoes, omits output artifact paths, omits run-manifest fields, permits a different fixture/seed grid without a blocker, or authorizes final merge before peer results. |
| Explanatory diagnostics | Text scan hits and final merge pending state. |
| Not concluded | No low-rank Wave 4 result, no comparison, no ranking, no default selection. |
| Artifact preserving result | Peer task note and W4-1 result. |

## Forbidden Claims And Actions

- Do not execute the low-rank lane in the current-agent phase.
- Do not copy chat instructions as the only coordination record.
- Do not launch additional agent labels beyond current agent and peer agent.
- Do not authorize final merge before peer lane artifacts exist.
- Do not allow peer-lane differences in fixture/seed grid or artifact contract
  to be silently repaired during final merge.

## Exact Next-Phase Handoff Conditions

W4-2 may begin only if:

- W4-1 peer task note exists;
- W4-1 local checks pass;
- W4-1 result exists;
- W4-2 current positive-feature subplan exists and passes Codex consistency
  review.

## Stop Conditions

Stop and write a blocker result if the peer note cannot be made boundary-safe
without changing the Wave 4 evidence contract or if writing the peer note would
require executing the peer algorithm lane in the current-agent process.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write W4-1 result.
3. Draft or refresh W4-2 subplan.
4. Review W4-2 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.

