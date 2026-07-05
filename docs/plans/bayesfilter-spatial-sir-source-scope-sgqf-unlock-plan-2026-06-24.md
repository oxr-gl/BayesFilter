# Experiment plan: spatial-sir-source-scope-sgqf-unlock

metadata_date: 2026-06-24
program_id: spatial-sir-source-scope-sgqf-unlock
status: DRAFT_PENDING_ROUTE_DEVELOPMENT
master_context:
- `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-two-lane-filter-comparison-p7-closeout-and-leaderboard-result-2026-06-24.md`

## Question
Can we build a **reviewed SGQF source-scope value route** for
`zhao_cui_spatial_sir_austria_j9_T20` that is memory-bounded, route-honest, and
consistent with the repo’s current factorized-transition governance, so the
source-scope highdim leaderboard can execute SGQF on the spatial SIR row
honestly?

## Mechanism being tested
The mechanism is **not** just a leaderboard wiring patch. This plan tests whether
we can first establish a reviewed SGQF route class for source-scope spatial SIR:
- no dense all-pairs retained-grid transition materialization,
- deterministic replay,
- TensorFlow implementation,
- explicit memory metadata,
- lower-rung tie-out before source-scope promotion.

## Scope
- Variant: source-scope SGQF unlock for `zhao_cui_spatial_sir_austria_j9_T20`
- Objective: reviewed value-only SGQF route class and leaderboard admission path
- Seed(s): deterministic replay required
- Training steps: N/A
- HMC/MCMC settings: none; this is not an HMC readiness experiment
- XLA/JIT mode: not required for the first unlock milestone
- Expected runtime: multi-phase route-development effort; not a one-step evaluator patch

## Governing references
- `bayesfilter/highdim/transition_route.py`
- `bayesfilter/highdim/rank_budget.py`
- `bayesfilter/highdim/source_route.py`
- `tests/highdim/test_p51_spatial_sir_route_preflight.py`
- `tests/highdim/test_p52_factorized_transition_route.py`
- `tests/highdim/test_p53_lower_rung_streaming_route.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`

## Target identity
This unlock is for the **source-scope spatial SIR row**:
- `zhao_cui_spatial_sir_austria_j9_T20`

It is **not**:
- a dense all-pairs retained-grid route,
- a lower-rung tie-out being mislabeled as source-scope readiness,
- a scout-only diagnostic route,
- or an execution-only placeholder being promoted to a leaderboard row.

## Baseline / comparator
Primary comparator / gate:
- the transition-route contract itself: a passing SGQF source-scope route must
  satisfy the factorized / streamed transition requirements already expressed in
  `bayesfilter/highdim/transition_route.py`.

Secondary explanatory comparators:
- existing lower-rung dense-equivalent route tests,
- existing UKF value-only source-row behavior,
- existing route/rank-selection blocker tests.

These are explanatory only. The primary pass criterion is an honest route class,
not merely “some finite number came out.”

## Success criteria
Primary:
- A reviewed SGQF route class exists for spatial SIR that does not materialize
  dense all-pairs transitions and preserves deterministic replay.
- Lower-rung / factorized-route tests pass before any source-scope promotion.
- The source-row runner can emit an SGQF executed value-only cell for
  `zhao_cui_spatial_sir_austria_j9_T20` only after the route contract passes.
- The highdim leaderboard can show SGQF on this row as executed value-only,
  still preserving the row’s no-free-theta boundary where applicable.

Secondary:
- memory metadata is emitted,
- route class and nonclaims are explicit,
- source-scope row stays separate from any lower-rung tie-out artifact.

Sanity checks:
- no dense all-pairs transition interface appears,
- route remains deterministic under replay,
- lower-rung tie-out is not over-interpreted as d=18 source-scope readiness.

## Diagnostics
Primary:
- route-class pass/fail against the factorized-transition contract,
- lower-rung dense-equivalent tie-out,
- source-row finite value smoke,
- memory and route metadata.

Secondary:
- runtime / memory measurements,
- explanatory comparison to current UKF value-only source-row execution.

Sanity checks:
- no forbidden transition interface,
- no silent route fallback,
- no promotion of scout-only or lower-rung evidence into source-scope correctness.

## Expected failure modes
- The required factorized/staged SGQF transition route may not exist yet and may
  require substantial new algorithmic work.
- Lower-rung dense-equivalent tie-out may pass while the source-scope route still
  fails memory or scaling constraints.
- The source row may remain no-free-theta value-only even after route unlock,
  limiting what the leaderboard can honestly claim.

## What would change our mind
- If the only way to run SGQF is through a forbidden dense all-pairs transition,
  keep the row blocked.
- If lower-rung evidence cannot be carried into a route class with deterministic
  replay and memory metadata, keep the source-row leaderboard cell blocked.
- If the source-row smoke is unstable or route-inconsistent after lower-rung
  success, stop before leaderboard promotion.

## Skeptical plan audit
Wrong baseline risk:
- Avoid treating an existing UKF or DPF source-row result as proof that SGQF has
  a valid source-scope route.

Proxy-metric risk:
- Finite execution, runtime, or a lower-rung tie-out do not unlock the row by
  themselves. Promotion requires a passing route contract.

Hidden-assumption risk:
- Do not assume that because the row has no free theta, any value-only route is
  acceptable; the transition-route class still matters.

Unfair-comparison risk:
- Do not promote a dense all-pairs or scout-only route into the source-scope
  leaderboard.

Artifact-answer mismatch risk:
- Updating only the leaderboard harness is insufficient; route/preflight/runner
  tests must move together with the new SGQF route class.

Audit verdict:
- Treat spatial SIR as a route-development program first and a leaderboard
  integration task second.

## Files likely to modify
Primary implementation files:
- `bayesfilter/highdim/transition_route.py`
- `bayesfilter/highdim/rank_budget.py`
- `bayesfilter/highdim/source_route.py`
- likely additional SGQF-specific transition application support in the highdim stack
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`

Primary tests to extend or add:
- `tests/highdim/test_p51_spatial_sir_route_preflight.py`
- `tests/highdim/test_p52_factorized_transition_route.py`
- `tests/highdim/test_p53_lower_rung_streaming_route.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`

## Execution order
1. Confirm and document the current SGQF spatial SIR blocker as a route-class blocker.
2. Add or extend lower-rung / factorized-route SGQF tests with deterministic replay and memory metadata.
3. Implement the reviewed SGQF transition-route class needed for source-scope spatial SIR.
4. Add a source-row SGQF value-only runner branch only after the route contract passes.
5. Update row-contract tests so the spatial SIR source row becomes SGQF executed value-only rather than blocked.
6. Re-emit the highdim leaderboard packet.
7. Run focused CPU-only verification.

## Command
First-pass verification commands once implementation exists:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p51_spatial_sir_route_preflight.py \
  tests/highdim/test_p52_factorized_transition_route.py \
  tests/highdim/test_p53_lower_rung_streaming_route.py \
  tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

```bash
python -m compileall -q scripts docs/benchmarks tests/highdim
```

## Interpretation rule
- If a reviewed SGQF spatial SIR route passes the factorized-transition
  contract, lower-rung tie-out, and source-row finite-value smoke, then promote
  the row to executed value-only in the highdim leaderboard.
- If the route still depends on forbidden dense all-pairs transitions, keep the
  row blocked.
- If lower-rung success does not scale to a valid source-row route, stop before
  leaderboard promotion and record the blocker explicitly.
