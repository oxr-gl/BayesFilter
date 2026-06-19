# W4-0 Subplan: Launch Packet And Review

Date: 2026-06-20
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-master-program-2026-06-20.md`

## Phase Objective

Create and review the Wave 4 launch packet, including master program, phase
subplans, current-lane validation harness, tests, visible runbook, peer-lane
handoff structure, and Claude review packet.

## Entry Conditions Inherited From Previous Phase

- Wave 3 completed with both candidate lanes passing a common deterministic
  smoke and no ranking.
- Wave 2 candidate artifacts remain diagnostic-only entry evidence.
- User requested a Wave 4 master program, dedicated subplans, Claude review up
  to convergence or max five rounds, visible gated runbook, and launch.

## Required Artifacts

- Wave 4 master program.
- W4-0 subplan and result.
- W4-1/W4-2/W4-3 subplans.
- Current-lane validation harness:
  `docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py`
- Current-lane focused tests:
  `tests/test_wave4_positive_feature_validation.py`
- Review packet:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-launch-review-packet-2026-06-20.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-claude-review-ledger-2026-06-20.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-visible-gated-execution-runbook-2026-06-20.md`
- Execution ledger and stop handoff.

## Required Checks, Tests, And Reviews

Local checks:

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py tests/test_wave4_positive_feature_validation.py
pytest -q tests/test_wave4_positive_feature_validation.py::test_wave4_positive_feature_smoke_contract
rg -n "best|superior|beats|faster|production-ready|HMC-ready|default-ready" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-*.md docs/benchmarks/scalable_ot_wave4_positive_feature_validation.py tests/test_wave4_positive_feature_validation.py
```

Review:

- Codex skeptical audit before launch.
- Claude Opus max-effort compact read-only review.
- If Claude returns `VERDICT: REVISE`, patch material issues and rerun focused
  checks/review, max five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the Wave 4 launch packet coherent, boundary-safe, and executable as an independent-lane replicated downstream hard screen? |
| Baseline/comparator | Wave 2 final merge, Wave 3 result, project/global policy, and visible runbook template. |
| Primary pass criterion | Required artifacts exist; local checks pass or text scan hits are only explicit forbidden-claim negations; Claude review returns `VERDICT: AGREE`; W4-1 subplan is ready. |
| Veto diagnostics | Hidden ranking, missing hard veto, unsupported claim, missing stop condition, invalid comparator, whole-file Claude prompt requirement, one-agent execution of both algorithm lanes, or unapproved boundary crossing. |
| Explanatory diagnostics | Existing Wave 2/Wave 3 metrics and local text scan hits. |
| Not concluded | No algorithm result, no ranking, no default selection, no speedup/posterior/HMC/API/production readiness, no dense equivalence. |
| Artifact preserving result | W4-0 result and Claude review ledger. |

## Forbidden Claims And Actions

- Do not run W4-1 diagnostics before W4-0 review passes.
- Do not execute the peer low-rank lane in the current-agent lane.
- Do not edit Phase 1 baseline, Phase 3 schema, public exports/defaults, or
  unrelated dirty files.
- Do not claim ranking, speedup, posterior correctness, HMC/API readiness,
  production/default readiness, dense equivalence, or broad scalable-OT
  selection.

## Exact Next-Phase Handoff Conditions

W4-1 peer handoff may begin only if:

- local W4-0 checks pass;
- Claude launch review returns `VERDICT: AGREE`;
- W4-0 result exists;
- W4-1 peer handoff subplan exists and passes Codex consistency review;
- no human-required boundary is open.

## Stop Conditions

Stop and write blocker result if review does not converge after five rounds,
checks fail and cannot be repaired within Wave-4-owned files, or execution
requires unapproved package/network/GPU/public/default/shared-schema boundary.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write W4-0 result.
3. Draft or refresh W4-1 subplan.
4. Review W4-1 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
