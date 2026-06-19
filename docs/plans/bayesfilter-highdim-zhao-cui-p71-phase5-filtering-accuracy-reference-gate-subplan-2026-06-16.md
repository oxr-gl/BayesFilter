# P71 Phase 5 Subplan: Filtering Accuracy And Reference Gate

metadata_date: 2026-06-16
status: DRAFT_PENDING_PHASE4_RESULT
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 5

## Phase Objective

Define and execute the first d18 filtering accuracy gate against a reviewed
reference/comparator chosen before seeing the validation outputs.

## Entry Conditions Inherited From Previous Phase

- Phase 4 admits exactly one d18 configuration for accuracy testing.
- Phase 4 records source invariants, branch hashes, and structural diagnostics.

## Required Artifacts

- Phase 5 result note.
- Reference/comparator design record.
- Accuracy JSON/CSV artifact.
- Run manifest with seed, command, environment, CPU/GPU status, wall time, and
  output paths.
- Refreshed Phase 6 robustness/performance subplan.

## Required Checks/Tests/Reviews

- Review the reference/comparator before execution.
- Run a focused smoke check on a lower or tiny row if needed, but do not treat
  it as d18 accuracy evidence.
- Run the exact d18 accuracy command only after the evidence contract is
  frozen.
- Claude read-only review of the reference choice and result interpretation.

## Reference Eligibility

The primary accuracy gate requires an independent same-target reference chosen
before execution.  An author-route replay, same-route replay, or reference
bridge may be used only as a consistency or source-route diagnostic; it cannot
be the primary accuracy comparator and cannot by itself support a d18 accuracy
claim.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the admitted fixed-route d18 filter match a reviewed reference/comparator within predeclared accuracy thresholds? |
| Baseline/comparator | A Phase 5-reviewed independent same-target reference, such as an independent high-particle SMC or other independent reference route, with exact command and thresholds frozen before execution.  Same-route replay/reference bridge evidence is consistency-only. |
| Primary criterion | Predeclared state/filtering accuracy metrics pass against the independent same-target reference for the admitted d18 configuration with no veto diagnostics. |
| Veto diagnostics | Nonfinite values, reference not independent or not documented, threshold changes after output, branch drift, poor ESS, unbounded correction weights, same-route replay promoted to accuracy, or one failed diagnostic hidden by averaging. |
| Explanatory diagnostics | Same-route replay diagnostics, per-time state errors, observed/unobserved component errors, normalizer error, ESS, correction weights, runtime, memory. |
| Not concluded | No multi-seed robustness, no scaling, no HMC production readiness, no adaptive parity. |
| Artifact | Phase 5 result note and accuracy artifact. |

## Forbidden Claims/Actions

- Do not choose the reference after seeing target outputs.
- Do not use author-route replay, same-route replay, or a reference bridge as
  the primary accuracy comparator.
- Do not average away a veto diagnostic.
- Do not claim d18 is validated from lower-dimensional or smoke rows.
- Do not use CUT4 as a d18 comparator; it is out of scope for this dimension.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if Phase 5 passes the single-seed/reference accuracy
gate and records all veto diagnostics as passed.

## Stop Conditions

Stop if no credible reference/comparator can be defined, if the accuracy gate
fails, or if resource/runtime requirements exceed approved scope.
