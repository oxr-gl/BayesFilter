# P90 Phase 1 Subplan: Same-Target Value Bridge Contract

Date: 2026-06-28

Status: `REVIEWED_READY_FOR_PHASE1_VALUE_BRIDGE_CONTRACT_DESIGN`

## Phase Objective

Design a same-target source-backed value bridge contract for the exact P89/P90
Zhao-Cui SIR d18 scalar. The contract must bind source anchors, same branch,
same retained objects, basis/rank/samples/schedules, parameterization, and
pinned tolerances before any implementation or execution.

## Entry Conditions Inherited From Previous Phase

- Phase 0 reviewed result preserves P89 blockers.
- P89 target manifest is the active target unless a reviewed manifest revision
  is written.
- `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING` remains open until this phase
  produces a reviewed bridge manifest.
- No runtime bridge execution has occurred.

## Required Artifacts

- Bridge contract/manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-value-bridge-contract-2026-06-28.md`
- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase1-value-bridge-contract-result-2026-06-28.md`
- Refreshed Phase 2 implementation subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase2-value-bridge-implementation-subplan-2026-06-28.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
rg -n "target_id|same-scalar|branch identity|retained object|source_route_sequential_negative_log_physical_density|source_route_previous_marginal_log_density|source_route_generate_retained_samples|eval_pdf|eval_irt_reference|eval_rt_jac_reference|marginalise|full_sol|tolerance|BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING" docs/plans/bayesfilter-highdim-zhao-cui-p89*.md docs/plans/bayesfilter-highdim-zhao-cui-p90*.md bayesfilter/highdim/source_route.py third_party/audit/zhao_cui_tensor_ssm_p10/source -g '*.md' -g '*.py' -g '*.m'
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

Claude Opus max-effort read-only review is required for the bridge contract,
Phase 1 result, and Phase 2 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can P90 specify an admissible same-target source-backed value bridge for the exact Zhao-Cui SIR d18 scalar? |
| Baseline/comparator | P89 target manifest, P89 missing-bridge blocker, local source-route value mechanics, and author source anchors. |
| Primary criterion | A bridge contract passes only if it names the exact scalar, reference route, source anchors, branch/retained identity, setup-static fields, parameterization, deterministic cases, tolerances, and fail-closed rules. |
| Veto diagnostics | Wrong target, proxy correctness, missing tolerances, missing retained/branch binding, missing author source anchors, runtime execution, or unsupported source-faithful claim. |
| Explanatory diagnostics | Prior bridge blocker inventory, local code surface inventory, author route mechanics. |
| Not concluded | No value correctness, implementation correctness, gradient correctness, FD validation, HMC/GPU/production readiness, or default-policy change. |
| Artifact | Bridge contract manifest and Phase 1 result. |

## Forbidden Claims/Actions

- Do not execute bridge validation.
- Do not modify algorithmic code unless Phase 1 is explicitly revised and
  reviewed for implementation; default Phase 1 is design-only.
- Do not claim `D18_CORRECTNESS_CANDIDATE`.
- Do not claim value correctness.
- Do not use UKF, LEDH, all-grid, rank/degree, holdout, ESS, replay, FD, JVP,
  or fixed-branch local diagnostics as source-backed value correctness.
- Do not run runtime, GPU/CUDA, HMC, package/network, production, CI, release,
  or default-policy commands.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only if:

- bridge contract receives Claude `VERDICT: AGREE`;
- Phase 1 result receives Claude `VERDICT: AGREE`;
- Phase 2 subplan receives Claude `VERDICT: AGREE`;
- the contract either closes the design side of
  `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING` or explicitly records
  `P90_BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_CONTRACT_MISSING`.

If no admissible bridge contract can be written, Phase 1 writes a blocker
result and downstream phases become no-runtime blocker closeouts.

## Stop Conditions

- No source-backed same-target bridge can be specified.
- Source anchors are insufficient or ungrounded.
- Tolerances cannot be justified before seeing results.
- The contract requires a runtime command before implementation subplan review.
- Claude review does not converge after five rounds.
- Continuing would require unreviewed algorithmic edits, runtime/GPU/HMC,
  package/network, default-policy, destructive git/filesystem, or unrelated
  dirty-worktree changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 1 result / close record.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 2 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
