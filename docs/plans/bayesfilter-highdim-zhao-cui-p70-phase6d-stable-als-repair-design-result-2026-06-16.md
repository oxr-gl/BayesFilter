# P70 Phase 6d Result: Stable Fixed-Variant ALS Repair Design

metadata_date: 2026-06-16
status: PHASE6D_REPAIR_DESIGN_CLAUDE_AGREE_PHASE7_BLOCKED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 6d
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

The first implementation target should be an objective-preserving
column-scaled augmented weighted ridge least-squares update for each ALS core.
This is a numerical stabilization of the fixed core solve, not a change to the
source-route model, samples, rank, degree, sweep order, or fixed-HMC branch
target.  It also does not intentionally change the current ridge objective.

The selected update should replace the current direct normal-equation solve
inside `FixedTTFitter._fit_core_update`, while preserving the current
diagnostic veto discipline and adding scale-aware diagnostics.

## Mathematical Specification

The current update solves
\[
  (A^\top W A+\rho I)u=A^\top W y.
\]
Phase 6c showed that the failing axis has column-norm spread about
\(4.586\times10^{11}\), and the normal matrix has condition about
\(1.236\times10^{17}\).  This is the wrong coordinate system for applying a
scalar ridge and a dense normal-equation solve.

For a core update with design \(A\in\mathbb{R}^{n\times p}\), weights
\(w_j\ge 0\), and target \(y\), define weighted column scales
\[
  s_i=\max\left\{\left(\sum_{j=1}^n w_j A_{ji}^2\right)^{1/2},\,s_{\min}\right\},
  \qquad S=\operatorname{diag}(s_1,\ldots,s_p),
\]
and \(B=A S^{-1}\).  Solve the augmented ridge least-squares system
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

The first implementation should use TensorFlow's least-squares/SVD-capable
linear algebra rather than explicitly forming and solving
\(B^\top W B+\lambda I\) as the primary solve.  It may still compute the
normal matrix condition as a diagnostic.

This augmented system is algebraically equivalent to the current objective
because substituting \(u=S^{-1}v\) gives
\[
  \sum_{j=1}^n w_j(B_jv-y_j)^2+\rho\,v^\top S^{-2}v.
\]
Thus the selected first repair changes the coordinate system used by the
linear solve, but not the objective's ridge geometry in \(u\)-coordinates.

An isotropic normalized-coordinate ridge,
\[
  \sum_{j=1}^n w_j(B_jv-y_j)^2+\lambda\|v\|_2^2,
\]
would be a different regularizer.  It may become a later fixed-branch
adaptation if the objective-preserving solve is inadequate, but it is not the
Phase 6d selected first target.  A trace-scaled ridge,
\[
  \lambda=\rho\,\operatorname{tr}(B^\top W B)/p,
\]
should likewise be retained as a diagnostic or optional later policy, not the
first default, because it changes the regularization geometry or magnitude
based on the current sample design.

The scale floor should be deterministic and dtype-local, for example
\[
  s_{\min}=\max\{\sqrt{\epsilon_{\rm mach}}\max_i s_i,\epsilon_{\rm mach}\}.
\]
The exact expression must be fixed in Phase 6e before implementation and
recorded in the branch manifest.

## Why This Is The First Repair

This directly targets the Phase 6c proximate failure:

- the observed failure is not clipping; clip fraction is \(0\);
- the observed failure is not a row-budget gate; row count passes the hard gate;
- the observed failure appears after accepted ALS updates, where environment
  scale enters the core design;
- the column-normalized explanatory probe showed that column scaling directly
  attacks the measured condition path, reducing the corresponding diagnostic
  normal condition from \(1.236\times10^{17}\) to about \(7.72\times10^2\)
  under an explanatory isotropic normalized-coordinate ridge;
- an augmented least-squares solve avoids the explicit normal-equation
  condition squaring in the primary solve.

Therefore the first repair should stabilize the core linear algebra before
changing sampling policy, rank, degree, sweep order, or model construction.

## Classification

This repair is `fixed_hmc_adaptation` for the BayesFilter fixed-variant branch,
not `source_faithful`.

Rationale:

- the author/source route uses adaptive transport construction and MATLAB
  linear algebra in its own code path;
- this repository's fixed-HMC branch already freezes rank, basis, samples,
  sweep order, and initialization for differentiability/replay;
