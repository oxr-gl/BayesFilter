# P2 Result: UKF Covariance Lifecycle Design

Date: 2026-06-10

## Status

`PASS_P2_UKF_COVARIANCE_DESIGN_READY_FOR_P3`

## Decision

`PASS_P2_UKF_COVARIANCE_DESIGN_READY_FOR_P3`

P2 defines the TensorFlow/TFP design for carrying Li--Coates Algorithm 1
covariance state per particle.  It does not implement the filter and does not
rank numerical results.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact TensorFlow/TFP UKF covariance objects should Algorithm 1 carry per particle? |
| Baseline/comparator | Li-Coates Algorithm 1 covariance lifecycle; P1 documentation; existing BayesFilter sigma-point code; exact Kalman recursion on LGSSM as collapse test. |
| Primary pass criterion | A design artifact defines UKF prediction/update signatures, sigma-point convention, covariance stabilization, per-particle state layout, and resampling semantics before code implementation. |
| Veto diagnostics | Shared covariance replacing `P^i`; undocumented sigma-point defaults; arbitrary hidden thresholding; NumPy in differentiable implementation; replacing Algorithm 1 zero-noise flow anchor without review. |
| Explanatory diagnostics | Alternative parameters, Cholesky vs SVD factorization, jitter sensitivity, runtime/memory estimates. |
| Not concluded | P2 does not implement the filter, certify source faithfulness, or rank results. |

## Skeptical Plan Audit

| Hazard | P2 audit result |
| --- | --- |
| Wrong baseline | Clear.  P2 uses P1 Algorithm 1 obligations plus repo sigma-point code, not old LEDH-PFPF-OT results. |
| Proxy metric promotion | Clear.  No metrics are promoted.  Exact-collapse tests are future P3/P4 diagnostics. |
| Missing stop condition | Clear.  P2 stops at reviewed design and does not run comparison ladders. |
| Unfair comparison | Not applicable.  P2 is design-only. |
| Hidden assumptions | Controlled by naming sigma-point parameters, floors, jitter, and source/extension boundaries. |
| Environment mismatch | No TensorFlow execution is required beyond source inspection; no GPU command is run. |
| Artifact fit | Clear.  P2 gives P3 an implementation API and veto checklist. |

## Existing Code Read

| Artifact | P2 classification |
| --- | --- |
| `bayesfilter/nonlinear/sigma_points_tf.py` | Preferred source for the general TensorFlow unscented sigma-point convention and eigen/SVD placement diagnostics. |
| `bayesfilter/linear/svd_factor_tf.py` | Preferred PSD/eigen helper pattern: `symmetrize`, `psd_eigh`, `eigh_solve`, `eigh_logdet`, `floor_count`. |
| `experiments/dpf_implementation/tf_tfp/references/ukf_tf.py` | Range-bearing approximate comparator.  Useful for fixture-specific intuition only; not the Algorithm 1 implementation API. |
| `experiments/dpf_implementation/tf_tfp/flows/ledh_tf.py` | Old frozen-local-affine flow scaffolding.  Quarantined for Algorithm 1 flow/covariance claims because it does not carry `P_{k-1}^i -> P^i -> P_k^i`. |
| `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py` | Old OT wrapper.  Reusable only for PF-PF logging/weight-structure ideas; not reusable as final Algorithm 1 implementation. |

## P3 Target Module

P3 should add a new route rather than mutating the quarantined old route:

```text
experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py
```

This route should identify itself with:

```text
method_generation = li_coates_algorithm1_ukf_covariance_lifecycle
flow_source_route = li_coates_2017_algorithm1_ledh_pfpf
covariance_route = per_particle_ukf_prediction_update
flow_anchor_route = zero_noise_transition
previous_ledh_pfpf_ot_evidence_status = quarantined
```

The old `ledh_pfpf_ot_tf.py` route must remain quarantined for Algorithm 1
claims unless a later audited extension explicitly wraps the new core.

## Tensor Shapes And State

Let `N` be particle count, `nx` state dimension, `ny` observation dimension, and
`S = 2 * nx + 1` the UKF state sigma-point count.

