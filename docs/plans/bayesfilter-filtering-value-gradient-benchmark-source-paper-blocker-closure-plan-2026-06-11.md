# Source-Paper Benchmark Blocker-Closure Plan

metadata_date: 2026-06-11
phase: FILTER_BENCH_SOURCE_PAPER_BLOCKER_CLOSURE
status: PLAN_DRAFT_PENDING_CLAUDE_REVIEW
supervisor: Codex
executor: Codex in this dialogue
reviewer: Claude Code read-only, opus max effort

## Objective

Repair the benchmark plan/runbook after the source-prior audit changed the
scope.  The current benchmark execution should use exact author-paper or
reviewed author-code model values as tests.  BayesFilter-only P44
cubic/quadratic/tanh diagnostic fixtures must be excluded from the promoted
source-paper benchmark scope.

This plan does not erase historical P1/P7/P8 artifacts that intentionally
preserved the earlier 7 x 12 diagnostic roster.  Instead it creates a
superseding source-paper scope contract, updates the visible runbook so future
execution follows that contract, and records which remaining items are fixable
implementation tasks rather than scientific blockers.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What fixable blockers must be closed before the filtering benchmark can use exact source-paper/code values across the in-scope model families? |
| Baseline/comparator | P10 truth-prior literature audit, Zhao--Cui paper/code values, current P8 synthetic-truth contract, P9 numeric-pending closeout, visible runbook, and local target/preflight artifacts. |
| Primary criterion | Emit a reviewed source-paper scope contract under `docs/plans` that removes P44 diagnostic rows from the promoted benchmark, locks source values for in-scope rows, classifies project-only/lower-rung rows, and updates the runbook/master notes so the next execution phase uses this scope. |
| Veto diagnostics | Reintroducing P44 diagnostic rows into the promoted source-paper benchmark; treating lower-rung/project fixtures as paper rows; silently dropping a source-paper model; treating missing numeric benchmark values as filter performance; using old LEDH-PFPF-OT as current evidence; changing criteria after seeing numeric results. |
| Explanatory diagnostics | P7/P8 historical roster status, P10 source ledger, focused schema tests, JSON/CSV/Markdown source-scope summaries, Claude read-only findings. |
| Not concluded | This closure does not run the full numeric benchmark, rank filters, certify DPF gradients, certify SIR d=18 value-route readiness, or hand off to Bayesian estimation. |
| Artifacts | Source-paper scope JSON/CSV/Markdown, focused tests, updated runbook/master amendments, execution result note, Claude review ledger entries. |

## Skeptical Plan Audit

Status: PASSED_FOR_SOURCE_SCOPE_REPAIR.

- Wrong baseline risk: the old P8 contract answered a different question:
  preserving the then-frozen diagnostic roster.  The new source-paper benchmark
  must be compared to paper/code values, not to P44 project fixtures.
- Proxy-promotion risk: preflight cells and source-scope rows are not numeric
  performance evidence.  The source-scope contract must mark numeric execution
  pending.
- Stop-condition risk: if a row lacks source support or route readiness, the
  contract must classify it as diagnostic-only, replacement-required, or
  route-repair-required rather than silently advancing.
- Unfair-comparison risk: final numeric runs must use common source values,
  data-generation rules, horizons, seeds, and coordinate conventions across
  algorithms.
- Hidden-assumption risk: lower-rung rows are useful engineering diagnostics
  but are not the same as paper-scale source rows unless the contract says so.
- Stale-context risk: historical P44 and LEDH-PFPF-OT artifacts remain
  provenance only.  Future promoted tables must read the superseding source
  scope.
- Environment-mismatch risk: this phase emits metadata and runs CPU-only tests.
  GPU benchmarks are out of scope.
- Artifact-answer risk: the artifact answers which rows are in scope and what
  remains to repair, not how the filters perform numerically.

## Blockers And Repairs

