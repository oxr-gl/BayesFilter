# P07 HMC And Autodiff Mechanics Subplan

Date: 2026-06-24

Status: `PROVISIONAL_OPTIONAL_PENDING_P06_RESULT_AND_HUMAN_APPROVAL`

## Phase Objective

If and only if explicitly approved after P06, test whether the locked low-rank
route has the minimum TensorFlow autodiff and XLA mechanics needed for later
HMC-readiness work. If not approved, write a skip result preserving HMC
readiness as a nonclaim.

## Entry Conditions Inherited From Previous Phase

- P01 through P06 results exist and do not fire a continuation veto.
- Candidate lock remains unchanged.
- No HMC readiness claim has been made.
- Explicit P07 approval is required before any HMC/autodiff runtime.

## Required Artifacts

- P07 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p07-hmc-autodiff-result-2026-06-24.md`
- P08 refreshed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-model-suite-promotion-p08-closeout-subplan-2026-06-24.md`
- Autodiff/HMC mechanics JSON/Markdown artifacts if runtime is approved.
- Logs under `docs/logs/low-rank-ledh-model-suite-promotion-2026-06-24/`.

## Required Checks, Tests, And Reviews

- If skipped:
  - write P07 skip result preserving HMC readiness as nonclaim;
  - refresh P08 accordingly.
- If approved:
  - refresh exact HMC/autodiff command and artifact contract;
  - syntax/focused tests for selected mechanics harness;
  - trusted GPU precheck where GPU is claimed;
  - fixed-randomness value/gradient mechanics smoke;
  - checks for finite value, finite gradients, connected parameters,
    repeatability, no `.numpy()` barrier in differentiable path, and XLA
    compile evidence where claimed;
  - Claude read-only review of result and P08 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the low-rank route mechanically compatible with TensorFlow autodiff/XLA for later HMC work, or is HMC readiness preserved as a nonclaim? |
| Baseline/comparator | Fixed-randomness TensorFlow value/gradient mechanics; streaming or finite-difference diagnostics only where declared. |
| Primary pass criterion | If approved, finite connected repeatable value/gradient and XLA mechanics screens pass; if skipped, nonclaim is explicitly preserved. |
| Veto diagnostics | Nonfinite value/gradient, disconnected parameter, stochastic randomness drift, `.numpy()` barrier, XLA failure where claimed, missing artifact, or unapproved HMC runtime. |
| Explanatory diagnostics | Gradient norms, finite-difference deltas, compile time, runtime, and warning text. |
| Not concluded | No NUTS readiness, sampler convergence, posterior correctness, statistical superiority, package/public default readiness, or scientific validity. |
| Artifact | P07 result, optional mechanics artifacts, logs, ledgers. |

## Forbidden Claims And Actions

- Do not run HMC/autodiff runtime without explicit P07 approval.
- Do not claim HMC readiness from a mechanics smoke.
- Do not change candidate settings after seeing results.
- Do not change public API, package metadata, model files, dependencies, or
  default policy.

## Exact Next-Phase Handoff Conditions

P07 hands off to P08 if either:

- P07 is skipped with a result preserving HMC readiness as nonclaim; or
- approved P07 runtime passes required mechanics screens and Claude/local review
  converges.

P08 must state clearly whether HMC readiness is claimed or not.

## Stop Conditions

- HMC/autodiff runtime is needed but not approved.
- Mechanics harness exposes a valid differentiability barrier.
- Review does not converge within five rounds for the same blocker.

## End-Of-Subplan Procedure

1. Run required local checks or write approved skip result.
2. Write P07 result or blocker result.
3. Draft or refresh P08 subplan.
4. Review P08 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
