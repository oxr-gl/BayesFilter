# Phase 8 Claude Micro-Review: Threshold Repair

Date: 2026-06-17
Review timestamp: 2026-06-18T03:54:42+08:00

## Scope

Read-only micro-review of the repaired Phase 8 sparse/localized diagnostic
thresholds after Claude round 01 requested numeric advance/block criteria.

Claude did not edit files, execute commands, authorize sparse implementation,
or authorize phase advancement.

## Prompt Boundary

The micro-review asked only whether the repaired threshold text was consistent
with the diagnostic-first Phase 8 boundary:

- Phase 8 remains a sparse/locality diagnostic, not a sparse solver implementation.
- The comparator remains the Phase 1 local dense TensorFlow baseline.
- Sparse implementation may advance only if all predeclared 99% mass-support,
  truncation residual, transported-particle error, and finite-value thresholds
  pass.
- Source availability and runtime proxies are not locality evidence.
- External sparse solver execution, package installation, network fetches, GPU
  evidence, and non-TensorFlow default routes remain blocked.

## Review Result

Claude returned `VERDICT: AGREE`.

Claude's only residual note was non-blocking: define `N` and "minimal per-row
99% mass support" exactly in the plan/result to avoid tie/cutoff drift.

## Codex Repair Follow-Up

Codex patched the Phase 8 subplan to define:

- `N = transport_matrix.shape[2]`, the source-particle count for each fixture
  batch row;
- deterministic stable descending row-mass sorting;
- `k_i(t)` as the first stable prefix whose cumulative mass reaches
  `t * row_mass_i`;
- no tie expansion beyond the first stable prefix;
- the retained 99% support and row-renormalization procedure used by the
  truncation check.

## Verdict

`VERDICT: AGREE_AFTER_TIE_SEMANTICS_REPAIR`