| Blocker | Current evidence | Repair in this phase | Residual status after repair |
| --- | --- | --- | --- |
| P44 diagnostics still appear in historical P1/P7/P8 roster | P8 contract has 12 model columns including P44 cubic/quadratic/tanh rows | Create a superseding source-paper scope contract excluding all P44 diagnostic rows; update runbook/master amendments to use the source-paper scope for future promoted benchmark execution | Historical artifacts preserved; promoted source-paper scope has no P44 rows |
| LGSSM row uses project P44 coordinates instead of Zhao--Cui paper values | P10 ledger found Zhao--Cui `m=n=3`, `T=50`, truth `(a,d)=(0.8,0.5)`, prior `Uniform([0.4,1]^2)` | Lock a source-paper LGSSM row with these values and mark the old P44 LGSSM row as historical exact-oracle diagnostic | Numeric evaluator still needed for the source-paper row |
| Synthetic SV/KSC need source values, not ad hoc truth draws | P10 ledger found `sigma=1`, truth `(gamma,beta)=(0.6,0.4)`, `T=1000`, prior `Uniform([0.1,0.9]^2)` | Lock actual transformed SV and KSC surrogate rows to these source values; KSC uses same SV truth and fixed mixture target label | KSC mixture-table source citation remains an audit note, not a truth-value blocker |
| Native generalized SV row is not the exact author-code row | P10 ledger found current native generalized SV dense lower-rung is project fixture; author code uses 8-parameter `svmodels` defaults for SP500 | Exclude the project fixture from promoted source-paper scope and add a replacement-required row for the author-code 8-parameter generalized SV values | Adapter/evaluator implementation remains a fixable follow-up before numeric source-paper tables include this row |
| Spatial SIR lower rung is not the paper-scale row; d=18 route is blocked | P10 ledger found Zhao--Cui uses `J=9`, `T=20`, fixed `kappa=0.1`, `nu=18`, initial states `S_j=485+j`, `I_j=15-j`; current d=18 route is blocked by rank selection | Promote only the source-paper `J=9` row; mark J=1 lower-rung as diagnostic-only and d=18 as route-repair-required | Value-route repair required before SIR paper-scale numeric performance |
| Predator-prey values need to be exact paper/code values | P10 ledger found truth `(r,K,a,s,u,v)=(0.6,114,25,0.3,0.5,0.5)`, `x0=(50,5)`, `T=20`, noise `4I`, prior box | Lock source-paper predator-prey row to these values; mark horizon-25 production row as project stress/diagnostic unless explicitly retained outside source-paper tables | Numeric evaluator still needed for source-paper row |
| Generalized SV must use Zhao--Cui estimated values but synthetic data | User amended the target after the first scope contract: use the same values as estimated in Zhao--Cui and generate data from those values, not SP500 returns directly.  Local evidence currently gives the `svmodels` route and author defaults, but not a checked numeric estimated vector. | Replace the SP500 direct-data/replacement-required row with a synthetic `svmodels` row whose promotion intent is retained but whose numeric execution is blocked until the estimated physical parameter vector is extracted, digitized, or regenerated from the author pipeline. | Fixable evidence/implementation blocker: `estimated_values_pending_extraction`; do not substitute author defaults or BayesFilter project fixture values. |
| Numeric benchmark has not run | P8/P9 correctly block numeric closeout | Preserve `numeric_benchmark_status = pending`; next phase must implement accepted source values/data/evaluators | Real benchmark remains pending, but no longer blocked by scope ambiguity |

## Execution Tasks

1. Draft this plan and get Claude read-only review.  Iterate until
   `VERDICT: AGREE` or max five reviews.
2. Add a source-paper scope emitter, or extend the existing P8 emitter with a
   clearly separate source-paper output.  The output must include:
   - in-scope promoted source-paper rows;
   - exact values and source anchors;
   - excluded historical/project diagnostic rows;
   - fixable implementation tasks;
   - numeric execution pending status;
   - nonclaims.
3. Add focused tests that require:
   - no P44 cubic/quadratic/tanh row in promoted source-paper rows;
   - exact Zhao--Cui LGSSM, SV, SIR, and predator-prey values;
   - generalized SV project fixture excluded from promoted rows;
   - generalized SV source route retained as a synthetic-from-estimated-values
     row with numeric execution blocked until the Zhao--Cui estimated vector is
     materialized;
   - lower-rung/project rows separated from promoted source-paper rows;
   - numeric benchmark still pending.
4. Update the visible runbook and master program with an amendment that future
   promoted source-paper benchmark execution uses this scope instead of the
   old P44-inclusive roster.
5. Run focused validation:

   ```bash
   CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py
   python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json
   CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
   CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
   git diff --check -- scripts/filtering_value_gradient_benchmark_emit_source_paper_scope.py tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-blocker-closure-plan-2026-06-11.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-blocker-closure-result-2026-06-11.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-summary-2026-06-11.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-summary-2026-06-11.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-visible-gated-execution-runbook-2026-06-10.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-closure-master-program-2026-06-10.md
   ```

6. Write the execution result note.
7. Ask Claude for execution review.  Repair material findings and retry until
   convergence or max five reviews.
8. Continue the visible execution by recording the next phase: numeric
   source-paper benchmark implementation remains pending after scope repair.

## Claude Review Rule

Claude is read-only.  Each prompt must request exactly:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
MAJOR:
- ...
MINOR:
- ...
```

If Claude does not respond, run the small probe required by the visible
runbook.  If the probe responds, shorten or split the prompt and retry.

## Pass And Block Tokens

This phase passes with:

```text
PASS_FILTER_BENCH_SOURCE_PAPER_BLOCKER_CLOSURE
```

The full numeric benchmark remains blocked with:

```text
BLOCK_FILTER_BENCH_SOURCE_PAPER_NUMERIC_RUN_PENDING
```

until accepted source-paper truth values, synthetic data/evaluator execution,
and reviewed value/score/curvature/stochastic tables exist.
