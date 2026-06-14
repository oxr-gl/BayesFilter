# P1 Plan: LGSSM Fixture And Kalman Reference

Date: 2026-05-28

## Evidence Contract

Question: can the experimental lane define a deterministic LGSSM fixture and
independent Kalman reference for later bootstrap PF and OT-DPF validation?

Baseline/reference: analytic Kalman filter for the same simulated LGSSM.

Primary criterion: fixture and Kalman code emit finite filtered means,
covariances, innovations, and log likelihood for fixed observations.

Veto diagnostics: non-finite reference values, inconsistent dimensions,
unstable covariance update, missing seed/model checksum, or production imports.

Explanatory-only diagnostics: fixture latent RMSE and observation summaries.

What will not be concluded: no particle-filter, OT-DPF, gradient, production,
posterior, or HMC validity.

## Skeptical Plan Audit Checklist

Check stale context, wrong baseline, proxy overclaim, missing stop conditions,
hidden production drift, monograph drift, vendored-code contamination,
high-dimensional-lane contamination, and artifact fitness.

## Inputs

- DPF1 classical PF spec.
- IE3 linear-Gaussian recovery result.

## Outputs

- `experiments/dpf_implementation/fixtures/lgssm.py`
- `experiments/dpf_implementation/references/kalman_lgssm.py`
- `docs/plans/bayesfilter-dpf-ot-implementation-p1-lgssm-fixture-and-kalman-reference-result-2026-05-28.md`

## Implementation Scope

Add a small linear Gaussian state-space fixture with fixed seed and an
independent Kalman reference.  No runner execution beyond import/compile checks.

## Stop Conditions

Stop if the fixture cannot be simulated deterministically, the Kalman reference
does not produce finite outputs, or code would import production/vendored paths.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/fixtures/lgssm.py experiments/dpf_implementation/references/kalman_lgssm.py
python -c "from experiments.dpf_implementation.fixtures.lgssm import build_lgssm_fixture; from experiments.dpf_implementation.references.kalman_lgssm import run_kalman_filter; f=build_lgssm_fixture(); r=run_kalman_filter(f); print(f.horizon, r.log_likelihood)"
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or
five iterations as in the master program.  This exact command is intentional
per user requirement; if unavailable, stop rather than substitute.

## What Must Not Be Concluded

The Kalman fixture is an independent reference for LGSSM only.  It does not
validate nonlinear models, OT resampling, DPF gradients, HMC, or production use.

## Review Record

- Iteration 1: `REJECT` as part of bundle review; patched reviewer-gate wording.
- Iteration 2: `ACCEPT`.
