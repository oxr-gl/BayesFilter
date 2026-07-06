# P06 Actual-SIR d18 Value/Gradient Probe Subplan

Date: 2026-06-24

Status: `DRAFT_PENDING_P05`

## Phase Objective

Probe whether the P05 validated LGSSM rule remains informative on the target
actual-SIR d18 family using paired streaming-vs-low-rank value and gradient
diagnostics at fixed parameter probe points.

P06 is an engineering target-family probe, not exact posterior correctness.
Streaming is a comparator, not an oracle.

## Entry Conditions Inherited From Previous Phase

- P05 result exists and either validates the frozen rule or explicitly hands
  off a non-promotion engineering probe with downgraded claims.
- P06 subplan has been refreshed to respect P05 results.
- Trusted GPU runtime approval is available.
- Actual-SIR d18 harness surfaces are present.
- No approval is inherited for HMC runtime, package/API/default changes,
  package installs, network fetches, model-file edits, or scientific claims.

## Required Artifacts

- P06 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p06-actual-sir-gradient-probe-result-2026-06-24.md`
- Structured aggregate JSON:
  `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p06-actual-sir-2026-06-24.json`
- Aggregate Markdown:
  `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p06-actual-sir-2026-06-24.md`
- Logs under:
  `docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/`
- Refreshed P07 closeout subplan.

## Required Checks, Tests, And Reviews

- Trusted GPU precheck.
- Quiet visible execution and structured artifact validation.
- Fixed actual-SIR d18 probe set with predeclared parameter points and seeds.
- Paired streaming and low-rank route execution with shared seeds, shapes,
  dtype, TF32 mode, GPU provenance, and candidate settings.
- Record route validity, residuals, values, gradients where differentiable,
  peak-neighborhood or fixed local-probe summaries, and nonclaims.
- If gradients cannot be validly obtained for actual-SIR without an unapproved
  implementation boundary, write a blocker result instead of substituting proxy
  metrics.
- Claude read-only review of P06 result and P07 closeout subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | On actual-SIR d18, does the low-rank route preserve paired value/gradient/peak-neighborhood behavior relative to streaming under the frozen rule? |
| Baseline/comparator | Streaming GPU/TF32 LEDH-PFPF-OT route as engineering comparator, not truth. |
| Primary pass criterion | Paired actual-SIR probe artifacts are finite, valid, route-matched, and consistent with the P05 frozen rule without hard validity vetoes. |
| Veto diagnostics | Nonfinite values/gradients, missing differentiable gradient path, invalid factors, active-path NumPy, dense materialization, route mismatch, missing GPU/XLA provenance, corrupt artifact, or unsupported exactness claim. |
| Explanatory diagnostics | Paired value/gradient deltas, residuals, projection iterations, timing, memory, ESS, and seed variation. |
| Not concluded | No exact posterior correctness for actual-SIR, no statistical superiority, no HMC readiness, no public default readiness, no scientific validity. |
| Artifact | P06 result, aggregate JSON/Markdown, row logs, review ledger, and refreshed P07 subplan. |

## Forbidden Claims And Actions

- Do not call streaming an exact oracle for actual-SIR.
- Do not claim actual-SIR posterior correctness from paired comparability.
- Do not run HMC.
- Do not change the frozen rule after P05.
- Do not change public API, package metadata, default policy, model files, or
  dependencies.

## Exact Next-Phase Handoff Conditions

P06 hands off to P07 only if:

- P06 result and structured artifacts exist, or a blocker result explains why
  actual-SIR gradients are not yet available;
- local validator passes or records a clear blocker classification;
- P07 closeout subplan is refreshed with P06 evidence and nonclaims;
- Claude review returns `VERDICT: AGREE`.

If actual-SIR gradient instrumentation is missing, P06 may hand off to P07 with
`DIRECT_ACTUAL_SIR_GRADIENT_GAP_REMAINS`, but it must not claim target-family
gradient validation.

## Stop Conditions

- Trusted GPU runtime is unavailable or unapproved.
- Actual-SIR gradient path is unavailable without unapproved code or model-file
  changes.
- Required artifacts are missing or corrupt.
- The frozen rule is violated in a way that invalidates target-family probing.
- Claude/Codex review does not converge within five rounds for the same
  blocker.

## End-Of-Subplan Procedure

1. Run required local checks and runtime validators.
2. Write P06 result or blocker result.
3. Draft or refresh P07 closeout subplan.
4. Review P07 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
5. Send material result/subplan to Claude read-only review and record verdict.
