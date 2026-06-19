# P75 Phase 10 Subplan: Bounded Capacity/Sample/Prefit Ladder

metadata_date: 2026-06-18
status: REVIEWED_CLAUDE_AGREE_READY_FOR_PHASE10
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase9-guided-prefit-decision-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run a small CPU-only diagnostic ladder to test whether the Phase 8
source-guided-prefit mechanism becomes materially better under modestly
increased capacity, sample count, and prefit steps.  This is not the large
pilot and not a lower-gate repair attempt.

## Entry Conditions Inherited From Phase 9

Phase 10 may begin only if:

- Phase 9 decision result exists;
- Phase 9 classifies Phase 8 as mechanism evidence only;
- this subplan exists and bounds the ladder;
- local planning checks pass;
- Claude returns `VERDICT: AGREE` for the Phase 9 result and this subplan, or
  fixable issues have been patched and re-reviewed.

## Required Artifacts

Phase 10 must produce:

- one ladder JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-capacity-sample-ladder-2026-06-18.json`;
- Phase 10 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase10-capacity-sample-ladder-result-2026-06-18.md`;
- a Phase 11 decision subplan or stop handoff;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Pre-run checks:

```bash
python -m py_compile bayesfilter/highdim/stochastic_density_training.py scripts/p75_stochastic_density_training_pilot.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
```

The exact ladder runner command must be implemented or assembled in Phase 10
before execution.  The command must stay within these limits:

- degree in `{1, 2}`;
- rank in `{1, 2}`;
- batch size in `{32, 64}`;
- density-objective batches in `{2, 4}`;
- prefit steps in `{0, 5, 10}`;
- total row count no more than `16` executed target-smoke rows;
- CPU-only with `CUDA_VISIBLE_DEVICES=-1`;
- per-row wall-clock cap no more than `180` seconds;
- no detached/background execution.

Post-run checks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p75-capacity-sample-ladder-2026-06-18.json
git diff --check -- bayesfilter/highdim/stochastic_density_training.py scripts/p75_stochastic_density_training_pilot.py tests/highdim/test_p75_stochastic_density_training.py docs/plans/bayesfilter-highdim-zhao-cui-p75-capacity-sample-ladder-2026-06-18.json docs/plans/bayesfilter-highdim-zhao-cui-p75-phase10-capacity-sample-ladder-result-2026-06-18.md
```

Review:

- Claude read-only review of the ladder JSON, Phase 10 result, and Phase 11
  subplan or stop handoff;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does a small increase in degree, rank, batch size, density batches, or prefit steps make source-guided prefit materially improve fresh diagnostics relative to calibrated constant? |
| Exact baseline/comparator | Within each row, compare calibrated constant against source-guided prefit on identical density-training and audit draws.  Random may be included as a floor-collapse sentinel. |
| Primary criterion | A row is a mechanism win only if source-guided prefit completes finite prefit/objective steps, preserves provenance separation, and improves holdout RMS-relative by at least 10 percent relative to calibrated constant while not worsening audit-line RMS by more than 10 percent. |
| Diagnostics that can veto | Audit-data use; nonfinite terms; wall-clock cap before declared steps; same-draw mismatch; audit-line worsening beyond the row criterion; lower-gate/validation/HMC/scaling/source-faithfulness overclaim; large-pilot launch. |
| Explanatory only | Training losses, prefit losses, gradient norms, rho range, normalizer, replay residuals, exact line residuals, runtime. |
| What will not be concluded | No lower-gate repair, validation readiness, HMC readiness, scaling, source-faithfulness, final rank/sample policy, or large-pilot authorization. |
| Artifact preserving result | Ladder JSON, Phase 10 result, ledgers, Claude review. |

## Forbidden Claims/Actions

- Do not run the degree-2/rank-4/batch-1024/500-batch pilot.
- Do not run validation, HMC, scaling, GPU, or rank promotion.
- Do not claim lower-gate repair unless a later reviewed plan explicitly sets
  frozen fresh-audit gates and those gates pass.
- Do not use audit samples for initialization, prefit, training, stopping,
  hyperparameter selection, or metric switching.
- Do not change the 10 percent mechanism criterion after seeing outputs.

## Exact Next-Phase Handoff Conditions

Phase 11 may begin only if:

- Phase 10 result exists;
- ladder JSON exists and is valid;
- the result classifies each row as mechanism win/loss/block under the frozen
  criterion;
- the result selects a bounded next action or stop handoff;
- the next action is not the large pilot unless the user separately approves a
  new reviewed large-pilot plan;
- Claude review agrees, or a blocker is escalated to the user.

## Stop Conditions

Stop before execution if:

- implementing or assembling the ladder would require GPU, package install,
  network access, outside-repo writes, or detached execution;
- the runner cannot preserve identical density-training and audit draws
  within each row;
- local tests fail.

Stop during execution if:

- any row shows audit leakage, nonfinite terms, or same-draw mismatch;
- the wall-clock cap prevents even one comparable row;
- the ladder would exceed the row-count or runtime bounds.

Stop after execution if:

- all rows block numerically or by provenance;
- the result would require changing criteria after seeing outputs;
- Claude identifies a material blocker that cannot be repaired within five
  review rounds.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it tests a narrow
capacity/sample/prefit-step hypothesis, freezes a relative mechanism criterion
before execution, preserves same-draw comparisons, and forbids the large pilot
and downstream claims.
