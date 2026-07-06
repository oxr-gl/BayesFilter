# BayesFilter LGSSM-First NeuTra/HMC Phase 5 Fixed Transport Result

Date: 2026-07-06

## Scope

This result closes Phase 5 of the LGSSM-first NeuTra/HMC program. It records
fixed identity/affine transport mechanics against the validated LGSSM generic
target.

This is fixed-transport mechanics evidence only. It is not NeuTra training
evidence, learned transport quality evidence, HMC convergence evidence,
posterior validation, production readiness, default-policy change, or
scientific promotion.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can fixed transports bind to the validated LGSSM target without changing target identity or hiding chain-rule errors? |
| Baseline/comparator | Phase 4 LGSSM target and existing fixed-transport mechanics helpers. |
| Primary criterion | Transported value/score matches base chain rule on probes and rejects mismatched signatures. |
| Veto diagnostics | Signature mismatch accepted, nonfinite transformed values/scores, fallback authority promoted, HMC/training hidden, GPU use, or DSGE/c603 transport import. |
| Explanatory diagnostics | Transport hash, manifest hash, probe residuals. |
| Not concluded | Learned NeuTra quality, HMC convergence, posterior correctness, production readiness. |
| Artifact | This Phase 5 result and focused tests. |

## Implemented Artifact

| Artifact | Purpose |
| --- | --- |
| `tests/test_lgssm_fixed_transport_mechanics_tf.py` | Focused CPU-only tests for LGSSM fixed affine-diagonal transport loading, identity equality, affine chain rule, target-signature mismatch rejection, mechanics manifest stability, and finite mechanics value/score. |

The tests use synthetic frozen affine-diagonal payloads with the Phase 4 LGSSM
target signature. No transport is trained and no DSGE/c603 payload is imported.

## Local Checks

| Check | Status |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_lgssm_fixed_transport_mechanics_tf.py -q` | `passed`: 4 tests, 2 TFP deprecation warnings. |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_neutra_artifact_loader.py tests/test_fixed_transport_hmc_binding.py -q` | `passed`: 12 tests. |
| `python -m py_compile tests/test_lgssm_fixed_transport_mechanics_tf.py` | `passed`. |
| `git diff --check -- tests/test_lgssm_fixed_transport_mechanics_tf.py ...Phase 5 planning artifacts...` | `passed`. |

## Decision Table

| Decision | Status |
| --- | --- |
| Phase 5 primary criterion | `passed`: identity and affine transport value/score chain-rule checks passed, target-signature mismatch was rejected, mechanics manifest was finite and stable. |
| Veto diagnostics | `not fired`: no signature mismatch acceptance, nonfinite transformed value/score, fallback authority promotion, HMC sampling, NeuTra training, GPU job, package install, git operation, DSGE/c603 import, default-policy change, or claim promotion occurred. |
| Main uncertainty | These are synthetic fixed transports. They validate binding mechanics, not learned NeuTra quality. |
| Next justified action | Refresh Phase 6 as a training approval/request gate before any LGSSM NeuTra training. |
| What is not concluded | No learned NeuTra quality, HMC convergence, posterior correctness, production readiness, default-policy change, or scientific validity. |

## Review

Passed bounded read-only substitute review.

| Reviewer | Scope | Verdict |
| --- | --- | --- |
| Fresh Codex reviewer `019f3865-2709-7320-80e8-f833787891c2` | Phase 5 review bundle and named artifacts only | `VERDICT: AGREE` |

## Handoff To Phase 6

Phase 6 must not run training until explicit approval is obtained. If approval
is absent, Phase 6 should close as a training-approval/request gate or stop
handoff, not silently train.
