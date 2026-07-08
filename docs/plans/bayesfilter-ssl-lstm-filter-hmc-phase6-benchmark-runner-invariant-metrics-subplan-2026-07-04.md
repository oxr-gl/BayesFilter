# Phase 6 Subplan: Shared Benchmark Runner And Invariant Metrics

Date: 2026-07-04

Status: `DRAFT_READY_FOR_PRECHECK`

## Phase Objective

Create the shared SSL-LSTM benchmark runner and invariant metric suite used to
evaluate all admitted filter adapters under the same data, priors, HMC runtime,
and evidence classification. Phase 6 is a shared benchmark gate, not a
parameter-matching gate.

## Entry Conditions Inherited From Previous Phase

- Phase 5 recorded admitted, failed, or blocked status for every candidate.
- The shared value/score protocol and artifact schema remain active.
- No candidate may be exempted from the shared benchmark for a favorable result.
- Candidate status at Phase 5 close:
  `fixed_sgqf` and `svd_ukf` are locally admitted for benchmark-harness work;
  `zhaocui_fixed` is blocked by missing SSL-LSTM Zhao-Cui implementation;
  `ledh_streaming_ot` is blocked by missing manual VJP streaming-OT score path.

## Required Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase6-benchmark-runner-invariant-metrics-result-2026-07-04.md`
- Benchmark runner code and tests.
- Synthetic SSL-LSTM data manifest with seeds, dimensions, noise scales,
  train/heldout split, and true latent trajectory.
- Metric implementation for heldout predictive log score proxy, decoded latent
  RMSE after alignment, trajectory alignment error, posterior predictive
  calibration, and HMC diagnostics fields.
- JSON result schema with candidate status, veto fields, explanatory fields,
  nonclaims, device/JIT/TF32 provenance, target-scope provenance, and artifact
  paths.
- Refreshed Phase 7 subplan.

## Required Checks, Tests, And Reviews

- Unit tests for metric shape, deterministic fixture generation, and artifact
  schema validation.
- Negative tests that prevent parameter matching from becoming the primary
  pass criterion and verify target-scope provenance is recorded for admitted
  rows.
- Small smoke run with admitted adapters only, labeled as smoke only; blocked
  candidates must appear in the artifact status table but must not be run.
- Claude read-only review for benchmark fairness, metric role classification,
  and artifact coverage.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a shared benchmark fairly evaluate filter-HMC SSL-LSTM estimation in invariant terms? |
| Baseline/comparator | Same data, prior, HMC runtime, metric suite, seeds, and budget for every admitted adapter. |
| Primary pass criterion | Benchmark runner and metric tests pass, smoke artifacts validate schema, parameter matching remains non-primary, and target-scope provenance is captured. |
| Veto diagnostics | Candidate-specific fixture changes, missing seeds, missing split, metric schema mismatch, parameter matching as promotion criterion, missing target-scope provenance, or missing device/JIT provenance. |
| Explanatory diagnostics | Runtime, memory, proxy heldout predictive log score values from smoke runs, and artifact sizes. |
| Not concluded | Estimation success, statistical ranking, default readiness, or HMC convergence. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase6-benchmark-runner-invariant-metrics-result-2026-07-04.md` |

## Forbidden Claims And Actions

- Do not rank candidate filters from smoke metrics.
- Do not change pass/fail criteria after seeing benchmark outputs.
- Do not let SGQF/UKF skip the shared benchmark.
- Do not run blocked Zhao-Cui or LEDH candidates as if their target score paths
  existed.
- Do not treat parameter matching as success.
- Do not treat heldout predictive log score proxy values as a ranking claim.
- Do not run long HMC evidence chains until Phase 7 gate is active.

## Exact Next-Phase Handoff Conditions

Phase 7 may start only when:

- benchmark runner and metric tests pass;
- data manifest and artifact schema are locked;
- all admitted candidates have the same declared run budget or an explicit
  blocker is recorded;
- candidate rows include target-scope provenance for admitted and blocked
  filters;
- Phase 7 subplan is refreshed for HMC mechanics and evidence ladder.

## Stop Conditions

- The shared metric harness cannot fairly compare all admitted candidates.
- Required device/JIT provenance cannot be recorded.
- The fixture is too ill-conditioned to distinguish implementation failure from
  expected non-identifiability.
- Any benchmark run would require unapproved package install, network fetch, or
  new compute policy.

## End-Of-Phase Protocol

1. Run benchmark runner tests, schema tests, and smoke checks.
2. Write the Phase 6 result/close record.
3. Draft or refresh the Phase 7 subplan.
4. Review Phase 7 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
