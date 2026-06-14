# P5 Subplan: DPF Filter Wiring And Supersession Guard

metadata_date: 2026-06-10
phase: FILTER_BENCH_P5
status: PLAN_DRAFT_PENDING_CLAUDE_REVIEW
supervisor: Codex
reviewer: Claude Code read-only

## Objective

Wire bootstrap DPF and source-faithful Algorithm 1 UKF LEDH-PFPF into the common
benchmark adapter while preventing old LEDH-PFPF-OT evidence from re-entering
as current.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can DPF filters run on the same target registry and report value, gradient status, Monte Carlo uncertainty, ESS, and resampling diagnostics? |
| Baseline/comparator | Current Algorithm 1 UKF LEDH-PFPF implementation and P9 supersession closeout; bootstrap DPF runners; historical LEDH-PFPF-OT artifacts. |
| Primary criterion | Current DPF adapters emit structured results with seeds, particle counts, MC standard errors where applicable, gradient status, and matrix-preserved reason codes. |
| Veto diagnostics | Old LEDH-PFPF-OT used as current algorithm; resampling-gradient invalidity hidden in either adapter output or emitted matrices; one-seed stochastic result treated as exact; missing ESS/resampling diagnostics. |
| Explanatory diagnostics | Multi-seed standard errors, ESS, resampling counts, finite value checks, fixed-branch gradient checks. |
| Not concluded | No DPF gradient certification unless P6 and row diagnostics support it. |
| Artifact | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p5-dpf-filters-result-2026-06-10.md` |

## Tasks

- Add bootstrap DPF adapter.
- Add Algorithm 1 UKF LEDH-PFPF adapter using the current source-faithful route.
- Record `previous_ledh_pfpf_ot_evidence_status` in diagnostics.
- Add multi-seed result aggregation fields.
- Add particle count and seed ladder policy for small/standard rows.
- Add a minimal matrix-emission check proving that
  `resampling_gradient_not_valid`, `fixed_branch_gradient_diagnostic`, and
  DPF adapter failures survive into the value/gradient/status matrices.

## Exit Criteria

Pass with `PASS_FILTER_BENCH_P5_DPF_FILTERS` only if DPF rows can report value
errors and gradient statuses without relying on old LEDH-PFPF-OT current
evidence, and those statuses are preserved in a minimal emitted matrix.  Block
if Algorithm 1 callbacks cannot be produced for required model rows or if any
invalid DPF gradient can disappear from the matrix artifact.

## Validation

- Tiny CPU-only DPF adapter smokes.
- Route identifier guard tests.
- Minimal multi-seed aggregation and matrix reason-code preservation check.
- Claude read-only review, max five iterations.
