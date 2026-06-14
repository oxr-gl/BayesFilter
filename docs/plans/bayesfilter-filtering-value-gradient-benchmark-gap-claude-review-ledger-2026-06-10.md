# Filtering Value/Gradient Benchmark Gap-Closure Claude Review Ledger

metadata_date: 2026-06-10
program: filtering-value-gradient-benchmark-gap-closure
status: PENDING_REVIEW
supervisor: Codex
reviewer: Claude Code read-only

## Review Scope

Claude is asked to review:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-closure-master-program-2026-06-10.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p0-contract-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p1-target-registry-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p2-adapter-protocol-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p3-reference-oracles-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p4-deterministic-filters-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p5-dpf-filters-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p6-gradient-semantics-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p7-preflight-matrix-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p8-runner-matrices-subplan-2026-06-10.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p9-closeout-subplan-2026-06-10.md`

## Iterations

### Iteration 1A: Master, P0, P1, P2

Worker: `filter-benchmark-gap-plan-review-iter1a`

Verdict: `VERDICT: REVISE`

Major findings:

- P2 allowed a proxy pass condition: protocol existence and planned tiny smokes
  were insufficient.
- P2 lacked a durable protocol artifact and stable target/registry row
  identifiers.

Minor findings:

- Master DAG wording was ambiguous about P4/P5/P7/P8 dependencies.
- P1 needed sharper supersession discipline for old blocker tests and mandatory
  schema validation once the registry JSON exists.

Repairs:

- P2 now requires a concrete schema/interface artifact, `target_id`,
  `registry_row_id`, and exercised tiny fixture rows per algorithm family,
  including invalid/unavailable gradient reason-code payloads.
- Master DAG was rewritten with explicit dependencies and P6/P7/P8 stop
  conditions.
- P1 now requires old blocker tests/ledgers to be marked historical-only or
  superseded where they conflict, plus mandatory schema validation.

### Iteration 1B: P3, P4, P5, P6

Worker: `filter-benchmark-gap-plan-review-iter1b`

Verdict: `VERDICT: REVISE`

Major findings:

- P3/P4 did not force separate actual non-Gaussian SV rows and
  Gaussian-mixture surrogate rows, leaving room to treat a surrogate as truth.
- P5 required DPF gradient statuses in adapters but did not guarantee those
  statuses would survive into emitted matrices.
- P6 allowed `reference_gradient_unavailable` to become a proxy pass for rows
  advertised as value/gradient comparable.
- P3 allowed blocked-only rows without distinguishing them from intended
  benchmark rows.

Minor findings:

- P3 and P6 needed a consistent reference-gradient policy.
- P4 should explicitly name the superseded scalar-only Zhao-Cui assumption.
- P5 needed a minimal matrix-emission check for multi-seed/status preservation.
- P6 should make finite-gradient and fixed-branch diagnostics explanatory-only.

Repairs:

- P3 now requires row classes and reference-gradient policies, including
  separate actual transformed/log-additive SV and Gaussian-mixture surrogate
  rows.
- P4 now requires the result artifact to name the superseded scalar-only
  Zhao-Cui assumption and preserve mixture-surrogate labels.
- P5 now requires matrix-preserved DPF status/reason codes and a minimal
  multi-seed matrix-emission check.
- P6 now blocks value/gradient rows without reference-gradient routes and marks
  finite/fixed-branch checks explanatory-only unless all gradient diagnostics
  support promotion.

### Iteration 1C: P7, P8, P9

Worker: `filter-benchmark-gap-plan-review-iter1c`

Verdict: `VERDICT: REVISE`

Major findings:

- P8 lacked per-cell comparator labels such as exact LGSSM, approximate
  non-Gaussian, no reference, and invalid gradient.
- P9 pass condition was artifact-completeness based rather than a handoff
  decision gate.
- P7/P8 run manifests lacked key provenance and direct plan/result linkage.
- The expected all-filter/all-model roster was not frozen and emitted in the
  benchmark artifact, leaving a hidden-hole failure mode.

Minor findings:

- P7 needed an explicit stop path when adapter repair does not converge.
- P8 needed to forbid treating P7 preflight as benchmark evidence.
- P8 needed to preserve P7 status distinctions at full-run time.
- P9 needed the repo decision-table style and separate engineering, numerical,
  and scientific ledgers.

Repairs:

- P7 now requires a frozen roster, preflight manifest, and block if repair does
  not converge without criteria changes.
- P8 now requires frozen roster validation, per-cell comparator labels, full
  run-manifest provenance, and preservation of P7 status distinctions.
- P9 now requires a decision table, separate engineering/numerical/scientific
  ledgers, and explicit handoff stop conditions.

### Iteration 2: Convergence Review

Worker: `filter-benchmark-gap-plan-review-iter2`

Verdict: `VERDICT: AGREE`

Claude reported no major issues.  Minor strengthening suggestions:

- P1 could explicitly require schema validation for historical/superseded marker
  fields.
- P9 could explicitly name the frozen roster/manifests among handoff
  prerequisites.

Repairs:

- P1 now includes historical/superseded marker fields in mandatory schema
  validation.
- P9 now lists missing frozen roster or missing preflight/full-run manifests as
  handoff-blocking conditions.

Review status: `PLAN_REVIEW_CONVERGED`
