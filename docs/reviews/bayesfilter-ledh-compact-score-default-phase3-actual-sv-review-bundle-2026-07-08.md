# Claude Read-Only Review Bundle: Phase 3 Actual-SV Compact Score

Date: 2026-07-08

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. Codex is
the supervisor and executor. Claude is an advisory read-only reviewer only.

## Objective

Review whether Phase 3 actual-SV compact score implementation/result and Phase
4 fixed-SIR subplan have any material boundary, correctness, or feasibility
problem before Codex advances the runbook.

## Artifacts To Review

- Implementation:
  `bayesfilter/highdim/ledh_score_contract.py`
- Implementation:
  `docs/benchmarks/benchmark_ledh_same_target_actual_sv_score.py`
- Tests:
  `tests/highdim/test_ledh_actual_sv_score_phase5_contract.py`
- Phase 3 result:
  `docs/plans/bayesfilter-ledh-compact-score-default-phase3-actual-sv-result-2026-07-08.md`
- Phase 4 subplan:
  `docs/plans/bayesfilter-ledh-compact-score-default-phase4-fixed-sir-subplan-2026-07-08.md`

## Key Implementation Anchors

- Compact actual-SV provenance:
  `ACTUAL_SV_COMPACT_SCORE_ROUTE_ID`.
- Compact transport helper:
  `_compact_forward_transport_jvp_tf`.
- Compact flow JVP:
  `_compact_streaming_flow_jvp_tf`.
- Compact default score loop:
  `_compact_value_and_score_from_components`.
- Default across-seed dispatch:
  `_manual_value_and_score_across_seeds` now calls compact.
- Artifact provenance:
  `_score_artifact_from_diagnostic` reads `base["score_route"]`.

## Local Evidence

Required test command:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_ledh_actual_sv_score_phase5_contract.py tests/highdim/test_ledh_score_contract_phase1.py -q
```

Result:

```text
38 passed, 2 warnings
```

Tiny diagnostic artifact:

```text
docs/plans/bayesfilter-ledh-compact-score-default-phase3-actual-sv-tiny-compact-score-2026-07-08.json
```

Key fields:

```text
score_derivative_provenance = compact_forward_sensitivity_no_autodiff_same_scalar_actual_sv_ledh_pfpf_ot
score_admission_status = tiny_score_diagnostic_not_admitted
max_abs_error = 6.049662710727599e-06
max_rel_error = 2.1665722010856176e-05
```

## Review Questions

1. Does the Phase 3 result avoid claiming full `N=10000,T=1000` actual-SV
   admission, memory evidence, HMC readiness, posterior correctness, or
   scientific superiority?
2. Is it acceptable for Phase 3 tiny gate that the compact loop uses the raw
   streaming value route for carried scalar state and the no-tape finite
   streaming value+JVP helper for tangent state, given same-scalar FD and exact
   value-route match tests pass?
3. Does the Phase 4 fixed-SIR subplan correctly forbid merely renaming the old
   p8p/manual-total-VJP route as compact?
4. Are there any material blockers that must be patched before starting Phase
   4?

## Required Verdict

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
