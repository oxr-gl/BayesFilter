# P75 Phase 6 Subplan: Guided Warm-Start Smoke

metadata_date: 2026-06-18
status: EXECUTED_GUIDED_WARM_START_SMOKE_RESULT_REVIEW_PENDING
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Test the smallest warm-start hypothesis: whether a source/UKF-style guided
scale initialization can move P75 out of the defensive-floor regime on the
same tiny target smoke that failed under random initialization.

## Entry Conditions Inherited From Phase 5

Phase 6 may begin only if:

- Phase 5 result exists;
- Phase 5 identifies initialization/objective-scale collapse as the selected
  next diagnostic;
- local checks pass;
- Claude returns `VERDICT: AGREE` for the Phase 5 result and this subplan, or
  fixable issues have been patched and re-reviewed.

## Required Artifacts

Phase 6 must produce:

- warm-start comparison JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-guided-warm-start-smoke-2026-06-18.json`;
- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-result-2026-06-18.md`;
- if warranted, a Phase 7 subplan for a proper UKF/source-guided initializer;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Local implementation checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
git diff --check -- scripts/p75_stochastic_density_training_pilot.py tests/highdim/test_p75_stochastic_density_training.py docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase6-guided-warm-start-smoke-subplan-2026-06-18.md
```

Warm-start smoke:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --target-pilot --compare-init-modes --degree 1 --rank 1 --batch-size 16 --batches 2 --max-seconds 180 --seed 7501 --output docs/plans/bayesfilter-highdim-zhao-cui-p75-guided-warm-start-smoke-2026-06-18.json
```

The comparison must reuse identical target-smoke and audit draws across the
random and guided arms.  The only intended difference between arms is the
initialization of \(h_\theta\).

Review:

- Claude read-only review of the Phase 6 result and any Phase 7 subplan;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does a guided target-scale warm start escape the defensive-floor collapse on the tiny P75 target smoke? |
| Exact baseline/comparator | Phase 4 random-initialization target smoke and the same command's random-init arm. |
| Primary pass/fail criterion | Guided arm must have `rho_max > 10 * tau`, finite non-tiny gradient norm, completed two batches without provenance/numerical veto, and a relative win over the concurrent random arm on the same draws: materially larger `rho_max` and gradient norm than random. |
| Diagnostics that can veto | Nonfinite objective/gradient/normalizer; audit seed overlap; target smoke exception; failure to write JSON; wall-clock cap before one step; using audit data for initialization; claiming lower-gate repair from this smoke. |
| Explanatory only | Holdout/replay/line residuals, loss trajectory, runtime, exact residual magnitudes, whether the audit gate still blocks. |
| What will not be concluded | No validation readiness, HMC readiness, scaling claim, source-faithful adaptive Zhao--Cui parity, final rank/sample policy, or full UKF-initializer success. |
| Artifact preserving result | Warm-start JSON, Phase 6 result note, ledgers, Claude review. |

## Forbidden Claims/Actions

- Do not run the degree 2/rank 4/batch 1024/up-to-500 pilot.
- Do not run validation, HMC, scaling, GPU, or rank promotion.
- Do not use audit holdout, replay, or line samples for initialization,
  training, stopping, or hyperparameter selection.
- Do not claim UKF truth or source-faithful Zhao--Cui.
- Do not change thresholds after seeing outputs.

## Exact Next-Phase Handoff Conditions

Phase 7 may begin only if:

- Phase 6 result exists;
- the warm-start JSON exists and is valid;
- the result decides whether guided initialization is worth formalizing;
- if formalization is selected, a Phase 7 subplan exists and bounds the exact
  UKF/source-guided initialization work;
- Claude returns `VERDICT: AGREE`, or a blocker is escalated to the user.

## Stop Conditions

Stop before execution if implementation checks fail.

Stop after execution if:

- the warm-start arm does not escape the defensive floor;
- either arm raises an exception or records nonfinite terms;
- the result would require a larger run to interpret;
- any audit/provenance leakage is detected;
- Claude identifies a material blocker that cannot be repaired within this
  phase.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it does not launch a
larger pilot, uses the same tiny target smoke as the blocked baseline, treats
audit residuals as explanatory unless they veto, and asks only whether guided
initialization changes the defensive-floor mechanism.
