# P70 Phase 6e Result: Stable ALS Implementation

metadata_date: 2026-06-16
status: PHASE6E_IMPLEMENTED_LOCAL_CHECKS_PASSED_CLAUDE_AGREE_PHASE7_BLOCKED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
subplan: docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6e-stable-als-implementation-subplan-2026-06-16.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Scope

Phase 6e implemented the Phase 6d selected stable ALS core-update repair:
objective-preserving column-scaled augmented weighted ridge least squares
inside `FixedTTFitter`.

No repaired Phase 6 diagnostic was run.  No Phase 6 four-row wrapper was run.
No Phase 7 action was run or authorized.

## Implemented Mathematics

For an ALS core update with design matrix \(A\), target vector \(y\), weights
\(w_j\), \(W=\operatorname{diag}(w_j)\), and ridge \(\rho\), the implementation
keeps the original objective
\[
  \min_u (Au-y)^\top W(Au-y)+\rho u^\top u .
\]

It computes weighted column scales
\[
  s_i=\max\left\{\left(\sum_j w_j A_{ji}^2\right)^{1/2},
  \max\{\sqrt{\epsilon_{\rm mach}}\max_k \|A_k\|_W,\epsilon_{\rm mach}\}\right\},
  \qquad S=\operatorname{diag}(s_i),
\]
sets \(B=AS^{-1}\), solves
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
  \qquad u=S^{-1}v ,
\]
using `tensorflow.linalg.lstsq(fast=False)`.

The augmented block \(\sqrt{\rho}S^{-1}\) is the essential
objective-preserving part.  An isotropic ridge in the scaled coordinates would
change the regularization geometry and remains a deferred adaptation.

## Code Changes

Implemented in `bayesfilter/highdim/fitting.py`:

- added a lane-neutral stabilization policy id and solver metadata;
- added `_ScaledAugmentedSolveResult`;
- added `_weighted_column_scales`;
- added `_solve_scaled_augmented_ridge`;
- updated `_fit_core_update` to use the stable augmented least-squares solve;
- retained the unscaled normal-equation condition number as diagnostic-only
  evidence;
- made the primary condition gate target the scaled augmented solved system;
- recorded solver mode, scale-floor rule, column-scale summaries, transformed
  ridge rule, ridge metric summary, unscaled normal condition, and nonclaims in
  update records and branch manifests.

Focused tests in `tests/highdim/test_fixed_branch_fit.py` now cover:

- objective equivalence on an imbalanced weighted ridge design;
- distinction from isotropic normalized-coordinate ridge;
- column-rescaling behavior for the unregularized prediction problem;
- invalid nonfinite, negative-weight, and invalid-ridge inputs;
- Phase-6c-shaped imbalanced diagnostics where unscaled normal conditioning is
  above the old veto but the scaled augmented solve is accepted;
- manifest policy fields;
- existing P70 wrapper failed-fit behavior through the focused wrapper test
  file.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 6e implementation gate passed with Claude `VERDICT: AGREE`. |
| Primary criterion | Passed focused compile and pytest checks. |
| Veto diagnostics | No repaired diagnostic command, no four-row Phase 6 wrapper, no Phase 7, no threshold loosening, no failed-fit transport, and no row/rank/degree/model/sample policy change in Phase 6e. |
| Main uncertainty | The repaired P70 diagnostic has not been run after this implementation, so this does not show that the Phase 6 row now passes. |
| Next justified action | Phase 6f diagnostic-planning subplan.  Any diagnostic command still requires a reviewed subplan and explicit user approval before it runs. |
| Not concluded | No fixed-variant success claim, no validation, no scaling result, no HMC readiness, no adaptive Zhao--Cui parity, no source-faithfulness closure. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `94069066a70df6f1f0f2b53d32b9d452bd67f891` |
| Working tree | Dirty before and after Phase 6e; unrelated pre-existing changes preserved. |
| Environment | CPU-only command environment with `CUDA_VISIBLE_DEVICES=-1` and `MPLCONFIGDIR=/tmp`. |
| Python | `Python 3.11.14` |
| TensorFlow | `2.19.1` |
| GPU status | Intentionally hidden for Phase 6e local checks. |
| Data version | N/A; focused unit tests and wrapper tests only. |
| Random seeds | N/A for local deterministic unit checks. |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6e-stable-als-implementation-subplan-2026-06-16.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6e-stable-als-implementation-result-2026-06-16.md` |

## Checks

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/fitting.py tests/highdim/test_fixed_branch_fit.py tests/highdim/test_p70_phase6_diagnostic_script.py
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_fixed_branch_fit.py tests/highdim/test_p70_phase6_diagnostic_script.py
```

Result: `42 passed, 2 warnings in 3.15s`.

Warnings were TensorFlow Probability `distutils` deprecation warnings already
seen in this test lane.

## Boundary Notes

This implementation is classified as `fixed_hmc_adaptation`.  It stabilizes
the fixed-branch ALS linear solve while preserving the fixed ridge objective,
but it is not claimed to be Zhao--Cui `source_faithful`.

The unscaled normal-equation condition is retained because it explains the
Phase 6c failure mode.  It is no longer the primary condition gate for the
actual solver surface; the scaled augmented solved-system condition is the
primary gate.

## Claude Review

Claude returned `VERDICT: AGREE`.

Findings:

- The algebra matches Phase 6d: with \(u=S^{-1}v\), the block
  \(\sqrt{\rho}S^{-1}\) preserves the original ridge objective.
- The focused tests are adequate for a bounded Phase 6e close.
- No forbidden action was implied so long as the result preserves the stated
  nonclaims and the `fixed_hmc_adaptation` classification.
- No material blocker remains before closing Phase 6e and limiting next work
  to Phase 6f diagnostic planning.
