# P6 Plan: LGSSM Validation Result

Date: 2026-05-28

## Evidence Contract

Question: on a fixed LGSSM, do classical bootstrap PF and finite-Sinkhorn
OT-DPF relaxed resampling emit finite, schema-valid, reproducible diagnostics
against the Kalman reference?

Reference/comparators: Kalman reference is independent analytic reference;
classical bootstrap PF is comparator; OT-DPF is candidate relaxed path.

Primary criterion: finite rows, finite weights, finite filtered means, finite
log-likelihood estimates, finite Sinkhorn residuals for OT rows, shared
fixture/model/observation checksums, recorded seed policy, reproducibility
digest, and loose smoke residual caps to Kalman.  The loose caps are run-validity
vetoes only, not ranking metrics.

Veto diagnostics: non-finite values, missing Kalman reference, malformed JSON,
checksum mismatch, missing relaxed-resampling caveat, or proxy overclaim.

Explanatory-only diagnostics: particle-count differences, ESS, resampling
counts, runtime, and one-fixture Monte Carlo differences.

What will not be concluded: no statistical convergence, production readiness,
posterior correctness, HMC readiness, learned/neural OT, or monograph validity.

## Skeptical Plan Audit Checklist

Check stale context, wrong baseline, proxy overclaim, missing stop conditions,
hidden production drift, monograph drift, vendored-code contamination,
high-dimensional-lane contamination, and artifact fitness.

## Inputs

- P1, P3, and P4 outputs.

## Outputs

- `experiments/dpf_implementation/reports/dpf-ot-lgssm-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_lgssm_2026-05-28.json`
- `docs/plans/bayesfilter-dpf-ot-implementation-p6-lgssm-validation-result-2026-05-28.md`

## Implementation Scope

Execute only the targeted LGSSM runner.  No sweeps.

## Stop Conditions

Stop if Kalman comparison cannot be computed, if OT residuals fail the declared
threshold, or if the result would treat relaxed OT-DPF as categorical PF.

## Verification Commands

```bash
python -m experiments.dpf_implementation.runners.run_lgssm_ot_dpf
python -m experiments.dpf_implementation.runners.run_lgssm_ot_dpf --validate-only
python -m experiments.dpf_implementation.runners.run_lgssm_ot_dpf --check-reproducibility
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or
five iterations as in the master program.  This exact command is intentional
per user requirement; if unavailable, stop rather than substitute.

## What Must Not Be Concluded

LGSSM smoke success is not nonlinear validation, exact DPF likelihood validity,
posterior correctness, HMC readiness, or production readiness.

## Review Record

- Iteration 1: `REJECT` as part of bundle review; patched reviewer-gate wording
  and made checksum/seed and loose-cap semantics explicit.
- Iteration 2: `ACCEPT`.
