# Phase 3 Result: KSC SV Same-Target Adapter And Score

Date: 2026-07-06

Status: `BLOCK_PHASE3_KSC_LEDH_ADAPTER_MISSING`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Do not admit any KSC LEDH value or score row yet. The repo contains same-target KSC value/score routes for fixed-SGQF, principal-square-root UKF, and Zhao-Cui fixed-branch TT, but no dedicated KSC LEDH adapter surface exists in the current GPU/XLA runner. |
| Primary criterion status | Passed by precise blocker: the KSC row target is clear, the existing non-LEDH same-target routes are clear, and the absence of a KSC-specific LEDH route in the current runner is explicit. |
| Veto diagnostic status | Passed: no actual-SV callback was reused as KSC proof, no KSC support was claimed by analogy alone, and no autodiff score was promoted as LEDH admission evidence. |
| Main uncertainty | Whether a future KSC LEDH route should be a dedicated mixture-aware flow adapter or whether the row should remain non-LEDH for leaderboard purposes. |
| Next justified action | Advance to Phase 4 predator-prey with the KSC boundary preserved: KSC has same-target non-LEDH comparators, but still no current LEDH adapter. |
| What is not concluded | No KSC LEDH value admission, no KSC LEDH score admission, no HMC readiness, and no claim that non-LEDH KSC score success implies LEDH support. |

## Question Answered

Phase 3 asked:

- Can BayesFilter execute the KSC row with an actual KSC-specific same-target
  LEDH scalar and a no-tape total derivative of that scalar?

Answer:

- Not under the current runner.

The repo does contain same-target KSC routes, but they are:

- fixed-SGQF;
- principal-square-root UKF;
- Zhao-Cui fixed-branch TT.

The repo does not contain:

- a `_dpf_ksc_callbacks(...)` surface;
- a `KSC_ROW` branch in the current LEDH callback routing;
- a reviewed current GPU/XLA LEDH adapter for the KSC surrogate row.

So Phase 3 closes by precise blocker:

- KSC LEDH adapter missing.

## Evidence

KSC row contract is real and separate:

- The source-scope contract preserves
  `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` as its own declared KSC
  Gaussian-mixture surrogate row:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`

Same-target non-LEDH KSC routes exist:

- The July 3 two-lane leaderboard artifact records executed KSC value/score
  rows for:
  - fixed-SGQF;
  - principal-square-root UKF;
  - Zhao-Cui fixed-branch TT.
- Their target contracts are explicitly KSC-surrogate compatible:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json`
- The leaderboard code exposes:
  - `fixed_sgqf_independent_panel_ksc_mixture`
  - `principal_sqrt_ukf_independent_panel_ksc_mixture`
  - `zhao_cui_ksc_mixture_fixed_branch_tt`
  in `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`

Current LEDH runner has no KSC branch:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py` defines
  `KSC_ROW`, but the current DPF callback routing does not provide a KSC LEDH
  callback surface.
- `_dpf_route(...)` routes LGSSM, actual SV, predator-prey, fixed spatial SIR,
  and generalized SV, but not `KSC_ROW`.
- No `_dpf_ksc_callbacks(...)` implementation exists in the current runner.

Current governance already says the same thing:

- The July 3 row-admission inventory keeps KSC blocked as
  `no reviewed KSC LEDH row adapter`:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-adapter-inventory-result-2026-07-03.md`
- The July 3 nonlinear adapter inventory likewise keeps KSC non-LEDH only:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase5-nonlinear-adapter-admission-result-2026-07-03.md`
- `tests/test_ledh_score_memory_n10000.py` still enforces:
  `blocked_no_ledh_ksc_row_adapter`

Why Phase 3 is a cleaner blocker than before:

- Phase 2 clarified that transformed-SV family language must be precise.
- That makes it easier to say plainly that KSC already has same-target
  non-LEDH routes, but LEDH support is still absent.

## Plain Scientific Classification

KSC is not blocked because the row target is unclear.

KSC is blocked because:

1. the row target is clear;
2. non-LEDH same-target routes already exist;
3. the current LEDH runner simply has no KSC-specific adapter surface.

Therefore:

- KSC LEDH row admission: blocked;
- reason: missing KSC-specific LEDH adapter, not target ambiguity.

## Required Checks Run

```bash
rg -n "ksc|gaussian_mixture_surrogate|blocked_no_ledh_ksc_row_adapter|same-target" docs/plans docs/benchmarks bayesfilter tests
```

Result: passed; the KSC row contract, existing same-target non-LEDH routes, and
the explicit blocked LEDH status were all located.

```bash
git diff --check -- docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase3-ksc-sv-same-target-result-2026-07-05.md docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase4-predator-prey-same-target-subplan-2026-07-05.md docs/plans/bayesfilter-ledh-highdim-row-score-admission-visible-execution-ledger-2026-07-05.md docs/reviews/ledh-highdim-row-score-admission-phase3-review-bundle-2026-07-06.md
```

Result: pending until this phase close patch is complete, then rerun.

## Evidence Contract Result

| Field | Status |
| --- | --- |
| Question | Answered directly: no current KSC-specific LEDH adapter exists in the runner. |
| Baseline/comparator | Passed: row contract, July 3 adapter inventory, KSC non-LEDH leaderboard cells, and current runner code agree. |
| Primary criterion | Passed by blocker: the missing LEDH surface is explicit. |
| Veto diagnostics | Passed: no analogical promotion and no callback reuse. |
| Explanatory diagnostics | Existing KSC SGQF/UKF/Zhao-Cui score routes remain useful evidence for the KSC row itself, but not for LEDH admission. |
| Not concluded | No KSC LEDH repair or score admission. |

## Next-Phase Handoff

Phase 4 should proceed as written:

- predator-prey remains a separate same-target adapter question;
- KSC remains blocked specifically because LEDH support is missing;
- no KSC result should be borrowed into predator-prey or generalized-SV work.
