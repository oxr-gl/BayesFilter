# P4 Plan: Integrated Bootstrap PF And OT-DPF Runners

Date: 2026-05-28

## Evidence Contract

Question: can the lane wire reusable experimental bootstrap PF and OT-DPF value
paths for LGSSM and range-bearing fixtures without production or vendored code?

Comparator: classical bootstrap PF for the same model and seed policy; later P6
and P7 references are Kalman and UKF.

Primary criterion: filter modules and runners compile, preserve CPU-only
discipline, return finite structured rows, and record relaxed-resampling caveats.

Veto diagnostics: non-finite weights, silent zero mass, missing resampling
method, missing Sinkhorn residuals for OT rows, missing seed/device/dtype, or
student/vendored/production imports.

Explanatory-only diagnostics: ESS, resampling count, runtime, proxy RMSE.

What will not be concluded: no accuracy, posterior, gradient, HMC, production,
or monograph validation until P6-P8.

## Skeptical Plan Audit Checklist

Check stale context, wrong baseline, proxy overclaim, missing stop conditions,
hidden production drift, monograph drift, vendored-code contamination,
high-dimensional-lane contamination, and artifact fitness.

## Inputs

- P1 LGSSM/Kalman fixture and P2 range-bearing/UKF fixture.
- P3 finite Sinkhorn resampler.
- DPF1 and DPF2 specs.

## Outputs

- `experiments/dpf_implementation/filters/__init__.py`
- `experiments/dpf_implementation/filters/bootstrap_pf.py`
- `experiments/dpf_implementation/filters/dpf_ot.py`
- `experiments/dpf_implementation/runners/run_lgssm_ot_dpf.py`
- `experiments/dpf_implementation/runners/run_range_bearing_ot_dpf.py`
- `docs/plans/bayesfilter-dpf-ot-implementation-p4-integrated-dpf-runner-result-2026-05-28.md`

## Implementation Scope

Implement clean-room NumPy bootstrap PF and finite-Sinkhorn OT-DPF runners.
Runners may write JSON/report artifacts only when executed by P6/P7.

## Stop Conditions

Stop if model callables cannot be made explicit, likelihood semantics are
ambiguous, or OT rows cannot report finite residual diagnostics.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/filters/__init__.py experiments/dpf_implementation/filters/bootstrap_pf.py experiments/dpf_implementation/filters/dpf_ot.py experiments/dpf_implementation/runners/run_lgssm_ot_dpf.py experiments/dpf_implementation/runners/run_range_bearing_ot_dpf.py
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or
five iterations as in the master program.  This exact command is intentional
per user requirement; if unavailable, stop rather than substitute.

## What Must Not Be Concluded

P4 wiring does not validate numerical behavior.  P6 and P7 must execute the
model-specific evidence contracts.

## Review Record

- Iteration 1: `REJECT` as part of bundle review; patched reviewer-gate wording.
- Iteration 2: `ACCEPT`.
