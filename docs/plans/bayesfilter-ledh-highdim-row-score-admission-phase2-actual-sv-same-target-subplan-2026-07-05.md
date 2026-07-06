# Phase 2 Subplan: Actual SV Same-Target Adapter And Score

metadata_date: 2026-07-05
status: DRAFT
master_program: docs/plans/bayesfilter-ledh-highdim-row-score-admission-master-program-2026-07-05.md
phase: 2

## Phase Objective

Repair the LEDH actual-SV row by first freezing the exact transformed actual-SV
target, then tracing the current LEDH forward path, then replacing any
wrong-target scalar with a same-target scalar, and only then implementing the
no-tape total derivative of that exact finite scalar.

## Entry Conditions Inherited From Previous Phase

- Phase 1 completed with a bounded blocker record:
  `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase1-fixed-spatial-sir-full-row-result-2026-07-05.md`
- The actual-SV corrected derivation note remains the governing same-target
  statement for transformed actual SV.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase2-actual-sv-same-target-result-2026-07-05.md`
- A same-target actual-SV row note or patched derivation note section naming:
  - the exact scalar;
  - the current wrong branch, if one exists;
  - the required same-target LEDH adapter.
- Tests:
  - tiny same-target value tests;
  - tiny score FD tests;
  - no-autodiff sentinels;
  - later `N=10000` score-memory test if admitted.

## Required Checks/Tests/Reviews

```bash
rg -n "actual[-_ ]SV|transformed actual-SV|log\\(y_t\\^2\\)|blocked_no_reviewed_current_gpu_xla_ledh_row_adapter|wrong relative to the stated target|same-target" docs/plans docs/chapters bayesfilter docs/benchmarks experiments tests
```

If code changes are made, required local checks expand to focused tiny same-target
value and score tests plus any row-specific smoke or `N=10000` tests created in
the phase.

Material review required:

- Claude read-only review of the Phase 2 result and the Phase 3 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the current LEDH actual-SV row compute the exact transformed actual-SV scalar, and if not, can it be repaired so that its no-tape total derivative is the derivative of the correct executed scalar? |
| Baseline/comparator | The actual-SV corrected derivation note, any exact transformed actual-SV reference route, and tiny fixed-randomness same-scalar FD checks. |
| Primary criterion | The phase identifies one exact scalar, labels wrong-target code as wrong, repairs or replaces the forward adapter, and verifies the no-tape total derivative of that repaired scalar. |
| Veto diagnostics | Mixing transformed-observation flow with a different correction density; reusing a wrong scalar after the mismatch is known; using autodiff score as admission evidence. |
| Explanatory diagnostics | Legacy callback structure, transformed-observation helper reuse, and diagnostic lowdim comparisons. |
| Not concluded | No exact raw actual-SV likelihood quadrature claim, no KSC claim, no generalized-SV claim, no HMC claim. |

## Forbidden Claims/Actions

- Do not treat a transformed flow plus raw-density correction as same-target
  proof.
- Do not reuse old mixed-target code as admission evidence after mismatch is
  shown.
- Do not implement the score first.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if Phase 2 records either:

1. a repaired actual-SV same-target LEDH value-and-score route, or
2. a precise blocker that leaves the transformed-SV target discipline clearer
   than before and still freezes the required KSC prerequisites.

## Stop Conditions

Stop if the phase cannot name the actual-SV scalar exactly, or if no same-target
forward route can be identified from the current code and a replacement design
cannot yet be justified.
