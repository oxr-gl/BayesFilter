# P91 Score Contract: Zhao-Cui SIR d18

Date: 2026-06-29

Status: `P91_SCORE_CONTRACT_LOCAL_READY_PENDING_REVIEW`

## Scope

This contract freezes score semantics for the P91 Zhao-Cui SIR d18 production
program. It is a document/source-inventory contract only. It does not
implement a new score route, run FD, run score identity, run GPU/XLA, run HMC,
benchmark performance, package/release/CI, change defaults, or claim production
readiness.

## Contract Anchors

| Anchor | Path / symbol | Contract role |
| --- | --- | --- |
| Production standard | `docs/plans/bayesfilter-highdim-zhao-cui-p91-production-contract-2026-06-29.md` | P91 gates and non-claims. |
| P90 value target | `bayesfilter/highdim/source_route.py:P90_VALUE_BRIDGE_TARGET_ID` | Target id is `zhao_cui_sir_austria_d18`. |
| P90 value binding | `bayesfilter/highdim/source_route.py:SourceRouteValueBridgeBinding` | Branch/setup identity: target, time, parameter/state dimensions, physical ordering, retained hash, basis/rank/sample/seed, transport hash, coordinate-frame hash, callable ids. |
| P90 derivative binding | `bayesfilter/highdim/source_route.py:SourceRouteDerivativeBinding` | Same-branch derivative binding plus explicit fixed TTSIRT derivative blocker. |
| P90 component carry | `bayesfilter/highdim/source_route.py:SourceRouteComponentDerivativeCarry` | Component value/parameter-score shape and finite checks. |
| P90 assembly carry | `bayesfilter/highdim/source_route.py:source_route_negative_log_assembly_derivative_carry` | Negative-log assembly sign convention. |
| Stable score API | `bayesfilter/highdim/score_api.py:HighDimScoreAPIResult` and `evaluate_highdim_score_api` | Existing highdim value/score API contract; finite value/score does not imply HMC readiness. |

## Score Sign And Scalar Convention

The P91 source-route score is the derivative of the implemented scalar used by
the selected API route. For the P90 source-route scalar, the bound scalar is a
negative log density:

```text
negative_log_scalar(theta)
  = - prior_or_previous_log_density(theta)
    - transition_log_density(theta)
    - likelihood_log_density(theta)
```

`source_route_negative_log_assembly_derivative_carry` encodes this sign by
negating the sum of component log-density parameter scores. Therefore:

```text
negative_log_score = d negative_log_scalar / d theta
                   = - d(prior_or_previous + transition + likelihood) / d theta
```

If a downstream API reports `log_likelihood` and `score`, it must state whether
`score` is the derivative of log likelihood or the derivative of negative log
likelihood. Phase 2 must fail closed if sign conventions are ambiguous.

## Parameterization And Shape

The released score contract uses a one-dimensional `theta` tensor. Existing
`HighDimScoreAPIResult` requires:

- `theta.shape.rank == 1`;
- `score.shape == theta.shape`;
- scalar value has rank zero;
- all theta/value/score entries are finite;
- diagnostics declare `api_scope == "bayesfilter.highdim"`;
- diagnostics declare `stable_subpackage_api is True`;
- diagnostics declare `stable_top_level_api is False`;
- diagnostics declare `hmc_readiness == "not_claimed"` unless a later P91 HMC
  gate changes that status through reviewed evidence.

Phase 1 does not choose a final public top-level API.

## Fixed Setup And Branch Identity

P91 inherits P90 same-branch discipline. Any score used for FD, score identity,
GPU/XLA, HMC, benchmark, or release must bind:

- target id;
- time index;
- parameter and state dimensions;
- physical ordering;
- previous retained hash when applicable;
- previous marginal keep/input axes when applicable;
- basis family/order/elements;
- TT rank tuple;
- sample count and seed;
- transport branch hash;
- coordinate-frame hash;
- transition/likelihood/prior callable identities;
- tolerance versions.

Phase 2 must expose these fields in an auditable channel for single and
batched calls. The required channel is a manifest, diagnostics payload, or
return metadata; Phase 2 must at minimum record them in the implementation
artifact manifest or diagnostics. A value/score artifact that omits setup
identity is not eligible for later FD, score-identity, GPU/XLA, HMC, benchmark,
or release gates.

## Derivative Policy

P91 does not claim full source-route analytical-gradient readiness at Phase 1.

Current derivative policy:

- transition and likelihood component score carries have local deterministic
  P90 evidence;
- negative-log assembly carry has local deterministic P90 evidence;
- previous marginal derivative owner remains blocked;
- fixed TTSIRT proposal/transport derivative owner remains blocked;
- any omitted/frozen derivative term must be surfaced in diagnostics and
  release notes rather than hidden.

This policy is intended to remain compatible with the downstream P91
simulation score-identity gate. This contract does not establish empirical
compatibility, and it is not a claim that omitted/frozen derivative terms are
harmless.

## Inherited Training And Basis Policy

The following constraints are inherited from the P91 production contract and
earlier owner/program direction. This score contract records them as external
inputs; it does not independently promote route, training, basis, or default
policy.

- Training-base route only for any new Zhao-Cui training wiring.
- No ALS revival.
- If training is used, L1 tuning is the default procedure.
- Basis/rank/setup are release parameters and must be recorded in manifests.
- Audit clouds are not tuning clouds.

## Single And Batched API Semantics

Phase 2 must implement or harden:

```text
single_value(theta, dataset_or_branch)
single_score(theta, dataset_or_branch)
batched_value(theta, batch_of_datasets_or_branches)
batched_score(theta, batch_of_datasets_or_branches)
```

The initial batched route must match looped single-route outputs under the same
theta/setup/branch identities and enforce a shared setup identity across all
batch items. If Phase 2 supports per-item setup identities instead, it must
return per-item identity metadata and fail closed on ambiguous or mixed
metadata. Batched performance is not scientific validity.

## Release Caveats Required Downstream

Any release note must state:

- score identity validates approximate score behavior, not exact likelihood
  truth;
- FD checks engineering consistency with the implemented scalar, not oracle
  truth;
- GPU/XLA capability is required for HMC-facing target, but CPU/GPU speed is
  model-specific;
- HMC smoke is not posterior correctness;
- omitted/frozen derivative policy must be documented.

## Nonclaims

This score contract does not conclude:

- FD consistency;
- score identity;
- GPU/XLA readiness;
- HMC readiness;
- CPU/GPU performance;
- packaging, CI, release, or default readiness;
- production readiness;
- exact likelihood correctness;
- posterior correctness;
- universal GPU superiority.

## Phase 2 Handoff

Phase 2 must either implement/harden single and batched value/score APIs under
this contract or close with an explicit API blocker. It must not run FD,
score-identity validation, GPU/XLA, HMC, benchmarks, packaging/release/CI, or
default-policy commands unless a reviewed Phase 2 refresh explicitly authorizes
a narrower diagnostic.
