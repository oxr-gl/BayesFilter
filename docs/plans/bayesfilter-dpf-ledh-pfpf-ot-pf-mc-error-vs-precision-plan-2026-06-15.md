# BayesFilter DPF LEDH-PFPF-OT PF MC Error vs Precision Plan - 2026-06-15

## Research Intent Ledger

- Main question: On the same focused LEDH-PFPF-OT value/score diagnostic, how
  large are FP32/TF32 precision errors relative to particle-filter Monte Carlo
  variability across independent particle seeds?
- Candidate or mechanism under test: streaming streaming tensor value/score
  route with fixed model/observations and independent particle fixtures.
- Expected failure mode: precision drift may be comparable to PF seed-to-seed
  variability, or score runs may be non-finite/too slow.
- Promotion criterion: FP32/TF32 paired precision drift RMS is a small fraction
  of FP64 seed-to-seed sample SD for value and score components.
- Promotion veto: non-finite value/score, missing paired artifacts, or a
  precision drift ratio near or above one for an HMC-relevant score component.
- Continuation veto: do not interpret precision-vs-MC ratios if FP64 seed
  variability cannot be estimated from at least two independent seeds.
- Repair trigger: high precision-vs-MC ratio triggers larger-seed and HMC energy
  diagnostics before any precision policy choice.
- Explanatory diagnostics: FP64 sample mean/SD, paired FP32/TF32 RMS error,
  max paired error, and ratio to FP64 sample SD.
- What must not be concluded: no production default change, no HMC readiness
  claim, no posterior validity claim, and no statistical ranking from a small
  seed count.

## Evidence Contract

- Engineering/scientific question: Is precision error small compared with the
  PF approximation noise floor for the value and gradient?
- Exact baseline/comparator: FP64 streaming streaming tensor score over
  independent particle seeds estimates PF Monte Carlo variability. Paired
  FP32-no-TF32 and FP32+TF32 runs at the same seeds estimate precision drift.
- Primary pass/fail criterion: finite paired runs and precision RMS / FP64
  sample SD ratios materially below one.
- Diagnostics that can veto: non-finite outputs, child failures, missing paired
  arms, or ratios near/above one.
- Explanatory-only diagnostics: sample mean, sample SD, max absolute drift,
  timing. With a small seed count these are descriptive.
- Artifact preserving result: `docs/benchmarks/experimental-batched-ledh-pfpf-ot-pf-mc-error-vs-precision-*.json`
  and result note under `docs/plans`.

## Skeptical Plan Audit

- Wrong baseline: avoided by estimating MC variability from FP64 across seeds,
  not from absolute log-likelihood scale.
- Proxy metrics: pointwise relative error to `abs(loglik)` is not used as a
  decision criterion.
- Missing stop conditions: stop interpretation if any arm is non-finite or if
  fewer than two FP64 seeds complete.
- Unfair comparison: paired precision drift uses the same seed and fixture
  settings as FP64 for each seed.
- Hidden assumption: seed-to-seed fixture variation is used as a practical PF
  MC noise proxy for this deterministic benchmark; it is not a full theoretical
  PF CLT estimate.
- Environment mismatch: GPU commands run in trusted context and record device.
- Artifact mismatch: aggregate JSON must include per-seed values/scores and
  compact ratio summaries.

Audit status: passed for a focused noise-floor diagnostic.
