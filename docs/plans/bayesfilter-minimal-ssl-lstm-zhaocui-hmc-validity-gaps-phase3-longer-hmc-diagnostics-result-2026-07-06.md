# Phase 3 Result: Longer HMC Diagnostics

Date: 2026-07-06

Status: `VALID_ARTIFACT_PROMOTION_SCREEN_FAILED_CONTINUE_TO_PHASE4`

## Phase Objective

Run the reviewed modest trusted GPU/XLA longer HMC diagnostic on the minimal
scalar-dimension `zhaocui_fixed` target, adding sampled-state target/reference
checks and minimal R-hat/ESS screening that the previous hard-veto ladder did
not compute.

## Review And Approval

- Claude review gate was attempted through the narrow review wrapper, but the
  approval reviewer rejected the external review because it would transfer
  private repository context to Claude.
- No workaround was attempted.
- A fresh visible Codex substitute review of the compact Phase 3 bundle returned
  `VERDICT: AGREE`.
- Blocking findings: none.
- Residual review risk: substitute review is weaker than full Claude review.
- User approval for the longer-HMC runtime boundary was recorded on
  2026-07-06.

## Skeptical Pre-Run Audit

Audit result: `PASS_WITH_BOUNDARIES`.

- Baseline risk was controlled by using the Phase 2 oracle artifact and the
  predecessor GPU/XLA mechanics artifact as context.
- Proxy-metric risk was controlled by treating R-hat/ESS as a minimal
  sampler-setting promotion screen, not proof of broad convergence.
- Native divergence risk was controlled by treating missing telemetry as a
  promotion veto, not zero divergences.
- Artifact mismatch risk was controlled by predeclaring JSON/Markdown/log paths
  and validating JSON after runtime.
- Environment mismatch risk was exposed by an initial non-trusted run that saw
  no GPU; per GPU policy, the exact command was rerun in a trusted context.

## Runtime Command

The trusted successful run used the exact reviewed command with required quiet
log capture:

```bash
CUDA_VISIBLE_DEVICES=0 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_validity_phase3_2026_07_06.py --trusted-gpu-xla-approval --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.md > docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase3_longer_gpu_xla_2026-07-06.log 2>&1
```

An initial visible non-trusted launch produced `gpu_device_not_visible`; that
was treated as sandbox/environment evidence only and superseded by the trusted
rerun above.

## Artifacts

