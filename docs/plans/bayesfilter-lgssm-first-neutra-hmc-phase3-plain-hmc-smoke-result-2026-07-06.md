# BayesFilter LGSSM-First NeuTra/HMC Phase 3 Plain HMC Smoke Result

Date: 2026-07-06

## Scope

This result closes Phase 3 of the LGSSM-first NeuTra/HMC program. It records a
tiny CPU-only plain HMC mechanics smoke against the Phase 2 generic rank-2
LGSSM adapter.

This is a mechanics/runtime smoke only. It is not HMC convergence evidence,
posterior validation, sampler ranking, NeuTra readiness, production readiness,
default-policy change, or scientific promotion.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does a tiny plain HMC smoke execute against the reviewed LGSSM target adapter without immediate mechanics/runtime failure? |
| Baseline/comparator | Phase 2 generic LGSSM target adapter and existing opt-in QR static LGSSM HMC smoke harness. |
| Primary criterion | Tiny smoke completes with finite target evaluations and no crash. |
| Veto diagnostics | Nonfinite target, crash, hidden long chain, GPU use, retuning beyond plan, or smoke promoted to convergence. |
| Explanatory diagnostics | Acceptance, step size, leapfrog count, runtime, finite checks. |
| Not concluded | HMC convergence, posterior correctness, sampler ranking, production readiness. |
| Artifact | This Phase 3 result, smoke JSON, and smoke log. |

## Run Manifest

| Field | Value |
| --- | --- |
| Command | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp/bayesfilter-mplconfig python - <<'PY' > docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase3-plain-hmc-smoke-2026-07-06.log 2>&1 ... PY` |
| Runtime | `tfp.mcmc.sample_chain` |
| Target | `bayesfilter.testing.lgssm_generic_target_adapter_tf.make_lgssm_generic_target_fixture` |
| State shape | rank-2 `[1, 2]` |
| `num_results` | `8` |
| `num_burnin_steps` | `4` |
| `step_size` | `0.02` |
| `num_leapfrog_steps` | `3` |
| Seed | `[20260706, 3]` |
| CPU/GPU status | CPU-only by `CUDA_VISIBLE_DEVICES=-1`; no GPU evidence claimed. |
| JSON artifact | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase3-plain-hmc-smoke-2026-07-06.json` |
| Log artifact | `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase3-plain-hmc-smoke-2026-07-06.log` |

## Result Summary

| Diagnostic | Value | Role |
| --- | --- | --- |
| finite sample count | `8` | primary mechanics screen |
| nonfinite sample count | `0` | primary mechanics veto |
| sample shape | `[8, 1, 2]` | interface-shape diagnostic |
| initial score finite | `true` | primary mechanics screen |
| acceptance rate | `1.0` | explanatory only |
| max absolute log accept ratio | `7.605363029616896e-05` | explanatory only |
| wall time seconds | `2.8518056171014905` | explanatory only |
| target signature | `290a91d2a8f90d5b29243965b258b1ec6fd965aa46ffca69dcb78f7fa1ecabcb` | identity diagnostic |
| adapter signature | `0a48b43d2750cad5b452708f7619a1119a259231d8955769809460f256575a97` | identity diagnostic |

The smoke passed the stated mechanics screen: it completed, returned finite
samples and finite target diagnostics, and did not crash.

TensorFlow emitted CUDA plugin/cuInit warnings in the log despite
`CUDA_VISIBLE_DEVICES=-1`. Because this was a deliberate CPU-only smoke and no
GPU result is claimed, these warnings are recorded as environment noise, not
driver/GPU evidence.

## Decision Table

| Decision | Status |
| --- | --- |
| Phase 3 primary criterion | `passed`: tiny CPU-only HMC mechanics smoke completed with finite target/sample diagnostics and no crash. |
| Veto diagnostics | `not fired`: no nonfinite sample, crash, GPU job, retuning, long chain, transport binding, NeuTra training, package install, git operation, DSGE/c603 runtime, default-policy change, or claim promotion occurred. |
| Main uncertainty | This smoke is intentionally too short to say anything about posterior convergence or sampler quality. |
| Next justified action | Refresh Phase 4 as deterministic LGSSM reference validation before any longer or decision-making sampler validation. |
| What is not concluded | No HMC convergence, posterior correctness, sampler ranking, production readiness, NeuTra readiness, default-policy change, or scientific validity. |

## Local Checks

| Check | Status |
| --- | --- |
| Phase 3 smoke command wrote JSON and log artifacts | `passed` |
| JSON summary readback found finite sample count `8`, nonfinite count `0`, sample shape `[8, 1, 2]` | `passed` |
| Bounded log tail inspected | `passed`, with CUDA/cuInit warnings recorded as CPU-only environment noise. |

## Review

Passed bounded read-only substitute review.

| Reviewer | Scope | Verdict | Note |
| --- | --- | --- | --- |
| Fresh Codex reviewer `019f384d-e06a-7ed0-b7d7-7b6d43de0d84` | Phase 3 review bundle and named artifacts only | `VERDICT: AGREE` | Noted one harmless duplicate checklist line in Phase 4 subplan. |

## Handoff To Phase 4

Phase 4 may begin. The refreshed Phase 4 subplan starts with deterministic
LGSSM target/reference validation. Any longer or decision-making HMC posterior
validation remains outside current approval and must get an explicit reviewed
plan and approval before execution.