- objective-preserving column scaling and augmented least squares preserve the
  current fixed core-update ridge objective through the explicit
  transformation \(u=S^{-1}v\), but they are not asserted to be present in the
  author paper/source code.

No claim of adaptive Zhao--Cui parity follows from this design.

## Rejected Or Deferred Alternatives

1. Isotropic normalized-coordinate ridge.
   Deferred because it changes the regularization geometry from
   \(\rho\|u\|_2^2\) to \(\lambda\|Su\|_2^2\).  It may be useful, but it is a
   stronger fixed-branch adaptation than the objective-preserving first repair.

2. Plain trace-scaled ridge in the original normal equations.
   Deferred because it still forms normal equations and changes the ridge
   magnitude without first fixing coefficient-scale invariance.

3. QR/SVD on the unscaled augmented system.
   Deferred as incomplete because it avoids normal-equation squaring but leaves
   the enormous coefficient-scale imbalance in place.

4. TT gauge/environment normalization after every accepted update.
   Deferred to a second-stage repair candidate.  It may be needed, but it is
   more invasive because it changes core gauges and branch manifests.  The
   first repair should stabilize the local solve without altering represented
   TT gauge structure beyond the solved core.

5. Increasing `fit_sample_count`.
   Deferred because Phase 6c identified solve scaling as the proximate failure.
   More rows may improve robustness later but would change the diagnostic row
   policy before testing the direct numerical repair.

6. Changing rank, degree, sweep order, or initializer.
   Rejected for the first repair because those changes would obscure the Phase
   6c root cause and could reintroduce the prior proxy-metric planning error.

7. Only fixing the ignored `ridge` argument.
   Required cleanup later, but not sufficient: in Phase 6c the supplied ridge
   equals `P70_FIT_RIDGE`, so the ignored argument is not the observed cause.

## Required Phase 6e Implementation Tests

Phase 6e should add focused tests before any repaired diagnostic rerun:

- synthetic design test: column-scaled augmented solve recovers the same
  minimizer as direct ridge solve on a well-conditioned problem;
- scale-invariance test: rescaling design columns and unscaling coefficients
  gives the same predictions within tolerance;
- condition-diagnostic test: a design modeled after the Phase 6c failing axis
  records the original unscaled normal condition and the scaled augmented
  condition without suppressing diagnostics;
- failure-semantics test: nonfinite design, nonfinite target, and genuinely
  rank-deficient systems still produce non-OK statuses or explicit diagnostics;
- manifest test: branch identity records solver mode, scale floor, column
  scales hash or summary, ridge rule, and nonclaims;
- source-route wrapper test: failed fits still raise
  `P70FixedFitDiagnosticError` and never emit a transport.

## Required Later Diagnostic Gate

After Phase 6e implementation tests pass and Claude reviews the implementation,
a separate Phase 6f subplan may request explicit user approval for a bounded
diagnostic command.  That diagnostic should start with the same first row
`rank_candidate_1_2_fit36`; only if the first row passes should a repaired
four-row diagnostic be considered.

No Phase 6f or Phase 7 command is authorized by Phase 6d.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Answered at design level: the first implementation target should be objective-preserving column-scaled augmented weighted ridge least squares. |
| Baseline/comparator | Current unscaled normal-equation solve in `FixedTTFitter._fit_core_update`. |
| Primary criterion | Met in draft: selected target is mathematically specified and tied to Phase 6c evidence. |
| Veto diagnostics | No code edit, no diagnostic rerun, no threshold loosening, no failed-fit transport, no Phase 7 unblock. |
| Explanatory diagnostics | Phase 6c column-normalized and trace-scaled probes motivated the design but were not treated as a repair result. |
| Not concluded | No repaired implementation, no Phase 6 pass, no validation, no HMC readiness, no source-faithfulness closure. |

## Next Handoff

Claude reviewed the initial design and returned `VERDICT: REVISE` because the
first draft mixed objective-preserving column scaling with isotropic ridge in
normalized coordinates.  The design was patched to select the
objective-preserving augmented block \(\sqrt{\rho}S^{-1}\) and to defer
isotropic normalized-coordinate ridge as a different fixed-branch adaptation.
Claude then returned `VERDICT: AGREE`.

The next safe step is to draft the Phase 6e implementation subplan for the
selected stable ALS repair.  Phase 6e must not run a repaired diagnostic until
focused implementation tests pass and a later reviewed subplan receives
explicit user approval for the exact diagnostic command.
