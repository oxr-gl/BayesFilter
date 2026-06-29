# Phase 3 Subplan: Code/Test/Benchmark Boundary Audit

Date: 2026-06-29

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Classify every relevant actual-SV code path, test surface, and benchmark artifact
as same-target, surrogate, diagnostic-only, KSC-only, or blocked pending new
derivation, so later implementation/rewrite work cannot drift by inertia.

## Entry Conditions Inherited From Previous Phase

- Phase 2 reconciliation has passed.
- The single-target contract is the active scalar authority.
- No route-decision or validation phase has started.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase2-derivation-chapter-reconciliation-result-2026-06-29.md`
- Phase 3 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase3-code-test-benchmark-boundary-audit-result-2026-06-29.md`
- Refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-actual-sv-single-target-phase4-route-decision-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
rg -n "exact transformed|same-target|Gaussian-closure|not exact transformed same-target admission|KSC|lane_id|target" bayesfilter/highdim/sv_mixture_cut4.py tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/test_actual_sv_two_lane_benchmark_script.py docs/benchmarks/benchmark_actual_sv_two_lane_comparison.py
git diff --check -- docs/plans/bayesfilter-actual-sv-single-target-phase3-*.md
```

Claude review is required for:

- the Phase 3 result,
- the route-classification table,
- the Phase 4 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which current code, test, and benchmark artifacts are same-target actual-SV evidence, and which are surrogate/diagnostic/KSC-only or blocked? |
| Baseline/comparator | single-target contract, derivation/chapter reconciliation result, and live repo code/test/benchmark surfaces. |
| Primary criterion | Every relevant surface is classified exactly once and the classification matches the governing contract. |
| Veto diagnostics | any unclassified surface; same-target label on Gaussian-closure route; KSC blended into actual-SV same-target evidence; tests that certify the wrong scalar; benchmark rows that imply co-equal targets. |
| Explanatory diagnostics | wrapper names, target strings, benchmark schema fields, and historical comments. |
| Not concluded | No implementation decision, no validation outcome, no gradient pass. |
| Artifact | Phase 3 result with route-inventory manifest. |

## Forbidden Claims/Actions

- Do not rewrite tests or benchmarks in this phase; classify first.
- Do not treat historical labels as authoritative if current diagnostics contradict them.
- Do not allow “useful surrogate” to be rewritten as “same-target.”

## Exact Next-Phase Handoff Conditions

Phase 4 may start only if:

- every relevant surface has a route class;
- the route-inventory manifest is reviewed;
- the Phase 4 subplan exists and is reviewed.

## Stop Conditions

- A relevant surface cannot be classified without first changing the governing contract.
- The code path and the benchmark/test path disagree materially about the route class.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run the local route-inventory checks.
2. Write the Phase 3 result with a full classification table.
3. Refresh the Phase 4 subplan.
4. Review the classification result and next subplan.
