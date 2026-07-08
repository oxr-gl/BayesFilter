# Phase 7 Result: Filter-Level Manual Route

date: 2026-06-23
phase: P7-FILTER-CUSTOM-GRADIENT
decision: PASSED
git_commit_at_checks: 97ad05d40676f3fd15a2a2b4d45034ebb657ed97

## Phase Objective And Question

P7 asked whether the LEDH-PFPF-OT P8p SIR value could expose an opt-in
manual reverse-score route that replaces the selected outer objective
`GradientTape` leaks P1-L001/P1-L003, without reopening the P5/P6 primitive
and transport boundaries.

## Entry Conditions

- P5 primitive adjoints existed and were inherited without broad redesign.
- P6 closed P1-L013/P1-L015 for the selected manual streaming finite transport
  route.
- The reviewed P7 subplan prohibited GPU, finite differences, N10000 actual
  gradient work, default-route changes, Zhao-Cui comparators, and
  `transport_ad_mode=full`.
- P7 could use tiny diagnostic autodiff only as an explanatory comparison, not
  as production proof.

## Implementation Summary

P7 added an opt-in manual route in
`docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`:

- analytical SIR RHS/RK4 VJP helpers;
- a manual transport VJP wrapper restricted to streaming transport,
  `transport_ad_mode="stabilized"`, and manual streaming transport gradient
  modes;
- parameter cotangent accumulation for log-kappa, log-nu, and observation
  covariance scale;
- `_manual_value_and_score_from_components`;
- `_manual_gradient_diagnostic`, returning
  `score_route="manual_reverse_scan_no_autodiff"`.

P7 also updated
`docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py` with
`--ad-evaluation-mode manual-reverse` and
`_manual_gradient_diagnostic_for_contexts`, so the selected route no longer
uses the previous outer objective reverse-mode tape.

Focused tests were added in
`tests/test_ledh_pfpf_ot_p7_manual_score.py`.

## Route Manifest Change

The current manifest
`docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json`
now records:

- `ad_evaluation_mode: manual-reverse`;
- `transport_plan_mode: streaming`;
- `transport_ad_mode: stabilized`;
- `transport_gradient_mode:
  manual_streaming_finite_sinkhorn_stopped_scale_keys`;
- no expected negative-control failures;
- P1-L001/P1-L003 classified as closed by the P7 manual reverse route;
- P1-L013/P1-L015 retained as closed by the P6 transport manual VJP.

## Commands And Results

All P7 local commands were run with `CUDA_VISIBLE_DEVICES=-1`, intentionally
CPU-only.  These are local implementation checks, not GPU evidence.

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_p7_manual_score.py -q
```

Result: `3 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope cpu --device /CPU:0 --expect-device-kind cpu --fd-mode ad-only --ad-evaluation-mode manual-reverse --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-plan-mode streaming --transport-ad-mode stabilized --time-steps 1 --num-particles 2 --batch-seeds 81120 --row-chunk-size 2 --col-chunk-size 2 --particle-chunk-size 2 --sinkhorn-iterations 1 --output /tmp/p7-manual-smoke.json
```

Result: passed with finite objective and gradient:

- objective: `-36.365299224853516`;
- gradient:
  `[-10.013418197631836, 3.666980028152466, 5.286164283752441]`;
- `primary_pass: true`;
- route: `manual-reverse`.

Runtime sentinel smoke: the manual route ran under
`audit.AutodiffRuntimeSentinel(p8p.tf, route_id='p7_manual_reverse_smoke')`
and returned the same finite objective/gradient with
`score_route: manual_reverse_scan_no_autodiff`.

Tiny explanatory parity check against diagnostic autodiff in float64:

- manual value: `[-36.36530051]`;
- diagnostic value: `[-36.36530051]`;
- manual gradient:
  `[-10.01340666, 3.66697616, 5.28615784]`;
- diagnostic gradient matched to roundoff, with maximum difference around
  `1e-14`.

After manifest/test refresh:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_audit_ledh_no_autodiff.py tests/test_ledh_pfpf_ot_p7_manual_score.py -q
```

Result: `12 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/test_ledh_pfpf_ot_p7_manual_score.py tests/test_audit_ledh_no_autodiff.py scripts/audit_ledh_no_autodiff.py
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_no_autodiff.py --manifest docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json --whitelist docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-current-route-audit-result-2026-06-23.json --expect-decision FAIL_CURRENT_ROUTE
```

Result: exited 0 and wrote the P7 audit artifact.  Important fields:

- `decision: FAIL_CURRENT_ROUTE`;
- `failed_p1_ids: []`;
- `bad_route_flag_vetoes: []`;
- selected transport custom-gradient bodies at decorator lines 1960 and 2064
  remain `PASS_GRAD_BODY_SCAN`;
- the unselected `filterflow_custom_op` boundary at decorator line 2170 still
  has `FAIL_GRAD_BODY_AUTODIFF` and remains a P8 certification problem;
- broad production static findings remain in diagnostic/legacy files.

```text
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/test_ledh_pfpf_ot_p7_manual_score.py tests/test_audit_ledh_no_autodiff.py scripts/audit_ledh_no_autodiff.py docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-current-route-audit-result-2026-06-23.json
```

Result: passed.

## Skeptical Plan Audit Outcome

The P7 plan survived the skeptical audit after narrowing the objective to the
selected manual route.  The main risk was mistaking a route-bound closure for
full no-autodiff certification.  P7 therefore records the broad audit decision
as `FAIL_CURRENT_ROUTE` and advances only because the selected P1 outer-tape
IDs are no longer failed and the P8 certification phase owns the remaining
static/runtime cleanup.

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Question | Answered for the selected tiny/manual route: the route can compute finite manual scores without the outer objective tape. |
| Baseline/comparator | Prior outer `GradientTape` route replaced for `manual-reverse`; P5/P6 boundaries inherited. |
| Primary criterion | Met for P7: finite tiny manual scores; P1-L001/P1-L003 no longer fail the manifest audit; P1-L013/P1-L015 remain closed. |
| Veto diagnostics | No GPU/FD/N10000/default-route/Zhao-Cui/`transport_ad_mode=full` work was run; no P5/P6 repair was reopened. |
| Explanatory only | Tiny diagnostic autodiff parity and CPU-only smoke output. |
| Not concluded | Full no-autodiff certification, GPU feasibility, N10000 feasibility, FD agreement, HMC readiness, posterior correctness, production default, or scientific validity. |

## Carry-Forward Blockers For P8

P8 must not claim certification from the P7 audit artifact.  Remaining
certification work includes:

- broad production static findings in diagnostic reverse/JVP helpers and old
  generic score helpers;
- the unselected `filterflow_custom_op` custom-gradient body with an internal
  tape;
- audit-tool treatment of manually implemented `tf.custom_gradient` boundaries:
  a manually audited boundary may be allowed only if its `grad` body scan is
  clean and the selected route manifest binds to it exactly;
- exact runtime sentinel coverage for the selected route;
- an exact route manifest suitable for Phase 9.

## Next Gate

Advance to P8 only under the refreshed P8 subplan.  P8 must either make the
exact selected route pass `PASS_NO_AUTODIFF_AUDIT` or write a blocker result.
GPU, FD, and N10000 work remain prohibited until P8 passes.
