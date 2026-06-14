# P52-M2 Result: Memory-Bounded Rank Ceiling Protocol

metadata_date: 2026-06-10
phase: P52-M2
status: PASS_P52_M2_MEMORY_RANK_CEILING
supervisor: Codex
reviewer: Claude Code read-only

## Decision

P52-M2 passes after local validation and Claude read-only review.  BayesFilter
now has a deterministic rank-budget preflight protocol that computes
`M_state`, `M_step`, `r_max`, feasible candidate ranks, and pass/block
classifications before a spatial SIR filtering row is allowed to run.

This phase is memory and rank feasibility only.  It does not establish
filtering correctness, production spatial SIR readiness, HMC readiness, GPU
readiness, or d=100 filtering correctness.

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | The implementation computes a hard rank ceiling from a 32 GB practical memory cap before running a rank ladder. |
| Baseline/comparator | P51-M3 all-pairs blocker, P52 master memory policy, and P30 M1 memory equations. |
| Primary criterion | Passed locally: `RankBudgetConfig`, memory formulas, `r_max`, candidate truncation, empty-budget blocker, and d=18/d=50/d=100 manifest are implemented and tested. |
| Veto diagnostics | Passed locally: ranks cannot grow beyond `r_max`; state-core memory is not the sole estimate; `R_eff` source is required; d=100 is labeled memory preflight only. |
| Not concluded | No accuracy, filtering correctness, production spatial SIR readiness, HMC readiness, GPU readiness, or exact posterior correctness. |

## Implementation

Added:

- `bayesfilter/highdim/rank_budget.py`
- internal `bayesfilter.highdim` exports for the rank-budget protocol
- `tests/highdim/test_p52_rank_budget.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p52-m2-memory-rank-ceiling-manifest-2026-06-10.json`

The default rank candidates are `{2, 4, 8, 16, 32}` with:

- physical cap: 32 GiB;
- algorithm cap: 16 GiB;
- single-step cap: 8 GiB;
- dtype bytes: 8;
- basis size: 3;
- conservative `R_eff = 16`;
- workspace multiplier `omega = 8`.

## Manifest Summary

| d | r_max | feasible ranks | claim class |
| --- | ---: | --- | --- |
| 18 | 98 | 2, 4, 8, 16, 32 | memory and rank feasibility forecast only |
| 50 | 59 | 2, 4, 8, 16, 32 | memory and rank feasibility forecast only |
| 100 | 41 | 2, 4, 8, 16, 32 | memory and rank feasibility forecast only |

These rows say that the declared rank candidates fit the conservative M2
workspace formula.  They do not say that the factorized route exists, that
`R_eff = 16` is empirically measured for spatial SIR, or that any filtering row
is accurate.

## Validation

Focused CPU-only validation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p52_rank_budget.py
python -m compileall -q bayesfilter/highdim/rank_budget.py tests/highdim/test_p52_rank_budget.py
git diff --check -- bayesfilter/highdim/rank_budget.py bayesfilter/highdim/__init__.py tests/highdim/test_p52_rank_budget.py docs/plans/bayesfilter-highdim-zhao-cui-p52-m2-memory-rank-ceiling-manifest-2026-06-10.json
```

Outcomes:

- pytest passed: `6 passed, 2 warnings in 5.65s`;
- compileall passed;
- git diff whitespace check passed.

The warnings came from TensorFlow Probability deprecation messages during the
existing broad `bayesfilter.highdim` import path.  GPU was intentionally hidden
with `CUDA_VISIBLE_DEVICES=-1`; no GPU claim is made.

Claude read-only review iteration 1 returned `VERDICT: AGREE`.  Claude found no
blocking baseline drift, proxy-metric promotion, stop-condition gap, `R_eff`
overclaim, d=100 overclaim, or artifact mismatch.  Claude noted one nonblocking
API-hardening item: if `p52_spatial_sir_rank_budget_manifest()` is reused later
with non-default arguments, its top-level status should be derived from row
outcomes rather than hardcoded to pass.

## Nonclaims

- No filtering correctness.
- No production spatial SIR readiness.
- No HMC readiness.
- No GPU readiness.
- No d=100 filtering correctness.
- No empirical measurement that `R_eff = 16` is sufficient for the repaired
  spatial SIR transition route.
