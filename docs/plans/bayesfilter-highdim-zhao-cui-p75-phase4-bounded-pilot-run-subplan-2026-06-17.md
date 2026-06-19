# P75 Phase 4 Subplan: Bounded Pilot Run

metadata_date: 2026-06-17
status: EXECUTED_TARGET_SMOKE_BLOCKED_RESULT_REVIEW_PENDING
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-result-2026-06-17.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run the smallest real fixed-variant target pilot that can test whether the P75
stochastic density-training command surface works beyond synthetic smoke, then
optionally run the user-requested degree 2/rank 4/batch 1024/up-to-500-batch
pilot if the real target smoke passes within bounds.

## Entry Conditions Inherited From Phase 3

Phase 4 may begin only if:

- Phase 3 result exists;
- implementation, tests, and runner are present;
- CPU-only focused tests pass;
- CPU-only schema and synthetic smoke commands pass;
- Phase 3 result states no target pilot has run;
- Claude returns `VERDICT: AGREE` for Phase 3 result and this subplan.

## Required Artifacts

Phase 4 must produce:

- tiny target-smoke JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-target-smoke-2026-06-17.json`;
- optional target-pilot JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-target-pilot-degree2-rank4-2026-06-17.json`;
- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase4-bounded-pilot-run-result-2026-06-17.md`;
- Phase 5 result-decision subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p75-phase5-result-decision-subplan-2026-06-17.md`;
- updated execution and Claude review ledgers.

## Required Checks/Tests/Reviews

Preflight checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --schema-only --output /tmp/p75-schema-preflight.json
```

Tiny real target smoke:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --target-pilot --degree 1 --rank 1 --batch-size 16 --batches 2 --max-seconds 180 --output docs/plans/bayesfilter-highdim-zhao-cui-p75-target-smoke-2026-06-17.json
```

Target pilot, only if tiny target smoke passes mechanics gates and does not
hit a stop condition:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_stochastic_density_training_pilot.py --target-pilot --degree 2 --rank 4 --batch-size 1024 --batches 500 --max-seconds 1800 --output docs/plans/bayesfilter-highdim-zhao-cui-p75-target-pilot-degree2-rank4-2026-06-17.json
```

Review:

- Claude read-only review of Phase 4 result and Phase 5 subplan;
- loop to convergence or max 5 rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can the P75 stochastic density trainer run on real fixed-variant author-SIR step-1 fresh batches with finite objective/gradient and independent fresh-audit diagnostics? |
| Exact baseline/comparator | P73 Phase 5/6 blocked diagnostic as historical failed-scale comparator; no same-schedule ALS superiority claim unless separately created. |
| Primary pass/fail criterion | Tiny real target smoke must complete at least one finite training step and write a valid manifest.  The optional target pilot passes only if it completes without numerical/provenance veto and records fresh-audit diagnostics under frozen gates. |
| Diagnostics that can veto | Nonfinite loss/gradient/parameter/log-normalizer; normalizer floor breach; audit seed/training seed overlap; runner exception; wall-clock cap before first step; P73-B unblocked unexpectedly; target smoke audit/provenance block. |
| Explanatory only | Training loss trajectory, cross-entropy, gradient norm, parameter delta, runtime, target-pilot audit residual magnitudes if gates still block. |
| What will not be concluded | No validation readiness, no HMC readiness, no scaling claim, no source-faithful adaptive Zhao--Cui parity, no final rank/sample policy, no full sequential lower-gate repair from step-1 alone. |
| Artifact preserving result | Phase 4 JSONs, result note, ledgers, Claude review. |

## Stop Conditions

Stop after tiny target smoke if:

- it raises an exception;
- it produces no training step;
- it reports nonfinite objective/gradient/normalizer/parameter values;
- it fails to write the JSON manifest;
- it hits the 180-second wall-clock cap before one step;
- it uses audit seeds for training;
- it modifies P72/P73 default behavior.

Stop before the degree 2/rank 4 run if:

- tiny target smoke does not pass mechanics gates;
- CPU runtime appears likely to exceed the reviewed cap by more than a small
  margin;
- the user or Claude review identifies the target pilot as too broad for the
  current phase;
- GPU is needed to make the run meaningful.  GPU would be a human-required
  boundary and is not approved by this subplan.

Stop during the degree 2/rank 4 run if:

- any mandatory numerical/provenance veto fires;
- the 1800-second wall-clock cap is reached;
- output cannot be written under `docs/plans`;
- continuing would require changing thresholds after seeing outputs.

## Forbidden Claims/Actions

- Do not run validation, HMC, scaling, GPU, or rank promotion.
- Do not claim source-faithful Zhao--Cui.
- Do not claim lower-gate repair unless the frozen fresh-audit gates pass, and
  even then restrict the claim to this one-step pilot.
- Do not change thresholds after seeing outputs.
- Do not use audit holdout, replay, or audit-line samples for training,
  stopping, learning-rate selection, regularization selection, degree, or
  rank.
- Do not compare against ALS as an apples-to-apples win unless a reviewed
  same-schedule ALS comparator is created.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only if:

- Phase 4 result exists;
- target smoke result exists;
- optional target-pilot result either exists or is explicitly skipped with a
  stop reason;
- Phase 5 subplan exists and defines result-decision criteria;
- local checks pass;
- Claude returns `VERDICT: AGREE`.

## Skeptical Plan Audit

This subplan passes the initial skeptical audit because it starts with a tiny
real target smoke before the larger run, keeps CPU-only execution bounded,
uses P73 as a historical failed-scale comparator rather than an ALS win/loss
baseline, and treats fresh-audit gates as veto evidence.
