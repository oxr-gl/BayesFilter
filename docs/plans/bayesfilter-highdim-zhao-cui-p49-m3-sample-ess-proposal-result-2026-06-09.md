# P49-M3 Sample, ESS, And Proposal-Correction Result

metadata_date: 2026-06-09
phase: P49-M3
status: PASS_P49_M3_SAMPLE_ESS_PROPOSAL

## Decision Table

| Field | Decision |
| --- | --- |
| Gate decision | Pass M3 for scoped source-route sample/ESS/proposal-correction accounting. |
| Primary criterion status | Passed: one-step tests cover sample-batch metadata, ESS accounting, ESS enhancement gate, explicit proposal correction, negative-log target conversion, and exact discrete normalizer recovery; the M2 retained-object regression remains the preserved no-pairwise-grid source-route guard. |
| Veto diagnostic status | Passed: ESS and correction ratio are first-class helpers; correction sign convention is explicit; M2 no-pairwise-grid source-route guards remain covered by `tests/highdim/test_p49_source_route_retained_object.py`. |
| Main uncertainty | This is an accounting/helper gate, not a complete stochastic source-route filter or adaptive TT/SIRT fit. |
| Next justified action | Advance to M4 recentering, Jacobian, and normalizer-accounting tests. |
| Not concluded | No paper-scale accuracy, HMC readiness, production adaptive transport quality, smoothing support, or full Zhao--Cui source-route completion. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the source-faithful lane use sample/ESS/proposal correction instead of pairwise retained-grid transition density? |
| Baseline/comparator | M1 source operation contract plus exact finite-discrete one-step identities. |
| Primary pass criterion | Focused one-step tests verify sample propagation metadata, ESS accounting, and proposal correction; the retained-object regression verifies no pairwise-grid source-route fallback. |
| Diagnostics that can veto | ESS omitted; correction ratio omitted; source-route correction uses the wrong sign; all-grid pairwise propagation accepted as source-faithful evidence. |
| Explanatory diagnostics | CPU-only pytest, compileall, static diff whitespace check, exact discrete-support normalizer equality. |
| What will not be concluded | Full filter correctness, paper-scale readiness, or differentiable HMC readiness. |
| Artifact preserving result | This file plus `tests/highdim/test_p49_source_route_sample_proposal.py` and the M2 guard regression `tests/highdim/test_p49_source_route_retained_object.py`. |

## Implemented Scope

M3 added minimal TensorFlow source-route accounting primitives in
`bayesfilter/highdim/source_route.py`:

- `SourceRouteSampleBatch` records weighted samples, time index, route label,
  and sample origin.
- `normalize_log_weights` and `effective_sample_size_from_log_weights` compute
  normalized log weights and ESS from finite log weights.
- `source_route_needs_enhancement` implements the ESS threshold gate.
- `source_route_proposal_log_weights` computes correction weights as
  `log_target_density - log_proposal_density`.
- `source_route_proposal_log_weights_from_negative_log_target` makes the
  negative-log target conversion explicit before applying proposal correction.
- `source_route_discrete_log_normalizer_from_correction` checks exact
  discrete-support proposal-correction accounting.
- `source_route_equal_weight_log_normalizer_estimate` records the equal-weight
  Monte Carlo estimator used for stochastic proposal samples.
- `source_route_push_sample_batch` creates a propagated sample batch while
  preserving sample count and advancing time.

The highdim subpackage exports were updated for these M3 helpers.  No top-level
`bayesfilter` API export was added.

## Local Validation

Commands run CPU-only with `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`:

```text
pytest -q tests/highdim/test_p49_source_route_sample_proposal.py tests/highdim/test_p49_source_route_retained_object.py tests/highdim/test_public_api_highdim.py tests/highdim/test_phase0_contracts.py
```

Result:

```text
36 passed, 2 TensorFlow Probability deprecation warnings
```

```text
python -m compileall -q bayesfilter/highdim/source_route.py tests/highdim/test_p49_source_route_sample_proposal.py tests/highdim/test_p49_source_route_retained_object.py
```

Result: passed.

```text
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p49_source_route_sample_proposal.py docs/plans/bayesfilter-highdim-zhao-cui-p49-visible-execution-ledger-2026-06-09.md
```

Result: passed.

## Interpretation

The M3 gate establishes that the source-faithful lane now has explicit,
tested primitives for weighted samples, ESS diagnostics, sample propagation
metadata, and proposal correction.  The correction sign convention is
mechanically visible: log-density inputs use `log_target_density -
log_proposal_density`, while negative-log target values must pass through the
separate conversion helper.

M3 deliberately does not implement adaptive TT-cross/SIRT fitting, stochastic
resampling/enhancement, or full sequential filtering.  Those remain assigned to
later gates.
