# Experiment plan: actual-transformed-sv-source-scope-sgqf-unlock

metadata_date: 2026-06-24
program_id: actual-transformed-sv-source-scope-sgqf-unlock
status: DRAFT_PENDING_IMPLEMENTATION
master_context:
- `docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-two-lane-filter-comparison-p7-closeout-and-leaderboard-result-2026-06-24.md`

## Question
Can we add a **same-target value-only SGQF evaluator** for
`zhao_cui_sv_actual_nongaussian_T1000` so the source-scope highdim leaderboard
can execute SGQF on the actual transformed non-Gaussian SV row honestly, using
existing exact transformed-SV dense machinery as the primary comparator?

## Mechanism being tested
The mechanism is an **augmented-noise SGQF precursor route** for the actual
transformed non-Gaussian SV family, used as the first engineering unlock before
any same-target source-scope admission claim is made.

Concretely, this plan tests whether we can:
1. build an SGQF execution path mirroring the existing augmented-noise structural
   route pattern already used by the source-row approximate executors,
2. validate that precursor route on short-horizon / short-prefix fixtures,
3. and only then decide in a later admission gate whether the row can be
   promoted beyond engineering/diagnostic status.

## Scope
- Variant: value-only SGQF unlock for `zhao_cui_sv_actual_nongaussian_T1000`
- Objective: same-target source-scope SGQF evaluator and test-suite coverage
- Seed(s): reuse the source-row dataset and truth theta already frozen in the existing numeric runner artifacts
- Training steps: N/A
- HMC/MCMC settings: none; this is not an HMC readiness experiment
- XLA/JIT mode: none required for the first pass
- Expected runtime: short-prefix checks under a few minutes; full T1000 smoke may take several minutes depending on retained-grid / quadrature choices

## Governing references
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `bayesfilter/highdim/sv_mixture_cut4.py`
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`

## Target identity
This plan governs an **augmented-noise SGQF precursor route** for the family
surrounding the actual transformed non-Gaussian SV source row:
- `zhao_cui_sv_actual_nongaussian_T1000`

It is **not** yet a direct same-target admission plan for that row.

It is **not**:
- the KSC Gaussian-mixture surrogate target,
- a transformed-residual diagnostic target,
- or a silent relabeling of an augmented-observation-noise approximation as the
  final source-row identity.

The later master-program admission gate must still decide whether this precursor
route can be promoted toward the actual transformed source-row identity.

## Baseline / comparator
Primary first-pass comparator:
- the existing source-row augmented-noise approximate route semantics already used
  by the current deterministic executors.

Later admission comparator (not the first engineering gate):
- the existing exact transformed-SV dense reference / same-target exact
  machinery already exercised in the repo.

Secondary explanatory comparator:
- the current source-row Zhao-Cui scalar dense route.

The later same-target comparator is the promotion oracle. The first-pass
engineering unlock should not pretend the precursor route is already same-target
admitted.

## Success criteria
Primary:
- A same-target SGQF **value** evaluator exists for the actual transformed SV
  row and can be named with explicit implementation entry points.
- On short-horizon / short-prefix checks, SGQF value stays close enough to the
  same-target dense/exact reference to justify source-row smoke integration.
- The source-row runner can emit an SGQF executed value cell for
  `zhao_cui_sv_actual_nongaussian_T1000` without silently changing the target.
- The highdim leaderboard can show SGQF on this row as executed value-only.

Secondary:
- Nonclaims remain explicit:
  - no surrogate substitution,
  - no score/Hessian claim,
  - no HMC readiness,
  - no production SV readiness.

Sanity checks:
- short-prefix SGQF value is finite,
- dense/exact reference value is finite,
- target metadata explicitly keeps this row distinct from the KSC surrogate row,
- no silent fallthrough to the current KSC SGQF route.

## Diagnostics
Primary:
- absolute SGQF-vs-dense/exact value gap on short prefixes,
- refinement behavior as retained-grid / SGQF settings change,
- source-row full-horizon finite-value smoke,
- correct row-status transition in runner / leaderboard artifacts.

Secondary:
- runtime / point-count diagnostics,
- memory diagnostics where available,
- comparison against current UKF / Zhao-Cui source-row values as explanatory context only.

Sanity checks:
- no KSC surrogate substitution,
- no augmented-noise substitution,
- no target-identity drift in emitted artifacts.

## Expected failure modes
- The current SGQF machinery may be too Gaussian-observation-specific and may
  require a deeper core extension rather than a thin wrapper.
- Short-prefix value may fail to match the same-target dense/exact reference
  well enough to justify source-row promotion.
- Full T1000 execution may be too expensive or unstable without additional
  staged retained-grid constraints.

## What would change our mind
- If the SGQF path can only run by switching to the KSC surrogate target, keep
  the row blocked.
- If short-prefix SGQF-vs-dense disagreement remains too large after reasonable
  settings refinement, keep the row blocked or demote it to diagnostic-only.
- If the full T1000 smoke is nonfinite or unstable after a successful short-
  prefix phase, stop at short-prefix evidence and do not promote the source-row
  leaderboard cell.

## Skeptical plan audit
Wrong baseline risk:
- Avoid treating the KSC surrogate route as if it were the actual transformed-SV
  same-target baseline.

Proxy-metric risk:
- Finite execution, runtime, or leaderboard emission do not unlock the row by
  themselves. Promotion requires same-target agreement evidence.

Hidden-assumption risk:
- Do not assume the existing SGQF surrogate route can be widened to the actual
  transformed target without real evaluator work.

Unfair-comparison risk:
- Do not compare SGQF on a surrogate or augmented route against the exact
  transformed-SV row and call it same-target.

Artifact-answer mismatch risk:
- Updating only the highdim leaderboard harness is insufficient; runner and
  row-contract tests must move together with the evaluator.

Audit verdict:
- Proceed with a staged value-only unlock. Start with short-prefix same-target
  SGQF vs dense/exact checks before touching the full T1000 runner path.

## Files likely to modify
Primary implementation files:
- `bayesfilter/highdim/sv_mixture_cut4.py`
- possibly a new SGQF actual-transformed-SV helper adjacent to it or in a nearby
  SGQF-specific file
- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`

Primary tests to extend or add:
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`

## Execution order
1. Add a short-prefix same-target SGQF actual-transformed-SV value evaluator and
   test it against the dense/exact reference.
2. Add refinement / stability checks for that short-prefix SGQF value path.
3. Add a source-row runner branch for SGQF actual-transformed-SV value-only execution.
4. Update row-contract tests so the actual-transformed-SV source row becomes SGQF
   executed value-only rather than blocked.
5. Re-emit the highdim leaderboard packet.
6. Run focused CPU-only verification.

## Command
First-pass verification commands once implementation exists:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

```bash
python -m compileall -q scripts docs/benchmarks tests/highdim
```

## Interpretation rule
- If SGQF value agrees adequately with the same-target dense/exact reference on
  short prefixes and the full T1000 smoke is finite, then promote the source-row
  SGQF cell to executed value-only.
- If SGQF only runs by changing the target identity, keep the row blocked.
- If short-prefix agreement is poor or unstable, stop before source-row
  promotion and write a blocked result note instead of a misleading unlock.
