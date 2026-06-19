# P70 Phase 6d Subplan: Stable Fixed-Variant ALS Repair Design

metadata_date: 2026-06-16
status: DRAFT_PENDING_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 6d
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Design, but do not yet implement, a numerically stable fixed-variant ALS core
update for the P70 UKF-guided fixed-HMC branch.  The design must address the
Phase 6c root cause: unscaled ALS design columns and absolute normal-equation
ridge leading to `CONDITION_NUMBER_VETO` after accepted core updates.

This phase must produce a repair-design artifact precise enough for a later
implementation phase.  It must not run the repaired four-row Phase 6
diagnostic, must not change code, and must not claim that the fixed variant is
fixed.

## Entry Conditions Inherited From Phase 6c

Phase 6d may begin only because Phase 6c produced:

- `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-result-2026-06-16.md`;
- JSON evidence:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-2026-06-16.json`;
- Claude `VERDICT: AGREE` on the Phase 6c execution/result review;
- a standing Phase 7 block.

The inherited numerical facts are:

- the actual ALS path accepted 23 updates and vetoed at axis \(23\);
- at the failing axis,
  \[
    \kappa(A^\top W A+\rho I)\approx 1.236\times 10^{17},
    \qquad \rho=10^{-10};
  \]
- the failing design column-norm spread was about \(4.586\times10^{11}\);
- column normalization of the same design was explanatory-only and gave
  condition about \(7.72\times10^2\);
- trace-scaled ridge was explanatory-only and gave condition about
  \(7.60\times10^{10}\);
- clipping was ruled out for that row.

## Mathematical Repair Candidates

The current update solves
\[
  \min_u \sum_{j=1}^n w_j (A_j u-y_j)^2 + \rho \|u\|_2^2
\]
through the normal equations
\[
  (A^\top W A+\rho I)u=A^\top W y.
\]
Phase 6c shows that this coordinate system is not scale invariant: if the
columns of \(A\) have norms spanning many orders of magnitude, the scalar
ridge \(\rho I\) regularizes coefficient coordinates unevenly and the normal
matrix may veto even when a column-normalized representation is benign.

Phase 6d must compare these design choices:

1. Column-scaled weighted ridge normal equations.
   Let \(S=\operatorname{diag}(s_1,\ldots,s_p)\), with
   \(s_i=\max(\|A_{\cdot i}\|_{W}, s_{\min})\), and set \(B=AS^{-1}\).  Solve
   \[
     (B^\top W B+\rho S^{-2})v=B^\top W y,\qquad u=S^{-1}v,
   \]
   which is algebraically equivalent to the current ridge objective but solved
   in scaled coordinates.  A different rule, such as isotropic
   normalized-coordinate ridge \(\lambda I\), may be useful later but must be
   classified as a fixed-branch adaptation that changes the regularization
   geometry.

2. Weighted QR/SVD least squares with ridge.
   Solve the augmented system
   \[
     \begin{bmatrix} W^{1/2}A \\ \sqrt{\rho} I \end{bmatrix}u
     \approx
     \begin{bmatrix} W^{1/2}y \\ 0 \end{bmatrix}
   \]
   using QR or SVD instead of explicitly forming \(A^\top W A\).  This avoids
   squaring \(\kappa(A)\), but it does not by itself solve coefficient-scale
   imbalance unless combined with column scaling.

3. TT gauge/environment normalization between accepted core updates.
   Normalize adjacent TT environments so accepted core updates do not create
   uncontrolled gauge scale.  The design must state whether this is required
   for correctness or only for conditioning, and must preserve the represented
   function up to an explicitly tracked gauge transformation.

4. Row/effective-sample repair is not the primary Phase 6d target.
   Phase 6c found only 26 unique rows out of 36 and centered row rank 25, so
   row support may be a later robustness target.  Phase 6d may record this as a
   secondary requirement but must not propose row-count tuning as the first
   repair unless the stable-solve alternatives are mathematically inadequate.

5. Ignored ridge argument cleanup.
   `_p59_fixed_ttsirt_transport_from_values(..., ridge=...)` currently passes
   `P70_FIT_RIDGE` into `FixedTTFitConfig` instead of the supplied `ridge`.
   Phase 6d must decide whether the later implementation should fix this as a
   separate bug or explicitly remove the unused argument.  This cleanup cannot
   be represented as the root-cause repair by itself.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What numerically stable ALS core-update design should be implemented next to address the Phase 6c condition veto while preserving fixed-HMC branch semantics? |
| Baseline/comparator | Current `FixedTTFitter._fit_core_update`: unscaled design, normal equations, scalar ridge `config.ridge`, condition veto on `A^T W A + rho I`, TensorFlow dense solve. |
| Primary criterion | A written design selects one first implementation target and explains mathematically why it addresses the measured Phase 6c failure without changing model, samples, rank, degree, sweep order, or treating failed fits as admissible.  If the selected target changes the ridge geometry, the design must classify that change explicitly. |
| Veto diagnostics | Any design that silently loosens the condition veto; treats column-normalized or trace-scaled probes as proof of repair; changes row/rank/degree/sweep/initializer policy as the first repair; emits a transport from a failed fit; claims Phase 6/7 readiness; or calls the selected repair source-faithful without paper/source anchors. |
| Explanatory diagnostics | Phase 6c metrics, candidate condition estimates, expected algebraic equivalence of scaled coordinates, and proposed tests. |
| Not concluded | No code repair, no diagnostic pass, no validation, no HMC readiness, no source-faithfulness closure for the fixed variant. |
| Artifact preserving result | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6d-stable-als-repair-design-result-2026-06-16.md`. |