| Object | Shape | Meaning |
| --- | --- | --- |
| `particles` | `[N, nx]` | Current `x_{k-1}^i` or post-flow `x_k^i`. |
| `covariances` | `[N, nx, nx]` | Per-particle posterior covariances `P_{k-1}^i` and `P_k^i`. |
| `predicted_means` | `[N, nx]` | Per-particle `m_{k|k-1}^i`. |
| `predicted_covariances` | `[N, nx, nx]` | Per-particle `P^i` used in LEDH coefficients. |
| `auxiliary_anchor` | `[N, nx]` | Zero-noise transition anchor `bar_eta_0^i = g_k(x_{k-1}^i,0)`. |
| `pre_flow_particles` | `[N, nx]` | Actual proposal samples `eta_0^i = g_k(x_{k-1}^i,v_k)`. |
| `post_flow_particles` | `[N, nx]` | Terminal proposal particles `eta_1^i = x_k^i`. |
| `theta_logdet` | `[N]` | `log prod_j |det(I + eps_j A_j^i)|`. |
| `log_weights` | `[N]` | Normalized log weights after the PF-PF correction. |

All tensors in the Algorithm 1 differentiable path should be `tf.float64`.
Integers such as ancestry are `tf.int32` or `tf.int64`.

## Callback Interface

P3 should implement a callback-driven core so P44 scalar fixtures, LGSSM
fixtures, and range-bearing fixtures can share the Algorithm 1 route:

```python
transition_mean_fn(x_prev: tf.Tensor, t: int) -> tf.Tensor
transition_sample_fn(x_prev: tf.Tensor, seed: int, t: int) -> tf.Tensor
transition_log_density_fn(x_next: tf.Tensor, x_prev: tf.Tensor, t: int) -> tf.Tensor
observation_mean_fn(x: tf.Tensor, t: int) -> tf.Tensor
observation_jacobian_fn(x: tf.Tensor, t: int) -> tf.Tensor
observation_log_density_fn(x: tf.Tensor, y: tf.Tensor, t: int) -> tf.Tensor
process_noise_covariance_fn(x_prev: tf.Tensor, t: int) -> tf.Tensor
observation_covariance_fn(t: int) -> tf.Tensor
```

For additive Gaussian transition models, UKF prediction may be implemented by
placing sigma points around `(x_{k-1}^i, P_{k-1}^i)`, applying
`transition_mean_fn`, and adding `Q_i`.  The actual proposal sample remains
`transition_sample_fn`; it is not replaced by the UKF mean.

For non-additive transition-noise models, P3 may either require an augmented
UKF design amendment or mark the model/filter pair `N/A_NOT_APPLICABLE` until
that amendment is reviewed.  It must not silently use additive-noise UKF on a
non-additive transition.

## UKF Prediction Contract

For each particle:

```text
input:  x_{k-1}^i, P_{k-1}^i, Q_i, transition_mean_fn
output: m_{k|k-1}^i, P^i, prediction_diagnostics_i
```

The prediction uses the repo's unscented sigma-point convention from
`bayesfilter/nonlinear/sigma_points_tf.py`:

```text
lambda = alpha^2 * (nx + kappa) - nx
spread = alpha^2 * (nx + kappa)
point_count = 2 * nx + 1
mean_weights[0] = lambda / spread
covariance_weights[0] = lambda / spread + (1 - alpha^2 + beta)
axis_weights = 1 / (2 * spread)
```

Recommended initial parameters for P3:

```text
alpha = 1.0
beta = 2.0
kappa = 0.0
```

This choice matches the existing unscented-rule tests that reproduce standard
normal first two moments.  Alternative UKF parameter ladders may be diagnostic
only until P5 explicitly plans them.

Prediction equations:

```text
sigma_x = sigma_points(x_{k-1}^i, P_{k-1}^i)
sigma_pred = transition_mean_fn(sigma_x, t)
m_{k|k-1}^i = sum_s wm_s sigma_pred_s
P^i = sum_s wc_s (sigma_pred_s - m)(sigma_pred_s - m)' + Q_i
```

`P^i` is then stabilized and used in the LEDH coefficients.  A shared covariance
across particles is a P3/P4 veto unless the model is linear-Gaussian and a test
shows all particle covariances are equal for mathematical reasons.

## UKF Update Contract

For each particle after weights are normalized:

```text
input:  m_{k|k-1}^i, P^i, y_k, R_k, observation_mean_fn
output: m_{k|k}^i, P_k^i, update_diagnostics_i
```

Update equations:

