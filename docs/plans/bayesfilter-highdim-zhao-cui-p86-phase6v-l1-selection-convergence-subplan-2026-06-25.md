# P86 Phase 6V Subplan: L1 Selection And Convergence Reentry

Date: 2026-06-25

Status: `REVIEWED_READY_FOR_NO_FIT_IMPLEMENTATION`

## Phase Objective

Create a reviewed, exact-guarded Phase 6V selection gate under the Zhao-Cui
training-base default policy:

```text
L1 regularization with explicit L1 weight tuning is the default Zhao-Cui
training-base procedure.
```

Phase 6V must decide whether the regularized rank-5 result is stable enough to
reopen the Phase 6 rank/degree convergence path. It may implement a no-fit
multi-arm preflight/guard and, after exact human approval, run a bounded
rank-5 L1-selection comparison. It must not jump directly to Phase 7.

## Entry Conditions Inherited From Previous Phase

- Phase 6S rank convergence is reviewed blocked:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank-convergence-result-2026-06-25.md`.
- Phase 6T L1 diagnostic is reviewed promising, not final:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-diagnostic-result-2026-06-25.md`.
- Phase 6U policy is reviewed:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6u-l1-default-policy-result-2026-06-25.md`.
- `DEFAULT_L1_WEIGHT` remains `0.0`; `l1_weight=0.0` remains a comparator arm.
- Phase 6T's `l1_weight=1e-9` artifact may be reused as one rank-5 candidate
  if command, route, seeds, sample clouds, optimizer, and validation/audit
  roles match the Phase 6V preflight.
- ALS training remains historical/buggy/stale and must not be revived.
- No exact human approval exists yet for any new Phase 6V fitting command.

## Skeptical Plan Audit

Potential flaws checked before execution:

- Wrong baseline: Phase 6V must compare rank-5 L1 candidates under the same
  route, target, basis, domain, rank, optimizer, sample-cloud roles, and LR
  schedule. The old rank-4 artifact is context, not a same-policy
  rank-convergence proof because it used a different training policy.
- Proxy promotion: validation/holdout residual may select or veto rank-5 L1
  candidates. It cannot establish posterior correctness, HMC readiness, KR
  closure, production readiness, or source-faithful TT-cross training.
- Missing stop conditions: Phase 6V stops before fitting unless a reviewed
  preflight exists and the user approves the exact candidate commands.
- Unfair comparisons: rank-5 L1 candidates must use identical seeds/cloud
  roles and differ only in `l1_weight`, except for the already reviewed
  Phase 6T reuse arm whose command must match the Phase 6V protocol.
- Hidden assumptions: if `l1_weight=0.0` at LR `0.0003` performs as well as
  L1-positive arms, Phase 6T's improvement may be mostly LR/schedule-driven;
  L1 tuning remains the default procedure, but a positive scalar cannot be
  declared necessary from this phase.
- Environment mismatch: all planned fits are CPU-hidden local diagnostics.
  They are not GPU, XLA-GPU, scale, or production evidence.
- Artifact mismatch: a selection result without exact commands, selected-arm
  rationale, validation/audit separation, nonclaim boundaries, and a next
  rank-convergence handoff cannot reopen Phase 6.

Audit result: proceed with a no-fit preflight/guard implementation and review
first. Do not run any new fitting command until exact human approval is given.

## Required Artifacts

- Phase 6V subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-subplan-2026-06-25.md`
- Phase 6V no-fit preflight JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-2026-06-25.json`
- Phase 6V no-fit preflight/guard implementation result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-guard-result-2026-06-25.md`
- Phase 6V candidate outputs:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-0-fit-2026-06-25.json`
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-3e-10-fit-2026-06-25.json`
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-diagnostic-2026-06-25.json`
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-3e-9-fit-2026-06-25.json`
- Phase 6V approval request, before any new fit:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-approval-request-2026-06-25.md`
- Phase 6V selection/convergence ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-ledger-2026-06-25.json`
- Phase 6V result / close record:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-result-2026-06-25.md`
- Refreshed next subplan or blocker handoff.
- Updated Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md`
- Updated visible execution ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md`

## Required Checks / Tests / Reviews

Before any fit:

- Add a `--phase6v-l1-selection-preflight` runner mode that writes a no-fit
  multi-arm preflight.
- Freeze Phase 6V candidate arms:
  - rank `5`;
  - target dimension `36`;
  - training samples `567600`;
  - holdout samples `65536`;
  - audit samples `65536`, reserved and not used for tuning;
  - seed `8606`;
  - optimizer `training_base_optimizer` / Adam;
  - batch size `4096`;
  - train steps `512`;
  - learning rate `0.0003`;
  - adaptive scheduler:
    `validation_check_every=16`, `plateau_patience=4`,
    `plateau_min_delta=1e-6`, `lr_reduction_factor=0.5`,
    `min_learning_rate=1e-6`, `early_stop_after_lr_drops=4`;
  - `l2_weight=1e-8`;
  - `logz_anchor_weight=0.0`;
  - serialized trained cores;
  - train/holdout/audit seeds:
    `8301/8401`, `9301/9401`, `9311/9501`.
- Candidate arms:
  - `l1_weight=0.0`;
  - `l1_weight=3e-10`;
  - `l1_weight=1e-9`, reused from the reviewed Phase 6T artifact if exact
    protocol checks pass;
  - `l1_weight=3e-9`.
- Preserve `l1_weight=0.0` as a comparator arm, not as a scalar default
  promotion.
- Add focused P86 tests for:
  - Phase 6V preflight command is frozen;
  - Phase 6V new-arm candidate commands are frozen for arms A, B, and D;
  - Phase 6V preflight records default L1-tuning policy, candidate arms,
    audit non-tuning, and Phase 6T reuse status;
  - exact guard accepts each new-arm candidate command;
  - reuse-arm validation accepts the Phase 6T `l1_weight=1e-9` artifact only
    when the artifact status, command, route, rank, target dimension,
    train/holdout/audit sample counts, optimizer, LR, L1/L2/logZ weights,
    train/holdout/audit seeds, adaptive scheduler, serialization status,
    validation/audit roles, and nonclaim boundaries match the Phase 6V
    frozen protocol;
  - exact guard rejects drift in output path, preflight path, rank, samples,
    LR, L1/L2/logZ weights, seeds, adaptive scheduler, and serialization.
- Run CPU-hidden local checks:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p86_phase5_budget_preflight.py
git diff --check -- scripts/p86_author_lagrangep_phase5_budget_fit.py tests/highdim/test_p86_phase5_budget_preflight.py docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-convergence-subplan-2026-06-25.md docs/plans/bayesfilter-highdim-zhao-cui-p86-claude-review-ledger-2026-06-24.md docs/plans/bayesfilter-highdim-zhao-cui-p86-visible-execution-ledger-2026-06-24.md
```

