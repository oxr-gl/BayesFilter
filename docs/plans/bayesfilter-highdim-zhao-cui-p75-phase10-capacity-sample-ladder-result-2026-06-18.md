# P75 Phase 10 Result: Bounded Capacity/Sample/Prefit Ladder

metadata_date: 2026-06-18
status: PHASE10_RESULT_PASSED_CLAUDE_AGREE_READY_FOR_PHASE11
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase10-capacity-sample-ladder-subplan-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p75-phase9-guided-prefit-decision-result-2026-06-18.md
json_artifact: docs/plans/bayesfilter-highdim-zhao-cui-p75-capacity-sample-ladder-2026-06-18.json
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Scientific/engineering question | Does a small increase in degree, rank, batch size, density batches, or prefit steps make source-guided prefit materially improve fresh diagnostics relative to calibrated constant? |
| Exact baseline/comparator | Within each row, calibrated constant versus source-guided prefit on identical density-training and audit draws.  Row 1 is a calibrated/random baseline-only reference. |
| Primary row criterion | Source-guided prefit must complete finite declared steps, preserve provenance separation, improve holdout RMS-relative by at least 10 percent versus calibrated constant, and not worsen audit-line RMS by more than 10 percent. |
| Diagnostics that can veto | Audit-data use, nonfinite terms, same-draw mismatch, incomplete declared steps, audit-line worsening beyond criterion, lower-gate/validation/HMC/scaling/source-faithfulness overclaim, large-pilot launch. |
| Outcome | Diagnostic completed.  No provenance, same-draw, nonfinite, or mechanics veto fired.  Source-guided prefit produced 0 mechanism wins out of 4 tested mechanism rows. |
| What is not concluded | No lower-gate repair, validation readiness, HMC readiness, scaling, source-faithfulness, final rank/sample policy, or large-pilot authorization. |
| Artifact preserving result | Ladder JSON, this result, Phase 11 decision subplan, ledgers, Claude review. |

## Command

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p75_capacity_sample_ladder.py --output docs/plans/bayesfilter-highdim-zhao-cui-p75-capacity-sample-ladder-2026-06-18.json --max-seconds-per-row 180.0
```

The runner executed in the foreground.  It used CPU-only intent with
`CUDA_VISIBLE_DEVICES=-1`.  TensorFlow emitted CUDA initialization warnings,
but the recorded run manifest still shows CPU-only intent and the run did not
use GPU evidence.

## Bounds Actually Used

| Bound | Value |
| --- | --- |
| Rows | `5` |
| Total target-pilot arm executions | `14` |
| Degree values | `{1, 2}` |
| Rank values | `{1, 2}` |
| Batch-size values | `{32, 64}` |
| Density-batch values | `{2, 4}` |
| Prefit-step values | `{0, 5, 10}` |
| Per-row wall-clock cap | `180` seconds |
| Large pilot | Not executed |

This stays inside both interpretations of the Phase 10 cap: fewer than 16
ladder rows and fewer than 16 target-pilot arm executions.

## Decision Summary

| Quantity | Value |
| --- | --- |
| Overall status | `diagnostic_completed` |
| Same-draw status | `true` |
| Mechanics status | `true` |
| Nonfinite detected | `false` |
| Baseline-only rows | `1` |
| Source-guided-prefit mechanism rows | `4` |
| Mechanism wins | `0` |
| Mechanism losses | `4` |
| Large pilot executed | `false` |
| Lower-gate repair claimed | `false` |
| Validation or HMC claimed | `false` |

## Row Table

| Row | degree | rank | batch size | batches | prefit steps | status | calibrated holdout | source-prefit holdout | holdout ratio | calibrated line RMS | source-prefit line RMS | line ratio | reason |
| ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1 | 1 | 32 | 2 | 0 | baseline_only | 0.9568899680347903 | N/A | N/A | 67.64689532762196 | N/A | N/A | baseline reference |
| 2 | 1 | 1 | 32 | 2 | 5 | mechanism_loss | 0.9568899680347903 | 0.949791415738309 | 0.9925816420553976 | 67.64689532762196 | 67.67056944530965 | 1.0003499660638235 | holdout improvement less than 10 percent |
| 3 | 1 | 2 | 64 | 2 | 10 | mechanism_loss | 0.966075144595077 | 0.9687729935354568 | 1.002792587052336 | 127.82343553026949 | 127.84636583930542 | 1.000179390492368 | holdout improvement less than 10 percent |
| 4 | 2 | 1 | 32 | 4 | 5 | mechanism_loss | 0.9544970428216808 | 0.9472206808599006 | 0.9923767579831679 | 73.79181781380427 | 73.79921720073163 | 1.0001002738128235 | holdout improvement less than 10 percent |
| 5 | 2 | 2 | 64 | 4 | 10 | mechanism_loss | 0.9645198230746281 | 0.9649828107329865 | 1.000480018810689 | 117.93987995384583 | 117.9485693750226 | 1.000073676700198 | holdout improvement less than 10 percent |

The source-guided prefit arms did not fail because of mechanics or provenance.
They failed because the improvement, when present, was only about 0.7 to 0.8
percent rather than the frozen 10 percent threshold, and two rows were slightly
worse than calibrated constant.

## Interpretation

Phase 10 weakens the hypothesis that the current square-root prefit, with this
objective and these tiny capacity/data increases, is a useful repair path by
itself.  It does not disprove larger-capacity or larger-sample stochastic
training as a general idea, but it does show that simply scaling the current
source-guided prefit mechanism from Phase 8 to this bounded ladder does not
produce material fresh-diagnostic improvement.

The result also preserves the earlier audit-line concern.  Audit-line RMS
values remain large in all rows.  The line criterion did not cause the Phase 10
mechanism losses because line ratios stayed close to 1, but the large absolute
line residuals still block any lower-gate repair claim.

## Decision

Do not launch the degree-2/rank-4/batch-1024/500-batch pilot under the current
P75 Phase 10 evidence.  The next justified action is a Phase 11 decision and
diagnosis pass that separates three possibilities before any larger run:

1. The current objective/parameterization is too weak, so the algorithm needs
   a mathematical redesign rather than more samples.
2. The current sample/capacity scale is too small, but a larger pilot requires
   a new reviewed plan with a stronger evidence contract.
3. The current prefit target is not aligned with the downstream density
   objective, so future work should modify the training objective or
   regularization before increasing runtime.

## Local Checks Passed

```text
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p75-capacity-sample-ladder-2026-06-18.json
status: passed

