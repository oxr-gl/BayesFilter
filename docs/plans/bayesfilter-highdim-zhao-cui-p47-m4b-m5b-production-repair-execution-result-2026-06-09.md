# P47 M4b/M5b Production Repair Execution Result

metadata_date: 2026-06-09
program: P47-production-repair
status: `REVIEWED_BLOCKER_CLOSEOUT`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Do not emit M4b or M5b production tokens from the current routes. |
| Primary criterion status | M4b blocked by route architecture preflight; M5b blocked by production accuracy/tuning gate. |
| Veto diagnostic status | No finite-output-as-correctness promotion; no lower-rung-to-production promotion; no S&P 500, adaptive MATLAB reproduction, production score API, or production HMC claim. |
| Main uncertainty | Whether a route amendment, time-local coordinate map, adaptive/low-rank propagation route, or different production comparator can repair these rows. |
| Next justified action | Ask Claude to review the blockers; if accepted, create separate route-amendment plans rather than loosening tolerances. |
| Not concluded | No production spatial SIR filtering and no production predator-prey filtering. |

## M4b Result

Status: `BLOCKED_M4B_ROUTE_ARCHITECTURE`.

The current multistate Zhao--Cui route retains all state axes on a
tensor-product grid.  The preflight cap is `50_000_000` pairwise transition
evaluations on CPU.

| Candidate | Sites J | State Dim | Order | Grid Points | Pairwise Evaluations | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| M4b-0 | 3 | 6 | 3 | 729 | 531441 | Feasibility only, below near-paper |
| M4b-1 | 5 | 10 | 3 | 59049 | 3486784401 | Blocked by cap |
| M4b-2 | 9 | 18 | 3 | 387420489 | 150094635296999121 | Blocked by cap |

Token not emitted:

```text
PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING
```

## M5b Result

Status: `BLOCKED_M5B_PRODUCTION_ACCURACY_TUNING`.

The horizon-25 same-target candidate ran deterministically and finitely, but
failed reviewed production tolerances.

| Metric | Tolerance | Observed |
| --- | ---: | ---: |
| Absolute log-likelihood gap | `< 5.0` | `145.7760213472871` |
| Maximum step log-normalizer gap | `< 1.0` | `11.414750146529755` |
| Maximum state-mean component error | `< 5.0` | `19.45492436940154` |
| Maximum covariance-entry error | `< 8.0` | `44.61958715970044` |
| Truth-path prey RMSE | `< 8.0` | `2.99204937` |
| Truth-path predator RMSE | `< 2.0` | `0.96692767` |
| Deterministic replay | required | `PASS` |

Quick tuning probes with higher order, higher rank, and several coordinate
windows returned `CONDITION_NUMBER_VETO`; they did not repair the production
row.

Token not emitted:

```text
PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING
```

## Local Commands

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-production-row-manifest-2026-06-09.json
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p47-m5b-production-row-manifest-2026-06-09.json
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim tests/highdim/test_p47_m4b_m5b_production_repair.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-m5b-production-repair-master-program-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-spatial-sir-production-row-subplan-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p47-m5b-predator-prey-production-row-subplan-2026-06-09.md docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-production-row-manifest-2026-06-09.json docs/plans/bayesfilter-highdim-zhao-cui-p47-m5b-production-row-manifest-2026-06-09.json docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-m5b-production-repair-claude-review-ledger-2026-06-09.md tests/highdim/test_p47_m4b_m5b_production_repair.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p47_m4b_m5b_production_repair.py
```

Initial focused pytest result before blocker repair:

```text
1 failed, 3 passed
```

The failure was the intended production criterion failure: M5b horizon 25 did
not satisfy the declared tolerance.  Codex then repaired the test/artifacts to
record the blocker instead of forcing a production pass.

## Claude Review

Claude returned:

```text
PASS_P47_PRODUCTION_REPAIR_BLOCKER_REVIEW
```

Claude accepted the blocker closeout and noted that follow-on artifacts should
decompose the M4b route-architecture amendment and M5b coordinate-map or
propagation-route amendment before any new execution attempt.