## Required Artifacts

- This subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6d-stable-als-repair-design-subplan-2026-06-16.md`.
- Repair-design result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6d-stable-als-repair-design-result-2026-06-16.md`.
- Updated P70 visible execution ledger.
- Updated P70 Claude review ledger.
- Updated P70 stop handoff.

## Required Checks/Reviews

No implementation checks are required unless the design phase edits code, which
is forbidden.  Local checks are:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6d-stable-als-repair-design-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6d-stable-als-repair-design-result-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-claude-review-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-stop-handoff-2026-06-16.md
```

Claude review must check:

- the design follows from Phase 6c evidence;
- the selected first repair is mathematically specified;
- actual branch behavior is distinguished from explanatory probes;
- source-faithful, fixed-HMC adaptation, and extension/invention claims are
  classified conservatively;
- no Phase 6 diagnostic rerun or Phase 7 unblock is authorized.

## Forbidden Claims/Actions

- Do not edit `bayesfilter/highdim/fitting.py` or `source_route.py` in Phase
  6d.
- Do not run the Phase 6 four-row diagnostic.
- Do not run a repaired diagnostic.
- Do not change thresholds, row count, rank, degree, sweep order, initializer,
  source-route sample construction, or model.
- Do not claim that QR/SVD, scaling, or gauge normalization is source-faithful
  unless anchored to the paper and author code.
- Do not proceed to Phase 7.

## Exact Next-Phase Handoff Conditions

Phase 6d may close only after:

- the repair-design result selects a first implementation target;
- rejected alternatives are explained;
- required implementation tests are listed;
- required diagnostic rerun gates are listed;
- Claude returns `VERDICT: AGREE`, or a blocker is written.

The next phase, if Phase 6d succeeds, should be Phase 6e implementation of the
selected stable ALS repair.  Phase 6e must have its own subplan and cannot run
the repaired four-row diagnostic until the implementation passes focused local
tests and receives explicit user approval for any diagnostic command.

## Stop Conditions

Stop and write a blocker if:

- the design cannot separate numerical stabilization from a scientific
  algorithm change;
- the selected repair would require changing source-route samples, rank,
  degree, or sweep policy before stabilizing the solve;
- Claude and Codex do not converge after five material review rounds;
- the evidence is insufficient to choose a first implementation target without
  another bounded diagnostic plan.

## Skeptical Plan Audit

The plan avoids the prior planning error of promoting proxy diagnostics.  Phase
6c column-normalized and trace-scaled-ridge numbers can motivate a repair
design, but they are not evidence that any repaired branch has passed.  Phase
6d is design-only and keeps Phase 7 blocked.  The baseline is the exact current
`FixedTTFitter` update, not a weaker toy model or the original author's
adaptive algorithm.
