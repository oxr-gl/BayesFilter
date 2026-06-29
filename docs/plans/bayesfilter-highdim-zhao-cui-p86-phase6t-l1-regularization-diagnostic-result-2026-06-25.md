# P86 Phase 6T Result: L1 Regularization Diagnostic Fit

Date: 2026-06-25

Status: `P86_PHASE6T_L1_REGULARIZATION_DIAGNOSTIC_PROMISING_REVIEWED`

## Current Decision

The approved Phase 6T single diagnostic fit completed and materially improved
the rank-5 training-base result relative to the failed Phase 6S adaptive rank-5
artifact.

This is a promising diagnostic for the hypothesis that the prior rank-5
failure was optimizer/regularization pathology rather than a simple
rank-capacity failure. It is not yet a production promotion, not a final rank
convergence ledger, and not a tuned hyperparameter selection.

## Decision Table

| Field | Status |
|---|---|
| Decision | Phase 6T diagnostic passed mechanically and produced a much better rank-5 artifact. |
| Primary criterion status | Passed for diagnostic purpose: holdout residual improved from Phase 6S rank-5 `9.553783177487691` to `0.03973471699747935`; normalizer recovered from `4.038658791921966e-08` to `1.0017186484259596e-05`. |
| Veto diagnostic status | No runtime/memory breach, no nonfinite diagnostics, no audit tuning, no ALS route, trained cores serialized, exact command matched preflight. |
| Main uncertainty | Single regularized rank-5 diagnostic; not multi-seed, not a full grid, not a final convergence/selection ledger, and not audited for downstream computation. |
| Next justified action | Claude review of this result, then a separate reviewed Phase 6U convergence/selection subplan before reopening Phase 7. |
| What is not being concluded | No production readiness, no final rank convergence, no posterior correctness, no KR closure, no HMC readiness, no LEDH comparison, no GPU performance, and no source-faithful TT-cross training claim. |

## Evidence Contract Check

| Field | Result |
|---|---|
| Question | Does the approved lower-LR/L1 diagnostic improve rank-5 validation/holdout/normalizer behavior without audit tuning? |
| Baseline/comparator | Reviewed rank-4 Phase 5 lower rung and reviewed Phase 6S adaptive rank-5 failure. |
| Primary diagnostic criterion | Passed: Phase 6T rank-5 holdout residual is `0.004159055764538314x` Phase 6S rank-5 and `0.1798684272396982x` rank 4. |
| Veto diagnostics | Passed mechanically: completed status, finite residuals/normalizers/loss, memory/runtime within cap, audit not used for tuning, ALS not used, trained cores serialized. |
| Explanatory diagnostics | Validation best remained at step 16, but deterioration was shallow rather than explosive; scheduler stopped at step 272 after four LR drops. |
| Not concluded | This does not by itself establish a final rank-convergence gate or production readiness. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-diagnostic-2026-06-25.json` |

## Comparator Table

| Field | Rank 4 lower rung | Phase 6S adaptive rank 5 | Phase 6T L1 rank 5 |
|---|---:|---:|---:|
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase5-budget-compliant-fit-2026-06-24.json` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json` | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-diagnostic-2026-06-25.json` |
| Status | `P86_PHASE5_BUDGET_COMPLIANT_TRAINING_BASE_COMPLETED` | raw `BLOCK_P86_PHASE6S_ADAPTIVE_RANK5_COMPARATOR_TRAINING_BASE` | `P86_PHASE6T_L1_REGULARIZATION_TUNING_DIAGNOSTIC_TRAINING_BASE_COMPLETED` |
| Rank | `4` | `5` | `5` |
| Learning rate | `0.001` | `0.001` | `0.0003` |
| L1 weight | historical default/no payload field | historical default/no payload field | `1e-09` |
| L2 weight | `1e-08` | `1e-08` | `1e-08` |
| LogZ anchor weight | `0.0` | `0.0` | `0.0` |
| Completed train steps | `89 / 89` | `272 / 1024` | `272 / 512` |
| Stop reason | `optimizer_steps_completed` | `early_stop_after_plateau_lr_drop_limit` | `early_stop_after_plateau_lr_drop_limit` |
| Fit residual | `0.22022907890919044` | `9.625018868846658` | `0.040245088500475236` |
| Holdout residual | `0.22090990401849483` | `9.553783177487691` | `0.03973471699747935` |
| Normalizer | `1.696098696075702e-06` | `4.038658791921966e-08` | `1.0017186484259596e-05` |
| Runtime seconds | `56.53906785399886` | `250.7143890260195` | `230.8402821199852` |
| Peak memory MiB | `2173.27734375` | `3082.3125` | `3084.953125` |

