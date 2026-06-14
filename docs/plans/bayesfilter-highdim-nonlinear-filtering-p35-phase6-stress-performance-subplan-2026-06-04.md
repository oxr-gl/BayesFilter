# P35 Phase 6 Subplan: Stress Models And Performance Ladder

metadata_date: 2026-06-04

parent_plan:
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-p35-zhao-cui-production-implementation-plan-2026-06-03.md`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- Stress-model success does not imply DSGE readiness.
- Short performance ladders do not establish production scalability.
- GPU smoke success does not establish numerical correctness.

## Evidence Contract

Question: after exact small-model value and derivative tests pass, how far can
the fixed-branch squared-TT implementation scale on Zhao--Cui-style stress
models before attempting DSGE-style models?

Promotion criteria:
- stress models run with finite diagnostics;
- memory and wall-time are recorded over dimension/rank/degree/horizon ladders;
- accuracy comparisons are recorded when references exist;
- failure modes are classified as implementation, tuning, approximation, or
  resource failures.

Veto diagnostics:
- nonfinite log likelihood or score;
- branch mismatch in derivative runs;
- deterministic replay failure on the selected stress configuration;
- memory use exceeds declared budget;
- rank saturation without a recorded failure decision;
- exact Phase 0--5 tests regress.

## Planned File Ownership

Allowed writes:

```text
bayesfilter/highdim/models.py
bayesfilter/highdim/validation.py
tests/highdim/test_scaling_smoke.py
docs/plans/*p35-phase6*result*.md
```

GPU/CUDA commands must follow `AGENTS.md`: any GPU detection, benchmark, or
GPU TensorFlow command requires escalated sandbox permissions.

## Stress Model Ladder

### Ladder A: Zhao--Cui-Style Linear-Gaussian

Purpose: scaling with known exact references.

Vary:

```text
state_dim: 1, 2, 4, 8
parameter_dim: 0, 1, 2
horizon: 1, 2, 5, 10
rank: 1, 2, 4, 8
degree: 2, 3, 5
```

Record exact evidence error, filtering marginal error, score error, memory,
time, ranks, and complexity gates.

### Ladder B: Stochastic Volatility

Purpose: nonlinear likelihood stress with low state dimension and longer
horizon.

Compare against:

- dense quadrature for tiny horizons where possible;
- particle-filter or existing reference only as explanatory diagnostics, not
  promotion criteria unless separately planned.

### Ladder C: SIR

Purpose: constrained nonlinear dynamics and observation likelihood stress.

Record positivity/domain failures separately from TT approximation failures.

### Ladder D: Predator-Prey

Purpose: difficult nonlinear stress only after state-domain policy is settled.

Do not run this ladder until the positivity/log-state contract is specified.

## Performance Metrics

Record:

```text
git commit
command
environment
CPU/GPU status
random seeds
dtype
model dimensions
rank/degree/horizon
row/column budgets
peak memory if available
wall time
fit residual
holdout residual
normalizer diagnostics
branch hash
failure status
deterministic replay status
```

## Backend Policy

Default implementation remains TensorFlow/TFP.  If GPU acceleration is tested,
record escalated GPU probe and TensorFlow device visibility.  JAX/PyTorch
experiments require a separate reviewed backend-exception plan before they can
influence production implementation.

## Tests And Commands

Smoke tests:

```bash
pytest -q tests/highdim/test_scaling_smoke.py
```

Long ladders require separate experiment/result notes under `docs/plans/` with
the evidence contract and run manifest filled before execution.

## Exit Criteria

- Phase 0--5 tests remain green.
- Scaling smoke passes.
- At least one result note records linear-Gaussian scaling with exact reference
  errors.
- Stress failures are classified, not hidden.
- No public API exposure occurs in Phase 6.
- A DSGE trial plan is allowed only after this phase's result ledger says which
  dimension/rank/horizon budget is defensible.
