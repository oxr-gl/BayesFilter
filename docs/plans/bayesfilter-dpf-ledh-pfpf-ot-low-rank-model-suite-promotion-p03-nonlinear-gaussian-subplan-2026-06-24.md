# P03 Nonlinear Gaussian Gate Subplan

Date: 2026-06-24

Status: `PROVISIONAL_PENDING_P02_RESULT_AND_REFRESH`

## Phase Objective

Test locked low-rank LEDH-PFPF-OT on nonlinear Gaussian state-space models such
as range-bearing or nonlinear growth/accumulation fixtures, focusing on
local-linearization stress, finite outputs, and bounded degradation relative to
the streaming route.

## Entry Conditions Inherited From Previous Phase

- P02 result exists and does not fire a promotion continuation veto.
- Candidate lock remains unchanged.
- Streaming comparator remains available.
- Trusted GPU runtime requires explicit approval.

## Required Artifacts

- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p03-nonlinear-gaussian-result-2026-06-24.md`
- P04 refreshed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p04-sv-heavy-tail-subplan-2026-06-24.md`
- Nonlinear Gaussian benchmark JSON/Markdown artifacts under
  `docs/benchmarks`.
- Command logs under
  `docs/logs/low-rank-ledh-model-suite-promotion-2026-06-24/`.

## Required Checks, Tests, And Reviews

- Identify exact fixture and harness surfaces before runtime.
- Run syntax and focused tests for chosen nonlinear Gaussian harness.
- Trusted GPU precheck.
- Paired streaming/low-rank rows with same seeds, shape, dtype, TF32 mode, GPU,
  and timing contract.
- Validators for finite outputs, ESS floors, route-fired evidence, Jacobian or
  local-linearization diagnostics where available, and bounded degradation
  against streaming.
- Claude read-only review of P03 result and P04 subplan if material.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does low-rank remain stable and comparable on nonlinear Gaussian filtering cases? |
| Baseline/comparator | Streaming GPU/TF32 LEDH-PFPF-OT; UKF or dense/reference diagnostics are explanatory unless explicitly validated. |
| Primary pass criterion | Low-rank passes finite/provenance/route/nonmaterialization screens and does not exceed predeclared bounded-degradation screens versus streaming. |
| Veto diagnostics | Nonfinite output, route mismatch, local Jacobian blowup without reviewed explanation, ESS collapse beyond declared threshold, missing comparator, dense materialization, or unsupported claim. |
| Explanatory diagnostics | UKF diagnostics, RMSE proxies, timings, memory, ESS, Jacobian summaries, and seed variation. |
| Not concluded | No exact nonlinear posterior correctness, statistical superiority, dense equivalence, HMC readiness, or broad promotion from this phase alone. |
| Artifact | P03 result, benchmark JSON/Markdown artifacts, logs, ledgers. |

## Forbidden Claims And Actions

- Do not treat UKF or proxy diagnostics as exact truth.
- Do not claim nonlinear posterior correctness.
- Do not change candidate settings after seeing results.
- Do not run HMC/autodiff runtime.
- Do not change default policy, public API, package metadata, model files, or
  dependencies.

## Exact Next-Phase Handoff Conditions

P03 hands off to P04 only if P03 passes its hard screens or writes a reviewed
non-candidate blocker, P04 subplan is refreshed, and local/Claude review
converges where material.

## Stop Conditions

- Valid nonlinear Gaussian gate shows candidate instability or unacceptable
  degradation.
- Required comparator or diagnostics cannot be produced.
- Trusted GPU runtime is unavailable or unapproved.
- Review does not converge within five rounds for the same blocker.

## End-Of-Subplan Procedure

1. Run required local checks.
2. Write P03 result or blocker result.
3. Draft or refresh P04 subplan.
4. Review P04 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
