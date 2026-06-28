# Actual-SIR Nystrom Threshold Calibration Plan

Date: 2026-06-24

Status: `THRESHOLD_CALIBRATION_PLAN_READY_REVIEW_BEFORE_EXECUTION`

## Purpose

Replace the inherited paired log-likelihood threshold `5.0` with a principled
calibration workflow.  The current `5.0` value is a legacy engineering screen
from earlier low-rank actual-SIR validation.  It is not derived from MCSE,
downstream posterior sensitivity, or a predeclared practical equivalence
margin.

This plan does not relax or tighten thresholds by itself.  It defines how a
future threshold must be chosen before promotion, rejection, or repair decisions
use paired log-likelihood deltas.

## Phase Objective

Calibrate a justified paired log-likelihood tolerance for the actual-SIR
Nystrom route by separating:

- measurement noise in the comparator filter;
- Nystrom approximation error relative to the comparator;
- downstream practical tolerance for the intended use.

## Entry Conditions

- The statistical testing amendment exists:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-statistical-testing-amendment-2026-06-24.md`.
- Existing `N=8192` artifacts show `1/12` unique seeds with
  `abs(paired_delta)>5.0`, but this is not statistically significant breakage.
- The fixed-policy candidate remains:
  `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=cholesky`.
- GPU policy remains: trusted GPU context, physical GPU1 if available,
  otherwise GPU0 with fallback note.

## Why The Legacy Threshold Is Not Enough

The legacy total-log-likelihood threshold `5.0` has interpretable scales:

- total log-likelihood delta: `5.0`;
- per time step for `T=20`: `0.25`;
- per observed component for `T=20,M=9`: about `0.027777777777777776`.

Those scales are not obviously impossible, but they are not a derivation.
Existing `N=8192` artifacts also suggest that the streaming comparator's
across-seed total log-likelihood SD is much smaller than `5.0`:

- streaming total log-likelihood SD across 12 unique seeds: about `0.375`;
- paired Nystrom-minus-streaming delta SD across the same seeds: about `3.244`;
- absolute paired delta mean: about `2.916`;
- absolute paired delta max: about `6.968`.

Therefore `5.0` should not be described as an MCSE-calibrated tolerance.  It is
closer to a practical engineering margin on total log likelihood, and that
margin still needs a principled justification.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What paired log-likelihood tolerance is justified for actual-SIR Nystrom validation? |
| Baseline/comparator | Same-artifact compiled streaming TF32 actual-SIR route; optional higher-fidelity comparator only if separately planned. |
| Candidate | Compiled TF32 actual-SIR Nystrom fixed policy. |
| Primary output | A calibrated threshold rule or an explicit blocker saying the threshold cannot be justified yet. |
| Deterministic veto diagnostics | Nonfinite outputs, malformed artifacts, wrong route/policy metadata, residual failure, comparator failure, GPU/TF32 mismatch, or harness invalidity. |
| Stochastic diagnostics | Streaming seed SD/MCSE proxy, Nystrom-minus-streaming paired deltas, per-time and per-observed-component normalized deltas, bootstrap or binomial confidence intervals. |
| Explanatory only | Runtime, ESS, residual magnitudes below deterministic thresholds, factor/scaling diagnostics. |
| Not concluded | No default readiness, no posterior correctness, no HMC readiness, no statistical superiority, and no final threshold without calibration result and review. |

## Skeptical Plan Audit

| Risk | Audit |
| --- | --- |
| Wrong baseline | Streaming TF32 is the operational comparator, not truth.  Any claim of posterior correctness requires a separate reference/oracle plan. |
| Proxy threshold | `5.0` cannot remain a promotion threshold merely because it was inherited. |
| MCSE confusion | Comparator MCSE estimates measurement uncertainty; they do not by themselves define practical harmlessness. |
| Downstream mismatch | A threshold suitable for a value-only engineering route may be too loose for posterior/HMC use. |
| Post-hoc rescue | The threshold must be frozen before validation seeds are interpreted. |
| Underpowered validation | If uncertainty bounds cannot separate acceptable from unacceptable error, the result is inconclusive rather than pass/fail. |

Audit status: `PASS_FOR_PLAN_DRAFT_ONLY`.  Do not execute calibration runs until
a dedicated subplan specifies commands, seed counts, artifacts, and the
practical equivalence margin.

## Calibration Framework

### Step 1 - Choose The Intended Use

The threshold must be tied to intended use:

| Intended use | Threshold meaning |
| --- | --- |
| Diagnostic engineering availability | Nystrom values are close enough to streaming values for bounded engineering experiments. |
| Default value route | Nystrom values are close enough to streaming under a predeclared seed-panel uncertainty model. |
| HMC/posterior route | Nystrom log likelihood and gradients are close enough that posterior geometry and acceptance behavior are not materially distorted. |

If the intended use is HMC/posterior, this plan is insufficient by itself.
Threshold calibration must include theta/probe-point sensitivity and gradient
error, not just fixed-parameter value deltas.

### Step 2 - Estimate Comparator Measurement Noise

Estimate the stochastic scale of the streaming comparator at the intended
shape.  Candidate diagnostics:

- streaming total log-likelihood SD across independent particle seeds;
- streaming log-likelihood MCSE for the seed-panel mean;
- independent streaming-vs-streaming differences, if the harness supports
  paired replicate keys;
- optional higher-particle streaming or FP64 reference rows, if separately
  planned and affordable.

This produces a measurement-noise scale, not a practical threshold.

### Step 3 - Define A Practical Equivalence Margin

Before validation outcomes are interpreted, choose a practical margin
`tau_practical` on a declared scale:

- total log-likelihood delta;
- per-time-step delta;
- per-observed-component delta;
- downstream objective/posterior perturbation if relevant.

Examples of possible margin definitions:

- `tau_practical = c * streaming_sigma`, where `c` is chosen before validation
  and justified as "Nystrom error should be at most c comparator-noise units";
- `tau_practical = T * tau_per_time`, where `tau_per_time` is a domain tolerance
  for total log score per observation time;
- `tau_practical = T * M * tau_per_component`, where `tau_per_component` is a
  per-observed-component log-score tolerance;
- for HMC/posterior use, a theta-local log-posterior perturbation and gradient
  perturbation margin defined in a separate posterior-sensitivity plan.

If no practical margin can be justified, the calibration result must be
`BLOCKED_NO_PRINCIPLED_THRESHOLD`.

### Step 4 - Freeze The Threshold Before Validation

The threshold may be estimated on a calibration split, but it must be frozen
before validation seeds are interpreted.  Recommended split:

- calibration seeds: estimate comparator noise and candidate threshold options;
- validation seeds: test the frozen threshold using a predeclared uncertainty
  rule.

Do not change `tau_practical`, rank, epsilon, solver, chunks, or seed policy
after seeing validation failures.

### Step 5 - Use Equivalence-Style Decisions

For a chosen metric such as q90 or q95 of `abs(delta)`, use confidence bounds:

- accept for the declared scope only if the upper confidence bound is below
  `tau_practical`;
- reject only if the lower confidence bound is above `tau_practical`, or if
  deterministic validity vetoes fire;
- otherwise classify as inconclusive and collect more evidence or narrow scope.

For exceedance-count rules, define exceedance as
`abs(delta) > tau_practical`, not necessarily `abs(delta) > 5.0`.

## Required Artifacts For The Next Subplan

A dedicated execution subplan must specify:

- exact intended use;
- chosen threshold scale;
- calibration seed set and validation seed set;
- exact commands and trusted GPU selection rule;
- JSON/Markdown/log artifact paths;
- deterministic validity checks;
- statistical method for confidence bounds;
- threshold-freezing record;
- result note with decision table and inference-status table.

## Forbidden Claims And Actions

- Do not claim `5.0` is MCSE-derived.
- Do not claim `5.0` is principled merely because `1/12` seeds exceeded it.
- Do not reject or promote based on paired deltas before a practical equivalence
  margin is chosen.
- Do not choose the threshold after looking at validation outcomes.
- Do not use a value-only threshold for HMC/posterior readiness.

## Handoff

Next required artifact:

`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-subplan-2026-06-24.md`

The subplan should first run a cheap artifact-only calibration summary over the
existing 12 seeds, then decide whether new GPU seeds are needed to estimate the
comparator-noise and Nystrom-error scales accurately enough.
