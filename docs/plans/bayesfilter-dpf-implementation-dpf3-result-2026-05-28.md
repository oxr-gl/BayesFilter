# DPF3 Particle-Flow / PF-PF Result

## Decision

`DPF3_FLOW_PFPF_SPEC_READY`

DPF4 may start: yes

## Scope

DPF3 specified the particle-flow / PF-PF proposal-correction contract, deferred
or excluded unsupported flow families, and preserved student EDH/PFPF evidence
as comparison-only context.  It did not implement code, run experiments, edit
production `bayesfilter/`, edit monograph chapters, use the high-dimensional
lane, or edit/execute vendored student code.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-dpf3-flow-pfpf-spec-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf3-excluded-flow-risk-register-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf3-kernel-pff-exclusion-check-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-implementation-dpf3-result-2026-05-28.md`

## Result Summary

| Area | Decision |
| --- | --- |
| Proposal-corrected PF-PF | specified with target/proposal/Jacobian log-weight contract |
| Affine EDH/PF-PF parity | first-rung analytic/parity reference |
| LEDH/local flow | candidate only with per-particle Jacobian contract |
| Nonlinear range-bearing fixture | controlled diagnostic/proxy row only |
| Student EDH/PFPF panels | comparison-only context |
| Stochastic flow | deferred clean-room spec |
| Kernel PFF | excluded pending debug |
| HMC/posterior/production | not concluded |

## Skeptical Result Audit

- Stale context: DPF2 was Claude-accepted and records `DPF3 may start: yes`.
- Wrong baseline: DPF3 uses DPF1/DPF0 monograph PF-PF correction, not student
  EDH/PFPF output.
- Proxy overclaim: affine parity and controlled/student proxy panels are not
  nonlinear filtering or posterior evidence.
- Stop conditions: missing proposal density, target density, pre/post-flow
  binding, Jacobian sign, or corrected log weight blocks movement.
- Hidden production/monograph drift: no production or monograph file was edited.
- Vendored-code contamination: no student code was copied, imported, executed,
  or edited.
- High-dimensional-lane contamination: no separate high-dimensional nonlinear
  filtering lane file was used.
- Artifact fitness: the spec and risk/exclusion registers answer the DPF3
  proposal-correction question.

## Review Record

- Claude reviewer command: `claude -p --model claude-opus-4-7 --effort max`
- Iteration 1: `ACCEPT`
- Claude findings: DPF3 anchors on DPF2 acceptance, uses DPF1/monograph/affine
  evidence as authority, keeps student EDH/PFPF comparison-only, separates
  affine parity from nonlinear diagnostics, states proposal/target/Jacobian/
  corrected-log-weight obligations, preserves kernel PFF exclusion and
  stochastic-flow deferral, and avoids HMC/posterior/production claims.
- Codex audit: accepted Claude's findings and applied only the authorized
  metadata update.
- Final review status: accepted for DPF4 start.

## Verification Summary

- `rg -n "excluded-flow-risk-register|kernel-pff-exclusion-check|kernel PFF remains excluded|Kernel PFF|Jacobian|proposal|corrected|affine|not concluded|target density|student|production|high-dimensional|HMC|posterior" docs/plans/bayesfilter-dpf-implementation-dpf3-*.md`: passed.
- `git diff --check`: passed.
- `py_compile`: not run because no Python files were touched.

## Run Manifest

- command family: document reads and `rg`/`sed` searches only.
- commit: `0477f56c9e76462de2d5acb167f5bf9d1b65de42`.
- CPU/GPU status: N/A; no experiment or GPU command was run.
- random seeds: N/A.
- touched Python files: none.

## What Is Not Concluded

DPF3 does not establish general nonlinear flow correctness, full filtering
correctness, original posterior preservation, HMC validity, production API
readiness, or banking/model-risk use.
