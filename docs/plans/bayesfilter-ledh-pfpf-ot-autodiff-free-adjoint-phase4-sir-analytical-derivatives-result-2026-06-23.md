# Phase 4 Result: SIR Analytical Derivatives

date: 2026-06-23
phase: P4-SIR-ANALYTICAL-DERIVATIVES
decision: PASSED

## Phase Objective And Question

Objective: wire analytical SIR parameter derivatives into the no-autodiff route
contract and prove the production path does not ask TensorFlow to differentiate
SIR callbacks.

Question: does SIR parameter sensitivity enter the LEDH gradient route
analytically?

## Inherited Entry Conditions

- P3 derivation contract passed bounded review.
- P4 subplan passed bounded review after one repair loop.
- P4 inherited the no-production-autodiff invariant, theta order, model
  callback adjoint interface, and no-Zhao-Cui-comparator boundary.
- P4 authorized analytical SIR derivative wiring and focused tests only.
- Transport repair, filter-level route certification, GPU rungs, FD,
  actual-gradient validation, HMC checks, and posterior checks remained
  forbidden.

## Evidence Produced

- Implementation diff:
  `bayesfilter/highdim/models.py`
- Focused tests:
  `tests/highdim/test_p81_analytical_sir_score.py`
- P4 current-route audit artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-current-route-audit-result-2026-06-23.json`
- Refreshed P5 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase5-ledh-flow-logweight-adjoints-subplan-2026-06-23.md`
- This P4 result artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-result-2026-06-23.md`

## Local Commands Actually Run

```text
rg -n 'parameterized_zhao_cui_sir_austria_model|class .*SIR|def transition_mean|def transition_log_density|def observation_log_density|parameter_order|manifest_payload|scaled_model' bayesfilter/highdim/models.py bayesfilter/highdim/*.py

rg -n 'def multistate_nonlinear_fixed_design_tt_score_path|def scalar_nonlinear_fixed_design_tt_score_path|FixedBranchDerivativeConfig|analytic_gradient|score_path|transition_adjacent|initial_adjacent' bayesfilter/highdim/derivatives.py bayesfilter/highdim/filtering.py bayesfilter/highdim/transition_route.py

sed -n '1,230p' tests/highdim/test_p81_analytical_sir_score.py

sed -n '320,790p' bayesfilter/highdim/models.py

sed -n '2360,2615p' bayesfilter/highdim/filtering.py

sed -n '1040,1708p' bayesfilter/highdim/filtering.py

python -m py_compile bayesfilter/highdim/models.py

python -m pytest tests/highdim/test_p81_analytical_sir_score.py -q

python scripts/audit_ledh_no_autodiff.py --manifest docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase2-current-route-manifest-2026-06-23.json --whitelist docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-audit-whitelist-2026-06-23.json --output /tmp/p4-current-route-audit-result.json --expect-decision FAIL_CURRENT_ROUTE

rg -n 'GradientTape|ForwardAccumulator|tape\.gradient|tape\.jacobian|tf\.gradients' bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py

git diff --check -- bayesfilter/highdim/models.py tests/highdim/test_p81_analytical_sir_score.py docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-claude-review-ledger-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-execution-ledger-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-visible-stop-handoff-2026-06-23.md

cp /tmp/p4-current-route-audit-result.json docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-current-route-audit-result-2026-06-23.json
```

No production-route transport repair, filter-level route certification, GPU,
FD, actual-gradient, HMC, or posterior command was run.

## Implemented Analytical SIR Surface

`ParameterizedZhaoCuiSIRSSM` now exposes:

- `scaled_parameter_derivatives(theta)`;
- `transition_mean_parameter_jacobian(theta, x_prev)`;
- `transition_log_density_parameter_score(theta, x_prev, x_next, t)`;
- `observation_log_density_parameter_score(theta, x_t, y_t, t)`;
- `infectious_components_vjp(cotangent)`.

The theta order is preserved as:

```text
(log_kappa_scale, log_nu_scale, log_obs_noise_scale)
```

The scaling derivatives are:

```text
d kappa / d theta[0] = kappa
d nu / d theta[1] = nu
d R / d theta[2] = 2 R
```

The transition mean Jacobian propagates analytical sensitivities through the
same RK4 variant as the forward model.  The transition log-density score uses
the Gaussian residual formula with process covariance fixed.  The observation
log-density score accounts for the observation covariance scaling.  The
infectious-component VJP scatter-adds observation cotangents into the infectious
state coordinates.

## Skeptical Plan Audit Outcome

Passed.

- Wrong baseline check: P4 did not use Zhao-Cui as LEDH comparator.  The
  existing highdim fixed-branch TT derivative lane was inspected and found to
  still use `tensorflow_forward_accumulator_for_model_log_density`, so it was
  not treated as a production LEDH derivative mechanism.
- Proxy metric check: diagnostic autodiff comparisons in tests explain local
  formula correctness only; they do not certify the production route.
- Stop-condition check: theta order, RK4/RHS sensitivity, observation gather,
  and observation covariance parameter adjoints are implemented and tested.
- Environment check: local CPU-style tests only; no GPU or route execution was
  needed.
- Artifact-answer check: artifacts directly answer whether SIR parameter
  sensitivity can be supplied analytically to later LEDH adjoint phases.

## Evidence Contract Outcome

Primary criterion passed for P4 scope.

- Production model code touched in P4 has no `GradientTape`,
  `ForwardAccumulator`, tape `.gradient`, tape `.jacobian`, or `tf.gradients`
  hits.
- Focused tests passed: `7 passed`.
- The only static forbidden-autodiff hits in P4-touched files are in
  `tests/highdim/test_p81_analytical_sir_score.py`, where they are
  diagnostic-only comparisons.
- P2 audit rerun still returns `FAIL_CURRENT_ROUTE`, as expected, because P4
  does not close the outer objective tape or transport grad-body leaks.

## Veto Diagnostics Status

- Production SIR autodiff callback: PASS for P4-touched model code.
- Diagnostic parity treated as proof: PASS; result limits diagnostic autodiff
  to local formula checks.
- Missing theta-order contract: PASS.
- Missing observation covariance adjoint: PASS.
- Source-faithfulness claims without anchors: PASS; P4 makes no
  source-faithfulness claim.
- GPU/FD/actual-gradient launched: PASS; none launched.
- Transport repair in P4: PASS; none performed.

## Decision Table

| Field | Status |
|---|---|
| Decision | `PASSED` |
| Primary criterion | Passed for analytical SIR derivative surface. |
| Veto diagnostics | No P4 veto fired. |
| Main uncertainty | The full filter route still lacks manual LEDH/log-weight/transport/filter-level composition. |
| Next justified action | Review P4 result and refreshed P5 subplan; execute P5 only after review. |
| What is not concluded | No full filter gradient correctness, no no-autodiff certification, no GPU feasibility, no FD agreement, no HMC readiness, and no scientific validity claim. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `8eca1559c9508527a8d61d4ca348d8cee632db42` |
| Commands | Exact local commands recorded above. |
| Environment | Local shell in `/home/chakwong/BayesFilter`; TensorFlow tests under existing local environment. |
| CPU/GPU status | GPU not used; no CUDA route command ran. |
| Data version | N/A. |
| Seeds | N/A; no stochastic experiment run. |
| Wall time | Focused pytest reported `7 passed` in about 66 seconds. |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-phase4-sir-analytical-derivatives-result-2026-06-23.md` |

## Unresolved Blockers Or Leaks Carried Forward

- No production no-autodiff LEDH-PFPF-OT route has been implemented.
- Current reviewed route still fails P2 audit with `FAIL_CURRENT_ROUTE`.
- P1-L001/P1-L003 remain open until P7 implements a manual objective score
  route and P8 audits it.
- P1-L013/P1-L015 remain open until P6 repairs/audits transport grad bodies.
- P5 LEDH flow/log-density/log-weight adjoints are not implemented yet.
- No valid N10000 actual-gradient artifact exists.
- FD remains prohibited.

## What Is Not Concluded

P4 does not conclude full filter gradient correctness, no-autodiff
certification, GPU feasibility, N10000 feasibility, FD agreement, posterior
correctness, HMC readiness, production readiness, default-policy promotion,
Zhao-Cui source-faithfulness, or scientific superiority.

## Exact Next Gate And Handoff Conditions

Next gate: P4 result bounded review and refreshed P5 subplan bounded review.

P5 may start only after:

- this P4 result passes bounded review;
- the refreshed P5 subplan passes bounded review;
- P5 preserves the P4 analytical SIR interface and no-production-autodiff
  boundary.

Transport repair, filter-level route certification, GPU rungs, FD validation,
actual-gradient runs, HMC checks, and posterior checks remain forbidden until
later reviewed phases authorize them.
