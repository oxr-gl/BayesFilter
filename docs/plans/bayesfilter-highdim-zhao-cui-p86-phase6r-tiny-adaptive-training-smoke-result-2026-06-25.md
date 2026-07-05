# P86 Phase 6R Result: Tiny Adaptive Training Smoke

Date: 2026-06-25

Status: `PASS_P86_PHASE6R_TINY_ADAPTIVE_TRAINING_SMOKE_REVIEWED`

## Current Decision

The exact approved CPU-hidden Phase 6R adaptive scheduler smoke executed and
wrote the expected JSON artifact:

`docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-tiny-adaptive-training-smoke-2026-06-24.json`

This is a scheduler/mechanics smoke only. It exercises adaptive-training
monitoring, LR reduction on validation plateau, early-stop status, and
trained-core serialization. It does not repair the old rank-5 comparator, does
not establish rank convergence, and does not promote Zhao-Cui SIR to
production.

## Exact Command Executed

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --phase6r-adaptive-smoke --target-dimension 36 --fit-rank 1 --training-sample-count 64 --holdout-sample-count 32 --seed 8615 --optimizer-batch-size 32 --prefit-steps 1 --train-steps 6 --learning-rate 0.001 --max-seconds 120 --memory-cap-mib 12288 --adaptive-training --validation-check-every 2 --plateau-patience 1 --plateau-min-delta 0.0 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 2 --serialize-trained-cores --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-tiny-adaptive-training-smoke-2026-06-24.json
```

The command was user-approved on 2026-06-25 HKT. It intentionally used
`CUDA_VISIBLE_DEVICES=-1`; TensorFlow emitted CUDA initialization chatter, but
the artifact records `intentional_gpu_hiding=true` and
`cuda_visible_devices=-1`.

## Decision Table

| Field | Status |
|---|---|
| Decision | Tiny adaptive scheduler smoke passed locally. |
| Primary criterion status | Passed: artifact written; status completed; validation trace populated; adaptive summary populated; trained cores serialized with values; runtime and memory inside envelope. |
| Veto diagnostic status | No fallback route; no audit-cloud tuning; ALS remains demoted; finite diagnostics; exact command matched the guarded `--phase6r-adaptive-smoke` mode. |
| Main uncertainty | Full rank-5 adaptive rerun has not been preflighted, approved, or executed under the repaired protocol. |
| Next justified action | Claude read-only bounded review of this result, then draft a separate adaptive rank-5 preflight/guard subplan. |
| What is not being concluded | No rank convergence, degree convergence, posterior correctness, KR closure, HMC readiness, LEDH comparison, scale, GPU performance, source-faithful TT-cross training, production readiness, or default-policy change. |

## Evidence Contract Check

| Contract item | Result |
|---|---|
| Question | Does the repaired runner emit adaptive-training monitor records, LR-drop/stop status, and trained-core serialization fields on a tiny bounded training smoke? |
| Baseline/comparator | Phase 6R local helper tests and the frozen guarded smoke command. |
| Primary criterion | Passed locally. JSON status is `P86_PHASE6R_ADAPTIVE_TRAINING_SMOKE_COMPLETED`; `training_executed=true`; `training_base_smoke_executed=true`; `fit_executed=false`; `smoke_kind=phase6r_adaptive_training_scheduler_smoke`. |
| Veto diagnostics | Passed: no command drift, validation trace length is 3, trained-core serialization status is `serialized_with_values`, finite diagnostics, no fallback, no audit tuning, memory/runtime within envelope. |
| Explanatory diagnostics | Runtime `5.3059792580024805` seconds; peak memory `609.0703125` MiB; fit residual `0.18177395138366628`; holdout residual `1.6408980086114933`; normalizer `0.011578465512630112`. |
| Not concluded | The smoke is not rank-convergence evidence and does not authorize a rank-5/full-budget rerun. |
| Artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-tiny-adaptive-training-smoke-2026-06-24.json` |

## Artifact Validation Summary

The post-run validator checked the saved JSON, not only stdout.

Key fields:

- `status`: `P86_PHASE6R_ADAPTIVE_TRAINING_SMOKE_COMPLETED`
- `schema_version`: `p86_phase6r_adaptive_training_smoke.v1`
- `smoke_kind`: `phase6r_adaptive_training_scheduler_smoke`
- `training_backend`: `training_base_optimizer`
- `validation_trace_len`: `3`
- `training_trace_len`: `3`
- `trained_core_serialization.status`: `serialized_with_values`
- `trained_core_serialization.core_count`: `36`
- `trained_core_serialization.total_values`: `1188`
- `trained_core_serialization.global_sha256`:
  `109a2b61578115a80166642d36be95fc5ab348e9eb4967f342cf084fd49ac9fd`

Adaptive summary:

- best monitor value: `1.639875696842547` at step `2`
- LR events:
  - `monitor_improved` at step `2`, LR `0.001`
  - `learning_rate_reduced_on_plateau` at step `4`, LR `0.0005`
  - `learning_rate_reduced_on_plateau` at step `6`, LR `0.00025`
- stop reason: `early_stop_after_plateau_lr_drop_limit`
- `lr_drop_count`: `2`

Training convergence payload:

```text
status=scheduler_stopped_after_plateau
adaptive_training=true
completed_steps=6
requested_steps=6
stop_reason=early_stop_after_plateau_lr_drop_limit
loss_still_improving_at_stop=true
convergence_claim_allowed=true
```

Interpretation discipline: this convergence payload is valid only for the tiny
scheduler smoke mechanics. It is not a rank-convergence or production gate.

## Boundary-Safety Patch During Closeout

While closing the smoke, Codex found and patched one guard gap: old exact
`--fit` command guards checked rank/sample/seed fields but did not reject extra
adaptive-training flags. The runner now includes adaptive-training protocol
fields in exact-fit argument expectations, so the historical fixed-budget
Phase 5/Phase 6 commands cannot silently run with protocol drift.

Changed files:

- `scripts/p86_author_lagrangep_phase5_budget_fit.py`
- `tests/highdim/test_p86_phase5_budget_preflight.py`

The smoke approval request was also corrected to show the actual
`--phase6r-adaptive-smoke` command. The earlier approval-request draft had a
stale `--training-base-smoke` token in the command block, while the request
text, user-facing approval prompt, runner guard, and executed artifact used the
dedicated Phase 6R smoke mode.

## Local Checks

Commands:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py tests/highdim/test_p86_author_lagrangep_fit_smoke_runner.py tests/highdim/test_p86_downstream_author_route_wiring.py tests/highdim/test_p86_lagrangep_mass_integral.py tests/highdim/test_p86_algebraic_measure_contract.py
```

Result:

```text
37 passed, 2 warnings
```

## Next Handoff

If Claude agrees with this closeout, the next phase should not run rank 5
immediately. It should first create a dedicated adaptive rank-5 preflight/guard
subplan that:

- freezes a new exact adaptive rank-5 command and output path;
- records validation-monitor policy, LR schedule, early-stop rule, and trained
  core serialization;
- updates exact-fit guards so the artifact command and executed optimizer
  protocol cannot diverge;
- requires focused tests and Claude review before exact human approval for the
  long rank-5 rerun;
- preserves that audit cloud is not used for tuning and that validation loss is
  a veto/monitor signal, not a production criterion.

## Claude Review Status

Claude read-only bounded review returned `VERDICT: AGREE`.

Review prompt:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the file itself explicitly asks you to inspect a cited line: docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-tiny-adaptive-training-smoke-result-2026-06-25.md. Do not edit, run commands, launch agents, or review the whole repo. Question: Does this Phase 6R tiny adaptive-training smoke result safely record the exact approved CPU-hidden scheduler smoke, correctly validate adaptive monitor/LR-drop/stop/core-serialization evidence, preserve the boundary that this is not rank convergence or production promotion, disclose the stale approval-command correction, and make a safe next-phase handoff to an adaptive rank-5 preflight/guard subplan before any long rerun approval? End with VERDICT: AGREE or VERDICT: REVISE.
```

Summary:

- Claude agreed the file records the exact approved CPU-hidden scheduler smoke.
- Claude agreed the adaptive monitor, LR-drop, stop-reason, and
  core-serialization evidence are tied to the saved JSON artifact.
- Claude agreed the result preserves the boundary that this is not rank
  convergence, not a repaired comparator, and not production/default
  promotion.
- Claude agreed the stale approval-command correction is disclosed.
- Claude agreed the next-phase handoff remains gated through a separate
  adaptive rank-5 preflight/guard subplan, focused tests, review, and human
  approval.

Verdict:

```text
VERDICT: AGREE
```
