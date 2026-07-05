# Phase 2 Subplan: Target / Truth / Source-Scope Contract Freeze

Date: 2026-06-29

## Status

`REVIEWED_CONTRACT_FREEZE_SUBPLAN_CLOSED`

## Phase Objective

Freeze the exact Generalized-SV row identity, target family, truth/test-point
convention, oracle/evaluator distinction, route classes, and forbidden
substitutes before any implementation or promotion work begins.

## Entry Conditions Inherited From Previous Phase

- Phase 1 has reviewed and preserved the fresh-agent reset memo and authority
  order.
- The active row remains
  `zhao_cui_generalized_sv_synthetic_from_estimated_values`.
- The reviewed upstream anchors remain:
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-generalized-sv-prior-mean-amendment-result-2026-06-12.md`
  - `docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md`
- No source-row SGQF evaluator is yet admitted.
- No score, derivative, HMC, benchmark, or leaderboard promotion work is
  authorized yet.

## Required Artifacts

- Target / truth / source-scope contract:
  `docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md`
- Generalized-SV testing specification:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md`
- Prior-mean amendment result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-generalized-sv-prior-mean-amendment-result-2026-06-12.md`
- Native dense-reference result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md`
- Phase 2 result:
  `docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-result-2026-06-29.md`
- Refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-subplan-2026-06-29.md`
- Visible execution ledger:
  `docs/plans/bayesfilter-generalized-sv-visible-execution-ledger-2026-06-29.md`
- Claude review ledger:
  `docs/plans/bayesfilter-generalized-sv-claude-review-ledger-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
test -f docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md
test -f docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md
test -f docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-generalized-sv-prior-mean-amendment-result-2026-06-12.md
test -f docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md
test -f docs/plans/bayesfilter-generalized-sv-visible-execution-ledger-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-claude-review-ledger-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-result-2026-06-29.md
test -f docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-subplan-2026-06-29.md
rg -n "zhao_cui_generalized_sv_synthetic_from_estimated_values|prior-mean|SP500|oracle|source-row SGQF evaluator|blocked or precursor-only|forbidden substitutes|KSC" docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-generalized-sv-prior-mean-amendment-result-2026-06-12.md docs/plans/bayesfilter-highdim-zhao-cui-p51-m2-native-generalized-sv-reference-result-2026-06-09.md
git diff --check -- docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-subplan-2026-06-29.md docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-result-2026-06-29.md docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-subplan-2026-06-29.md docs/plans/bayesfilter-generalized-sv-visible-execution-ledger-2026-06-29.md docs/plans/bayesfilter-generalized-sv-claude-review-ledger-2026-06-29.md
```

Required read-only Claude reviews:

- target / truth / source-scope contract,
- Phase 2 result,
- refreshed Phase 3 subplan.

No implementation, evaluator runtime, benchmark, leaderboard mutation, score,
derivative, HMC, GPU/CUDA, package/network, release, CI, or default-policy
command is authorized in Phase 2.

## Skeptical Plan Audit

| Risk Checked | Phase 2 Control |
| --- | --- |
| Wrong baseline | Phase 2 freezes the reviewed testing specification, prior-mean amendment result, and native dense-reference result as explicit upstream anchors for the contract. |
| Proxy metric promoted | Contract freeze is document authority only; it does not admit any evaluator or same-target pass by itself. |
| Missing stop condition | The contract preserves explicit vetoes for wrong target identity, wrong truth/test point, native/source-row blending, and precursor-as-promotion drift. |
| Unfair comparison | The contract separates actual-SV, KSC surrogate SV, native generalized-SV dense oracle, and source-row SGQF routes. |
| Hidden assumption | SP500 remains source-estimation input only; it is not benchmark observation data. The native dense reference remains oracle only; it is not the source-row evaluator. |
| Stale context | Phase 2 inherits the Phase 1 authority order and may not let older historical artifacts or implementation surfaces silently rewrite identity semantics. |
| Environment mismatch | Phase 2 is document/source-inventory only. No runtime evidence is created. |
| Artifact-answer mismatch | Phase 2 must close with a reviewed contract result and refreshed Phase 3 subplan; a contract file alone is insufficient. |

Audit status: passed if the contract remains identity-explicit, preserves the
oracle/evaluator split, and does not accidentally admit the SGQF source-row
evaluator.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the Generalized-SV contract unambiguously freeze the governing row, target family, truth/test-point convention, oracle/evaluator split, route classes, and forbidden substitutes for the governed program? |
| Baseline/comparator | Phase 1 reviewed authority package, generalized-SV testing specification, prior-mean amendment result, and native dense-reference result. |
| Primary criterion | The contract and Phase 2 result preserve exact row identity, synthetic prior-mean truth/test-point convention, SP500 input-role limits, route classes, and explicit non-admission of the source-row SGQF evaluator. |
| Veto diagnostics | wrong row id, actual-SV/generalized-SV confusion, KSC promoted as same-target generalized-SV evidence, native oracle/source-row blending, wrong truth/test point, or accidental SGQF evaluator admission. |
| Explanatory diagnostics | keyword/anchor coverage, contract vocabulary, and cross-artifact consistency notes. |
| Not concluded | No SGQF source-row evaluator admission, no same-target value pass, no score admission, no HMC readiness, no production readiness, and no leaderboard promotion. |
| Artifact | `docs/plans/bayesfilter-generalized-sv-phase2-target-truth-source-scope-contract-result-2026-06-29.md` plus refreshed `docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-subplan-2026-06-29.md`. |

## Forbidden Claims/Actions

- Do not claim the contract itself proves same-target equality.
- Do not claim the native dense reference executes the benchmark row.
- Do not use actual-SV or KSC evidence as generalized-SV same-target evidence.
- Do not change the prior-mean truth/test-point convention or SP500 input role.
- Do not authorize runtime, benchmark, evaluator, score, derivative, HMC,
  GPU/CUDA, package/network, release, CI, or default-policy work.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only if:

- the target / truth / source-scope contract receives Claude `VERDICT: AGREE`;
- the Phase 2 result receives Claude `VERDICT: AGREE`;
- the refreshed Phase 3 subplan receives Claude `VERDICT: AGREE`;
- the execution ledger records Phase 2 as reviewed closed with preserved
  non-admission language for the source-row SGQF evaluator.

## Stop Conditions

- The contract conflicts with the reviewed testing specification or prior-mean
  amendment result.
- The contract blurs the native dense oracle with the source-row evaluator.
- The contract silently promotes a precursor route into admission.
- Local document checks fail and cannot be repaired within document scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require runtime, benchmark, evaluator, GPU/CUDA,
  package/network, release, CI, default-policy, destructive git/filesystem, or
  unrelated dirty worktree changes.

## End-Of-Phase Requirements

1. Run the required document/source-inventory checks.
2. Write the Phase 2 result.
3. Refresh the Phase 3 subplan.
4. Review the contract, Phase 2 result, and refreshed Phase 3 subplan.
5. Update the execution ledger and Claude review ledger.
