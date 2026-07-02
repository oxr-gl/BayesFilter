# LEDH-PFPF-OT Manual Adjoint Derivation Contract

status: M1_DERIVATION_CONTRACT
date: 2026-06-22

## Purpose

This contract defines the first finite-computation target for the
LEDH-PFPF-OT manual-adjoint/custom-gradient lane.  It is deliberately narrower
than the full production filter:

- dense transport only;
- tiny/small primitive tests only;
- finite Sinkhorn computation, not the exact regularized OT optimizer;
- private opt-in route only;
- no streaming memory claim;
- no SIR d18 or P82 validation claim.

The contract is intended to make M2 primitive VJP/JVP tests precise before any
manual-gradient implementation is written.

## Prior Runtime Evidence Anchors

The governed `N=10000` raw/full-AD route is excluded by recorded runtime
evidence, not by conversation memory:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3j-n10000-full-transport-fd-result-2026-06-19.md`
  records OOM/unbounded-runtime failure for `N=10000`,
  `transport_ad_mode=full`.
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase4-fd-only-ledh-consistency-result-2026-06-22.md`
  records the repeated P82 `N=10000` full-transport AD-only runtime blocker.
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-full-ad-route-correction-2026-06-22.md`
  makes the route non-executable for governed P82 validation.

This exclusion applies to governed large-particle validation.  It does not
forbid tiny dense full-graph TensorFlow autodiff/JVP/VJP references used as M2
oracle checks, provided the fixture is fixed, bounded, and explicitly not
promoted as scale evidence.

## Code Anchors

Current finite transport and filter anchors:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:511`
  implements streaming softmin without materializing the cost matrix.
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:898`
  builds streaming transported particles from potentials.
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1143`
  builds the dense finite transport matrix from dense potentials.
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1182`
  maps dense potentials to a dense transport matrix.
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1201`
  computes dense finite Sinkhorn potentials.
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1242`
  executes the dense finite Sinkhorn loop.
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1426`
  defines the dense log-domain softmin.
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:675`
  inserts dense/streaming annealed transport into the LEDH-PFPF-OT step.
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex:202`
  distinguishes exact regularized OT, finite Sinkhorn, and scalars built from
  the finite computation.

## Object Being Differentiated

M1 does not target the exact regularized OT optimizer.  It targets the finite
program actually executed by dense Sinkhorn-style code.

For the first primitive tests, define inputs:

| Symbol | Code analogue | Shape | M2 gradient status |
|---|---|---|---|
| `X` | `particles` / `x` | `[B, N, D]` | differentiable |
| `ell` | `logw` | `[B, N]` | differentiable |
| `eps` | `epsilon_tensor` | scalar or `[B]` | constant in M2 |
| `gamma` | `scaling_tensor` | scalar | constant in M2 |
| `tau` | `threshold_tensor` | scalar | constant in M2 |
| `K` | `max_iterations_tensor` | scalar int | constant in M2 |
| `mask` | `fixed_resampling_mask` | `[B]` | constant in M2 |

The dense primitive value is the code-defined scalar

```text
S(X, ell) = <A, Y(X, ell)>
```

where:

- `A` is a fixed test cotangent with shape `[B, N, D]`;
- `Y = T(X, ell) X` is the transported particle tensor;
- `T(X, ell)` is the dense finite transport matrix produced by the finite
  Sinkhorn loop and `transport_from_potentials` code path;
- if `mask[b]` is false, the transport branch returns the identity route for
  that batch row.

M2 may also test sub-scalars:

```text
S_bary(T, X) = <A, T X>
S_soft(eps, C, v) = <a, softmin(eps, C, v)>
S_loop(Cxy, Cyx, Cxx, Cyy, ell, beta) = <q, potentials_K>
```

These sub-scalars are test fixtures for primitive adjoints.  They are not
scientific objectives.

## Exact Regularized OT Versus Finite Sinkhorn

The exact regularized OT object solves an optimization problem.  The M1/M2
target is different: it is a finite TensorFlow program using:

- code-defined cost matrices;
- code-defined initial potentials;
- a finite while-loop update;
- code-defined stabilization and final softmin passes;
- code-defined barycentric projection.

Any gradient produced by this lane is a gradient of the finite program selected
by the route contract, not a theorem about the exact regularized OT optimizer.

## First Supported Route

The first supported route is:

```text
manual_dense_finite_sinkhorn_stopped_scale_keys
```

Binding choices:

- dense transport plan;
- tiny/small `B, N, D`;
- no warmstart;
- fixed finite iteration behavior for primitive tests;
- `eps`, `gamma`, `tau`, and `K` treated as constants;
- scale and normalization metadata treated as stopped/frozen;
- no public/default API exposure;
- no streaming or chunked memory claim.

The word "stopped" here is a route contract, not a claim that the existing
`transport_ad_mode=stabilized` implementation already has the desired manual
adjoint.  The manual route must explicitly define which local quantities are
replayed, stopped, and differentiated.

## M2 Oracle Baseline And Environment

The M2 oracle baseline is:

```text
tiny dense full-graph TensorFlow autodiff/JVP/VJP of the same fixed finite
program, with the same fixed iteration count and the same frozen constants.
```

This is allowed only because the fixtures are tiny.  It is not evidence that
raw full AD is feasible for `N=10000`.

M2 is intentionally an oracle-style primitive stage:

- default dtype: `float64`;
- expected execution: CPU-safe unless a later M2 patch explicitly justifies a
  trusted GPU smoke;
- no GPU/TF32 performance, stability, or production-readiness evidence;
- no P82 actual-gradient evidence.

Finite differences in M2 are explanatory step-ladder diagnostics.  They do not
replace the tiny autodiff/JVP/VJP oracle.

## Unsupported In M2

M2 must reject or avoid:

- governed `N=10000` actual-gradient runs;
- streaming transport;
- warmstarted potentials;
- data-dependent early stopping as a differentiated control-flow object;
- gradients with respect to `eps`, `gamma`, `tau`, or `K`;
- public/default integration;
- `transport_ad_mode=full` as the target route;
- HMC/NUTS or posterior-correctness claims.

Existing code modes `full`, `diff-scale`, `diff-keys`, and `diff-potentials`
remain unsupported by the manual-adjoint route until a later phase explicitly
derives and tests them.

## Frozen-Control Boundary

M2 validates the adjoint of a frozen-control finite loop.  It does not validate
gradients through adaptive stopping, through a changing scale schedule, or
through large-particle runtime behavior.  The executed loop count and constants
must be part of each fixture record.

## Memory-Discipline Boundary

Primitive adjoint derivability is not the same as memory discipline.  M1 and M2
can establish only local derivative consistency for dense tiny finite kernels.
The memory ledger begins in M4 and measured memory feasibility begins in M6.

Therefore, passing M1 and M2 does not unblock P82.  P82 remains blocked until
M7 produces a reviewed handoff from a route that has passed the intervening
integration and memory gates.

## Primitive Adjoint Equations

This section states the equations M2 must test.  These equations are a finite
program contract for tests, not an implementation proof.

### Barycentric Projection

For `Y = T X` with `T` shape `[B, N, N]`, `X` shape `[B, N, D]`, and upstream
cotangent `A` shape `[B, N, D]`:

```text
bar_T[b, i, j] += sum_d A[b, i, d] X[b, j, d]
bar_X[b, j, d] += sum_i T[b, i, j] A[b, i, d]
```

This checks only the direct projection.  If `T` itself depends on `X`, the
transport-matrix adjoint must add further contributions to `bar_X`.

### Dense Log-Domain Softmin

The dense softmin code computes

```text
s_i = -eps * logsumexp_j(v_j - C_ij / eps).
```

With `eps` constant and upstream `bar_s_i`, define

```text
p_ij = softmax_j(v_j - C_ij / eps).
```

Then the VJP contributions are:

