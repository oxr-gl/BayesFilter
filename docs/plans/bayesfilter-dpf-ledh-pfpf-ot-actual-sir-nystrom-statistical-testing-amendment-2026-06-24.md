# Actual-SIR Nystrom Statistical Testing Amendment

Date: 2026-06-24

Status: `SUPERSEDES_ZERO_FAILURE_STOCHASTIC_REJECTION_RULE_THRESHOLD_CALIBRATION_REQUIRED`

Companion threshold-calibration plan:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-plan-2026-06-24.md`.
This amendment fixes the stochastic interpretation rule; the companion plan
addresses the separate problem that the legacy `5.0` threshold itself is not
principled.

## Purpose

Amend the actual-SIR Nystrom testing plan so stochastic diagnostics are
interpreted statistically.  A single paired log-likelihood threshold exceedance
must not be treated as deterministic algorithm breakage.  Rejection, default
promotion, or repair decisions must use deterministic validity vetoes for
invariants and statistically meaningful criteria for random outcomes.

This amendment supersedes any future interpretation that treats one random seed
with paired log-likelihood delta above `5.0` as a statistically significant
failure by itself.  Historical artifacts remain valid records of what was run,
but their stochastic paired-delta conclusions must be read through this
amendment.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does the fixed-policy Nystrom route have statistically meaningful paired-comparator error beyond an acceptable stochastic error budget? |
| Candidate under test | Compiled TF32 actual-SIR Nystrom route, initially the fixed policy `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=cholesky`. |
| Comparator | Same-artifact compiled streaming TF32 actual-SIR route. |
| Expected stochastic failure mode | Some seeds exceed a paired-delta engineering threshold even when the route is acceptable under a tail-rate or MCSE-aware criterion. |
| Deterministic failure mode | Nonfinite outputs, malformed artifact, wrong route/policy metadata, missing GPU/TF32 evidence, residual invariant failure, comparator failure, or invalid harness. |
| Promotion criterion | Promotion/default-readiness requires deterministic validity plus a predeclared statistical acceptance rule for paired deltas and uncertainty evidence supporting that rule. |
| Rejection criterion | Reject the candidate only if deterministic validity fails, or if a predeclared statistical test rejects the acceptable-error model in a meaningful sense. |
| Continuation veto | Invalid harness/comparator, corrupted artifacts, trusted GPU unavailable for required gates, unsupported default/HMC/posterior claim, or absence of enough statistical evidence to answer a promotion/rejection question. |
| Repair trigger | Repair is triggered by deterministic failures or statistically supported evidence that paired-delta exceedance behavior is beyond the acceptable error budget. |
| Must not conclude | No statistical rejection from one exceedance; no default readiness from a small passing seed panel; no superiority, posterior correctness, HMC readiness, or failure-probability claim without uncertainty evidence. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Is Nystrom's paired-comparator behavior acceptable under a statistical error model, not a zero-failure seed rule? |
| Exact baseline | Same-artifact compiled streaming TF32 actual-SIR route, same observations, seed policy, dtype, TF32 mode, transport policy, and trusted GPU provenance. |
| Deterministic veto diagnostics | Nonfinite route output, nonfinite Nystrom factors/particles, residual threshold failure, missing/malformed artifacts, wrong policy metadata, comparator failure, trusted GPU/TF32 mismatch, route mismatch, unsupported backend. |
| Stochastic diagnostics | Per-seed paired signed delta, absolute delta, indicator `abs(delta)>tau_practical`, seed-panel mean/quantiles, MCSE or bootstrap/interval estimates where available.  Legacy `5.0` may be reported only as a legacy diagnostic until calibrated. |
| Stochastic rejection rule | Must be predeclared in the subplan after threshold calibration.  Acceptable examples: binomial exceedance-rate test, one-sided confidence bound on exceedance probability, paired-delta mean/quantile bootstrap interval, or MCSE-calibrated tolerance. |
| Explanatory only | Runtime, warm ratios, ESS, residual magnitudes below threshold, factor/scaling diagnostics, descriptive seed-panel SD without a predeclared decision rule. |
| Not concluded | A stochastic threshold exceedance alone does not prove algorithm breakage, scientific invalidity, posterior error, or default unsuitability. |
| Artifact | This amendment plus a future statistical calibration/validation subplan and result note. |

## Deterministic Versus Stochastic Gates

| Diagnostic class | Examples | Decision role |
| --- | --- | --- |
| Deterministic validity veto | Nonfinite outputs, malformed JSON, wrong policy metadata, missing GPU/TF32 evidence, comparator route failure, residual invariant failure | Immediate hard veto for the affected artifact/gate. |
| Stochastic paired-comparator evidence | Paired log-likelihood delta, filtered-summary deltas, threshold exceedance counts across seeds | Statistical evidence only; interpret through a predeclared uncertainty model. |
| Descriptive support | Observed means, SDs, quantiles, one-seed deltas, runtime ratios | Useful for planning and calibration; not sufficient for rejection or promotion. |

## Current N8192 Evidence Reinterpreted

Existing unique fixed-policy `N=8192` artifacts have 12 seeds and one
legacy `abs(delta)>5.0` exceedance:

- observed exceedance count: `1 / 12`;
- observed exceedance rate: `0.08333333333333333`;
- one-sided 95% binomial upper confidence bound for exceedance probability:
  approximately `0.33868066843403255`;
- probability of at least one exceedance in 12 seeds if true exceedance
  probability is `0.05`: approximately `0.4596399123373629`;
- probability of at least one exceedance in 12 seeds if true exceedance
  probability is `0.10`: approximately `0.7175704635190003`.

Interpretation:

- The single seed `82921` exceedance is not statistically significant evidence
  against a 5% or 10% tail-exceedance model.
- The current 12-seed panel is also too small to certify a low exceedance rate:
  with one exceedance, the one-sided 95% upper bound is about `0.34`.
- Therefore the current evidence supports neither statistical rejection nor
  default certification.  It supports continued statistical calibration.

## Revised Decision Rules For Future Plans

Future actual-SIR Nystrom promotion or rejection plans must use rules of this
form:

0. First calibrate or explicitly justify the paired-delta threshold.  Do not
   treat legacy `5.0` as principled without the companion threshold-calibration
   workflow.
1. First apply deterministic validity vetoes.  Any deterministic veto blocks
   interpretation until the artifact or implementation issue is repaired.
2. If deterministic validity passes, treat paired-delta exceedances as random.
3. Predeclare an acceptable stochastic error budget, such as:
   - exceedance probability for `abs(delta)>tau_practical` must be below a chosen bound;
   - paired-delta mean or high quantile must be below a chosen bound with a
     one-sided confidence interval;
   - paired-delta magnitude must be small relative to a calibrated MCSE or
     downstream posterior/reference tolerance.
4. Reject only when the predeclared statistical test rejects the acceptable
   model at the chosen level.
5. Promote only when the predeclared statistical acceptance criterion is met
   with enough uncertainty evidence for the intended scope.

## Suggested Next Statistical Validation Phase

Draft a dedicated subplan before execution with one of these primary criteria.

Recommended first statistical gate after threshold calibration:

- run a seed panel large enough to bound the exceedance probability for
  `abs(delta)>tau_practical`, where `tau_practical` is frozen by the companion
  threshold-calibration workflow;
- use a one-sided 95% binomial confidence bound;
- do not reject from isolated exceedances;
- do not certify default readiness unless the upper confidence bound is below
  the predeclared acceptable tail rate.

Example sample-size guide for a 10% acceptable exceedance-probability bound:

- `0` exceedances need about `29` valid seeds for a one-sided 95% upper bound
  below `0.10`;
- `1` exceedance needs about `46` valid seeds;
- `2` exceedances need about `61` valid seeds;
- `3` exceedances need about `76` valid seeds.

These are planning numbers, not a command to run immediately.  A future subplan
must choose the actual acceptable tail rate, seed count, runtime budget, GPU
policy, artifacts, and stop conditions before launching.

## Forbidden Claims And Actions

- Do not call seed `82921` statistically significant breakage from the current
  12-seed panel.
- Do not reject Nystrom from a single stochastic threshold exceedance.
- Do not promote Nystrom to default from a small panel with no uncertainty
  bound.
- Do not relax thresholds after seeing failures to rescue a candidate.
- Do not treat descriptive SD, q90, max, ESS, or runtime as a promotion or
  rejection criterion unless the subplan predeclares the statistical rule.

## Handoff

Future Nystrom runbooks should add a statistical validation phase before any
default-readiness or rejection packet.  The old G5 conclusion should be read as:

`NOT_STATISTICALLY_CERTIFIED_FOR_DEFAULT`, not
`STATISTICALLY_REJECTED_OR_BROKEN`.
