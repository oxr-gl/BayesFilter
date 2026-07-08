# Phase 4 Result: Material SIR Gradient Diagnostic

Date: 2026-06-30

Status: `BLOCKED_EXIT137_MEMORY`

## Decision

Phase 4 did not produce a complete material SIR gradient classification.  The
GPU/XLA/TF32 route launched correctly, but both monolithic material attempts
were killed with exit code 137 before the full budget ladder could complete.

This is a runtime/memory blocker, not a route wiring failure and not a
completed gradient result.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Not answered; complete JSON/Markdown artifact was not produced. |
| Baseline/comparator | Preserved in attempted commands: same seeds, theta, FD offsets, route, and budgets. |
| Primary criterion | Not applicable because the run did not complete all candidate budgets. |
| Veto diagnostics | Exit code 137 during budget 100 vetoes Phase 4 promotion. |
| Explanatory diagnostics | Partial budget-10 progress was captured. |
| Not concluded | No SIR gradient correctness, HMC readiness, posterior correctness, production budget, or nonlinear-model generalization. |

## Commands Attempted

Original reviewed wrapper:

```bash
bash scripts/run_sir_gradient_phase4_material_diagnostic.sh
```

Route facts observed before the first exit-137 kill:

- TensorFlow created GPU device `/device:GPU:0` on NVIDIA GeForce RTX 4080
  SUPER.
- XLA service initialized for CUDA.
- XLA compiled the manual route cluster.
- Budget 10 completed and budget 100 started.

First partial progress:

- budget 10 `max_row_residual`: `1.4185905456542969e-05`
- budget 10 `max_abs_fd_z`: `441.06424461688147`

Repaired wrapper:

```bash
bash scripts/run_sir_gradient_phase4_material_diagnostic.sh
```

Repair before rerun:

- Added `--seed-microbatch-size 1`.
- Added `--theta-offset-batch-size 2`.
- Claude reviewed the wrapper/subplan pair and returned `VERDICT: AGREE`.
- Codex traced the local code and verified that seed microbatching and theta
  offset batching preserve the same fixed seeds, theta rows, regression
  offsets, and averaging/gate definitions.

Second partial progress:

- budget 10 completed;
- budget 100 started;
- process memory rose to approximately 41 GB RSS with host memory and swap
  essentially exhausted;
- process was killed with exit code 137.

Progress artifact after second attempt:

```json
{
  "completed": [
    {
      "max_abs_fd_z": 362.54378733987676,
      "max_row_residual": 1.4722347259521484e-05,
      "steps": 10
    }
  ],
  "elapsed_seconds": 2012.1867197409738,
  "stage": "budget_started",
  "steps": 100
}
```

## Interpretation

The Phase 4 route gate is no longer the active blocker: trusted GPU execution,
CUDA/XLA initialization, and XLA compilation all occurred.  The active blocker
is peak memory accumulation in the monolithic budget ladder process.

The two budget-10 partial records are not sufficient to classify the SIR
gradient.  They do, however, warn that a small streaming row residual by itself
does not remove the observed gradient/FD discrepancy at the low budget:

- row residual was about `1.4e-05`, below the declared `1e-3` row threshold;
- max FD z remained very large at budget 10.

That warning is explanatory only until a complete per-budget artifact exists.

## Root-Cause Hypothesis For The Blocker

The diagnostic accumulates substantial TensorFlow/XLA memory across budget
contexts and FD evaluations in one Python process.  Even seed and theta-offset
chunking did not prevent peak host memory/swap exhaustion.  The smallest next
repair is to isolate budgets into separate Python processes and then aggregate
the per-budget JSON/Markdown artifacts under the frozen Phase 1 gate.

## Phase 4 Gate

Phase 4 gate: `BLOCKED`.

Reason:

- `BLOCKED_EXIT137_MEMORY_DURING_BUDGET100`

## Next Handoff

Advance to Phase 5 with a focused per-budget process-isolation repair:

- run one candidate budget per trusted GPU process;
- preserve the same seeds, theta, FD offsets, route prerequisites, and Phase 1
  gate;
- start with budgets 10 and 100 before attempting 200 or 400;
- aggregate only completed per-budget artifacts;
- keep budget-10 partial evidence explanatory unless regenerated as a complete
  per-budget artifact.
