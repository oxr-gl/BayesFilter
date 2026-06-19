# W3-0 Subplan: Launch Packet And Review

Date: 2026-06-19
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-master-program-2026-06-19.md`

## Phase Objective

Create and review the Wave 3 launch packet, including master program, phase
subplans, diagnostic harness, tests, visible runbook, and Claude review packet.

## Entry Conditions Inherited From Previous Phase

- Wave 2 final merge completed with both lanes diagnostic-only passed.
- No ranking/default/scientific claim is authorized from Wave 2.
- User requested Wave 3 plan, Claude review loop, visible runbook, and launch.

## Required Artifacts

- Wave 3 master program.
- W3-0 subplan and result.
- W3-1/W3-2/W3-3 subplans.
- Diagnostic harness:
  `docs/benchmarks/scalable_ot_wave3_downstream_smoke.py`
- Focused tests:
  `tests/test_wave3_downstream_smoke.py`
- Review packet:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-launch-review-packet-2026-06-19.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-claude-review-ledger-2026-06-19.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-visible-gated-execution-runbook-2026-06-19.md`
- Execution ledger and stop handoff.

## Required Checks, Tests, And Reviews

Local checks:

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave3_downstream_smoke.py tests/test_wave3_downstream_smoke.py
rg -n "best|superior|beats|faster|production-ready|HMC-ready|default-ready" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave3-*.md docs/benchmarks/scalable_ot_wave3_downstream_smoke.py tests/test_wave3_downstream_smoke.py
```

Review:

- Codex skeptical audit before launch.
- Claude Opus max-effort compact read-only review.
- If Claude returns `VERDICT: REVISE`, patch material issues and rerun focused
  checks/review, max five rounds for same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the Wave 3 launch packet coherent, boundary-safe, and executable as a no-ranking downstream smoke? |
| Baseline/comparator | Wave 2 final merge, Wave 2 JSON artifacts, project/global policy, and visible runbook template. |
| Primary pass criterion | Required artifacts exist; local checks pass or only hit explicit negations; Claude review returns `VERDICT: AGREE`; W3-1 subplan is ready. |
| Veto diagnostics | Hidden ranking, missing hard veto, unsupported claim, missing stop condition, invalid comparator, whole-file Claude prompt requirement, or unapproved boundary crossing. |
| Explanatory diagnostics | Existing Wave 2 metrics and local text scan hits. |
| Not concluded | No algorithm result, no ranking, no default selection, no speedup/posterior/HMC/API/production readiness, no dense equivalence. |
| Artifact preserving result | W3-0 result and Claude review ledger. |

## Forbidden Claims And Actions

- Do not run Wave 3 diagnostics before W3-0 review passes.
- Do not edit Phase 1 baseline, Phase 3 schema, public exports/defaults, or
  unrelated dirty files.
- Do not claim ranking, speedup, posterior correctness, HMC/API readiness,
  production/default readiness, dense equivalence, or broad scalable-OT
  selection.

## Exact Next-Phase Handoff Conditions

W3-1 may begin only if:

- local W3-0 checks pass;
- Claude launch review returns `VERDICT: AGREE`;
- W3-0 result exists;
- W3-1 subplan exists and passes Codex consistency review;
- no human-required boundary is open.

## Stop Conditions

Stop and write blocker result if review does not converge after five rounds,
checks fail and cannot be repaired within Wave-3-owned files, or execution
requires unapproved package/network/GPU/public/default/shared-schema boundary.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write W3-0 result.
3. Draft or refresh W3-1 subplan.
4. Review W3-1 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
