# Phase 8 Subplan: Sparse/Localized Diagnostic

Date: 2026-06-17
Draft timestamp: 2026-06-18T03:45:49+08:00

## Phase Objective

Plan a locality-first diagnostic for sparse, screened, multiscale, and
localized OT.  Phase 8 should measure whether the Phase 1 dense transport plans
have enough concentrated support to justify a later sparse/screened TensorFlow
prototype.

Phase 8 is not a sparse solver implementation phase.  It should first compute
support and truncation diagnostics from existing dense baseline artifacts or a
small local dense replay.  Sparse implementation remains blocked unless the
diagnostic shows locality/screenability under declared criteria.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result records `PHASE_1_BASELINE_FIXTURE_PASSED`.
- Phase 2 result records
  `PHASE_2_CANDIDATE_AUDITS_PASSED_WITH_USER_APPROVED_MICRO_REVIEW_RESOLUTION`.
- Phase 3 result records `PHASE_3_COMMON_INTERFACE_HARNESS_PASSED`.
- Phase 4 result records `PHASE_4_NYSTROM_PROTOTYPE_PASSED`.
- Phase 5 result records
  `PHASE_5_POSITIVE_FEATURE_PROTOTYPE_PASSED_SEMANTIC_REPLACEMENT`.
- Phase 6 result records
  `PHASE_6_LOW_RANK_COUPLING_TRANSPORT_OBJECT_FIXTURE_PASSED`.
- Phase 7 result records
  `PHASE_7_EXACT_ONLINE_GPU_REFERENCE_ONLY_PASSED`.
- Sparse/localized audit records `source_reference_only` and
  `execution_value_pending`.
- The comparator remains the Phase 1 local TensorFlow dense baseline.
  Later LEDH-specific fixtures are future scope and are not part of the Phase 8
  advance/block criterion unless a separate reviewed subplan adds them.
- No sparse speedup, ranking, production/default readiness, or posterior
  correctness has been claimed.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p08-sparse-localized-diagnostic-result-2026-06-17.md`
- Diagnostic script:
  `docs/benchmarks/scalable_ot_p08_sparse_locality_diagnostics.py`
- JSON result:
  `docs/benchmarks/scalable-ot-p08-sparse-locality-diagnostics-2026-06-17.json`
- Markdown result:
  `docs/benchmarks/scalable-ot-p08-sparse-locality-diagnostics-2026-06-17.md`
- Updated execution ledger and stop handoff.
- Phase 9 sliced/subspace/minibatch exploratory subplan draft:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p09-sliced-subspace-minibatch-subplan-2026-06-17.md`

## Source Anchors Required Before Execution

