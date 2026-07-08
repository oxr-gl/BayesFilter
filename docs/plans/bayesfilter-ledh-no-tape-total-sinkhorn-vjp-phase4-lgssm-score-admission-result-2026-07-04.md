# Phase 4 Result: LGSSM Same-Target Score Admission

Date: 2026-07-04

Status: `CLOSED_REVIEWED_PREFIX_SCORE_PASS_FULL_ROW_ADMISSION_BLOCKED`

## Phase Objective

Use the no-tape total transport VJP in the LGSSM LEDH route and test whether
the same-target leaderboard row can admit an LEDH score.

## Entry Conditions

- Phase 3 P8p SIR regression result was closed and reviewed.
- Phase 3/4 Claude review returned `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.

## Implementation Artifacts

- `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
  - Added opt-in `--score-mode manual-reverse`.
  - Added no-tape manual reverse scan for the LGSSM physical parameter vector
    `[phi1, phi2, phi3, q_scale, r_scale]`.
  - Added same-scalar finite-difference diagnostic and explicit
    value/score route metadata.
  - Preserved value-only default behavior unless score mode is requested.
- `tests/test_ledh_lgssm_manual_score_phase4.py`
  - Added same-scalar FD test for active streaming transport.
  - Added runtime no-autodiff sentinel test.
  - Added static source audit for the new manual score helpers.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does LEDH compute the total derivative of the same LGSSM LEDH scalar without tape? |
| Baseline/comparator | Same-scalar central finite difference for a fixed tiny prefix fixture. |
| Primary criterion | Local prefix route must be same-route, same-algorithm, no-tape, and FD-pass. |
| Veto diagnostics | Tape route; stopped partial derivative; value/score route mismatch; value/score transport mismatch; nonfinite score; FD mismatch. |
| Not concluded | Full T50 leaderboard score admission, GPU/XLA production score, HMC readiness, posterior correctness, runtime superiority. |

## Checks Run

CPU-only checks intentionally set `CUDA_VISIBLE_DEVICES=-1`.

| Command | Result |
| --- | --- |
| `python -m py_compile docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py` | pass |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_lgssm_manual_score_phase4.py` | pass: 3 tests |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_ledh_lgssm_manual_score_phase4.py tests/test_ledh_pfpf_ot_p7_manual_score.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py` | pass: 15 tests |
| `python -m json.tool docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-tiny-prefix-2026-07-04.json` | pass |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py ... --score-mode manual-reverse ...` | pass; refreshed the JSON after fixing stale nested score metadata |

## Numerical Result

Artifact:
`docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-tiny-prefix-2026-07-04.json`

Tiny prefix fixture:

- time steps: `2`;
- particles: `4`;
- seed: `81120`;
- device: CPU-hidden diagnostic;
- transport: streaming manual finite total VJP, `transport_ad_mode=full`;
- value/score route status: `same_route_value_score`;
- same-scalar FD status: `pass`;
- max absolute score error: `9.465646044759524e-09`;
- max relative score error: `8.792013654782173e-10`;
- parameter order: `[phi1, phi2, phi3, q_scale, r_scale]`;
- manual score:
  `[4.6517339713326, -2.2383309550434705, 0.6785225994442738, 8.17939757825367, 10.766186687265593]`.

## Bug Found And Fixed

The first local diagnostic failed for the three `phi` components while
`q_scale` and `r_scale` matched finite differences.  The cause was a plain
reduction bug in the initial-particle `phi` chain rule: the contribution was
reduced over both particle and state axes, then reused for all three `phi`
components.  The correct calculation reduces over particles only, preserving
one contribution per state coordinate.

After that fix, both no-resampling and active streaming-transport tiny prefix
diagnostics passed same-scalar finite differences.

## Decision Table

| Decision | Primary Criterion Status | Veto Status | Main Uncertainty | Next Justified Action | Not Concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 4 locally as prefix score pass but keep full row blocked | pass for tiny prefix | no local prefix veto found | Full T50 GPU/XLA material score has not run | Phase 5 closeout / decide whether to add a full-row GPU score gate | Full leaderboard score admission, HMC readiness |

## Nonclaims

- This is not a full T50 leaderboard score admission.
- This is not trusted GPU/XLA material score evidence.
- This is not a claim that LEDH score equals the exact Kalman score; it is a
  total derivative of the LEDH-PFPF-OT scalar.
- This is not HMC readiness.

## Phase 5 Handoff

Phase 5 may close the no-tape total VJP program only as a local prefix score
success with full-row admission still blocked, unless a later trusted GPU/XLA
full-row score gate is explicitly added and passed.

## Read-Only Review

The user explicitly approved sending the bounded Phase 4/5 review bundle and
referenced fixed-path BayesFilter artifacts to Claude Code for read-only review
despite the external data-disclosure risk.

- Review result: `REVIEW_STATUS=agreed`, `VERDICT=AGREE`
- Review run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-114127-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-phase5`
- Review summary:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-114127-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-phase5/status.json`
