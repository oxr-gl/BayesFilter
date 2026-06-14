# P7 Subplan: Preflight Matrix Coverage

metadata_date: 2026-06-10
phase: FILTER_BENCH_P7
status: PLAN_DRAFT_PENDING_CLAUDE_REVIEW
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Run a tiny preflight matrix before the full benchmark.  This phase proves that
the registry, adapters, references, gradient statuses, and result schema are
connected.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does every planned algorithm/model pair produce a structured cell or a structured reason code before the full run? |
| Baseline/comparator | P1 registry, P2 adapter protocol, P3 references, P4/P5 algorithm adapters, P6 gradient taxonomy. |
| Primary criterion | Tiny preflight matrix has no silent holes and emits a manifest linking the frozen expected row/column roster to observed preflight cells. |
| Veto diagnostics | Empty cells without reason codes; adapter failures mistaken for algorithm failures; stochastic one-seed noise interpreted as performance. |
| Explanatory diagnostics | small horizons, tiny particle counts, one or two seeds, finite checks. |
| Not concluded | Preflight values are not benchmark values. |
| Artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p7-preflight-matrix-result-2026-06-10.md`, preflight JSON, and preflight run manifest. |

## Tasks

- Run tiny versions of every algorithm/model pair.
- Emit a preflight value matrix and gradient-status matrix.
- Emit the frozen expected all-filter/all-model roster used for preflight.
- Distinguish implementation failure, unsupported row, reference unavailable,
  invalid gradient, and successful smoke.
- Repair fixable adapter failures before proceeding.
- Record run manifest fields: git commit or dirty-state summary, command,
  environment/conda env, CPU/GPU status, dtype, seeds, wall time, plan file,
  result file, registry artifact, and preflight output path.
- If fixable adapter failures do not converge after the phase repair loop or
  require criteria changes, stop with `BLOCK_FILTER_BENCH_P7_PREFLIGHT_MATRIX`
  rather than narrowing the roster silently.

## Exit Criteria

Pass with `PASS_FILTER_BENCH_P7_PREFLIGHT_MATRIX` only if there are no silent
holes in the preflight matrix and the frozen roster is preserved in the artifact.
Block if any required algorithm/model pair has neither a result nor a reason
code, or if repair fails to converge without changing benchmark criteria.

## Validation

- CPU-only focused preflight command.
- Claude read-only review, max five iterations.
