# DPF5 Validation Harness Result

## Decision

`DPF5_HARNESS_READY`

DPF6 may start: yes

## Scope

DPF5 specified the validation harness, benchmark ladder, seed/uncertainty
policy, and CPU/GPU runtime policy.  It did not implement benchmark scripts,
run broad experiments, edit production `bayesfilter/`, edit monograph chapters,
use the high-dimensional lane, or edit/execute vendored student code.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-dpf5-validation-harness-spec-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf5-benchmark-ladder-matrix-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf5-seed-uncertainty-policy-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf5-cpu-gpu-runtime-policy-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf5-result-2026-05-28.md`

## Result Summary

| Area | Decision |
| --- | --- |
| Validation ladder | specified from import boundary through runtime envelope |
| Veto ordering | correctness/numerical/gradient vetoes before proxy or speed ranking |
| Student comparison | qualitative/explanatory only |
| Seed/uncertainty | required for stochastic promotion; one-seed is smoke-only |
| CPU/GPU policy | CPU-first; trusted/escalated GPU commands required |
| Future scripts | not authorized in DPF5 result |
| Production/default movement | blocked until DPF6 and separate patch plan |

## Skeptical Result Audit

- Stale context: DPF4 was Claude-accepted and records `DPF5 may start: yes`.
- Wrong baseline: independent references and DPF1-DPF4 contracts precede proxy
  and student comparison rows.
- Proxy overclaim: proxy RMSE, ESS, runtime, finite gradients, and student
  agreement cannot promote correctness, posterior validity, HMC validity, or
  production readiness.
- Stop conditions: failed veto diagnostics block ranking and downstream
  promotion.
- Hidden production/monograph drift: no production or monograph file was edited.
- Vendored-code contamination: no student code was copied, imported, executed,
  or edited.
- High-dimensional-lane contamination: no separate high-dimensional nonlinear
  filtering lane file was used.
- Artifact fitness: the harness, ladder, seed policy, and runtime policy answer
  the DPF5 validation question.

## Review Record

- Claude reviewer command: `claude -p --model claude-opus-4-7 --effort max`
- Iteration 1: `ACCEPT`
- Claude findings: DPF5 anchors to accepted DPF4 and DPF1-DPF4 references,
  enforces veto-before-ranking discipline, defines seed/uncertainty and
  CPU/GPU trusted-permission policies, excludes student agreement from
  promotion, and blocks HMC/posterior/production/default claims.
- Codex audit: accepted Claude's findings and applied only the authorized
  metadata update.
- Final review status: accepted for DPF6 start.

## Verification Summary

- `rg -n "benchmark-ladder-matrix|seed-uncertainty-policy|cpu-gpu-runtime-policy|veto|seed|runtime|CPU|GPU|proxy|not concluded|promotion|student|production|high-dimensional|HMC|posterior" docs/plans/bayesfilter-dpf-implementation-dpf5-*.md`: passed.
- `git diff --check`: passed.
- `py_compile`: not run because no Python files were touched.

## Run Manifest

- command family: document reads and `rg`/`sed` searches only.
- commit: `0477f56c9e76462de2d5acb167f5bf9d1b65de42`.
- CPU/GPU status: N/A; no experiment or GPU command was run.
- random seeds: N/A.
- touched Python files: none.

## What Is Not Concluded

DPF5 does not make a production/default decision, validate HMC/posterior
inference, validate high-dimensional readiness, or rank candidate methods.
