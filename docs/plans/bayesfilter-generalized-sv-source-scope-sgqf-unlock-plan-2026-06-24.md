# Experiment plan: generalized-sv-source-scope-sgqf-unlock

metadata_date: 2026-06-24
program_id: generalized-sv-source-scope-sgqf-unlock
status: DRAFT_PENDING_IMPLEMENTATION
master_context:
- `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-two-lane-filter-comparison-p7-closeout-and-leaderboard-result-2026-06-24.md`

## Question
Can we add a **same-target value-only SGQF evaluator** for
`zhao_cui_generalized_sv_synthetic_from_estimated_values` so the source-scope
highdim leaderboard can execute SGQF on that row honestly, using the repo’s
existing native generalized-SV dense reference as the primary comparator?

## Mechanism being tested
The mechanism is an **augmented-noise SGQF precursor route** for the
generalized-SV source family, used as the first engineering unlock before any
same-target source-scope admission claim is made.

Concretely, this plan tests whether we can:
1. evaluate a generalized-SV augmented-noise SGQF route that remains consistent
   with the source-row synthetic prior-mean target,
2. validate the precursor route first on short-prefix fixtures,
3. and only then decide in a later admission gate whether the row can be
   promoted beyond engineering/diagnostic status.

## Scope
- Variant: value-only SGQF unlock for `zhao_cui_generalized_sv_synthetic_from_estimated_values`
- Objective: same-target source-scope SGQF evaluator and test suite coverage
- Seed(s): reuse existing source-row synthetic prior-mean dataset seed / fixture already frozen in the runner artifacts
- Training steps: N/A
- HMC/MCMC settings: none; this is not an HMC readiness experiment
- XLA/JIT mode: none required for the first pass
- Expected runtime: short-prefix checks under a few minutes; full-row smoke potentially several minutes, depending on retained grid / quadrature choices

## Governing references
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- `tests/highdim/test_p51_native_generalized_sv_reference.py`
- `tests/highdim/test_p45_generalized_sv_comparison_blocker.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `bayesfilter/highdim/native_generalized_sv.py`
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`

