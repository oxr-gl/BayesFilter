# P8 Subplan: Benchmark Runner And Matrix Emission

metadata_date: 2026-06-10
phase: FILTER_BENCH_P8
status: PLAN_DRAFT_PENDING_CLAUDE_REVIEW
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Implement the full benchmark runner and emit tables that answer the user's
question directly: algorithms as rows, models as columns, with value errors and
gradient errors in separate matrices.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the benchmark produce full value and gradient comparison matrices with no unexplained holes? |
| Baseline/comparator | P7 preflight matrix and all preceding adapters/references. |
| Primary criterion | Full runner emits structured JSON, CSV/Markdown matrices, diagnostics, frozen row/column roster, per-cell comparator labels, final status taxonomy, and run manifest. |
| Veto diagnostics | Missing holes without reason codes; thresholds changed after results; MC uncertainty omitted for DPF; runtime/environment omitted; old LEDH-PFPF-OT included as current; P7 preflight cited as benchmark evidence; comparator class omitted from cells. |
| Explanatory diagnostics | runtime, ESS, MC SE, seed-level rows, branch diagnostics, dense reference order. |
| Not concluded | Benchmark result is filtering evidence only, not Bayesian-estimation readiness. |
| Artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-runner-matrices-result-2026-06-10.md` and benchmark output JSON/CSV/Markdown. |

## Tasks

- Implement a standard benchmark command.
- Emit `value_error_matrix`, `gradient_error_matrix`, `status_matrix`,
  `diagnostics_matrix`, and seed-level raw rows.
- Emit the frozen expected all-filter/all-model roster in the benchmark artifact
  and validate the actual matrix cells against it.
- Include per-cell comparator labels, at minimum: `exact_LGSSM`,
  `exact_or_dense_numerical`, `transformed_actual_nongaussian`,
  `gaussian_mixture_surrogate`, `approximate_nongaussian`, `no_reference`,
  `invalid_gradient`, and `historical_only`.
- Preserve the P7 status distinctions at full-run time: implementation failure,
  unsupported pair, reference unavailable, invalid gradient, and successful
  benchmarked result.
- Include run manifest: git commit, dirty-state summary, command,
  environment/conda env, CPU/GPU status, dtype, seeds, wall time, output paths,
  plan file, result file, registry artifact, adapter schema artifact, and
  reference-oracle artifact.
- Include MC uncertainty for stochastic rows.
- Include post-run red-team note in the result artifact.
- State explicitly that P7 preflight is a wiring gate only and cannot be cited
  as benchmark evidence or used to excuse missing full-run cells.

## Exit Criteria

Pass with `PASS_FILTER_BENCH_P8_RUNNER_MATRICES` only if the matrices are
complete against the frozen roster, every non-result cell has a machine-readable
reason code, and every cell has a comparator label.  Block if the output cannot
answer the value/gradient comparison question.

## Validation

- Full CPU-only benchmark command unless a later plan explicitly requests GPU.
- JSON schema validation.
- Claude read-only review, max five iterations.
