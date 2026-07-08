# Phase 4 Result: Short Replicated Debug Ladder

Date: 2026-07-06

Status: `PASSED_ALL_PREDECLARED_SEEDS`

## Phase Objective

Run a short replicated CPU-hidden debug ladder over predeclared seeds to
collect hard-veto and descriptive sampler diagnostics without making
convergence, ranking, or default-readiness claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do several tiny CPU-hidden HMC runs avoid hard vetoes under fixed predeclared settings? |
| Baseline/comparator | Phase 2/3 canary plus identical scalar target across fixed seeds. |
| Primary pass criterion | All predeclared seeds complete without hard vetoes and artifacts preserve evidence limits. |
| Veto diagnostics | Runtime exception, nonfinite sample, native divergence if exposed and positive, invalid artifact, missing seed, changed settings after seeing results, or unsupported claim. |
| Explanatory diagnostics | Acceptance rate, runtime, finite counts, and per-seed hard-veto rows only. |
| Not concluded | HMC convergence, posterior correctness, ranking, GPU/XLA readiness, default readiness, source-faithful parity, or LEDH result. |

## Skeptical Plan Audit

Result: `PASSED_FOR_FIXED_SHORT_DEBUG_LADDER`

Phase 4 stayed within the reviewed CPU-hidden debug envelope. The harness was
repaired to fail closed on settings drift: exact seeds
`(20260706, 2401)`, `(20260706, 2402)`, `(20260706, 2403)`, exact settings
`num_results=2`, `num_burnin_steps=1`, `num_leapfrog_steps=1`,
`step_size=1e-5`, `use_xla=False`, and `chain_execution_mode="tf_function"`.
Acceptance rate remained explanatory only. R-hat/ESS were not computed.

## Review Trail

Phase 4 handoff review initially returned `VERDICT: REVISE` for four fixable
issues: settings drift, missing explicit quiet-log contract, stale Phase 2
nonclaims, and inconsistent R-hat/ESS wording. The harness, tests, and subplan
were patched. Focused re-review returned `VERDICT: AGREE`.

## Command

```bash
mkdir -p docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_ladder_2026-07-06
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py \
  --mode phase4-short-ladder \
  --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_short_ladder_cpu_hidden_2026-07-06.json \
  --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_short_ladder_cpu_hidden_2026-07-06.md \
  > docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_ladder_2026-07-06/phase4_short_ladder_cpu_hidden_2026-07-06.log 2>&1
```

## Local Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Compile | `PASSED` | `python -m compileall -q docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py` |
| Focused CPU-hidden pytest | `PASSED` | `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 pytest -q tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py` returned `9 passed`. |
| Forbidden-mechanism scan | `PASSED` | No `GradientTape`, `tf.py_function`, `import numpy`, or `np.` matches in the new harness/test or existing Zhao-Cui fixed adapter. |
| `git diff --check` | `PASSED` | Command returned exit status 0 after ladder artifact generation. |
| Standalone short ladder command | `PASSED` | Exit status 0; JSON, Markdown, and quiet log written. |

## Artifact Summary

Artifacts:

- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_short_ladder_cpu_hidden_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_short_ladder_cpu_hidden_2026-07-06.md`
- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_ladder_2026-07-06/phase4_short_ladder_cpu_hidden_2026-07-06.log`

Per-seed summary:

| Seed | Status | Hard vetoes | Acceptance rate | Nonfinite sample count | Divergence status |
| --- | --- | --- | --- | --- | --- |
| `[20260706, 2401]` | `passed` | `[]` | `1.0` explanatory only | `0` | `not_exposed_by_kernel` |
| `[20260706, 2402]` | `passed` | `[]` | `1.0` explanatory only | `0` | `not_exposed_by_kernel` |
| `[20260706, 2403]` | `passed` | `[]` | `1.0` explanatory only | `0` | `not_exposed_by_kernel` |

Global summary:

| Diagnostic | Value |
| --- | --- |
| Status | `passed` |
| All predeclared seeds passed | `True` |
| Hard vetoes | `[]` |
| Fixed seeds | `[[20260706, 2401], [20260706, 2402], [20260706, 2403]]` |
| Sample shape per seed | `[2, 24]` |
| Native divergence count | `None` for all rows; not interpreted as zero divergences |
| Quiet log path | `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_ladder_2026-07-06/phase4_short_ladder_cpu_hidden_2026-07-06.log` |

The log includes TensorFlow's CPU-hidden CUDA initialization warning. This is
not GPU evidence; the artifact records `gpu_devices: []`,
`physical_devices: ['/physical_device:CPU:0']`, and
`trust_basis: cpu_hidden_debug_no_gpu_claim`.

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `ADVANCE_TO_PHASE5_GPU_XLA_NEED_AUDIT` |
| Primary criterion status | `PASSED` |
| Veto diagnostic status | `NO_PHASE4_HARD_VETO_OBSERVED` |
| Main uncertainty | Tiny seed ladder still cannot assess convergence, posterior correctness, ranking, or default readiness. |
| Next justified action | Audit whether Phase 5 GPU/XLA is actually needed; absent a remaining runtime-path question, record deferral rather than escalating runtime scope. |
| What is not being concluded | HMC convergence, posterior correctness, ranking, GPU/XLA readiness, default readiness, source-faithful parity, or LEDH result. |

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | `PASSED_FOR_ALL_PREDECLARED_SEEDS` |
| Statistically supported ranking | `NOT_CLAIMED` |
| Descriptive-only differences | `Per-seed acceptance/runtime differences are descriptive only.` |
| Default-readiness | `NOT_CHECKED` |
| Next evidence needed | Explicit Phase 5 deferral or approved new runtime-path question. |

## Handoff

Phase 5 should start with a need audit, not an automatic GPU/XLA launch. The
CPU-hidden mechanics question has already been answered at the current evidence
class.
