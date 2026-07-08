# Phase 1 Result: Minimal Smoke Harness And Artifact Writer

Date: 2026-07-06

Status: `PASSED`

## Phase Objective

Create a minimal scalar SSL-LSTM smoke harness that emits a structured artifact
for `zhaocui_fixed` first, with descriptive mechanics comparator rows for
`fixed_sgqf` and `svd_ukf`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the minimal scalar SSL-LSTM `zhaocui_fixed` mechanics be materialized as a structured smoke artifact? |
| Baseline/comparator | Existing `tests/test_ssl_lstm_zhaocui_fixed_adapter.py` fixture; `fixed_sgqf` and `svd_ukf` rows are mechanics comparators only. |
| Primary pass criterion | Harness emits schema-valid artifact with scalar dimensions, finite deterministic `zhaocui_fixed` value/score, and finite-difference subset residual. |
| Veto diagnostics | Nonfinite value/score, nondeterminism, finite-difference mismatch, target autodiff/NumPy, invalid artifact, wrong dimensions, or unsupported claim. |
| Explanatory diagnostics | Runtime, score norm, comparator values, reference sample count, and recenter diagnostics. |
| Not concluded | Posterior correctness, HMC convergence, ranking, source-faithful parity, GPU/XLA production readiness, default readiness, or LEDH result. |

## Skeptical Plan Audit

Result: `PASSED`

The implemented harness answers the mechanics-smoke question directly by
materializing the already admitted scalar fixture. The primary gate is the
`zhaocui_fixed` row only. `fixed_sgqf` and `svd_ukf` rows are labeled
descriptive mechanics comparators and are not used for ranking or superiority.
Finite differences are an adapter-admission veto/diagnostic, not the target
score path. The generated artifact labels the run as CPU-hidden debug evidence
and makes no GPU/XLA production, posterior correctness, HMC convergence,
source-faithful parity, default-readiness, or LEDH claim.

## Implementation

Added:

- `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_smoke_2026_07_06.py`
- `tests/test_minimal_ssl_lstm_zhaocui_smoke.py`

Generated artifacts:

- `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.md`

## Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Compile | `PASSED` | `python -m compileall -q docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_smoke_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_smoke.py` |
| Focused pytest | `PASSED` | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_minimal_ssl_lstm_zhaocui_smoke.py` returned `3 passed`. |
| Harness run | `PASSED` | `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_smoke_2026_07_06.py --output docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.json --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.md` returned status `passed`. |
| JSON artifact validation | `PASSED` | Scalar dimensions, primary filter, finite score, FD pass, and CPU-hidden manifest were checked. |
| Markdown artifact validation | `PASSED` | Summary includes scalar dimensions, comparator roles, and nonclaims. |
| Target-path forbidden scan | `PASSED` | `rg -n "GradientTape|tf\\.py_function|np\\.|numpy" bayesfilter/nonlinear/ssl_lstm_zhaocui_fixed_adapter.py` returned no hits. |
| `git diff --check` | `PASSED` | Command returned exit status 0 after edits. |

Environment note: the artifact-producing TensorFlow command emitted a CUDA
initialization warning even with `CUDA_VISIBLE_DEVICES=-1`. This result remains
classified as CPU-hidden debug evidence only and is not GPU evidence.

## Primary Result Snapshot

| Metric | Value |
| --- | --- |
| Status | `passed` |
| Primary filter | `zhaocui_fixed` |
| Dimensions | `latent_dim=1`, `hidden_dim=1`, `observation_dim=1`, `horizon=2` |
| Log likelihood | `-1.3969803149874547` |
| Score norm | `1.6251569331205422` |
| FD max abs error | `8.616574120878795e-11` |
| Determinism check | `passed` |

Comparator rows are descriptive only:

| Filter | Log likelihood | Score norm |
| --- | --- | --- |
| `fixed_sgqf` | `-1.514549865972079` | `1.735676436384646` |
| `svd_ukf` | `-1.5143464314470754` | `1.7355295124178867` |

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `PASS_ADVANCE_TO_PHASE2` |
| Primary criterion status | `PASSED` |
| Veto diagnostic status | `NO_VETO_OBSERVED` |
| Main uncertainty | The result is a minimal CPU-hidden debug smoke only; it does not address HMC behavior, posterior correctness, GPU/XLA production readiness, or source-faithful Zhao-Cui parity. |
| Next justified action | Run Phase 2 local-checks and artifact-boundary review. |
| What is not being concluded | No posterior correctness, HMC convergence, ranking, method superiority, source-faithful parity, GPU/XLA production readiness, default readiness, or LEDH result. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | `PASSED` for scalar mechanics smoke. |
| Statistically supported ranking | `NOT_CHECKED`; no ranking is claimed. |
| Descriptive-only differences | Comparator log likelihoods and score norms are descriptive only. |
| Default-readiness | `NOT_CHECKED`; no default change is justified. |
| Next evidence needed | Phase 2 local boundary checks, then a separately reviewed launch-smoke bridge if needed. |

## Handoff

Phase 2 may start. Phase 2 should rerun focused local checks, inspect artifact
boundaries, scan for unsupported claims, and decide whether the optional
launch-smoke bridge is still needed.
