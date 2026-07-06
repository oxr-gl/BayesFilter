# P06 Optional HMC/Autodiff Mechanics Subplan

Date: 2026-06-24

Status: `COMPLETE_P06_SKIPPED_NONCLAIM_PRESERVED`

## Phase Objective

Optionally evaluate bounded HMC/autodiff mechanics for the low-rank actual-SIR
d18 LEDH-PFPF-OT default candidate after P05, without converting mechanical
autodiff evidence into posterior correctness, sampler validity, HMC readiness,
or scientific validity claims.

P06 may be skipped. If skipped or not approved, HMC readiness remains an
explicit nonclaim and the program may still proceed to P07 for the bounded
engineering default decision.

## Entry Conditions Inherited From Previous Phase

- P00 through P04 have required passing results.
- P05 result exists and either:
  - passes a bounded default-surface implementation gate; or
  - explicitly says P06 should be skipped and HMC remains a nonclaim.
- P06 subplan is refreshed after P05 closes.
- Explicit P06 human approval is required before HMC-specific runtime,
  gradient/autodiff experiments, or any HMC-readiness claim.
- If P05 only changes the actual-SIR low-rank validation/reporting defaults and
  tests, P06 remains optional and may be skipped with HMC preserved as a
  nonclaim.
- No approval is inherited for long MCMC chains, posterior correctness claims,
  package/dependency changes, public API changes, model-file changes, network
  access, or scientific claims.

## Required Artifacts

- This subplan, refreshed after P05 result if P06 is executed or skipped.
- P06 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-p06-hmc-autodiff-result-2026-06-24.md`
- Any focused HMC/autodiff smoke artifacts named in the refreshed subplan.
- Updated execution ledger.
- Updated Claude review ledger if Claude is used.
- Refreshed P07 closeout subplan.

## Required Checks, Tests, And Reviews

- Skeptical plan audit before any P06 runtime.
- If P06 is skipped: boundary scan proving the P06 result preserves HMC as a
  nonclaim.
- If P06 is executed:
  - source scan for differentiability barriers in the intended default path;
  - focused TensorFlow/XLA/autodiff smoke tests named after P05 discovery;
  - no-NumPy/default-path scan over any touched implementation path;
  - syntax check over any changed tests/docs;
  - focused tests named in the refreshed P06 subplan;
  - artifact validator for finite gradients/mechanics only, if generated.
- Claude Opus/max read-only review before execution because P06 crosses an
  HMC/autodiff boundary.
- Claude Opus/max read-only review of the P06 result before P07 if P06 makes
  any mechanics claim beyond "skipped, HMC nonclaim preserved."

## Skeptical Plan Audit

| Audit item | Status |
| --- | --- |
| Wrong baseline | Guarded: P06 is not a benchmark ranking; it only checks bounded mechanics if approved. |
| Proxy metric promoted | Guarded: finite gradients or short mechanics smokes cannot establish HMC readiness or posterior correctness. |
| Missing stop conditions | Guarded by explicit HMC approval, refreshed plan, bounded smoke scope, artifact validity, and claim boundaries. |
| Unfair comparison | Guarded: P06 does not compare samplers unless a refreshed plan explicitly adds a comparator and uncertainty contract. |
| Hidden assumptions | Guarded: P06 may be skipped and HMC remains a nonclaim. |
| Stale context | Guarded: P06 must be refreshed after P05 because default-surface code may change. |
| Environment mismatch | Guarded: any GPU/autodiff runtime must record device, XLA, dtype, TF32, and seed/state provenance. |
| Artifact mismatch | Guarded: P06 result must separate mechanics evidence from HMC-readiness and scientific claims. |

Audit conclusion: P06 remains provisional and optional after P04. It must not
execute until P05 closes, P06 is refreshed/reviewed, and explicit P06 approval
is granted. If skipped, the program can still proceed to P07 with HMC readiness
as a nonclaim.

## Evidence Contract

- Question: do the bounded default-route mechanics expose immediate
  TensorFlow/XLA/autodiff barriers relevant to future HMC work?
- Baseline/comparator: none by default; this is a mechanics screen, not a
  sampler comparison. If a comparator is needed, the refreshed P06 subplan must
  name it and state an uncertainty contract.
- Primary pass criterion: approved focused mechanics artifacts show finite,
  graph-compatible TensorFlow/XLA/autodiff behavior for the scoped operation
  under test, and the P06 result preserves HMC-readiness as a nonclaim unless a
  separately approved HMC gate is added.
- Veto diagnostics: absent P06 approval; stale P06 plan after P05; nonfinite
  values; graph/XLA failure; gradient disconnection where gradient is required;
  fallback to NumPy implementation; unplanned public API/package/model change;
  long-chain MCMC or scientific claim without separate plan and approval.
- Explanatory diagnostics: finite-value checks, gradient norms, traced device
  placement, XLA compile status, warning counts, and any smoke timings.
- Not concluded: posterior correctness, sampler convergence, HMC readiness,
  scientific validity, statistical superiority, dense Sinkhorn equivalence,
  public API readiness, or production readiness.
- Artifact preserving result: P06 result, focused smoke artifacts if executed,
  updated ledgers, and refreshed P07 subplan.

## Forbidden Claims And Actions

- Do not execute HMC/autodiff runtime before P06 is refreshed/reviewed and
  explicit P06 approval is granted.
- Do not run long MCMC chains, sampler comparisons, network fetches, package
  installs, public API changes, model-file changes, or dependency changes
  without separate approval.
- Do not claim HMC readiness, posterior correctness, sampler convergence,
  scientific validity, statistical superiority, dense Sinkhorn equivalence,
  public API readiness, or production readiness from a mechanics smoke.
- Do not introduce NumPy as BayesFilter-owned algorithmic implementation.
- Do not treat Claude as execution authority.

## Exact Next-Phase Handoff Conditions

- If P06 is skipped, write a skipped/nonclaim P06 result and hand off to P07.
- If P06 passes bounded mechanics, write the P06 result and hand off to P07 with
  HMC readiness still classified according to the result's evidence class.
- If P06 fails a mechanics screen, write a blocker/repair result and hand off
  to P07 with HMC explicitly noncertified unless the user approves repair.
- If P06 discovers that HMC work requires model-file, package, dependency,
  public API, or scientific-claim boundaries, stop for human direction.

## Stop Conditions

- P05 result is absent.
- P06 subplan is stale after P05.
- Explicit P06 approval is absent and P06 is not being skipped.
- Any runtime would cross unapproved HMC, package, dependency, public API,
  model-file, network, or scientific-claim boundaries.
- Required mechanics artifacts are missing, corrupt, nonfinite, or fail their
  scoped pass criteria.
- Claude/Codex review does not converge after five rounds for the same blocker.

## End-Of-Subplan Duties

1. Run required local checks or write the skipped/nonclaim result.
2. Write the P06 result or blocker result.
3. Draft or refresh P07.
4. Review P07 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.

## Provisional Self-Review

- Consistency: optional branch, downstream of P05.
- Correctness: separates mechanics from HMC readiness.
- Feasibility: bounded smoke only unless refreshed and approved otherwise.
- Artifact coverage: P06 result, optional smoke artifacts, ledgers, P07 refresh.
- Boundary safety: no HMC runtime or claim without explicit P06 approval.
