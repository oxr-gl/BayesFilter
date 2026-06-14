# P1 Subplan: Target Registry And Reference Taxonomy

metadata_date: 2026-06-10
phase: FILTER_BENCH_P1
status: PLAN_DRAFT_PENDING_CLAUDE_REVIEW
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Create the benchmark target registry that fixes model identity, observations,
theta, horizon, dimensions, reference type, and gradient parameterization for
every row before any algorithm is run.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do we have a row registry that makes every future table cell interpretable? |
| Baseline/comparator | P30 model suite, P44 cross-model rows, P50/P51 SV and generalized SV rows, P53 spatial SIR route rows. |
| Primary criterion | Structured registry exists and contains required model rows, reference metadata, dimensions, horizons, theta, observations, and cell applicability policy. |
| Veto diagnostics | Stale scalar-only Zhao-Cui blockers retained as registry truth; old blocker tests treated as current admission logic instead of historical/superseded evidence; missing reference type; missing value scalar or gradient parameterization; hidden fixture drift. |
| Explanatory diagnostics | Existing target registry tests and old blocker tests. |
| Not concluded | No algorithm has been run yet. |
| Artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p1-target-registry-result-2026-06-10.md` and registry JSON. |

## Tasks

- Create `docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json`.
- Include required rows listed in the master program.
- For SV, encode the transformed/log-additive non-Gaussian target and the
  Gaussian-mixture approximation target separately.
- Mark native generalized SV lower-rung dense reference as available only where
  the existing native dense reference route applies.
- Update or supersede stale P45 blocker language for Zhao-Cui by distinguishing
  the old scalar helper from the multistate route.
- Mark old blocker tests and ledgers as historical-only or superseded whenever
  they conflict with current benchmark admission logic.
- Add mandatory schema validation for the registry JSON once the registry is
  created, including historical/superseded marker fields for stale blocker
  artifacts.

## Exit Criteria

Pass with `PASS_FILTER_BENCH_P1_TARGET_REGISTRY` only if every registry row has
all required fields, registry schema validation passes, and no stale scalar-only
blocker is used to suppress a benchmarkable model/filter pair.  Block if any
model row lacks a reference identity or fixed theta/observations.

## Validation

- Add focused registry schema tests when the registry JSON is created.
- Run CPU-only focused tests if code or JSON schema is added.
- Claude read-only review, max five iterations.
