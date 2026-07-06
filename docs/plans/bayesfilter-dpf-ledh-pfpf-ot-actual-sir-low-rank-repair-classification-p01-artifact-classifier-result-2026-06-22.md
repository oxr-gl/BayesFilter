# P01 Prior Tuning P03 Artifact Classifier Result

Date: 2026-06-22
Status: `PASS_ARTIFACT_CLASSIFIER_BOTH_REPAIRS_NEEDS_SOURCE_INSPECTION`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Prior tuning P03 artifacts support two independent repair signals: comparable-but-slow rows nominate a performance-repair question, while incomparable and ESS hard-veto rows nominate tuning/comparability/validity repair. Source inspection is required before assigning route cause. |
| Primary criterion status | Passed: artifact-only classifier table was written and separates hard-veto, comparable-but-slow, incomparable, and descriptive-only evidence. |
| Veto diagnostic status | No missing row artifact, aggregate/row mismatch, nonparseable JSON, or label mismatch was found. |
| Main uncertainty | P01 cannot prove whether the slow comparable rows are caused by route implementation, timing-source asymmetry, solver math, or tuning. |
| Next justified action | Proceed to P02 code-path classifier. |
| What is not concluded | No route-performance proof, tuning proof, speedup claim, candidate freeze, statistical ranking, posterior correctness, or implementation direction. |

## Evidence Artifact

Structured summary:
`docs/benchmarks/actual-sir-low-rank-repair-classification-p01-artifact-summary-2026-06-22.json`

Prior tuning P03 source aggregate:
`docs/benchmarks/actual-sir-low-rank-tuning-p03-screen-stage-a-2026-06-22.json`

## Artifact Integrity

| Check | Result |
| --- | --- |
| Aggregate parsed | `PASS` |
| Row artifact paths exist | `PASS`: `0` missing paths |
| Row JSON files parse | `PASS`: all referenced row JSON files parsed |
| Candidate count | `PASS`: `20` |
| Label counts | `PASS`: `comparable-but-slow=7`, `incomparable=11`, `hard-vetoed=2`, `freeze-nominated=0` |
| Current-wrapper drift diagnostic | `PASS`: `python -m pytest tests/test_actual_sir_low_rank_tuning_grid.py -q` -> `13 passed` |

## Artifact-Only Signals

| Signal | Evidence | Interpretation Role |
| --- | --- | --- |
| Comparable-but-slow | 7 candidates passed paired comparability but failed warm-time screen. | Repair trigger for performance investigation, not proof of route cause. |
| Incomparable | 11 candidates failed paired comparability without hard veto. | Repair trigger for tuning/comparability investigation. |
| ESS hard veto | 2 candidates hard-vetoed on `low_rank:ess_fraction_min_threshold`. | Hard-veto evidence for those candidates only. |
| No freeze | `num_freeze_nominated=0`. | Blocks Stage B/P04 from the earlier tuning plan. |

## Descriptive Timing And Delta Summary

| Metric | Count | Min | Median | Max |
| --- | ---: | ---: | ---: | ---: |
| Comparable streaming/low-rank warm median | 7 | 0.01371426686468479 | 0.016513046517512397 | 0.018582506337490805 |
| Comparable low-rank/streaming warm median | 7 | 53.81405402684932 | 60.55817737444639 | 72.91676688712182 |
| Comparable log-likelihood mean abs delta | 7 | 0.00677490234375 | 0.0496826171875 | 4.40484619140625 |
| Incomparable log-likelihood mean abs delta | 11 | 6.12896728515625 | 22.84820556640625 | 58.295166015625 |

These timing and delta values are descriptive because P03 was one tuning
seed/shape and no uncertainty analysis was planned. They support repair
classification only.

## Hard-Veto Candidates

| Candidate | Hard vetoes | Mean log-likelihood delta | Warm median streaming/low-rank |
| --- | --- | ---: | ---: |
| `r32_eps0p015625_alpha1em08_it120` | `low_rank:ess_fraction_min_threshold`, repeated in route row diagnostics | 6.08831787109375 | 0.008455183993493414 |
| `r128_eps0p03125_alpha1em08_it120` | `low_rank:ess_fraction_min_threshold`, repeated in route row diagnostics | 45.3990478515625 | 0.007414628863153121 |

## P01 Classifier

`BOTH_REPAIRS_NEEDS_SOURCE_INSPECTION`

Reason:

- `route_performance_repair_signal=true`: comparable candidates exist and all
  failed the warm-time screen by a large descriptive margin.
- `tuning_comparability_ess_repair_signal=true`: most candidates were
  incomparable and two candidates were hard-vetoed on ESS.
- Source inspection is required before deciding whether the performance signal
  is route-execution overhead, timing-source asymmetry, solver math, or another
  cause.

## Handoff

Proceed to:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p02-code-path-classifier-subplan-2026-06-22.md`

P02 must inspect source anchors and must not edit route internals or claim
speedup.