## Target identity
This plan governs an **augmented-noise SGQF precursor route** for the source-
scope generalized SV family:
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`

It is **not** yet a direct same-target admission plan for the source-row SGQF
score claim.

It is **not**:
- the KSC Gaussian-mixture surrogate SV target,
- a transformed-residual diagnostic target,
- an augmented-noise approximation being silently re-labeled as same-target,
- or the native lower-rung reference alone.

The later master-program admission gate must still decide whether this precursor
route can be promoted toward the native raw-y generalized-SV source-row identity.

## Baseline / comparator
Primary first-pass comparator:
- the existing source-row augmented-noise approximate route semantics already used
  by the current deterministic executors.

Later admission comparator (not the first engineering gate):
- the existing native dense same-target generalized-SV reference in
  `bayesfilter/highdim/native_generalized_sv.py`

Secondary explanatory comparator:
- the existing source-row UKF augmented-noise value path in
  `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`

The later same-target comparator is the promotion oracle. The first-pass
engineering unlock should not pretend the precursor route is already same-target
admitted.

## Success criteria
Primary:
- A same-target SGQF **value** precursor evaluator exists for generalized SV and
  can be named with explicit implementation entry points.
- On short-prefix / short-fixture checks, the SGQF value stays close enough to
  the native dense reference to justify source-row smoke integration.
- The source-row runner can emit an SGQF executed value cell for
  `zhao_cui_generalized_sv_synthetic_from_estimated_values` without silently
  changing the target identity.
- The highdim leaderboard can show SGQF on this row as executed value-only.

Secondary:
- The emitted SGQF row preserves explicit nonclaims:
  - no score/Hessian claim,
  - no HMC readiness,
  - no production generalized-SV readiness,
  - no Zhao-Cui same-target equality claim unless separately established.

Sanity checks:
- short-prefix SGQF value is finite,
- dense reference value is finite,
- target metadata / nonclaims clearly preserve raw-y generalized SV identity,
- the leaderboard keeps actual transformed SV, KSC surrogate SV, and generalized
  SV as separate rows.

## Diagnostics
Primary:
- absolute SGQF-vs-dense value gap on short prefixes,
- refinement behavior as dense order / SGQF settings increase,
- source-row full-horizon finite-value smoke,
- correct row status transition in runner / leaderboard artifacts.

Secondary:
- runtime / point-count diagnostics,
- memory diagnostics where available,
- comparison against current UKF source-row value as explanatory context only.

Sanity checks:
- no transformed-residual substitution,
- no KSC surrogate substitution,
- no silent fallthrough to an existing augmented-noise path.

## Expected failure modes
- The current SGQF machinery may be too Gaussian-observation-specific and may
  need a deeper core extension rather than a thin wrapper.
- Short-prefix value may fail to match the dense native reference well enough to
  justify source-row promotion.
- The source-row target identity may require additional parameter/observation
  plumbing not currently exposed by the runner.
- The full-horizon source row may be too expensive without additional staged
  settings or retained-grid constraints.

## What would change our mind
- If the SGQF path can only run by changing the target identity, we should keep
  the row blocked.
- If short-prefix SGQF-vs-dense disagreement remains too large after reasonable
  settings refinement, we should keep the row blocked or demote it to
  diagnostic-only.
- If the full source-row smoke is numerically unstable or nonfinite even after a
  reviewed short-prefix pass, we should stop at the short-prefix evidence stage
  and not promote the source-row leaderboard cell.

## Skeptical plan audit
Wrong baseline risk:
- Avoid using the current source-row UKF augmented-noise path as the promotion
  anchor. The dense native generalized-SV reference is the primary comparator.

Proxy-metric risk:
- Finite execution, low runtime, or successful artifact emission do not unlock
  the row by themselves. Promotion requires same-target agreement evidence.

Hidden-assumption risk:
- Do not assume that because generalized SV has a dense same-target reference,
  SGQF can already target it without new evaluator work.

Unfair-comparison risk:
- Do not compare SGQF on a transformed or approximated target against a dense
  native raw-y reference and call it same-target.

Artifact-answer mismatch risk:
- Updating only the highdim leaderboard harness is insufficient; the runner and
  row-contract tests must move together with the evaluator.

Audit verdict:
- Proceed with a staged value-only unlock. Start with short-prefix same-target
  SGQF vs dense checks before touching the full source-row runner path.

## Files likely to modify
Primary implementation files:
- `bayesfilter/highdim/native_generalized_sv.py`
- possibly a new SGQF generalized-SV helper adjacent to it or in a nearby
  SGQF-specific file
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`

Primary tests to extend or add:
- `tests/highdim/test_p51_native_generalized_sv_reference.py`
- `tests/highdim/test_p45_generalized_sv_comparison_blocker.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`

## Execution order
1. Add an augmented-noise SGQF generalized-SV precursor route and test it first
   on short-prefix fixtures.
2. Compare that precursor route against the native dense same-target reference on
   short prefixes.
3. Add a source-row runner branch for SGQF generalized-SV value-only execution.
4. Update row-contract tests so the generalized-SV source row can transition from
   blocked to executed value-only only if the precursor route passes the later
   same-target admission gate.
5. Re-emit the highdim leaderboard packet.
6. Run focused CPU-only verification.

## Command
First-pass verification commands once implementation exists:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p51_native_generalized_sv_reference.py \
  tests/highdim/test_p45_generalized_sv_comparison_blocker.py \
  tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

```bash
python -m compileall -q scripts docs/benchmarks tests/highdim
```

## Interpretation rule
- If SGQF value agrees adequately with the native dense reference on short
  prefixes and the source-row smoke is finite, then promote the source-row SGQF
  cell to executed value-only.
- If SGQF only runs by changing the target identity, keep the row blocked.
- If short-prefix agreement is poor or unstable, stop before source-row
  promotion and write a blocked result note instead of a misleading unlock.
