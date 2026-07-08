# BayesFilter LGSSM-First NeuTra/HMC Phase 4 Reference Validation Result

Date: 2026-07-06

## Scope

This result closes Phase 4 of the LGSSM-first NeuTra/HMC program. It records a
deterministic CPU-only target/reference validation for the Phase 2 generic
LGSSM adapter.

This is deterministic target validation only. It is not HMC convergence
evidence, stochastic posterior validation, sampler ranking, NeuTra readiness,
production readiness, default-policy change, or scientific promotion.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the Phase 2 generic LGSSM target agree with deterministic source-fixture and grid references under stated tolerances? |
| Baseline/comparator | `QRStaticLGSSMTarget.target_log_prob`, exact QR Kalman value/score checks, and deterministic fixed grid over the two unconstrained coordinates. |
| Primary criterion | Adapter-source value residual and finite-difference score residual stay below predeclared tolerances with all grid values finite. |
| Veto diagnostics | Nonfinite grid value/score, value residual above `1e-9`, finite-difference score residual above `1e-4`, hidden HMC sampling, GPU use, or posterior claims beyond deterministic target validation. |
| Explanatory diagnostics | Grid log normalizer, grid posterior mean/covariance, maximum/minimum log posterior, runtime. |
| Not concluded | HMC convergence, stochastic posterior validation, generic nonlinear SSM validity, NeuTra readiness, production readiness. |
| Artifact | This result, deterministic reference JSON, and bounded log. |

## Run Manifest

| Field | Value |
| --- | --- |
| Command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-mplconfig python - <<'PY' > docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-2026-07-06.log 2>&1 ... PY` |
| Target | Phase 2 generic LGSSM adapter |
| Comparator | `QRStaticLGSSMTarget.target_log_prob` and finite differences of the generic adapter |
| Grid | `25 x 25`, 625 points |
| Rho range | `[-0.1, 0.5]` |
| Log measurement noise range | `[-1.4, -0.7]` |
| Value tolerance | `1e-9` |
| Score tolerance | `1e-4` |
| CPU/GPU status | CPU-only by `CUDA_VISIBLE_DEVICES=-1`; no GPU evidence claimed. |
| JSON artifact | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-2026-07-06.json` |
| Log artifact | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase4-lgssm-reference-validation-2026-07-06.log` |

## Result Summary

| Diagnostic | Value | Role |
| --- | --- | --- |
| all values finite | `true` | primary target/reference screen |
| max adapter-source value residual | `0.0` | primary target/reference screen |
| max selected finite-difference score residual | `4.7978010453419984e-11` | primary target/reference screen |
| grid point count | `625` | deterministic coverage diagnostic |
| grid log normalizer | `-2.2189897648018` | explanatory finite-grid artifact only |
| grid mean | `[0.1878462782084164, -1.0925644016315064]` | explanatory finite-grid artifact only |
| target signature | `290a91d2a8f90d5b29243965b258b1ec6fd965aa46ffca69dcb78f7fa1ecabcb` | identity diagnostic |
| adapter signature | `0a48b43d2750cad5b452708f7619a1119a259231d8955769809460f256575a97` | identity diagnostic |

The deterministic reference gate passed. The generic adapter matched the source
fixture value exactly on the fixed grid, and selected finite-difference score
residuals were far below the predeclared tolerance.

TensorFlow emitted CUDA plugin/cuInit warnings in the log despite
`CUDA_VISIBLE_DEVICES=-1`. Because this was a deliberate CPU-only validation
and no GPU result is claimed, these warnings are recorded as environment noise,
not driver/GPU evidence.

## Decision Table

| Decision | Status |
| --- | --- |
| Phase 4 primary criterion | `passed`: all fixed-grid values/scores finite, value residual `0.0 <= 1e-9`, score residual `4.7978010453419984e-11 <= 1e-4`. |
| Veto diagnostics | `not fired`: no nonfinite grid values/scores, residual failure, HMC sampling, GPU job, NeuTra training, package install, git operation, DSGE/c603 runtime, default-policy change, or claim promotion occurred. |
| Main uncertainty | Grid moments are finite-grid artifacts only; they are not exact continuous posterior moments. |
| Next justified action | Refresh Phase 5 as fixed identity/affine transport mechanics binding against the validated LGSSM target. |
| What is not concluded | No HMC convergence, stochastic posterior validation, generic nonlinear SSM validity, NeuTra readiness, production readiness, default-policy change, or scientific validity. |

## Local Checks

| Check | Status |
| --- | --- |
| Phase 4 deterministic validation command wrote JSON and log artifacts | `passed` |
| JSON readback found `pass=true`, all values finite, value residual `0.0`, score residual `4.7978010453419984e-11`, grid point count `625` | `passed` |
| Bounded log tail inspected | `passed`, with CUDA/cuInit warnings recorded as CPU-only environment noise. |

## Review

Passed bounded read-only substitute review.

| Reviewer | Scope | Verdict |
| --- | --- | --- |
| Fresh Codex reviewer `019f385e-05bd-7331-b2d1-211f67e1cac0` | Phase 4 review bundle and named artifacts only | `VERDICT: AGREE` |

## Handoff To Phase 5

Phase 5 may begin. It must remain fixed identity/affine transport mechanics
binding against the validated LGSSM target. It must not train NeuTra, use GPU,
run long HMC, change defaults, or claim HMC readiness/posterior correctness.
