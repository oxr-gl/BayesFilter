# P05 Stiff Nonlinear Dynamics Gate Subplan

Date: 2026-06-24

Status: `PROVISIONAL_PENDING_P04_RESULT_AND_REFRESH`

## Phase Objective

Test locked low-rank LEDH-PFPF-OT under stiff nonlinear dynamics such as
predator-prey or comparable fixtures, where local Jacobians and flow stability
are likely failure modes.

## Entry Conditions Inherited From Previous Phase

- P04 result exists and does not fire a continuation veto.
- Candidate lock remains unchanged.
- Streaming comparator remains available.
- Trusted GPU runtime requires explicit approval.

## Required Artifacts

- P05 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p05-stiff-nonlinear-result-2026-06-24.md`
- P06 refreshed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p06-resource-envelope-subplan-2026-06-24.md`
- Stiff nonlinear JSON/Markdown artifacts under `docs/benchmarks`.
- Logs under `docs/logs/low-rank-ledh-model-suite-promotion-2026-06-24/`.

## Required Checks, Tests, And Reviews

- Identify current stiff nonlinear fixture/harness surfaces.
- Syntax and focused tests for selected harness.
- Trusted GPU precheck.
- Paired streaming/low-rank runs with fixed seeds and comparable settings.
- Validators for finite outputs, local Jacobian diagnostics, flow stability,
  route-fired evidence, nonmaterialization, ESS thresholds, and provenance.
- Claude read-only review of P05 result and P06 subplan if material.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does low-rank remain stable under stiff nonlinear dynamics and local-flow stress? |
| Baseline/comparator | Streaming GPU/TF32 LEDH-PFPF-OT under same seeds/settings. |
| Primary pass criterion | Low-rank passes finite/provenance/route/nonmaterialization screens and declared flow/Jacobian/ESS stability screens. |
| Veto diagnostics | Nonfinite flow/output, exploding Jacobian diagnostic, route mismatch, missing comparator, dense materialization, active-path NumPy, or unsupported claim. |
| Explanatory diagnostics | Runtime, memory, ESS, Jacobian summaries, flow step diagnostics, and seed variation. |
| Not concluded | No exact posterior correctness, statistical superiority, dense equivalence, HMC readiness, or broad scientific validity. |
| Artifact | P05 result, benchmark artifacts, logs, ledgers. |

## Forbidden Claims And Actions

- Do not claim broad nonlinear robustness from one stiff fixture.
- Do not rank methods from descriptive diagnostics alone.
- Do not change candidate settings after seeing results.
- Do not run HMC/autodiff runtime.
- Do not change default policy, public API, package metadata, model files, or
  dependencies.

## Exact Next-Phase Handoff Conditions

P05 hands off to P06 only if P05 passes or writes a reviewed blocker that does
not invalidate the candidate, P06 subplan is refreshed, and local/Claude review
converges where material.

## Stop Conditions

- Valid stiff dynamics gate reveals candidate instability or unacceptable
  degradation.
- Required comparator/diagnostics cannot be produced.
- Trusted GPU runtime is unavailable or unapproved.
- Review does not converge within five rounds for the same blocker.

## End-Of-Subplan Procedure

1. Run required local checks.
2. Write P05 result or blocker result.
3. Draft or refresh P06 subplan.
4. Review P06 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
