# BayesFilter LGSSM-First NeuTra/HMC Phase 1 Interface Inventory Result

Date: 2026-07-06

## Scope

This result closes Phase 1 of the LGSSM-first NeuTra/HMC program. It is a
read-only interface inventory and Phase 2 handoff. It is not an implementation
result, posterior validation, HMC-readiness claim, NeuTra-readiness claim,
production-readiness claim, or scientific promotion.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What existing BayesFilter surfaces can be reused for an LGSSM-first target adapter and what gaps must Phase 2 close? |
| Baseline/comparator | Current `SSMTargetContract`, `GenericSSMPosteriorAdapter`, QR Kalman code, fixed-transport mechanics, and QR static LGSSM HMC smoke harness. |
| Primary criterion | Inventory classifies reusable surfaces and defines an exact Phase 2 implementation/test boundary without DSGE/c603 dependency. |
| Veto diagnostics | Treating opt-in HMC smoke as readiness, ignoring exact Kalman reference needs, hidden DSGE dependency, missing target-signature policy, or unreviewed GPU/training/HMC execution. |
| Explanatory diagnostics | File/symbol anchors, existing tests, target signature surfaces, gap table. |
| Not concluded | No new implementation correctness, no LGSSM posterior validation, no HMC readiness, no NeuTra readiness. |
| Artifact | This Phase 1 result and refreshed Phase 2 subplan. |

## Inventory Classification

| Surface | Anchor | Classification | Phase 2 implication |
| --- | --- | --- | --- |
| Generic SSM target metadata | `bayesfilter/ssm/contracts.py` lines 82-188, 191-244, 247-339, 393-506 | `reuse` | Use `SSMStaticShape`, `SSMDataSignature`, `BayesianSSMProblem`, `ParameterChart`, `ParameterPrior`, `FilterProgram`, `SSMTargetContract`, `stable_ssm_target_signature`, and validation gates as the target authority. |
| Process-local identity rejection and stable signatures | `bayesfilter/ssm/contracts.py` lines 71-75, 442-487, 509-520 and helper tail | `reuse` | Phase 2 must persist only stable manifest fields; no Python object identity or runtime addresses may enter signatures. |
| Batch-native posterior adapter | `bayesfilter/ssm/target_builder.py` lines 80-215 and 254-320 | `reuse` | Phase 2 should build through `build_ssm_posterior_adapter` and provide rank-2 `[B, D]` prior and LGSSM likelihood value/score functions. |
| Adapter metadata and nonclaims | `bayesfilter/ssm/target_builder.py` lines 25-32, 46-77, 151-179 | `reuse` | Phase 2 result must preserve nonclaims and must not mark XLA/full-chain HMC readiness. |
| Generic adapter tests | `tests/test_general_ssm_target_builder.py` lines 1-153 and 176-251 | `reuse` | Copy test shape: CPU-only TensorFlow import guard, rank-2 finite value/score, direct prior-plus-filter tie-out, finite-difference score, signature stability, and bad-shape rejection. |
| QR static LGSSM target fixture | `bayesfilter/testing/tf_hmc_readiness.py` lines 33-184 | `patch_needed` | Reuse its exact one-dimensional LGSSM model, prior, and curvature diagnostics as source material, but do not use it directly as the generic adapter because it is rank-1 and HMC-smoke oriented. |
| QR static LGSSM HMC smoke | `bayesfilter/testing/tf_hmc_readiness.py` lines 186-238 and `tests/test_hmc_linear_qr_readiness_tf.py` lines 10-73 | `blocked` for Phase 2 | Opt-in HMC smoke is deferred to Phase 3. Phase 2 may use only value/score/reference checks, not sampling. |
| QR Kalman value code | `bayesfilter/linear/kalman_qr_tf.py` lines 144-220 and related compact/batched functions | `reuse` | Phase 2 should compute exact LGSSM likelihood via current QR Kalman code under CPU-only tests. |
| QR Kalman derivative code | `bayesfilter/linear/kalman_qr_derivatives_tf.py` lines 64-260 and existing public wrapper used by the fixture | `reuse` or `patch_needed` | Phase 2 can tie analytic score to the existing static fixture path; if batch-native analytic derivatives are awkward, use per-row TensorFlow autodiff for the adapter and compare against analytic score for a batch of one. |
| QR compact/batched tests | `tests/test_linear_qr_compact_loglik_tf.py` lines 1-438 | `reuse` | Phase 2 should not re-prove QR Kalman. It should reference these existing checks and add adapter-specific tests only. |
| Fixed-transport HMC mechanics | `bayesfilter/inference/fixed_transport_hmc.py` lines 1-182 | `blocked` for Phase 2, `reuse` later | Preserve for Phase 5. Phase 2 must not bind transports or run HMC mechanics. |
| DSGE/c603 import material | Existing c603 handoff/import result notes | `blocked` until Phase 9 | c603 remains stress/import evidence only. It must not shape the Phase 2 LGSSM target adapter. |

