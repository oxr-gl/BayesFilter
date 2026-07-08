# P91 Production Contract: Zhao-Cui SIR d18 Score-Identity And HMC/GPU Readiness

Date: 2026-06-29

Status: `P91_PRODUCTION_CONTRACT_LOCAL_READY_PENDING_REVIEW`

## Purpose

This contract supersedes the P90 FD-first production blocker framing for
Zhao-Cui SIR d18. P91 treats Zhao-Cui as an approximate high-dimensional
score/likelihood method. Production readiness requires score-identity
validation, FD engineering consistency, batched API correctness, GPU/XLA HMC
capability, model-specific CPU/GPU benchmarks, HMC smoke, and release caveats.

This contract does not promote Zhao-Cui to production.

## Inherited P90 State

P90 final status:

```text
ZHAO_CUI_SIR_D18_NOT_PRODUCTION_READY_UNDER_P90
```

P90 retained positives:

- Phase 3 same-scalar value bridge passed.
- Phase 5 deterministic derivative-carry implementation passed focused local
  tests.

P90 unresolved blockers remain relevant unless replaced by reviewed P91 gates:

- full source-route analytical derivative readiness;
- FD consistency;
- HMC readiness;
- GPU/XLA production readiness;
- packaging, CI, release, and default readiness.

## Owner Decisions Recorded

| Decision | Contract |
| --- | --- |
| Scientific gate | Score identity at true parameters across multiple regimes/seeds is the primary scientific validation gate. |
| FD role | FD consistency is necessary engineering evidence for the implemented scalar/score, but it is not a truth oracle and does not prove exact likelihood correctness. |
| Root solving | Solving `score(theta) = 0` is not a production gate for high-dimensional Zhao-Cui. |
| Hessian/information checks | Hessian, information equality, and sandwich covariance checks are optional/advisory. |
| GPU/XLA role | GPU/XLA JIT capability is required for HMC-facing production. |
| CPU/GPU speed | CPU/GPU performance is model-specific; GPU is not assumed universally faster. |
| Batched route | Single and batched value/score APIs are required, and batched outputs must agree with looped single outputs. |
| Training | Training-base route only; no ALS revival. If training is used, L1 tuning remains the Zhao-Cui default. |

## Required Production Gates

Zhao-Cui SIR d18 may be recommended for production only if all required P91
gates pass with reviewed artifacts:

1. Score contract freeze.
2. Single and batched value/score API parity.
3. FD engineering evidence against the same implemented scalar/score, or an
   explicit owner-reviewed acceptance of a limited FD diagnostic with caveats.
4. Score identity across multiple `theta_0` regimes and seeds.
5. GPU/XLA JIT capability for HMC-facing value/score paths.
6. CPU/GPU/single/batched benchmarks with model-specific recommendations.
7. HMC smoke on the compiled HMC-facing route.
8. Packaging/CI/release-note readiness with explicit caveats.
9. Final decision from reviewed evidence only.

## Required Non-Claims

P91 artifacts must not claim:

- exact likelihood correctness from score identity;
- FD as a true-gradient oracle;
- universal GPU speed superiority;
- posterior correctness from HMC smoke;
- root-solving validity without a separate reviewed artifact;
- Hessian/information equality without a separate reviewed artifact;
- release, package, CI mutation, or default-policy change without required
  authorization.

## Runtime And Authority Boundaries

- Phase 0 is document-only.
- CPU-only numerical runs must hide GPU before framework import and record that
  choice.
- GPU/CUDA/XLA/HMC commands require trusted/escalated execution and exact
  reviewed subplans.
- Package installation, network fetch, release, CI-service mutation, and
  default-policy changes require reviewed subplans and any required human
  authorization.
- Claude is read-only reviewer only.

## Initial Score-Identity Standard

The default initial score-identity plan is:

- four true-parameter regimes: baseline/moderate, low infection, high
  infection, and near-boundary but numerically stable;
- ten seeds per regime initially;
- componentwise average score within the reviewed uncertainty criterion,
  with the initial owner-requested finite-sample screen recorded as
  `2 sample SD`; standard-error z-scores are advisory diagnostics;
- componentwise failures reported explicitly, with optional joint diagnostics
  advisory only.

This is validation of approximate score behavior, not proof of exact
likelihood truth.

## Release-Note Caveat Seed

Any P91 release note should say, in substance:

```text
Zhao-Cui SIR d18 is validated as an approximate high-dimensional
score/likelihood method by simulation score-identity checks, FD engineering
consistency, GPU/XLA capability checks, model-specific benchmarks, and HMC
smoke. These checks do not certify exact likelihood correctness, posterior
correctness, or universal GPU superiority.
```

## Phase 1 Handoff

Phase 1 must freeze the score contract: score sign/convention,
parameterization, fixed setup policy, branch/retained identity, derivative
policy, single/batched API semantics, and release caveats. Phase 1 must not run
FD, score-identity, GPU/XLA, HMC, benchmark, package/release/CI, or
default-policy commands.
