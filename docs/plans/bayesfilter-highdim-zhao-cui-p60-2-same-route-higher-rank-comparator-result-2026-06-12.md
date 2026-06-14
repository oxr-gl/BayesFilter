# P60-2 Result: Same-Route Higher-Rank Comparator

metadata_date: 2026-06-12
status: BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does the d=18 author-SIR source-route result remain stable against a strictly stronger fixed-rank approximation on the same Zhao-Cui `full_sol` route? |
| Baseline/comparator | `candidate_low`: degree-0/rank-1 bounded P59/P60 source-route row.  `candidate_high`: degree-1/rank-2 bounded P59/P60 source-route row. |
| Primary criterion | Both rows must execute on the same realized 36D `[x_t, x_{t-1}]` route, then pass predeclared log-marginal, normalizer, correction, probe-density, retained-density, memory, and runtime gates. |
| Veto diagnostics | Source-route drift, candidate row failure, nonfinite diagnostics, retained-density unavailable, threshold failure, post-hoc comparator substitution, d=50/d=100 launch. |
| Not concluded | No same-route rank convergence, no correctness candidate, no d=50/d=100 scaling, no HMC readiness. |

## Implementation

Changed code:

- `bayesfilter/highdim/source_route.py`
  - Added explicit P60-2 status constants.
  - Added `P60AuthorSIRSameRouteRankComparatorResult`.
  - Added optional `fit_rank` to the P59 author-SIR fixed-TTSIRT prep and
    step-spec assembly helpers.  Defaults remain rank 1.
  - Added `p60_author_sir_same_route_rank_comparator(...)`, which runs the
    fixed `candidate_low`/`candidate_high` rows and fails closed.
- `bayesfilter/highdim/__init__.py`
  - Exported P60-2 constants, result class, and helper.
- `tests/highdim/test_p60_author_sir_rank_comparator.py`
  - Added focused tests for default rank-1 compatibility, rank-2 prep,
    fail-closed P60-2 behavior, non-stronger rank rejection, and incoherent
    pass rejection.

## Result

P60-2 is blocked.

| Field | Value |
| --- | --- |
| Status | `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` |
| Candidate low | `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY` |
| Candidate high | blocked by exception during source-route assembly |
| High-row blocker | `candidate_high_exception_ValueError_NORMALIZER_FLOOR_EXCEEDED` |
| Low rank tuple | `(1, ..., 1)` over 37 rank entries |
| Low fit degree | `0` |
| High planned rank tuple | `(1, 2, ..., 2, 1)` |
| High planned fit degree | `1` |

The important thing is that the failure is now visible and recoverable.  The
execution did not substitute a degree-only comparator, did not loosen
tolerances, and did not claim rank convergence.

## Commands Run

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: passed.

```text
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: passed.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -c "import bayesfilter.highdim as h; r=h.p59_author_sir_step_spec_assembly(sample_count=1, fit_sample_count=2, fit_degree=1, fit_rank=2); print(r.status)"
```

Result: failed with `ValueError: NORMALIZER_FLOOR_EXCEEDED` while building the
degree-1/rank-2 high-row transport normalizer.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: `5 passed, 2 warnings` in about 1 minute 32 seconds.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -c "import json, bayesfilter.highdim as h; r=h.p60_author_sir_same_route_rank_comparator(sample_count=1, fit_sample_count=2, low_fit_degree=0, high_fit_degree=1, low_fit_rank=1, high_fit_rank=2); print(json.dumps({'status': r.status, 'blockers': r.blockers, 'low': None if r.low_result is None else r.low_result.status, 'high': None if r.high_result is None else r.high_result.status, 'manifest': r.manifest}, indent=2, sort_keys=True, default=str))"
```

Result: emitted `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` with blocker
`candidate_high_exception_ValueError_NORMALIZER_FLOOR_EXCEEDED`.

TensorFlow printed CUDA plugin import warnings even with
`CUDA_VISIBLE_DEVICES=-1`; these were intentional CPU-only runs and are not GPU
evidence.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Block P60-2. | Not met: the rank-2 high comparator row does not complete. | Candidate high hits `NORMALIZER_FLOOR_EXCEEDED`; no post-hoc comparator substitution was made. | The rank-2 normalizer failure may be due to underdetermined tiny smoke data, rank-2 initialization/scaling, or a real limitation in the bounded fixed-TTSIRT helper. | Create a focused P60-2 repair subplan for the rank-2 normalizer floor before rerunning this gate. | No rank convergence, correctness candidate, scaling, or HMC readiness. |

## Token

`BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE`
