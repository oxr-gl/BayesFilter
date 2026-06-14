# DPF4 Differentiable Objective And Gradient Result

## Decision

`DPF4_GRADIENT_CONTRACT_READY`

DPF5 may start: yes

## Scope

DPF4 classified DPF objectives and specified what gradients mean for each
scalar.  It did not implement code, run experiments, edit monograph chapters,
edit production `bayesfilter/`, use high-dimensional/HMC lanes as authority, or
edit/execute vendored student code.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-dpf4-objective-classification-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf4-gradient-contract-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf4-downstream-evidence-requirements-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf4-result-2026-05-28.md`

## Result Summary

| Area | Decision |
| --- | --- |
| Classical PF likelihood estimator | value-side estimator; not smooth HMC by default |
| Soft/EOT/Sinkhorn scalars | relaxed-target or solver-object gradients only |
| Learned/amortized scalars | learned-surrogate; deferred pending provenance |
| PF-PF corrected scalar | research candidate with proposal-correction interpretation |
| HMC/posterior claims | blocked pending separate evidence |
| Production/API movement | blocked until DPF6 and separate patch plan |

## Skeptical Result Audit

- Stale context: DPF3 was Claude-accepted and records `DPF4 may start: yes`.
- Wrong baseline: objective classes derive from DPF0-DPF3 and DPF monograph
  target analysis, not student HMC wording.
- Proxy overclaim: finite gradients, runtime, student same-regime rows, and
  learned residuals are explanatory until downstream gates pass.
- Stop conditions: ambiguous scalar, same-scalar mismatch, or unclassified target
  status blocks HMC/posterior wording.
- Hidden production/monograph drift: no production or monograph file was edited.
- Vendored-code contamination: no student code/notebook was used as authority.
- High-dimensional-lane contamination: no separate high-dimensional or external
  HMC lane file was used as authority.
- Artifact fitness: the objective ledger, gradient contract, and downstream
  requirements answer what the differentiated scalar and gradient mean.

## Review Record

- Claude reviewer command: `claude -p --model claude-opus-4-7 --effort max`
- Iteration 1: `ACCEPT`
- Claude findings: DPF4 anchors to accepted DPF3 rather than student/external
  lanes, states stop conditions, classifies candidate scalars, makes
  same-scalar gradient semantics explicit, separates stopped/reparameterized/
  relaxed/solver/learned paths, and blocks production/posterior/HMC overclaim.
- Codex audit: accepted Claude's findings and applied only the authorized
  metadata update.
- Final review status: accepted for DPF5 start.

## Verification Summary

- `rg -n "objective-classification-ledger|downstream-evidence-requirements|what it is not|proxy|surrogate|likelihood|posterior|HMC|not concluded|gradient|same-scalar|student|high-dimensional|production" docs/plans/bayesfilter-dpf-implementation-dpf4-*.md`: passed.
- `git diff --check`: passed.
- `py_compile`: not run because no Python files were touched.

## Run Manifest

- command family: document reads and `rg`/`sed` searches only.
- commit: `0477f56c9e76462de2d5acb167f5bf9d1b65de42`.
- CPU/GPU status: N/A; no experiment or GPU command was run.
- random seeds: N/A.
- touched Python files: none.

## What Is Not Concluded

DPF4 does not validate posterior inference, HMC convergence, scientific
validity, production optimization, production API readiness, banking use, or
model-risk use.
