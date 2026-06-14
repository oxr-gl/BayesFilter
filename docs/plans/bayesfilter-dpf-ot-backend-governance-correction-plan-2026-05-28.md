# DPF OT Backend Governance Correction Plan

Date: 2026-05-28

## Decision

`ACCEPTED_FOR_EXECUTION`

## Scope

This correction is limited to repo-wide governance and the DPF implementation
and evidence lane.  It does not authorize production `bayesfilter/` algorithm
edits, monograph chapter edits, vendored student edits, or high-dimensional
nonlinear filtering lane edits.

This correction is documentation/governance-only.  It may relabel existing
NumPy artifacts in plans, README files, and result notes, but it must not edit
algorithmic Python implementation files in this pass.

## Problem

The DPF OT lane created NumPy-based experimental OT-DPF value-path artifacts and
described them as an implementation path.  The repo-level policy is stricter:
TensorFlow / TensorFlow Probability is the default BayesFilter implementation
backend.  NumPy is allowed only for reference solutions, comparison fixtures,
closed-form sanity checks, serialization/reporting, and narrowly reviewed
exceptions.  Therefore the current NumPy OT-DPF artifacts must be reclassified
as prototype/reference/comparison smoke evidence, not the real BayesFilter-owned
default implementation.

## Evidence Contract

Question: can we correct governance and DPF lane records so the repo-wide
TF/TFP default is durable and the NumPy OT-DPF artifacts cannot be mistaken for
the actual implementation?

Baseline: user-stated backend policy and existing DPF OT lane artifacts.

Primary criterion:

- root governance documents record TF/TFP as the default implementation backend;
- NumPy is explicitly limited to reference/comparison/closed-form/reporting or
  reviewed exceptions;
- DPF OT lane docs and reports reclassify the current NumPy OT-DPF artifacts as
  prototype/reference/comparison smoke evidence only;
- the actual gap is recorded as `TF_TFP_OT_DPF_IMPLEMENTATION_NOT_BUILT`;
- a TF/TFP rewrite plan is created.

Veto diagnostics:

- any production `bayesfilter/` algorithm file is edited;
- any monograph chapter, vendored student file, or high-dimensional nonlinear
  filtering lane file is edited;
- NumPy artifacts continue to be called the real BayesFilter-owned default
  implementation;
- TF/TFP rewrite plan permits NumPy implementation code without a reviewed
  exception;
- proxy/smoke evidence is promoted to production, posterior, HMC, or monograph
  validation.

What will not be concluded:

- no TF/TFP implementation is built by this correction;
- no production readiness;
- no HMC or posterior correctness;
- no monograph validation;
- no learned/neural OT promotion.

## Skeptical Plan Audit

| Check | Status | Notes |
| --- | --- | --- |
| stale context | pass | The DPF OT lane has accepted NumPy smoke artifacts, and the user has now supplied a stricter backend policy. |
| wrong backend | pass | This plan corrects the default backend to TF/TFP and reclassifies NumPy as reference/prototype only. |
| NumPy implementation overclaim | pass | The main correction target is removing any implication that NumPy OT-DPF is the default implementation. |
| proxy overclaim | pass | Smoke, RMSE, Sinkhorn residuals, and finite differences remain experimental evidence only. |
| missing stop conditions | pass | Vetoes cover forbidden writes, backend drift, and overclaim. |
| hidden production drift | pass | Production `bayesfilter/` algorithm files are forbidden. |
| monograph drift | pass | `docs/chapters/` and references are forbidden. |
| vendored-code contamination | pass | Vendored student paths are forbidden. |
| high-dimensional-lane contamination | pass | High-dimensional nonlinear filtering plans/reports/chapters are forbidden. |
| artifact fitness | pass | Governance files, corrected lane docs, final audit notes, and TF/TFP rewrite plan answer the correction question. |

## Inputs

- Thread-supplied repo policy: TF/TFP is default implementation backend.
- Existing DPF OT master/subplans/results:
  - `docs/plans/bayesfilter-dpf-ot-implementation-master-program-2026-05-28.md`
  - `docs/plans/bayesfilter-dpf-ot-implementation-p8-final-audit-and-handoff-result-2026-05-28.md`
- Existing DPF implementation README and reports:
  - `experiments/dpf_implementation/README.md`
  - `experiments/dpf_implementation/reports/dpf-ot-final-audit-2026-05-28.md`
  - `experiments/dpf_implementation/reports/dpf-ot-lgssm-result-2026-05-28.md`
  - `experiments/dpf_implementation/reports/dpf-ot-range-bearing-result-2026-05-28.md`
  - `experiments/dpf_implementation/reports/dpf-ot-gradient-check-result-2026-05-28.md`

## Allowed Write Set

- `AGENTS.md` at repo root, if absent or needing governance update.
- `CLAUDE.md` at repo root, if absent or needing governance update.
- `docs/plans/bayesfilter-dpf-ot-backend-governance-correction-plan-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-backend-governance-correction-result-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-rewrite-plan-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-implementation-master-program-2026-05-28.md`
  only to relabel the prior NumPy lane as prototype/reference/comparison smoke.
- `docs/plans/bayesfilter-dpf-ot-implementation-p8-final-audit-and-handoff-result-2026-05-28.md`
  only to record `TF_TFP_OT_DPF_IMPLEMENTATION_NOT_BUILT` and revised caveats.
- `experiments/dpf_implementation/README.md` only to correct artifact
  classification and backend policy.
- `experiments/dpf_implementation/reports/dpf-ot-final-audit-2026-05-28.md`
  only to correct final status/caveats.
