# P57-M7 Source-Faithful Rank And UKF Calibration Result

metadata_date: 2026-06-11
status: PASS
phase: P57-M7

## Decision

`PASS_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION`

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | How should rank be selected for the fixed TT/SIRT source route, and where can UKF help without becoming a false comparator? |
| Baseline/comparator | Author SIR setup in `eg3_sir/mainscript.m:37-56`, especially `max_rank=40`, `init_rank=20`, `kick_rank=5`; P56 source-anchor audit; P52/P53 rank/UKF artifacts as scout/preflight only. |
| Primary criterion | Implemented a P57 source-rank policy that selects ranks only from fixed TT/SIRT source-route comparator evidence. UKF is accepted only with `scout_not_truth`; old local/operator `R_eff` evidence is rejected as source-faithful rank evidence. |
| Veto diagnostics | Old P52/P53 `R_eff` route cannot enter `P57RankComparatorEvidence`; UKF cannot promote stronger than `scout_not_truth`; no-comparator evidence blocks; largest-rank self-promotion is forbidden by policy. |
| Not concluded | No d=18 spatial SIR filtering success, no d=50/d=100 correctness, no HMC readiness, and no TT/SIRT fitting quality claim. |

## Implementation

Touched source files:

- `bayesfilter/highdim/rank_budget.py`
- `bayesfilter/highdim/__init__.py`

Added tests:

- `tests/highdim/test_p57_m7_source_faithful_rank_ukf_calibration.py`

Key implementation points:

- `P57_AUTHOR_SIR_D18_RANK_LADDER = (10, 20, 40)` records the author d=18 rank ladder anchor.
- `P57_FIXED_TTSIRT_MEMORY_TERMS` requires TT cores, mass contractions, CDF/KR state, sample batches, autodiff workspace, and retained objects.
- `P57RankComparatorEvidence` accepts only `route_class="fixed_ttsirt_source_route"`.
- `p57_select_source_faithful_rank(...)` selects the smallest feasible rank that passes dense lower-rung or same-route-higher-rank comparator tolerances.
- If no dense or higher-rank comparator exists, the result is `BLOCK_P57_M7_RANK_COMPARATOR_MISSING`.
- If comparator evidence exists but tolerances fail, the result is `BLOCK_P57_M7_RANK_TOLERANCE_FAILURE`.
- Gradient evidence, when available, must satisfy directional cosine `>= 0.995` and relative score error `<= 5e-2`.
- UKF enters only via `ukf_claim_class="scout_not_truth"` and cannot certify correctness or final rank.

## Promotion Tolerances

| Quantity | Tolerance |
| --- | --- |
| Per-observation log-likelihood error | `<= 1e-3` |
| Filtered mean scaled RMSE | `<= 5e-2` |
| Covariance relative Frobenius error | `<= 1e-1` |
| Replay residual | `<= 0.0` |
| Gradient directional cosine, if reference exists | `>= 0.995` |
| Relative score error, if reference exists | `<= 5e-2` |

## Source Anchors

| Source claim | Anchor |
| --- | --- |
| Author SIR dimension/horizon and sample setup. | `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-17`, `:39-45` |
| Author rank controls for the SIR run. | `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:48-51` |
| Full source-route solve uses `full_sol(...); solve(...)`. | `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:53-56` |
| P56 demoted old local/operator route and `R_eff` rank budget for source-faithful claims. | `docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md` |

## Checks

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p57_m7_source_faithful_rank_ukf_calibration.py \
  tests/highdim/test_p52_ukf_scout.py \
  tests/highdim/test_p52_rank_budget.py \
  tests/highdim/test_p53_m5_rank_selection_integration.py
```

Result: `21 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/rank_budget.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p57_m7_source_faithful_rank_ukf_calibration.py
```

Result: passed.

```text
git diff --check -- \
  bayesfilter/highdim/rank_budget.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p57_m7_source_faithful_rank_ukf_calibration.py
```

Result: passed.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass M7 after Claude review. | Met: source-rank policy is fixed TT/SIRT comparator-based and UKF is diagnostic only. | No veto triggered in focused checks; old local/operator route evidence is rejected. | The policy is a gate, not evidence that a spatial SIR rank has passed on data. | M8 should implement/check preconditioned Algorithm 5 route. | d=18/d=50/d=100 spatial SIR success and HMC readiness. |

## Nonclaims

- This does not certify adaptive TT-cross parity.
- This does not certify S&P 500 reproduction.
- This does not implement smoothing.
- This does not run the d=18 spatial SIR ladder.
- This does not make UKF a correctness oracle or final rank selector.
