# P04 Trusted GPU 50k/100k Scale Ladder Subplan

Status: `READY_AFTER_P03`

## Phase Objective

Run the selected low-rank filter-integration route in trusted GPU context at
50k particles and conditionally 100k particles, preserving diagnostic-only
interpretation, nonmaterialized transport, and explicit evidence that the
low-rank route fired inside the filter loop.

## Entry Conditions Inherited From Previous Phase

P03 must have passed.  GPU commands must use trusted/elevated context because
GPU/CUDA evidence from a sandbox is not dispositive.  Runtime and memory remain
explanatory except for crash/OOM/timeout as hard execution vetoes.

Inherited P03 setting:

- `rank=16`
- `assignment_epsilon=0.015625`
- P03 rows `4096` and `8192` both passed.
- Each P03 row recorded low-rank invocation count `2` equal to active mask count
  `2`.

## Required Artifacts

- GPU scale JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-gpu-scale-2026-06-20.json`
- GPU scale Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-integration-gpu-scale-2026-06-20.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p04-trusted-gpu-scale-result-2026-06-20.md`
- Log:
  `docs/benchmarks/logs/low-rank-ledh-pfpf-integration-p04-gpu-scale.log`

## Required Checks, Tests, And Reviews

- Trusted/elevated GPU scale command with selected P02/P03 setting.
- Required command setting: `--rank 16 --assignment-epsilon 0.015625 --conditional-100k`.
- JSON inspection for 50k row, conditional 100k row, no dense materialization,
  finite outputs, and hard veto status.
- JSON inspection that active rows include `low_rank_resampling_invocations > 0`
  and invocation count equal to active mask count.
- Read-only Claude review of the phase result before P05 closeout if GPU scale
  produces a pass or material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the selected low-rank route survive actual filter-loop execution at 50k particles and, if 50k passes, at 100k particles in trusted GPU context? |
| Baseline/comparator | P03 selected setting and hard diagnostics; dense Sinkhorn is not attempted at scale. |
| Primary pass criterion | 50k active row proves low-rank route execution and passes all hard diagnostics under the master fixed-threshold table; 100k is attempted only if 50k passes and is recorded as pass/fail/skipped with reason. |
| Veto diagnostics | Trusted GPU unavailable, crash/OOM/timeout, missing/zero low-rank invocation evidence, invocation count mismatch, nonfinite output, invalid factors, residual threshold failure under the master fixed-threshold table, dense transport materialized, missing artifact, or unsupported claim. |
| Explanatory diagnostics | Runtime, memory, GPU visibility, TF32 status, ESS, moment deltas, projection iterations. |
| Not concluded | No speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or TF32-help claim. |
| Artifact | P04 JSON/Markdown/result/log. |

## Forbidden Claims And Actions

- Do not run non-trusted GPU evidence and treat it as machine failure.
- Do not install packages, use network, use POT, or run external solvers.
- Do not make speedup or production/default claims from this phase.
- Do not continue to public API or default changes.

## Exact Next-Phase Handoff Conditions

P05 may start after P04 writes either a pass result, a trusted-GPU-unavailable
blocker result, or a validity failure result with artifacts and non-claims.

## Stop Conditions

- `LOW_RANK_FILTER_INTEGRATION_SCALE_BLOCKED_TRUSTED_GPU_UNAVAILABLE`
- `LOW_RANK_FILTER_INTEGRATION_SCALE_FAILED_TUNING_OR_VALIDITY`
- `LOW_RANK_FILTER_INTEGRATION_SCALE_BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the P04 result/close record.
3. Draft or refresh P05 subplan.
4. Review P05 for consistency, correctness, feasibility, artifact coverage, and boundary safety.
