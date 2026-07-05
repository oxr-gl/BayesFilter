# P90 Phase 4 Subplan: Source-Route Derivative-Carry Design

Date: 2026-06-28

Status: `LOCKED_PENDING_PHASE3_VALUE_BRIDGE_PASS`

## Phase Objective

Design derivative-carry data structures and source-backed operation ownership
for the exact same scalar, branch, retained objects, and setup-static fields
that passed the value bridge.

## Entry Conditions Inherited From Previous Phase

- Phase 3 value bridge reviewed pass.
- `D18_CORRECTNESS_CANDIDATE` may be nominated only if Phase 3 allowed it.
- The derivative design must use the same scalar and branch as Phase 3.

## Required Artifacts

- Derivative manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-derivative-carry-manifest-2026-06-28.md`
- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase4-derivative-carry-design-result-2026-06-28.md`
- Refreshed Phase 5 implementation subplan.
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase5-derivative-implementation-subplan-2026-06-28.md`

## Required Checks/Tests/Reviews

Allowed checks before implementation:

```bash
rg -n "source_route_previous_marginal_log_density|source_route_generate_retained_samples|source_route_sequential_negative_log_physical_density|eval_irt_reference|eval_rt_jac_reference|marginalise|AbstractIRT|normalizer|branch" docs/plans/bayesfilter-highdim-zhao-cui-p89*.md docs/plans/bayesfilter-highdim-zhao-cui-p90*.md bayesfilter/highdim/source_route.py third_party/audit/zhao_cui_tensor_ssm_p10/source -g '*.md' -g '*.py' -g '*.m'
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

Claude review is required for the derivative manifest, Phase 4 result, and
Phase 5 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What derivative objects and source-backed operations are required to differentiate the exact same scalar that passed Phase 3? |
| Baseline/comparator | Phase 3 passed value bridge, P89 derivative inventory, local source-route code, and author TTSIRT derivative anchors. |
| Primary criterion | Every scalar component has an explicit derivative owner, source/local classification, carry field, branch identity binding, and test plan. |
| Veto diagnostics | Missing previous-marginal derivative owner, missing proposal correction derivative, missing normalizer derivative, branch mismatch, fixed-branch/autodiff evidence promoted, or value bridge weakened. |
| Explanatory diagnostics | Component table and source-anchor inventory. |
| Not concluded | No derivative implementation or gradient correctness. |
| Artifact | Derivative manifest, Phase 4 result, and refreshed Phase 5 subplan. |

## Forbidden Claims/Actions

- Do not implement derivatives in Phase 4.
- Do not run FD, HMC, GPU/CUDA, production, packaging, CI, release, or default-
  policy commands.
- Do not claim source-route analytical-gradient readiness.
- Do not use JVP/autodiff/fixed-branch evidence as source-route derivative
  readiness.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only if:

- derivative manifest receives Claude `VERDICT: AGREE`;
- Phase 4 result receives Claude `VERDICT: AGREE`;
- Phase 5 subplan receives Claude `VERDICT: AGREE`;
- the derivative manifest binds the same value-bridge scalar and branch.

## Stop Conditions

- A derivative owner cannot be specified for a scalar component.
- Source anchors are insufficient for a source-route claim.
- The design requires changing the Phase 3 scalar or branch.
- Claude review does not converge after five rounds.
- Continuing would require unreviewed implementation/runtime/GPU/HMC/package/
  default-policy/destructive/unrelated-dirty-work changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 4 result / close record.
3. Draft or refresh Phase 5 subplan.
4. Review Phase 5 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
