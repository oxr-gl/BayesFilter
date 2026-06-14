# DPF Nonlinear-SSM Evidence Ladder Master Program

Date: 2026-05-29

## Decision

`ACCEPTED_BY_CLAUDE_REVIEW_ITERATION_1`

## Lane Boundary

This is the BayesFilter-owned DPF implementation/evidence lane only.  Do not
use or edit the high-dimensional nonlinear filtering lane, production
`bayesfilter/` code, vendored student code, or monograph chapters.  Do not
implement or test NAWM/DSGE-specific models here.  NAWM/DSGE validation belongs
to the DSGE repo.  Implementation remains experimental under
`experiments/dpf_implementation/tf_tfp/`.

## Backend Policy

BayesFilter algorithmic implementation defaults to TensorFlow / TensorFlow
Probability.  NumPy is not allowed as an implementation backend.  NumPy may
appear only as reference/comparison/reporting by reviewed exception; this ladder
targets TF/TFP-only differentiable code.

## Goal

Build a bounded evidence ladder for the TF/TFP LEDH-PF-PF-OT DPF across general
nonlinear SSM models, emphasizing differentiable parameter-estimation evidence
instead of only filtered-state RMSE.

## Model Ladder

| Rung | Model | Comparator | Main question |
| --- | --- | --- | --- |
| P1 | LGSSM multiseed | exact Kalman plus existing comparators | Does the LEDH-PF-PF-OT regression remain stable across seeds? |
| P2 | Range-bearing stress | UKF approximate, bootstrap PF, bootstrap OT-DPF | Are nonlinear Jacobian/angle diagnostics finite under stress? |
| P3 | CUT4 component | TF/TFP differentiable CUT4 comparator | Can the repo expose a same-scalar deterministic differentiable comparator? |
| P4 | Stochastic volatility | TF/TFP CUT4 | Do value, gradient, and one-parameter MLE/SE diagnostics agree at smoke scale? |
| P5 | Structural AR(1) quadratic completion | TF/TFP structural CUT4 | Does the filter respect the exogenous/endogenous structural split from ch18b? |
| P6 | Particle-count/seed ladder | same fixtures | How much of the observed difference is DPF Monte Carlo variability? |

## Parameter-Estimation Equivalence Criteria

Do not set final universal thresholds by fiat.  Acceptance bands must be
calibrated from comparator self-consistency, DPF multi-seed variability,
particle-count convergence, and likelihood curvature.  This first pass uses
structured smoke/evidence artifacts and reports:

- same-scalar value differences;
- GradientTape gradients for DPF and comparator;
- comparator Hessian/observed-information standard error for selected scalar
  parameters;
- `z = |theta_DPF - theta_comparator| / SE_comparator` for one-parameter smoke
  MLEs where bounded optimization is feasible;
- an information-distance placeholder or value when multi-parameter Hessian is
  available.

Filtered-state RMSE is diagnostic only.

## Evidence Ledgers

Keep separate ledgers for implementation correctness, differentiable scalar
validity, parameter-estimation evidence, comparator limitations, Monte Carlo
variability, structural residuals, and production readiness.  Do not promote
value-only evidence into gradient or estimation evidence.

## Phase Order

