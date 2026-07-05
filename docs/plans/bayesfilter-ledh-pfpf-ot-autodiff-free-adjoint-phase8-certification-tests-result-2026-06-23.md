# Phase 8 Result: Exact-Route No-Autodiff Certification

date: 2026-06-23
phase: P8-CERTIFICATION-TESTS
decision: PASSED
git_commit_at_checks: 97ad05d40676f3fd15a2a2b4d45034ebb657ed97

## Phase Objective And Question

P8 asked whether the exact selected LEDH-PFPF-OT P8p SIR
`manual-reverse` route can pass static and runtime no-autodiff certification
before any GPU ladder, finite-difference comparison, N10000 run, default-route
change, or scientific claim.

## Entry Conditions

- P7 implemented the opt-in `--ad-evaluation-mode manual-reverse` route.
- P7 closed the selected outer-tape P1 IDs but did not certify the broad route.
- P7 audit artifact remained `FAIL_CURRENT_ROUTE` with broad static findings.
- P8 inherited P5/P6 manual primitive and selected transport boundaries.
- P8 was reviewed with Claude before execution and patched to predeclare the
  exact route manifest path.

Comparator and inherited audit artifacts:

```text
docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-tooling-result-2026-06-23.md
docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-audit-result-2026-06-23.json
docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-filter-custom-gradient-result-2026-06-23.md
docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase7-current-route-audit-result-2026-06-23.json
```

## Implementation And Audit Summary

P8 added exact-route audit support to
`scripts/audit_ledh_no_autodiff.py`.  The audit now supports an opt-in
`route_scope: selected_route_exact` manifest that separates:

- active selected-route production findings;
- excluded diagnostic-only or unselected-route findings;
- allowed manual `tf.custom_gradient` boundaries whose `grad` bodies are still
  scanned;
- unapproved custom-gradient boundaries, which remain hard failures.

P8 also tightened the selected manual route in
`docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py` so the
manual score path calls the selected finite streaming transport helper
directly, rather than certifying through the generic transport dispatcher that
still contains unselected legacy branches.

The exact route manifest is:

```text
docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json
```

The exact audit result is:

```text
docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-current-route-audit-result-2026-06-23.json
```

Audit result summary:

- `decision: PASS_NO_AUTODIFF_AUDIT`;
- active `production_findings: 0`;
- `raw_production_findings_count: 39`, all classified as diagnostic,
  unselected-route, or allowed manual custom-gradient boundary findings;
- `bad_route_flag_vetoes: []`;
- selected custom-gradient boundary:
  `annealed_transport_tf.py:1960`, `PASS_GRAD_BODY_SCAN`;
- `unapproved_custom_gradient_boundary_results: []`;
- nonclaim: certification applies only to the exact manifest route and is not
  transferable to another route manifest.

## Commands And Results

All commands below used `CUDA_VISIBLE_DEVICES=-1`.  They are GPU-hidden /
CPU-only local certification checks, not GPU evidence.

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile scripts/audit_ledh_no_autodiff.py tests/test_audit_ledh_no_autodiff.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/test_ledh_pfpf_ot_p7_manual_score.py
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_audit_ledh_no_autodiff.py tests/test_ledh_pfpf_ot_p7_manual_score.py -q
```

Result: `15 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_no_autodiff.py --manifest docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json --whitelist docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-current-route-audit-result-2026-06-23.json --expect-decision PASS_NO_AUTODIFF_AUDIT
```

Result: passed and wrote the exact audit artifact.

```text
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope cpu --device /CPU:0 --expect-device-kind cpu --fd-mode ad-only --ad-evaluation-mode manual-reverse --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-plan-mode streaming --transport-ad-mode stabilized --time-steps 1 --num-particles 2 --batch-seeds 81120 --row-chunk-size 2 --col-chunk-size 2 --particle-chunk-size 2 --sinkhorn-iterations 1 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-manual-route-runtime-sentinel-smoke-2026-06-23.json
```

Result: passed with:

- `status: pass`;
- `primary_pass: true`;
- objective: `-36.365299224853516`;
- gradient:
  `[-10.013418197631836, 3.666980028152466, 5.286164283752441]`;
- `primary_pass_criterion`: finite values and connected manual score route,
  not FD agreement or scientific validity.

Runtime sentinel coverage was exercised by
`tests/test_ledh_pfpf_ot_p7_manual_score.py`, including the selected manual
route and context aggregation route under `AutodiffRuntimeSentinel`.

```text
git diff --check -- scripts/audit_ledh_no_autodiff.py tests/test_audit_ledh_no_autodiff.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-current-route-audit-result-2026-06-23.json docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-manual-route-runtime-sentinel-smoke-2026-06-23.json
```

Result: passed.

## Skeptical Plan Audit Outcome

The initial P8 audit would have been misleading if it certified a whole file
instead of an exact selected route, because the file still contains diagnostic
reverse/JVP helpers and unselected legacy transport branches.  P8 therefore
made route scope explicit in the manifest and test suite.  Bad flags and
unapproved custom-gradient boundaries still fail; excluded findings are
recorded in the audit artifact rather than silently hidden.

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Question | Answered for the exact P8 manifest route. |
| Baseline/comparator | P7 manual route and exact P2/P7 artifacts named in Entry Conditions. |
| Primary criterion | Met: exact route audit passed, runtime sentinel tests passed, focused tests passed. |
| Veto diagnostics | No selected-route forbidden API; no selected custom-gradient grad-body autodiff; no bad route flags; no production-route finding excused by whitelist or production whitelist exemption; no GPU/FD/N10000/default/scientific drift. |
| Explanatory only | Tiny GPU-hidden / CPU-only smoke values and diagnostic/test-only autodiff locations. |
| Not concluded | GPU feasibility, N10000 feasibility, FD agreement, HMC readiness, posterior correctness, production default, or scientific validity. |

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| `PASSED` | Exact-route no-autodiff audit and focused runtime checks passed. | No P8 veto fired. | GPU memory/runtime behavior remains untested after route cleanup. | Review refreshed P9 subplan, then run trusted GPU ladder sequentially. | GPU feasibility, FD agreement, HMC readiness, posterior/scientific validity. |

## Carry-Forward Conditions For P9

P9 may run only after bounded review agrees this P8 result and the refreshed
P9 subplan are safe.  Every GPU rung must reference or extend the exact P8
route identity:

```text
docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-exact-route-manifest-2026-06-23.json
docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase8-current-route-audit-result-2026-06-23.json
```

P9 must run trusted GPU commands with escalation, stop at the first non-`PASSED`
rung, and must not run finite differences.
