# P91 Release Notes Draft: Zhao-Cui SIR d18

Date: 2026-06-29

Status: `DRAFT_PENDING_PHASE8_REVIEW`

## Summary

P91 prepares Zhao-Cui SIR d18 for a final production decision as an approximate
high-dimensional score/likelihood route within a narrow validated scope. The
reviewed evidence now covers score contract, batched API semantics,
owner-accepted limited FD engineering evidence with caveats, local component
score identity, trusted GPU/XLA capability, model-specific CPU/GPU/batched
benchmarks, and a tiny trusted GPU/XLA HMC implementation smoke.

This draft does not publish a package, change defaults, or by itself promote
Zhao-Cui SIR d18 to production. Final promotion is reserved for Phase 9.

Throughout this draft, artifact-level `Passed` means a reviewed P91 gate passed
inside its stated scope. It does not mean final production promotion until
Phase 9 makes that decision.

## User-Facing Scope

Validated scope:

- model: Zhao-Cui SIR Austria d18 local complete-data component route;
- parameterization: three-parameter log-scale surface
  `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`;
- API surface: highdim subpackage only;
- single-score route: `evaluate_highdim_score_api`;
- batched-score route: `evaluate_batched_highdim_score_api`;
- XLA helper route:
  `zhao_cui_sir_austria_local_complete_data_log_density_xla` and
  `zhao_cui_sir_austria_batched_local_complete_data_log_density_xla`;
- GPU/XLA and HMC evidence: trusted local machine run on NVIDIA GeForce RTX
  4080 SUPER with TensorFlow `2.19.1` and TensorFlow Probability `0.25.0`.

Plain-language scope note:

- "local complete-data component route" means the checked target conditions on
  a fixed latent state path and observation path. It is the HMC-facing component
  used in P91 checks, not the full filtering likelihood after marginalizing
  latent states.
- "setup identity" means metadata proving that batched and single calls used
  the same fixed model/setup assumptions.
- "fails closed" means an ambiguous or missing setup identity is rejected
  rather than silently accepted.

Not validated by P91:

- exact likelihood correctness;
- posterior correctness or convergence;
- full observed-data/filtering score identity through previous marginal and
  fixed TTSIRT proposal/transport derivatives;
- full source-route FD derivative readiness;
- universal GPU speed superiority;
- package publication, CI-service mutation, release tagging, or default-policy
  change.

## Evidence Summary

| Gate | Artifact Status | Release Interpretation |
| --- | --- | --- |
| Score contract | Passed | Score sign, setup identity, branch metadata, batched semantics, and caveats are frozen for P91. |
| Batched API | Passed | Batched highdim API matches looped single API on deterministic fixtures and fails closed on missing/ambiguous setup identity. |
| FD consistency | Accepted with caveats | Limited t=1 FD diagnostic remains historical blocked evidence under its arbitrary `5e-5` tolerance, but owner accepted the small miss for continuation. This is not a full FD pass. |
| Score identity | Passed | Local complete-data component score satisfies the reviewed finite-sample screen: average scores at true parameters were no farther from zero than two sample standard deviations across four regimes and ten seeds each. Advisory standard-error z-scores suggest more seeds before stronger precision claims. |
| GPU/XLA JIT | Passed | Single and batched local complete-data value/score helpers compile and run on trusted GPU/XLA with finite outputs and stable tracing. |
| Performance | Passed | On the deterministic fixture, GPU/XLA steady timing is faster than CPU for single and batched routes, and batched per-item timing is better than looped single. This is model/fixture-specific. |
| HMC smoke | Passed | A tiny TFP HMC call under trusted GPU/XLA returns finite samples, target values, scalar per-sample gradients, and log-accept ratios with no OOM, retry, or post-warmup retrace. |

## Test And CI Split

Fast CPU-only checks:

- `tests/highdim/test_p91_batched_score_api.py`;
- `tests/highdim/test_p91_gpu_xla_local_target.py`;
- `tests/highdim/test_p91_fd_consistency_limited.py`;
- `tests/highdim/test_p91_score_identity.py`.

GPU/XLA and HMC evidence are not default fast CI. They require trusted GPU
execution and should be run deliberately:

- `scripts/p91_gpu_xla_jit_check.py`;
- `scripts/p91_performance_benchmark.py --target gpu --xla true`;
- `scripts/p91_hmc_smoke.py --xla true`.

Repository marker policy already includes:

- `gpu`: checks requiring escalated GPU/CUDA visibility;
- `hmc`: sampler-readiness checks run deliberately, not as default fast CI;
- `extended`: opt-in diagnostics that may take longer than the fast local gate.

## Operational Notes

- CPU-only runs must set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import and
  record that GPU was intentionally hidden.
- GPU/CUDA/XLA/HMC commands must run with trusted/escalated permissions.
- CPU/GPU performance recommendations are model-specific. P91 evidence says
  GPU/XLA is healthy and faster on the tested deterministic fixture; it does
  not say GPU is universally faster.
- The Phase 7 HMC smoke recorded `divergence_status = unavailable` because the
  TFP HMC trace did not expose a native boolean divergence field in the
  harness. No ESS, speed, or acceptance-rate proxy was used to override a hard
  veto.

## Preserved Caveats

P91 preserves these blocker labels:

- `BLOCK_FIXED_TTSIRT_PREVIOUS_MARGINAL_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FIXED_TTSIRT_PROPOSAL_TRANSPORT_DERIVATIVE_NOT_IMPLEMENTED`;
- `BLOCK_FULL_SOURCE_ROUTE_FD_NOT_CLAIMED`.

These blockers do not negate the local complete-data score/HMC evidence, but
they do prevent claiming full observed-data/filtering score readiness or exact
source-route derivative readiness.

In plain language, the unresolved derivative blockers mean P91 has not checked
all derivative terms needed for the full filtering route that integrates over
latent states. The supported evidence is for the local complete-data component
route named above.

## Recommended Release Wording

Suggested wording for a project release note after Phase 9, if final promotion
is approved:

```text
Zhao-Cui SIR d18 is supported only within the following validated P91 scope:
the highdim subpackage API and the local complete-data Zhao-Cui SIR d18
component route. Here, "local complete-data" means the checked target conditions
on a fixed latent state path and observation path; it is not the full filtering
likelihood after marginalizing latent states.

Within that scope, P91 evidence includes batched API parity, owner-accepted
limited FD engineering evidence with caveats, simulation score-identity checks
at true parameters, trusted GPU/XLA compile/run evidence, model-specific
CPU/GPU/batched benchmarks, and a tiny trusted GPU/XLA TFP HMC implementation
smoke.

These checks do not certify exact likelihood correctness, posterior
correctness, full observed-data/filtering score identity, full source-route FD
derivative readiness, or universal GPU speed superiority. Users should treat
CPU/GPU performance as model-specific and rerun the GPU/XLA/HMC checks on
their target model and hardware.
```

## Phase 9 Handoff

Phase 9 must decide whether these reviewed artifacts are sufficient for final
P91 production promotion. This draft intentionally does not make that final
decision.