| Phase | Plan | Main output |
| --- | --- | --- |
| P0 | `bayesfilter-dpf-nonlinear-ssm-evidence-p0-scope-and-estimation-criteria-plan-2026-05-29.md` | scope and estimation criteria |
| P1 | `bayesfilter-dpf-nonlinear-ssm-evidence-p1-lgssm-multiseed-regression-plan-2026-05-29.md` | LGSSM multiseed regression |
| P2 | `bayesfilter-dpf-nonlinear-ssm-evidence-p2-range-bearing-stress-plan-2026-05-29.md` | range-bearing stress |
| P3 | `bayesfilter-dpf-nonlinear-ssm-evidence-p3-cut4-differentiable-comparator-plan-2026-05-29.md` | TF/TFP CUT4 component |
| P4 | `bayesfilter-dpf-nonlinear-ssm-evidence-p4-stochastic-volatility-gradient-mle-plan-2026-05-29.md` | SV gradient/MLE smoke |
| P5 | `bayesfilter-dpf-nonlinear-ssm-evidence-p5-structural-ar1-quadratic-completion-plan-2026-05-29.md` | structural split gradient/MLE smoke |
| P6 | `bayesfilter-dpf-nonlinear-ssm-evidence-p6-particle-count-seed-ladder-plan-2026-05-29.md` | particle-count/seed calibration |
| P7 | `bayesfilter-dpf-nonlinear-ssm-evidence-p7-final-audit-handoff-plan-2026-05-29.md` | final audit/handoff |

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-nonlinear-ssm-evidence-*-2026-05-29.md`
- `experiments/dpf_implementation/tf_tfp/cubature/`
- `experiments/dpf_implementation/tf_tfp/fixtures/stochastic_volatility_tf.py`
- `experiments/dpf_implementation/tf_tfp/fixtures/structural_ar1_quadratic_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/cut4_sv_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/cut4_structural_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_multiseed_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_stress_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_sv_cut4_ledh_gradient_mle_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_structural_ar1_cut4_ledh_gradient_mle_tf.py`
- `experiments/dpf_implementation/reports/dpf-nonlinear-ssm-*-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_nonlinear_ssm_*.json`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `docs/references.bib`
- high-dimensional nonlinear filtering lane artifacts;
- vendored student code;
- DSGE/NAWM model implementations;
- production API files.

## Stop Rules

Stop or write a structured blocker if TF/TFP is unavailable, CPU-only import
discipline cannot be enforced, implementation needs NumPy, CUT4 cannot expose a
same-scalar differentiable value/gradient, DPF and comparator do not target the
same scalar, bounded MLE/Hessian diagnostics are numerically invalid, structural
deterministic residuals are not recorded, or forbidden write sets would need
edits.

## Skeptical Audit Checklist

Before each phase, check stale context, wrong comparator, value-only evidence
overclaimed as gradient evidence, arbitrary thresholds without calibration,
missing stop conditions, hidden production drift, monograph drift, vendored-code
contamination, high-dimensional-lane contamination, DSGE/NAWM drift, and
whether artifacts answer the estimation/gradient question.

## Review Loop

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

If unavailable, stop and report a blocker.  Claude reviews read-only and returns
`ACCEPT` or `REJECT` with findings.  Codex audits findings, patches agreed
blockers, and loops up to five iterations.  On iteration 5, accept only for user
inspection unless a major blocker remains.  Unresolved objections are risks, not
validation.

## Final Acceptance Criteria

P7 can pass only if P0-P6 have accepted or structured-blocker results, required
verification passes or blockers are recorded, no production/vendored/monograph/
high-dimensional/DSGE drift occurred, and caveats remain explicit.

## Initial Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| stale context | pass | Read AGENTS, CLAUDE, ch18b, LEDH-PF-PF-OT handoff, and current reports. |
| wrong comparator | pass | Kalman/UKF/CUT4 roles are separated; CUT4 is comparator, not ground truth. |
| value-only overclaim | pass | Estimation/gradient criteria are central. |
| arbitrary thresholds | pass | Final thresholds are calibration outputs, not fixed in advance. |
| missing stop conditions | pass | Stop rules cover CUT4, same-scalar, MLE/Hessian, structural residuals. |
| hidden production drift | pass | Production writes forbidden. |
| monograph drift | pass | ch18b read-only; no chapter edits. |
| vendored/highdim contamination | pass | Forbidden as authority or implementation source. |
| DSGE/NAWM drift | pass | Structural toy model only; no DSGE/NAWM implementation. |
| artifact fitness | pass | P0-P7 answer the nonlinear SSM estimation/gradient evidence question. |

## Review Record

- Iteration 1: `ACCEPT`.  Claude accepted the master/subplan bundle and noted
  one non-blocking weakness: the P0 grep check is weaker than later P7 checks.
  Codex audited the finding as useful but non-material because P7 contains the
  stronger import-boundary, NumPy, JSON, and git verification gates.
