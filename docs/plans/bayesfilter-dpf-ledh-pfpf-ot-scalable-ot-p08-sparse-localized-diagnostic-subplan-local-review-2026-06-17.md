# Phase 8 Local Review: Sparse/Localized Diagnostic Subplan

Date: 2026-06-17
Review timestamp: 2026-06-18T03:45:49+08:00

## Scope

Local Codex skeptical review of:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p08-sparse-localized-diagnostic-subplan-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-sparse-localized-audit-2026-06-17.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p07-exact-online-gpu-reference-result-2026-06-17.md`
- Phase 3 schema helper.

## Findings

No local blocker found for Phase 8 planning.

- Baseline is Phase 1 local dense TensorFlow transport matrix.
- The subplan is diagnostic-first and blocks sparse solver implementation until
  locality/support criteria pass.
- Source availability is not treated as locality or execution-value evidence.
- Required locality metrics include mass-capture support sizes,
  nearest-neighbor mass, truncation residuals, and transported-particle error.
- C++/POT sparse solvers remain reference-only and are not promoted as
  BayesFilter defaults.
- Package installation, network fetches, external sparse solver execution, GPU
  evidence, and Mini-batch unblocking remain blocked without approval.
- Forbidden claims block sparse speedup, ranking, posterior/default readiness,
  exact sparse validity, and general scalability.
- Claude remains read-only reviewer and cannot authorize implementation if
  locality criteria fail.

## Verdict

`LOCAL_REVIEW: PASS_AFTER_THRESHOLD_REPAIR`

## Repair Addendum

Claude round 01 found that the first draft named locality metrics without
numeric advance/block thresholds.  The subplan was patched to require all Phase
1 fixtures to pass these 99% mass-support and truncation thresholds before any
later sparse prototype can advance:

- median 99% row-mass support at most `max(8, ceil(0.25 * N))`;
- 90th-percentile 99% row-mass support at most `max(16, ceil(0.50 * N))`;
- 99% row-mass truncation max row residual at most `5.0e-3`;
- max column residual at most `5.0e-2`;
- max transported-particle error at most `5.0e-2`;
- finite dense and truncated transported particles.

The subplan now also states that later LEDH-specific fixtures are future scope,
not part of the Phase 8 comparator unless a separate reviewed subplan adds
them.

## Next Required Review

Run a bounded Claude read-only review of the Phase 8 subplan before diagnostic
execution.  If broad file review stalls, use a micro review focused on the
diagnostic-first boundary, locality thresholds, and source-vs-execution-value
claims.
