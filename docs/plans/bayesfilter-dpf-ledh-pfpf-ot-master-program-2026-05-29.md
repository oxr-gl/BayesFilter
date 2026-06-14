# TF/TFP LEDH-PF-PF-OT Master Program

Date: 2026-05-29

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Lane Boundary

This is the BayesFilter-owned differentiable particle filter
implementation/evidence lane only.  Do not use or edit the high-dimensional
nonlinear filtering lane, production `bayesfilter/` code, vendored student code,
or monograph chapters.  Implementation remains experimental under
`experiments/dpf_implementation/tf_tfp/`.

## Default Architecture Statement

The default experimental DPF architecture for large nonlinear models is now
TF/TFP LEDH-PF-PF with finite Sinkhorn/entropic OT as the default
differentiable resampling component:

- local EDH/LEDH particle-flow proposal;
- per-particle local linearization/Jacobian contract;
- invertible affine flow map or structured blocker;
- forward log-determinant accounting;
- proposal-to-target PF-PF corrected weights;
- finite-budget entropic OT/Sinkhorn relaxed resampling;
- `tf.GradientTape` compatible named scalar proxy.

The existing TF/TFP OT-DPF with a bootstrap proposal remains a comparator and
component baseline.  It is not the default architecture for large nonlinear
models.

## Backend Contract

BayesFilter algorithmic implementation defaults to TensorFlow / TensorFlow
Probability.  NumPy is forbidden as an implementation backend in this lane.  It
is allowed only for reference/comparison fixtures, closed-form sanity checks,
serialization/reporting, and reviewed exceptions.  Differentiable or
gradient-bearing paths must use TF/TFP.

## Phase Order

| Phase | Plan | Main output |
| --- | --- | --- |
| P0 | `bayesfilter-dpf-ledh-pfpf-ot-p0-scope-default-architecture-plan-2026-05-29.md` | default architecture and import gate |
| P1 | `bayesfilter-dpf-ledh-pfpf-ot-p1-ledh-math-contract-plan-2026-05-29.md` | LEDH/PF-PF math contract |
| P2 | `bayesfilter-dpf-ledh-pfpf-ot-p2-affine-lgssm-edh-parity-plan-2026-05-29.md` | affine LGSSM EDH parity gate |
| P3 | `bayesfilter-dpf-ledh-pfpf-ot-p3-nonlinear-local-linearization-plan-2026-05-29.md` | range-bearing local-linearization gate |
| P4 | `bayesfilter-dpf-ledh-pfpf-ot-p4-pfpf-correction-logdet-plan-2026-05-29.md` | PF-PF correction/log-det gate |
| P5 | `bayesfilter-dpf-ledh-pfpf-ot-p5-tf-tfp-ledh-flow-implementation-plan-2026-05-29.md` | TF/TFP LEDH flow implementation |
| P6 | `bayesfilter-dpf-ledh-pfpf-ot-p6-integrated-ledh-pfpf-ot-runner-plan-2026-05-29.md` | integrated LEDH-PF-PF-OT filter/runners |
| P7 | `bayesfilter-dpf-ledh-pfpf-ot-p7-gradient-tape-contract-plan-2026-05-29.md` | same-scalar GradientTape gate |
| P8 | `bayesfilter-dpf-ledh-pfpf-ot-p8-lgssm-validation-plan-2026-05-29.md` | LGSSM validation result |
| P9 | `bayesfilter-dpf-ledh-pfpf-ot-p9-range-bearing-validation-plan-2026-05-29.md` | range-bearing validation result |
| P10 | `bayesfilter-dpf-ledh-pfpf-ot-p10-final-audit-handoff-plan-2026-05-29.md` | final audit and handoff |

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-*-2026-05-29.md`
- `experiments/dpf_implementation/tf_tfp/flows/`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_gradient_checks_tf.py`
- `experiments/dpf_implementation/reports/dpf-ledh-pfpf-ot-tf-tfp-*-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_ot_tf_tfp_*.json`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `docs/references.bib`
- high-dimensional nonlinear filtering plans, reports, chapters, or sources;
- vendored student code;
- existing NumPy prototype modules except read-only comparison;
- production API files.

## Evidence Ledgers

Keep separate ledgers for engineering correctness, mathematical contract,
linear-Gaussian parity, nonlinear proxy diagnostics, PF-PF density correction,
OT resampling component validity, GradientTape same-scalar validity, and
production readiness.  Do not promote proxy RMSE, finite gradients, UKF
agreement, or smoke tests into posterior, HMC, production, NAWM-scale, banking,
model-risk, or monograph claims.

## Stop Rules

Stop or write a structured blocker if TF/TFP is unavailable, CPU-only import
discipline cannot be enforced, algorithmic implementation needs NumPy,
pre-flow proposal density cannot be evaluated, the flow map lacks an invertible
Jacobian/log-det contract, corrected weights cannot be formed, Sinkhorn emits
invalid residuals, value and gradient target different scalars, JSON outputs are
malformed, or any forbidden write set would need edits.

## Skeptical Audit Checklist

Before each phase, record checks for stale context, wrong default architecture,
bootstrap-proposal overclaim, OT-resampling overclaim, missing stop conditions,
hidden production drift, monograph drift, vendored-code contamination,
high-dimensional-lane contamination, and artifact fitness.

## Review Protocol

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

If unavailable, stop and report a blocker.  Claude reviews read-only and returns
`ACCEPT` or `REJECT` with findings.  Codex audits Claude's findings, patches
agreed blockers, and loops up to five iterations.  On iteration 5, accept only
for user inspection unless a major blocker remains.  Unresolved objections are
risks, not validation.

## Implementation Acceptance Gates

- P1-P4 specify the LEDH/PF-PF density, map, Jacobian, and correction contract.
- P5-P6 implement only TF/TFP code under the allowed write set.
- P8 passes LGSSM finite/parity smoke against Kalman and comparator rows.
- P9 passes range-bearing finite/proxy smoke against UKF and comparator rows.
- P7 passes a same-scalar GradientTape/finite-difference check.
- NumPy import and student/vendored/highdim import gates pass.

## Final Acceptance Criteria

P10 can pass only if P0-P9 have accepted or structured-blocker results, the
default architecture statement is updated in lane artifacts, all required
verification commands pass or have structured blockers, and caveats remain
explicit.

## Initial Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| stale context | pass | Read `AGENTS.md`, `CLAUDE.md`, DPF3 PF-PF spec, and current TF/TFP OT-DPF handoff. |
| wrong default architecture | pass | This program corrects bootstrap OT-DPF overreach and makes LEDH-PF-PF-OT the default experimental target. |
| bootstrap-proposal overclaim | pass | Existing bootstrap OT-DPF remains comparator/component only. |
| OT-resampling overclaim | pass | OT is resampling component, not proposal correction or categorical PF equivalence. |
| missing stop conditions | pass | Stop rules require proposal density, invertible map, log-det, corrected weights, and same-scalar gradient. |
| hidden production drift | pass | Production `bayesfilter/` remains forbidden. |
| monograph drift | pass | Monograph edits are forbidden; use patch/result registers only. |
| vendored-code contamination | pass | Student/vendored work remains comparison-only and unused. |
| high-dimensional-lane contamination | pass | Separate high-dimensional lane is not authority for this lane. |
| artifact fitness | pass | P0-P10 answer the close question: build and test the default experimental LEDH-PF-PF-OT DPF. |

## Review Record

- Iteration 1: pending.
