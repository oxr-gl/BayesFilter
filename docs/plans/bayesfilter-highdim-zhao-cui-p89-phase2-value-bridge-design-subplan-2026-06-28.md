# P89 Phase 2 Subplan: Same-Target Source-Backed Value Bridge Design

Date: 2026-06-28

Status: `REVIEWED_READY_FOR_PHASE2_VALUE_BRIDGE_DESIGN`

Reviewed by bounded read-only Claude Opus max-effort review on 2026-06-28 with
`VERDICT: AGREE`.

## Phase Objective

Design, or explicitly block, a same-target source-backed value bridge for the
exact P89 target manifest. Phase 2 is a bridge-design phase only. It may inspect
documents, local code, tests, and author-source anchors. It must not execute the
bridge, run TensorFlow/Python experiments, implement derivatives, run FD, run
HMC/GPU/XLA, or claim correctness.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result is reviewed closed.
- The target manifest is reviewed:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-target-manifest-2026-06-28.md`.
- Inherited label remains:
  `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE`.
- `D18_CORRECTNESS_CANDIDATE` remains blocked until Phase 3 value-bridge
  validation passes under a reviewed execution subplan.
- Source-route full-history analytical derivative readiness remains blocked.
- Gradient, FD, HMC, GPU/XLA, production, and final promotion phases remain
  blocked behind the value bridge.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase2-value-bridge-design-result-2026-06-28.md`
- Value bridge manifest or blocker section inside the Phase 2 result.
- Refreshed Phase 3 value-bridge validation subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase3-value-bridge-validation-subplan-2026-06-28.md`
- Updated execution ledger, Claude review ledger, and stop handoff.

If a bridge is designed, the bridge manifest must include:

- exact target manifest path and status;
- exact scalar field list;
- same-branch and retained-object requirements;
- source-backed reference route or author-source bridge anchors;
- value comparison tolerances;
- allowed runtime command shape for Phase 3, if any;
- pass/fail criteria and veto diagnostics;
- nonclaims.

If no bridge can be designed, the result must state `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING` and refresh Phase 3 as a no-runtime blocker closeout.

## Required Checks/Tests/Reviews

Phase 2 is document/code/source audit only. Allowed checks:

```bash
rg -n "same-target|reference bridge|source-backed|D18_CORRECTNESS_CANDIDATE|missing_same_target_reference_or_bridge|target_id|source_route_sequential_negative_log_physical_density|source_route_previous_marginal_log_density|eval_pdf|eval_irt|marginalise|full_sol" docs/plans/bayesfilter-highdim-zhao-cui-p83*.md docs/plans/bayesfilter-highdim-zhao-cui-p86*.md docs/plans/bayesfilter-highdim-zhao-cui-p87*.md docs/plans/bayesfilter-highdim-zhao-cui-p88*.md docs/plans/bayesfilter-highdim-zhao-cui-p89*.md bayesfilter/highdim/source_route.py tests/highdim third_party/audit/zhao_cui_tensor_ssm_p10/source -g '*.md' -g '*.py' -g '*.m'
rg -n "P89_TARGET_MANIFEST|same-scalar|same scalar|branch identity|retained object|tolerance|BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING|Phase 3" docs/plans/bayesfilter-highdim-zhao-cui-p89*.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p89*.md
```

Claude Opus max-effort read-only review is required for the Phase 2 result and
refreshed Phase 3 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is there a same-target source-backed value bridge that can validate the exact P89 target scalar against a reference with pinned tolerances? |
| Baseline/comparator | P89 target manifest, P88 missing-bridge blocker, local source-route code, tests, prior P83/P86/P87/P88 bridge attempts, and author source anchors. |
| Primary criterion | A bridge design is admissible only if it is same-target, source-backed, tolerance-pinned, same-branch aware, executable only in Phase 3, and separates diagnostics from correctness. Otherwise Phase 2 must block. |
| Veto diagnostics | Wrong target; local proxy substituted for source-backed reference; UKF/all-grid/LEDH/rank/degree/holdout/ESS evidence treated as correctness; missing tolerances; missing branch/retained-object binding; runtime execution in Phase 2; source-faithful claim without paper and author-source anchors. |
| Explanatory diagnostics | Inventory of candidate bridges, missing fields, source anchors, and why candidates pass or fail admissibility. |
| Not concluded | No correctness candidate, posterior correctness, gradient readiness, FD validation, HMC/GPU/production readiness, LEDH agreement, scale readiness, or default-policy change. |
| Artifact | Phase 2 result, bridge manifest or blocker, refreshed Phase 3 subplan, ledgers, stop handoff. |

## Forbidden Claims/Actions

- Do not claim `D18_CORRECTNESS_CANDIDATE`.
- Do not claim value correctness, posterior correctness, gradient correctness,
  derivative readiness, FD validation, HMC readiness, GPU/XLA readiness,
  production readiness, or default-policy readiness.
- Do not run TensorFlow/JAX/PyTorch/Python experiment commands, tests, bridge
  execution, HMC/sampler, GPU/CUDA, production benchmark, package/network, or
  default-policy commands.
- Do not modify algorithmic code.
- Do not accept rank/degree, validation/holdout, ESS, replay, UKF, all-grid,
  LEDH, or local fixed-branch diagnostics as a source-backed bridge unless the
  bridge is same-target, source-backed, and tolerance-pinned.
- Do not let Claude authorize runtime or scientific-claim crossing.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only if:

- Phase 2 result receives Claude `VERDICT: AGREE`;
- refreshed Phase 3 subplan receives Claude `VERDICT: AGREE`;
- if a bridge exists, Phase 2 records a bridge manifest with exact source
  anchors, tolerances, branch requirements, commands, pass/fail criteria, and
  nonclaims;
- if no bridge exists, Phase 2 records `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING`
  and Phase 3 is refreshed as no-runtime blocker closeout;
- stop handoff records whether Phase 3 is execution validation or blocker
  closeout.

## Stop Conditions

- No same-target source-backed bridge candidate can be specified.
- Required source anchors or tolerances cannot be provided.
- Bridge design would require treating a proxy as correctness.
- Local checks fail and cannot be repaired within document/code/source audit.
- Claude review does not converge after five rounds for the same blocker.
- Continuing would require runtime execution, algorithmic edits, GPU/HMC,
  package/network, default-policy, destructive git/filesystem, or unrelated
  dirty-worktree changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write the Phase 2 result / close record.
3. Include either a value bridge manifest or explicit blocker.
4. Draft or refresh the Phase 3 validation/blocker subplan.
5. Review the Phase 2 result and Phase 3 subplan for consistency,
   correctness, feasibility, artifact coverage, and boundary safety.
