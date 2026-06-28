# P02 Result: Threshold Principle And Freeze

Date: 2026-06-24

Status: `P2_FREEZE_PASS_TO_P3`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Freeze `tau_component = 0.03` nats per observed component for bounded value-route actual-SIR Nystrom validation at `T=20,M=9`. |
| Primary criterion status | `PASS`: P1 descriptive scales were available, P2 local checks passed, and Claude read-only review converged on round 2. |
| Veto diagnostic status | `PASS`: no post-hoc validation outcome use, no multiple-threshold shopping, no default/HMC/posterior claim, no missing disjoint-seed rule. |
| Main uncertainty | The frozen threshold is a practical value-route margin, not a theorem and not HMC/posterior-safe. |
| Next justified action | Run P3 statistical validation on disjoint seeds using the frozen threshold and exact Clopper-Pearson rule. |
| What is not being concluded | No validation pass/fail yet, no default readiness, no posterior correctness, no HMC readiness, no statistical superiority. |

## Frozen Threshold

| Quantity | Value |
| --- | ---: |
| `tau_component` | `0.03` nats per observed component |
| `T` | `20` |
| `M` | `9` |
| `tau_total = T * M * tau_component` | `5.4` total log-likelihood units |

Scope:

- bounded value-route validation only;
- same actual-SIR shape `T=20,M=9,D=18`;
- fixed Nystrom policy `rank=32,epsilon=0.5,kernel_mode=raw,scaling_normalization=none,core_solver=cholesky`;
- not HMC/posterior validation.

## Rationale

`tau_component=0.03` is a practical equivalence margin for bounded value-route
validation.  It is:

- slightly above the legacy `5.0` equivalent `0.027777777777777776`;
- above P1 descriptive q90 `0.025054897732204866`;
- near P1 descriptive q95 `0.0314671156141493`;
- below the old max-threshold equivalent `0.05555555555555555`.

The acceptable exceedance probability for P3 is frozen at `0.20` for bounded
value-route usability: at least 80% of valid same-shape validation seeds should
fall within the practical per-component margin.  This is intentionally weaker
than any default-production, HMC, posterior, or broad robustness criterion.

## P3 Statistical Rule

P3 must:

1. apply deterministic validity vetoes first;
2. use validation seeds disjoint from P1 seeds;
3. compute `abs(delta)/(T*M)` for each deterministic-valid validation seed;
4. count exceedances of `tau_component`;
5. use `n_valid` as the denominator after deterministic validity checks;
6. compute the exact one-sided 95% Clopper-Pearson upper confidence bound for
   the exceedance probability;
7. accept bounded value-route validation only if the upper bound is `<= 0.20`;
8. classify as inconclusive if deterministic checks pass but the confidence
   bound is above `0.20`;
9. reject only if deterministic validity fails or a predeclared statistical
   rejection rule fires.

Deterministic-invalid rows must not be silently counted as stochastic
non-exceedances.

## Legacy-Fail Calibration Rule

Seed `82921` was admissible in P1 descriptive calibration because it failed only
the legacy paired threshold being recalibrated.  Legacy threshold failures are
admissible calibration evidence when deterministic validity passed.

Rows with deterministic invalidity remain inadmissible for calibration or
validation.

## Local Checks

P2 local checks passed:

- P1 JSON parsed and had `status=PASS`;
- P1 unique seed count was `12`;
- `tau_component=0.03` and `tau_total=5.4` were present;
- disjoint validation rule was explicit;
- required nonclaims were present.

## Claude Review

Claude read-only review ledger:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-claude-review-ledger-2026-06-24.md`

Review rounds:

- P2-R1: `VERDICT: REVISE`.
- P2-R2: `VERDICT: AGREE`.

## Handoff

Proceed to:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-threshold-calibration-p03-statistical-validation-subplan-2026-06-24.md`

P3 may run GPU validation only after local checks verify disjoint seeds,
artifact paths, trusted GPU selection, deterministic validity checks, and the
frozen threshold rule.
