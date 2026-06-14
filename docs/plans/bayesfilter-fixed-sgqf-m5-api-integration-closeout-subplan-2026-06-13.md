# Fixed-SGQF M5 Subplan: API Integration Closeout

metadata_date: 2026-06-13
phase: M5
status: READY_FOR_IMPLEMENTATION

## Objective

Expose the Fixed-SGQF lane through stable nonlinear entry points and verify end-to-end deterministic use on existing fixtures.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can callers use Fixed-SGQF value and score entry points through the nonlinear package API with deterministic end-to-end behavior? |
| Baseline/comparator | Completed M1-M4 implementation under the p47 branch contract; existing nonlinear package exports and end-to-end test patterns. |
| Primary pass criterion | `bayesfilter.nonlinear` exports the Fixed-SGQF value and score entry points, targeted end-to-end tests pass, and eager/compiled behavior matches where compilation is already supported. |
| Veto diagnostics | API exports are missing or ambiguous; integration only works through private helpers; deterministic behavior differs across supported execution modes without explanation. |
| Not concluded | No automatic highdim integration or benchmark-matrix admission claim. |

## Tasks

1. Export Fixed-SGQF value/score entry points through `bayesfilter/nonlinear/__init__.py`.
2. Add a small end-to-end integration test path using existing nonlinear fixtures.
3. Add compiled-parity coverage only where the SGQF lane already supports it cleanly.
4. Keep API integration scoped to the nonlinear package in this first pass.

## Required Checks

- `pytest -q tests/test_fixed_sgqf_integration_tf.py`
- `pytest -q tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py`
- `python -m compileall bayesfilter/nonlinear`