| Artifact | Path |
| --- | --- |
| Harness | `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_validity_phase3_2026_07_06.py` |
| Tests | `tests/test_minimal_ssl_lstm_zhaocui_hmc_validity_phase3.py` |
| Review bundle | `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-review-bundle-2026-07-06.md` |
| JSON result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.json` |
| Markdown result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.md` |
| Quiet log | `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase3_longer_gpu_xla_2026-07-06.log` |
| Next subplan | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase4-divergence-telemetry-subplan-2026-07-06.md` |

## Checks

| Check | Status |
| --- | --- |
| `python -m py_compile docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_validity_phase3_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_hmc_validity_phase3.py` | passed |
| `CUDA_VISIBLE_DEVICES=-1 python -m pytest -q tests/test_minimal_ssl_lstm_zhaocui_hmc_validity_phase3.py` | passed: `9 passed` |
| Phase 2 JSON status check | passed: `status=passed`, hard vetoes `[]` |
| Substitute review | passed: `VERDICT: AGREE` |
| Trusted runtime command | completed with exit code `0` |
| JSON validation | passed |
| GPU/XLA provenance | passed: GPU `/physical_device:GPU:0`, `use_xla=True`, `jit_compile=True` |

## Runtime Artifact Summary

| Diagnostic | Result | Role |
| --- | --- | --- |
| Artifact status | `passed` | primary artifact criterion |
| Promotion screen | `failed` | minimal sampler-setting screen |
| Continuation vetoes | `[]` | continuation veto evidence |
| Promotion vetoes | `split_rhat_threshold_failed`, `ess_threshold_failed`, `native_divergence_telemetry_not_exposed` | sampler-setting promotion vetoes |
| Sample shape | `[64, 4, 24]` | required diagnostic |
| Samples all finite | `true` | continuation veto screen |
| Sampled-state reference check | `passed` | target/reference screen, not full posterior proof |
| Reference max absolute error | `4.440892098500626e-16` | reference diagnostic |
| Reference max relative error | `3.210361025909055e-16` | reference diagnostic |
| Split R-hat finite coordinates | `24 / 24` | promotion diagnostic |
| Split R-hat max | `2083851.3177999416` | promotion veto |
| Cross-chain ESS finite coordinates | `24 / 24` | promotion diagnostic |
| Cross-chain ESS min | `4.000003545362901` | promotion veto |
| Native divergence status | `not_exposed_by_kernel` | promotion veto, not zero divergences |
| Acceptance rate | `1.0` | explanatory only |
| Runtime | `32.184033575002104` seconds artifact runtime, `32.23408003899385` seconds wall time | explanatory |

## Inference Status

| Field | Status |
| --- | --- |
| Artifact validity | `PASSED` |
| Continuation veto screen | `PASSED_NO_CONTINUATION_VETO` |
| Minimal sampler promotion screen | `FAILED` |
| Hard veto evidence | No nonfinite samples, no runtime exception, no provenance failure in the trusted rerun. |
| Statistically supported ranking | `NOT_CLAIMED` |
| Descriptive-only diagnostics | Acceptance, runtime, trace summaries, and sample summaries are descriptive only. |
| Native divergence evidence | `NOT_AVAILABLE`; kernel did not expose native divergence telemetry, so this is not zero divergences. |
| HMC convergence | `NOT_ESTABLISHED` |
| Posterior correctness | `NOT_ESTABLISHED`; sampled-state value agreement passed but is not full posterior evidence. |
| Default-readiness | `NOT_CHECKED` |
| Production-readiness | `NOT_CHECKED` |
| Next evidence needed | Native divergence telemetry inspection, then tuning/mass diagnostics before any broader convergence or readiness claim. |

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `VALID_ARTIFACT_CONTINUE_TO_PHASE4` |
| Primary criterion status | `PASSED`: valid trusted GPU/XLA artifact with required diagnostics. |
| Veto diagnostic status | Promotion vetoes fired for R-hat, ESS, and unavailable native divergence telemetry. |
| Main uncertainty | The fixed-kernel setting produced poor chain-mixing diagnostics; this rejects the setting, not the target or research direction. |
| Next justified action | Execute Phase 4 native divergence telemetry inspection, then use Phase 5 tuning/mass diagnostics to address sampler-setting failure. |
| What is not being concluded | No full posterior correctness, broad HMC convergence, ranking/superiority, default readiness, production readiness, source-faithful parity, public API/package readiness, or LEDH result. |

## Post-Run Red-Team Note

| Field | Note |
| --- | --- |
| Strongest alternative explanation | The R-hat/ESS failure may be caused by a conservative fixed step size and no adaptation/mass tuning, not by target invalidity. |
| Result that would overturn this phase decision | Reproduced nonfinite sample/target, invalid JSON, GPU/XLA provenance failure, sampled-state target/reference mismatch, or exposed positive native divergence under the reviewed settings. |
| Weakest part of evidence | Sampled-state reference agreement is not full posterior correctness, and native divergence telemetry remains unavailable. |

## Boundary Classification

| Boundary | Status |
| --- | --- |
| Trusted GPU/XLA longer HMC runtime | `EXECUTED_WITH_APPROVAL` |
| Long diagnostics beyond reviewed command | `NOT_RUN` |
| Public API/default-policy change | `NOT_INTRODUCED` |
| Model-file edit | `NOT_INTRODUCED` |
| Source-faithful Zhao-Cui parity claim | `NOT_CLAIMED` |
| HMC convergence/posterior correctness claim | `NOT_CLAIMED` |
| Ranking/superiority claim | `NOT_CLAIMED` |

## Handoff

Proceed to Phase 4:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase4-divergence-telemetry-subplan-2026-07-06.md`

Phase 4 must not treat acceptance, log-acceptance, target-log-probability, or
missing native telemetry as divergence evidence. If native telemetry remains
unavailable, it should record that limitation and hand off to Phase 5
tuning/mass diagnostics without claiming zero divergences.
