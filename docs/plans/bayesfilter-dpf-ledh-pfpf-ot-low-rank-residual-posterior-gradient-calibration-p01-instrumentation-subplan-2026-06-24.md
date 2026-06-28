# P01 Value/Gradient Instrumentation Subplan

Date: 2026-06-24

Status: `READY_FOR_EXECUTION`

## Phase Objective

Implement or refresh a focused TensorFlow/TFP-oriented LGSSM value/gradient
calibration harness and tests. The harness must measure residual diagnostics
alongside posterior value, posterior gradient, and a small peak-neighborhood
diagnostic at fixed, predeclared probe points.

P01 is an implementation and local-check phase. It does not produce trusted
GPU calibration evidence unless a later phase runs the harness under trusted
GPU/XLA execution.

## Entry Conditions Inherited From Previous Phase

- P00 result exists and passes as ready for P01 instrumentation.
- Master program, visible runbook, ledgers, stop handoff, and P01 subplan have
  converged under local and Claude read-only review.
- The P01 model-suite stop remains valid and is not being retroactively waived.
- Residual diagnostics remain proxy diagnostics until calibrated against
  value/gradient/peak behavior.
- No approval is inherited for GPU runtime, HMC runtime, package installs,
  network fetches, package/API/default changes, model-file edits, or scientific
  claims.

## Required Artifacts

- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p01-instrumentation-result-2026-06-24.md`
- New or refreshed harness:
  `docs/benchmarks/benchmark_low_rank_ledh_posterior_gradient_calibration.py`
- Focused tests:
  `tests/test_low_rank_ledh_posterior_gradient_calibration.py`
- Execution ledger update:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-visible-execution-ledger-2026-06-24.md`
- Refreshed P02 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-residual-posterior-gradient-calibration-p02-reproduction-determinism-subplan-2026-06-24.md`

## Required Checks, Tests, And Reviews

- Local skeptical audit before code changes.
- Implement only the named harness/test plus plan/result/ledger artifacts unless
  a minimal helper is necessary and recorded in the P01 result.
- Preserve TensorFlow/TFP as the implementation backend; do not use NumPy in
  BayesFilter-owned algorithmic implementation paths.
- Harness must emit structured JSON/Markdown with:
  - route and candidate settings;
  - fixed probe parameter vector and perturbation schedule;
  - exact Kalman value and gradient for LGSSM where available;
  - streaming and low-rank value/gradient metrics;
  - gradient relative norm error, max coordinate error, cosine similarity;
  - peak-neighborhood summary from predeclared local probes;
  - factor residual, induced row/column residual, projection iterations;
  - finite/provenance/nonmaterialization diagnostics;
  - nonclaims.
- Compile-check the harness and test.
- Run focused pytest for the new test.
- Run a no-active-path-NumPy text/structure audit on the new harness/test and
  touched low-rank path.
- Claude read-only review of P01 result and refreshed P02 subplan if local
  checks expose a material ambiguity or implementation boundary changed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we instrument LGSSM residual/value/gradient/peak diagnostics in a TensorFlow/TFP harness suitable for later GPU calibration? |
| Baseline/comparator | Exact Kalman value/gradient oracle for LGSSM, streaming finite-particle route, and low-rank route. |
| Primary pass criterion | Harness and focused tests exist, local checks pass, required metrics are present in command-shape artifacts, no active-path NumPy barrier is introduced, and boundaries/nonclaims are preserved. |
| Veto diagnostics | Missing exact reference fields, missing gradient metrics, active-path NumPy, nonfinite smoke outputs, dense materialization in low-rank route, failed tests, or unsupported claims. |
| Explanatory diagnostics | Local CPU-hidden smoke outputs, source inventory, warning text, and implementation notes. |
| Not concluded | No threshold calibration, GPU readiness, posterior correctness, HMC readiness, package default readiness, public API readiness, statistical superiority, or scientific validity. |
| Artifact | P01 result, harness, tests, optional smoke JSON/Markdown, ledger, and refreshed P02 subplan. |

## Forbidden Claims And Actions

- Do not claim that `0.005` is calibrated or invalidated from P01 alone.
- Do not run trusted GPU calibration evidence in P01 unless P01 is explicitly
  amended and approved; local CPU-hidden smoke is command-shape evidence only.
- Do not use NumPy in algorithmic implementation paths.
- Do not add PyTorch or JAX.
- Do not run HMC.
- Do not change public API, package metadata, default policy, model files, or
  dependencies.
- Do not tune thresholds after seeing P02/P03/P05 outcomes.

## Exact Next-Phase Handoff Conditions

P01 hands off to P02 only if:

- P01 result exists and records implementation surfaces and checks;
- harness/test artifacts exist at the required paths;
- compile and focused pytest pass;
- no-active-path-NumPy audit passes or any hit is proven reporting-only;
- P02 subplan is refreshed with actual harness command shape and artifact paths;
- local/Claude review, if triggered, converges.

If instrumentation is missing or invalid, write a blocker result and stop.

## Stop Conditions

- Exact Kalman value/gradient reference cannot be implemented without an
  unapproved backend, package install, model-file edit, or public API change.
- Focused tests fail in a way that invalidates the harness.
- Active-path NumPy or `.numpy()` barrier appears in differentiable candidate
  implementation.
- Required metrics cannot be emitted as structured artifacts.
- Claude/Codex review does not converge within five rounds for the same
  blocker.

## End-Of-Subplan Procedure

1. Run required local checks.
2. Write P01 result or blocker result.
3. Draft or refresh P02 subplan.
4. Review P02 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
