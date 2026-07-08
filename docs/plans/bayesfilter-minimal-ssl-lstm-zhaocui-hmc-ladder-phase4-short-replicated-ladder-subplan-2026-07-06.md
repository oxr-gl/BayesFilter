# Phase 4 Subplan: Short Replicated Debug Ladder

Date: 2026-07-06

Status: `DRAFT_PENDING_PHASE4_HANDOFF_REVIEW`

## Phase Objective

If the CPU-hidden canary passes or is repaired, run a short replicated
CPU-hidden debug ladder over predeclared seeds to collect hard-veto and
descriptive sampler diagnostics. Phase 4 is a fixed reviewed contract, not a
parameterized ladder surface.

## Entry Conditions Inherited From Previous Phase

- Phase 3 result exists.
- The canary hard-veto screen is passed or repaired.
- Short replicated ladder remains CPU-hidden debug evidence only.

## Required Artifacts

- JSON ladder artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_short_ladder_cpu_hidden_2026-07-06.json`
- Markdown ladder artifact:
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_short_ladder_cpu_hidden_2026-07-06.md`
- Quiet logs under:
  `docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_ladder_2026-07-06/`
- Phase 4 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase4-short-replicated-ladder-result-2026-07-06.md`
- Draft/refreshed Phase 5 subplan.

## Required Checks, Tests, And Reviews

- Rerun focused tests and the canary smoke.
- Run short replicated CPU-hidden ladder only after predeclared settings are
  recorded in the artifact.
  Fixed settings are mandatory and fail closed in the harness:
  `num_results=2`, `num_burnin_steps=1`, `num_leapfrog_steps=1`,
  `step_size=1e-5`,
  `FullChainHMCConfig(..., use_xla=False, chain_execution_mode="tf_function")`.
  Fixed seeds are mandatory and fail closed in the harness:
  `(20260706, 2401)`, `(20260706, 2402)`, `(20260706, 2403)`.
- Validate hard-veto fields and inference-status table.
- `git diff --check`.
- Review Phase 4 result/Phase 5 subplan if external review is available; else
  local Codex substitute review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do several tiny CPU-hidden HMC runs avoid hard vetoes under fixed predeclared settings? |
| Baseline/comparator | Phase 2/3 canary plus identical scalar target across seeds. |
| Primary pass criterion | All predeclared seeds complete without hard vetoes and artifacts preserve evidence limits. |
| Veto diagnostics | Runtime exception, nonfinite sample, divergence if exposed and positive, invalid artifact, missing seed, changed settings after seeing results, or unsupported claim. |
| Explanatory diagnostics | Acceptance rate, runtime, finite counts, and per-seed hard-veto rows only. |
| Not concluded | HMC convergence, posterior correctness, ranking, GPU/XLA readiness, default readiness, source-faithful parity, or LEDH result. |

## Executable Harness Contract

Phase 4 must use the explicit short-ladder mode in:

`docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py`

Required command shape:

```bash
mkdir -p docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_ladder_2026-07-06
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py \
  --mode phase4-short-ladder \
  --output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_short_ladder_cpu_hidden_2026-07-06.json \
  --markdown-output docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_short_ladder_cpu_hidden_2026-07-06.md \
  > docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_ladder_2026-07-06/phase4_short_ladder_cpu_hidden_2026-07-06.log 2>&1
```

The artifact must include a row for every predeclared seed, record the quiet
log path, and must not compute or promote R-hat/ESS in this short debug
ladder.

## Forbidden Claims And Actions

- Do not rank or claim convergence from few short chains.
- Do not compute or promote R-hat/ESS in this phase.
- Do not switch settings after seeing results.
- Do not run GPU or detached execution without approval.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only when:

- Phase 4 result exists;
- hard-veto status is recorded for every predeclared seed;
- Phase 5 explicitly says whether GPU/XLA bridge is needed and requests
  approvals before launch.

## Stop Conditions

Stop if short ladder fails with a true hard veto, if more runtime would be
needed to interpret results, if claims would need stronger evidence, or if
unapproved runtime scope is required.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write Phase 4 result/close record.
3. Draft or refresh Phase 5 subplan.
4. Review Phase 5 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
