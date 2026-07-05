# Phase 2 Result: Regional Orthogonal Kappa/Nu Coordinates

Date: 2026-07-01

Status: `PASSED_WITH_PHASE3_HANDOFF`

## Decision

Phase 2 passes as a diagnostic gate.  The regional kappa/nu score expansion
reconstructs scalar kappa, scalar nu, rho, and tau chain-rule sums under the
same GPU/TF32 seed-microbatch route as Phase 1.

The mismatch is best described as mostly an infection-vs-recovery contrast
problem: regional `rho_j = (log_kappa_j - log_nu_j)/sqrt(2)` carries nearly the
same gap pattern as kappa.  The common-rate `tau_j` direction has a smaller but
still visible mismatch.  Nu alone is closer than kappa but not exact.

Phase 3 should audit the RK4 transition sensitivity/VJP before transport terms
are involved.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the problematic direction better described as regional infection-vs-recovery geometry rather than kappa alone? |
| Baseline/comparator | Phase 1 current-code GPU/TF32 seed-microbatch route, same seeds/theta/budget/chunks. |
| Primary criterion | Regional rho/tau diagnostics classify whether the mismatch is concentrated in infection-vs-recovery contrast, common-rate direction, both, or neither, while preserving chain-rule reconstruction. |
| Veto diagnostics | Missing regional mapping, CPU material route, changed baseline seeds/theta/budget, nonfinite diagnostic, unsupported production claim. |
| Nonclaims | No Fisher-orthogonality claim, no HMC readiness, no production regional parameterization, no full score correctness claim. |

## Commands Run

Local checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_regional_orthogonal_gradient_decomposition.py
bash -n scripts/run_sir_gradient_reparam_rootcause_phase2_regional_orthogonal_budget10.sh
pytest -q tests/test_p8p_regional_orthogonal_gradient_decomposition.py
pytest -q tests/test_p8p_regional_kappa_gradient_decomposition.py
```

Material GPU/TF32 run:

```bash
bash scripts/run_sir_gradient_reparam_rootcause_phase2_regional_orthogonal_budget10.sh
```

## Artifacts

- Diagnostic code:
  `docs/benchmarks/benchmark_p8p_regional_orthogonal_gradient_decomposition.py`
- Tests:
  `tests/test_p8p_regional_orthogonal_gradient_decomposition.py`
- Wrapper:
  `scripts/run_sir_gradient_reparam_rootcause_phase2_regional_orthogonal_budget10.sh`
- Material JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase2-regional-orthogonal-budget10-2026-07-01.json`

## Route

The material run used:

- device `/GPU:0`;
- `float32`;
- TF32 enabled;
- streaming transport;
- manual streaming finite Sinkhorn stopped-scale-key gradient;
- seed microbatch size `1`;
- seeds `81120,81121,81122,81123,81124`;
- `T=3`, `N=64`;
- Sinkhorn iterations `10`;
- elapsed time `682.417145651998` seconds.

The artifact records GPU/TF32 route evidence and explicitly records that no
explicit XLA compiler status is claimed.

## Chain-Rule Reconstruction

| Direction | Scalar manual | Sum regional manual | Absolute delta |
| --- | ---: | ---: | ---: |
| `log_kappa` | `-205.1933135986328` | `-205.1933135986328` | `0.0` |
| `log_nu` | `84.62630462646484` | `84.62630462646484` | `0.0` |
| `rho` | `-204.93341064453125` | `-204.9334259033203` | `1.52587890625e-05` |
| `tau` | `-85.25375366210938` | `-85.25375366210938` | `0.0` |

Tolerance was `1.0e-4`; reconstruction passed.

## Aggregate Gaps

| Direction family | Sum FD | Sum manual | FD - manual |
| --- | ---: | ---: | ---: |
| `log_kappa` | `-263.2179145812988` | `-205.19331789016724` | `-58.02459669113159` |
| `log_nu` | `104.27092838287354` | `84.62630987167358` | `19.64461851119995` |
| `rho` | `-260.09749126434326` | `-204.933424949646` | `-55.164066314697266` |
| `tau` | `-111.56081295013428` | `-85.25375056266785` | `-26.30706238746643` |

Interpretation:

- `rho` retains almost all of the kappa-side discrepancy.
- `tau` is not clean, but its aggregate gap is about half the rho gap.
- `log_nu` has a smaller positive mismatch; it is not the main failure mode by
  magnitude.
- The high-gap regions remain `0`, `1`, `6`, `7`, and `8`, with region `4`
  still notable.

## Largest Regional Gaps

| Family | Largest absolute gaps `(region: FD-manual, MCSE)` |
| --- | --- |
| `log_kappa` | `0: -12.610847, 10.455665`; `7: -11.319313, 3.490962`; `1: -10.991699, 4.219496`; `6: -9.088837, 3.397395`; `8: -8.325085, 2.105026` |
| `log_nu` | `1: 4.455915, 1.122789`; `0: 3.886610, 2.591190`; `7: 3.257496, 1.051759`; `6: 2.898286, 0.843234`; `8: 2.661261, 0.565029` |
| `rho` | `0: -11.528683, 9.214918`; `1: -11.254803, 3.739999`; `7: -10.450791, 3.205867`; `6: -8.439097, 2.982064`; `8: -7.701783, 1.875097` |
| `tau` | `0: -6.075865, 5.578575`; `7: -5.306271, 1.736501`; `1: -4.492327, 2.253267`; `4: -4.443133, 2.269618`; `6: -4.257079, 1.833202` |

MCSE remains explanatory, but it does not reverse the qualitative ordering:
rho/kappa remains the dominant mismatch family.

## Classification

Phase 2 classification:

- `infection_vs_recovery_contrast`: supported as the dominant pattern.
- `common_rate_direction`: secondary contributor, not clean enough to ignore.
- `both`: supported in the weak sense that tau also has visible gaps, but rho
  is clearly larger.
- `neither`: not supported.
- `inconclusive_due_to_mcse_or_runtime`: not the main classification; runtime
  was high, but the artifact completed and chain-rule checks passed.

## Skeptical Audit

- Wrong baseline: avoided by preserving Phase 1 seed microbatch size `1`,
  theta, seeds, chunks, transport policy, and budget.
- Proxy metrics: FD gaps classify root-cause direction only; they are not
  promoted to HMC readiness or correctness.
- Missing stop conditions: none triggered; chain-rule passed and no route veto
  fired.
- Unfair comparison: all regional families used the same fixed-route contexts.
- Hidden assumption: rho/tau are diagnostic linear coordinates only, not
  Fisher-orthogonal coordinates.
- Environment mismatch: material route was GPU/TF32; no XLA claim is made.
- Artifact mismatch: JSON records compiler status as not explicitly captured.

## Phase 3 Handoff

Advance to Phase 3 with this target:

- Audit `_sir_rhs_vjp_tf` and `_sir_transition_mean_vjp_tf` directly.
- Compare manual RK4 VJP against TensorFlow autodiff on fixed tiny tensors.
- Report state, kappa, and nu VJP residuals, including regional kappa/nu
  chain-rule residuals.
- Keep this as a transition-only audit; do not claim full filter correctness
  even if it passes.

## Nonclaims

- No SIR gradient correctness claim.
- No HMC readiness claim.
- No posterior correctness claim.
- No Fisher-orthogonal parameterization claim.
- No production regional parameterization.
