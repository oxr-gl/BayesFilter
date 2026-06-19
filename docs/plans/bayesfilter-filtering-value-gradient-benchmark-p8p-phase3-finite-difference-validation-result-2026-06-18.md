# P8p Phase 3 Result: Central Finite-Difference Validation

Date: 2026-06-18

Status: `BLOCKED_AD_FD_RESIDUAL_EXCEEDS_PREDECLARED_TOLERANCE`

## Phase Objective

Validate the P8p theta-gradient on the same fixed-randomness diagnostic SIR d18
target using a more deliberate central finite-difference check than the Phase 2
smoke.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | On a small fixed-randomness SIR d18 diagnostic target, do AD gradients and central finite differences agree in sign and reasonable scale for all theta components while preserving Phase 2 route guarantees? |
| Baseline/comparator | Phase 2 passed tiny smoke and same-target central finite differences. |
| Primary pass criterion | Phase 3 passes if the run preserves Phase 2 route/artifact guarantees, all AD and FD components are finite, signs agree for all nonzero components, and each absolute AD-FD residual is within `max(10.0, 0.20 * max(1, abs(fd)))`. |
| Veto diagnostics | Missing theta-zero parity; nonfinite value/gradient/FD; disconnected theta component; repeated-evaluation drift; categorical resampling; missing trusted GPU placement; sign disagreement; residual beyond tolerance; changing tolerance after seeing result. |
| Not concluded | Exact score correctness, stochastic PF marginal-gradient correctness, full-horizon stability, HMC readiness, posterior convergence, production/default readiness, or filter ranking. |

## Checks

Prechecks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-*
```

Both passed.

Trusted GPU command:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --time-steps 3 \
  --num-particles 16 \
  --batch-seeds 81120,81121 \
  --theta 0.02,-0.01,0.01 \
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

Artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8p-phase3-finite-difference-validation-2026-06-18.json`

Post-run validation command:

```bash
python - <<'PY'
# computed AD/FD residuals against predeclared tolerance
PY
```

## Route Guarantees

The run preserved the Phase 2 route guarantees:

| Field | Status |
| --- | --- |
| Trusted GPU output devices | passed |
| Theta-zero P8j parity | passed, max abs delta `0.0` |
| Values finite | passed |
| Gradients finite | passed |
| All theta components connected | passed |
| Repeated same-theta value delta | `0.0` |
| Repeated same-theta gradient delta | `0.0` |
| Random streams fixed across theta | true |
| Resampling mask fixed | true |
| Relaxed Sinkhorn OT used | true |
| Categorical resampling used | false |

## AD Versus FD Gate

The predeclared tolerance was:

```text
abs(AD - FD) <= max(10.0, 0.20 * max(1, abs(FD)))
```

| Parameter | AD | FD | Abs residual | Tolerance | Sign OK | Gate |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `log_kappa_scale` | `-312.2449951171875` | `-224.6017303466797` | `87.64326477050781` | `44.92034606933594` | true | fail |
| `log_nu_scale` | `113.51848602294922` | `135.07843017578125` | `21.55994415283203` | `27.01568603515625` | true | pass |
| `log_obs_noise_scale` | `44.57378005981445` | `117.40874481201172` | `72.83496475219727` | `23.481748962402346` | true | fail |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Block Phase 3 and stop before full-horizon probing. | Failed.  Two AD/FD residuals exceed the predeclared tolerance. | Veto fired: residual beyond tolerance. | It is unclear whether the mismatch is due to finite-difference step/noisy nonsmooth relaxed OT numerics, TF32 precision, a missing gradient path in theta-dependent covariance/log-density wiring, or a genuine gradient bug. | Write/review a focused Phase 3 repair subplan before rerunning; first discriminate step-size/precision effects and inspect covariance/transport gradient paths. | No exact score correctness, no full-horizon gradient stability, no HMC readiness, no posterior validity, no production/default readiness. |

## Post-Run Red Team

Strongest alternative explanation:

- The objective is connected and repeatable, but finite differences through
  relaxed OT and PF correction may be noisy or step-size sensitive at `float32`
  TF32.  That would not prove a code bug, but it is still a Phase 3 validation
  failure under the declared gate.

What would overturn this blocker:

- A reviewed focused repair/rerun showing AD/FD residuals pass under a
  predeclared step-size/precision diagnostic without changing the target after
  seeing the result.

Weakest part of the evidence:

- Only one step size and precision mode were used in Phase 3.  The next repair
  should separate finite-difference step sensitivity from actual AD wiring
  failure.

## Implementation Note

The Phase 3 JSON currently contains `"phase": "P8p Phase 2"` because the first
harness version hardcoded the phase label.  This is metadata-only and did not
affect the numerical gate.  The harness and Phase 2/3 subplans were patched to
accept `--phase-label` before future reruns.

## Handoff

Do not advance to Phase 4 full-horizon gradient probing.  The next safe action
is a focused Phase 3 repair subplan with:

- FD step ladder, for example `1e-2`, `5e-3`, `1e-3`, `5e-4`, `1e-4`;
- precision comparison, at least `float32 TF32 enabled` versus `float32 TF32
  disabled`, and possibly tiny CPU `float64`;
- isolated value-only theta-zero parity retained;
- no full-horizon run until AD/FD validation passes or the blocker is
  reclassified with review.
