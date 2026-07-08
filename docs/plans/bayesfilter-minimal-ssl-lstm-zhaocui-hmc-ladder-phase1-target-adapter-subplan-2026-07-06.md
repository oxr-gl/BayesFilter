# Phase 1 Subplan: Minimal HMC Target Adapter Bridge

Date: 2026-07-06

Status: `DRAFT_PENDING_PHASE0_REVIEW`

## Phase Objective

Implement an internal minimal HMC target adapter for scalar `zhaocui_fixed` that
wraps the existing TensorFlow manual value/score path with a simple Gaussian
prior and exposes BayesFilter HMC metadata. This phase is a CPU-hidden
debug/reference exception and is not default XLA/HMC evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result exists.
- Review path is approved/completed or substitute-reviewed and recorded.
- Scalar fixture remains frozen.
- No public API, model-file, package metadata, GPU, long, detached, or
  source-faithfulness work is required.

## Required Artifacts

- Minimal HMC harness, expected path:
  `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py`
- Focused test, expected path:
  `tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`
- Phase 1 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase1-target-adapter-result-2026-07-06.md`
- Draft/refreshed Phase 2 subplan.

## Required Checks, Tests, And Reviews

- `python -m compileall -q docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`
- Focused CPU-hidden pytest for adapter value/gradient shape, finiteness, and determinism.
- Forbidden target-path scan over `bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py`.
- Source scan of new harness/test to ensure no `GradientTape`, `tf.py_function`,
  or NumPy target score path.
- Review Phase 1 result/Phase 2 subplan if external review is available; else
  local Codex substitute review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the scalar `zhaocui_fixed` value/score be wrapped as an internal BayesFilter HMC target adapter without changing its target score path, under an explicit CPU-hidden debug/reference exception? |
| Baseline/comparator | Completed scalar smoke harness and existing Phase 7 `_Phase7HMCAdapter` pattern. |
| Primary pass criterion | Adapter returns finite deterministic log prob and gradient with shape `(24,)`, records graph-native HMC capability, and does not use target-path autodiff/NumPy. |
| Veto diagnostics | Nonfinite value/score, wrong shape, nondeterminism, invalid `ValueScoreCapability`, target-path autodiff/NumPy, public API change, or unsupported claim. |
| Explanatory diagnostics | Initial log prob, score norm, prior scale, offset scale, runtime, metadata signature, and explicit non-JIT/debug exception labeling if used. |
| Not concluded | No HMC sample pass, convergence, posterior correctness, ranking, GPU/XLA readiness, default readiness, source-faithful parity, or LEDH result. |

## Forbidden Claims And Actions

- Do not claim that target-adapter admission proves HMC works.
- Do not label non-JIT/eager checks as default XLA/HMC evidence.
- Do not change public APIs, model files, package metadata, or default policy.
- Do not use `GradientTape`, `tf.py_function`, finite differences, or NumPy as
  the target score path.
- Do not run long HMC, GPU, or detached execution.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only when:

- harness/test files exist;
- compile and focused tests pass;
- Phase 1 result records value/score checks and evidence limits;
- Phase 2 CPU-hidden HMC canary subplan exists and is reviewed or queued for
  approved/substitute review.

## Stop Conditions

Stop if adapter admission requires target-path autodiff/NumPy, public API or
model-file changes, broadening the fixture, unapproved runtime scope, or
unsupported scientific/runtime claims.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write Phase 1 result/close record.
3. Draft or refresh Phase 2 subplan.
4. Review Phase 2 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