- Claude read-only bounded review is required on this subplan before
  implementation.
- Claude read-only bounded review is required on the no-fit implementation
  result
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-guard-result-2026-06-25.md`
  before requesting exact fitting approval.
- After approved fits complete, Claude read-only bounded review is required on
  the Phase 6V result.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Under the reviewed Zhao-Cui L1-tuning default procedure, is rank-5 training stable enough to reopen Phase 6 rank/degree convergence work? |
| Baseline/comparator | Reviewed Phase 6S rank-5 failure, reviewed Phase 6T `l1_weight=1e-9` diagnostic, and new same-LR rank-5 L1 comparator arms. The Phase 5 rank-4 artifact is historical context only for this phase. |
| Primary criterion | A selected rank-5 L1 arm must complete mechanically, preserve route/backend/cloud roles, have finite fit/holdout/normalizer diagnostics, pass veto checks, and keep final holdout residual below `0.5 * 0.22090990401849483`. Selection is lexicographic after vetoes: lowest final holdout residual wins only if it improves over `l1_weight=0.0` by at least `max(0.005, 0.05 * zero_l1_holdout)`. If no positive-L1 arm meets that margin and the zero-L1 arm passes all vetoes, select the zero-L1 comparator as the Phase 6V candidate while preserving L1 tuning as the default procedure. If no arm passes the holdout threshold and vetoes, Phase 6V blocks. |
| Veto diagnostics | Exact-command drift, nonfinite objective/residual/normalizer, fallback route, audit cloud used for tuning, runtime/memory breach, validation blow-up pattern comparable to Phase 6S, selected-arm final holdout worse than twice its best validation check, unsupported rank-convergence/production/HMC/source-faithful TT-cross claim, or missing Claude/human approval boundary. |
| Explanatory diagnostics | Training trace, validation trace, best/final validation ratio, normalizer path, regularization term, runtime/memory, comparison to rank-4 context, and whether the winning difference appears LR-only or L1-positive. |
| Not concluded | No final rank convergence, no degree convergence, no posterior correctness, no KR closure, no HMC readiness, no LEDH comparison, no GPU performance, no d50/d100 scale claim, no production readiness, and no source-faithful TT-cross training claim. |
| Artifact | Phase 6V preflight, candidate JSON outputs, selection/convergence ledger, result record, Claude review ledger, and execution ledger. |

## Candidate Commands To Freeze

No-fit preflight:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --phase6v-l1-selection-preflight --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-2026-06-25.json
```

