# BayesFilter LGSSM-First NeuTra/HMC Phase 3 Subplan

Date: 2026-07-06

## Phase Objective

Run a tiny CPU-only plain HMC mechanics smoke on the reviewed LGSSM target
adapter, without convergence or posterior-readiness claims. The smoke target is
the Phase 2 generic rank-2 LGSSM adapter, not the older rank-1 fixture directly.

## Entry Conditions Inherited From Previous Phase

- Phase 2 LGSSM target adapter passed.
- Phase 2 review passed or a fixable blocker was visibly repaired.
- No HMC readiness or posterior validation claim has been made.
- The target used in this phase is
  `bayesfilter.testing.lgssm_generic_target_adapter_tf.make_lgssm_generic_target_fixture`.

## Required Artifacts

- Bounded CPU-only smoke log/result, under `docs/plans/` or another explicitly
  recorded artifact path.
- Phase 3 result:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase3-plain-hmc-smoke-result-2026-07-06.md`
- Refreshed Phase 4 subplan.

## Required Checks/Tests/Reviews

- CPU-only tiny smoke with `CUDA_VISIBLE_DEVICES=-1`.
- Bounded runtime and logs.
- Exact command and random seed recorded.
- Finite target values/samples and no immediate mechanics/runtime crash.
- Review before continuing to reference validation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does a tiny plain HMC smoke execute against the reviewed LGSSM target adapter without immediate mechanics/runtime failure? |
| Baseline/comparator | Phase 2 generic LGSSM target adapter and existing opt-in QR static LGSSM HMC smoke harness. |
| Primary criterion | Tiny smoke completes with finite target evaluations and no crash. |
| Veto diagnostics | Nonfinite target, crash, hidden long chain, GPU use, retuning beyond plan, or smoke promoted to convergence. |
| Explanatory diagnostics | Acceptance, step size, leapfrog count, runtime, finite checks. |
| Not concluded | HMC convergence, posterior correctness, sampler ranking, production readiness. |
| Artifact | Phase 3 result and smoke log. |

## Forbidden Claims/Actions

- Do not run long HMC.
- Do not use GPU unless separately approved.
- Do not claim convergence or posterior validation.
- Do not retune step size, mass, leapfrog count, or chain length beyond the
  values stated in the Phase 3 run record.
- Do not treat acceptance rate, sample mean, or sample spread as posterior
  validation.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only after smoke result is recorded and reviewed, with
explicit nonclaims.

## Stop Conditions

Stop if target mechanics fail, if smoke scope would expand, or if review does
not converge after five rounds.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 3 result;
3. draft or refresh Phase 4 subplan;
4. review Phase 4 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
