# Phase 5 Result: LEDH Flow And Log-Weight Adjoints

date: 2026-06-23
phase: P5-LEDH-FLOW-LOGWEIGHT-ADJOINTS
status: PASSED_LOCAL_REVIEW_PENDING

## Phase Objective And Question

P5 asked whether the non-transport LEDH flow/log-density/log-weight primitive
layer can be manually differentiated without adding production autodiff.

## Inherited Entry Conditions

- P4 analytical SIR derivatives passed.
- P3 derivation contract assigns P5 responsibility for Gaussian log-density,
  log-normalization, likelihood-increment, floor-mask, and LEDH flow primitive
  adjoints.
- P6 still owns transport no-autodiff repair for P1-L013/P1-L015.
- P7/P8 still own filter-level route implementation and no-autodiff
  certification.
- GPU, finite differences, N10000 actual-gradient validation, HMC checks, and
  posterior/scientific claims remained forbidden in P5.

## Implementation Evidence

Implementation file:

```text
experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py
```

Added P5 primitive helpers:

- `BatchedLEDHFlowVJPTensors` at line 327.
- `_batched_gaussian_logpdf_vjp` at line 803.
- `_transition_gaussian_log_density_vjp` at line 837.
- `_observation_gaussian_log_density_vjp` at line 864.
- `_normalize_log_weights_vjp` at line 911.
- `_floor_log_weights_vjp` at line 950.
- `_normalize_log_weights_with_floor_vjp` at line 979.
- `_log_weight_correction_vjp` at line 1003.
- `_observation_difference_residual_vjp` at line 1022.
- `_batched_ledh_linearized_flow_with_aux_tf` at line 1039.
- `_batched_ledh_linearized_flow_vjp` at line 1196.

Test file:

```text
tests/test_ledh_pfpf_ot_p5_primitive_adjoints.py
```

Focused tests cover:

- Gaussian log-density residual/covariance VJP.
- Log-normalization, likelihood-increment, and fixed floor-mask VJP.
- Named transition and observation Gaussian log-density VJPs.
- Log-weight correction sign distribution.
- Observation residual subtraction conventions.
- Linearized LEDH flow matrix primitive VJP.

Diagnostic autodiff appears only in this focused test file and is listed as
test-only whitelist entry `P5-DIAG-001`.  It is not a production derivative
mechanism and is not a promotion criterion.

## Local Commands Actually Run

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_ledh_pfpf_ot_p5_primitive_adjoints.py
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_p5_primitive_adjoints.py -q
```

Output:

```text
6 passed
```

Expected negative-control audit passed with expected decision:

```text
python scripts/audit_ledh_no_autodiff.py --manifest docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json --whitelist docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-current-route-audit-result-2026-06-23.json --expect-decision FAIL_CURRENT_ROUTE
```

Static scan:

```text
rg -n 'GradientTape|ForwardAccumulator|tape\.gradient|tape\.jacobian|tf\.gradients' experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_ledh_pfpf_ot_p5_primitive_adjoints.py
```

Classification:

- `tests/test_ledh_pfpf_ot_p5_primitive_adjoints.py` contains tiny diagnostic
  `tf.GradientTape` comparisons only.
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  still contains the pre-existing value-and-score tape at lines 1756 and
  1767.  This is not introduced by P5 and remains a P7/P8 route-certification
  issue.

Passed:

```text
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_ledh_pfpf_ot_p5_primitive_adjoints.py docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-execution-ledger-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-stop-handoff-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-current-route-audit-result-2026-06-23.json docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json
```

## Skeptical Plan Audit Outcome

P5 did not use finite differences, Zhao-Cui comparison, GPU, actual-gradient
validation, or filter-level certification.  The route audit remains a negative
control and must not be read as no-autodiff certification.  The P5 diagnostic
autodiff tests are explanatory only and are now explicitly recorded in the
audit whitelist/manifest as test-only.

## Evidence Contract Outcome

| Field | Status |
|---|---|
| Primary criterion | Passed locally for P5 primitive adjoint tests and no new P5 production tape helper. |
| Veto diagnostics | Passed for P5 scope: no FD; no `transport_ad_mode=full`; no transport repair; no GPU; no hidden tape in new P5 primitives. |
| Audit state | `FAIL_CURRENT_ROUTE`, expected; failed IDs remain `P1-L001`, `P1-L003`, `P1-L013`, `P1-L015`. |
| Explanatory only | Tiny diagnostic autodiff parity in `tests/test_ledh_pfpf_ot_p5_primitive_adjoints.py`. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `8eca1559c9508527a8d61d4ca348d8cee632db42` |
| Environment | Local repo shell; CPU-hidden commands used `CUDA_VISIBLE_DEVICES=-1`. |
| CPU/GPU status | CPU-only by explicit device hiding; no GPU command was run. |
| Dtype | `tf.float64` in focused P5 tests. |
| Seeds | N/A; deterministic tensor fixtures. |
| Artifact paths | This result, P5 audit JSON, updated P2 manifest/whitelist, focused P5 tests. |

## Unresolved Blockers And Leaks Carried Forward

- P1-L001 and P1-L003: outer objective `tf.GradientTape` remains open for P7.
- P1-L013 and P1-L015: transport custom-gradient grad-body tape remains open
  for P6.
- The pre-existing value-and-score tape in
  `experimental_batched_ledh_pfpf_ot_tf.py` remains noncertified for the
  production no-autodiff route.

## Nonclaims

P5 does not certify the full LEDH-PFPF-OT gradient route, does not close the
transport leaks, does not prove N10000 feasibility, does not establish FD
agreement, does not claim HMC/posterior readiness, and does not make a
scientific-validity claim.

## Next Gate And Handoff

Refresh and review P6 before execution.  P6 must inherit P5 cotangent shapes
for log-weight normalization, floored log weights, transition/observation
log-density VJPs, and LEDH flow outputs.  P6 may only audit/repair the
transport no-autodiff route and must not run GPU, FD, actual-gradient, or
filter-level certification.