## Findings

1. The current SSM contract stack is already the right authority boundary for
   BayesFilter-owned SSM targets. It validates shapes, charts, priors, filter
   target policy, frozen transport bindings, and stable signatures without
   process-local identity.
2. The current generic posterior adapter already enforces batch-native rank-2
   value/score semantics. Phase 2 does not need a new generic adapter
   abstraction.
3. The LGSSM material exists, but it is split across a rank-1 HMC-readiness
   fixture and QR Kalman value/derivative tests. Phase 2 should add a small
   LGSSM generic-adapter fixture/helper that composes those pieces through
   `SSMTargetContract`.
4. The exact Phase 2 boundary is an adapter construction and test boundary, not
   a sampler boundary. Phase 2 should stop before HMC, NeuTra training, GPU, or
   transport work.
5. DSGE/c603 is not needed for Phase 2 and remains intentionally deferred.

## Phase 2 Implementation Boundary

Phase 2 should add the smallest BayesFilter-owned LGSSM generic target surface:

- a helper module or test fixture that creates a deterministic static LGSSM
  `SSMTargetContract` using the QR static LGSSM model, two unconstrained
  parameters, Gaussian prior metadata, exact filter metadata, stable data/model
  hashes, and `approximation_semantics="exact"`;
- rank-2 prior value/score: for `theta: [B, 2]`, return Gaussian log prior
  values `[B]` and scores `[B, 2]`;
- rank-2 LGSSM likelihood value/score: for `theta: [B, 2]`, return QR Kalman
  log likelihood values `[B]` and scores `[B, 2]`;
- a composed `GenericSSMPosteriorAdapter` with stable target and adapter
  signatures;
- focused tests proving finite values/scores, direct prior-plus-likelihood
  tie-out, rank-2 batch-of-one behavior, rank-1 rejection, stable signature
  behavior, and score agreement against finite difference or existing analytic
  QR diagnostics.

Phase 2 should not add public HMC launch APIs, transport loaders, training
runners, default policies, package dependencies, or DSGE/c603 code.

## Decision Table

| Decision | Status |
| --- | --- |
| Phase 1 primary criterion | `passed`: inventory classifies surfaces and names Phase 2 boundary. |
| Veto diagnostics | `not fired`: no HMC, GPU, training, package, git, or DSGE/c603 runtime work was run. |
| Main uncertainty | Exact Phase 2 helper location: testing helper vs package helper. The safer initial choice is a test/support helper unless a public API is clearly needed. |
| Next justified action | Refresh Phase 2 subplan to implement the LGSSM generic adapter and focused CPU-only tests. |
| What is not concluded | No adapter correctness, posterior validation, HMC readiness, NeuTra readiness, production readiness, or scientific validity. |

## Local Checks

Passed after initial write.

| Check | Status |
| --- | --- |
| `test -f` Phase 1 result | `passed` |
| `test -f` Phase 1 review bundle | `passed` |
| `rg -n 'reuse\|patch_needed\|blocked' ...phase1-interface-inventory-result...` | `passed` |
| `rg -n 'DSGE/c603\|deferred\|stress' ...phase1 result... ...phase2 subplan...` | `passed` |
| `git diff --check -- docs/plans/bayesfilter-lgssm-first-neutra-hmc-* docs/reviews/bayesfilter-lgssm-first-neutra-hmc-*` scoped by explicit file list | `passed` |

One initial shell check used unescaped Markdown backticks and triggered command
substitution. That check result was discarded as a command quoting defect and
rerun with single-quoted `rg` syntax.

## Review

Passed bounded read-only substitute review.

| Reviewer | Scope | Verdict | Caveat |
| --- | --- | --- | --- |
| Fresh Codex reviewer `019f3806-8828-7382-8814-0634bd41c559` | Phase 1 review bundle and named planning artifacts only | `VERDICT: AGREE` | Artifact-consistency and boundary-safety review; not an independent source-line verification. |

## Handoff To Phase 2

Phase 2 may begin. The refreshed Phase 2 subplan must preserve this result's
implementation boundary and must not cross sampler, training, GPU, transport,
package, git, DSGE/c603, default policy, or scientific-claim boundaries.
