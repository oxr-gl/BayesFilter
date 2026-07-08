# Phase 6 Result: Windowed Acceptance Telemetry Repair

Date: 2026-07-06

Status: `VALID_ARTIFACT_ACCEPTANCE_TELEMETRY_REPAIRED_TIMEOUT_HANDOFF`

## Phase Objective

Localize and repair the Phase 5 staged tuning blocker
`windowed_stage_acceptance_telemetry_invalid_or_default` before any dimensional
lift, source-faithful track, or comparator/readiness planning.

## Skeptical Pre-Run Audit

Audit result: `PASS_WITH_BOUNDARIES`.

- The initial blocker was rechecked against the Phase 5 public tuning artifact
  and focused windowed-mass tests.
- Constant acceptance traces were not automatically accepted as real telemetry;
  they were allowed only when fixed-size chunk-runner runtime decision counts
  supported every acceptance decision.
- The repair preserved hard vetoes for missing, malformed, nonfinite,
  fixture/synthetic, nonruntime, or unsupported default-like acceptance traces.
- The rerun stayed CPU-hidden, bounded, non-XLA, and diagnostic.
- Native divergence telemetry unavailability from Phase 4 was preserved as
  unavailability, not zero divergences.
- No posterior correctness, convergence, ranking, readiness, source-faithful
  parity, dimensional generality, or LEDH claim was allowed.

## Repair Summary

The original hard veto was localized to acceptance telemetry policy rather than
to missing HMC execution. A real fixed-size chunk-runner path can produce a
constant all-accepted trace in a short smoke run. The repair added runtime
decision-count provenance so that such a trace is accepted only when the trace
is finite, aligned, binary, supported by the TFP HMC chunk runner, and its
accepted-decision count exactly matches the trace.

The windowed-mass stage now carries these provenance fields:

- `constant_trace`
- `runtime_decision_count_supported`
- `accepted_decision_count`
- `acceptance_decision_count`
- `policy_filled_or_default`

Unsupported constant/default-like traces still hard-veto with
`windowed_stage_acceptance_telemetry_invalid_or_default`.

