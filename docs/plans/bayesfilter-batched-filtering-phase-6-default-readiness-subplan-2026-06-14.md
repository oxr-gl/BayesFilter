# Phase 6 Subplan: Default-Readiness Decision

Date: 2026-06-14

## Status

`DRAFT_FOR_LOCAL_AND_CLAUDE_REVIEW`

## Phase Objective

Produce a final default-readiness decision for the experimental batched
filtering value+score work.  The decision must separate:

- engineering correctness;
- compiled CPU/GPU performance evidence;
- downstream value/score boundary integration;
- filter-family coverage, including Kalman versus SVD sigma-point evidence;
- production default policy;
- remaining gaps and nonclaims.

This phase may recommend an optional experimental path or a conditional
production-candidate path.  It must not change a production default without
explicit human approval.

## Entry Conditions Inherited From Previous Phase

- Phase 0 inventory and boundary audit passed.
- Phase 1 deterministic correctness tests passed.
- Phase 2 nonlinear branch/fail-closed tests passed.
- Phase 3 non-default experimental interface candidate passed.
- Phase 4 JIT-only compiled benchmark ladder passed with capacity and scalar
  infeasibility records.
- Phase 5 named downstream value/score boundary test passed using
  `static_unroll_chain_value_and_score`; this downstream-boundary evidence is
  Kalman-only unless Phase 6 result explicitly records additional SVD-UKF
  downstream evidence.
- No public export/default change is authorized.
- CUT4 remains outside default-promotion scope.
- Existing unrelated dirty worktree changes must be preserved.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-result-2026-06-14.md`
- Final visible handoff:
  `docs/plans/bayesfilter-batched-filtering-visible-stop-handoff-2026-06-14.md`
- Claude review artifact:
  `docs/plans/bayesfilter-batched-filtering-phase-6-claude-review-round-01-2026-06-14.md`

## Required Checks, Tests, And Reviews

Pre-decision checks:

1. Verify Phase 0-5 result files exist.
2. Verify Phase 1-5 required test suites passed in their result files.
3. Verify no experimental batched module is publicly exported:
   `rg -n "experimental_batched_value_score|experimental_batched_kalman|experimental_batched_svd" bayesfilter/__init__.py bayesfilter/linear/__init__.py bayesfilter/nonlinear/__init__.py`
4. Verify Phase 4 GPU benchmark artifacts report `jit_compile: true` and GPU
   device placement for GPU rows.
5. Verify the Phase 4 result records trusted-context GPU execution provenance
   before GPU timings are used in the synthesis.
6. Verify Phase 5 result names the downstream boundary, records that the
   exercised adapter called `experimental_batched_kalman_value_score`, and
   preserves nonclaims.
7. Verify commit/snapshot coherence:
   - record current `git rev-parse HEAD`;
   - record which Phase 0-5 result files include explicit commit manifests;
   - require the Phase 6 result to scope the decision to the verified commit
     set and to mark any result without an explicit commit manifest as
     result-file-scoped historical evidence rather than unbounded live-code
     evidence.

Review:

- Claude Opus max effort must review this subplan read-only before execution.
- Claude must review the Phase 6 result before final handoff.
- Stop after five rounds for the same material blocker.
- Claude cannot authorize a production default change.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Decision question | Is the batched filtering value+score work ready to become a production default, an optional experimental path, a conditional production candidate, or blocked? |
| Baseline/comparator | Phase 0-5 result files, scalar authority parity tests, public API guard, JIT-only benchmark artifacts, and named downstream boundary test. |
| Primary criterion | A decision table and inference-status table are produced that explicitly separate, at minimum, Kalman evidence, SVD-UKF evidence, downstream-boundary coverage, trusted/JIT performance provenance, default-policy blockers, human approvals required, and nonclaims. |
| Promotion veto diagnostics | Any missing phase result, scalar parity failure, nonfinite output, wrong GPU placement, missing trusted GPU provenance for GPU timing, eager GPU timing used as speed evidence, public export/default change, unsupported HMC/NeuTra/posterior claim, or unsupported generalization from Kalman-only downstream evidence to SVD-UKF downstream readiness. |
| Explanatory diagnostics | Benchmark timing, capacity limits, scalar comparator infeasibility, test warnings, and implementation complexity. |
| Not concluded | No production default change, no sampler convergence, no posterior quality, no CUT4 readiness, no broad model coverage. |
| Artifact preserving result | Phase 6 result and visible stop handoff. |

## Forbidden Claims And Actions

- Do not change production defaults or public exports.
- Do not claim default readiness unless all default-readiness gaps are explicitly
  satisfied or explicitly accepted by the human.
- Do not claim HMC/NeuTra sampler convergence or posterior quality.
- Do not claim CUT4 readiness.
- Do not claim SVD-UKF downstream integration evidence from the Phase 5
  Kalman-only boundary test.
- Do not treat Phase 4 timings as scientific or statistical ranking evidence.
- Do not install packages, fetch network resources, commit, push, or run
  destructive filesystem/git commands.
- Do not let Claude edit files or authorize execution.

## Exact Next-Phase Handoff Conditions

There is no automatic next implementation phase in this master program.  The
final handoff must state:

- final phase reached;
- final status;
- result artifacts;
- Claude review trail;
- tests and benchmarks actually run;
- unresolved blockers or gaps;
- what was not concluded;
- exact next human decision required.

## Stop Conditions

Stop and write a blocker result if:

- any Phase 0-5 required result artifact is missing;
- any required public/export guard failed;
- Phase 4 GPU artifacts are not JIT compiled, have wrong device placement, or
  lack trusted-context provenance in the Phase 4 result;
- Phase 5 did not exercise a named existing downstream boundary;
- decision language treats Phase 5 as SVD-UKF downstream evidence without a new
  reviewed SVD-UKF downstream artifact;
- current commit/snapshot scope cannot be recorded clearly enough to avoid a
  stale-context or artifact-mismatch claim;
- decision language would require a production default change without human
  approval;
- Claude review does not converge after five rounds for the same material
  blocker.

## End-Of-Phase Procedure

1. Run pre-decision checks.
2. Write Phase 6 result with decision and inference-status tables.
3. Review Phase 6 result locally for unsupported claims.
4. If material, send Phase 6 result to Claude read-only review.
5. Write final visible stop handoff.
