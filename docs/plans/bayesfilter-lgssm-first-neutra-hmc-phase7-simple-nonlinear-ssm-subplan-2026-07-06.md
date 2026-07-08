# BayesFilter LGSSM-First NeuTra/HMC Phase 7 Subplan

Date: 2026-07-06

## Phase Objective

Move from LGSSM to the first BayesFilter-owned simple nonlinear non-DSGE SSM
target.

## Entry Conditions Inherited From Previous Phase

- Phase 6 bounded CPU-only learned affine LGSSM NeuTra-style training gate has
  passed:
  - frozen affine payload was written and reloaded;
  - target signature matched
    `290a91d2a8f90d5b29243965b258b1ec6fd965aa46ffca69dcb78f7fa1ecabcb`;
  - transformed mechanics value/score were finite;
  - deterministic LGSSM reference residual checks passed;
  - no HMC convergence, posterior correctness, production, default-policy, or
    scientific validity claim was made.
- Owner directive received after Phase 6: future BayesFilter NeuTra training is
  GPU by default/requirement; external sample generation should use multicore
  CPU parallelism.  The Phase 6 CPU-only affine training gate is retained only
  as a historical smoke/integration fixture.
- Phase 6 result and this refreshed Phase 7 subplan must receive bounded
  read-only review before Phase 7 execution.
- DSGE/c603 remains deferred.

## Required Artifacts

- Phase 7 target-selection note naming the simple nonlinear non-DSGE SSM and
  filter/approximation semantics before implementation.
- BayesFilter-owned nonlinear SSM generic target fixture or adapter code.
- Focused tests for finite batch-native value/score and manifest/signature
  stability.
- Phase 7 result:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase7-simple-nonlinear-ssm-result-2026-07-06.md`
- Refreshed Phase 8 subplan.

## Required Checks/Tests/Reviews

- Model choice justification.
- Filter choice and target signature.
- Finite value/score checks.
- Gradient/reference diagnostics where feasible.
- `git diff --check` on Phase 7 code/planning artifacts.
- Review before multi-filter phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generic target adapter handle a BayesFilter-owned simple nonlinear non-DSGE SSM? |
| Baseline/comparator | Closed LGSSM foundation and chosen nonlinear model/filter reference diagnostics. |
| Primary criterion | Finite batch-native posterior value/score and reviewed target manifest. |
| Veto diagnostics | DSGE dependency, c603 import, nonfinite values/scores, missing or unstable target signature, unreviewed approximation semantics, training/HMC/GPU hidden under target-adapter work, or posterior correctness overclaim. |
| Explanatory diagnostics | Filter diagnostics, gradient residuals, runtime. |
| Not concluded | Broad nonlinear validity, learned NeuTra quality, HMC convergence, posterior correctness, sampler ranking, production readiness, default-policy change, or scientific validity. |
| Artifact | Phase 7 result and tests/logs. |

## Forbidden Claims/Actions

- Do not use DSGE/c603.
- Do not claim exactness unless the chosen nonlinear case has an exact
  comparator.
- Do not use GPU, learned transport training, or long HMC without a reviewed
  subplan and explicit approval.
- If a reviewed subplan introduces learned NeuTra training, do not run it on
  CPU except for explicitly labeled tiny smoke/reference diagnostics; serious
  NeuTra training must use trusted GPU execution.
- If sample/replay dataset generation is needed, plan it as multicore CPU work
  with worker count, seeds, target signature, and artifact hashes recorded.
- Do not treat Phase 6 LGSSM training loss as evidence for nonlinear SSM
  validity.

## Exact Next-Phase Handoff Conditions

Phase 8 may begin only if a nonlinear target adapter exists with reviewed
filter semantics and finite checks.

## Stop Conditions

Stop if model/filter semantics are unclear, if gradients are unavailable but
needed for HMC, or if review does not converge after five rounds.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 7 result;
3. draft or refresh Phase 8 subplan;
4. review Phase 8 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
