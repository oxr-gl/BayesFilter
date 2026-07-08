# Phase 1 Repair Subplan: Runtime-Bounded Filtering Geometry Micro Preflight

Date: 2026-07-08
Status: `DRAFT_READY_FOR_REVIEW`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Parent subplan: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-subplan-2026-07-08.md`

## Phase Objective

Repair Phase 1 execution flow after the horizon-30 filtering-geometry diagnostic timed out before writing JSON/Markdown artifacts. The repair asks the smallest useful question: can the scalar filtering target wrapper, finite value/score checks, and low-rank SPD geometry utility complete on a micro filtering target with the minimum valid sample-ratio gate?

This repair is not a substitute for the original Phase 1 geometry scale. It is a micro preflight to distinguish broken harness/runtime flow from a true target-geometry failure.

## Entry Conditions Inherited From Phase 1

- Phase 1 subplan review returned local Codex substitute `VERDICT: AGREE`.
- Compile and focused unit tests passed before the first diagnostic.
- The first horizon-100/260 run was interrupted after exceeding the visible-execution boundary with no JSON/Markdown artifact.
- The repaired horizon-30/72 run hit `timeout 300` with no JSON/Markdown artifact.
- The only log content in both long runs was TensorFlow CUDA initialization noise while CPU-hidden execution was intended.
- No result so far supports a filtering-geometry, HMC-readiness, posterior-correctness, or scientific claim.

## Required Artifacts

- Repair subplan: this file.
- Repair review bundle: `docs/reviews/scalar-filtering-geometry-hmc-phase1-runtime-repair-review-bundle-2026-07-08.md`
- Micro JSON artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_micro_cpu_hidden_2026-07-08.json`
- Micro Markdown artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_micro_cpu_hidden_2026-07-08.md`
- Micro log artifact: `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_micro_cpu_hidden_2026-07-08.log`
- Phase 1 result or next repair result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-result-2026-07-08.md`

## Required Checks, Tests, Reviews

- Local Codex substitute review of this repair subplan because Claude review is policy-blocked for private repository context transfer.
- `python -m py_compile docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py`
- `pytest tests/test_scalar_ssl_lstm_filtering_geometry.py tests/test_quadratic_geometry.py -q`
- Micro preflight command:

```bash
timeout 120 env CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py \
  --horizon 4 \
  --sample-count 45 \
  --pilot-direction-count 16 \
  --trust-radius 0.20 \
  --no-finite-difference-curvature \
  --json-path docs/benchmarks/scalar_ssl_lstm_filtering_geometry_micro_cpu_hidden_2026-07-08.json \
  --markdown-path docs/benchmarks/scalar_ssl_lstm_filtering_geometry_micro_cpu_hidden_2026-07-08.md \
  > docs/benchmarks/scalar_ssl_lstm_filtering_geometry_micro_cpu_hidden_2026-07-08.log 2>&1
```

- `git diff --check`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the scalar filtering target wrapper and geometry utility complete on a micro CPU-hidden filtering target and write structured artifacts? |
| Baseline/comparator | The two parent Phase 1 runs that timed out before writing artifacts. |
| Primary criterion | The micro command exits before `timeout 120` and writes JSON/Markdown/log artifacts with a parseable `decision` block. |
| Veto diagnostics | Timeout, missing JSON/Markdown artifact, nonfinite target value/score accepted, sample count below required ratio accepted, rejected geometry treated as success, unsupported HMC/posterior/default claim. |
| Explanatory diagnostics | Whether `geometry_sanity_passed` is true or false, score norm, holdout status, condition number, runtime, and TensorFlow device noise. |
| Not concluded | No full Phase 1 scale readiness, no mass handoff readiness unless the parent Phase 1 gate is later satisfied, no HMC readiness, no posterior correctness, no convergence, no default readiness. |
| Preserving artifact | Micro JSON/Markdown/log and Phase 1 result/repair note. |

## Fixed Micro Settings

| Setting | Value | Provenance | Role |
| --- | --- | --- | --- |
| Horizon | `4` | Existing focused test horizon for finite filtering score | Micro preflight only |
| Sample count | `45` | Exactly `5 * (1 + 4 + 1 + 3)` for the four-dimensional low-rank fit | Minimum sample-ratio gate |
| Pilot direction count | `16` | Small bounded basis-search effort | Runtime repair setting |
| Trust radius | `0.20` | Smaller than parent `0.30` to reduce nonlinearity in micro preflight | Runtime repair setting |
| Finite-difference curvature | Disabled | Avoids extra value/score calls in runtime repair | Execution-flow repair |
| Wall timeout | `120` seconds | Strict repair budget | Continuation veto if exceeded |

The inherited geometry coordinate convention remains `theta = center + scale * z`; the micro preflight must serialize the same whitened-coordinate convention if it writes a JSON artifact.

## Forbidden Claims And Actions

- Do not run HMC.
- Do not advance to Phase 2 from a micro preflight alone unless the parent Phase 1 result explicitly justifies that the micro artifact satisfies the reviewed handoff conditions.
- Do not claim HMC readiness, posterior correctness, convergence, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness.
- Do not treat timeout as evidence against the scientific idea; it is an execution-flow/harness issue unless a structured target artifact says otherwise.
- Do not install packages, fetch network resources, edit model files, or perform destructive git/filesystem actions.

## Exact Next-Phase Handoff Conditions

This repair does not directly hand off to Phase 2. It hands back to Phase 1 assessment:

- If the micro preflight writes a valid artifact, use it to decide whether to repair the parent Phase 1 scale, reduce the parent gate, or write a blocker result.
- If the micro preflight times out or fails to write artifacts, write Phase 1 as blocked on filtering-score runtime/harness execution flow and stop before mass/HMC.
- If the micro artifact reports rejected geometry, write Phase 1 as a geometry repair-trigger result, not as HMC failure.

## Stop Conditions

- Repair review returns unresolved `REVISE`.
- Micro command times out or produces no JSON/Markdown artifact.
- Required checks fail and cannot be repaired in Phase 1 scope.
- Continuing would require HMC execution, package installation, network fetch, credentials, default-policy change, model-file edit, destructive git/filesystem action, or unsupported scientific/runtime claim.

## Skeptical Audit

- Wrong baseline: the repair compares against the timed-out Phase 1 execution flow, not against posterior correctness.
- Proxy metric risk: micro success is only harness/runtime evidence and cannot promote HMC or Phase 2 by itself.
- Missing stop conditions: timeout or missing artifact stops Phase 1 before mass/HMC.
- Unfair comparison: no ranking or sampler comparison occurs.
- Hidden assumptions: horizon-4 completion may not transfer to horizon 30 or 100.
- Stale context: the repair directly addresses the observed timeout/missing artifact.
- Environment mismatch: CPU-hidden debug/reference status remains explicit.
- Artifact adequacy: the micro artifact answers completion and structured-output viability only.

Audit result: `PASS_WITH_BOUNDARIES_PENDING_REVIEW`. Execute only after repair review.
