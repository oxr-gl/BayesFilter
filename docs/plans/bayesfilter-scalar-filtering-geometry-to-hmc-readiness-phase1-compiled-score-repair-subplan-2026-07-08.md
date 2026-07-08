# Phase 1 Repair Subplan: Compiled Filtering Score Geometry Retry

Date: 2026-07-08
Status: `DRAFT_READY_FOR_REVIEW`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Parent subplan: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-subplan-2026-07-08.md`

## Phase Objective

Repair the Phase 1 parent-scale runtime blocker by compiling the scalar filtering target value/score wrapper with `tf.function(jit_compile=False)` for CPU-hidden debug execution, verify compiled/eager parity on the micro target, then retry the repaired parent-scale horizon-30 diagnostic.

This is an execution-flow repair. It must not change the filtering target, geometry pass/fail criteria, or non-claims.

## Entry Conditions Inherited From Prior Phase 1 Repairs

- Phase 1 subplan review returned local Codex substitute `VERDICT: AGREE`.
- Initial horizon-100/260 diagnostic was interrupted after no artifact was written near the visible-execution boundary.
- Repaired horizon-30/72 diagnostic hit `timeout 300` with no JSON/Markdown artifact.
- Micro horizon-4/45 preflight completed in about 29.7 seconds and wrote a valid artifact with no vetoes.
- Micro result is harness/runtime evidence only and does not establish parent-scale or Phase 2 readiness.

## Required Artifacts

- Repair subplan: this file.
- Repair review bundle: `docs/reviews/scalar-filtering-geometry-hmc-phase1-compiled-score-repair-review-bundle-2026-07-08.md`
- Updated benchmark script: `docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py`
- Updated focused tests: `tests/test_scalar_ssl_lstm_filtering_geometry.py`
- Parent retry JSON artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json`
- Parent retry Markdown artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.md`
- Parent retry log artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.log`
- Phase 1 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-result-2026-07-08.md`

## Required Checks, Tests, Reviews

- Local Codex substitute review of this repair subplan because Claude review is policy-blocked for private repository context transfer.
- `python -m py_compile docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py`
- `pytest tests/test_scalar_ssl_lstm_filtering_geometry.py tests/test_quadratic_geometry.py -q`
- Parent retry command:

```bash
timeout 300 env CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py \
  --json-path docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json \
  --markdown-path docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.md \
  > docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.log 2>&1
```

- `git diff --check`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does compiling the value/score wrapper make the horizon-30 filtering geometry diagnostic complete and write structured artifacts without changing the target? |
| Baseline/comparator | Prior horizon-30/72 run with eager repeated score calls timed out after `timeout 300` and wrote no artifact. |
| Primary criterion | Compiled/eager value-score parity test passes, parent retry exits before `timeout 300`, and JSON/Markdown/log artifacts are written with a parseable `decision` block. |
| Veto diagnostics | Compiled/eager mismatch, timeout, missing artifacts, target value/score nonfinite accepted, rejected geometry treated as pass, hidden XLA/GPU/default-readiness claim, hidden HMC execution. |
| Explanatory diagnostics | Runtime, center score norm, finite sample count, condition number, holdout fit, and whether geometry passes. |
| Not concluded | No HMC readiness, no posterior correctness, no sampler convergence, no statistical ranking, no default readiness, no GPU/XLA production readiness. |
| Preserving artifact | Parent retry JSON/Markdown/log and Phase 1 result note. |

## Fixed Repair Settings

| Setting | Value | Provenance | Role |
| --- | --- | --- | --- |
| Value/score wrapper | `tf.function(jit_compile=False)` | Execution-flow repair after repeated eager calls timed out | CPU-hidden debug optimization |
| XLA JIT | Disabled | CPU-hidden debug/localization exception | Not production/default evidence |
| Horizon | `30` | Repaired parent Phase 1 setting | Parent-scale diagnostic |
| Sample count | `72` | Repaired parent setting, still above required 45 | Sample-ratio hard gate |
| Pilot directions | `64` | Repaired parent setting | Explanatory basis-search effort |
| Timeout | `300` seconds | Repaired parent execution cap | Continuation veto |

## Forbidden Claims And Actions

- Do not run HMC.
- Do not claim GPU/XLA production readiness from non-XLA CPU-hidden graph execution.
- Do not claim posterior correctness, convergence, default readiness, sampler superiority, or Zhao-Cui source-faithfulness.
- Do not change the geometry pass/fail criteria after seeing the retry result.
- Do not install packages, fetch network resources, edit model files, or perform destructive git/filesystem actions.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- Compiled/eager parity test passes.
- Parent retry writes a valid JSON artifact before timeout.
- Parent artifact records `geometry_sanity_passed: true`.
- Artifact records CPU-hidden/non-XLA debug execution and the whitened coordinate convention.
- Phase 1 result explicitly preserves non-claims and explains that micro preflight was not itself Phase 2 readiness.
- Phase 2 mass-handoff subplan is drafted and reviewed.

If the parent retry times out or writes no artifact, write Phase 1 as blocked on filtering-score runtime/harness execution flow and stop before mass/HMC.

## Stop Conditions

- Repair review returns unresolved `REVISE`.
- Compiled/eager parity fails.
- Parent retry times out or produces no structured artifact.
- Required tests fail and cannot be repaired within Phase 1 scope.
- Continuing would require HMC execution, package installation, network fetch, credentials, default-policy change, model-file edit, destructive git/filesystem action, or unsupported scientific/runtime claim.

## Skeptical Audit

- Wrong baseline: the comparator is the timed-out eager parent run, not posterior correctness.
- Proxy metric risk: faster runtime and geometry pass do not prove HMC or posterior validity.
- Missing stop conditions: timeout, missing artifact, parity mismatch, and rejected geometry all block Phase 2.
- Unfair comparison: no stochastic method ranking occurs.
- Hidden assumptions: graph execution may speed repeated calls but still differs from GPU/XLA production.
- Stale context: the repair directly addresses the observed repeated-score-call runtime blocker.
- Environment mismatch: CPU-hidden non-XLA debug execution is labeled and cannot be production evidence.
- Artifact adequacy: the retry artifact answers parent-scale Phase 1 geometry only.

Audit result: `PASS_WITH_BOUNDARIES_PENDING_REVIEW`. Execute only after repair review.
