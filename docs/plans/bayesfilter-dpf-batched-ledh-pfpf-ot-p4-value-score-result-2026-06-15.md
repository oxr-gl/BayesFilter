# Phase 4 Result: Batched Value+Score

Date: 2026-06-15

## Status

`PASSED_WITH_BOUNDARY_REPAIR`

## Research Intent Ledger

| Field | Entry |
| --- | --- |
| Main question | Does TensorFlow autodiff produce finite row-local scores for the relaxed batched LEDH-PFPF-OT objective? |
| Candidate/mechanism | Experimental value+score wrapper differentiating the sum of row-local relaxed batched values with respect to `theta_batch`. |
| Expected failure mode | Active annealed transport backward semantics may not equal central finite differences because transport contains intentional `stop_gradient` / custom-gradient boundaries. |
| Promotion criterion | Score shape `[B,p]`, finite scores, active-transport row-locality, CPU graph smoke, and no-resampling finite-difference agreement within `rtol=2e-4, atol=2e-4`. |
| Promotion veto | Nonfinite score, cross-row gradient leakage, no-resampling finite-difference mismatch, runtime stochastic branch, or categorical PF-gradient claim. |
| Repair trigger | Active-transport finite-difference mismatch while no-resampling finite differences pass. |
| What must not be concluded | No classical particle-filter likelihood score, no active-transport FD equivalence, no HMC/NeuTra readiness, no posterior validity, no GPU performance, no public API/default readiness. |

## Evidence Contract Status

| Contract Item | Status |
| --- | --- |
| Score target | TensorFlow autodiff gradient of `sum(value(theta_batch))` for the fixed relaxed batched objective. |
| Comparator | Central finite differences on no-resampling fixed deterministic fixture. |
| Primary criterion | Passed after boundary repair: focused CPU tests passed. |
| Veto diagnostics | No nonfinite score, no row cross-talk, no no-resampling FD mismatch, no RNG/ESS branch introduced. |
| Explanatory diagnostics | Active-transport raw autodiff vs central finite difference showed max delta about `4.33e-3`; no-resampling fixture max delta was about `5e-11`. |
| Non-claims | Active transport FD equivalence, classical PF likelihood-gradient correctness, HMC/NeuTra readiness, GPU performance, production/default readiness remain unclaimed. |

## Actions

- Added `BatchedLEDHPFPFOTValueScoreTensors`.
- Added `batched_ledh_pfpf_ot_value_and_score_tf`.
- Added deterministic theta-driven fixture tests for value+score shape,
  finiteness, CPU `tf.function` graph parity, no-resampling finite differences,
  active-transport row locality, and source boundary checks.
- Repaired the Phase 4 subplan after local diagnostics showed active transport
  has a different backward contract from central finite differences.
- Obtained Claude read-only review for both the original boundary and the
  repaired boundary.

## Checks Run

```text
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_ledh_pfpf_ot_tf.py
```

Result:

```text
20 passed, 5095 warnings in 17.51s
```

```text
git diff --check -- experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py docs/plans/bayesfilter-dpf-batched-ledh-pfpf-ot-p4-value-score-subplan-2026-06-15.md
```

Result: passed with no output.

## Claude Review

Initial boundary review:

```text
VERDICT: AGREE
```

Repair review:

```text
VERDICT: AGREE
```

Claude agreed that the repaired no-resampling finite-difference gate plus
active-transport finiteness/row-locality gate is methodologically sound under
the stated nonclaims.

## Decision Table

| Decision | Primary Criterion Status | Veto Diagnostic Status | Main Uncertainty | Next Justified Action | Not Concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 5 with benchmark boundaries | Passed after boundary repair | No Phase 4 continuation veto fired | Active transport has a separate backward contract from value finite differences | Benchmark compiled value/value+score behavior as experimental, with JIT/device metadata and no production claim | Active-transport FD equivalence, classical PF score, HMC/NeuTra readiness, GPU speedup, production/default readiness |

## Handoff To Phase 5

Phase 5 may benchmark experimental value and value+score only after the
benchmark subplan predeclares:

- JIT/compiled-only timing for GPU comparisons;
- CPU-only correctness rerun before benchmarks;
- device metadata and compile/warm-call separation;
- no active-transport finite-difference equivalence claim;
- no speedup or production claim without the artifact supporting it.
