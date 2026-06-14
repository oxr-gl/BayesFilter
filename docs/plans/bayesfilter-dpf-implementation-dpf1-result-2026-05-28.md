# DPF1 Classical PF Baseline Result

## Decision

`DPF1_CLASSICAL_BASELINE_READY`

DPF2 may start: yes

## Scope

DPF1 specified the BayesFilter-owned classical bootstrap/SIR PF baseline needed
before differentiable DPF components can be evaluated.  No code was implemented,
no experiments were run, and no production, monograph, vendored student, or
high-dimensional lane files were edited.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-spec-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf1-reference-test-contract-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf1-student-comparison-context-register-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf1-result-2026-05-28.md`

## Result Summary

| Requirement | Status |
| --- | --- |
| Classical bootstrap/SIR algorithm contract | specified |
| Likelihood/log-likelihood/score separation | specified |
| ESS/resampling/seed/dtype/device artifact fields | specified |
| LGSSM analytic reference test contract | specified |
| Nonlinear range-bearing proxy scope | comparison-only/proxy-only |
| Student comparison context | registered, not acceptance evidence |
| Production movement | blocked until DPF6 and separate patch plan |

## Skeptical Result Audit

- Stale context: DPF0 was Claude-accepted and records `DPF1 may start: yes`.
- Wrong baseline: DPF1 uses classical PF plus analytic/Kalman reference, not
  student output.
- Proxy overclaim: controlled/student RMSE, ESS, runtime, and same-regime rows
  are not acceptance evidence.
- Stop conditions: ambiguous likelihood semantics, no independent reference, or
  student acceptance evidence would block implementation movement.
- Hidden production/monograph drift: no production or monograph file was edited.
- Vendored-code contamination: no student code was copied, imported, executed,
  or edited.
- High-dimensional-lane contamination: no separate high-dimensional nonlinear
  filtering lane file was used.
- Artifact fitness: the spec and reference contract answer what classical
  baseline must exist before DPF2-DPF5.

## Review Record

- Claude reviewer command: `claude -p --model claude-opus-4-7 --effort max`
- Iteration 1: `REJECT`
- Claude blocking finding: the result claimed `DPF1_CLASSICAL_BASELINE_READY`
  and `DPF2 may start: yes` while this review and verification section still
  said pending, making the artifact internally inconsistent under the phase
  review loop.
- Claude non-blocking checks passed: classical bootstrap/SIR PF is the baseline,
  likelihood/log-likelihood/score semantics are explicit enough, student and
  controlled rows are excluded from acceptance evidence, and production/HMC/
  posterior/vendored/high-dimensional contamination is blocked.
- Codex audit: agreed with the rejection.  The issue is a metadata/review-loop
  consistency defect, not a conceptual defect in the DPF1 specification.
- Patch after iteration 1: filled review record and verification summary before
  resubmission.
- Iteration 2: `ACCEPT`
- Claude iteration-2 finding: previous blocking issue is fixed; no remaining
  blocker for DPF2 start.
- Codex iteration-2 audit: accepted Claude's decision; no further patch needed.
- Final review status: accepted for DPF2 start.

## Verification Summary

- `rg -n "reference-test-contract|comparison-only|not acceptance evidence|student|vendor|production|HMC|not concluded|not validate|Likelihood|log likelihood|ESS|Kalman" docs/plans/bayesfilter-dpf-implementation-dpf1-*.md`: passed.
- `git diff --check`: passed.
- `py_compile`: not run because no Python files were touched.

## Run Manifest

- command family: document reads and `rg`/`sed` searches only.
- commit: `0477f56c9e76462de2d5acb167f5bf9d1b65de42`.
- CPU/GPU status: N/A; no experiment or GPU command was run.
- random seeds: N/A.
- touched Python files: none.

## What Is Not Concluded

DPF1 does not validate differentiable resampling, PF-PF, learned OT, HMC,
posterior inference, production readiness, or banking/model-risk use.
