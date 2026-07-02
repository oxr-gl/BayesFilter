# Phase R13 Blocker: GPU XLA Sinkhorn Budget Ladder

Date: 2026-06-30

Status: `BLOCKED_EXECUTION_DESIGN`

## Question

R13 was intended to test whether the remaining Contract E LGSSM score/value
gate failure was explained by too few finite Sinkhorn iterations.  The planned
route was GPU, TensorFlow `float32`, TF32 enabled, XLA enabled, batched seeds,
Contract E Cholesky-ridge reset, and manual reverse-scan score.

## What Happened

The runner was launched with:

```bash
bash scripts/run_contract_e_r13_gpu_sinkhorn_budget_ladder.sh
```

The command entered the high-budget ladder and became dominated by XLA
compile/host work.  During the stall, code tracing found that the manual dense
finite Sinkhorn primitives still used Python-unrolled loops:

- `_filterflow_manual_dense_finite_sinkhorn_outputs`
- `_filterflow_manual_dense_finite_sinkhorn_vjp`

Both helpers used `for _ in range(steps)`.  Therefore the `steps50` rung was
not a clean compact XLA while-loop budget test.  It was also testing giant graph
construction/compilation as the step count increased.

The run was interrupted after the design flaw was identified.  The final
stderr included an XLA/PTX internal failure while the interrupt was propagating,
so the interrupted process is not interpretable as a numerical Sinkhorn
convergence result.

## Decision

Do not interpret R13 as evidence for or against the Sinkhorn-budget hypothesis.
R13 is blocked by execution design.  The next phase must first repair the
manual dense finite Sinkhorn forward and VJP recursions to use `tf.while_loop`
inside XLA, then rerun a bounded ladder.

## Evidence Preserved

- R13 plan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r13-gpu-xla-sinkhorn-budget-ladder-plan-2026-06-30.md`
- R13 runner:
  `scripts/run_contract_e_r13_gpu_sinkhorn_budget_ladder.sh`
- Relevant implementation:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`

## Nonclaims

- No claim that Sinkhorn budget is or is not the LGSSM gradient root cause.
- No claim that `steps50` is numerically invalid.
- No CPU fallback evidence.
- No production default change.
