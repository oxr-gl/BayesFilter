# Phase 2 Result: CPU-Hidden HMC Canary

Date: 2026-07-06

Status: `PASSED_NO_HARD_VETO`

## Phase Objective

Run the smallest CPU-hidden HMC canary for the scalar `zhaocui_fixed` target
adapter using BayesFilter `run_full_chain_tfp_hmc`. This phase is an explicit
CPU-hidden, non-JIT debug/reference exception and is not default XLA/HMC
evidence.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the scalar `zhaocui_fixed` target run through the HMC machinery without hard-veto failure in a tiny CPU-hidden, non-JIT debug canary? |
| Baseline/comparator | Phase 1 adapter and existing `run_full_chain_tfp_hmc` launch-smoke pattern. |
| Primary pass criterion | Canary artifact records finite initial value/score, no HMC runtime exception, no nonfinite samples, and valid schema. |
| Veto diagnostics | Nonfinite initial value/score, HMC runtime exception, nonfinite samples, invalid artifact, wrong fixture, unsupported claim, missing debug/reference exception label, or evidence-class mismatch. |
| Explanatory diagnostics | Acceptance rate, runtime, initial score norm, sample finite counts, and TensorFlow CUDA warning under CPU-hidden execution. |
| Not concluded | HMC convergence, posterior correctness, R-hat/ESS, ranking, GPU/XLA production readiness, default readiness, source-faithful parity, or LEDH result. |

## Skeptical Plan Audit

Result: `PASSED_FOR_TINY_CPU_HIDDEN_CANARY`

The canary used the Phase 1 adapter and existing `run_full_chain_tfp_hmc` API.
Settings were fixed before launch: `num_results=2`, `num_burnin_steps=1`,
`num_leapfrog_steps=1`, `step_size=1e-5`, seed `(20260706, 2201)`,
`use_xla=False`, and `chain_execution_mode="tf_function"`. The run produced a
standalone artifact and quiet log. Acceptance rate was labeled explanatory only
and was not used as convergence, ranking, or default-readiness evidence.

## Review Trail

Phase 2 handoff review initially returned `VERDICT: REVISE` because the
standalone canary was not yet executable, the subplan used artifact language
where `FullChainHMCConfig` requires `use_xla=False`, and the seed was omitted.
The harness, tests, and subplan were patched. Focused re-review returned
`VERDICT: AGREE`.

## Command

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py \
  --mode phase2-canary \
  --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_canary_cpu_hidden_2026-07-06.json \
  --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_canary_cpu_hidden_2026-07-06.md \
  --num-results 2 \
  --num-burnin-steps 1 \
  --step-size 1e-5 \
  --num-leapfrog-steps 1 \
  --seed 20260706 2201
```

Quiet log:

- `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_ladder_2026-07-06/phase2_canary_cpu_hidden_2026-07-06.log`

## Local Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Compile | `PASSED` | `python -m compileall -q docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py` |
| Focused CPU-hidden pytest | `PASSED` | `CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 pytest -q tests/test_minimal_ssl_lstm_zhaocui_hmc_ladder.py` returned `6 passed`. |
| Forbidden-mechanism scan | `PASSED` | No `GradientTape`, `tf.py_function`, `import numpy`, or `np.` matches in the new harness/test or existing Zhao-Cui fixed adapter. |
| `git diff --check` | `PASSED` | Command returned exit status 0 after canary artifact generation. |
| Standalone canary command | `PASSED` | Exit status 0; JSON and Markdown artifacts written. |

## Artifact Summary

Artifacts:

- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_canary_cpu_hidden_2026-07-06.json`
- `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_canary_cpu_hidden_2026-07-06.md`

Observed diagnostics:

| Diagnostic | Value |
| --- | --- |
| Status | `passed` |
| Hard vetoes | `[]` |
| Initial log probability | `-1.3985848756201187` |
| Initial score norm | `1.624779105977436` |
| Initial score shape | `[24]` |
| HMC runtime error | `None` |
| Sample shape | `[2, 24]` |
| Samples all finite | `True` |
| Finite sample count | `2` |
| Nonfinite sample count | `0` |
| Acceptance rate | `1.0` explanatory only |
| Native divergence status | `not_exposed_by_kernel` |
| Native divergence count | `None`; not interpreted as zero divergences |
| CUDA visibility | `CUDA_VISIBLE_DEVICES=-1`; no GPU evidence claimed |

The log includes TensorFlow's CPU-hidden CUDA initialization warning. This is
not GPU evidence; the artifact records `gpu_devices: []`,
`physical_devices: ['/physical_device:CPU:0']`, and
`trust_basis: cpu_hidden_debug_no_gpu_claim`.

## Decision Table

| Field | Decision |
| --- | --- |
| Phase decision | `ADVANCE_TO_PHASE3_NO_OP_REPAIR_CLASSIFICATION` |
| Primary criterion status | `PASSED` |
| Veto diagnostic status | `NO_PHASE2_HARD_VETO_OBSERVED` |
| Main uncertainty | Tiny canary cannot assess convergence, posterior correctness, tuning adequacy, R-hat/ESS, ranking, or default readiness. |
| Next justified action | Write Phase 3 no-op repair result, then review whether Phase 4 short replicated debug ladder should launch. |
| What is not being concluded | HMC convergence, posterior correctness, R-hat/ESS, ranking, GPU/XLA readiness, default readiness, source-faithful parity, or LEDH result. |

## Inference Status

| Field | Status |
| --- | --- |
| Hard veto screen | `PASSED_FOR_TINY_CPU_HIDDEN_CANARY` |
| Statistically supported ranking | `NOT_CLAIMED` |
| Descriptive-only differences | `Acceptance rate and runtime are explanatory only.` |
| Default-readiness | `NOT_CHECKED` |
| Next evidence needed | Phase 3 no-op repair classification; optional Phase 4 short replicated debug ladder only if reviewed and still CPU-hidden/debug scoped. |

## Handoff

Phase 3 may begin as a no-op repair classification because no Phase 2 hard
veto fired. Do not treat this canary as convergence, posterior, ranking,
default-readiness, source-faithfulness, GPU/XLA, or LEDH evidence.
