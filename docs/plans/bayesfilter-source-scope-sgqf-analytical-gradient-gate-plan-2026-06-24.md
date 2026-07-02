# Experiment plan: source-scope-sgqf-analytical-gradient-gate

metadata_date: 2026-06-24
program_id: source-scope-sgqf-analytical-gradient-gate
status: DRAFT_PENDING_IMPLEMENTATION
master_context:
- `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md`
- `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-subplan-2026-06-23.md`

## Question
For each source-scope SGQF family, what evidence is required before the row may
be promoted from **value-only** to **analytical-score admitted**, and which rows
currently remain diagnostic-score-only or blocked for analytical-gradient claims?

## Mechanism being tested
The mechanism is the family-by-family analytical-gradient gate for SGQF source-
scope rows.

This plan does **not** assume that every value-capable SGQF row is already score-
capable. Instead it tests whether each family has:
1. an explicit analytical derivative route,
2. same-branch finite-difference validation,
3. target-consistent score semantics,
4. and a reviewed promotion path for source-scope score claims.

## Scope
Families to classify:
- source-scope LGSSM
- KSC surrogate SV source row
- actual transformed SV source row
- predator-prey source row
- generalized SV source row
- spatial SIR source row

Expected statuses per family:
- `analytical_score_admitted`
- `value_only_executed`
- `diagnostic_score_only`
- `blocked_missing_analytical_route`
- `blocked_not_same_target`
- `blocked_no_free_theta`

## Governing references
- `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p3-analytical-score-kernel-certification-subplan-2026-06-23.md`
- `docs/plans/bayesfilter-fixed-sgqf-leaderboard-promotion-p4-ksc-surrogate-analytical-wrapper-score-subplan-2026-06-23.md`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_p47_predator_prey_filtering.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`

## Why this plan is needed
The current family unlock plans are mostly value-first. That is why the
analytical-gradient tests are missing from those row plans: most rows are not yet
past the value-route stage.

This plan adds the missing unifying rule so the repo can answer, consistently:
- which unlocked SGQF source-scope rows are value-only,
- which have enough reviewed evidence for analytical-score claims,
- and which remain blocked for score reasons even after value unlock.

## Success criteria
Primary:
- A source-scope SGQF analytical-gradient ledger exists with one explicit score
  status for every family row.
- Existing analytical-score-support rows (for example, the SGQF KSC tiny-fixture
  path and predator-prey family tests) are reconciled honestly into source-scope
  statuses rather than silently widened.
- The runner / leaderboard artifacts can distinguish value-only execution from
  analytical-score admission.

Secondary:
- finite-difference validation fixtures are named explicitly for every candidate
  analytical-score row,
- autodiff remains diagnostic-only unless a reviewed exception is written,
- no-free-theta rows are classified explicitly as such.

## Diagnostics
Primary:
- existence of explicit analytical derivatives,
- same-branch finite-difference agreement,
- source-scope score target consistency,
- row-by-row blocker reasons.

Secondary:
- runtime / memory / branch metadata,
- autodiff agreement checks as explanatory only.

## Expected failure modes
- family plans may have value support without any reviewed source-scope score route,
- tiny-fixture analytical-score evidence may be over-read as source-scope score admission,
- source rows with no free theta (for example, spatial SIR) may be wrongly treated as score-blocked instead of no-free-theta value-only.

## What would change our mind
- If a family lacks an explicit analytical derivative route or same-branch FD
  evidence, it should remain value-only or blocked for score claims.
- If a family’s only score evidence comes from autodiff, that is not enough for
  source-scope analytical-score promotion under the current repo policy.

## Files likely to modify
- `tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- family-specific test files that currently provide SGQF score evidence:
  - `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
  - `tests/highdim/test_p47_predator_prey_filtering.py`

## Execution order
1. Write a family-by-family SGQF analytical-gradient ledger.
2. Classify existing family score evidence as source-scope-admitted, tiny-fixture-only, diagnostic-only, no-free-theta, or blocked.
3. Update gradient-semantics / source-scope tests to enforce that ledger.
4. Update the highdim leaderboard artifact to carry explicit score-status fields where relevant.
5. Run focused CPU-only verification.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_p47_predator_prey_filtering.py
```

```bash
python -m compileall -q docs/benchmarks tests/highdim
```

## Interpretation rule
- If a family has explicit analytical derivatives plus same-branch FD validation
  on the source-scope target (or a reviewed source-scope-equivalent target), it
  may be promoted to `analytical_score_admitted`.
- If a family has only value execution, keep it `value_only_executed`.
- If score evidence exists only on a tiny fixture or via autodiff, keep it
  `diagnostic_score_only` or `blocked_missing_analytical_route` rather than
  over-promoting it.
