# P02 Tiny Actual-SIR Tuning Smoke Subplan

Status: `DRAFT_AFTER_P01`

## Phase Objective

Run the smallest actual-SIR d18 mini-grid smoke that proves tuning-grid
execution, artifact writing, route-fired diagnostics, and hard-veto evaluation
in trusted context before the material tuning screen.

## Entry Conditions Inherited From Previous Phase

P01 must pass. Harness or wrapper execution path must be chosen and locally
checked. P02 inherits the fixed gates from the master program.

## Required Artifacts

- Smoke JSON aggregate or row artifacts:
  `docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22*.json`
- Smoke Markdown aggregate or row artifacts:
  `docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22*.md`
- Log:
  `docs/benchmarks/logs/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22.log`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p02-tiny-smoke-result-2026-06-22.md`

## Required Checks/Tests/Reviews

- Run `B=1,T=3,N=128`, seed `81120`, route `both`, four-candidate bounded
  mini-grid through `docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py`.
- Exact initial command, subject to trusted GPU availability:

```bash
timeout 900 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/run_actual_sir_low_rank_tuning_grid.py \
  --mode execute \
  --num-particles 128 \
  --time-steps 3 \
  --batch-seeds 81120 \
  --low-rank-ranks 16,32 \
  --low-rank-assignment-epsilons 0.25,0.125 \
  --low-rank-max-projection-iterations-list 120 \
  --warmups 0 \
  --repeats 1 \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --tf32-mode enabled \
  --output docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22.json \
  --markdown-output docs/benchmarks/actual-sir-low-rank-tuning-p02-tiny-smoke-2026-06-22.md \
  --quiet
```

- Confirm actual-SIR semantics, finite outputs, route-fired counts, no dense
  low-rank transport materialization, factor validity, and JSON/Markdown output.
- Treat paired deltas and runtime as explanatory only in P02.
- Claude read-only review only if smoke interpretation or artifact schema is
  materially ambiguous.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the chosen tuning execution path produce valid actual-SIR artifacts on a tiny four-candidate mini-grid? |
| Baseline/comparator | Streaming and low-rank routes inside the owned validation harness. |
| Primary pass criterion | Tiny mini-grid writes artifacts and passes hard validity diagnostics for the executed routes. |
| Veto diagnostics | Nonfinite output, missing actual-SIR semantics, route-fired mismatch, dense materialization, invalid factors, missing artifact, or trusted GPU unavailable if GPU evidence is claimed. |
| Explanatory diagnostics | Paired deltas, runtime, memory, projection iterations, factor residual magnitude. |
| Not concluded | No candidate nomination, tuning success, speedup, posterior correctness, or held-out support. |
| Artifact | P02 JSON/Markdown/log/result. |

## Forbidden Claims/Actions

- Do not use P02 as promotion evidence.
- Do not continue to P03 if artifacts are missing required hard-veto fields.
- Do not change thresholds after seeing smoke results.

## Exact Next-Phase Handoff Conditions

Advance to P03 only if P02 writes complete artifacts and no hard-veto or schema
veto fires. If P02 exposes a fixable harness/schema issue, patch under P01/P02
repair loop and rerun focused checks.

## Stop Conditions

- Stop if actual-SIR semantics cannot be established.
- Stop if trusted GPU is required but unavailable and CPU-hidden smoke is
  insufficient for the next planned GPU tuning screen.
- Stop after five unresolved Claude review rounds for the same material blocker.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the P02 phase result.
3. Draft or refresh P03 with exact grid, artifact paths, and row budget.
4. Review P03 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