python -m py_compile bayesfilter/highdim/stochastic_density_training.py scripts/p75_stochastic_density_training_pilot.py scripts/p75_capacity_sample_ladder.py
status: passed

CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p75_stochastic_density_training.py
status: passed, 15 passed and 2 TensorFlow Probability deprecation warnings

rg -n "mechanism_win_count|large_pilot_executed|lower_gate_repair_claimed|validation_or_hmc_claimed|diagnostic_completed|mechanism_loss|holdout_improvement_less_than_10_percent|PHASE10|Phase 11|degree-2/rank-4/batch-1024/500-batch|large pilot" docs/plans/bayesfilter-highdim-zhao-cui-p75-capacity-sample-ladder-2026-06-18.json docs/plans/bayesfilter-highdim-zhao-cui-p75-phase10-capacity-sample-ladder-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase11-negative-ladder-decision-subplan-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-gated-execution-runbook-2026-06-17.md docs/plans/bayesfilter-highdim-zhao-cui-p75-visible-execution-ledger-2026-06-17.md
status: passed with expected result, boundary, and handoff hits

git diff --check -- bayesfilter/highdim/stochastic_density_training.py scripts/p75_stochastic_density_training_pilot.py scripts/p75_capacity_sample_ladder.py tests/highdim/test_p75_stochastic_density_training.py docs/plans/bayesfilter-highdim-zhao-cui-p75-capacity-sample-ladder-2026-06-18.json docs/plans/bayesfilter-highdim-zhao-cui-p75-phase10-capacity-sample-ladder-result-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p75-phase11-negative-ladder-decision-subplan-2026-06-18.md
status: passed
```

## Skeptical Post-Run Audit

The Phase 10 result should be treated as a negative bounded diagnostic, not as
a scientific impossibility result.  The artifact answers the stated question
only for the reviewed small ladder and the current source-guided-prefit
mechanism.  It should block the large pilot by inertia, but it should not block
a separately reviewed redesign or larger-sample plan with a stronger
mathematical rationale.