```text
bar_v_j  += -eps * sum_i bar_s_i p_ij
bar_C_ij +=        bar_s_i p_ij
```

M2 must compare this VJP against TensorFlow autodiff on tiny dense cases.
Gradients with respect to `eps` are out of scope for M2.

### Finite Sinkhorn Loop

The dense loop updates four potential arrays:

```text
a_y, b_x, a_x, b_y
```

using repeated softmin calls, averaging, a finite iteration counter, and final
softmin passes.  M2 may implement the loop adjoint by reverse replay of the
finite update sequence or by a private custom-gradient wrapper, but it must
test the resulting VJP/JVP against TensorFlow autodiff on tiny dense cases.

M2 must not use an unbounded or data-dependent large loop as evidence.  The
primitive tests should force fixed finite iteration behavior or otherwise make
the executed loop count part of the fixture.

### Dense Transport Matrix From Potentials

The dense code-defined transport matrix is

```text
T = exp(temp)
temp_ij = (f_i + g_j - C_ij) / eps
temp_ij = temp_ij - logsumexp_i(temp_ij) + log(N) + ell_i
```

using the normalization axis and broadcasting in the current code.  M2 must
test the VJP of this code-defined map against TensorFlow autodiff.  It must not
replace this map with a mathematically cleaner but different normalization.

## Shape Contract For M2

Primitive fixtures should include at least:

| Fixture | B | N | D | Purpose |
|---|---:|---:|---:|---|
| scalar tiny | 1 | 3 | 1 | easy FD inspection |
| vector tiny | 1 | 4 | 2 | barycentric shape and cost gradients |
| batched tiny | 2 | 3 | 2 | batch broadcasting and mask behavior |

All tests must use deterministic constants or fixed seeds recorded in the test
or result.

## M2 Tolerances

Initial tolerances for `float64` primitive tests:

| Check | Tolerance |
|---|---:|
| value equality between reference and manual route | `1e-10` absolute |
| VJP max absolute error | `1e-8` |
| JVP/VJP directional agreement | `1e-8` |
| finite-difference directional residual | slope error decreasing over a step ladder, diagnostic not primary |

If M2 uses `float32`, it must state separate tolerances before execution.

## Required M2 Tests

M2 must create or update focused tests that cover:

1. barycentric projection VJP;
2. dense log-domain softmin VJP;
3. dense transport-from-potentials VJP;
4. finite Sinkhorn loop VJP/JVP on tiny dense fixed-iteration fixtures;
5. scalar directional finite-difference spot checks;
6. unsupported-route rejection for streaming, warmstart, and full N10000 route
   claims.

## M2 Advancement Rule

M2 may advance to M3 only if:

- every named primitive passes on every listed fixture within tolerance;
- the finite Sinkhorn loop VJP/JVP passes against the tiny full-graph
  autodiff/JVP/VJP oracle;
- unsupported-route rejection passes;
- all values and adjoints are finite;
- the M2 result artifact records the exact dtype, fixtures, tolerances,
  oracle comparator, and observed max errors.

Any primitive parity failure blocks integration or scale-up work.  FD
mismatches are explanatory unless they coincide with autodiff/JVP/VJP
disagreement or expose a fixture/scalar bug.

Failure of any named advancement condition stops M2 promotion and does not
unblock M3 integration, M7 handoff, or P82 validation.

M2 evidence destination:

`docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase2-primitive-vjp-result-2026-06-22.md`

## Boundary For Later Phases

M3 may build a private dense custom-gradient prototype only after M2 passes.
M4 may design filter-loop integration only after the private dense prototype
passes.  M6 is the first phase allowed to make a measured streaming/chunked
memory statement.  P82 may resume only after M7 produces a reviewed handoff.

## Nonclaims

This contract does not conclude:

- manual-adjoint correctness;
- implementation readiness;
- streaming memory improvement;
- SIR d18 readiness;
- P82 FD agreement;
- HMC/NUTS readiness;
- posterior correctness;
- exact likelihood correctness;
- default-gradient readiness;
- production readiness.
