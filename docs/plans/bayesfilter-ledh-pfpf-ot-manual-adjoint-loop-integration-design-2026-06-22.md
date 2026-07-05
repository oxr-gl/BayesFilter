# LEDH-PFPF-OT Manual Adjoint Loop Integration Design

Date: 2026-06-22

Status: M4_DRAFT_FOR_REVIEW

## Objective

Define the integration contract for the private M3 route before wiring it into
the LEDH-PFPF-OT value recursion.  This is a design artifact only.  It does not
implement filter-loop integration and does not establish memory discipline.

## Supported Route

Route name:

```text
manual_dense_finite_sinkhorn_stopped_scale_keys
```

M4 design scope:

- dense transport plan only;
- no warmstart;
- scalar `epsilon`;
- fixed finite Sinkhorn step count;
- stopped scale, keys, `epsilon`, `epsilon0`, `scaling`, and step count;
- gradients only with respect to particles/log weights and downstream model
  parameters that flow into those quantities;
- opt-in only.

Unsupported until a later reviewed phase:

- streaming/chunked route;
- vector-`epsilon`;
- warmstarted potentials;
- adaptive differentiated stopping;
- gradients through Sinkhorn hyperparameters;
- public/default promotion;
- governed `N=10000` validation;
- P82 FD return.

## Current Code Anchors

Primary value recursion:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `batched_ledh_pfpf_ot_value_core_tf`

Transport core:

- `batched_annealed_transport_core_tf`

Private M3 helper:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `_filterflow_manual_dense_finite_transport_matrix_stopped_scale_keys`

Existing public route boundary:

- `transport_gradient_mode in {"filterflow_clipped", "filterflow_custom_op", "raw"}`

M5 may add a new opt-in experimental route name only if tests show defaults and
existing routes remain unchanged.  M3's public-mode rejection test is a
pre-integration boundary; M5 must update it only with an explicit opt-in
contract and replacement default-preservation tests.

## Filter-Loop Tensor Flow

At each time step `t`, the current value recursion does:

1. Reads deterministic fixed inputs:
   - `observations[t]`;
   - current `particles`;
   - fixed `pre_flow_particles[:, t, :, :]`;
   - fixed `fixed_resampling_mask[:, t]`.
2. Runs `batched_ledh_flow_core_tf` with deterministic callbacks.
3. Computes corrected log weights:
   - previous `log_weights`;
   - transition log density;
   - observation log density;
   - flow proposal density;
   - flow log determinant.
4. Normalizes corrected log weights and accumulates `log_likelihood`.
5. Computes ESS/filtered moments for reporting.
6. Calls `batched_annealed_transport_core_tf`.
7. Updates:
   - `particles = transported.particles`;
   - `log_weights = transported.log_weights`.

The manual route must preserve this scalar recursion.  It is not allowed to
change the corrected-weight scalar, fixed mask, flow scalar, or likelihood
accumulation.

## Proposed M5 Integration Point And Ownership Boundary

Add a private opt-in branch inside `batched_annealed_transport_core_tf` after:

```text
center = reduce_mean(x)
centered = x - stop(center)
scale = _filterflow_scale(x)
scaled_x = centered / stop(scale)
```

and before:

```text
transported = matmul(transport_matrix, x)
```

The proposed branch should be available only when all are true:

- `transport_plan_mode == "dense"`;
- no `warmstart_state`;
- scalar `epsilon_tensor`;
- route opt-in name explicitly selected;
- `transport_ad_mode == "stabilized"` for the first M5 implementation.

For M5, "equivalent stopped-scale/key route" is not an accepted loose
substitute.  Any later equivalent route must show, on the same tiny fixtures:
forward parity, gradient parity with respect to particles/log weights, same
mask semantics, same dtype behavior, and same scalar/broadcast contract.

The branch should call:

```text
_filterflow_manual_dense_finite_transport_matrix_stopped_scale_keys(
    scaled_x,
    logw,
    epsilon_tensor,
    epsilon0,
    scaling_tensor,
    steps=<fixed_steps>,
)
```

where `epsilon0` is recomputed from `scaled_x` under the same stopped-scale
contract.  M5 must decide whether `steps` equals the existing
`sinkhorn_iterations` value or a smaller fixed diagnostic count for the first
smoke; either choice must be named in the result.

Manual adjoint attachment point:

- the custom gradient attaches to the returned dense transport matrix `T`;
- downstream `transported = tf.linalg.matmul(T, x)` remains ordinary
  TensorFlow matmul and contributes the direct barycentric gradient;
- the branch does not wrap the entire downstream value recursion;
- active/inactive row mixing is owned by `batched_annealed_transport_core_tf`,
  not by the private M3 helper.

Mask/log-weight ownership:

- M5 should invoke the helper on the full batch and blend externally with the
  existing `tf.where(mask[:, None, None], transport_matrix, identity_transport)`
  and `tf.where(mask[:, None], uniform_log, logw)` pattern;
- inactive rows must use identity transport and original log weights;
- active rows must use the manual dense transport matrix and uniform log
  weights.

M5 may choose active-row slicing only if it proves the same mixed-mask forward
and gradient behavior as the full-batch blend on tiny fixtures.  Full-batch
blend is the default M5 handoff.

## Stopped Quantities

The route stops:

