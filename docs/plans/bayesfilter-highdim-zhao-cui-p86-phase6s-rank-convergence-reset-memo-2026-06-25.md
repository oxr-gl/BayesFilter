# P86 Phase 6S Reset Memo: Rank Convergence Remains Blocked

Date: 2026-06-25

Status: `BLOCK_P86_PHASE6S_RANK_CONVERGENCE_NOT_ESTABLISHED_REVIEWED`

## Summary

The runbook continued through the Phase 6R/6S repair loop. The repaired
adaptive rank-5 rerun was approved, executed, validated, reviewed, and compared
against the Phase 5 rank-4 lower rung.

Final decision: Zhao-Cui SIR is still not production-promoted. Rank convergence
is not established.

## Key Artifacts

- Phase 6R smoke result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6r-tiny-adaptive-training-smoke-result-2026-06-25.md`
- Phase 6S preflight/guard result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-adaptive-rank5-preflight-guard-result-2026-06-25.md`
- Phase 6S adaptive rank-5 fit artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank5-adaptive-comparator-fit-2026-06-25.json`
- Phase 6S adaptive rank-5 fit result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-adaptive-rank5-fit-result-2026-06-25.md`
- Phase 6S convergence ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank-convergence-ledger-2026-06-25.json`
- Phase 6S convergence result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6s-rank-convergence-result-2026-06-25.md`

## Final Evidence State

- Rank 4 holdout residual: `0.22090990401849483`
- Adaptive rank 5 holdout residual: `9.553783177487691`
- Rank-5/rank-4 holdout residual ratio: `43.24741898709909`
- Rank 5 stopped by the approved adaptive scheduler:
  `early_stop_after_plateau_lr_drop_limit`
- Rank 5 serialized trained cores with values.
- No fallback route, ALS route, audit tuning, nonfinite diagnostics,
  runtime breach, or memory breach was observed.

## Important Classifier Repair

The Phase 6S fit artifact raw status is blocked because the runner originally
treated any adaptive early stop before the max-step ceiling as incomplete
optimizer execution. Codex patched the runner so
`scheduler_stopped_after_plateau` is classified as a completed adaptive
protocol outcome, while fixed-budget max-step exhaustion remains strict.

The long fit was not rerun after this patch. The saved artifact is interpreted
as mechanically admissible after classifier repair, not as a new rerun.

## Nonclaims

No rank convergence, degree convergence, posterior correctness, KR closure, HMC
readiness, LEDH comparison, scale, GPU performance, source-faithful TT-cross
training, production readiness, or default-policy change is concluded.

This does not prove the Zhao-Cui paper is wrong. It blocks this fixed
training-base production-promotion path.

## Safest Next Action

Stop the production-promotion path. If continuing, create a new reviewed
diagnostic subplan focused on the smallest discriminating question among:

- validation/overfitting behavior;
- objective-vs-holdout mismatch;
- normalizer collapse;
- initialization sensitivity;
- whether an author-source-faithful TT-cross route is needed rather than the
  fixed training-base adaptation.
