# W2-0 Subplan: Coordinator Launch Packet And Review

Date: 2026-06-19
Master program:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-coordinator-master-program-2026-06-19.md`

## Phase Objective

Create and review the Wave 2 launch packet: coordinator master program,
current-agent positive-feature lane program, peer-agent low-rank handoff
status, visible gated runbook, review packet, and first executable current-lane
subplan.

## Entry Conditions Inherited From Previous Phase

- Wave 1 coordinator merge is complete.
- Wave 2 algorithm-complete structure exists.
- The user clarified that Codex/current agent owns positive-feature Sinkhorn
  and peer agent owns low-rank coupling solver-route validation.
- No active request changes the two-agent structure.

## Required Artifacts

- Coordinator master program.
- This W2-0 subplan.
- W2-0 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-p00-coordinator-launch-packet-result-2026-06-19.md`
- Current-agent master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-master-program-2026-06-19.md`
- Current-agent status:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-positive-feature-status-2026-06-19.md`
- Peer-agent low-rank status, read-only for this phase:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-status-2026-06-19.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-visible-gated-execution-runbook-2026-06-19.md`
- Review packet:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-launch-review-packet-2026-06-19.md`
- Review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-claude-review-ledger-2026-06-19.md`
- W2-1 subplan.

## Required Checks, Tests, And Reviews

Local checks:

```bash
python -m py_compile docs/benchmarks/scalable_ot_wave2_positive_feature_diagnostics.py tests/test_wave2_positive_feature_diagnostics.py
rg -n "Agent A|Agent B|Agent C|Agent D|Agent E|best|superior|beats|faster|production-ready|HMC-ready|default-ready" docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-*.md
```

Review:

- Codex skeptical audit before launch.
- Claude Opus max-effort read-only review of the compact launch packet.
- If Claude returns `VERDICT: REVISE`, patch material issues and rerun focused
  review, max five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the Wave 2 launch packet coherent, boundary-safe, and executable without mid-lane synthesis? |
| Baseline/comparator | User's seven-point prompt, Wave 2 structure, global/project agent policy, and visible runbook template. |
| Primary pass criterion | Required artifacts exist; local planning checks pass or only show deliberate forbidden-claim negations; Claude review converges to `VERDICT: AGREE`; W2-1 subplan is ready. |
| Veto diagnostics | Wrong lane assignment, mid-lane merge dependency, missing stop condition, write-set collision, unsupported claim, whole-file Claude prompt requirement, or unapproved boundary crossing. |
| Explanatory diagnostics | Existing peer-agent low-rank closeout status and prior Phase 5 positive-feature result. |
| Not concluded | No algorithm result, no ranking, no default selection, no speedup/posterior/HMC/API/production readiness, no dense equivalence. |
| Artifact preserving result | W2-0 result and Claude review ledger. |

## Forbidden Claims And Actions

- Do not execute positive-feature diagnostics before W2-0 review passes.
- Do not edit peer-agent low-rank artifacts except coordinator-owned status
  references.
- Do not send whole files to Claude.
- Do not claim any algorithm is better, faster, default-ready, HMC-ready,
  production-ready, posterior-correct, or dense-equivalent.

## Exact Next-Phase Handoff Conditions

W2-1 may begin only if:

- W2-0 local checks pass or findings are documented as allowed negations;
- Claude launch review returns `VERDICT: AGREE`;
- W2-0 result exists;
- W2-1 subplan exists and passes Codex consistency review;
- no human-required boundary is open.

## Stop Conditions

Stop and write a blocker result if:

- Claude review does not converge after five rounds for the same blocker;
- the plan requires package installs, network, GPU evidence, external solvers,
  public API/default/export changes, or shared schema/baseline edits;
- the lane assignment cannot be made unambiguous;
- a required check fails and cannot be repaired within coordinator/current-lane
  owned files.

## End-Of-Phase Checklist

1. Run required local checks.
2. Write W2-0 result.
3. Draft or refresh W2-1 subplan.
4. Review W2-1 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
