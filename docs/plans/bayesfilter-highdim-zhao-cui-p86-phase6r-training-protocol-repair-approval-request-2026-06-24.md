# P86 Phase 6R Approval Request: Tiny Adaptive Scheduler Smoke

Date: 2026-06-24

Status: `APPROVED_AND_EXECUTED_RECORDED_IN_PHASE6R_SMOKE_RESULT`

## Request

Approve exactly one tiny CPU-hidden training smoke to exercise the repaired
adaptive-training scheduler and trained-core serialization path. The command
uses the dedicated `--phase6r-adaptive-smoke` mode and guard; it does not reuse
the historical one-step `--training-base-smoke` guard.

Execution note: the command was approved by the user and executed on
2026-06-25 HKT. The result is recorded in
`docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-tiny-adaptive-training-smoke-result-2026-06-25.md`.

Correction note: an earlier draft of the command block in this approval request
incorrectly showed `--training-base-smoke` even though the request text, the
user-facing approval prompt, the runner guard, and the executed command all
used the dedicated `--phase6r-adaptive-smoke` mode. This file now records the
actual approved and executed command.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the repaired runner emit adaptive-training monitor records, LR-drop/stop status, and trained-core serialization fields on a tiny bounded training smoke? |
| Baseline/comparator | Phase 6R local helper tests. |
| Primary criterion | JSON is written; training executes only the tiny smoke; adaptive-training fields exist; validation trace is populated when holdout is present; trained-core serialization metadata exists; memory/runtime are within envelope. |
| Veto diagnostics | Command drift; missing validation trace; missing trained-core serialization; nonfinite diagnostics; unapproved rank-5/full-budget semantics; claiming convergence/production. |
| Explanatory diagnostics | LR events, validation residuals, stop reason, core hashes, runtime, memory. |
| Not concluded | No rank convergence, no degree convergence, no correctness, no HMC readiness, no LEDH comparison, no scale, no production readiness. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-tiny-adaptive-training-smoke-2026-06-24.json` |

## Exact Command Requiring Approval

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --phase6r-adaptive-smoke --target-dimension 36 --fit-rank 1 --training-sample-count 64 --holdout-sample-count 32 --seed 8615 --optimizer-batch-size 32 --prefit-steps 1 --train-steps 6 --learning-rate 0.001 --max-seconds 120 --memory-cap-mib 12288 --adaptive-training --validation-check-every 2 --plateau-patience 1 --plateau-min-delta 0.0 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 2 --serialize-trained-cores --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-tiny-adaptive-training-smoke-2026-06-24.json
```

## Stop Conditions

- Do not run without exact human approval.
- Stop if Claude review of the Phase 6R implementation result requests a
  material revision.
- Stop if this command would be interpreted as rank-convergence evidence.
