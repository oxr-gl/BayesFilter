# P86 Phase 6S Approval Request: Adaptive Rank-5 Rerun

Date: 2026-06-25

Status: `APPROVED_AND_EXECUTED_RECORDED_IN_PHASE6S_FIT_RESULT`

## Request

The Phase 6S preflight/guard result passed Claude review. The user approved
exactly one CPU-hidden adaptive rank-5 same-route comparator rerun, and Codex
executed the command on 2026-06-25 HKT. This command is the first repaired
replacement for the undertrained/protocol-incomplete fixed-step Phase 6 rank-5
comparator.

Execution result:

- Fit artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json`
- Fit result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-adaptive-rank5-fit-result-2026-06-25.md`
- Convergence result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank-convergence-result-2026-06-25.md`

The run produced a mechanically admissible adaptive rank-5 artifact after a
classifier repair, but rank convergence remains blocked because rank-5 holdout
residual is much worse than rank 4.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the same-route rank-5 comparator train under the repaired adaptive scheduler without fixed-budget exhaustion and with replayable trained cores? |
| Baseline/comparator | Baseline is the Phase 5 rank-4 training-base artifact; diagnostic predecessor is the old fixed-budget rank-5 artifact, treated as undertrained/protocol-incomplete. |
| Primary criterion | The command writes the Phase 6S fit JSON; adaptive training executes; validation trace is populated; stop/convergence status is explicit; trained cores are serialized; no fallback/audit tuning; finite diagnostics; memory/runtime inside envelope. |
| Veto diagnostics | Command drift; no scheduler/validation trace; max-step exhaustion with still-improving loss; missing trained-core serialization; audit cloud used for tuning; nonfinite loss/residual/normalizer; memory/runtime breach; claiming rank convergence from the fit alone. |
| Explanatory diagnostics | LR events, validation residuals, fit/holdout residuals, normalizers, core hashes/values, runtime, memory, and training trace. |
| Not concluded | No rank convergence until a later reviewed convergence ledger compares lower and stronger rungs; no degree convergence, posterior correctness, KR closure, HMC readiness, LEDH comparison, scale, GPU performance, source-faithful TT-cross training, production readiness, or default-policy change. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json` |

## Exact Command Requiring Approval

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-preflight-2026-06-25.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 1024 --learning-rate 0.001 --max-seconds 14400 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json
```

## Stop Conditions

- Stop if exact human approval for the command above is unavailable.
- Stop if the command would be interpreted as production, correctness, HMC,
  LEDH, GPU, or source-faithful TT-cross evidence.
- Stop after the run if the artifact status is blocked or if scheduler
  diagnostics show max-step exhaustion while still improving; write a blocker
  rather than ranking configurations.