```text
sigma_x = sigma_points(m_{k|k-1}^i, P^i)
sigma_y = observation_mean_fn(sigma_x, t)
ybar = sum_s wm_s sigma_y_s
S = sum_s wc_s (sigma_y_s - ybar)(sigma_y_s - ybar)' + R_k
Cxy = sum_s wc_s (sigma_x_s - m)(sigma_y_s - ybar)'
K = Cxy S^{-1}
m_{k|k}^i = m_{k|k-1}^i + K (y_k - ybar)
P_k^i = P^i - K S K'
```

For angular observations, P3 may use fixture-specific residual functions, but
the result must record that residual convention.  The generic route should use
ordinary Euclidean residuals.

## Covariance Stabilization

P3 should use TensorFlow-only stabilization:

1. Symmetrize every covariance-like matrix:
   `P <- 0.5 * (P + P^T)`.
2. Compute eigenvalues with `tf.linalg.eigh`.
3. Apply an eigenvalue floor only as an explicit diagnostic branch.  The
   declared P3 smoke-test policy is:
   `covariance_floor = 1e-10` in `tf.float64`, chosen as a conservative
   numerical PSD floor for Cholesky/solve viability and not as an accuracy or
   promotion tolerance.  P3 artifacts must record this exact value, and P5 must
   treat floor sensitivity as explanatory unless a later plan promotes a
   stricter numerical-validity criterion.
4. Record at least:
   - raw minimum eigenvalue;
   - number of floored eigenvalues;
   - PSD projection residual;
   - maximum floor count over particles/time;
   - whether Cholesky would have failed without stabilization when checked.
5. Use the implemented covariance in subsequent computation.  Do not pretend
   the raw covariance was used after flooring.

The floor is a numerical validity safeguard, not a promotion threshold.  Any
result that needs flooring should remain valid only with the floor diagnostics
reported.

## LEDH Coefficient Contract

For each pseudo-time step `j` and particle `i`, P3 must compute:

```text
H_j^i = observation_jacobian_fn(auxiliary_state_i, t)
e_j^i = observation_mean_fn(auxiliary_state_i, t) - H_j^i auxiliary_state_i
A_j^i = -0.5 P^i H' (lambda_j H P^i H' + R)^{-1} H
b_j^i = (I + 2 lambda_j A_j^i)
        [ (I + lambda_j A_j^i) P^i H' R^{-1} (y_k - e_j^i)
          + A_j^i bar_eta_0^i ]
```

Then:

```text
auxiliary_state_i <- auxiliary_state_i + eps_j (A_j^i auxiliary_state_i + b_j^i)
eta_1_i           <- eta_1_i           + eps_j (A_j^i eta_1_i           + b_j^i)
theta_i           <- theta_i + log |det(I + eps_j A_j^i)|
```

The determinant, auxiliary update, and actual update must use the same
`A_j^i,b_j^i` matrices.  Reusing the old frozen local-affine map is a veto.

## Resampling Semantics

The source-faithful core should support:

```text
resampling_route = none
resampling_route = classical_resampling
```

For classical resampling, ancestry indices must be applied to all carried
state:

```text
particles    <- gather(post_flow_particles, ancestor_indices)
covariances  <- gather(P_k, ancestor_indices)
log_weights  <- uniform
```

P3 should include a deterministic ancestry test proving that `P_k^i` moves with
`x_k^i`.  OT or differentiable resampling is a BayesFilter extension and must
not be labelled as source Algorithm 1.  If P3 adds an OT wrapper, it must carry
covariances by a reviewed barycentric/transport policy and use a distinct
route identifier.

## Exact-Collapse Test Plan

P3/P4 should run these tests before any comparison result is interpreted:

| Test | Expected result | Veto if |
| --- | --- | --- |
| Linear transition UKF prediction | `m_{k|k-1}` and `P^i` match Kalman prediction to tight tolerance | UKF prediction deviates beyond tolerance without recorded floor branch |
| Linear observation UKF update | `m_{k|k}` and `P_k^i` match Kalman update to tight tolerance | UKF update deviates beyond tolerance |
| Deterministic transition edge case | With `Q=0` and linear deterministic transition, predicted covariance is exactly the pushforward `F P_{k-1}^i F'` before stabilization diagnostics | Artificial process noise or floor branch is silently injected without diagnostics |
| Identity observation edge case | With `h(x)=x`, finite `R`, and Euclidean residuals, the UKF update matches the Kalman identity-observation update | Observation transform, residual sign, or covariance update deviates beyond tolerance |
| Scalar determinant hand check | `log_theta = sum_j log(abs(1 + eps_j A_j))` | determinant sign or pseudo-time product mismatch |
| Nonlinear particle covariance variation | nonlinear fixture produces finite, particle-indexed covariance diagnostics | all covariances accidentally shared when the model should vary |
| Resampling ancestry | deterministic ancestry gathers matching covariance matrices | states and covariances become misaligned |

