# Phase 2 Subplan: CPU-Hidden HMC Canary

Date: 2026-07-06

Status: `READY_FOR_STANDALONE_CANARY_AFTER_HANDOFF_REVIEW`

## Phase Objective

Run the smallest CPU-hidden HMC canary for the scalar `zhaocui_fixed` target
adapter using BayesFilter `run_full_chain_tfp_hmc`. This phase is an explicit
CPU-hidden, non-JIT debug/reference exception unless a reviewed Phase 1 result
changes that scope.

## Entry Conditions Inherited From Previous Phase

- Phase 1 target adapter exists and passes focused value/score checks.
- The run remains CPU-hidden debug evidence.
- No convergence, posterior, ranking, GPU/XLA production, source-faithful, or
  default-readiness claim is in scope.

## Required Artifacts

- JSON canary artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_canary_cpu_hidden_2026-07-06.json`
- Markdown canary artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_canary_cpu_hidden_2026-07-06.md`
- Quiet run log under:
  `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_ladder_2026-07-06/`
- Phase 2 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase2-cpu-hidden-canary-result-2026-07-06.md`
- Draft/refreshed Phase 3 subplan.

## Required Checks, Tests, And Reviews

- Re-run focused compile/test from Phase 1.
- Run canary with CPU hidden, fixed small settings:
  `num_results=2`, `num_burnin_steps=1`, `num_leapfrog_steps=1`,
  `step_size=1e-5`, `seed=(20260706, 2201)`, and
  `FullChainHMCConfig(..., use_xla=False, chain_execution_mode="tf_function")`.
  The artifact must record `jit_compile=False`/`use_xla=False` and label this
  as a debug/reference exception, not default XLA/HMC evidence.
- Validate JSON/Markdown artifact fields and hard-veto classification.
- `git diff --check`.
- Review Phase 2 result/Phase 3 subplan if external review is available; else
  local Codex substitute review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the scalar `zhaocui_fixed` target run through the HMC machinery without hard-veto failure in a tiny CPU-hidden, non-JIT debug canary? |
| Baseline/comparator | Phase 1 adapter and existing `run_full_chain_tfp_hmc` launch-smoke pattern. |
| Primary pass criterion | Canary artifact records finite initial value/score, no HMC runtime exception, no nonfinite samples, and valid schema. |
| Veto diagnostics | Nonfinite initial value/score, HMC runtime exception, nonfinite samples, invalid artifact, wrong fixture, unsupported claim, missing debug/reference exception label, or evidence-class mismatch. |
| Explanatory diagnostics | Acceptance rate, runtime, initial score norm, sample finite counts, TensorFlow CUDA warning under CPU-hidden execution. |
| Not concluded | HMC convergence, posterior correctness, R-hat/ESS, ranking, GPU/XLA production readiness, default readiness, source-faithful parity, or LEDH result. |

## Executable Harness Contract

Phase 2 must use the explicit canary mode in:

`docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py`

Required command shape:

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

The default harness mode remains `phase1-adapter`; Phase 2 HMC execution must
be explicit via `--mode phase2-canary`.

## Forbidden Claims And Actions

- Do not interpret acceptance rate as convergence or ranking evidence.
- Do not label non-JIT/eager canary output as default XLA/HMC evidence.
- Do not compute or promote R-hat/ESS in this launch canary.
- Do not run GPU, long, detached, or external-review commands without approval.
- Do not change pass/fail criteria after seeing canary results.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only when:

- canary artifact exists;
- Phase 2 result classifies pass/fail and any hard vetoes;
- if hard vetoes are fixable, Phase 3 identifies the smallest repair;
- if no hard veto fires, Phase 3 may record no repair needed and advance.

## Stop Conditions

Stop if canary failure indicates invalid target semantics, corrupted artifact,
unapproved broader runtime need, or a fix requiring public API/model/default
policy changes.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write Phase 2 result/close record.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 3 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
