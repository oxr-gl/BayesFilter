# P7 Plan: Range-Bearing Validation Result

Date: 2026-05-28

## Evidence Contract

Question: on a fixed Gaussian range-bearing fixture, do UKF, classical bootstrap
PF, and finite-Sinkhorn OT-DPF emit finite, schema-valid, reproducible nonlinear
smoke diagnostics?

Reference/comparators: UKF is approximate reference; classical bootstrap PF is
comparator; OT-DPF is relaxed-resampling candidate.

Primary criterion: finite UKF, PF, and OT-DPF rows; finite weights and summaries;
finite Sinkhorn residuals; shared fixture/model/observation checksums; recorded
seed policy; reproducibility digest; and loose proxy RMSE caps.  The loose caps
are run-validity vetoes only, not ranking metrics.

Veto diagnostics: non-finite values, missing UKF approximate-reference caveat,
angle residual mishandling, malformed JSON, checksum mismatch, or proxy RMSE
promoted to correctness.

Explanatory-only diagnostics: latent state RMSE, UKF residuals, ESS,
resampling count, runtime, and controlled-baseline same-regime context.

What will not be concluded: UKF is not ground truth; proxy RMSE is not posterior
validity; OT-DPF relaxed resampling is not categorical PF equivalence.

## Skeptical Plan Audit Checklist

Check stale context, wrong baseline, proxy overclaim, missing stop conditions,
hidden production drift, monograph drift, vendored-code contamination,
high-dimensional-lane contamination, and artifact fitness.

## Inputs

- P2, P3, and P4 outputs.
- Controlled fixed-grid report as comparison-only context.

## Outputs

- `experiments/dpf_implementation/reports/dpf-ot-range-bearing-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_range_bearing_2026-05-28.json`
- `docs/plans/bayesfilter-dpf-ot-implementation-p7-range-bearing-validation-result-2026-05-28.md`

## Implementation Scope

Execute only the targeted range-bearing runner on the moderate fixture.  No
broad grid or sweep.

## Stop Conditions

Stop if UKF covariance becomes invalid, if OT residuals fail, or if proxy
metrics are used as production/scientific validation.

## Verification Commands

```bash
python -m experiments.dpf_implementation.runners.run_range_bearing_ot_dpf
python -m experiments.dpf_implementation.runners.run_range_bearing_ot_dpf --validate-only
python -m experiments.dpf_implementation.runners.run_range_bearing_ot_dpf --check-reproducibility
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or
five iterations as in the master program.  This exact command is intentional
per user requirement; if unavailable, stop rather than substitute.

## What Must Not Be Concluded

Range-bearing smoke success is proxy-only and does not validate posterior,
HMC, production, model-risk, or monograph claims.

## Review Record

- Iteration 1: `REJECT` as part of bundle review; patched reviewer-gate wording
  and made checksum/seed and loose-cap semantics explicit.
- Iteration 2: `ACCEPT`.
