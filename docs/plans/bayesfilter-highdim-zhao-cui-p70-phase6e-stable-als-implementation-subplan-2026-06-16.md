# P70 Phase 6e Subplan: Stable ALS Implementation

metadata_date: 2026-06-16
status: IMPLEMENTED_LOCAL_CHECKS_PASSED_CLAUDE_AGREE_PHASE7_BLOCKED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 6e
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement the Phase 6d selected stable ALS repair in the fixed TT fitter:
objective-preserving column-scaled augmented weighted ridge least squares for
each core update.  Add focused tests and diagnostics that prove the
implementation preserves the ridge objective while stabilizing the linear solve
surface.

Phase 6e may edit code and tests after this subplan receives Claude agreement.
Phase 6e must not run the repaired Phase 6 diagnostic and must not unblock
Phase 7.

## Entry Conditions Inherited From Phase 6d

Phase 6e may begin only after:

- `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6d-stable-als-repair-design-result-2026-06-16.md`
  has status `PHASE6D_REPAIR_DESIGN_CLAUDE_AGREE_PHASE7_BLOCKED`;
- Claude has accepted the objective-preserving scaled augmented solve;
- the Phase 6c root-cause evidence remains the active baseline;
- no repaired diagnostic command has been approved.

The selected update is:
\[
  s_i=\max\left\{\left(\sum_j w_j A_{ji}^2\right)^{1/2},s_{\min}\right\},
  \qquad S=\operatorname{diag}(s_i),\qquad B=AS^{-1},
\]
\[
  \begin{bmatrix}
    W^{1/2}B\\
    \sqrt{\rho}S^{-1}
  \end{bmatrix}v
  \approx
  \begin{bmatrix}
    W^{1/2}y\\
    0
  \end{bmatrix},
  \qquad u=S^{-1}v.
\]

This is algebraically equivalent to minimizing
\[
  \sum_j w_j(A_ju-y_j)^2+\rho\|u\|_2^2
\]
but should be numerically better conditioned than solving
\((A^\top W A+\rho I)u=A^\top Wy\) directly.

## Required Code Surfaces

Allowed code surfaces:

- `bayesfilter/highdim/fitting.py`
  - add a private helper for weighted column scales;
  - add a private helper for objective-preserving scaled augmented ridge solve;
  - update `_fit_core_update` to use the stable solve;
  - preserve `build_core_update_system` as a diagnostic/reference builder for
    the current design matrix and unscaled normal-equation condition unless a
    documented test requires exposing scaled diagnostics separately;
  - record solver mode, scale-floor policy, scaled design condition, unscaled
    normal condition, and column-scale summaries in update records and
    branch-manifest diagnostics.
- `tests/highdim/test_fixed_branch_fit.py`
  - add focused unit tests for the new stable solve and diagnostics.

Allowed only if strictly required by tests:

- `bayesfilter/highdim/__init__.py` if a new public dataclass/config field is
  unavoidable.  Prefer private helpers and existing public API.

Forbidden code surfaces:

- Do not change `bayesfilter/highdim/source_route.py` in Phase 6e except for a
  separately justified compile-breaking import adjustment.  The ignored
  `ridge` argument cleanup is deferred unless the implementation cannot be
  tested without it.
- Do not edit diagnostic wrappers or runbook scripts except to add a future
  Phase 6f plan, which is out of scope here.

## Implementation Requirements

The implementation must:

- keep `FixedTTFitConfig.ridge` as the objective ridge in \(u\)-coordinates;
- compute weighted column norms from the actual design and weights;
- use a deterministic scale floor.  Phase 6e should set
  \[
    s_{\min}=\max\{\sqrt{\epsilon_{\rm mach}}\max_i s_i,\epsilon_{\rm mach}\}
  \]
  in `tf.float64`, with a special case when all column norms are zero;
- build an augmented system with rows
  \(W^{1/2}B\) and \(\sqrt{\rho}S^{-1}\);
- solve the augmented system with TensorFlow least-squares linear algebra
  rather than explicit `tf.linalg.solve` on normal equations;
- unscale \(u=S^{-1}v\) before reshaping into the TT core;
- preserve nonfinite checks and `HighDimStatus` semantics;
- keep a condition-veto diagnostic.  The primary veto should be based on an
  implementation-defined condition diagnostic for the actual solve surface,
  while the unscaled normal-equation condition must still be recorded as
  explanatory evidence.  The subresult must explain this distinction;
- keep failed fits inadmissible and keep `P70FixedFitDiagnosticError` behavior
  intact through existing wrapper tests;
- record enough manifest data to replay and audit solver policy:
  `solver_backend`, `solver_mode`, `scale_floor`, `scale_floor_rule`,
  `column_scale_min`, `column_scale_max`, `column_scale_spread`,
  `unscaled_normal_condition_number`, `scaled_augmented_condition_number`, and
  nonclaims.

## Required Tests

Focused tests in `tests/highdim/test_fixed_branch_fit.py` must include:

1. Objective equivalence on a well-conditioned problem.
   Compare the stable scaled augmented solve's prediction/core update with the
   direct ridge normal-equation solution on a small well-conditioned design.