## Ratios

- Phase 6T holdout / Phase 6S holdout: `0.004159055764538314`
- Phase 6T holdout / rank-4 holdout: `0.1798684272396982`
- Phase 6T fit / Phase 6S fit: `0.004181299699134793`
- Phase 6T fit / rank-4 fit: `0.18274193716747983`
- Phase 6T normalizer / Phase 6S normalizer: `248.03250287683983`
- Phase 6T normalizer / rank-4 normalizer: `5.906016263933558`

## Validation Trace Interpretation

Phase 6S validation residual exploded:

```text
step 16: 0.030539674365849725
step 80: 0.26672687719411875
step 144: 1.6010281454417215
step 208: 5.083282362733053
step 272: 9.553783177487691
```

Phase 6T validation residual stayed close to the early best:

```text
step 16: 0.027721343609222935
step 80: 0.03241314768767047
step 144: 0.03744206449615727
step 208: 0.03909920645142353
step 272: 0.03973471699747935
```

The best validation residual for Phase 6T was still at step 16. That means the
run remains a training-dynamics diagnostic rather than proof that the schedule
is globally tuned. The important difference is that the validation degradation
was shallow and the final holdout residual remained far below both the Phase 6S
rank-5 failure and the rank-4 lower rung.

## Exact Command

Approved and run:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-preflight-2026-06-25.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.000000001 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-diagnostic-2026-06-25.json
```

Runner output:

```text
{"fit_executed": true, "p86_status": "P86_PHASE6T_L1_REGULARIZATION_TUNING_DIAGNOSTIC_TRAINING_BASE_COMPLETED"}
```

## Mechanical Checks

- Exact command matched the preflight `candidate_fit_command`: `true`
- Preflight status:
  `P86_PHASE6T_L1_REGULARIZATION_TUNING_PREFLIGHT_READY_NOT_FIT`
- Post-fit finite loss status: `ok`
- Post-fit finite normalizer status: `ok`
- Post-fit finite holdout residual status: `ok`
- Fallback route status: `not_used`
- Audit cloud tuning status: `not_used_for_tuning`
- ALS training status:
  `historical_buggy_stale_route_not_allowed_for_fixed_variant_zhao_cui_training`
- Runtime status: `within_approved_envelope`
- Memory status: `within_approved_envelope`
- Trained core serialization: `serialized_with_values`

## Runtime Note

The command was intentionally CPU-hidden with `CUDA_VISIBLE_DEVICES=-1` and
`MPLCONFIGDIR=/tmp`. TensorFlow emitted CUDA factory/cuInit log noise despite
intentional GPU hiding. This artifact is not GPU evidence.

## Interpretation

Phase 6T supports the hypothesis that Phase 6S rank-5 failed because the
training route was under-regularized or too aggressive at LR `0.001`, with
normalizer collapse and runaway validation residuals. Lower LR plus a small L1
penalty produced a much healthier rank-5 artifact in this single diagnostic.

This does not yet close Phase 6. A fair promotion path now needs a reviewed
Phase 6U convergence/selection subplan that decides whether to:

- replicate the Phase 6T diagnostic across seeds;
- compare `l1_weight=0` at LR `0.0003` against `l1_weight=1e-9`;
- test nearby L1 values from the preflight grid;
- decide whether rank-5 regularized training is stable enough to reopen the
  rank/degree convergence gate.

## Claude Review Status

Claude read-only bounded review returned `VERDICT: AGREE`.

Review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-diagnostic-result-2026-06-25.md. Do not edit, run commands, launch agents, or review the whole repo. Question: Does this Phase 6T diagnostic result correctly record the approved run, compare rank 4 / Phase 6S rank 5 / Phase 6T L1 rank 5, interpret the large improvement as promising diagnostic evidence rather than final rank convergence or production readiness, preserve audit-cloud non-tuning and ALS exclusion, disclose CPU-hidden non-GPU posture, and hand off safely to a Phase 6U convergence/selection subplan before reopening Phase 7? End with VERDICT: AGREE or VERDICT: REVISE.
```

Summary:

- Claude agreed the approved run and exact command are recorded correctly.
- Claude agreed the rank-4 / Phase 6S rank-5 / Phase 6T L1 rank-5 comparison
  is present.
- Claude agreed the result interprets the improvement as promising diagnostic
  evidence, not final rank convergence or production readiness.
- Claude agreed audit-cloud non-tuning, ALS exclusion, CPU-hidden non-GPU
  posture, and Phase 6U handoff are preserved.

Verdict:

```text
VERDICT: AGREE
```
