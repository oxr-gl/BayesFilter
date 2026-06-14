# P3 Plan: Finite Sinkhorn Resampler

Date: 2026-05-28

## Evidence Contract

Question: can the lane implement a finite-budget entropic OT/Sinkhorn relaxed
resampler with explicit residuals and caveats?

Comparator/reference: declared source and target marginals for a finite cost
matrix; IE5 residual semantics.

Primary criterion: the resampler returns a finite nonnegative coupling with
bounded row/column/mass residuals, finite barycentric particles, declared
epsilon, iteration budget, stabilization mode, tolerance, cost function, and
target marginal.

Veto diagnostics: non-finite cost/coupling, negative coupling beyond tolerance,
row/column residual above tolerance, missing epsilon/budget/stabilization, or
claiming categorical or unregularized-OT equivalence.

Explanatory-only diagnostics: residual trend and runtime.

What will not be concluded: no exact categorical resampling, exact
unregularized OT, posterior preservation, HMC target validity, or production
readiness.

## Skeptical Plan Audit Checklist

Check stale context, wrong baseline, proxy overclaim, missing stop conditions,
hidden production drift, monograph drift, vendored-code contamination,
high-dimensional-lane contamination, and artifact fitness.

## Inputs

- DPF2 component spec and resampling test contract.
- IE5 resampling/Sinkhorn result.

## Outputs

- `experiments/dpf_implementation/resampling/__init__.py`
- `experiments/dpf_implementation/resampling/sinkhorn.py`
- `docs/plans/bayesfilter-dpf-ot-implementation-p3-finite-sinkhorn-resampler-result-2026-05-28.md`

## Implementation Scope

Implement a NumPy log-domain finite Sinkhorn solver and barycentric relaxed
resampling helper.  No learned/neural OT.

## Stop Conditions

Stop if residuals cannot be computed, if the target marginal is ambiguous, or
if exact categorical equivalence would be needed for acceptance.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/resampling/__init__.py experiments/dpf_implementation/resampling/sinkhorn.py
python -c "import numpy as np; from experiments.dpf_implementation.resampling.sinkhorn import sinkhorn_resample; x=np.array([[0.0],[1.0],[2.0]]); w=np.array([0.2,0.3,0.5]); r=sinkhorn_resample(x,w,epsilon=0.5,max_iterations=100); print(r.diagnostics['max_row_residual'], r.diagnostics['max_column_residual'])"
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or
five iterations as in the master program.  This exact command is intentional
per user requirement; if unavailable, stop rather than substitute.

## What Must Not Be Concluded

Finite Sinkhorn residuals validate only the finite solver object under declared
settings, not categorical PF equivalence or posterior correctness.

## Review Record

- Iteration 1: `REJECT` as part of bundle review; patched reviewer-gate wording.
- Iteration 2: `ACCEPT`.
