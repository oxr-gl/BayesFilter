# Phase 3 Subplan: KSC SV Same-Target Adapter And Score

metadata_date: 2026-07-05
status: DRAFT
master_program: docs/plans/bayesfilter-ledh-highdim-row-score-admission-master-program-2026-07-05.md
phase: 3

## Phase Objective

Build a KSC-specific LEDH same-target row and no-tape score after the
transformed-SV target discipline is stabilized by the actual-SV phase.

## Entry Conditions Inherited From Previous Phase

- Phase 2 finished and left a clearer transformed-SV target discipline:
  the current actual-SV LEDH runner is not the old Gaussian-closure scalar, but
  its transformed-row admission bridge remains unreviewed.
- KSC is still blocked because no dedicated LEDH adapter exists.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase3-ksc-sv-same-target-result-2026-07-05.md`
- A KSC row-target note naming:
  - the exact KSC surrogate scalar;
  - the exact differentiated parameter vector;
  - the exact KSC LEDH adapter surface.
- Tests:
  - tiny same-target value tests;
  - tiny score FD tests;
  - no-autodiff sentinels;
  - later `N=10000` score-memory test if admitted.

## Required Checks/Tests/Reviews

```bash
rg -n "ksc|gaussian_mixture_surrogate|blocked_no_ledh_ksc_row_adapter|same-target" docs/plans docs/benchmarks bayesfilter tests
```

Material review required:

- Claude read-only review of the Phase 3 result and the Phase 4 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter execute the KSC row with an actual KSC-specific same-target LEDH scalar and a no-tape total derivative of that scalar, without borrowing actual-SV row-target language that has not been reviewed for KSC? |
| Baseline/comparator | The KSC row definition in the ledger, any exact or reviewed KSC reference route, and tiny same-scalar FD checks. |
| Primary criterion | The phase produces a dedicated KSC LEDH adapter and a same-scalar no-tape score, or it records a precise blocker that still keeps KSC separate from actual SV. |
| Veto diagnostics | Reusing actual-SV raw callbacks as KSC evidence; skipping KSC-specific target freezing; using autodiff score as admitted evidence. |
| Explanatory diagnostics | Shared transformed-SV helpers and diagnostic mixture routes. |
| Not concluded | No actual-SV claim, no generalized-SV claim, no HMC claim. |

## Forbidden Claims/Actions

- Do not claim KSC support by analogy alone.
- Do not reuse actual-SV callbacks as KSC proof.
- Do not treat the actual-SV raw-likelihood-corrected flow adapter as if it
  automatically settles the KSC row target.
- Do not promote score before the KSC value adapter exists.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only after Phase 3 records either a passed KSC row or a
precise blocker that still preserves KSC as a distinct target family.

## Stop Conditions

Stop if the phase cannot state the KSC row target exactly or if no KSC-specific
adapter surface can be located or justified.
