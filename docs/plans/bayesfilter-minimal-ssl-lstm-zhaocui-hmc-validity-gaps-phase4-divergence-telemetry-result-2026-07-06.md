# Phase 4 Result: Native Divergence Telemetry Inspection

Date: 2026-07-06

Status: `VALID_ARTIFACT_NATIVE_DIVERGENCE_NOT_EXPOSED_CONTINUE_TO_PHASE5`

## Phase Objective

Determine whether the current TensorFlow Probability HMC result objects expose a
native boolean divergence field for the minimal `zhaocui_fixed` HMC path, without
substituting acceptance, log-acceptance, target-log-probability, energy, R-hat,
or ESS proxies for native divergence telemetry.

## Skeptical Pre-Run Audit

Audit result: `PASS_WITH_BOUNDARIES`.

- The command answers only native divergence telemetry availability.
- Phase 3 remained the baseline: valid artifact, no continuation vetoes, and
  promotion veto `native_divergence_telemetry_not_exposed`.
- Acceptance, log-acceptance, and target-log-probability were classified as
  health context only.
- Missing native telemetry was predeclared as unavailability, not zero
  divergences.
- The run was CPU-hidden and short; no trusted GPU/XLA, long HMC, public API,
  default-policy, model-file, or source-faithful boundary was crossed.

## Runtime Command

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_divergence_telemetry_2026_07_06.py --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase4_divergence_telemetry_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase4_divergence_telemetry_cpu_hidden_2026-07-06.md > docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase4_divergence_telemetry_cpu_hidden_2026-07-06.log 2>&1
```

## Artifacts

| Artifact | Path |
| --- | --- |
| Harness | `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_divergence_telemetry_2026_07_06.py` |
| Tests | `tests/test_minimal_ssl_lstm_zhaocui_hmc_divergence_telemetry.py` |
| JSON result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase4_divergence_telemetry_cpu_hidden_2026-07-06.json` |
| Markdown result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase4_divergence_telemetry_cpu_hidden_2026-07-06.md` |
| Quiet log | `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase4_divergence_telemetry_cpu_hidden_2026-07-06.log` |
| Refreshed next subplan | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase5-tuning-mass-ladder-subplan-2026-07-06.md` |

## Checks

| Check | Status |
| --- | --- |
| `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_divergence_telemetry_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_hmc_divergence_telemetry.py` | passed |
| `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 python -m pytest -q -p no:cacheprovider tests/test_minimal_ssl_lstm_zhaocui_hmc_divergence_telemetry.py` | passed: `6 passed` |
| Phase 4 artifact command | passed with exit code `0` |
| `python -m json.tool docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase4_divergence_telemetry_cpu_hidden_2026-07-06.json` | passed |

## Runtime Artifact Summary

| Diagnostic | Result | Role |
| --- | --- | --- |
| Artifact status | `passed` | primary artifact criterion |
| Hard vetoes | `[]` | continuation/veto evidence |
| Phase 3 preconditions | `true` | entry condition |
| Native divergence telemetry status | `native_divergence_not_exposed_by_kernel` | primary inspection result |
| BayesFilter `native_divergence_status` | `not_exposed_by_kernel` | extractor result |
| BayesFilter `divergence_count` | `None` | unavailability, not zero divergences |
| TFP raw field search | no accepted boolean divergence fields | field-tree evidence |
| Trace keys | `is_accepted`, `log_accept_ratio`, `target_log_prob` | health context only |
| Acceptance rate | `1.0` | explanatory only |
| Log-accept finite count | `8`; nonfinite count `0` | explanatory only |
| Target-log-prob finite | `true` | explanatory only |
| Sample shape | `[4, 2, 24]` | tiny CPU-hidden inspection |
| CPU-hidden status | `CUDA_VISIBLE_DEVICES=-1` | runtime boundary |

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | `PASSED_NO_HARD_VETO` |
| Native divergence evidence | `NOT_AVAILABLE`; TFP HMC kernel results did not expose a native boolean divergence field reachable by the BayesFilter extractor. |
| Zero-divergence claim | `NOT_CLAIMED`; missing telemetry is not zero divergences. |
| Statistically supported ranking | `NOT_APPLICABLE` |
| Descriptive-only diagnostics | Acceptance, log-acceptance, target-log-probability, and runtime are health context only. |
| HMC convergence | `NOT_ESTABLISHED` |
| Posterior correctness | `NOT_ESTABLISHED` |
| Default-readiness | `NOT_CHECKED` |
| Next evidence needed | Phase 5 tuning/mass diagnostics with this telemetry limitation carried forward. |

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `VALID_ARTIFACT_CONTINUE_TO_PHASE5` |
| Primary criterion status | `PASSED`: inspected TFP result tree, native boolean field search, and BayesFilter extractor output were recorded. |
| Veto diagnostic status | No hard vetoes. |
| Main uncertainty | This phase only establishes telemetry availability status; it does not evaluate whether a tuned kernel improves Phase 3 R-hat/ESS. |
| Next justified action | Execute Phase 5 tuning/mass diagnostics using the repaired `hmc_kernel_tuning.py` path, with Phase 3 as fixed-kernel comparator and Phase 4 missing telemetry preserved as a limitation. |
| What is not being concluded | No zero-divergence, posterior correctness, HMC convergence, ranking/superiority, default-readiness, production-readiness, source-faithful parity, public API/package readiness, or LEDH claim. |

## Post-Run Red-Team Note

| Field | Note |
| --- | --- |
| Strongest alternative explanation | TFP’s current HMC kernel may simply not publish divergence flags for this route; the absence of the field does not imply no numerical pathologies. |
| Result that would overturn this phase decision | A reviewed trace route exposing a native boolean divergence field under the same HMC kernel/result structure. |
| Weakest part of evidence | The raw TFP tree inspection is structural, while the BayesFilter run remains a tiny CPU-hidden diagnostic; neither is posterior evidence. |

## Boundary Classification

| Boundary | Status |
| --- | --- |
| CPU-hidden short telemetry inspection | `EXECUTED` |
| Trusted GPU/XLA runtime | `NOT_RUN` |
| Long HMC/tuning run | `NOT_RUN` |
| Public API/default-policy change | `NOT_INTRODUCED` |
| Model-file edit | `NOT_INTRODUCED` |
| Source-faithful Zhao-Cui parity claim | `NOT_CLAIMED` |
| Zero-divergence claim | `NOT_CLAIMED` |
| HMC convergence/posterior correctness claim | `NOT_CLAIMED` |
| Ranking/superiority claim | `NOT_CLAIMED` |

## Handoff

Proceed to Phase 5:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase5-tuning-mass-ladder-subplan-2026-07-06.md`

Phase 5 must not reinterpret missing native divergence telemetry as zero
divergences. It should address the Phase 3 sampler-setting promotion vetoes
through a predeclared tuning/mass diagnostic and should rank no viable candidate
without uncertainty evidence.
