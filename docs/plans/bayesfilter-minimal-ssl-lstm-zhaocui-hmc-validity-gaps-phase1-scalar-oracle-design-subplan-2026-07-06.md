# Phase 1 Subplan: Scalar Posterior/Reference Oracle Design

Date: 2026-07-06

Status: `PASSED`

## Phase Objective

Design the smallest independent scalar posterior/reference oracle for the
minimal `zhaocui_fixed` target, so later HMC samples can be compared against a
predeclared reference instead of relying on launch, acceptance, or finite-sample
checks.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed and recorded the correct baseline.
- Existing internal target remains internal-only and unchanged except under a
  reviewed implementation phase.
- No posterior correctness or convergence claim has been made.

## Required Artifacts

- Phase 1 design result.
- Phase 2 oracle implementation subplan refreshed with exact commands,
  artifacts, reference method, tolerances, and evidence roles.
- Review bundle for Phase 2.

## Required Checks, Tests, Reviews

- Skeptical plan audit.
- Research intent ledger.
- Review of oracle target quantity: target log density, reference posterior
  approximation, and comparison surface must be separately named.
- Local checks limited to import/shape/metadata inspection unless Phase 1
  explicitly designs a no-runtime static artifact.
- Material review before Phase 2 implementation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What independent scalar reference can test whether the minimal HMC target posterior is right enough to compare future samples? |
| Baseline/comparator | Internal `MinimalZhaoCuiHMCTargetAdapter`, frozen scalar fixture, and Phase 5 hard-veto artifact as mechanics context only. |
| Primary pass criterion | Phase 2 subplan predeclares the reference method, target quantity, parameter subset or full-state grid strategy, tolerances, artifacts, hard vetoes, explanatory diagnostics, and nonclaims. |
| Veto diagnostics | Reference uses the same implementation path without independence, grid/domain misses material posterior mass without detection, tolerances invented without provenance, comparison surface unclear, or posterior correctness claimed before execution. |
| Explanatory diagnostics | Candidate grid bounds, pilot finite checks, selected coordinates, numerical precision, runtime estimate, and expected artifact schema. |
| Not concluded | Any posterior correctness or HMC convergence result; Phase 1 is design only. |

## Research Intent Ledger

| Field | Ledger |
| --- | --- |
| Main question | Can a scalar reference artifact distinguish target/posterior errors from sampler launch mechanics? |
| Candidate/mechanism under test | Independent reference computation for the frozen minimal scalar target. |
| Expected failure mode | Reference too coupled to HMC target, too low resolution, wrong domain, or unclear posterior quantity. |
| Promotion criterion | A reviewed Phase 2 plan with exact reference method and artifact schema. |
| Promotion veto | Missing independence, missing mass/domain checks, unsupported tolerance, or unclear target. |
| Continuation veto | Need for unreviewed package install, network fetch, or long runtime. |
| Repair trigger | Reviewer finds wrong target quantity, weak reference independence, or missing mass diagnostics. |
| Explanatory diagnostics | Grid/domain design, finite checks, normalization stability, and runtime estimate. |
| Must not conclude | HMC validity, posterior correctness, or convergence. |

## Forbidden Claims And Actions

Do not run long HMC or compare samples in Phase 1. Do not claim the reference is
correct before implementation and checks. Do not call any diagnostic a
posterior-validity result until Phase 2 executes and reviews it.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 only if the oracle implementation subplan has exact commands
and artifacts, reviewed reference independence, reviewed tolerances or
hypothesis labels, and material review convergence.

The Phase 0 substitute reviewer added one binding watch item for Phase 1:
the Phase 2 subplan must contain actual reference details and
hypothesis-labeled tolerances, not just repeat the generic Phase 1
requirements.

## Stop Conditions

Stop if an independent reference cannot be defined, if the only feasible
reference is circular with the target implementation, if required runtime or
package boundaries need human approval not yet granted, or if review does not
converge.
