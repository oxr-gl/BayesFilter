# Fixed-SGQF Structural Adapter Plan

metadata_date: 2026-06-16
program_id: fixed-sgqf-structural-adapter
status: EXECUTION_READY

## Purpose

This plan governs the next engineering step after the nonlinear suite comparison
integration pass: build an exact-gated structural→fixed-SGQF adapter for
fixtures that are exactly representable in the current additive-state
fixed-SGQF lane, while explicitly blocking inexact fixtures.

## Governing context

Current comparison status:
- Model A is already benchmarked exactly in the fixed-SGQF lane.
- Model B and Model C are currently represented explicitly as blocked in the
  comparison harnesses because no same-target structural adapter exists yet.
- The user wants the next concrete engineering step rather than stopping at the
  governance/eligibility layer.

## Model policy

### Model A
- unchanged; already exact and integrated.

### Model B
- must remain blocked as exact same-target in the current additive-state lane.
- reason: innovation enters the deterministic block through a nonlinear
  completion, so the full-state process noise is not a constant additive Gaussian
  covariance.

### Model C
- target for the first new exact structural adapter.
- exact in model form for the current additive-state lane except for the current
  positive-definite covariance assumption blocking the deterministic phase
  coordinate with zero variance.

## Skeptical plan audit

Status target: `PASS_TO_EXACT_GATED_ADAPTER_IMPLEMENTATION`

Risks:
1. admitting Model B through an inexact closure and still calling it same-target;
2. adding variance floors for deterministic coordinates and calling the row
   exact;
3. overexpanding into a full structural score adapter when the current pass
   should focus on value-path exactness first;
4. changing benchmark outputs without explicit blocked-row reasons.

## Evidence contract

Question:
- Can we build an exact-gated same-target structural adapter that admits
  Model-C-class fixtures into the current fixed-SGQF lane while honestly
  blocking Model B?

Primary pass criterion:
- exact eligibility decisions are explicit;
- Model C becomes a same-target adapter success row if semidefinite state
  covariance handling is solved exactly;
- Model B remains explicitly blocked if still ineligible;
- the nonlinear benchmark harness reflects that distinction.

Veto diagnostics:
- Model B is admitted without exact-law justification;
- deterministic variance floors are used and the row is still labeled exact;
- benchmark outputs hide adapter rejections.

## Likely files to modify

### Primary implementation
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`
- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py` (only if derivative
  adaptation is truly in-scope now)
- new internal adapter module:
  `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`

### Benchmark harnesses
- `docs/benchmarks/benchmark_bayesfilter_v1_nonlinear_filters.py`
- `docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py`

### Tests
- `tests/test_nonlinear_benchmark_models_tf.py`
- `tests/test_fixed_sgqf_values_tf.py`
- optional if score adaptation is added now:
  `tests/test_fixed_sgqf_scores_tf.py`

## Execution order

1. Write this plan artifact.
2. Implement an exact-gated structural adapter module.
3. Add semidefinite state-covariance support if needed for Model C exactness.
4. Add eligibility tests:
   - Model C exact-eligible,
   - Model B exact-ineligible.
5. Add adapter-based value tests for Model C.
6. Wire the nonlinear benchmark harness to use the adapter.
7. Keep the smoke harness blocked unless an exact same-target path exists there.
8. Write the result artifact.

## Verification

Minimum verification:
- adapter eligibility tests,
- fixed-SGQF value tests for adapted Model C rows,
- nonlinear benchmark harness rerun,
- explicit check that Model B remains honestly blocked if still ineligible.
