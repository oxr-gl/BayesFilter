# Claude Read-Only Review Bundle

Date: 2026-07-08
Review name: `bayesfilter-ledh-compact-score-default-phase2-result-phase3-subplan-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review the Phase 2 LGSSM compact reference result and Phase 3 actual-SV compact
port subplan.

## Artifacts To Inspect

- `docs/plans/bayesfilter-ledh-compact-score-default-phase2-lgssm-reference-result-2026-07-08.md`
- `docs/plans/bayesfilter-ledh-compact-score-default-phase3-actual-sv-subplan-2026-07-08.md`
- `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
- `tests/highdim/test_ledh_lgssm_score_phase2_contract.py`
- `tests/test_ledh_lgssm_manual_score_phase4.py`

Context anchors:

- `docs/benchmarks/benchmark_ledh_same_target_actual_sv_score.py`
- `docs/benchmarks/benchmark_ledh_same_target_actual_sv_value.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is LGSSM correctly frozen as compact reference, and is the actual-SV port subplan safe and concrete? |
| Baseline/comparator | LGSSM compact source/tests, Phase 1 validator, actual-SV current reverse-record route and admitted value artifact. |
| Primary criterion | Phase 2 must avoid stale memory overclaim; Phase 3 must explicitly replace actual-SV reverse records with compact forward sensitivity and preserve same target scalar. |
| Veto diagnostics | LGSSM historical reverse admitted; stale `T=2` artifact treated as fresh; actual-SV plan omits transport value+JVP; actual-SV plan permits `manual_total_vjp*` admission; wrong target scalar or KSC/raw likelihood substitution; Claude authority transfer. |
| Explanatory diagnostics | Suggested extra tests, missing source anchors, implementation ordering improvements. |
| Not concluded | No actual-SV implementation yet, no full `N=10000,T=1000` admission, no HMC/posterior/scientific claim. |

## Review Questions

1. Does Phase 2 correctly identify the LGSSM compact reference mechanism?
2. Does Phase 2 avoid overclaiming fresh memory evidence?
3. Does Phase 3 have enough detail to port actual-SV to compact forward
   sensitivity without preserving the old route as default?
4. Are required tests, stop conditions, and nonclaims sufficient?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
