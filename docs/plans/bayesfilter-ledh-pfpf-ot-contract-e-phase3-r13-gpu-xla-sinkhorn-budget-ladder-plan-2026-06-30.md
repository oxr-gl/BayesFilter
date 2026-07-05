# Phase R13 Plan: GPU XLA TF32 Manual-Score Sinkhorn Budget Ladder

Date: 2026-06-30

Status: `ACTIVE`

## Objective

Test whether the remaining R12 LGSSM value/score gate failures are explained by
insufficient finite Sinkhorn budget in the Contract E GPU/XLA/TF32 manual-score
route.

## Entry Conditions

- R12 established that the R11 all-`NaN` score failure was score-route wiring.
- R12 manual reverse-scan route produced finite GPU/XLA/TF32 scores.
- R12 still failed the exact Kalman `2*MCSE` gate.
- R12 diagnostics showed very large Sinkhorn row residuals at `eps0.55_steps2`
  (`~0.96` to `~1.00`) while column residuals, ridge selection, and Contract E
  covariance restoration were clean.

## Evidence Contract

- Scientific/engineering question: at fixed `N=1000,T=10,seed_count=10`, does
  increasing the finite Sinkhorn budget reduce row residuals and bring the
  Contract E manual-score value/score closer to exact Kalman?
- Comparator: exact FP64 Kalman value and score for the same LGSSM fixture and
  parameter convention.
- Candidate route: visible GPU, TensorFlow `float32`, TF32 enabled, XLA
  `jit_compile=True`, batched seeds, Contract E Cholesky-ridge reset with
  stopped minimal-ridge chart replay, and manual reverse-scan score route.
- Fixed quantities: `N=1000`, `T=10`, `seed_count=10`, state dimensions
  `D in {2,1}`, theta, observations, initial/transition/residual seed schedules,
  Contract E ridge policy, and Kalman comparator.
- Ladder:
  - `eps0.55_steps2` as the R12 baseline;
  - `eps0.55_steps8` to match the older LGSSM statistical harness budget;
  - `eps0.55_steps20` as a higher-budget finite route;
  - `eps0.55_steps50` as an expensive but still bounded diagnostic rung.
- Primary criterion: for any ladder rung, all requested fixtures must have
  seed-mean value and all three score components within `2*MCSE` of exact
  Kalman.
- Budget-hypothesis support criterion: row residuals should materially decrease
  as steps increase, and Kalman value/score z-scores should move toward zero
  for the previously failing components.
- Veto diagnostics:
  - CPU route or no visible logical GPU;
  - XLA disabled;
  - TF32 disabled;
  - score route is not `manual-reverse-scan`;
  - any nonfinite value or score;
  - ridge failure;
  - covariance residual above `5e-4`;
  - condition proxy above `1e8`;
  - OOM or XLA compile failure.
- Explanatory diagnostics: row/column residuals, seed SDs, MCSEs, z-scores,
  realized ridge, ridge attempts, covariance/mean residuals.
- Not concluded even if a higher rung passes: no FD certificate, no SIR/SV or
  nonlinear correctness, no HMC readiness, no production readiness, and no
  proof that this Sinkhorn budget is globally adequate.
- Artifact: JSON and markdown result under `docs/plans`, plus R13 closeout
  interpreting the ladder.

## Skeptical Plan Audit

- Wrong baseline risk: R13 must include the R12 baseline rung
  `eps0.55_steps2`; otherwise improvement claims lack an apples-to-apples
  anchor.
- Proxy metric risk: row residual improvement is not the primary scientific
  gate.  It explains the mechanism, but exact Kalman `2*MCSE` remains the
  promotion criterion.
- Hidden route drift risk: using CPU, non-XLA, non-TF32, or the outer-tape score
  route would invalidate R13.  The runner manifest and route guard must be
  inspected before interpreting the ladder.
- Runtime risk: the ladder can be compile-heavy.  The planned rungs are bounded
  and use the existing multi-setting runner; if OOM occurs, stop and record the
  highest completed rung rather than falling back to CPU.
- Tuning-overclaim risk: if one rung passes, R13 can nominate a budget for
  follow-up confirmation but cannot promote a default without broader evidence.

Audit status: `PASS`.

## Planned Command

GPU/CUDA commands must be run with escalated/trusted sandbox permissions.

```bash
bash scripts/run_contract_e_r13_gpu_sinkhorn_budget_ladder.sh
```

## Required Checks

Before GPU run:

```bash
python -m py_compile \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py \
  docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py \
  docs/benchmarks/contract_e_reset_tf.py
python -m pytest tests/test_contract_e_phase3_gradient_route_audit.py \
  tests/test_contract_e_cholesky_ridge_reset.py -q
```

After GPU run:

- Read JSON and markdown artifacts.
- Verify route/device manifest: GPU visible, XLA true, TF32 true,
  `manual-reverse-scan`.
- Compare row residuals and Kalman z-scores across settings.
- Write R13 closeout with a decision table and nonclaims.

## Stop Conditions

- Stop if Claude review blocks the plan and the blocker cannot be patched
  locally.
- Stop if local checks fail.
- Stop if GPU/XLA/TF32 route is not active under trusted execution.
- Stop on OOM/XLA compile failure and record the highest completed rung.
- Stop if any rung has nonfinite value or score; do not average it away.
- Stop if all rungs fail without row-residual improvement; the Sinkhorn-budget
  hypothesis is weakened and the next phase should trace estimator bias or VJP
  correctness instead.

## Claude Review Contract

Claude is a read-only reviewer.  Review only whether this R13 plan tests the
right hypothesis, preserves the R12 route contract, avoids proxy-metric
promotion, and has sufficient stop conditions and artifacts.  Claude cannot
authorize default changes or scientific promotion.
