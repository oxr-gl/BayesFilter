# LEDH-PFPF-OT Autodiff-Free Adjoint Contract

date: 2026-06-23
status: ACTIVE_P0_CONTRACT_FREEZE
program: LEDH-PFPF-OT-AUTODIFF-FREE-ADJOINT

## Purpose

This contract freezes the no-production-autodiff invariant for the
LEDH-PFPF-OT SIR gradient program.  It exists to prevent another partial
manual-gradient route from advancing while an outer or hidden autodiff path
still computes the production gradient.

## Inherited Stop-State Lock

The inherited reviewed state is locked as:

```text
S7R_BLOCKED_N2500_GPU_OOM_REVIEWED
```

The locked facts are:

- N100 and N1000 actual-gradient artifacts were validated only for the prior
  remediated partial route.
- N2500 stopped with trusted GPU `RESOURCE_EXHAUSTED`.
- No valid N10000 actual-gradient artifact exists.
- S8/P82 finite-difference consistency work remains prohibited.
- P0 authorizes no new GPU rung, FD run, implementation change, default-policy
  change, HMC claim, production-readiness claim, or scientific claim.

## Production Route

For this program, "production route" means the route selected to produce
LEDH-PFPF-OT SIR actual-gradient artifacts for certification and GPU ladder
gates, including:

- the filter objective and returned gradient;
- every called LEDH flow, log-weight, resampling, and transport component;
- every `tf.custom_gradient` boundary and its `grad` body;
- every helper or callback reached by that route;
- every command path bound to the Phase 8/Phase 9 route manifest.

Phase 1 must pin this route with exact file and line anchors before any repair
phase can claim progress.

## Diagnostic Route

Diagnostic or test-only autodiff is allowed only when all of the following are
true:

- it is listed by exact path or exact symbol in a zero-default whitelist;
- it is not imported into or reached by the production route;
- it is used only to explain or debug, never as a promotion criterion;
- the artifact says it is diagnostic-only.

Diagnostic autodiff cannot certify the production route, cannot substitute for
the no-autodiff audit, and cannot authorize GPU ladder or FD advancement.

## Forbidden Production Autodiff APIs

The production route must not call or hide:

- `tf.GradientTape`;
- `tf.autodiff.ForwardAccumulator`;
- tape `.gradient(`;
- tape `.jacobian(`;
- tape `.batch_jacobian(`;
- `tf.gradients`;
- custom-gradient `grad` bodies that open autodiff;
- callbacks or helper functions whose production gradient depends on
  TensorFlow autodiff.

## Allowed Production Mechanisms

The production route may use:

- TensorFlow tensor math in forward code;
- `tf.custom_gradient` only as a boundary whose `grad` body is manually coded;
- manually coded adjoints for model, flow, log-weight, transport, and filter
  recursions;
- static and runtime no-autodiff sentinels;
- exact route manifests that bind the audited route to later GPU artifacts.

## Binary Gate

No production LEDH-PFPF-OT gradient artifact may count unless the selected route
passes an explicit no-autodiff audit bound to the exact same route manifest.

An audit pass is not portable across command flags, entrypoints,
`transport_ad_mode`, transport gradient mode, transport plan mode, dtype/TF32
policy, chunk settings, seed policy, whitelist hash, or audit-tool hash.

## Phase Advancement Locks

- P1 may start only after P0 result, execution ledger, stop handoff, and P1
  subplan all preserve this contract and the inherited stop-state lock.
- GPU ladder remains prohibited until Phase 8 audit passes on the exact route
  manifest.
- FD remains prohibited until Phase 9 produces a valid audited N10000
  actual-gradient artifact.
- If any phase is `BLOCKED` or `FAILED`, the program stops until a reviewed
  remediation plan exists and passes.

## Nonclaims

This contract does not claim:

- that any current route is autodiff-free;
- that any implementation repair has been completed;
- that the no-autodiff audit tool exists;
- that N10000 is feasible;
- that FD agreement, posterior correctness, HMC readiness, production
  readiness, default-policy promotion, or scientific superiority has been
  established.
