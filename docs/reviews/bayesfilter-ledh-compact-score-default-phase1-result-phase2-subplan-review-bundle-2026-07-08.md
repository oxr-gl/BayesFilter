# Claude Read-Only Review Bundle

Date: 2026-07-08
Review name: `bayesfilter-ledh-compact-score-default-phase1-result-phase2-subplan-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review the Phase 1 shared compact score contract result and Phase 2 LGSSM
reference subplan.

## Artifacts To Inspect

- `docs/plans/bayesfilter-ledh-compact-score-default-phase1-contract-result-2026-07-08.md`
- `docs/plans/bayesfilter-ledh-compact-score-default-phase2-lgssm-reference-subplan-2026-07-08.md`
- `bayesfilter/highdim/ledh_score_contract.py`
- `tests/highdim/test_ledh_score_contract_phase1.py`
- `tests/highdim/test_ledh_fixed_sir_score_phase3_contract.py`
- `tests/highdim/test_ledh_actual_sv_score_phase5_contract.py`
- `tests/highdim/test_ledh_predator_prey_score_phase4_contract.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Did Phase 1 close the full-admission gap for `manual_total_vjp*`, and is Phase 2 safe to start? |
| Baseline/comparator | Phase 0 inventory, old validator allowlist, updated validator, focused tests. |
| Primary criterion | Old `manual_total_vjp*` routes fail full admission; LGSSM compact route still validates; Phase 2 focuses only on freezing LGSSM reference. |
| Veto diagnostics | Old route still admitted; tiny historical diagnostics impossible to represent; LGSSM compact route broken; Phase 2 overclaims fresh memory evidence; unsupported score/scientific claim. |
| Explanatory diagnostics | Suggested extra tests, wording changes, stale artifact notes. |
| Not concluded | No non-LGSSM compact port, no new full score admission, no HMC/posterior/scientific claim. |

## Review Questions

1. Does the updated validator enforce compact-only full admission?
2. Do the tests cover the dangerous old-route-plus-memory-pass case?
3. Does Phase 2 have the right scope and stop conditions?
4. Are there unsupported claims or authority transfers?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
