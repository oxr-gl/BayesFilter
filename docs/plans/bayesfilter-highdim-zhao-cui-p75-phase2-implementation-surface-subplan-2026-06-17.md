# P75 Phase 2 Subplan: Implementation Surface And Test Plan

metadata_date: 2026-06-17
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE2
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Map the Phase 1 stochastic density objective to exact source files, APIs,
tests, diagnostics, command surfaces, artifacts, and Phase 3 implementation
boundaries.  Phase 2 is still planning-only: it must not edit implementation
code and must not run training.

## Entry Conditions Inherited From Phase 1

Phase 2 may begin only if:

- Phase 1 result exists;
- Phase 1 freezes the `rho_theta` family, exact `log Z` normalizer treatment,
  KL/cross-entropy objective, training/evaluation split, finite-gradient gate,
  and CPU-only pilot ladder;
- Phase 1 local checks pass;
- Claude returns `VERDICT: AGREE` for the Phase 1 result and this subplan.

## Required Artifacts

Phase 2 must produce:

- Phase 2 implementation-surface result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-result-2026-06-17.md`;
- Phase 3 opt-in implementation subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-subplan-2026-06-17.md`;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Local checks:

```bash
test -s docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-result-2026-06-17.md
rg -n "rho_theta|log Z|KL|cross-entropy|audit holdout|finite-gradient|CPU-only|not validation" docs/plans/bayesfilter-highdim-zhao-cui-p75-phase1-stochastic-objective-design-result-2026-06-17.md
rg -n "Trainable|tf.Variable|GradientTape|normalizer|Adam|audit exclusion|CPU-only|pytest|no training" docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-subplan-2026-06-17.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p75-phase2-implementation-surface-result-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-subplan-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-claude-review-ledger-2026-06-17.md
```

Review:

- Claude read-only review of Phase 2 surface map and Phase 3 implementation
  subplan;
- loop to convergence or max 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What minimal opt-in implementation surface can realize the Phase 1 objective without overclaiming? |
| Exact baseline/comparator | Phase 1 design result and current P73/P72 evaluator/gate surfaces. |
| Primary pass/fail criterion | Phase 2 passes if it maps the objective, trainable variables, exact normalizer, fresh-batch generation, audit exclusion, unit tests, command artifacts, and Phase 3 boundaries to concrete files without code edits or training. |
| Diagnostics that can veto | Missing trainable-parameter surface, non-differentiable normalizer route, audit-holdout leakage, TensorFlow backend violation, unbounded target pilot, proxy-loss promotion, source-faithfulness overclaim. |
| Explanatory only | Runtime estimates, approximate parameter count, candidate file names, candidate test names. |
| What will not be concluded | No implementation correctness, no pilot result, no lower-gate repair, no validation readiness, no HMC readiness, no adaptive Zhao--Cui parity. |
| Artifact preserving result | Phase 2 result, Phase 3 subplan, ledgers. |

## Required Design Mapping

Phase 2 must map these surfaces:

- new opt-in module, expected name
  `bayesfilter/highdim/stochastic_density_training.py`;
- new opt-in tests, expected name
  `tests/highdim/test_p75_stochastic_density_training.py`;
- new diagnostic runner, required name
  `scripts/p75_stochastic_density_training_pilot.py`;
- package export policy, likely no default public export unless explicitly
  reviewed;
- trainable adapter with `tf.Variable` cores and a method to snapshot into
  immutable `FunctionalTT`/`SquaredTTDensity` for evaluation/manifests;
- differentiable `rho_theta`, exact squared-TT `normalizer`, `log Z`,
  weighted empirical cross-entropy/KL objective, regularization, and
  finite-gradient diagnostics;
- fresh-batch generator for training clouds and a separate audit generator for
  audit holdout/replay/line clouds;
- manifest fields for seeds, hashes, objective settings, optimizer settings,
  CPU-only status, pilot-halting conditions, and nonclaims.

The Phase 3 implementation must create all three named surfaces above.  It may
reuse internal helper code from P72/P73, but the P75 runner itself must exist
as the explicit command surface for smoke and pilot artifacts.

## Required Test Mapping

Phase 2 must define focused Phase 3 tests for:

- `tf.Variable` cores are watched by `GradientTape`;
- exact trainable normalizer matches immutable `SquaredTTDensity.normalizer`
  after snapshot on a tiny hand-built TT;
- objective returns finite loss, finite `log Z`, and finite gradients on a
  tiny synthetic batch;
- weighted empirical cross-entropy uses normalized target weights and reduces
  to the unweighted average only when uniform weights are explicitly supplied;
- one Adam or gradient-descent smoke step changes at least one core by a
  finite amount;
- audit holdout records are rejected or excluded from training manifests;
- positivity assumptions are enforced: \(q_0>0,\tau>0\) or a reviewed positive
  floor is required before evaluating `log rho_theta`;
- CPU-only command path records `CUDA_VISIBLE_DEVICES=-1`;
- P73-B blocked evaluator remains distinct from the new opt-in P75 trainer.

## Forbidden Claims/Actions

- Do not edit implementation code in Phase 2.
- Do not run training or pilot diagnostics.
- Do not run validation, HMC, scaling, GPU, or rank promotion.
- Do not change P72/P73/P75 thresholds after seeing outputs.
- Do not train on audit holdout or audit-line samples.
- Do not claim stochastic training is source-faithful Zhao--Cui.
- Do not claim a planned test is evidence that the method works.
- Do not leave the P75 runner implicit or delegated to an unrelated script.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- Phase 2 result exists and passes local checks;
- the result names exact implementation files and test commands;
- the result distinguishes implementation mechanics from fresh-audit evidence;
- Phase 3 subplan exists and authorizes only opt-in code/tests;
- Claude returns `VERDICT: AGREE`.

## Stop Conditions

Stop and write a blocker if:

- exact normalizer differentiation is not implementable without `.numpy()` in
  the training path;
- the existing target/audit generation cannot be separated into training and
  audit seeds;
- the minimal implementation would require non-TensorFlow backends, package
  install, network access, GPU, or outside-repo writes;
- Phase 3 would need to modify default Zhao--Cui behavior rather than adding an
  opt-in P75 surface;
- the explicit P75 runner surface cannot be created without broad unrelated
  script refactors;
- Claude and Codex do not converge after five review rounds for the same
  blocker.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit if Phase 1 passes review:
it keeps Phase 2 planning-only, requires concrete source and test surfaces
before code edits, preserves audit exclusion, and blocks proxy-loss promotion.
