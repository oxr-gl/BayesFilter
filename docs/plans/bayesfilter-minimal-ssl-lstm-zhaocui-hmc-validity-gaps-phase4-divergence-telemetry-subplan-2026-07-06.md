# Phase 4 Subplan: Native Divergence Telemetry Inspection

Date: 2026-07-06

Status: `READY_FOR_REVIEW`

## Phase Objective

Determine whether the current TensorFlow Probability HMC result objects expose
a native boolean divergence field for the minimal `zhaocui_fixed` HMC path. If
they do not, record the limitation without substituting acceptance,
log-acceptance, energy, target-log-probability, or R-hat/ESS proxies for native
divergence telemetry.

## Entry Conditions Inherited From Previous Phase

- Phase 3 result exists:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-longer-hmc-diagnostics-result-2026-07-06.md`.
- Phase 3 trusted GPU/XLA JSON artifact exists:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.json`.
- Phase 3 artifact status is `passed` with no continuation vetoes.
- Phase 3 promotion screen failed because of R-hat, ESS, and
  `native_divergence_telemetry_not_exposed`.
- Sampled-state target/reference agreement passed in Phase 3; this remains
  target/reference evidence only, not full posterior correctness.

## Required Artifacts

- Telemetry harness:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_divergence_telemetry_2026_07_06.py`
- Tests:
  `tests/test_minimal_ssl_lstm_zhaocui_hmc_divergence_telemetry.py`
- JSON artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase4_divergence_telemetry_cpu_hidden_2026-07-06.json`
- Markdown artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase4_divergence_telemetry_cpu_hidden_2026-07-06.md`
- Quiet log:
  `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/phase4_divergence_telemetry_cpu_hidden_2026-07-06.log`
- Phase 4 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase4-divergence-telemetry-result-2026-07-06.md`
- Refreshed Phase 5 tuning/mass ladder subplan.

## Required Checks, Tests, Reviews

Before execution:

- Skeptical plan audit: confirm the command answers only native telemetry
  availability and does not smuggle a zero-divergence, convergence, ranking,
  readiness, or posterior claim.
- Confirm Phase 3 JSON status is `passed`, continuation vetoes are `[]`, and
  `native_divergence_telemetry_not_exposed` is present as a promotion veto.
- Compile the new harness and tests.
- Run focused CPU-hidden tests.
- Run `git diff --check`.
- Claim-boundary scan over Phase 4 files.
- Read-only review of this subplan. Claude remains blocked for private-context
  transfer unless policy changes; use fresh visible Codex substitute review if
  needed and record that it is weaker than full Claude review.

Execution command after review:

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_divergence_telemetry_2026_07_06.py --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase4_divergence_telemetry_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_validity_phase4_divergence_telemetry_cpu_hidden_2026-07-06.md
```

Stdout/stderr must be captured in the quiet log path listed above.

After execution:

- Validate JSON with `python -m json.tool`.
- Write Phase 4 result with decision and inference-status tables.
- Refresh Phase 5 tuning/mass ladder subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the current TFP HMC kernel result structure expose any native boolean divergence field reachable by the BayesFilter extractor for the minimal HMC target? |
| Baseline/comparator | Phase 3 runtime artifact reporting `not_exposed_by_kernel`, plus local TFP HMC kernel bootstrap/one-step result structures. |
| Primary pass criterion | Artifact records the inspected result-object tree, the exact native boolean field search, extractor output, and a clear status: `native_divergence_available` or `native_divergence_not_exposed_by_kernel`. |
| Veto diagnostics | Runtime exception, nonfinite target/value in the tiny inspection, missing field-tree artifact, treating proxy metrics as divergence, claiming zero divergences from missing telemetry, invalid artifact, or unsupported claim. |
| Explanatory diagnostics | Kernel result class names, public field names, dtypes/shapes of inspected fields, acceptance/log-accept/target-log-prob health recorded only as non-divergence health context. |
| Not concluded | Zero divergences unless a native boolean divergence field is exposed and checked, HMC convergence, posterior correctness, ranking/superiority, source-faithful parity, default readiness, production readiness, public API/package readiness, or LEDH evidence. |

## Forbidden Claims And Actions

- Do not call acceptance, log-acceptance, target-log-probability, energy,
  R-hat, ESS, or any non-boolean/private inferred quantity a divergence.
- Do not claim zero divergences from `not_exposed_by_kernel`.
- Do not change HMC internals, public API, defaults, model files, package state,
  or source-faithful Zhao-Cui route.
- Do not run long HMC or trusted GPU/XLA runtime in this phase. The execution is
  CPU-hidden, short, and telemetry-inspection-only.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 after Phase 4 result records one of:

- native divergence telemetry is available, with exact field anchors and no
  proxy substitution; or
- native divergence telemetry remains unavailable, with field-tree evidence and
  explicit nonclaim of zero divergences.

Phase 5 must address the Phase 3 sampler-setting promotion vetoes with a
reviewed tuning/mass diagnostic design. It must not reinterpret Phase 4 missing
telemetry as zero divergences.

## Stop Conditions

Stop if review does not converge after five rounds for the same blocker, if the
artifact cannot record the inspected result-object tree, if the tiny inspection
has runtime/nonfinite invalidity, if pressure arises to use proxy divergence
metrics, or if continuing would cross an unreviewed runtime/product/scientific
or source-faithful boundary.
