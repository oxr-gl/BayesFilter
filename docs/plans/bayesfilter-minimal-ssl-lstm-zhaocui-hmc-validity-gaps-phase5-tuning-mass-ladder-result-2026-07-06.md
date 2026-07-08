# Phase 5 Result: HMC Tuning And Mass-Matrix Diagnostic

Date: 2026-07-06

Status: `VALID_ARTIFACT_STRUCTURED_TUNING_HARD_VETO_BLOCKS_PHASE6`

## Phase Objective

Run the smallest CPU-hidden diagnostic that exercises BayesFilter's staged HMC
kernel tuning machinery on the minimal `zhaocui_fixed` target, using Phase 3
fixed-kernel HMC as comparator and Phase 4 native-divergence unavailability as
a preserved limitation.

## Skeptical Pre-Run Audit

Audit result: `PASS_WITH_BOUNDARIES`.

- Phase 3 and Phase 4 preconditions were checked before tuning.
- The command used the public BayesFilter-owned tuning entry point,
  `tune_hmc_kernel`, not a bespoke sampler.
- The run was CPU-hidden, bounded, and non-XLA.
- A public tuner hard veto was predeclared as blocker evidence, not wrapper
  invalidity.
- Missing native divergence telemetry was carried forward as unavailability,
  not zero divergences.
- No ranking, posterior correctness, broad convergence, readiness,
  source-faithful parity, or production claim was allowed.

## Runtime Command

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase5_tuning_mass_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase5_tuning_mass_cpu_hidden_2026-07-06.md --tuning-output-dir docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase5_tuning_public_artifacts_2026-07-06 > docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase5_tuning_mass_cpu_hidden_2026-07-06.log 2>&1
```

## Artifacts

| Artifact | Path |
| --- | --- |
| Harness | `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py` |
| Tests | `tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py` |
| JSON result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase5_tuning_mass_cpu_hidden_2026-07-06.json` |
| Markdown result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase5_tuning_mass_cpu_hidden_2026-07-06.md` |
| Public tuning artifact | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase5_tuning_public_artifacts_2026-07-06/hmc_kernel_tuning_result.json` |
| Public progress artifact | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase5_tuning_public_artifacts_2026-07-06/hmc_kernel_tuning_progress.json` |
| Quiet log | `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase5_tuning_mass_cpu_hidden_2026-07-06.log` |
| Refreshed next subplan | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase6-dimensional-lift-subplan-2026-07-06.md` |

## Checks

| Check | Status |
| --- | --- |
| `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py` | passed |
| `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 python -m pytest -q -p no:cacheprovider tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py` | passed: `7 passed` |
| Phase 5 artifact command | passed with exit code `0` after wrapper classification repair |
| `python -m json.tool docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase5_tuning_mass_cpu_hidden_2026-07-06.json` | passed |

## Runtime Artifact Summary

| Diagnostic | Result | Role |
| --- | --- | --- |
| Wrapper artifact status | `passed` | valid structured artifact |
| Phase decision | `structured_tuning_hard_veto_blocks_phase6` | blocker evidence |
| Wrapper hard vetoes | `[]` | wrapper validity |
| Public tuner final status | `hard_veto` | tuning blocker |
| Public tuner diagnostic role | `hard_veto` | tuning blocker |
| Public tuner hard veto | `windowed_stage_acceptance_telemetry_invalid_or_default` | continuation veto for dimensional lift |
| Final kernel hash | `None` | no handoff candidate |
| Final kernel payload | not available | no handoff candidate |
| Attempt count | `1` | smoke diagnostic |
| Windowed mass stage | `hard_veto` | blocker localization |
| Fixed-mass step stage | not reached | blocked by windowed mass |
| Frozen-step trajectory stage | not reached | blocked by windowed mass |
| Native divergence status carried forward | `native_divergence_not_exposed_by_kernel` | limitation, not zero divergences |
| Runtime | about `11.1` seconds | explanatory |
| CPU-hidden status | `CUDA_VISIBLE_DEVICES=-1` | runtime boundary |

## Inference Status

| Field | Status |
| --- | --- |
| Artifact validity | `PASSED` |
| Public tuning hard-veto screen | `FAILED`: `windowed_stage_acceptance_telemetry_invalid_or_default` |
| Tuned-kernel handoff candidate | `NOT_AVAILABLE` |
| Native divergence evidence | `NOT_AVAILABLE`; Phase 4 limitation persists. |
| Zero-divergence claim | `NOT_CLAIMED` |
| Statistically supported ranking | `NOT_APPLICABLE` |
| Descriptive-only diagnostics | Stage statuses, acceptance/progress summaries, repair triggers, and runtime are diagnostic only. |
| HMC convergence | `NOT_ESTABLISHED` |
| Posterior correctness | `NOT_ESTABLISHED` |
| Default-readiness | `NOT_CHECKED` |
| Next evidence needed | Repair or localize the windowed-mass acceptance telemetry hard veto before any dimensional lift. |

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `VALID_ARTIFACT_BLOCK_PHASE6_DIMENSIONAL_LIFT` |
| Primary criterion status | `PASSED`: a structured public tuning artifact and progress artifact were produced. |
| Veto diagnostic status | Public tuner hard veto `windowed_stage_acceptance_telemetry_invalid_or_default` blocks Phase 6 dimensional lift. |
| Main uncertainty | The hard veto may reflect acceptance telemetry extraction/default-fill policy rather than a target-level impossibility. |
| Next justified action | Replace the dimensional-lift plan with a focused Phase 6 repair/localization subplan for windowed-mass acceptance telemetry. |
| What is not being concluded | No zero-divergence, posterior correctness, broad convergence, tuned-kernel superiority, default readiness, production readiness, public API/package readiness, source-faithful parity, or LEDH claim. |

## Post-Run Red-Team Note

| Field | Note |
| --- | --- |
| Strongest alternative explanation | The staged tuner may be using a trace route where acceptance telemetry is default-like even though HMC execution occurred; this is an implementation/telemetry blocker, not evidence against the model target. |
| Result that would overturn this phase decision | A reviewed rerun where windowed-mass capture records non-default runtime acceptance telemetry and reaches fixed-mass step tuning without hard veto. |
| Weakest part of evidence | The public artifact intentionally hides HMC mechanics, so the next phase must localize telemetry through focused internal tests or a narrow private diagnostic. |

## Boundary Classification

| Boundary | Status |
| --- | --- |
| CPU-hidden bounded tuning diagnostic | `EXECUTED` |
| Trusted GPU/XLA runtime | `NOT_RUN` |
| Long HMC | `NOT_RUN` |
| Public API/default-policy change | `NOT_INTRODUCED` |
| Model-file edit | `NOT_INTRODUCED` |
| Source-faithful Zhao-Cui parity claim | `NOT_CLAIMED` |
| Zero-divergence claim | `NOT_CLAIMED` |
| HMC convergence/posterior correctness claim | `NOT_CLAIMED` |
| Ranking/superiority claim | `NOT_CLAIMED` |

## Handoff

Proceed to the refreshed Phase 6 repair/localization subplan:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase6-dimensional-lift-subplan-2026-07-06.md`

Do not proceed to dimensional lift until the windowed-mass acceptance telemetry
hard veto is repaired or a reviewed alternative diagnostic route is approved.