New fit arm A, `l1_weight=0.0`:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-2026-06-25.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-0-fit-2026-06-25.json
```

New fit arm B, `l1_weight=3e-10`:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-2026-06-25.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.0000000003 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-3e-10-fit-2026-06-25.json
```

Reuse arm C, `l1_weight=1e-9`:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-diagnostic-2026-06-25.json
```

Reuse arm C validation is not an exact command-acceptance test. It is a
manifest/protocol equivalence test against the Phase 6V frozen protocol. The
validation must require:

- status
  `P86_PHASE6T_L1_REGULARIZATION_TUNING_DIAGNOSTIC_TRAINING_BASE_COMPLETED`;
- `fit_executed=true`;
- `training_backend=training_base_optimizer`;
- target dimension `36`, rank `5`, training samples `567600`, holdout samples
  `65536`, and audit samples `65536`;
- `learning_rate=0.0003`, `l1_weight=1e-9`, `l2_weight=1e-8`, and
  `logz_anchor_weight=0.0`;
- adaptive scheduler fields matching the Phase 6V frozen protocol;
- train/holdout/audit seeds `8301/8401`, `9301/9401`, and `9311/9501`;
- route manifest equality for target, basis family/order/element count,
  domain map, domain scale, measure convention, and XLA-static fields;
- `trained_core_serialization.status=serialized_with_values`;
- post-fit statuses for finite residuals/normalizer, no fallback route, no
  audit tuning, and runtime/memory within envelope;
- nonclaims preserving no rank convergence, no production readiness, no HMC,
  no LEDH, and no source-faithful TT-cross training claim.

New fit arm D, `l1_weight=3e-9`:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-2026-06-25.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.000000003 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-3e-9-fit-2026-06-25.json
```

## Forbidden Claims / Actions

- Do not run any Phase 6V fit before exact human approval of the frozen
  commands.
- Do not tune on the audit cloud.
- Do not use audit-cloud results to select an L1 candidate.
- Do not compare a regularized rank-5 arm against the old rank-4 arm as if it
  closed same-policy rank convergence.
- Do not revive ALS training.
- Do not change route, basis, domain, target, rank, measure convention, cloud
  roles, optimizer backend, or output paths while calling arms comparable.
- Do not declare a universal L1 scalar default.
- Do not claim Phase 7 is open from the no-fit preflight or from validation
  selection alone.
- Do not claim production readiness, posterior correctness, HMC readiness, KR
  closure, LEDH superiority, GPU performance, d50/d100 scaling, or
  source-faithful author TT-cross training.

## Exact Next-Phase Handoff Conditions

Phase 6V may hand off to a refreshed Phase 6W rank/degree convergence subplan
only if:

- the no-fit preflight and exact guard pass local checks;
- Claude agrees the no-fit implementation/result is boundary-safe;
- the user approves the exact Phase 6V fitting commands before execution;
- all approved candidate fits complete or are recorded with precise blockers;
- a selection ledger chooses or rejects a candidate using validation/holdout
  only, with audit preserved;
- the selected candidate, if any, passes the Phase 6V primary criterion and no
  veto diagnostic fires;
- Claude agrees the Phase 6V result avoids rank-convergence and production
  overclaims.

Phase 7 may be refreshed only after a later reviewed same-policy rank/degree
convergence phase passes or explicitly reframes the gate with owner approval.

## Stop Conditions

Stop if:

- Claude requests a material subplan or result revision that cannot be fixed
  within five review loops;
- the no-fit preflight/guard cannot freeze all candidate commands exactly;
- focused tests fail and the failure is not immediately fixable;
- Phase 6T reuse does not match the Phase 6V protocol;
- exact human approval for the new fitting commands is absent;
- any fit exceeds approved runtime/memory or produces nonfinite diagnostics;
- audit-cloud data would be needed for selection;
- results require changing criteria after seeing outputs;
- continuing would require GPU evidence, HMC, LEDH, package installation,
  remote access, default-policy change, production promotion, or a scientific
  claim outside this phase.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 6V result or blocker;
3. draft or refresh the next Phase 6W rank/degree convergence subplan or a
   blocker handoff;
4. review the next subplan for consistency, correctness, feasibility,
   artifact coverage, boundary safety, and approval needs;
5. request Claude read-only bounded review of material results and repair
   visibly if review finds a fixable problem.
