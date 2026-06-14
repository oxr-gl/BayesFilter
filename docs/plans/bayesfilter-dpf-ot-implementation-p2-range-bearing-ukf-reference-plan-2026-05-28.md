# P2 Plan: Range-Bearing Fixture And UKF Reference

Date: 2026-05-28

## Evidence Contract

Question: can the lane define a clean-room Gaussian range-bearing fixture and
UKF approximate reference for a bounded nonlinear DPF smoke?

Comparator/reference: UKF on the same fixed fixture, labeled approximate.

Primary criterion: UKF produces finite filtered means, covariances, innovation
statistics, and state summaries on the fixed fixture.

Veto diagnostics: non-finite UKF values, non-PSD covariance after stabilization,
angle residual mishandling, missing approximate-reference caveat, or imports
from controlled/student/vendored code.

Explanatory-only diagnostics: latent RMSE, observation RMSE, and comparison to
controlled-baseline reports.

What will not be concluded: UKF is not ground truth and cannot validate OT-DPF
posterior correctness.

## Skeptical Plan Audit Checklist

Check stale context, wrong baseline, proxy overclaim, missing stop conditions,
hidden production drift, monograph drift, vendored-code contamination,
high-dimensional-lane contamination, and artifact fitness.

## Inputs

- `experiments/controlled_dpf_baseline/fixtures/range_bearing.py` as clean-room
  fixture reference, not implementation authority.
- Controlled fixed-grid result as proxy-only context.
- DPF5 validation harness spec.

## Outputs

- `experiments/dpf_implementation/fixtures/range_bearing.py`
- `experiments/dpf_implementation/references/ukf.py`
- `docs/plans/bayesfilter-dpf-ot-implementation-p2-range-bearing-ukf-reference-result-2026-05-28.md`

## Implementation Scope

Add local fixture and UKF reference under `experiments/dpf_implementation/`.
Do not import from controlled/student/vendored paths in implementation code.

## Stop Conditions

Stop if the UKF cannot maintain finite covariance, if angle wrapping is absent,
or if a result would call UKF ground truth.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/fixtures/range_bearing.py experiments/dpf_implementation/references/ukf.py
python -c "from experiments.dpf_implementation.fixtures.range_bearing import make_fixture; from experiments.dpf_implementation.references.ukf import run_range_bearing_ukf; f=make_fixture('range_bearing_gaussian_moderate'); r=run_range_bearing_ukf(f); print(f.horizon, r.filtered_means.shape, r.approximate_reference)"
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or
five iterations as in the master program.  This exact command is intentional
per user requirement; if unavailable, stop rather than substitute.

## What Must Not Be Concluded

No exact nonlinear reference, production readiness, posterior correctness, HMC
readiness, or monograph claim follows from UKF finite outputs.

## Review Record

- Iteration 1: `REJECT` as part of bundle review; patched reviewer-gate wording.
- Iteration 2: `ACCEPT`.
