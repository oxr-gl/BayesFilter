# P02 Result: LGSSM Exact-Reference Gate

Date: 2026-06-25

Status: `P02_PASS_REPAIRED_PENDING_REVIEW_TO_P03_ACTUAL_SIR_STRESS`

## Phase Objective

Test fixed SVD-Nystrom value-route behavior on an LGSSM case with exact Kalman
reference before nonlinear and resource stress.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does fixed SVD-Nystrom pass an LGSSM exact-reference quality gate? |
| Baseline/comparator | Exact Kalman reference for the declared LGSSM; streaming route may be explanatory. |
| Primary criterion | Deterministic validity and predeclared exact-reference error thresholds pass for all included rows. |
| Veto diagnostics | Exact-reference failure, nonfinite outputs, wrong route/policy metadata, GPU/TF32 mismatch, dense materialization, missing SVD metadata, or malformed artifacts. |
| Explanatory diagnostics | Runtime, memory, ESS, residuals, factor/core diagnostics, streaming deltas. |
| Not concluded | No nonlinear validity, no promotion, no statistical superiority, no HMC readiness. |
| Artifact | P02 run artifacts and this result. |

## Harness Repair

P02 required a dedicated SVD-Nystrom LGSSM exact-reference harness because the
existing LGSSM gate was low-rank-specific. The bounded harness adds:

- `docs/benchmarks/benchmark_svd_nystrom_lgssm_kalman_gate.py`
- `tests/test_svd_nystrom_lgssm_kalman_gate.py`

The harness reuses the existing LGSSM fixture, Kalman reference, and LEDH
callback machinery, but runs the locked SVD-Nystrom route. Local checks passed:

- `3 passed` before the diagnostic flag repair;
- `4 passed` after adding `--no-nystrom-diagnostics`.

Because the harness is newly added, it remains a P02 artifact requiring review
before any future repair/promotion rerun treats it as mature infrastructure.

## Runs

| Run | Device/precision | Artifact | Status | Interpretation |
| --- | --- | --- | --- | --- |
| CPU shape smoke | CPU hidden, TF32 disabled, `N=16`, `T=1`, `rank=4` | `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-cpu-shape-lgssm-small-2026-06-25.json` | PASS | Harness command shape and artifact schema are valid. |
| Trusted GPU default target | GPU1, TF32 enabled, XLA enabled, `N=1024`, `T=12`, locked `rank=32` policy | `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-lgssm-reference-small-gpu1-2026-06-25.json` | FAIL | Hard deterministic veto: nonfinite route output, factors, and particles. |
| CPU diagnostic | CPU hidden, TF32 disabled, same `N/T/rank` policy | `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-lgssm-reference-small-cpu-diagnostic-2026-06-25.json` | PASS | Same policy is finite and within exact-reference thresholds off GPU/TF32. |
| GPU no-TF32 diagnostic | GPU1, TF32 disabled, same `N/T/rank` policy | `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-lgssm-reference-small-gpu1-tf32disabled-2026-06-25.json` | PASS | GPU path is finite when TF32 is disabled. |
| GPU TF32 no-XLA diagnostic | GPU1, TF32 enabled, XLA disabled | log only | FAIL before artifact | CUDA solver failure in diagnostic eig/SVD path. |
| GPU TF32 no-XLA no-diagnostics diagnostic | GPU1, TF32 enabled, XLA disabled, Nystrom diagnostics disabled | log only | FAIL before artifact | CUDA `gesvd` failure in actual SVD core, not only spectrum diagnostics. |
| Repaired P02 rerun | GPU0 because GPU1 saturated, TF32 enabled, XLA enabled, `N=1024`, `T=12`, locked `rank=32` policy | `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-repaired-lgssm-reference-small-gpu0-2026-06-25.json` | PASS | Bounded factor/core precision repair makes the default-target P02 exact-reference gate finite and within thresholds. |

## Key Diagnostics

| Diagnostic | GPU TF32 | GPU no-TF32 | CPU no-TF32 |
| --- | ---: | ---: | ---: |
| Status | FAIL | PASS | PASS |
| Finite route output | false | true | true |
| Finite factors | false | true | true |
| Finite particles | false | true | true |
| Mean RMSE | NaN | `0.12203076773031596` | `0.12211573668063272` |
| Variance RMSE | NaN | `0.24273017634681113` | `0.24272995334353728` |
| Loglik abs delta | NaN | `1.7836990356445312` | `1.7883644104003906` |
| Row residual | NaN | `0.0035163164138793945` | `0.0042567127384245396` |
| Column residual | NaN | `4.76837158203125e-07` | `0.005672592669725418` |

## Repaired Rerun Diagnostics

The repaired P02 rerun preserves the original failed P02 evidence and writes a
fresh artifact:
`docs/benchmarks/svd-nystrom-nohmc-promotion-p02-repaired-lgssm-reference-small-gpu0-2026-06-25.json`.

| Diagnostic | Repaired GPU TF32 rerun |
| --- | ---: |
| Status | PASS |
| Hard vetoes | `[]` |
| TF32 recorded | `True` |
| Finite route output | true |
| Finite factors | true |
| Finite particles | true |
| Transport matrix materialized | false |
| Mean RMSE | `0.12198596717117477` |
| Variance RMSE | `0.2425361188055973` |
| Loglik abs delta | `1.7873344421386719` |
| Row residual | `0.0034079551696777344` |
| Column residual | `0.0034064650535583496` |

Trusted GPU preflight selected physical GPU1 as requested. A later `nvidia-smi`
check showed GPU1 memory held by an unrelated process:
`cross_country_multi_asset_macro_mixed_frequency_phase5l_single_call_retained_archive.py`.
No P02 benchmark process was left running.

For the repaired rerun, trusted GPU preflight found GPU1 saturated, so GPU0 was
used under the owner rule "GPU1 if available, otherwise GPU0."

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Original run stopped at P02 blocker | FAIL for default GPU/TF32 target | HARD VETO: GPU TF32 SVD core produced nonfinite/failing route | Needed a reviewed numerical repair to make SVD core robust under TF32 | P02A repair subplan and diagnostics were executed | No nonlinear validity, no promotion, no default switch, no statistical superiority, no HMC readiness |
| Repaired P02 rerun passes pending review | PASS for repaired GPU/TF32 target | No hard vetoes in repaired rerun | Material repair still needs read-only review before P03 execution | Run bounded Claude review of P02A/P02 repair artifacts; if converged, refresh P03 status and launch P03 | No nonlinear validity, no promotion, no default switch, no statistical superiority, no HMC readiness |

## Inference Status

| Row | Status |
| --- | --- |
| Hard veto screen | PASS for repaired trusted GPU/TF32 rerun; original failed artifact preserved |
| Statistically supported ranking | NO |
| Descriptive-only differences | CPU, GPU-no-TF32, and one-row repaired metric magnitudes are diagnostic/descriptive only |
| Default-readiness | NO |
| Next evidence needed | Read-only material repair review, then P03 actual-SIR stress if review converges |

## Handoff

`P02_PASS_REPAIRED_PENDING_REVIEW_TO_P03_ACTUAL_SIR_STRESS`

P03 must not run until material repair review converges. After review
convergence, the supervisor must record the explicit post-review handoff token
`P02_REPAIR_REVIEW_AGREE_PASS_TO_P03_ACTUAL_SIR_STRESS` before executing P03.
Candidate promotion is still blocked by downstream phases and final review.
