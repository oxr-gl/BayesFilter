# P5 Plan: Gradient Contract And Same-Scalar Check

Date: 2026-05-28

## Evidence Contract

Question: can the lane test a named relaxed OT-DPF scalar under a same-scalar
gradient contract with fixed observations and common random numbers?

Scalar: `lgssm_relaxed_ot_log_normalizer_proxy`, the negative sum of incremental
log normalizers for a small LGSSM OT-DPF path with finite Sinkhorn relaxed
resampling and fixed base noise.

Comparator: central finite differences for the same scalar.  If a CPU-only
autodiff backend is available, compare autodiff gradient to finite differences;
otherwise record a finite-difference-only structured blocker.

Primary criterion: finite scalar, common-random-number finite-difference
gradient, same-scalar digest agreement, and a structured gradient-status label.
If CPU-only autodiff is available and used, autodiff must also match finite
differences within declared tolerance.  If no autodiff backend is used, the
phase may pass only as `finite_difference_same_scalar_passed`, not as autodiff
gradient validation.

Veto diagnostics: value/gradient scalar mismatch, non-finite values, changing
randomness across perturbations, importing GPU before `CUDA_VISIBLE_DEVICES=-1`,
or promoting the gradient to posterior/HMC validity.

Explanatory-only diagnostics: gradient norm and runtime.

What will not be concluded: no HMC readiness, posterior correctness, production
readiness, unbiased likelihood score, or monograph claim.

## Skeptical Plan Audit Checklist

Check stale context, wrong baseline, proxy overclaim, missing stop conditions,
hidden production drift, monograph drift, vendored-code contamination,
high-dimensional-lane contamination, and artifact fitness.

## Inputs

- DPF4 gradient contract.
- P1 LGSSM fixture.
- P3/P4 OT-DPF value path.

## Outputs

- `experiments/dpf_implementation/runners/run_gradient_checks.py`
- `experiments/dpf_implementation/reports/dpf-ot-gradient-check-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_gradient_check_2026-05-28.json`
- `docs/plans/bayesfilter-dpf-ot-implementation-p5-gradient-contract-and-finite-difference-result-2026-05-28.md`

## Implementation Scope

Start with a finite-difference-only same-scalar check.  CPU-only PyTorch may be
used only if it stays bounded and imports after `CUDA_VISIBLE_DEVICES=-1`; if it
is not used or is unavailable, record `autodiff_not_tested` as an unresolved
risk, not a blocker.  Do not run HMC chains.

## Stop Conditions

Stop if common random numbers cannot be fixed, the scalar cannot be named,
finite differences are non-finite/unstable, or an autodiff path would require a
forbidden dependency or broad experiment.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/runners/run_gradient_checks.py
python -m experiments.dpf_implementation.runners.run_gradient_checks
python -m experiments.dpf_implementation.runners.run_gradient_checks --validate-only
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or
five iterations as in the master program.  This exact command is intentional
per user requirement; if unavailable, stop rather than substitute.

## What Must Not Be Concluded

Finite same-scalar gradient parity is not posterior validity, HMC validity, or
a production score API.

## Review Record

- Iteration 1: `REJECT` as part of bundle review; patched reviewer-gate wording
  and resolved autodiff/finite-difference ambiguity.
- Iteration 2: `ACCEPT`.
