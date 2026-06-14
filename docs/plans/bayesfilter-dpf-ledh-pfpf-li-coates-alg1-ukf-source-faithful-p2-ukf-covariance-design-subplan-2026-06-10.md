# P2 Subplan: UKF Covariance Lifecycle Design

Date: 2026-06-10

## Status

`DRAFT_FOR_CLAUDE_REVIEW`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact TensorFlow/TFP UKF covariance objects should Algorithm 1 carry per particle? |
| Baseline/comparator | Li-Coates Algorithm 1 covariance lifecycle; existing BayesFilter UKF/sigma-point documentation; exact Kalman recursion on LGSSM as a collapse test. |
| Primary pass criterion | A design artifact defines UKF prediction/update signatures, sigma-point convention, covariance stabilization, per-particle state layout, and resampling semantics before code implementation. |
| Veto diagnostics | Shared covariance replacing `P^i`; undocumented sigma-point defaults; treating covariance stabilization as arbitrary thresholding; using NumPy for differentiable implementation; replacing Algorithm 1 zero-noise flow anchor without review. |
| Explanatory diagnostics | Alternative sigma-point parameters, Cholesky vs SVD factorization, jitter sensitivity, runtime/memory estimates. |
| Not concluded | P2 does not implement the filter and does not rank numerical results. |
| Required artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-result-2026-06-10.md` |

## Design Obligations

1. Define an additive-noise UKF prediction function:
   - inputs: previous particle state `x_{k-1}^i`, covariance `P_{k-1}^i`,
     transition parameters, process-noise covariance;
   - outputs: predictive mean `m_{k|k-1}^i`, predictive covariance `P^i`,
     and diagnostics.
2. Define an additive-noise UKF update function:
   - inputs: predictive mean `m_{k|k-1}^i`, predictive covariance `P^i`,
     observation `y_k`, observation parameters, observation-noise covariance;
   - outputs: updated mean `m_{k|k}^i`, updated covariance `P_k^i`, likelihood
     diagnostic if needed, and diagnostics.
3. Specify sigma-point convention:
   - source/provenance in existing BayesFilter documentation;
   - `alpha`, `beta`, `kappa`, weights, and dimensional edge cases;
   - what changes if `dim=1` or covariance is nearly singular.
4. Specify covariance stabilization:
   - symmetrization rule;
   - PSD/eigenvalue or Cholesky/SVD checks;
   - jitter rule with provenance and diagnostic recording;
   - no hidden thresholds that become performance criteria.
5. Specify per-particle covariance state:
   - tensor shape and dtype;
   - initialization from prior covariance;
   - ancestry under classical resampling;
   - transport/mixture policy under OT resampling if used.
6. Specify exact-collapse tests:
   - linear-Gaussian UKF prediction/update must match Kalman covariance;
   - deterministic transition and identity observation edge cases.
7. Specify nonlinear smoke tests:
   - finite covariances;
   - PSD status;
   - particle-indexed covariance variation on nonlinear fixtures.

## Gate

P2 passes only when the design result is reviewed and includes a decision table,
an exact-collapse test plan, and a veto list that will be used in P3 and P4.