2. Column-rescaling invariance.
   Rescale design columns by a deterministic diagonal matrix and confirm that
   after unscaling the fitted predictions agree within tolerance.

3. Phase-6c-shaped conditioning regression.
   Build a synthetic design with severe column spread.  Verify that the update
   records both the unscaled normal condition and the scaled augmented
   condition, and that the stable solve does not veto solely because the
   unscaled normal condition is above the old threshold.

4. Nonfinite and degenerate failure semantics.
   Confirm nonfinite design/target/weights and truly unsolvable augmented
   systems still return non-OK statuses or explicit diagnostics.

5. Manifest/diagnostic contract.
   Confirm branch diagnostics include solver mode, scale floor, scale spread,
   scaled condition, unscaled condition, and nonclaims.

6. Existing P70 failed-fit wrapper tests.
   Run the current P70 focused wrapper tests to ensure failed fits still raise
   diagnostic errors and do not emit transports.

## Required Local Checks

After implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/fitting.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_p70_phase6_diagnostic_script.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_fit.py tests/highdim/test_p70_phase6_diagnostic_script.py
git diff --check -- bayesfilter/highdim/fitting.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_p70_phase6_diagnostic_script.py docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6e-stable-als-implementation-subplan-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6e-stable-als-implementation-result-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-execution-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-claude-review-ledger-2026-06-16.md docs/plans/bayesfilter-highdim-zhao-cui-p70-visible-stop-handoff-2026-06-16.md
```

Do not run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p70_phase6_rank_channel_normalizer_diagnostic.py
```

or any repaired first-row/Phase 6 diagnostic in Phase 6e.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the implementation correctly replace the fixed-core linear solve with objective-preserving column-scaled augmented weighted ridge least squares while preserving failed-fit semantics and diagnostics? |
| Baseline/comparator | Phase 6d design and current `FixedTTFitter._fit_core_update` unscaled normal-equation implementation. |
| Primary criterion | Focused unit tests pass and inspect the stable solve, objective equivalence, scale-invariance behavior, diagnostics, failure semantics, and wrapper failure behavior. |
| Veto diagnostics | Any implementation that changes rank/degree/row/sweep/initializer/model/source sample policy; suppresses failed-fit status; emits transport from failed fit; loosens veto without new diagnostic semantics; treats Phase 6c explanatory probes as pass evidence; or runs a repaired diagnostic. |
| Explanatory diagnostics | Unscaled normal condition, scaled augmented condition, scale spread, old direct-solve comparison on well-conditioned fixtures. |
| Not concluded | No repaired Phase 6 pass, no validation, no scaling, no HMC readiness, no adaptive Zhao--Cui parity, no source-faithfulness closure. |
| Artifact preserving result | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6e-stable-als-implementation-result-2026-06-16.md`. |

## Required Artifacts

- Phase 6e subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6e-stable-als-implementation-subplan-2026-06-16.md`.
- Phase 6e result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6e-stable-als-implementation-result-2026-06-16.md`.
- Code/test patch only on allowed surfaces.
- Updated execution ledger.
- Updated Claude review ledger.
- Updated stop handoff.

## Claude Review Requirements

Before implementation, Claude must review this subplan for:

- mathematical consistency with Phase 6d;
- sufficient tests for objective preservation and failure semantics;
- boundary safety: no diagnostic rerun or Phase 7 unblock;
- source-governance classification as `fixed_hmc_adaptation`, not
  `source_faithful`;
- no hidden row/rank/degree/sweep/model policy changes.

After implementation, Claude must review the result and focused test evidence
before any Phase 6f diagnostic plan is drafted.

## Forbidden Claims/Actions

- Do not run any repaired diagnostic command.
- Do not run the Phase 6 four-row wrapper.
- Do not claim the fixed variant works.
- Do not proceed to Phase 7.
- Do not claim source-faithfulness for the stable solve unless separately
  anchored to paper and author source lines.
- Do not change source-route sample construction, model, rank, degree, sweep,
  row, or initializer policy.

## Exact Next-Phase Handoff Conditions

Phase 6e may close only after:

- code and tests are implemented on allowed surfaces;
- required local checks pass or failures are recorded;
- a Phase 6e result note is written;
- Claude reviews the implementation/result and returns `VERDICT: AGREE`, or a
  blocker is written.

If Phase 6e succeeds, the next safe step is Phase 6f diagnostic-planning
subplan.  Phase 6f must request explicit user approval before any diagnostic
command runs.

## Stop Conditions

Stop and write a blocker if:

- objective equivalence cannot be tested convincingly;
- stable solve requires changing model, samples, rank, degree, sweep order,
  row count, or initializer policy;
- focused tests show failed-fit semantics are weakened;
- implementation would require broad public API changes not authorized by this
  plan;
- Claude and Codex do not converge after five material review rounds.

## Skeptical Plan Audit

This plan does not treat a stable local solve as a repaired filter.  It only
authorizes implementation and focused tests for the core update.  The plan
keeps Phase 6c explanatory probes in the explanatory ledger and requires a
separate Phase 6f gate before any repaired diagnostic can be run.  The baseline
is the current fixed fitter, not the adaptive author algorithm, so the repair
remains classified as a fixed-HMC adaptation.
