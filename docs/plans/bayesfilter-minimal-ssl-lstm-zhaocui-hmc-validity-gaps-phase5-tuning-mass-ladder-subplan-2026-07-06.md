# Phase 5 Subplan: HMC Tuning And Mass-Matrix Ladder Diagnostic

Date: 2026-07-06

Status: `READY_FOR_REVIEW`

## Phase Objective

Run the smallest CPU-hidden diagnostic that exercises BayesFilter's staged HMC
kernel tuning machinery on the minimal `zhaocui_fixed` target, using Phase 3
fixed-kernel HMC as the comparator and Phase 4 native-divergence unavailability
as a preserved limitation.

This phase may nominate a tuned-kernel path for later validation, but it must
not claim posterior correctness, HMC convergence, sampler superiority,
default-readiness, production-readiness, zero divergences, or source-faithful
Zhao-Cui parity.

## Entry Conditions Inherited From Previous Phase

- Phase 2 scalar oracle artifact exists and passed.
- Phase 3 longer HMC artifact exists, passed artifact-validity checks, and
  failed only the sampler-setting promotion screen:
  `split_rhat_threshold_failed`, `ess_threshold_failed`, and
  `native_divergence_telemetry_not_exposed`.
- Phase 4 native divergence telemetry artifact exists and passed with
  `native_divergence_not_exposed_by_kernel`; this remains telemetry
  unavailability, not zero divergences.
- Focused `hmc_kernel_tuning.py` tests pass after the user's repair:
  `185 passed, 1 skipped` for `tests/test_hmc_kernel_tuning_*.py`, plus
  related HMC tuning-policy/budget checks.

## Required Artifacts

- Harness:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py`
- Tests:
  `tests/test_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5.py`
- JSON artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase5_tuning_mass_cpu_hidden_2026-07-06.json`
- Markdown artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase5_tuning_mass_cpu_hidden_2026-07-06.md`
- Quiet log:
  `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase5_tuning_mass_cpu_hidden_2026-07-06.log`
- Phase 5 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase5-tuning-mass-ladder-result-2026-07-06.md`
- Draft/refreshed Phase 6 dimensional-lift subplan.

## Required Checks, Tests, Reviews

Before execution:

- Skeptical plan audit: confirm the command answers only whether the repaired
  staged tuning machinery can produce a valid diagnostic/handoff artifact on
  the minimal target.
- Confirm Phase 3 JSON status is `passed`, continuation vetoes are `[]`, and
  sampler-setting promotion vetoes are present.
- Confirm Phase 4 JSON status is `passed` and
  `native_divergence_telemetry_status` is
  `native_divergence_not_exposed_by_kernel`.
- Compile the new harness and tests.
- Run focused CPU-hidden tests.
- Run `git diff --check`.
- Claim-boundary scan over Phase 5 files.
- Use visible Codex substitute review if Claude remains blocked by private
  context-transfer policy; record that residual review risk.

Execution command after review:

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase5_tuning_mass_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase5_tuning_mass_cpu_hidden_2026-07-06.md > docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase5_tuning_mass_cpu_hidden_2026-07-06.log 2>&1
```

After execution:

- Validate JSON with `python -m json.tool`.
- Write Phase 5 result with decision and inference-status tables.
- Draft or refresh Phase 6 dimensional-lift subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repaired BayesFilter staged tuning machinery produce a finite, internally valid tuning/mass diagnostic artifact and frozen-kernel handoff candidate for the minimal `zhaocui_fixed` target? |
| Baseline/comparator | Phase 3 fixed-kernel no-adaptation artifact plus Phase 2 scalar oracle and Phase 4 telemetry-status artifact. |
| Candidate/mechanism under test | `bayesfilter.inference.hmc_kernel_tuning.tune_hmc_kernel` with `HMCKernelTuningConfig.smoke(...)` or the smallest diagnostic preset needed to avoid a purely synthetic pass. |
| Primary pass criterion | Artifact status `passed` with no hard vetoes, finite required target/value/score checks, valid staged-tuning result object, valid final/handoff kernel payload or explicit non-promoting repair/budget status, and preserved nonclaims. |
| Promotion criterion | None in this phase. A passed artifact only nominates the tuned-kernel path for later validation. |
| Veto diagnostics | Runtime exception, nonfinite target/value/score, invalid mass artifact, invalid staged result, missing required artifact, Phase 3/4 precondition failure, proxy divergence substitution, unsupported zero-divergence claim, post-hoc threshold edits, or ranking by descriptive metrics alone. |
| Continuation veto | Artifact invalidity, broken target/reference precondition, inability to produce any structured tuning result, or review nonconvergence. Poor tuned-kernel diagnostics without invalidity may trigger repair, not abandonment. |
| Explanatory diagnostics | Acceptance, step size, leapfrog count, mass summaries, stage statuses, runtime, R-hat/ESS if computed, and native-divergence status carried from Phase 4. |
| Not concluded | Zero divergences, posterior correctness, broad HMC convergence, tuned-kernel superiority, default readiness, production readiness, public API/package readiness, source-faithful Zhao-Cui parity, or LEDH evidence. |

## Forbidden Claims And Actions

- Do not claim zero divergences while Phase 4 telemetry remains unavailable.
- Do not rank candidates by descriptive acceptance, runtime, ESS, R-hat, or
  step-size diagnostics alone.
- Do not claim posterior correctness, broad convergence, tuned-kernel
  superiority, default-readiness, production-readiness, public API/package
  readiness, or source-faithful Zhao-Cui parity.
- Do not change public HMC defaults, model files, package state, or the
  source-faithful Zhao-Cui route.
- Do not run trusted GPU/XLA or long HMC in this phase; this is CPU-hidden and
  diagnostic.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 only after Phase 5 records one of:

- a finite structured tuning artifact with a non-promoting frozen-kernel handoff
  candidate suitable for later validation; or
- a valid structured failure explaining the smallest repair needed before
  dimensional lift.

The handoff must carry Phase 4 `native_divergence_not_exposed_by_kernel` as a
limitation and must not treat it as zero divergences.

## Stop Conditions

Stop on invalid tuning artifact, nonfinite target/value/score, missing required
artifact, post-hoc threshold edits, proxy-divergence substitution, unsupported
readiness/superiority/correctness claims, review nonconvergence, or any need to
cross an unreviewed runtime/product/scientific/model-file/source-faithful
boundary.
