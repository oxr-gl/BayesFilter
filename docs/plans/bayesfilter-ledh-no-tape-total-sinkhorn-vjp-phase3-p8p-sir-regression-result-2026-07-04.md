# Phase 3 Result: P8p SIR Regression Integration

Date: 2026-07-04

Status: `CLOSED_REVIEWED`

## Phase Objective

Use the no-tape total finite streaming Sinkhorn primitive in the scoped P8p SIR
manual route and verify that the same-scalar total-derivative diagnostics still
pass.

## Entry Conditions

- Phase 2 validated the primitive against raw tape and central finite
  differences.
- Phase 2 review returned `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.

## Implementation Artifacts

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  - Added `_filterflow_manual_streaming_finite_transport_total_pullback` so
    callers can use the no-tape transport VJP directly.
  - `_filterflow_manual_streaming_finite_transport_total_vjp` now delegates its
    custom-gradient body to that pullback.
  - Added a shape invariant for the softmin epsilon cotangent accumulator in
    compiled loops.
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
  - Removed the local tape from `_manual_transport_vjp_tf` for
    `transport_ad_mode="full"`.
  - Added explicit branchwise VJPs for `_filterflow_epsilon_start`,
    `_filterflow_scale`, and the centered/scaled particle transform.
- `tests/test_ledh_pfpf_ot_p7_manual_score.py`
  - Added a runtime no-autodiff sentinel test for full-mode manual transport.
- `tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py`
  - Updated the source audit to follow the new pullback helper.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the no-tape primitive preserve the scoped P8p SIR total-derivative behavior? |
| Baseline/comparator | P8p tiny raw autodiff diagnostic and prior manual scan baseline/reference checks. |
| Primary criterion | P8p same-scalar total-derivative checks pass with route metadata proving no-tape total VJP use. |
| Veto diagnostics | P8p route falls back to tape; stopped partial derivative used as score; value/score algorithm mismatch; scoped diagnostic promoted to full leaderboard row; same-scalar check fails. |
| Explanatory diagnostics | Tiny objective/gradient gaps, runtime sentinel status, static source audit. |
| Not concluded | Full observed-data SIR leaderboard score, LGSSM score admission, GPU/XLA production claim, HMC readiness. |

## Checks Run

CPU-only checks intentionally set `CUDA_VISIBLE_DEVICES=-1`.

| Command | Result |
| --- | --- |
| `python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py tests/test_ledh_pfpf_ot_p7_manual_score.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py` | pass |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_pfpf_ot_p7_manual_score.py::test_p7_manual_score_matches_tiny_diagnostic_autodiff tests/test_ledh_pfpf_ot_p7_manual_score.py::test_p7_manual_full_transport_score_runs_under_runtime_autodiff_sentinel tests/test_ledh_pfpf_ot_p7_manual_score.py::test_p7_manual_score_runs_under_runtime_autodiff_sentinel` | pass: 3 tests |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_ledh_pfpf_ot_p7_manual_score.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py tests/test_audit_ledh_clean_xla.py::test_default_clean_xla_audit_reports_current_route_unclean_with_line_anchors` | pass: 13 tests |
| `PYTHONPATH=/home/chakwong/BayesFilter CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY' ... > docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-2026-07-04.json` | pass |
| `python -m json.tool docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-2026-07-04.json` | pass |
| Static AST/source check for `_manual_transport_vjp_tf`, `_filterflow_manual_streaming_finite_transport_total_pullback`, and `_filterflow_manual_streaming_finite_transport_total_vjp` forbidding `GradientTape`, `ForwardAccumulator`, `.gradient(` | pass |
| `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py::test_phase4_manual_scan_loop_matches_preedit_baseline_fixture tests/test_audit_ledh_clean_xla.py::test_phase4_manual_scan_loop_matches_python_record_reference tests/test_audit_ledh_clean_xla.py::test_phase5_streaming_sinkhorn_loop_state_matches_preedit_fixture` | pass: 3 tests |
| `git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py tests/test_ledh_pfpf_ot_p7_manual_score.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase1.py tests/test_ledh_no_tape_total_sinkhorn_vjp_phase2.py docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-2026-07-04.json` | pass |

## Numerical Result

Artifact:
`docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-2026-07-04.json`

Tiny P8p full-mode fixture:

- manual objective: `-36.365299224853516`;
- raw autodiff objective: `-36.365299224853516`;
- max log-likelihood gap versus autodiff: `0.0`;
- manual gradient: `[-10.013418197631836, 3.666980028152466, 5.286164283752441]`;
- raw autodiff gradient: `[-10.013410568237305, 3.666977882385254, 5.286158561706543]`;
- max gradient gap versus autodiff: `7.62939453125e-06`;
- predeclared tiny tolerance: `1.0e-05`;
- runtime no-autodiff sentinel for full-mode manual score: pass.

## Decision Table

| Decision | Primary Criterion Status | Veto Status | Main Uncertainty | Next Justified Action | Not Concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 3 locally and request read-only review | pass | no Phase 3 veto found | Tiny P8p regression is not LGSSM or leaderboard score evidence | Phase 4 LGSSM same-target score admission attempt | Full leaderboard row, GPU/XLA production status, HMC readiness |

## Skeptical Audit

- Wrong baseline risk: Phase 3 compares to a tiny raw autodiff diagnostic and
  existing P8p manual scan baseline/reference checks.  It does not compare to a
  stopped partial derivative.
- Hidden tape risk: a full-mode local tape was found in `_manual_transport_vjp_tf`
  and removed.  Runtime sentinel and static checks now cover the full-mode path.
- Value/score mismatch risk: the P8p artifact records
  `value_score_same_transport_algorithm: true` and the primitive
  `_filterflow_manual_streaming_finite_transport_total_pullback`.
- Overclaim risk: this result does not admit a leaderboard score.

## Nonclaims

- This does not prove LGSSM score admission.
- This does not prove full SIR leaderboard score correctness.
- This does not certify GPU/XLA behavior.
- This does not claim HMC readiness.

## Phase 4 Handoff

Phase 4 may start.  Claude read-only review accepted this result and the
refreshed Phase 4 subplan:

- `REVIEW_STATUS=agreed`
- `VERDICT=AGREE`
- Run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-035504-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-phase4`
- Summary:
  `/home/chakwong/BayesFilter/.claude_reviews/20260704-035504-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-phase4/status.json`

Phase 4 must separately prove LGSSM same-target score admission with
same-route/no-tape evidence and exact/FD comparison.