## P3 Veto List

- NumPy appears in the differentiable Algorithm 1 implementation path.
- The route imports or calls `run_ledh_pfpf_ot_tf` as the final Algorithm 1
  path.
- `P^i` is not used in `A_j^i,b_j^i`.
- Only a shared/global covariance is carried when the source route claims
  per-particle covariance lifecycle.
- The zero-noise anchor `bar_eta_0^i` is absent or replaced by the actual
  proposal particle without a reviewed amendment.
- The actual proposal particle is not migrated.
- The determinant product is missing or computed from a different map.
- Covariances are dropped or not resampled with particle state.
- Non-finite particles, log weights, determinant terms, or covariances appear.
- The artifact cites old LEDH-PFPF-OT performance rows as source-faithful
  evidence.

## Run Manifest

| Field | Value |
| --- | --- |
| git branch | `main` |
| git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| phase | `P2` |
| execution mode | visible current-dialogue execution |
| detached execution | `False` |
| CPU/GPU status | no TensorFlow/GPU command run |
| random seeds | `N/A` |
| output artifact | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-result-2026-06-10.md` |
| execution ledger | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-visible-overnight-execution-ledger-2026-06-10.md` |
| subplan | `docs/plans/bayesfilter-dpf-ledh-pfpf-li-coates-alg1-ukf-source-faithful-p2-ukf-covariance-design-subplan-2026-06-10.md` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `P2_UKF_COVARIANCE_DESIGN_REVISED_AFTER_ITERATION_1` | UKF signatures, sigma-point convention, stabilization, state layout, resampling semantics, and tests specified; deterministic-transition and identity-observation edge tests added after review | Shared covariance, hidden thresholds, NumPy path, old route reuse, missing zero-noise anchor all explicitly vetoed | P3 may discover fixture-specific residual or non-additive-noise needs | Claude read-only P2 review iteration 2, then repair or implement P3 | No implementation, no faithfulness audit, no value/gradient comparison |
| `PASS_P2_UKF_COVARIANCE_DESIGN_READY_FOR_P3` | Claude iteration 2 agreed the design now satisfies the P2 contract | No remaining P2 veto identified | Implementation may reveal fixture-specific needs | Start P3 implementation | No implementation, no faithfulness audit, no value/gradient comparison |

## Claude Review

Iteration 1 command:

```bash
bash scripts/dpf_v2_algorithm_full_comparison_claude_readonly_review.sh \
  --cwd /home/chakwong/BayesFilter \
  --name li-coates-alg1-ukf-p2-design-review-iter1 \
  "<read-only P2 design review prompt>"
```

Verdict:

`VERDICT: REVISE`

Findings:

- P2 was close and covered UKF signatures, unscented convention/defaults,
  per-particle covariance lifecycle, zero-noise anchor, old-route quarantine,
  and OT-as-extension boundary.
- Blocking gap: the exact-collapse test plan omitted the deterministic
  transition and identity-observation edge cases required by the P2 subplan.
- Stabilization wording needed to make `covariance_floor = 1e-10` a declared
  diagnostic policy rather than an unexplained house constant.

Repair:

- Added deterministic-transition and identity-observation rows to the
  exact-collapse test plan.
- Tightened the covariance-floor policy to state its value, dtype, purpose,
  diagnostic status, and non-promotion role.

Iteration 2:

Verdict:

`VERDICT: AGREE`

Findings:

- Deterministic-transition and identity-observation edge cases are now included.
- `covariance_floor = 1e-10` is declared as a diagnostic PSD policy with value,
  dtype, purpose, reporting, and non-promotion wording.
- Previously satisfied requirements remain intact: UKF signatures,
  per-particle covariance lifecycle, unscented defaults, zero-noise anchor,
  old-route quarantine, NumPy veto, and OT-as-extension boundary.
