# P35 Phase Subplans Claude Review Ledger

metadata_date: 2026-06-04

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports," Foundations of Computational Mathematics, 2022.

what_is_not_concluded:
- This ledger does not approve production implementation.
- Claude review does not certify mathematical correctness.
- The phase subplans do not themselves run numerical validation.

## Review Scope

Review the P35 phase subplans:

```text
docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase0-design-contract-subplan-2026-06-04.md
docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase1-basis-tt-algebra-subplan-2026-06-04.md
docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase2-squared-density-transport-subplan-2026-06-04.md
docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase3-fixed-branch-fitting-subplan-2026-06-04.md
docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase4-filtering-value-path-subplan-2026-06-04.md
docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase5-fixed-branch-derivatives-subplan-2026-06-04.md
docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase6-stress-performance-subplan-2026-06-04.md
docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-phase7-public-api-decision-subplan-2026-06-04.md
```

## Iteration 1

Claude verdict: `FAIL`.

Codex classification summary: all findings `ACCEPT`.

| Severity | Claude finding | Codex classification | Patch |
|---|---|---|---|
| BLOCKER | Parent plan allowed top-level exports by Phase 5, contradicting subplans' Phase 7-only API decision. | ACCEPT | Patched parent P35 plan to prohibit top-level exports in Phases 0--6 and allow public API decision only in Phase 7. |
| MAJOR | Deterministic replay was not gated for HMC-facing score use. | ACCEPT | Added repeated same seed/config replay gates to Phase 3 fit, Phase 4 value/retained marginal, Phase 5 score, Phase 6 stress, and Phase 7 API criteria. |
| MAJOR | Phase 4 lacked recursive non-identity coordinate/reference-map filtering test. | ACCEPT | Added exact small-model recursive fixture with non-identity affine map and non-uniform reference measure, including retained marginal and next-step measure checks. |

No disputed findings remain after iteration 1.

## Iteration 2

Claude verdict: `PASS`.

Scope: re-review after iteration-1 patches.

| Checked item | Status |
|---|---|
| Public API exposure consistently deferred to Phase 7 only. | PASS |
| Deterministic replay gates present for fit, value/retained marginal, score, stress, and API decision. | PASS |
| Recursive non-identity affine map plus non-uniform reference filtering gate present in Phase 4. | PASS |

Final review status: no new blocker or major findings remain for the P35 phase
subplans.
