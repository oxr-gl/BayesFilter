# P52-M3 Result: UKF Scouting And Centering Protocol

metadata_date: 2026-06-10
phase: P52-M3
status: PASS_P52_M3_UKF_SCOUTING
supervisor: Codex
reviewer: Claude Code read-only

## Decision

P52-M3 passes after repair, local validation, and Claude read-only review.
BayesFilter now has a deterministic UKF scout protocol for spatial SIR
dimensions 18, 50, and 100.  The scout emits centers, scales, covariance
spectra, effective-dimension paths, local-correlation summaries, sigma-point
counts, covariance-assumption metadata, lower-rung sanity-comparator metadata,
and explicit `scout_not_truth` claim labels.

This phase is scout metadata only.  It does not establish a Zhao-Cui filtering
likelihood, filtering correctness, exact likelihood, production spatial SIR
readiness, HMC readiness, GPU readiness, or d=100 filtering correctness.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | UKF provides deterministic centers, scales, covariance diagnostics, and effective-dimension summaries for spatial SIR d=18/d=50/d=100. |
| Baseline/comparator | Existing spatial SIR model equations, P30 M1 UKF scout equations, and P52-M2 rank-budget boundaries. |
| Primary criterion | Passed locally: UKF scout produces finite means/covariances and a manifest of center, scale, covariance-spectrum, local-correlation, and sigma-point diagnostics for each requested dimension. |
| Veto diagnostics | Passed locally: UKF cannot promote truth/correctness/HMC claims, UKF nonclaims are in results and manifest, and d=100 remains scout evidence. |
| Not concluded | No Zhao-Cui filtering correctness, no exact likelihood, no HMC readiness, and no d=100 filtering correctness. |

## Implementation

Added:

- `bayesfilter/highdim/ukf_scout.py`
- internal `bayesfilter.highdim` exports for the UKF scout protocol
- `tests/highdim/test_p52_ukf_scout.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p52-m3-ukf-scouting-manifest-2026-06-10.json`

The manifest intentionally stores compact summaries rather than full
covariance tensors: final center head/tail, final scale range, final covariance
eigenvalue range, effective-dimension path, maximum absolute correlation path,
sigma-point count, covariance-assumption shapes/ranges, and lower-rung sanity
comparator metadata.

## Manifest Summary

| d | sites | sigma points | effective dimension path | final max abs correlation | claim class |
| --- | ---: | ---: | --- | ---: | --- |
| 18 | 9 | 37 | 18, 18 | 0.5912766842218832 | scout_not_truth |
| 50 | 25 | 101 | 50, 50 | 0.6380579742296284 | scout_not_truth |
| 100 | 50 | 201 | 100, 100 | 0.7084447634812308 | scout_not_truth |

These diagnostics are scale and design aids only.  The d=100 row is not a
filtering run.

The lower-rung sanity comparator recorded in the manifest is the prior
J=1/d=2 spatial SIR Zhao-Cui value/moment diagnostic against dense reference.
It is included only to preserve the subplan comparator trail.  It is not a
d=18 dense reference, not UKF correctness, not production spatial SIR
readiness, and not HMC readiness.

## Validation

Focused CPU-only validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p52_ukf_scout.py
python -m compileall -q bayesfilter/highdim/ukf_scout.py tests/highdim/test_p52_ukf_scout.py
git diff --check -- bayesfilter/highdim/ukf_scout.py bayesfilter/highdim/__init__.py tests/highdim/test_p52_ukf_scout.py docs/plans/bayesfilter-highdim-zhao-cui-p52-m3-ukf-scouting-manifest-2026-06-10.json
```

Outcomes after the repair prompted by Claude review iteration 1:

- pytest passed: `5 passed, 2 warnings in 3.15s`;
- compileall passed;
- git diff whitespace check passed.

The warnings came from TensorFlow Probability deprecation messages during the
existing broad `bayesfilter.highdim` import path.  GPU was intentionally hidden
with `CUDA_VISIBLE_DEVICES=-1`; no GPU claim is made.

Claude read-only review iteration 1 returned `VERDICT: REVISE`.  Claude found
that the initial M3 artifacts did not preserve the process/observation
covariance choices required by the subplan, and that the lower-rung sanity
comparator named in the subplan was not recorded.  The repair added covariance
metadata and the scoped J=1 lower-rung sanity comparator to the scout manifest,
implementation payload, tests, result, and ledger.

Claude read-only review iteration 2 returned `VERDICT: AGREE`.  Claude found
that the covariance choices are now persisted, the J=1/d=2 sanity comparator is
restored and scoped correctly, UKF remains `scout_not_truth`, and d=100 remains
scout evidence only.

## Nonclaims

- No filtering correctness.
- No exact likelihood.
- No production spatial SIR readiness.
- No HMC readiness.
- No GPU readiness.
- No d=100 filtering correctness.
- No claim that UKF is a correctness oracle for Zhao-Cui filtering.
