# P8p SIR Sinkhorn Budget Hypothesis Diagnostic Plan

Date: 2026-06-27

## Question

Does the P8p parameterized SIR d18 gradient mismatch suffer from the same
finite-Sinkhorn under-convergence issue that was found in the LEDH-PFPF-OT
LGSSM diagnostic?

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | On the same fixed-randomness short SIR d18 target, does increasing only the finite Sinkhorn budget reduce streaming row residuals, and does the manual-gradient versus FD-regression discrepancy shrink when the residual passes? |
| Baseline/comparator | P8p SIR d18 target with fixed seeds, theta, chunks, dtype, TF32 policy, manual streaming reverse score route, and 13-point raw-coordinate regression FD. Candidate budgets: `10`, `100`, `200`, `400`. |
| Primary diagnostic criterion | The hypothesis is supported only if `steps=10` has row residual above the predeclared threshold, larger budgets reduce/pass row residual, and the manual-minus-FD z-scores also improve materially. |
| Veto diagnostics | Nonfinite values/gradients/FD slopes, missing trusted GPU placement when GPU is claimed, row residual not recorded, failed script smoke, timeout/missing artifact, or accidental use of `transport_ad_mode=full`. |
| Explanatory only | FD slope standard error, R2, objective values, compile/timing, TF allocator telemetry, and column residual placeholder on the manual streaming route. |
| Not concluded | No SIR gradient correctness, HMC readiness, posterior correctness, production readiness, default-policy change, or claim that Sinkhorn budget is the only remaining issue. |

## Skeptical Plan Audit

- Wrong-baseline risk: the run reuses the P8p fixed-randomness SIR target and
  changes only `sinkhorn_iterations`; theta, seeds, chunks, dtype, TF32, and
  transport route are fixed.
- Proxy-risk: row residual is a numerical validity veto, not a correctness
  proof.  FD agreement is interpreted only after row residual is visible.
- FD-noise risk: the diagnostic uses 13 points, drops the lowest and highest
  objective values, and records slope standard error rather than relying on a
  single central difference.
- Environment risk: GPU evidence must run with trusted/escalated device access;
  CPU smoke is only a wiring check.
- Boundary risk: this adds a diagnostic script and artifacts only.  It does not
  edit production LEDH/SIR behavior or old result files.

Audit status: PASS for bounded diagnostic execution.

## Commands

CPU smoke:

```bash
python docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --time-steps 1 \
  --num-particles 4 \
  --batch-seeds 81120 \
  --candidate-steps 2 \
  --regression-offsets=-3,-2,-1,0,1,2,3 \
  --trim-extreme-values 1 \
  --row-chunk-size 4 \
  --col-chunk-size 4 \
  --particle-chunk-size 4 \
  --manual-reverse-compiler eager \
  --output /tmp/p8p_sir_sinkhorn_budget_smoke.json
```

Trusted GPU diagnostic:

```bash
/usr/bin/timeout 3600 python docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --time-steps 3 \
  --num-particles 64 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --theta 0.02,-0.01,0.01 \
  --candidate-steps 10,100,200,400 \
  --base-step 0.001 \
  --regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6 \
  --trim-extreme-values 1 \
  --sinkhorn-epsilon 1.0 \
  --row-chunk-size 64 \
  --col-chunk-size 64 \
  --particle-chunk-size 64 \
  --seed-microbatch-size 0 \
  --theta-offset-batch-size 13 \
  --dtype float32 \
  --tf32-mode enabled \
  --manual-reverse-compiler xla \
  --progress-output docs/plans/bayesfilter-p8p-sir-sinkhorn-budget-hypothesis-diagnostic-progress-2026-06-27.json \
  --output docs/plans/bayesfilter-p8p-sir-sinkhorn-budget-hypothesis-diagnostic-2026-06-27.json \
  --markdown-output docs/plans/bayesfilter-p8p-sir-sinkhorn-budget-hypothesis-diagnostic-2026-06-27.md
```

Fallback trusted GPU diagnostic if the full ladder is killed by XLA compile or
resource limits:

```bash
/usr/bin/timeout 2400 python docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --time-steps 3 \
  --num-particles 64 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --theta 0.02,-0.01,0.01 \
  --candidate-steps 1,2,5,10,20 \
  --base-step 0.001 \
  --regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6 \
  --trim-extreme-values 1 \
  --sinkhorn-epsilon 1.0 \
  --row-chunk-size 64 \
  --col-chunk-size 64 \
  --particle-chunk-size 64 \
  --seed-microbatch-size 0 \
  --theta-offset-batch-size 13 \
  --dtype float32 \
  --tf32-mode enabled \
  --manual-reverse-compiler xla \
  --progress-output docs/plans/bayesfilter-p8p-sir-sinkhorn-budget-hypothesis-diagnostic-fallback-progress-2026-06-27.json \
  --output docs/plans/bayesfilter-p8p-sir-sinkhorn-budget-hypothesis-diagnostic-fallback-2026-06-27.json \
  --markdown-output docs/plans/bayesfilter-p8p-sir-sinkhorn-budget-hypothesis-diagnostic-fallback-2026-06-27.md
```

Fallback interpretation: if low-budget residuals improve/pass by `10` or `20`
but manual-vs-FD z-scores remain large, this argues against the SIR mismatch
being the same simple row-residual under-convergence failure.  It does not rule
out a different Sinkhorn derivative/objective issue.

## Stop Conditions

- Stop after writing and interpreting the result artifact.
- Stop on timeout, nonfinite values, missing GPU placement, or missing residuals.
- Do not launch N1000/N10000 or HMC from this diagnostic.
