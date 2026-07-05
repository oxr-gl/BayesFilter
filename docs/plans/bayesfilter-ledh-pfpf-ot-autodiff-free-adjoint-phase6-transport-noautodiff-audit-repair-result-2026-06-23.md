# Phase 6 Result: Transport No-Autodiff Audit And Repair

date: 2026-06-23
phase: P6-TRANSPORT-NOAUTODIFF-AUDIT-REPAIR
status: PASSED_LOCAL_REVIEW_PENDING

## Phase Objective And Question

P6 asked whether the selected LEDH-PFPF-OT transport custom-gradient route can
be audited and repaired so its `grad` body contains no production autodiff,
without using `transport_ad_mode=full`, GPU, finite differences, actual-gradient
validation, or filter-level certification.

## Inherited Entry Conditions

- P5 primitive adjoints passed and provide non-transport cotangent boundaries.
- P6 owns only transport repair for P1-L013/P1-L015.
- P7 still owns outer objective/manual reverse-scan replacement for
  P1-L001/P1-L003.
- P8/P9 still own no-autodiff certification and GPU ladder.
- GPU, finite differences, actual-gradient validation, and filter-level
  certification remained forbidden in P6.

## Implementation Evidence

Patched selected transport route:

```text
experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py
```

The selected route
`manual_streaming_finite_sinkhorn_stopped_scale_keys` uses
`_filterflow_manual_streaming_finite_transport_stopped_scale_keys` at line
1942, with `@tf.custom_gradient` at line 1960.  Its backward pass no longer
replays the transport value under `tf.GradientTape`; it now composes:

- `_filterflow_streaming_transport_from_potentials_vjp`;
- `_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys`;
- the same finite stopped-scale/key scalar used by the forward route.

The candidate blockwise route
`_filterflow_manual_streaming_blockwise_vjp_finite_transport_stopped_scale_keys`
starts at line 2046 and has a `@tf.custom_gradient` boundary at line 2064.  It
also passes grad-body scan.

The unselected `filterflow_custom_op` boundary still opens a tape at lines
2196 and 2207.  P6 did not hide this.  It remains route-flag vetoed by the
manifest policy and must not be selected by a production no-autodiff route.

## Tests And Audit Evidence

Updated focused audit tests:

- `tests/test_audit_ledh_no_autodiff.py:28`
  confirms the overall current route still fails for P1-L001/P1-L003.
- `tests/test_audit_ledh_no_autodiff.py:41`
  confirms the old selected manual streaming boundary is not an automatic pass
  and now passes grad-body scan.
- `tests/test_audit_ledh_no_autodiff.py:60`
  explicitly guards that the replay route `grad` body has no `GradientTape` or
  `.gradient` findings.

Focused transport tests exercised:

- `test_streaming_softmin_vjp_matches_dense_and_tiny_autodiff`;
- `test_streaming_transport_from_potentials_vjp_matches_manual_and_tiny_autodiff`;
- `test_streaming_sinkhorn_recursion_vjp_matches_manual_and_tiny_autodiff`;
- `test_blockwise_route_matches_dense_and_preserves_streaming_metadata`;
- `test_blockwise_route_rejects_unsupported_combinations_and_preserves_defaults`;
- `test_m6_manual_streaming_matches_dense_route_without_dense_matrix`;
- `test_m6_manual_streaming_core_rejects_unsupported_combinations`.

Diagnostic autodiff in those tests remains test-only and explanatory.

## Local Commands Actually Run

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py scripts/audit_ledh_no_autodiff.py tests/test_audit_ledh_no_autodiff.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_audit_ledh_no_autodiff.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "p2 or p6 or streaming_softmin_vjp or streaming_transport_from_potentials_vjp or streaming_sinkhorn_recursion_vjp or m6_manual_streaming or blockwise_route" -q
```

Output:

```text
22 passed, 15 deselected
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "streaming_softmin_vjp or streaming_transport_from_potentials_vjp or streaming_sinkhorn_recursion_vjp or m6_manual_streaming or blockwise_route" -q
```

Output:

```text
14 passed, 15 deselected
```

Expected current-route audit:

```text
python scripts/audit_ledh_no_autodiff.py --manifest docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json --whitelist docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-current-route-audit-result-2026-06-23.json --expect-decision FAIL_CURRENT_ROUTE
```

Audit outcome:

- Decision: `FAIL_CURRENT_ROUTE`, expected because P7 outer objective leaks
  remain.
- Failed P1 IDs: `P1-L001`, `P1-L003`.
- P1-L013/P1-L015 are no longer failed IDs.
- Manual streaming finite boundary at line 1960:
  `PASS_GRAD_BODY_SCAN`.
- Blockwise boundary at line 2064:
  `PASS_GRAD_BODY_SCAN`.
- Unselected custom-op boundary at line 2170:
  `FAIL_GRAD_BODY_AUTODIFF`, route-flag-gated and not a selected transport
  candidate.

Passed:

```text
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_audit_ledh_no_autodiff.py docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase6-current-route-audit-result-2026-06-23.json
```

## Skeptical Plan Audit Outcome

P6 did not use GPU, finite differences, actual-gradient validation, full-filter
certification, or P5 helper repairs.  The selected transport route is repaired
at the grad-body level; the overall route intentionally still fails until P7
replaces the outer objective tape.

The audit keeps the unselected custom-op tape visible and route-flag-gated
instead of hiding it.  This prevents a route-name-only promotion.

## Evidence Contract Outcome

| Field | Status |
|---|---|
| Primary criterion | Passed locally for selected transport route: grad-body audit passes and focused transport tests pass without `transport_ad_mode=full`. |
| Veto diagnostics | Passed for P6 scope: no selected transport grad body opens autodiff; no GPU/FD/actual-gradient/full-filter certification; no P5 helper repair. |
| Remaining audit failure | P1-L001/P1-L003 outer objective leaks remain for P7. |
| Explanatory only | Tiny test autodiff parity and CPU-only test timings. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `8eca1559c9508527a8d61d4ca348d8cee632db42` |
| Environment | Local repo shell; CPU-hidden commands used `CUDA_VISIBLE_DEVICES=-1`. |
| CPU/GPU status | CPU-only by explicit device hiding; no GPU command was run. |
| Dtype | `tf.float64` in focused transport tests. |
| Seeds | N/A; deterministic tensor fixtures. |
| Artifact paths | This result; P6 audit JSON; updated P2 route manifest; focused audit/transport tests. |

## Unresolved Blockers And Leaks Carried Forward

- P1-L001 and P1-L003 remain open for P7.
- P1-L013 and P1-L015 are closed for the selected manual streaming finite
  transport route.
- The unselected `filterflow_custom_op` transport route still contains a
  tape-based custom-gradient body and remains forbidden for production
  no-autodiff manifests.

## Nonclaims

P6 does not certify the full LEDH-PFPF-OT gradient route, does not replace the
outer objective tape, does not prove N10000 feasibility, does not establish FD
agreement, does not claim HMC/posterior readiness, and does not make a
scientific-validity claim.

## Next Gate And Handoff

Refresh and review P7 before execution.  P7 must inherit:

- P5 non-transport primitive adjoints;
- P6 selected transport grad-body closure for P1-L013/P1-L015;
- current audit failure limited to P1-L001/P1-L003 for the reviewed manifest;
- route-flag vetoes for `transport_ad_mode=full`, forward-JVP,
  reverse-gradient, and `filterflow_custom_op`.

P7 may implement the filter-level manual route and reverse-time scan only after
its refreshed subplan passes bounded review.  GPU, FD, actual-gradient, and
full certification remain forbidden until later phases.