- `experiments/dpf_implementation/reports/dpf-ot-lgssm-result-2026-05-28.md`
  only to label NumPy as prototype/reference/comparison smoke.
- `experiments/dpf_implementation/reports/dpf-ot-range-bearing-result-2026-05-28.md`
  only to label NumPy as prototype/reference/comparison smoke.
- `experiments/dpf_implementation/reports/dpf-ot-gradient-check-result-2026-05-28.md`
  only to label NumPy as finite-difference/reference smoke.

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `docs/references.bib`
- high-dimensional nonlinear filtering plans, reports, chapters, or sources;
- vendored student code;
- unrelated student DPF closeout artifacts;
- controlled-baseline code or reports;
- generated PDFs.
- algorithmic Python files under `experiments/dpf_implementation/` in this
  correction pass; the TF/TFP rewrite plan will handle code movement/rewrite.

## Execution Steps

1. Review this correction plan with Claude Code using exact command:
   `claude -p --model claude-opus-4-7 --effort max`.
2. If accepted, create or update root `AGENTS.md` and `CLAUDE.md` with backend
   governance.
3. Patch DPF OT lane records to say the current NumPy artifacts are
   prototype/reference/comparison smoke evidence only.
4. Patch DPF OT final reports to record
   `TF_TFP_OT_DPF_IMPLEMENTATION_NOT_BUILT`.
5. Create `docs/plans/bayesfilter-dpf-ot-tf-tfp-rewrite-plan-2026-05-28.md`.
6. Write correction result note.
7. Run verification and Claude result review.

## TF/TFP Rewrite Plan Requirements

The follow-up plan must require:

- TF/TFP-only implementation scope for algorithmic code;
- NumPy import gate for implementation modules;
- NumPy allowed only in reference/comparator/closed-form/reporting files;
- LGSSM with Kalman/reference comparator;
- range-bearing Gaussian with UKF/reference comparator;
- finite Sinkhorn/entropic OT in TensorFlow;
- same-scalar autodiff gradient check using `tf.GradientTape`;
- finite-difference comparator as reference only;
- CPU-only first with `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import;
- verification commands, stop conditions, and non-implications.

## Verification Commands

```bash
rg -n "TensorFlow|TensorFlow Probability|TF/TFP|NumPy|default backend|reviewed exception" AGENTS.md CLAUDE.md docs/plans/bayesfilter-dpf-ot-*.md experiments/dpf_implementation/README.md experiments/dpf_implementation/reports/dpf-ot-*.md
rg -n "import numpy|from numpy" experiments/dpf_implementation/filters experiments/dpf_implementation/resampling experiments/dpf_implementation/runners
rg -n "import numpy|from numpy" experiments/dpf_implementation/fixtures experiments/dpf_implementation/references experiments/dpf_implementation/reports || true
rg -n "NumPy.*prototype|prototype/reference/comparison|TF_TFP_OT_DPF_IMPLEMENTATION_NOT_BUILT|not the BayesFilter-owned default implementation" docs/plans/bayesfilter-dpf-ot-*.md experiments/dpf_implementation/README.md experiments/dpf_implementation/reports/dpf-ot-*.md
git diff --name-only -- experiments/dpf_implementation/*.py experiments/dpf_implementation/filters experiments/dpf_implementation/resampling experiments/dpf_implementation/runners experiments/dpf_implementation/fixtures experiments/dpf_implementation/references
git diff --name-only -- bayesfilter tests docs/chapters docs/references.bib experiments/student_dpf_baselines experiments/controlled_dpf_baseline
git diff --check -- AGENTS.md CLAUDE.md docs/plans/bayesfilter-dpf-ot-*.md experiments/dpf_implementation/README.md experiments/dpf_implementation/reports/dpf-ot-*.md
git diff --check
git status --short --branch
```

Interpretation of NumPy checks:

- Existing `import numpy` in prototype/reference/comparison code is expected and
  is not made compliant by this documentation-only correction.
- This correction passes only if docs classify that NumPy code as
  prototype/reference/comparison smoke and if the TF/TFP rewrite plan defines a
  future implementation-module NumPy import gate.
- If this correction modifies algorithmic Python files, stop: that is outside
  scope.

Full `git diff --check` may be reported with an explicit caveat if pre-existing
dirty `docs/main.pdf` binary whitespace noise remains outside this lane.  The
scoped diff check must pass.

## Claude Review Protocol

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

If the exact command/model/effort is unavailable, stop and report a blocker.
Claude reviews read-only and returns `ACCEPT` or `REJECT` with findings.  Codex
audits Claude's findings, patches if needed, and loops up to five iterations.
On iteration 5, accept only for user inspection unless a major blocker remains.

## Review Record

- Iteration 1: `REJECT`.
- Claude finding: allowed write set was too broad/insufficiently justified for
  documentation-only correction, and NumPy verification did not distinguish
  forbidden implementation-path NumPy from allowed reference/reporting NumPy.
- Codex audit: agreed.
- Patch after iteration 1: clarified documentation/governance-only scope,
  narrowed allowed write semantics to relabel-only documentation changes,
  forbade algorithmic Python edits in this correction pass, and added
  path/status-aware NumPy verification interpretation.
- Iteration 2: `ACCEPT`.
- Claude finding: the plan is now documentation/governance-only, the allowed
  write set is narrowly justified, algorithmic Python edits are forbidden,
  NumPy verification is honest/path-aware, and no production, monograph,
  high-dimensional, or vendored drift is authorized.  Minor note: root
  `AGENTS.md`/`CLAUDE.md` creation remains broader than lane docs, but is
  explicitly governance-scoped.
- Codex audit: agreed; the minor note is within the user-requested repo-wide
  governance scope.
