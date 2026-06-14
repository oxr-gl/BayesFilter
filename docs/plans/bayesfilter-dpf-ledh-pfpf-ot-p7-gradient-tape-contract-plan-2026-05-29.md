# P7 Plan: GradientTape Contract

Date: 2026-05-29

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: can the LEDH-PF-PF-OT path expose a named scalar whose
`tf.GradientTape` gradient matches a finite-difference reference under fixed
observations and common random numbers?

Baseline/comparator: existing OT-DPF GradientTape smoke pattern.

Pass criterion: result records scalar id, same-scalar contract, GradientTape
gradient, finite-difference reference, absolute/relative error, and caveats.

Veto diagnostics: value and gradient use different scalars, non-finite
gradient, finite-difference mismatch above tolerance, stochastic seeds not
fixed, or HMC/posterior overclaim.

Not concluded: HMC readiness, posterior score correctness, production
readiness, NAWM-scale readiness.

## Inputs

- P5-P6 implementation.
- `experiments/dpf_implementation/tf_tfp/runners/run_gradient_checks_tf.py`

## Outputs

- `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_gradient_checks_tf.py`
- `experiments/dpf_implementation/reports/dpf-ledh-pfpf-ot-tf-tfp-gradient-check-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_ot_tf_tfp_gradient_check_2026-05-29.json`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-p7-gradient-tape-contract-result-2026-05-29.md`

## Allowed Write Set

- listed output files;
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*-2026-05-29.md`

## Forbidden Write Set

Production code, vendored code, monograph chapters, high-dimensional lane
artifacts, and NumPy algorithm paths.

## Skeptical Audit Checklist

Check stale context, wrong default architecture, bootstrap-proposal overclaim,
OT-resampling overclaim, missing stop conditions, hidden production drift,
monograph drift, vendored-code contamination, high-dimensional-lane
contamination, and artifact fitness.

## Stop Conditions

Stop if the same-scalar contract cannot be enforced, if GradientTape returns
`None`, if finite differences cannot be computed on the same scalar, or if the
result would imply HMC readiness.

## Verification Commands

- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_gradient_checks_tf`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_gradient_checks_tf --validate-only`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_gradient_checks_tf --check-reproducibility`

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to max five
iterations with Codex audit.

## What Must Not Be Concluded

No HMC readiness, posterior correctness, production, public API, NAWM-scale, or
monograph claim.
