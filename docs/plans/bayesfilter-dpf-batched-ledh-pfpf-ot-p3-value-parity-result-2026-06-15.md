# Phase 3 Result: Batched Value Recursion And Parity

Date: 2026-06-15

## Status

`PASSED`

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Does the batched fixed-branch LEDH-PFPF-OT value recursion preserve scalar-row relaxed objective semantics? |
| Candidate/mechanism | Experimental TensorFlow batched value recursion over `[B,N,D]` particles with fixed pre-flow particles and fixed transport masks. |
| Expected failure mode | Scalar-row comparators accidentally use local row indices or runtime stochastic decisions rather than row-owned fixed tensors. |
| Promotion criterion | B=1 and B=20 scalar-stack parity within Phase 0 tolerances, plus row permutation, identical-row, fixed-mask, and graph-smoke checks. |
| Promotion veto | Value parity failure, row cross-talk, uncompiled-only path, runtime ESS branch, RNG use, or relaxed-objective semantic drift. |
| Repair trigger | If parity failed because the comparator lost row-owned tensors, repair the fixture/comparator without changing tolerances. |
| What must not be concluded | No score correctness, no GPU speed, no production/default readiness, and no categorical particle-filter likelihood-gradient claim. |

## Evidence Contract Status

| Contract Item | Status |
| --- | --- |
| Comparator | Fixed scalar-row stack built from the same deterministic fixture and fixed masks. |
| Primary criterion | Passed: B=1 and B=20 parity tests passed under `atol=1e-10, rtol=1e-10`. |
| Veto diagnostics | No nonfinite values, row cross-talk, runtime ESS branch, RNG call, or public export drift observed in the focused checks. |
| Explanatory diagnostics | Initial resumed run exposed a comparator fixture bug: scalar sliced rows rebuilt transition matrices from local row indices. |
| Non-claims | Score correctness, GPU performance, and production readiness remain unclaimed. |

## Actions

- Added `BatchedLEDHPFPFOTValueTensors`.
- Added `batched_ledh_pfpf_ot_value_core_tf`.
- Added B=1 parity, B=20 scalar-stack parity, row-permutation, identical-row, and CPU `tf.function` smoke tests.
- Repaired the test fixture so transition log-density callbacks close over row-owned transition tensors after scalar slicing or row permutation.
- Aligned graph-smoke Sinkhorn iterations with the eager comparator.

## Checks Run

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_ledh_pfpf_ot_tf.py
```

Result:

```text
16 passed, 4600 warnings in 8.52s
```

```text
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py
```

Result: passed with no output.

## Decision Table

| Decision | Primary Criterion Status | Veto Diagnostic Status | Main Uncertainty | Next Justified Action | Not Concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 4 | Passed | No Phase 3 veto fired | Parity fixture is small and fixed-branch only | Implement value+score for the relaxed objective and finite-difference diagnostics | No score correctness, GPU speed, production default, HMC/NeuTra readiness, or posterior validity |

## Handoff To Phase 4

Phase 4 may begin after refreshing the subplan to state:

- the score target is the TensorFlow autodiff gradient of the fixed relaxed batched value objective;
- finite differences use the same fixed tensors and fixed masks;
- finite-difference tolerance is declared before execution;
- `raw` transport gradients are used for finite-difference equivalence checks unless a custom-gradient boundary is explicitly reviewed;
- categorical classical particle-filter score claims remain forbidden.
