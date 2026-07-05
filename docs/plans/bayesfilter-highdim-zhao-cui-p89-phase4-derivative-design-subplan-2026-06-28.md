# P89 Phase 4 Subplan: Diagnostic Source-Route Derivative Design Inventory

Date: 2026-06-28

Status: `REVIEWED_READY_FOR_PHASE4_DIAGNOSTIC_DERIVATIVE_DESIGN`

## Phase Objective

Inventory and refine the source-route analytical derivative design gaps under
the unresolved value-bridge blocker. Phase 4 is diagnostic/design-only. It may
classify derivative components and draft future implementation requirements,
but it must not implement derivatives, run FD, run runtime checks, or promote
source-route analytical-gradient readiness.

## Entry Conditions Inherited From Previous Phase

- Phase 3 result records `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING`.
- `D18_CORRECTNESS_CANDIDATE` remains blocked.
- Phase 2 result is reviewed closed:
  `P89_PHASE2_REVIEWED_BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING_CLOSED`.
- Phase 3 result and this Phase 4 subplan receive bounded Claude
  `VERDICT: AGREE`.
- P89 target manifest remains reviewed:
  `P89_TARGET_MANIFEST_REVIEWED_AGREE`.
- Source-route full-history analytical derivative readiness remains blocked by
  P88 Phase 5 and cannot be promoted in Phase 4.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase4-derivative-design-result-2026-06-28.md`
- Derivative design inventory or explicit blocker section inside the Phase 4
  result.
- Refreshed Phase 5 derivative implementation subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p89-phase5-derivative-implementation-subplan-2026-06-28.md`
- Updated execution ledger, Claude review ledger, and stop handoff.

If Phase 4 produces a future implementation design, the design must still
record that it is non-promotional until a value bridge replacement closes
`BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING`.

## Required Checks/Tests/Reviews

Phase 4 is document/code/source audit only. Allowed checks:

```bash
rg -n "P89_PHASE3.*BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING|BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING|P88_PHASE5_REVIEWED_BLOCK_SOURCE_ROUTE_DERIVATIVE_READINESS_CLOSED|source-route full-history analytical derivative readiness|source_route_previous_marginal_log_density|source_route_generate_retained_samples|source_route_sequential_negative_log_physical_density|source_route_run_sequential_fixed_hmc|eval_irt_reference|eval_rt_jac_reference|marginalise|AbstractIRT" docs/plans/bayesfilter-highdim-zhao-cui-p88*.md docs/plans/bayesfilter-highdim-zhao-cui-p89*.md bayesfilter/highdim/source_route.py third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src -g '*.md' -g '*.py' -g '*.m'
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p89*.md
```

Claude Opus max-effort read-only review is required for the Phase 4 result and
refreshed Phase 5 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What source-route analytical derivative gaps remain, and can a future implementation design be specified without weakening the missing value-bridge blocker? |
| Baseline/comparator | P89 Phase 3 value-bridge blocker, P89 target manifest, P88 Phase 5 derivative blocker, local source-route code, and author TTSIRT derivative/marginalization anchors. |
| Primary criterion | Phase 4 may pass only as diagnostic/design inventory: it must preserve missing value bridge and derivative readiness blockers, classify source-backed vs local components, and define or block future implementation requirements. |
| Veto diagnostics | Derivative readiness promoted; value bridge blocker weakened; JVP/autodiff/fixed-branch evidence promoted as source-route derivative correctness; implementation/FD/HMC/GPU/production authorized; source-faithful claim without anchors. |
| Explanatory diagnostics | Component classification, source anchors, local code surfaces, missing derivative-carry paths, and future implementation requirements. |
| Not concluded | No value correctness, gradient correctness, analytical-gradient readiness, FD validation, HMC/GPU/production readiness, LEDH agreement, scale readiness, or default-policy change. |
| Artifact | Phase 4 result, derivative design inventory/blocker, refreshed Phase 5 subplan, ledgers, stop handoff. |

## Forbidden Claims/Actions

- Do not claim `D18_CORRECTNESS_CANDIDATE`.
- Do not claim value correctness, posterior correctness, gradient correctness,
  source-route analytical-gradient readiness, FD validation, HMC readiness,
  GPU/XLA readiness, production readiness, or default-policy readiness.
- Do not run TensorFlow/JAX/PyTorch/Python experiment commands, tests,
  derivative implementation, FD validation, HMC/sampler, GPU/CUDA, production
  benchmark, package/network, or default-policy commands.
- Do not modify algorithmic code.
- Do not weaken, omit, or rephrase away `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING`.
- Do not treat local fixed-branch, JVP, ForwardAccumulator, reverse-mode, or FD
  evidence as source-route analytical derivative readiness.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only if:

- Phase 4 result receives Claude `VERDICT: AGREE`;
- refreshed Phase 5 subplan receives Claude `VERDICT: AGREE`;
- Phase 4 result preserves `BLOCK_SOURCE_ROUTE_VALUE_BRIDGE_MISSING`;
- Phase 4 result preserves that source-route full-history analytical
  derivative readiness remains blocked unless the result explicitly records a
  non-promotional implementation design;
- Phase 5 is either blocked/no-runtime closeout or explicitly labeled
  diagnostic implementation scaffolding that cannot promote readiness before a
  value bridge replacement exists.

## Stop Conditions

- Phase 3 blocker is not reviewed or is materially revised.
- Required derivative component anchors cannot be classified.
- A proposed derivative design would weaken the missing value-bridge blocker.
- Local checks fail and cannot be repaired within document/code/source audit.
- Claude review does not converge after five rounds for the same blocker.
- Continuing would require runtime execution, algorithmic edits, GPU/HMC,
  package/network, default-policy, destructive git/filesystem, or unrelated
  dirty-worktree changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write the Phase 4 result / close record.
3. Include derivative design inventory or explicit blocker.
4. Draft or refresh the Phase 5 derivative implementation subplan.
5. Review the Phase 4 result and Phase 5 subplan for consistency,
   correctness, feasibility, artifact coverage, and boundary safety.