- centering/scale metadata used to form `scaled_x`;
- same-particle cost keys via `C(x, stop_gradient(x))`;
- `epsilon`;
- `epsilon0`;
- `scaling`;
- fixed step count.

The route differentiates:

- `scaled_x` as the query/source particles;
- `logw`;
- downstream model parameters only through their effect on particles/log
  weights and the rest of the value recursion.

## Replay Contract

Default M4/M5 replay contract:

```text
recompute C(x, stop_gradient(x)) under the same stopped-key rule
```

This is the same scalar rule validated in M3.  If M5 chooses to retain cost or
potential states instead of recomputing, it must document this as a
same-scalar implementation choice and verify value/gradient parity on tiny
fixtures.

## Retained/Recomputed Ledger

Required forward values for the dense private route:

| Quantity | Shape | M5 default | Reason |
|---|---|---|---|
| `scaled_x` | `[B,N,D]` | retain by TensorFlow/custom-gradient closure | differentiable source/query state |
| `logw` | `[B,N]` | retain by closure | differentiable log weights |
| `epsilon` | scalar | retain, stopped | scalar route parameter |
| `epsilon0` | `[B]` | recompute or retain stopped | schedule start, no gradient |
| `scaling` | scalar | retain, stopped | schedule constant |
| `steps` | Python/int scalar | retain as route metadata | fixed finite loop count |
| `C(scaled_x, stop(scaled_x))` | `[B,N,N]` | recompute under same stop rule | dense cost for tiny route |
| loop states `(running,a_y,b_x,a_x,b_y)` | per step | recompute during VJP by M3 helper | reverse finite loop |
| `alpha,beta` | `[B,N]` | recompute during VJP by M3 helper | final transport potentials |
| transport matrix `T` | `[B,N,N]` | materialized for dense route | value path and diagnostics |

This ledger is dense and therefore not memory-disciplined for large `N`.  M6
is the first phase allowed to claim measured memory improvement or reject the
route on memory grounds.

## Mask Policy

The fixed resampling mask remains authoritative:

- `fixed_resampling_mask[:, t]` selects active rows at time `t`;
- inactive rows must pass through identity transport and original log weights;
- active rows receive the manual dense transport and uniform log weights;
- no ESS/runtime branch may replace the fixed mask.

M5 must test at least one mixed mask with active and inactive rows.

## Randomness Policy

The value recursion remains fixed-branch and deterministic:

- `pre_flow_particles` are fixed inputs;
- `fixed_resampling_mask` is a fixed input;
- callbacks must not contain hidden RNG;
- no `tf.random`, NumPy RNG, or Python `random` may be introduced.

M5 should reuse the existing source checks that reject forbidden RNG tokens.

## M5 Test Handoff

M5 should add focused tests before any larger smoke:

1. Opt-in route is accepted only for the new explicit experimental route name.
2. Defaults remain unchanged.
3. Existing `raw`, `filterflow_clipped`, and `filterflow_custom_op` route
   behavior remains available.
4. Unsupported manual-route combinations reject:
   - streaming;
   - warmstart;
   - vector `epsilon`;
   - any `transport_ad_mode` other than `stabilized`.
5. Tiny dense transport-matrix value parity against the M3 value helper under
   the same stopped-key scalar.
6. Tiny dense transport-matrix gradient parity for particles/log weights
   against raw TensorFlow autodiff of the same stopped-key value helper.
7. Small value/score smoke using the existing `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`
   fixture style:
   - CPU/float64;
   - `B<=3`, `N<=4`, `T<=3`;
   - mixed fixed mask;
   - finite value and score;
   - graph/eager parity if route is graph-compatible.

Canonical comparators:

- transport value comparator: M3 value helper for the same stopped-key scalar;
- transport gradient comparator: tiny raw TensorFlow autodiff of that same M3
  value helper;
- value/score smoke comparator: current fixed-branch value/score fixture style
  at tiny scale, with raw AD only where cheap and same-route scalar parity is
  available.

Initial tolerances unless M5 explicitly patches the subplan before running:

- transport value max absolute error: `1e-10`;
- transport gradient max absolute error: `1e-8`;
- tiny value/score graph/eager parity: `1e-10`;
- finite value/score/gradient: required.

M5 must not use central FD as the primary promotion criterion.  Tiny raw AD is
allowed only because the fixture is small.  These checks are go/no-go gates for
tiny opt-in integration only, not evidence for wider route validity.

## Stop Conditions For M5

M5 must stop and write a blocker if:

- the opt-in route cannot be isolated from defaults;
- value parity fails on tiny dense cases;
- gradients are nonfinite;
- unsupported hyperparameter gradients reconnect;
- masks change scalar behavior;
- graph/eager behavior diverges without explanation;
- integration requires a different scalar than M3;
- any plan tries to run P82/N10000 validation before M6/M7.

Any failure of unsupported-combination rejection, mixed-mask behavior, tiny
transport value parity, tiny transport gradient parity, finite value/score, or
graph/eager parity when graph mode is claimed must stop M5.  Do not advance to
broader fixtures or M6 after such a failure without a visible repair loop and
focused rerun.

## Nonclaims

This design does not conclude:

- implementation correctness;
- memory discipline;
- streaming/chunked feasibility;
- SIR d18 readiness;
- P82 FD agreement;
- GPU/TF32 evidence;
- HMC/default/posterior/production readiness.