## Runtime Command

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_cpu_hidden_2026-07-06.md --tuning-output-dir docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_public_artifacts_2026-07-06
```

The final rerun reused the Phase 5 harness with Phase 6 output paths. The
harness Markdown title still says "Phase 5" because the executable is the
staged tuning harness; this Phase 6 result record is the controlling close
record for the acceptance-telemetry repair.

## Artifacts

| Artifact | Path |
| --- | --- |
| Patched implementation | `bayesfilter/inference/hmc_kernel_tuning.py` |
| Focused windowed-mass tests | `tests/test_hmc_kernel_tuning_windowed_mass.py` |
| Phase 5 harness manifest fix | `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py` |
| Phase 5 harness tests | `tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py` |
| Final JSON result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_cpu_hidden_2026-07-06.json` |
| Final Markdown result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_cpu_hidden_2026-07-06.md` |
| Final public tuning result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_public_artifacts_2026-07-06/hmc_kernel_tuning_result.json` |
| Final public progress result | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_public_artifacts_2026-07-06/hmc_kernel_tuning_progress.json` |
| Private event summary file | `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_public_artifacts_2026-07-06/private_diagnostics/hmc_tuning_events.jsonl` |
| Next subplan | `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-frozen-step-trajectory-timeout-handoff-subplan-2026-07-06.md` |

## Checks

| Check | Status |
| --- | --- |
| `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 python -m py_compile bayesfilter/inference/hmc_kernel_tuning.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py tests/test_hmc_kernel_tuning_windowed_mass.py tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py` | passed |
| `PYTHONPYCACHEPREFIX=/tmp/bayesfilter-pycache CUDA_VISIBLE_DEVICES=-1 python -m pytest -q -p no:cacheprovider tests/test_hmc_kernel_tuning_windowed_mass.py tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py` | passed: `29 passed, 1 skipped` |
| Final Phase 6 rerun command | passed wrapper execution and wrote structured artifacts |
| `python -m json.tool docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase6_acceptance_telemetry_repair_final_cpu_hidden_2026-07-06.json` | passed |
| Private diagnostic event count | `15` lines |

## Runtime Artifact Summary

| Diagnostic | Result | Role |
| --- | --- | --- |
| Wrapper artifact status | `passed` | valid structured artifact |
| Public tuner status | `hard_veto` | tuning blocker evidence |
| Public tuner diagnostic role | `hard_veto` | blocker evidence |
| Public tuner hard veto | `phase6_public_timeout_soft_deadline` | next repair target |
| Original acceptance hard veto | absent in final rerun | repaired/localized |
| Windowed-mass stage | `passed`; hard vetoes `[]` | repaired stage |
| Fixed-mass step stage | `passed`; hard vetoes `[]` | handoff stage |
| Frozen-step trajectory stage | `hard_veto`; hard vetoes `["phase6_public_timeout_soft_deadline"]` | timeout blocker |
| Final kernel hash | `None` | no final handoff candidate |
| Final kernel payload | unavailable | no final handoff candidate |
| Runtime | about `44.3` seconds | explanatory |
| Public timeout budget | `90.0` seconds | runtime boundary |
| Public timeout closeout reason | `phase6_public_timeout_soft_deadline_before_next_candidate` | repair trigger |
| Candidate count in private summary | `4` | explanatory only |
| Completed candidate count in private summary | `3` | explanatory only |
| Candidate pass count in private summary | `2` | explanatory only |
| Selected pair exists in private summary | `true` | resume/handoff signal only |
| Native divergence status carried forward | `native_divergence_not_exposed_by_kernel` | limitation, not zero divergences |
| CPU-hidden status | `CUDA_VISIBLE_DEVICES=-1` | runtime boundary |

## Inference Status

| Field | Status |
| --- | --- |
| Artifact validity | `PASSED` |
| Original acceptance-telemetry hard veto | `REPAIRED`: final rerun passes the windowed-mass stage without `windowed_stage_acceptance_telemetry_invalid_or_default`. |
| Public tuning hard-veto screen | `FAILED`: `phase6_public_timeout_soft_deadline` in the frozen-step trajectory stage. |
| Tuned-kernel handoff candidate | `NOT_AVAILABLE`: `final_kernel_hash` is `None`. |
| Native divergence evidence | `NOT_AVAILABLE`; Phase 4 limitation persists. |
| Zero-divergence claim | `NOT_CLAIMED`; missing native divergence telemetry is not zero divergences. |
| Statistically supported ranking | `NOT_APPLICABLE` |
| Descriptive-only diagnostics | Stage statuses, acceptance, candidate counts, repair triggers, and runtime are diagnostic only. |
| HMC convergence | `NOT_ESTABLISHED` |
| Posterior correctness | `NOT_ESTABLISHED` |
| Default-readiness | `NOT_CHECKED` |
| Next evidence needed | Reviewed Phase 7 timeout/trajectory handoff repair before dimensional lift, source-faithful work, or comparator/readiness planning. |

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `VALID_ARTIFACT_ACCEPTANCE_TELEMETRY_REPAIRED_BLOCKED_BY_TIMEOUT` |
| Primary criterion status | `PASSED`: the acceptance-telemetry blocker was localized and repaired with focused tests and a final structured rerun. |
| Veto diagnostic status | Public tuner hard veto `phase6_public_timeout_soft_deadline` blocks the next HMC handoff step. |
| Main uncertainty | The frozen-step trajectory stage was not completed under the current public timeout budget, so no final frozen kernel is available. |
| Next justified action | Execute a reviewed Phase 7 timeout/trajectory handoff plan: either enlarge the public timeout, split/resume from the selected private handoff, or reduce candidate scope under explicit evidence boundaries. |
| What is not being concluded | No zero-divergence, posterior correctness, broad HMC convergence, tuned-kernel superiority, ranking, default readiness, production readiness, public API/package readiness, source-faithful Zhao-Cui parity, dimensional generality, or LEDH claim. |

## Post-Run Red-Team Note

| Field | Note |
| --- | --- |
| Strongest alternative explanation | The new timeout may be a budget/scheduling artifact rather than evidence that the frozen-step trajectory candidate is bad. |
| Result that would overturn this phase decision | A reviewed rerun or split/resume route that completes frozen-step trajectory screening, writes a valid public tuning artifact, and either produces a final kernel handoff or records a different hard veto. |
| Weakest part of evidence | The final rerun is CPU-hidden and bounded; private diagnostic candidate counts are useful for handoff design but are not public HMC validity evidence. |

## Boundary Classification

| Boundary | Status |
| --- | --- |
| CPU-hidden bounded diagnostic | `EXECUTED` |
| Trusted GPU/XLA runtime | `NOT_RUN` |
| Long HMC/convergence run | `NOT_RUN` |
| Public API/default-policy change | `NOT_INTRODUCED` |
| Model-file edit | `NOT_INTRODUCED` |
| Source-faithful Zhao-Cui parity claim | `NOT_CLAIMED` |
| Zero-divergence claim | `NOT_CLAIMED` |
| HMC convergence/posterior correctness claim | `NOT_CLAIMED` |
| Ranking/superiority claim | `NOT_CLAIMED` |

## Review Note

Claude review remains unavailable for this lane because external review would
transmit private repository context. A visible Codex substitute review was used
for the Phase 7 subplan boundary audit:

- `docs/reviews/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-timeout-handoff-codex-substitute-review-2026-07-06.md`

Residual risk: no independent external reviewer has checked the Phase 6 repair,
so Phase 7 must keep the same hard evidence boundaries and focused local
checks.

## Handoff

Proceed to the new timeout/trajectory handoff subplan:

- `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase7-frozen-step-trajectory-timeout-handoff-subplan-2026-07-06.md`

Do not proceed to dimensional lift, source-faithful anchor work, comparator
readiness, or readiness/default claims until the frozen-step trajectory timeout
blocker is either repaired or explicitly recorded as the active blocker.
