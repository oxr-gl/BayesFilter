# P03 Focused Implementation Subplan

Date: 2026-06-23

## Phase Objective

Implement the P02-selected opt-in Sinkhorn scaling gauge-normalization repair,
with focused tests proving the new path is exercised and default raw behavior is
unchanged.

## Entry Conditions Inherited From Previous Phase

- P02 selected exactly one repair family:
  `scaling_normalization="balanced"` / CLI
  `--nystrom-scaling-normalization balanced`, with `none` as the default.
- Claude reviewed P02 and returned `VERDICT: AGREE`.
- P03 implementation scope was refreshed from P02.
- Default raw path, thresholds, and rank/epsilon defaults remain unchanged.

## Required Artifacts

- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-implementation-result-2026-06-23.md`
- P04 refreshed subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p04-brittle-row-repair-gate-subplan-2026-06-23.md`
- Focused test log:
  `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-focused-tests-2026-06-23.log`
- Claude implementation review log:
  `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p03-claude-review-rN-2026-06-23.log`

## Required Checks, Tests, And Reviews

- Edit only scoped implementation/harness/test files needed by the selected
  opt-in repair.
- Preserve `kernel_mode="raw"` as the serious repair gate mode; do not use
  `positive_projected` except as prior diagnostic context.
- Focused CPU-hidden tests:
  `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py`
- Local structural check that CLI/harness metadata records the selected repair.
- Claude read-only implementation review is required before P04 because this
  selected repair changes transport-update math and validation metadata, even
  though it is opt-in and default-preserving.
- Refresh and internally review P04 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is balanced Sinkhorn scaling gauge normalization implemented as a scoped opt-in path without changing default raw behavior? |
| Baseline/comparator | Existing raw Nystrom behavior and focused tests. |
| Primary pass criterion | Focused tests pass, the balanced path is exercised by a discriminating test, default `scaling_normalization="none"` behavior remains unchanged, and P04 artifact contract is ready. |
| Veto diagnostics | Test failure, default behavior change, metadata missing, repair not exercised, broad unrelated edits, or threshold changes. |
| Explanatory diagnostics | Local fixture outputs, metadata fields, code diff. |
| Not concluded | No GPU repair success, no default readiness, no scientific validity. |
| Artifact preserving result | P03 result and focused test log. |

## Forbidden Claims And Actions

- Do not run the serious GPU repair gate in P03.
- Do not change thresholds.
- Do not change default policy.
- Do not modify unrelated dirty files.
- Do not claim the repair works from unit tests.
- Do not combine balanced scaling normalization with positive kernel projection
  in the P04 repair gate.

## Implementation Contract

The implementation should be as small as possible:

- Exact allowed code scope:
  - `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`;
  - `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`;
  - `tests/test_nystrom_transport_tf.py`;
  - `tests/test_actual_sir_nystrom_compiled_redo.py`.
- Add an explicit Nystrom scaling-normalization argument with allowed values
  `none` and `balanced`.
- Preserve `none` as the default everywhere.
- In `balanced`, after each full Sinkhorn `u/v` update, apply a batchwise
  positive scalar gauge transform:
  - `u <- u / c`;
  - `v <- v * c`;
  - with `u` and `v` shaped `[B,N]`, compute:
    - `mean_log_u = mean(log(max(u, denominator_floor)), axis=1, keepdims=True)`;
    - `mean_log_v = mean(log(max(v, denominator_floor)), axis=1, keepdims=True)`;
    - `log_c = 0.5 * (mean_log_u - mean_log_v)`;
    - `c = exp(log_c)`.
  This balances the batchwise geometric means of the clipped current `u` and
  `v` factors after the scalar transform.
- The transform must not alter the kernel matrix, landmarks, core solver,
  rank, epsilon, denominator floor, residual thresholds, paired thresholds, or
  default route.
- Record the selected scaling normalization in Python diagnostics, tensor row
  summaries, benchmark `transport` metadata, and nystrom row metadata.
- Record `max_abs_log_scaling_gauge_shift` and
  `scaling_normalization_applications` in Python diagnostics, tensor row
  summaries, benchmark `transport` metadata, and nystrom row metadata.
- Expose the mode in
  `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` as
  `--nystrom-scaling-normalization {none,balanced}`.
- Keep `--nystrom-kernel-mode raw` for P04/P05 repair validation.

Allowed tests:

- A unit test showing `none` remains the default in diagnostics and CLI
  metadata.
- A unit/XLA test showing `balanced` is accepted, XLA-compilable, finite on a
  deterministic tiny fixture, and records its mode.
- A discriminating fixture where `balanced` records a positive gauge-shift
  diagnostic while `none` records no balancing shift.
- A parse/build-result test showing the benchmark propagates
  `--nystrom-scaling-normalization balanced`.

Disallowed implementation work:

- No changes to rank/epsilon defaults.
- No changes to residual thresholds or paired thresholds.
- No positive kernel projection in the selected repair gate.
- No core-solver-only sweep.
- No automatic fallback from raw/none to balanced mode.
- No broad refactor of the actual-SIR benchmark.

## Exact Next-Phase Handoff Conditions

Advance to P04 only if:

- P03 focused tests pass;
- P03 result records exact files changed and checks run;
- P04 subplan names the exact GPU command, log, JSON, Markdown, and thresholds,
  including `--nystrom-scaling-normalization balanced` and
  `--nystrom-kernel-mode raw`;
- Claude implementation review converges with `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker result if:

- focused tests fail and cannot be repaired within scoped files;
- implementation requires a broad rewrite or new backend;
- code cannot expose enough metadata for P04;
- repair would change default raw behavior or thresholds.

## Skeptical Plan Audit

Proxy risk: passing tests only proves mechanics.  Mitigation: P04 is the first
repair-effectiveness gate.

Boundary risk: selected repair might be a semantic change.  Mitigation: P03
requires opt-in metadata and Claude review for algorithmic math changes.

Artifact risk: P04 may not be able to select the mode.  Mitigation: CLI/harness
metadata is part of P03 primary criterion.

Audit status: `READY_AFTER_P02_PASS`.
