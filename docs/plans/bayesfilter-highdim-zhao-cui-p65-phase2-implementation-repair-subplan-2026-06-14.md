# P65 Phase 2 Subplan: High-Rank Fixed-ALS Zero-TT Repair

metadata_date: 2026-06-15
status: REVIEWED_READY_FOR_PHASE2_PRECHECK
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p65-fixed-branch-rank-capacity-master-program-2026-06-14.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Repair the Phase 1 target:

`BLOCK_P65_HIGH_RANK_FIXED_ALS_ZERO_SQRT_TT`

The high-rank fixed branch currently passes P59 assembly but its fitted
square-root TT cores are zero or near-zero, so its squared-TT transport is
defensive-only.  Phase 2 must test and patch a bounded repair mechanism for that
specific target without changing the Zhao--Cui target, previous-marginal axes,
source-pushed fit-data route, defensive `tau`, or P60 thresholds.

## Entry Conditions Inherited From Previous Phase

- Phase 0 reproduced the P64/P60 baseline under the full pinned tuple.
- Phase 1 identified the repair target
  `BLOCK_P65_HIGH_RANK_FIXED_ALS_ZERO_SQRT_TT`.
- Phase 1 did not prove the causal mechanism; underdetermined or degenerate
  fixed ALS is a hypothesis, not an established theorem.
- Phase 1 showed that small fit-data capacity rows `3`, `4`, and `6` do not
  clear the collapse.
- Phase 1 showed that the high `(degree=0, rank=2)` tuple also collapses; this
  is tuple-level evidence only.

## Required Artifacts

- This refreshed Phase 2 subplan.
- Implementation diff anchors if code changes.
- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase2-implementation-repair-result-2026-06-14.md`.
- Refreshed Phase 3 subplan if the repair path is ready for bug-test closeout.
- Updated Claude review ledger and visible execution ledger.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a bounded fixed-branch repair mechanism prevent the high-rank fitted square-root TT from collapsing to zero while preserving source-route invariants and P60 comparison governance? |
| Baseline/comparator | Phase 1 baseline: `sample_count=1`, `fit_sample_count=2`, low `(degree=0, rank=1)`, high `(degree=1, rank=2)`, high fitted square-root normalizers `[0.0, 0.0]`, high zero/near-zero TT core signature. |
| Primary pass criterion | A repaired path produces nonzero high fitted square-root mass at both steps, high TT core norms are not zero/near-zero under the declared tolerance, no high defensive-only steps remain, and focused compile/tests pass. |
| Veto diagnostics | Changed target/order/axes; artificial reference-grid fit data; defensive `tau` removal/rescale; P60 threshold weakening; hidden adaptive stochastic reselection; nonfinite density/normalizer; repair that only hides the diagnostic; unsupported source-faithful claim. |
| Explanatory diagnostics | Fitted TT core norms, zero-core count, square-root normalizer, mixture normalizer, fit residual, condition numbers, ESS, correction-weight ranges, clipping, target-value range, branch manifests. |
| Not concluded | No final bug fix until Phase 3 closeout; no d=18 correctness, no d=50/d=100 scaling, no adaptive Zhao--Cui parity, no HMC readiness, no theorem that the selected mechanism is uniquely necessary. |

## Repair Candidate Order

Phase 2 must start with the least scientifically risky mechanism that could
actually repair the high branch.  A pure admissibility guard may be implemented
only as fail-closed safety; it does not count as repairing the high branch unless
paired with a mechanism that produces a nonzero high square-root TT.

1. **Core-norm diagnostic gate, no behavior change.**
   - Expose or test the high-rank zero-TT signature in the P60 manifest.
   - This is a safety prerequisite and regression detector.
   - It cannot by itself close the repair.
2. **Deterministic nonzero warm-start or normalization stabilization.**
   - Patch only the fixed high-rank fitting path if a reviewed local mechanism
     shows the current deterministic ALS update collapses the cores.
   - Before any behavior-changing patch, document the stabilization in the P50
     mathematical chapter or a dedicated derivation note, and record paper/source
     anchors or classify the change as `fixed_hmc_adaptation` or
     `extension_or_invention`.
   - Preserve branch determinism and record changed branch identity.
   - Do not add stochastic adaptive reselection.
3. **Admissible capacity rule.**
   - If the high-rank branch cannot be stabilized under the current tiny fixed
     data, mark that configuration inadmissible and select only a noncollapsed
     fixed branch under a reviewed deterministic rule.
   - This is a fixed-variant adaptation, not a source-faithful Zhao--Cui repair.
   - A branch-substitution outcome is not a repair of the failing high-rank
     branch.  It must be reported as an adaptation or blocker result unless the
     same promoted comparison target is preserved and the high branch itself no
     longer has zero square-root TT mass.

## Required Checks/Tests/Reviews

- Before code edits, inspect the fixed TT fitter and source-route branch identity
  surfaces that would be touched.
- Before any behavior-changing stabilization, write or update the mathematical
  derivation/anchor note required by the Zhao-Cui source-anchor gate.
- Write or update a focused test that fails on the current high-rank zero-TT
  signature.
- Run compile checks on touched files:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/fitting.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

- Run focused P59/P60 tests after any patch:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p59_author_sir_36d_target_fit.py \
  tests/highdim/test_p59_author_sir_step_spec_assembly.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

- Run a repaired comparator JSON probe that prints:
  - high fitted square-root normalizers;
  - high defensive-only steps;
  - high TT core norm range and zero-core count;
  - preserved source invariants;
  - branch hashes.
- Bounded Claude review is required before executing Phase 2 and again after any
  behavior-changing implementation diff.

## Forbidden Claims/Actions

- Do not claim final bug repair before Phase 3.
- Do not call a guard-only change a repaired high-rank branch.
- Do not weaken P60 thresholds.
- Do not remove or rescale defensive `tau`.
- Do not introduce artificial reference-grid fit data.
- Do not change target order or previous-marginal axes.
- Do not use stochastic adaptive reselection.
- Do not claim source faithfulness unless paper and author-source anchors support
  the exact operation.
- Do not present branch substitution as repairing the failed high-rank branch
  unless the original promoted high branch itself is repaired under the declared
  comparison target.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- a reviewed Phase 2 patch or deterministic rule produces nonzero high fitted
  square-root mass at both steps;
- high TT core norms are not zero/near-zero under the declared tolerance;
- high defensive-only steps are empty;
- any behavior-changing stabilization is documented with mathematical
  derivation and paper/source anchors or explicitly classified as
  `fixed_hmc_adaptation` or `extension_or_invention`;
- focused tests and compile checks pass;
- Phase 2 result records exact changed files, branch behavior, preserved
  invariants, and residual risks;
- Claude review converges or all material review blockers are resolved.

If Phase 2 can only add a guard and cannot repair the high branch, write a Phase
2 blocker result and do not advance to Phase 3 as a repaired bug.

## Stop Conditions

- The candidate repair requires changing the scientific target or source-route
  axes.
- The repair only hides or renames the defensive-only collapse.
- The implementation requires a broader redesign than this subplan authorizes.
- Focused tests fail in a way requiring new mathematical documentation.
- Claude and Codex do not converge after five rounds for the same blocker.

## End-Of-Subplan Protocol

1. Run required local checks.
2. Write Phase 2 result or blocker.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 3 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
