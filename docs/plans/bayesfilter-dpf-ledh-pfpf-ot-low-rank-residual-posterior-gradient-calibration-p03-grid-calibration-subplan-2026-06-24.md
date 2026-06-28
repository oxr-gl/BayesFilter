# P03 Residual-Control Calibration Grid Subplan

Date: 2026-06-24

Status: `DRAFT_PENDING_P02`

## Phase Objective

Run a bounded calibration grid over residual-control knobs to map low-rank
factor residuals to posterior value, posterior gradient, and peak-neighborhood
harm on calibration rows only. P03 may nominate a threshold or diagnostic rule
for P04, but it cannot validate that rule.

## Entry Conditions Inherited From Previous Phase

- P02 result exists, trusted GPU artifacts are valid, and P03 handoff is
  approved by local/Claude review.
- P02 did not invalidate the harness, exact reference, TensorFlow backend, or
  gradient instrumentation.
- P03 subplan has been refreshed with P02 observed costs and command shape.
- Trusted GPU runtime approval is available.
- No approval is inherited for HMC runtime, package/API/default changes,
  package installs, network fetches, model-file edits, or scientific claims.

## Required Artifacts

- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p03-grid-calibration-result-2026-06-24.md`
- Structured aggregate JSON:
  `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p03-grid-2026-06-24.json`
- Aggregate Markdown:
  `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p03-grid-2026-06-24.md`
- Logs under:
  `docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/`
- Refreshed P04 subplan.

## Required Checks, Tests, And Reviews

- Trusted GPU precheck.
- Quiet visible execution and structured artifact validation.
- Bounded grid over calibration rows. Initial intended grid:
  - rank: `16,32,64`;
  - projection iterations: `120,240,480`;
  - assignment epsilon: `0.125,0.25,0.5`;
  - LGSSM calibration seeds include the original three seeds and may include a
    small predeclared calibration-only extension if P02 runtime budget permits.
- For every row, record residual diagnostics, value error, gradient relative
  error, cosine similarity, max coordinate error, peak-neighborhood diagnostic,
  runtime/provenance, and route validity.
- Produce a calibration table that separates:
  - hard validity vetoes;
  - value/gradient harm screens;
  - residuals as candidate proxy diagnostics;
  - descriptive timing/ESS.
- Claude read-only review of P03 result and P04 threshold-freeze subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which residual-control settings keep posterior value, gradient, and peak-neighborhood diagnostics acceptable on calibration rows, and how predictive is factor residual? |
| Baseline/comparator | Exact Kalman value/gradient oracle for LGSSM, with streaming route as paired finite-particle comparator. |
| Primary pass criterion | Calibration grid artifacts are finite, valid, and complete enough for P04 to freeze a rule before holdout. |
| Veto diagnostics | Nonfinite values/gradients, invalid factors, active-path NumPy, dense materialization, missing exact reference, missing GPU/XLA provenance, corrupt artifact, or unsupported claim. |
| Explanatory diagnostics | Residual-value/gradient association, timing, projection iterations, ESS, and seed variation. |
| Not concluded | No holdout validation, no final threshold, no statistical superiority, no posterior correctness, no HMC readiness, no default readiness. |
| Artifact | P03 result, aggregate JSON/Markdown, row logs, review ledger, and refreshed P04 subplan. |

## Forbidden Claims And Actions

- Do not validate a threshold in P03; P03 only supplies calibration evidence.
- Do not include holdout seeds in threshold selection unless P04 explicitly
  downgrades holdout claims and creates new holdout rows.
- Do not choose a rule based on actual-SIR P06 data, which occurs later.
- Do not run HMC.
- Do not change public API, package metadata, default policy, model files, or
  dependencies.

## Exact Next-Phase Handoff Conditions

P03 hands off to P04 only if:

- P03 result and structured artifacts exist;
- artifact validator passes;
- calibration/holdout split remains intact;
- P04 subplan can freeze a rule without seeing holdout outcomes;
- Claude review returns `VERDICT: AGREE`.

If P03 shows residual is not predictive but direct gradient screens are viable,
P04 may freeze a direct value/gradient gate instead of a residual threshold.

## Stop Conditions

- Trusted GPU runtime is unavailable or unapproved.
- Grid artifacts are missing, corrupt, or incomplete.
- The harness is invalidated by calibration rows.
- Calibration/holdout separation is broken.
- Claude/Codex review does not converge within five rounds for the same
  blocker.

## End-Of-Subplan Procedure

1. Run required local checks and runtime validators.
2. Write P03 result or blocker result.
3. Draft or refresh P04 subplan.
4. Review P04 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
5. Send material result/subplan to Claude read-only review and record verdict.
