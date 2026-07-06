# BayesFilter LGSSM-First NeuTra/HMC Phase 2 Target Adapter Result

Date: 2026-07-06

## Scope

This result closes Phase 2 of the LGSSM-first NeuTra/HMC program. It records a
BayesFilter-owned static QR LGSSM target exposed through the generic
`SSMTargetContract` and `GenericSSMPosteriorAdapter` surfaces.

This is an adapter-level implementation result only. It is not an HMC
convergence claim, posterior validation claim, NeuTra-readiness claim,
production-readiness claim, default-policy change, or scientific promotion.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter expose a real exact LGSSM posterior target through the generic batch-native SSM adapter? |
| Baseline/comparator | Phase 1 inventory, `QRStaticLGSSMTarget`, exact QR Kalman likelihood code, and existing QR derivative diagnostics. |
| Primary criterion | Adapter emits finite rank-2 posterior value/score, stable target signature, and focused gradient/reference checks pass. |
| Veto diagnostics | Process-local signature, shape ambiguity, nonfinite value/score, gradient/reference mismatch, hidden HMC/training/GPU, or DSGE/c603 dependency. |
| Explanatory diagnostics | Target signature, adapter signature, finite probes, gradient residuals. |
| Not concluded | HMC convergence, posterior validation, NeuTra readiness, production readiness, scientific validity. |
| Artifact | This Phase 2 result, helper module, and focused tests. |

## Implemented Artifacts

| Artifact | Purpose |
| --- | --- |
| `bayesfilter/testing/lgssm_generic_target_adapter_tf.py` | Testing helper that builds a static QR LGSSM `SSMTargetContract`, rank-2 Gaussian prior value/score, rank-2 QR Kalman likelihood value/score, and composed `GenericSSMPosteriorAdapter`. |
| `tests/test_lgssm_generic_target_adapter_tf.py` | Focused CPU-only tests for stable contract/signature, finite batch values/scores, direct prior-plus-likelihood tie-out, batch-of-one equivalence to source fixture, rank-1 rejection, manifest stability, finite-difference score, and analytic QR likelihood score agreement. |

The helper is intentionally under `bayesfilter/testing/`. It is not exported as
a production SSM API.

## Adapter Signatures

CPU-only signature probe produced:

| Field | Value |
| --- | --- |
| `stable_ssm_target_signature` | `290a91d2a8f90d5b29243965b258b1ec6fd965aa46ffca69dcb78f7fa1ecabcb` |
| `stable_ssm_posterior_adapter_signature` | `0a48b43d2750cad5b452708f7619a1119a259231d8955769809460f256575a97` |
| initial batch shape | `(1, 2)` |

TensorFlow emitted CUDA initialization warnings during the CPU-only signature
probe despite `CUDA_VISIBLE_DEVICES=-1`. Because this was a deliberate
CPU-only check that completed successfully, these warnings are recorded as
environment noise, not GPU evidence.

## Local Checks

| Check | Status |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_lgssm_generic_target_adapter_tf.py -q` | `passed`: 8 tests, 2 TFP deprecation warnings. |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_general_ssm_target_builder.py tests/test_linear_qr_compact_loglik_tf.py -q` | `passed`: 23 tests. |
| `CUDA_VISIBLE_DEVICES=-1 python - <<'PY' ... signature probe ... PY` | `passed`: target and adapter signatures printed. |
| `python -m py_compile bayesfilter/testing/lgssm_generic_target_adapter_tf.py tests/test_lgssm_generic_target_adapter_tf.py` | `passed`. |
| `git diff --check -- ...Phase 2 code/test/planning artifacts...` | `passed`. |

## Decision Table

| Decision | Status |
| --- | --- |
| Phase 2 primary criterion | `passed`: finite rank-2 value/score, stable target/adapter signature, direct tie-outs, finite-difference score, and analytic QR likelihood score checks passed. |
| Veto diagnostics | `not fired`: no HMC, NeuTra training, GPU job, package install, git operation, transport binding, DSGE/c603 runtime, default-policy change, or scientific claim was run/made. |
| Main uncertainty | The rank-2 likelihood helper uses a Python loop over batch rows for this testing fixture. That is acceptable for Phase 2 adapter correctness, but it is not a production performance claim. |
| Next justified action | Refresh Phase 3 to run a tiny CPU-only plain HMC mechanics smoke against the generic LGSSM adapter. |
| What is not concluded | No HMC convergence, posterior validation, NeuTra readiness, production readiness, default-policy change, sampler ranking, or scientific validity. |

## Review

Passed bounded read-only substitute review.

| Reviewer | Scope | Verdict |
| --- | --- | --- |
| Fresh Codex reviewer `019f3845-c433-7e13-9961-3a174d3bb980` | Phase 2 review bundle and named artifacts only | `VERDICT: AGREE` |

## Handoff To Phase 3

Phase 3 may begin. It must use the generic LGSSM adapter from
`bayesfilter/testing/lgssm_generic_target_adapter_tf.py`, not the older rank-1
fixture directly, and it must remain a tiny CPU-only HMC mechanics smoke with
explicit nonclaims.
