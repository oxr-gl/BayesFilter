# W2-2 Subplan: Final Coordinator Merge

Date: 2026-06-19
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-coordinator-master-program-2026-06-19.md`

## Phase Objective

Merge the final Wave 2 lane statuses after both algorithm-complete lanes close
or one true blocker is recorded.  The merge records lane viability under each
lane's own evidence contract and does not rank algorithms.

## Entry Conditions Inherited From Previous Phase

- W2-1 current-agent positive-feature lane is closed or blocked.
- Peer-agent low-rank lane has a final status/result or true blocker.
- No mid-lane synthesis is needed.

## Required Artifacts

- Peer-agent status/result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-status-2026-06-19.md`
  and
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-result-2026-06-19.md`
- Current-agent status/result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-status-2026-06-19.md`
  and
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-result-2026-06-19.md`
- Final merge result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-final-merge-result-2026-06-19.md`

## Required Checks, Tests, And Reviews

Local checks:

```bash
rg -n "LOW_RANK_COUPLING_VALIDATION_|POSITIVE_FEATURE_SINKHORN_" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-*-status-2026-06-19.md docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-*-result-2026-06-19.md
rg -n "best|superior|beats|faster|production-ready|HMC-ready|default-ready" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-final-merge-result-2026-06-19.md
```

Review:

- Codex skeptical audit before writing merge.
- Claude review optional unless the merge makes a nontrivial comparative
  decision beyond lane-status aggregation.  The default merge must not rank.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What final lane statuses are available after Wave 2 algorithm-complete execution? |
| Baseline/comparator | Lane final status/result artifacts only. |
| Primary pass criterion | Merge reads both final lane closeouts and records statuses, hard veto screens, non-claims, and next justified action without ranking. |
| Veto diagnostics | Missing lane final result, unsupported comparative/ranking/default claim, stale intermediate artifact use, or shared contract contradiction. |
| Explanatory diagnostics | Lane summary metrics from final artifacts only. |
| Not concluded | No algorithm ranking, no default selection, no speedup/posterior/HMC/API/production readiness, no dense equivalence, no broad scalable-OT selection. |
| Artifact preserving result | Wave 2 final merge result. |

## Forbidden Claims And Actions

- Do not rank low-rank coupling against positive-feature.
- Do not edit lane-owned implementation/test/diagnostic files.
- Do not infer default readiness or production readiness.
- Do not use descriptive dense-reference deltas, runtime, or memory as
  promotion criteria.

## Exact Next-Phase Handoff Conditions

No automatic next phase is launched from W2-2.  Any follow-on work requires a
new reviewed subplan.

## Stop Conditions

Stop and write a blocker result if:

- either final lane status/result is missing or internally inconsistent;
- a merge would require ranking or default selection without a reviewed
  comparative evidence contract;
- a shared contract contradiction appears.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write final merge result.
3. Do not draft an implementation subplan unless the user asks for follow-on
   work.
4. Record unresolved blockers and non-claims.
