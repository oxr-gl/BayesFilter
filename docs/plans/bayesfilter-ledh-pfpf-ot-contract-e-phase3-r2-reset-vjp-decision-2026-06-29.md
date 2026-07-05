# Phase R2 Decision: Contract E Reset VJP Boundary

Date: 2026-06-29

Status: `R2_BLOCKED_WITH_EXPLICIT_BOUNDARIES`

Subplan:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-subplan-2026-06-29.md`

Updated manifest:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-manifest-2026-06-29.json`

## Objective

R2 isolates the Contract E reset map and decides whether the reset derivative
can be implemented manually, can be deliberately stopped with bias/nonclaims,
or must remain blocked.  R2 is local and static: it does not run material
Phase 3, GPU/XLA, Kalman comparison, full-filter finite differences, or
production gradient evidence.

## Skeptical Pre-Execution Audit

The R2 plan survived the required pre-execution audit for this limited scope.
The baseline is not a proxy production metric: a local reset-map FD check is
required only if a manual reset VJP is claimed.  Since R2 does not claim or
implement such a VJP, the valid evidence path is an exact blocker ledger.  The
plan preserves the material blocker, forbids hidden autodiff fallbacks, names
all E01-E14 reset sub-boundaries, and treats spectral rank/floor crossings as
blocking events rather than smooth implementation details.

Claude bounded read-only re-review of the patched subplan returned
`VERDICT: AGREE`.

## Forward Reset Map

The current Contract E reset implementation is anchored in
`docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`,
inside `_make_compiled_contract_e`.

For one batch member, write the post-flow particles as \(x_i\), normalized
weights as \(w_i\), the dense transport matrix as \(M\), and fixed residual
noise as \(z_j\).  The forward reset computes
\[
  \mu_w=\sum_i w_i x_i,\qquad
  \Sigma_w=\sum_i w_i(x_i-\mu_w)(x_i-\mu_w)^\top ,
\]
\[
  y^+_j=\sum_i M_{ji}x_i,\qquad
  \Sigma_+=\frac1N\sum_j(y^+_j-\bar y^+)(y^+_j-\bar y^+)^\top ,
\]
\[
  G=\operatorname{sym}(\Sigma_w-\Sigma_+),\qquad
  P=\Pi_{\lambda>\tau_{\rm eig}}(\Sigma_w),
\]
\[
  R=\operatorname{sym}(G+\tau P),\qquad
  B=\sqrt{\rho}\,R^{1/2}.
\]
The residual noise is centered and scaled:
\[
  \xi_j=\sqrt{\frac{N}{N-1}}\left(z_j-\frac1N\sum_k z_k\right),
  \qquad
  \widetilde y_j=y^+_j+B\xi_j .
\]
Then
\[
  \widetilde\Sigma=
  \frac1N\sum_j(\widetilde y_j-\bar{\widetilde y})
  (\widetilde y_j-\bar{\widetilde y})^\top ,
  \qquad
  A=\Sigma_w^{1/2}\widetilde\Sigma^{\dagger,-1/2},
\]
and the final equal-weight reset cloud is
\[
  y^\star_j=\mu_w + A(\widetilde y_j-\bar{\widetilde y}) .
\]

This map is differentiable only after fixing every hard spectral branch:
projector rank, square-root support, pseudo-inverse support, and eigenvalue
floor decisions.  The current code uses `tf.linalg.eigh`, hard comparisons
against `spectral_floor`, square roots, and reciprocal square roots.  A generic
TensorFlow gradient through those operations is not an acceptable material VJP.

## R2 Decision

R2 does not implement a manual reset VJP.  Therefore no reset sub-boundary can
be classified as `manual_vjp_implemented`, because the required local same-map
FD parity artifact does not exist.  R2 also does not adopt a deliberate
stop-gradient policy for the material route, because that would omit part of
the declared Contract E gradient and needs a separate bias/nonclaim design.

The terminal R2 decision is:

```text
E01-E13: blocked
E14: non_gradient_monitor
```

This is a productive blocker, not a dead end.  It prevents another accidental
promotion of the outer-tape diagnostic and gives the next phase the exact
choice it must resolve: derive a fixed-rank manual reset VJP with local FD
parity, or propose a reviewed stop-gradient policy with explicit bias
nonclaims.

## Per-Sub-Boundary Decision Table

| ID | Boundary | R2 terminal classification | Evidence / blocker |
| --- | --- | --- | --- |
| E01 | Weighted target moments | `blocked` | Algebraic VJP is feasible, but no implemented reset VJP or FD parity artifact exists. |
| E02 | Barycentric first-stage map | `blocked` | Linear map VJP is feasible, but the reset output cotangent depends on downstream spectral adjoints not yet derived. |
| E03 | Plus-cloud uniform moments | `blocked` | Algebraic VJP is feasible, but no local same-map parity check exists. |
| E04 | Covariance gap | `blocked` | Linear/symmetric VJP is feasible, but downstream square-root/projector cotangents are unresolved. |
| E05 | Target projector/rank/eigen classification | `blocked` | Hard eigenvalue floor and retained-rank branch; no fixed-rank spectral projector VJP is derived or checked. |
| E06 | Residual covariance | `blocked` | Algebraic VJP depends on unresolved projector cotangent from E05. |
| E07 | Residual covariance square root | `blocked` | Principal square-root VJP requires a fixed spectral class and Sylvester/eigenbasis derivative; not implemented or FD checked. |
| E08 | Residual-noise recentering and injection | `blocked` | Noise centering is algebraic, but the cotangent to \(B\) depends on unresolved E07. |
| E09 | Tilde-cloud uniform moments | `blocked` | Algebraic VJP is feasible, but no implemented reset VJP or FD parity artifact exists. |
| E10 | Target covariance square root | `blocked` | Principal square-root VJP for \(\Sigma_w^{1/2}\) is not implemented and is unsafe at rank/floor crossings. |
| E11 | Tilde covariance pseudo-inverse square root | `blocked` | Hard retained-support branch and reciprocal square-root derivative are unresolved near the spectral floor. |
| E12 | Affine moment-restoration map | `blocked` | Matrix-product VJP depends on unresolved target-sqrt and tilde-pseudo-inverse-sqrt adjoints. |
| E13 | Final recentering to reset cloud | `blocked` | Algebraic VJP is feasible, but no end-to-end reset VJP has passed local FD parity. |
| E14 | Diagnostic moment and conditioning monitors | `non_gradient_monitor` | Diagnostics do not feed the material score route and require no VJP in R2. |

## Material Gate

The material Phase 3 gate remains blocked by:

```text
PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN
```

R2 cannot unblock material mode.  The current taped score diagnostic remains a
diagnostic only.  Material mode can be reconsidered only after a later phase
implements and audits a full manual likelihood reverse scan, including a
resolved Contract E reset policy.

## Nonclaims

- No Contract E reset VJP is implemented.
- No stop-gradient reset policy is approved.
- No full Phase 3 LGSSM gradient correctness claim is made.
- No GPU/XLA, Kalman, SIR, SV, HMC, production, or nonlinear-model claim is
  made.
