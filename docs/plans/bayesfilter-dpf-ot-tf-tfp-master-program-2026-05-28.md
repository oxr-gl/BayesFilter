# TF/TFP OT-DPF Master Program

Date: 2026-05-28

## Decision

`DRAFT_FOR_CLAUDE_REVIEW`

## Lane Boundary

This is the BayesFilter-owned DPF implementation/evidence lane only.  Do not use
or edit the high-dimensional nonlinear filtering lane, production
`bayesfilter/` code, vendored student code, or monograph chapters.  Implementation
is experimental and limited to `experiments/dpf_implementation/tf_tfp/`.

## Backend Contract

BayesFilter's default algorithmic backend is TensorFlow / TensorFlow
Probability.  NumPy is forbidden as an implementation backend in this lane.  It
is allowed only for reference/comparison fixtures, closed-form sanity checks,
serialization/reporting, or reviewed exceptions.  This program uses no NumPy
imports under `experiments/dpf_implementation/tf_tfp/`.

## Goal

Build the actual experimental TF/TFP finite-Sinkhorn relaxed OT-DPF path for:

1. LGSSM with TF/TFP Kalman reference.
2. Gaussian range-bearing model with TF/TFP UKF approximate reference.
3. Same-scalar `tf.GradientTape` gradient check with a finite-difference
   reference.

Implemented variant target:

`bootstrap proposal + stable log weights + finite-budget entropic OT/Sinkhorn
barycentric relaxed resampling + equal post-resampling weights`, implemented in
TF/TFP.

This is relaxed finite-budget OT resampling, not categorical PF equivalence and
not exact unregularized OT.

## Phase Order

Only the filenames in this table are authoritative for this TF/TFP lane.  Any
older or reviewer-cached names such as `p1-problem-setup` or
`p2-classical-sis-bootstrap-baseline` are not part of this program.

| Phase | Plan | Main output |
| --- | --- | --- |
| P0 | `bayesfilter-dpf-ot-tf-tfp-p0-scope-import-gate-plan-2026-05-28.md` | scope/import gate |
| P1 | `bayesfilter-dpf-ot-tf-tfp-p1-lgssm-fixture-kalman-plan-2026-05-28.md` | LGSSM fixture and Kalman reference |
| P2 | `bayesfilter-dpf-ot-tf-tfp-p2-range-bearing-ukf-plan-2026-05-28.md` | range-bearing fixture and UKF reference |
| P3 | `bayesfilter-dpf-ot-tf-tfp-p3-sinkhorn-resampler-plan-2026-05-28.md` | TensorFlow Sinkhorn resampler |
| P4 | `bayesfilter-dpf-ot-tf-tfp-p4-integrated-dpf-runner-plan-2026-05-28.md` | TF bootstrap PF and OT-DPF runners |
| P5 | `bayesfilter-dpf-ot-tf-tfp-p5-gradient-tape-contract-plan-2026-05-28.md` | same-scalar gradient contract |
| P6 | `bayesfilter-dpf-ot-tf-tfp-p6-lgssm-validation-plan-2026-05-28.md` | LGSSM validation result |
| P7 | `bayesfilter-dpf-ot-tf-tfp-p7-range-bearing-validation-plan-2026-05-28.md` | range-bearing validation result |
| P8 | `bayesfilter-dpf-ot-tf-tfp-p8-final-audit-handoff-plan-2026-05-28.md` | final audit/handoff |

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-ot-tf-tfp-*-2026-05-28.md`
- `experiments/dpf_implementation/README.md`
- `experiments/dpf_implementation/tf_tfp/`
- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-*-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_*.json`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `docs/references.bib`
- high-dimensional nonlinear filtering plans, reports, chapters, or sources;
- vendored student code;
- existing NumPy prototype modules outside `experiments/dpf_implementation/README.md`;
- production API files.

## Evidence Ledgers

Keep separate ledgers for engineering correctness, numerical validity,
reference/comparator evidence, relaxed-resampling component evidence, gradient
validity, proxy comparison, and production readiness.  Do not promote proxy
metrics, finite gradients, UKF agreement, or smoke evidence into production,
posterior, HMC, banking/model-risk, or monograph claims.

## Skeptical Audit Checklist

Before each phase, record checks for stale context, wrong backend, NumPy
implementation drift, proxy overclaim, missing stop conditions, hidden
production drift, monograph drift, vendored-code contamination,
high-dimensional-lane contamination, and artifact fitness.

## Stop Rules

Stop or write a structured blocker if TensorFlow/TFP is unavailable, CPU-only
import discipline cannot be enforced, any algorithmic implementation needs
NumPy, value and gradient target different scalars, Sinkhorn emits non-finite or
invalid marginal residuals, JSON outputs are malformed, or any forbidden write
set would need edits.

## Review Protocol

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

If unavailable, stop and report a blocker.  Claude must review read-only and
return `ACCEPT` or `REJECT` with findings.  Codex audits Claude's findings,
patches agreed blockers, and loops up to five iterations.  On iteration 5,
accept only for user inspection unless a major blocker remains.  A bundled plan
or result review is allowed only if Claude gives per-file or per-phase status.

## Final Acceptance Criteria

P8 can pass only if P0-P7 have accepted or structured-blocker results, the
NumPy import gate passes for `experiments/dpf_implementation/tf_tfp`, targeted
LGSSM/range-bearing/gradient runners pass or have structured blockers, scoped
diff checks pass, and caveats remain explicit.

## Review Record

- Iteration 1: `REJECT`.
- Claude finding: master allegedly had broken phase references; P0/P4/P6/P7
  needed stronger exact-artifact and verification contracts.
- Codex audit: the named broken phase references were not present in this file,
  likely stale reviewer context, but the ambiguity risk is worth removing.
  Agreed with P0/P4/P6/P7 auditability findings.
- Iteration 2: `REJECT`.
- Claude finding: master, P0-P5, P7, and P8 accepted; P6 still needed exact
  numeric LGSSM smoke caps instead of unnamed loose residual caps.
- Codex audit: agreed.
- Iteration 3: `ACCEPT`.
- Claude finding: P6 now has exact numeric smoke caps and no regression was
  found in the reviewed accepted files.
- Codex audit: agreed; implementation may proceed.
