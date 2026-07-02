# Phase R14 Plan: Manual Dense Sinkhorn `tf.while_loop` Repair

Date: 2026-06-30

Status: `ACTIVE`

## Objective

Repair the Contract E manual dense finite Sinkhorn value and VJP recursions so
finite Sinkhorn iteration count is represented by TensorFlow `tf.while_loop`
inside XLA, not by Python-unrolled `range(steps)`.

## Entry Conditions

- R12 fixed the all-`NaN` GPU score route by using the manual reverse-scan
  route.
- R12 still failed the exact Kalman `2*MCSE` gate.
- R13 attempted a Sinkhorn-budget ladder but was blocked because the manual
  dense finite Sinkhorn forward/VJP helpers were Python-unrolled by step count.

## Required Artifacts

- Patch to
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
- Route-audit guard proving the two manual dense finite Sinkhorn helpers no
  longer contain `for _ in range(steps)` and do contain `tf.while_loop`.
- Local check output for primitive adjoint tests and Contract E route tests.
- R14 result/closeout under `docs/plans`.

## Evidence Contract

- Engineering question: can the manual dense finite Sinkhorn forward and VJP
  recursions be represented as compact TensorFlow while loops without changing
  their numerical outputs or manual adjoints?
- Comparator: existing tiny dense autodiff/manual-adjoint tests and existing
  Contract E manual-route tests.
- Primary pass criterion:
  - targeted tests for manual adjoint primitives and Contract E manual route
    pass;
  - static route audit confirms `tf.while_loop` is present and Python
    `range(steps)` is absent in the two Sinkhorn recursion helpers.
- Veto diagnostics:
  - any `GradientTape`, `.gradient`, `.jacobian`, or `tf.linalg.eigh` appears
    in the manual route helpers;
  - primitive VJP/JVP tests regress;
  - Contract E reset route tests regress;
  - GPU smoke/rerun uses CPU, non-XLA, non-TF32, or non-manual score route.
- Explanatory diagnostics: compile/runtime warnings, row residuals, z-scores,
  and GPU memory behavior in any rerun.
- Not concluded even if R14 passes: no claim that the LGSSM gradient gate is
  fixed, no default Sinkhorn budget promotion, no SIR/SV correctness, and no
  HMC readiness.

## Skeptical Plan Audit

- Wrong baseline risk: changing loop representation must preserve the same
  finite recursion, not alter Sinkhorn math.  Existing tiny oracle tests are the
  primary protection.
- Proxy metric risk: compile improvement is not enough; value/VJP parity tests
  must pass before the repaired route can be used for R13-style evidence.
- Hidden assumption risk: `steps` remains a validated nonnegative Python scalar
  for TensorArray sizing and `maximum_iterations`; the runtime recursion itself
  must be a TensorFlow while loop.
- Boundary risk: do not touch unrelated streaming Sinkhorn work or change
  default budgets in this phase.

Audit status: `PASS`.

## Planned Implementation

1. Replace the forward `for _ in range(steps)` in
   `_filterflow_manual_dense_finite_sinkhorn_outputs` with a `tf.while_loop`
   carrying `(iteration, running, a_y, b_x, a_x, b_y)`.
2. Replace the VJP forward replay loop with a `tf.while_loop` that writes
   `(running, a_y, b_x, a_x, b_y)` to TensorArrays before each update.
3. Replace the reverse Python loop over `reversed(states)` with a descending
   `tf.while_loop` that reads the TensorArray state at `index - 1`.
4. Add/refresh a static test guard for these exact helpers.

## Required Checks

```bash
python -m py_compile \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py
python -m pytest \
  tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py \
  tests/test_contract_e_phase3_gradient_route_audit.py \
  tests/test_contract_e_cholesky_ridge_reset.py \
  -q
```

If those pass, run a bounded GPU/XLA/TF32 rerun.  Start with the R13 ladder
through `steps20`; add `steps50` only if the repaired route compiles and runs
cleanly through `steps20`.

## Stop Conditions

- Stop if Claude review finds a material plan flaw that cannot be patched
  locally.
- Stop if the static route audit still finds Python-unrolled Sinkhorn loops.
- Stop if primitive adjoint tests fail.
- Stop if GPU rerun fails because the route is not GPU/XLA/TF32/manual-score.
- Stop if `steps20` remains compile-blocked after the while-loop repair; record
  this as a separate XLA/kernel scaling blocker rather than interpreting it as
  Sinkhorn convergence evidence.

## Next-Phase Handoff Conditions

R15 may rerun the full Sinkhorn-budget ladder only after R14 has a passing
static route audit and targeted primitive/manual-route tests.  R15 must preserve
the exact GPU/XLA/TF32/manual-score route and the Kalman `2*MCSE` evidence
contract.
