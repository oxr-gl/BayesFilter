# W2-LR-1 Result: Validation Implementation And Replay

Date: 2026-06-19
Owner: peer agent

## Status

`LOW_RANK_COUPLING_VALIDATION_P01_REPLAY_PASSED`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | The low-rank coupling solver-route candidate passed a Wave 2 hard-veto validation screen under CPU-only TensorFlow replay. |
| Baseline/comparator | P12 diagnostic result is entry context; Phase 1 dense/streaming baseline is context only and not a promotion comparator. |
| Primary criterion | Passed: validation JSON status is `PASS`, hard vetoes are `[]`, candidate record validates under Phase 3 schema, all three fixture rows passed finite/nonnegative/positive-factor checks, residuals and apply parity are below fixed thresholds, and source-route classification remains weakest-route `extension_or_invention`. |
| Veto diagnostics | No compile, test, diagnostic, JSON, schema, finite-value, sign, residual, parity, source-route, positive-feature evidence, external solver, package/network, public/shared edit, or CPU-scope hard veto fired. |
| Explanatory diagnostics | Rank, fixture shape, projection iterations, projection error, floor hits, factor minima, and wall time are explanatory only. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or full solver fidelity is concluded. |

## Checks Run

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile \
  docs/benchmarks/scalable_ot_wave2_low_rank_coupling_validation.py \
  tests/test_wave2_low_rank_coupling_validation.py

CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_low_rank_coupling_solver_tf.py \
  tests/test_wave2_low_rank_coupling_validation.py

CUDA_VISIBLE_DEVICES=-1 python \
  docs/benchmarks/scalable_ot_wave2_low_rank_coupling_validation.py \
  --output docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.json \
  --markdown-output docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.md

python -m json.tool \
  docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.json
```

Observed results:

- CPU-only compile: passed.
- Focused pytest: `5 passed`.
- Diagnostic replay: exited 0 and wrote JSON/Markdown.
- JSON parse/schema check: passed.

TensorFlow emitted a CUDA/no-device initialization line during the diagnostic
run despite `CUDA_VISIBLE_DEVICES=-1`.  The run manifest records CPU scope and
`cuda_visible_devices: "-1"`; the CUDA line is treated as environment noise, not
GPU evidence.

## Validation Summary

| Metric | Value | Role |
| --- | ---: | --- |
| max factor marginal residual | `1.1449623765757977e-07` | hard veto |
| max induced row residual | `5.267489473492759e-07` | hard veto |
| max induced column residual | `5.724811882323877e-07` | hard veto |
| max materialized tiny apply parity | `1.1102230246251565e-16` | hard veto |

Diagnostic artifacts:

- `docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.json`
- `docs/benchmarks/scalable-ot-wave2-low-rank-coupling-validation-2026-06-19.md`

Wave 2 status:

`LOW_RANK_COUPLING_VALIDATION_PASSED_DIAGNOSTIC_ONLY`

## Source-Route Boundary

- Overall source route remains `extension_or_invention`.
- `source_faithful` remains limited to the factored coupling
  parameterization, lazy apply, factor marginal diagnostics, and mirrored
  Dykstra-style projection.
- Deterministic initialization/schedules and Phase 1 scaled adapter remain
  `fixed_hmc_adaptation`.
- Cost-nudged assignment kernel remains `extension_or_invention`.

## Next Subplan Review

W2-LR-2 closeout is consistent, feasible, artifact-complete, and boundary-safe
if it writes only lane-local final result/status records, records this
diagnostic-only pass, preserves non-claims, and stops without coordinator
synthesis.

## Handoff

Advance to W2-LR-2 lane closeout.
