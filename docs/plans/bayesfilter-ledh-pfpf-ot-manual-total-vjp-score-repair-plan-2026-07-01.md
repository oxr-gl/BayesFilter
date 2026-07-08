# LEDH-PFPF-OT Manual Total-VJP Score Repair Plan

Date: 2026-07-01

Status: draft for Claude read-only review before execution.

## Objective

Repair the LEDH-PFPF-OT manual transport score route so that the manual
gradient computes the total derivative of the finite-particle log-likelihood
value actually executed by the code.

The target is the ordinary score of the finite-particle objective
\[
  \nabla_\theta \widehat\ell_N(\theta)
  =
  {d\over d\theta}F(\theta,z(\theta)).
\]
The current stopped route computes only a partial derivative
\[
  \partial_\theta F(\theta,z)\big|_{z=z(\theta)}
\]
for the transport normalization/key variables \(z(\theta)\).  That is wrong
relative to the score target.

## Current Root Cause

The current manual transport reverse pass maps an adjoint of the normalized
particles
\[
  u_i={x_i-\bar x\over s(x)}
\]
back to the original particles as if \(\bar x\) and \(s(x)\) were constants:
\[
  \bar x_i \leftarrow \bar x_i + {\bar u_i\over s}.
\]
That formula is correct only for the artificial map
\[
  u_i={x_i-c\over s}
\]
with fixed \(c\) and \(s\).  For the actual map, the VJP must include the mean
and scale terms.  In addition, the manual finite Sinkhorn route currently stops
the cost keys and does not propagate through the adaptive starting epsilon
\(\epsilon_0(u)\).  Those omissions also change the derivative target.

## Evidence Contract

Question:
Can the manual transport score route be changed from a stopped partial
derivative into the total derivative of the executed finite-particle objective?

Baseline/comparators:

- Exact finite-particle scalar value from the current forward code.
- CPU float64 TensorFlow tape for the same fixed finite-Sinkhorn route.
- CPU float64 central finite differences for the same fixed finite-Sinkhorn
  route.
- Raw/full convergence-loop TensorFlow tape only as an explanatory comparator,
  because it is not the same finite scalar as the manual fixed-iteration route.
- Existing stopped route only as a negative control, not as a correctness
  comparator.

Primary pass criteria:

- New manual total-VJP route agrees with same finite-route tape on tiny
  active-transport SIR within the predeclared tolerance.
- New manual total-VJP route agrees with central FD on tiny active-transport SIR
  within the predeclared tolerance.
- No-resampling route remains unchanged and agrees with FD/tape.
- Existing primitive tests either pass or are updated to test the correct total
  derivative instead of the stopped partial derivative.

Veto diagnostics:

- Nonfinite values or gradients.
- Manual total-VJP differs from same finite-route tape on the tiny active SIR
  diagnostic.
- Manual total-VJP differs from FD when raw/full tape agrees with FD.
- A route is called "score" while still omitting known mean, scale, key, or
  \(\epsilon_0\) derivative terms.
- GPU/TF32 claims are made from CPU float64 diagnostics.

Explanatory diagnostics:

- Size of the old stopped-route gap versus FD.
- Per-parameter and per-seed gradient differences.
- Which omitted term accounts for the largest correction, if decomposed.

What will not be concluded:

- No HMC readiness.
- No posterior correctness.
- No material GPU/TF32 validation.
- No claim that the full derivative is numerically stable at production scale
  until a separate GPU/XLA plan is run.

## Skeptical Plan Audit

Known risk:
Deleting `tf.stop_gradient` alone does not repair the manual score.  The manual
reverse loop is hard-coded.  The VJP formulas must be changed.

Wrong-baseline risk:
The old stopped-gradient route cannot be used as the correctness baseline.  It
is the rejected partial derivative.  Raw/full convergence-loop tape also cannot
be the primary baseline for the manual fixed-iteration route when it executes a
different finite scalar.  The correct baseline is tape and FD for the same
finite scalar.

Proxy-metric risk:
Primitive parity against another stopped primitive is not enough.  The promotion
criterion must compare the end-to-end manual total-VJP score to raw/full and FD.

Environment risk:
CPU float64 tiny diagnostics are allowed for mathematical repair.  They must not
be reported as production GPU/TF32 evidence.

Plan status after audit:
Execution may begin only after Claude review converges or reaches five rounds.

## Phase 1: Documentation And Derivation Repair

Artifacts:

- Update `docs/chapters/ch32c_entropic_ot_sinkhorn.tex` or the more specific
  local chapter section if found during execution.
