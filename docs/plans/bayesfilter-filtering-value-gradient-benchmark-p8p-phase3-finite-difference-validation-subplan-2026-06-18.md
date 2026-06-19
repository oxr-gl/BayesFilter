# P8p Phase 3 Subplan: Central Finite-Difference Validation

Date: 2026-06-18

Status: `DRAFT_AFTER_PHASE2_PASS`

## Phase Objective

Validate the P8p theta-gradient on the same fixed-randomness diagnostic SIR d18
target using a more deliberate central finite-difference check than the Phase 2
smoke.

Phase 3 is still a computational diagnostic.  It does not prove stochastic PF
marginal-gradient correctness or HMC readiness.

## Entry Conditions Inherited From Previous Phase

Phase 3 may start only if:

- Phase 2 result passed;
- `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py` compiles;
- Phase 2 JSON shows theta-zero P8j parity, fixed random streams, fixed mask,
  relaxed Sinkhorn OT, no categorical resampling, finite connected gradients,
  and trusted GPU placement.

## Required Artifacts

- Phase 3 JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-2026-06-18.json`
- Phase 3 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-result-2026-06-18.md`
- Phase 4 subplan draft:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase4-full-horizon-gradient-probe-subplan-2026-06-18.md`

## Required Checks, Tests, And Reviews

Precheck:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-*
```

Trusted GPU finite-difference validation:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --time-steps 3 \
  --num-particles 16 \
  --batch-seeds 81120,81121 \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P8p Phase 3" \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 1.0 \
  --row-chunk-size 16 \
  --col-chunk-size 16 \
  --particle-chunk-size 16 \
  --dtype float32 \
  --tf32-mode enabled \
  --fd-step 0.0005 \
  --repeat-evaluations 2 \
  --check-theta-zero-p8j-parity \
  --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-2026-06-18.json
```

Review:

- Claude read-only review if finite-difference signs disagree with AD,
  residuals are difficult to interpret, or Phase 4 subplan changes the target
  boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | On a small fixed-randomness SIR d18 diagnostic target, do AD gradients and central finite differences agree in sign and reasonable scale for all theta components while preserving Phase 2 route guarantees? |
| Baseline/comparator | Phase 2 passed tiny smoke and same-target central finite differences. |
| Primary pass criterion | Phase 3 passes if the run preserves Phase 2 route/artifact guarantees, all AD and FD components are finite, signs agree for all nonzero components, and each absolute AD-FD residual is within `max(10.0, 0.20 * max(1, abs(fd)))` for this small noisy diagnostic. |
| Veto diagnostics | Missing theta-zero parity; nonfinite value/gradient/FD; disconnected theta component; repeated-evaluation drift; categorical resampling; missing trusted GPU placement; sign disagreement; residual beyond tolerance; changing tolerance after seeing result. |
| Explanatory diagnostics | Absolute and relative AD-FD residuals, gradient norms, runtime, memory, per-seed values. |
| Not concluded | Exact score correctness, stochastic PF marginal-gradient correctness, full-horizon stability, HMC readiness, posterior convergence, production/default readiness, or filter ranking. |

## Forbidden Claims And Actions

- Do not claim HMC readiness from Phase 3.
- Do not change finite-difference tolerance after seeing the result.
- Do not run full-horizon `N=10000` or `N=50000` in Phase 3.
- Do not mutate unrelated Zhao-Cui fixed-branch or monograph files.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if:

- Phase 3 result passes the declared FD validation criterion;
- Phase 4 subplan is drafted for full-horizon gradient probing with a bounded
  particle count and runtime budget;
- any residual concern is documented as explanatory or blocking.

## Stop Conditions

Stop and write a blocker if:

- AD and FD signs disagree;
- residuals exceed the declared tolerance;
- the run violates Phase 2 fixed-randomness or relaxed-OT route guarantees;
- trusted GPU placement cannot be verified;
- a new target or prior decision is required from the user.