| Anchor | Required use |
| --- | --- |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-sparse-localized-audit-2026-06-17.md` | Paper-note-code-execution matrix and diagnostic-first contract for sparse/localized lane. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` lines 762-826 | Sparse multiscale OT, Screenkhorn, support restriction, and stabilization caveats. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex` lines 978-995 | Localization/block OT motivation and block transport equations. |
| `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-source-lock-result-2026-06-17.md` lines 82 and 95 | Sparse/source-reference row and conditional locality posture. |
| `.localsource/scalable_ot_code_audit/MANIFEST.md` lines 103, 126-148, and 210 | POT Screenkhorn and Schmitzer sparse/multiscale source posture. |

## Required Checks, Tests, And Reviews

Before diagnostic execution:

1. Re-read the sparse/localized audit note, Phase 1 result, Phase 3 schema, and
   source anchors above.
2. Record semantic posture before execution:
   - `reference_only` for source/library inspection;
   - `exact_semantics` only if a sparse active support is certified or exact
     dense plan is preserved;
   - `approximate_kernel` or `semantic_replacement` only if support restriction
     intentionally changes the transport object.
3. Define locality metrics before running:
   - support size needed for 90%, 95%, 99%, and 99.9% plan mass per row;
   - nearest-neighbor mass curve under particle-space distance;
   - truncated transport row/column residuals for declared thresholds;
   - truncated transported-particle error against dense baseline.
4. Apply these predeclared advance/block thresholds:
   - `advance_sparse_prototype_candidate` only if every Phase 1 fixture has
     median support for 99% row mass at most `max(8, ceil(0.25 * N))`;
   - and every Phase 1 fixture has 90th-percentile support for 99% row mass at
     most `max(16, ceil(0.50 * N))`;
   - and a 99% row-mass truncation/renormalization check has max row residual
     at most `5.0e-3`, max column residual at most `5.0e-2`, and max
     transported-particle error at most `5.0e-2`;
   - otherwise Phase 8 must record
     `SPARSE_LOCALITY_DIAGNOSTIC_BLOCKS_SPARSE_IMPLEMENTATION_FOR_NOW`.
5. Treat 90%, 95%, and 99.9% mass-support curves, nearest-neighbor mass, and
   runtime/memory proxy as explanatory unless the 99% advance thresholds above
   pass.
6. Confirm no C++/POT sparse code is promoted to BayesFilter default.

If diagnostic proceeds:

1. Syntax/import check for diagnostic script.
2. Dense baseline replay or existing artifact read for Phase 1 fixtures.
3. JSON/Markdown artifacts with locality curves and truncation checks.
4. Phase 3 schema candidate record only if a sparse/truncated transport object
   is emitted; otherwise record diagnostic-only result.
5. Hard-veto diagnostics must include finite dense transport, finite truncated
   particles when computed, marginal residuals, dense transported-particle
   error, and explicit decision to advance or block sparse implementation.

Review:

- Phase 8 is diagnostic-bearing.  Run local checks first, then use Claude as
  read-only reviewer for the subplan or material repairs.
- Claude cannot authorize sparse implementation if locality criteria fail.
- Stop after five review rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do Phase 1 dense transport plans have enough local support concentration to justify a later sparse/screened/localized TensorFlow prototype? |
| Baseline/comparator | Phase 1 local dense TensorFlow transport matrix and transported particles. |
| Primary pass criterion | A diagnostic artifact records finite dense plans, locality/support curves, truncated marginal residuals, truncated transported-particle errors, and the predeclared threshold-based advance/block decision for sparse implementation. |
| Promotion veto | Runtime-only evidence; source availability treated as locality evidence; diffuse plan support under the declared 99% mass thresholds; invalid marginal residuals after truncation; missing transported particles; C++/POT route promoted as BayesFilter default. |
| Continuation veto | Phase 1 dense transport matrix unavailable; locality thresholds cannot be defined; diagnostic requires package installation, network fetch, GPU evidence, external sparse solver execution, or non-TensorFlow default code. |
| Repair trigger | Localized threshold, support-curve, tiny truncation materialization, dtype, fixture-selection, or artifact-schema issue. |
| Explanatory diagnostics | Mass capture curves, support counts, nearest-neighbor mass, truncation residuals, dense-reference particle error, memory proxy, and source implementation effort. |
| Not concluded | No sparse speedup, no production/default readiness, no posterior correctness, no ranking, and no sparse solver validity beyond the diagnostic. |
| Artifact preserving result | Phase 8 diagnostics, result note, ledger, stop handoff, and Phase 9 subplan. |

## Predeclared Advance/Block Thresholds

Let `N = transport_matrix.shape[2]`, the source-particle count for each Phase
1 fixture batch row.  For each target row `i`, sort the row masses in
descending order using a deterministic stable sort.  For threshold `t`, define
`k_i(t)` as the smallest prefix length whose cumulative sorted mass is at least
`t * row_mass_i`.  Ties are not expanded beyond the first stable prefix that
meets the threshold, so the diagnostic is deterministic but does not claim a
unique mathematical active set when equal masses occur.

The "minimal per-row 99% mass support" is exactly the support formed by those
stable sorted prefix indices for `k_i(0.99)`.  The truncation check zeros all
other entries, then row-renormalizes each nonzero retained row to the original
dense row sum before recomputing row residuals, column residuals, and
transported particles.

Phase 8 may mark sparse implementation as an
`advance_sparse_prototype_candidate` only if all of the following hold on every
Phase 1 fixture:

- median over rows of `k_i(0.99)` is at most `max(8, ceil(0.25 * N))`;
- 90th percentile over rows of `k_i(0.99)` is at most
  `max(16, ceil(0.50 * N))`;
- after retaining the minimal per-row 99% mass support and row-renormalizing,
  max row residual is at most `5.0e-3`;
- max column residual is at most `5.0e-2`;
- max transported-particle error against the dense transported particles is at
  most `5.0e-2`;
- dense and truncated transported particles are finite.

If any threshold fails, Phase 8 must record
`SPARSE_LOCALITY_DIAGNOSTIC_BLOCKS_SPARSE_IMPLEMENTATION_FOR_NOW`.  This is not
a rejection of sparse OT as a literature direction; it is evidence that the
current Phase 1 fixtures do not justify implementation in this runbook without
additional LEDH-specific fixtures or a new plan.

## Skeptical Plan Audit

- Wrong baseline: Phase 8 must inspect Phase 1 local dense transport plans, not
  external sparse demos.
- Proxy metric risk: source maturity and runtime are irrelevant until locality
  and truncated-transport validity are measured.
- Missing stop conditions: stop if dense transport matrix is unavailable or
  the predeclared locality thresholds above cannot be applied.
- Unfair comparisons: sparse/localized is conditional; do not rank it against
  low-rank/Nystrom/positive-feature lanes from source evidence.
- Hidden assumptions: distance metric, support threshold, epsilon, row/column
  orientation, truncation normalization, and Phase 1-only comparator scope must
  be recorded.
- Stale context: Phase 4/5/6 do not establish locality.
- Environment mismatch: no package install, no external C++/POT execution, no
  GPU evidence, no non-TensorFlow default implementation.
- Artifact adequacy: a sparse source library is not a BayesFilter locality
  artifact.

Skeptical audit status:
`PASSED_FOR_PHASE_8_SPARSE_LOCALIZED_DIAGNOSTIC_PLAN`.

## Forbidden Claims And Actions

- Do not implement a sparse solver before locality diagnostic criteria pass.
- Do not claim sparse speedup, ranking, production/default readiness, posterior
  correctness, exact sparse validity, or general scalability.
- Do not run C++/POT sparse solvers, install packages, fetch network sources,
  or use GPU evidence without approval.
- Do not treat source availability as support-locality evidence.
- Do not modify unrelated dirty user work.
- Do not unblock Mini-batch/BoMb.

## Exact Next-Phase Handoff Conditions

Phase 9 may begin only after:

- Phase 8 result records `advance_sparse_prototype_candidate`,
  `SPARSE_LOCALITY_DIAGNOSTIC_BLOCKS_SPARSE_IMPLEMENTATION_FOR_NOW`, or a
  precise failure/blocker for sparse implementation;
- diagnostic JSON/Markdown artifacts exist;
- local syntax/import/diagnostic checks pass;
- sparse semantic class and source-route classification are recorded;
- Phase 9 sliced/subspace/minibatch exploratory subplan exists and has been
  reviewed for consistency, correctness, feasibility, artifact coverage, and
  boundary safety;
- no human-required stop condition is active.

## Stop Conditions

Stop and write/update the stop handoff if:

- Phase 1 dense transport matrix cannot be obtained;
- locality/support thresholds cannot be declared before execution;
- diagnostic would require package installation, network fetch, GPU evidence,
  credentials, destructive action, external sparse solver execution, or
  non-TensorFlow default code;
- local checks reveal a hard veto not localized to a repair trigger;
- Claude and Codex do not converge after five focused review rounds for the
  same material blocker.

## End-Of-Phase Checklist

1. Run the required local checks.
2. Write the Phase 8 result/close record.
3. Draft or refresh the Phase 9 sliced/subspace/minibatch exploratory subplan.
4. Review the Phase 9 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