- Add a proposition-proof statement:
  - stopped-gradient route is a partial derivative;
  - total derivative requires VJP through normalization and transport keys;
  - if a method calls the partial derivative a score, it is wrong relative to
    that claim.

Required derivation:

For \(u_i=(x_i-\bar x)/s(x)\), if \(a_i=\partial L/\partial u_i\), then
\[
  dL
  =
  \sum_i a_i^\top {dx_i-d\bar x\over s}
  -
  \left(\sum_i a_i^\top (x_i-\bar x)\right){ds\over s^2}.
\]
Therefore
\[
  \bar x_i
  =
  {a_i\over s}
  -
  {1\over N}\sum_k {a_k\over s}
  -
  {1\over s^2}
  \left(\sum_k a_k^\top (x_k-\bar x)\right)
  \nabla_{x_i}s(x).
\]

The implemented `s(x)` is
\[
  s(x)=\sqrt d\,\max_j \operatorname{std}_i(x_{ij})
\]
with a one-valued fallback when the diameter is zero.  Its derivative is
piecewise defined and nonsmooth at ties and at the zero fallback.  The code must
either implement the TensorFlow subgradient of the executed map or explicitly
define and test a smooth replacement.

Stop conditions:

- Stop if the LaTeX section cannot state the target and computed quantity
  without ambiguity.
- Stop if a proposed derivation still treats parameter-dependent quantities as
  constants while calling the result a score.

## Phase 2: Code Repair

Artifacts:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- focused tests under `tests/`

Implementation requirements:

1. Add new total-derivative route names rather than silently changing the old
   stopped route:
   - `manual_streaming_finite_sinkhorn_total_vjp`
   - `manual_streaming_blockwise_vjp_finite_sinkhorn_total_vjp`
   or equivalent names that do not contain `stopped_scale_keys`.
2. Keep old stopped names only as deprecated/diagnostic partial-derivative
   routes. They must not be documented as score routes.
3. Remove `tf.stop_gradient` from the total-route forward value calculation.
4. Repair the manual VJP through:
   - particle centering;
   - scale \(s(x)\);
   - Sinkhorn cost keys;
   - adaptive \(\epsilon_0(u)\), unless a fixed \(\epsilon_0\) option is
     explicitly chosen and recorded as the finite objective.
5. In the SIR manual reverse loop, replace
   `d_post_flow = d_particles + d_scaled_x / scale[:, None, None]`
   with the correct VJP through \(u=(x-\bar x)/s(x)\).
6. Do not claim the old stopped route is correct, approximately correct, or a
   surrogate score unless a separate objective and support are written.

Acceptable implementation strategy:

- Use TensorFlow tape for the same finite fixed-iteration route as the tiny
  reference comparator.
- If deriving the scale/key/\(\epsilon_0\) VJP directly is too large for the
  first repair, implement a small custom-gradient bridge that uses TensorFlow to
  compute the VJP of the local normalization/key map while keeping the outer
  transport recursion manual.  This is acceptable only if tests show the
  resulting gradient equals the full derivative of the executed finite scalar.

Stop conditions:

- Stop if the repair would require changing the finite scalar value without a
  new reviewed objective.
- Stop if the manual route cannot be compared to same finite-route tape and FD
  on a tiny diagnostic.
- Stop if the implementation only deletes `stop_gradient` but leaves the VJP
  formula unchanged.

## Phase 3: Tests And Diagnostics

Required checks:

```bash
python -m py_compile \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py \
  experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py \
  docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py

pytest -q tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
pytest -q tests/test_p8p_sir_active_transport_comparator_contract.py
```

Add or update a focused diagnostic so that the active-transport tiny SIR result
expects:

- manual total-VJP approximately equals same finite-route tape;
- same finite-route tape approximately equals FD;
- old stopped route differs when the missing terms are nonzero.

If any command uses GPU/CUDA, run it only with escalated permissions and record
it as GPU evidence.  The initial repair should use CPU float64 unless a reviewed
GPU phase is added.

## Claude Review Requirements

Before execution:

- Claude must review this plan read-only.
- Give Claude exact paths and ask for material blockers only:
  - wrong mathematical target;
  - omitted VJP terms;
  - insufficient tests;
  - unsafe route renaming/default changes;
  - evasive language.
- Iterate fixes up to five rounds.

After execution:

- Claude must review the diff, tests, and result note read-only.
- Claude cannot authorize scientific claims or production promotion.

## Close Record

Write a result note under `docs/plans/` with:

- files changed;
- derivation summary;
- exact checks run;
- key numerical comparison table;
- Claude review outcome;
- remaining limitations;
- next GPU/XLA validation plan if the CPU float64 repair passes.
