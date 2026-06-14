# P6 Plan: Integrated LEDH-PF-PF-OT Runner

Date: 2026-05-29

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: can the TF/TFP LEDH flow be integrated as a PF-PF proposal-corrected
filter with finite Sinkhorn/entropic OT resampling?

Baseline/comparator: existing TF bootstrap PF and bootstrap OT-DPF runners.

Pass criterion: filter records pre-flow proposal density, target density,
forward log-det, corrected weights, ESS, finite diagnostics, and Sinkhorn
residuals.

Veto diagnostics: non-finite corrected weights, missing density field, invalid
Sinkhorn residual, branch requiring NumPy, or comparator promotion.

Not concluded: production readiness, posterior correctness, HMC readiness,
large-model readiness.

## Inputs

- P1-P5 results.
- `experiments/dpf_implementation/tf_tfp/filters/bootstrap_pf_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py`

## Outputs

- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_ledh_pfpf_ot_tf.py`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p6-integrated-ledh-pfpf-ot-runner-result-2026-05-29.md`

## Allowed Write Set

- listed output files;
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*-2026-05-29.md`
- `experiments/dpf_implementation/reports/dpf-ledh-pfpf-ot-tf-tfp-*-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_ot_tf_tfp_*.json`

## Forbidden Write Set

Production code, vendored code, monograph chapters, high-dimensional lane
artifacts, and NumPy algorithm paths.

## Skeptical Audit Checklist

Check stale context, wrong default architecture, bootstrap-proposal overclaim,
OT-resampling overclaim, missing stop conditions, hidden production drift,
monograph drift, vendored-code contamination, high-dimensional-lane
contamination, and artifact fitness.

## Stop Conditions

Stop if corrected weights cannot be normalized, if densities/log-det are not
recorded, if Sinkhorn fails, or if CPU-only import discipline cannot be kept.

## Verification Commands

- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ledh_pfpf_ot_tf`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ledh_pfpf_ot_tf`
- `python -m py_compile experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/runners/run_lgssm_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_ledh_pfpf_ot_tf.py`

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to max five
iterations with Codex audit.

## What Must Not Be Concluded

No production, public API, HMC, posterior, NAWM-scale, or monograph claim.
