# Phase 1 Result: Minimal HMC Target Adapter Bridge

Date: 2026-07-06

Status: `PASSED_WITH_PHASE2_HANDOFF_REVIEW`

## Phase Objective

Implement an internal minimal HMC target adapter for scalar `zhaocui_fixed`
that wraps the existing TensorFlow manual value/score path with a Gaussian
prior and exposes BayesFilter HMC metadata. This phase is a CPU-hidden
debug/reference exception and is not default XLA/HMC evidence.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the scalar `zhaocui_fixed` value/score be wrapped as an internal BayesFilter HMC target adapter without changing its target score path, under an explicit CPU-hidden debug/reference exception? |
| Baseline/comparator | Completed scalar smoke harness and existing Phase 7 `_Phase7HMCAdapter` pattern. |
| Primary pass criterion | Adapter returns finite deterministic log prob and gradient with shape `(24,)`, records graph-native HMC capability, and does not use target-path autodiff/NumPy. |
| Veto diagnostics | Nonfinite value/score, wrong shape, nondeterminism, invalid `ValueScoreCapability`, target-path autodiff/NumPy, public API change, or unsupported claim. |
| Explanatory diagnostics | Initial log prob, score norm, prior scale, offset scale, runtime, metadata signature, and explicit non-JIT/debug exception labeling. |
| Not concluded | No HMC sample pass, convergence, posterior correctness, ranking, GPU/XLA readiness, default readiness, source-faithful parity, or LEDH result. |

## Skeptical Plan Audit

Result: `PASSED_FOR_PHASE1_LOCAL_CHECKS`

The baseline remained the completed scalar smoke fixture plus the existing
Phase 7 adapter pattern. The implementation did not broaden the model, did not
introduce a new sampler runner, did not run HMC, and did not treat CPU-hidden
non-JIT execution as BayesFilter default GPU/XLA evidence. The only promotion
criterion for this phase was target-adapter admission: finite deterministic
value/score, expected shapes, graph-native metadata, and absence of forbidden
target-path mechanisms.

## Implementation

Added:

- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py`
- `tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py`

The harness defines `MinimalZhaoCuiHMCTargetAdapter`, reuses the frozen scalar
fixture from the minimal smoke harness, calls `tf_ssl_lstm_zhaocui_fixed_score`,
adds a Gaussian prior centered at the frozen `theta`, and exposes
`ValueScoreCapability` with `graph_native` authority. It supports scalar inputs
with gradient shape `(24,)` and a small batch path with score shape `(2, 24)`.

## Local Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Compile | `PASSED` | `python -m compileall -q docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py` |
| Focused CPU-hidden pytest | `PASSED` | `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 pytest -q tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py` returned `4 passed`. |
| New harness/test forbidden-mechanism scan | `PASSED` | No `GradientTape`, `tf.py_function`, `import numpy`, or `np.` matches in the new harness/test. TensorFlow `.numpy()` conversions occur only after evaluation for artifact/reporting and test assertions. |
| Zhao-Cui adapter forbidden-mechanism scan | `PASSED` | No `GradientTape`, `tf.py_function`, `import numpy`, or `np.` matches in `bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py`. |
| `git diff --check` | `PASSED` | Command returned exit status 0 before this result note. |
| Phase 1 artifact write | `PASSED` | JSON/Markdown artifact written with status `passed` and no hard vetoes. |

## Artifact Summary

Artifacts:

- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_adapter_cpu_hidden_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_adapter_cpu_hidden_2026-07-06.md`

Observed adapter diagnostics:

| Diagnostic | Value |
| --- | --- |
| Status | `passed` |
| Hard vetoes | `[]` |
| Log probability | `-1.3985848756201187` |
| Score norm | `1.624779105977436` |
| Score shape | `[24]` |
| Batch score shape | `[2, 24]` |
| Value/score authority | `graph_native` |
| Runtime scope | `CPU-hidden debug/reference exception` |
| CUDA visibility | `CUDA_VISIBLE_DEVICES=-1`; no GPU evidence claimed |

TensorFlow emitted a CPU-hidden CUDA initialization warning during artifact
generation. This is not GPU evidence; the artifact records `gpu_devices: []`,
`physical_devices: ['/physical_device:CPU:0']`, and
`trust_basis: cpu_hidden_debug_no_gpu_claim`.

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `ADVANCE_TO_PHASE2_STANDALONE_CANARY` |
| Primary criterion status | `PASSED` |
| Veto diagnostic status | `NO_PHASE1_HARD_VETO_OBSERVED` |
| Main uncertainty | Focused tests exercised the canary path, but the standalone Phase 2 artifact has not yet been launched in its final output/log path. |
| Next justified action | Run the standalone Phase 2 tiny CPU-hidden HMC canary artifact command. |
| What is not being concluded | No HMC sample pass, convergence, posterior correctness, ranking, GPU/XLA readiness, default readiness, source-faithful parity, or LEDH result. |

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | `PASSED_FOR_PHASE1_TARGET_ADAPTER_ADMISSION` |
| Statistically supported ranking | `NOT_CLAIMED` |
| Descriptive-only differences | `Score norm and runtime are explanatory only.` |
| Default-readiness | `NOT_CHECKED` |
| Next evidence needed | Phase 2 tiny CPU-hidden HMC canary with hard-veto classification. |

## Handoff

Phase 2 may begin. The Phase 2 handoff repair was rechecked and focused local
substitute re-review returned `VERDICT: AGREE`. The next phase remains a
CPU-hidden, non-JIT debug/reference canary unless a reviewed plan explicitly
changes that scope.
