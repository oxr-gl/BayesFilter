# P6 Result: Integrated LEDH-PF-PF-OT Runner

Date: 2026-05-29

## Decision

`P6_INTEGRATED_LEDH_PFPF_OT_RUNNER_ACCEPTED`

## Files

- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_ledh_pfpf_ot_tf.py`

## Result

Implemented an integrated experimental TF/TFP LEDH-PF-PF-OT filter with:

- bootstrap transition pre-flow proposal `q0`;
- local LEDH transport proposal;
- target transition and observation densities at post-flow particles;
- PF-PF corrected log weights;
- ESS and weighted moments;
- finite Sinkhorn/entropic OT relaxed resampling;
- JSON/reporting runners for LGSSM and range-bearing fixtures.

## Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| default architecture | pass | LEDH-PF-PF-OT is implemented as the main path. |
| bootstrap overclaim | pass | Bootstrap PF and bootstrap OT-DPF remain comparators. |
| OT overclaim | pass | Sinkhorn is relaxed resampling, not proposal correction. |
| missing stop conditions | pass | Corrected-weight, log-det, and Sinkhorn failures veto. |
| drift/contamination | pass | No production, monograph, vendored, or high-dimensional lane edits. |

## Verification

- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ledh_pfpf_ot_tf`: pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ledh_pfpf_ot_tf`: pass.
- `python -m py_compile` over touched runner/filter files: pass.

## What Is Not Concluded

No production/API readiness, HMC readiness, posterior correctness,
NAWM-scale readiness, or monograph claim.
