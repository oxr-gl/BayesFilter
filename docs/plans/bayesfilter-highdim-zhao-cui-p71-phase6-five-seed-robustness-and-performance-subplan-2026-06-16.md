# P71 Phase 6 Subplan: Five-Seed Robustness And Performance

metadata_date: 2026-06-16
status: DRAFT_PENDING_PHASE5_RESULT
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 6

## Phase Objective

Repeat the admitted d18 validation on five fixed seeds and record robustness,
Monte Carlo uncertainty, runtime, and memory.

## Entry Conditions Inherited From Previous Phase

- Phase 5 passed the reference accuracy gate for one admitted d18
  configuration.
- Phase 5 preserved the exact command template, thresholds, and branch identity.

## Required Artifacts

- Phase 6 result note.
- Five-seed JSON/CSV artifact.
- Run manifest with seeds, commands, environment, CPU/GPU status, wall time,
  memory, output paths, and git commit.
- Frozen seed, device, and resource-budget table copied into the result before
  execution.
- Refreshed Phase 7 value-gradient/HMC subplan.

## Required Checks/Tests/Reviews

- Run each seed with the same frozen configuration.
- Report per-seed results, average, spread, and veto diagnostics.
- GPU commands, if any, must run with trusted/escalated permissions.
- Claude read-only review of robustness interpretation.

## Frozen Seeds, Device Class, And Budgets

The first reviewed P71 five-seed gate uses these seeds unless Phase 5 writes a
reviewed replacement before seeing Phase 6 outputs:

- `7101`;
- `7102`;
- `7103`;
- `7104`;
- `7105`.

The default device class is trusted GPU if Phase 5's admitted command is GPU
eligible; otherwise trusted CPU-only with `CUDA_VISIBLE_DEVICES=-1` set before
framework import.  The result must record the actual device class and must not
compare CPU and GPU timings as if they were the same budget.

Initial resource budget hypotheses:

- per-seed wall-time budget: 60 minutes;
- full five-seed wall-time budget: 6 hours;
- peak GPU memory budget, if GPU is used: 20 GiB;
- peak host memory budget: 64 GiB.

If these budgets are infeasible, Phase 6 must write a blocker or a revised
reviewed subplan before execution.  They must not be relaxed after seeing run
outputs.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the admitted d18 result robust over five fixed seeds with acceptable runtime and memory? |
| Baseline/comparator | Phase 5 admitted configuration and reference/comparator, repeated on seeds `7101` through `7105` unless Phase 5 writes a reviewed replacement before seeing Phase 6 outputs. |
| Primary criterion | All five seeds pass veto diagnostics and accuracy thresholds; the average and seed spread are reported and remain within the Phase 5-predeclared accuracy tolerance and the resource budgets above. |
| Veto diagnostics | Any seed nonfinite, any seed fails source invariants, any seed fails accuracy, seed spread too large, GPU sandbox failure treated as trusted, CPU/GPU budget mixing, or runtime/memory exceeding the predeclared budget. |
| Explanatory diagnostics | Per-seed errors, averages, intervals/spread, ESS, correction ranges, wall time, memory, CPU/GPU device status. |
| Not concluded | No d50/d100 scaling, no HMC production readiness, no default-policy change. |
| Artifact | Phase 6 result note plus five-seed artifact. |

## Forbidden Claims/Actions

- Do not use the average to hide a failed seed.
- Do not change the particle/sample/rank/degree policy after seeing seed
  outputs.
- Do not change the seed list, device class, or resource budgets after seeing
  outputs.
- Do not extrapolate to higher dimensions.

## Exact Next-Phase Handoff Conditions

Phase 7 may begin only if all five seeds pass and Phase 6 identifies the exact
value path and variables eligible for gradient/HMC diagnostics.

## Stop Conditions

Stop if any seed fails a veto diagnostic, if runtime/memory is infeasible, or
if trusted GPU evidence is unavailable for GPU claims.
