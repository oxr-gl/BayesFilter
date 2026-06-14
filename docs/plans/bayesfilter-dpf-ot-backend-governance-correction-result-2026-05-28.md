# DPF OT Backend Governance Correction Result

Date: 2026-05-28

## Decision

`BACKEND_GOVERNANCE_CORRECTION_ACCEPTED`

## Decision Table

| Check | Status | Evidence |
| --- | --- | --- |
| repo backend governance | pass | root `AGENTS.md` and `CLAUDE.md` record TF/TFP as the default implementation backend |
| NumPy policy | pass | NumPy is limited to reference/comparison/closed-form/reporting or reviewed exceptions |
| DPF OT reclassification | pass | DPF OT lane docs and reports mark existing artifacts as NumPy prototype/reference/comparison smoke |
| implementation gap | pass | `TF_TFP_OT_DPF_IMPLEMENTATION_NOT_BUILT` is recorded |
| follow-up plan | pass | `docs/plans/bayesfilter-dpf-ot-tf-tfp-rewrite-plan-2026-05-28.md` created |
| forbidden writes | pass with caveat | this correction touched only governance and DPF OT documentation/report paths; pre-existing controlled-baseline dirty files remain unrelated |
| scoped whitespace | pass | lane-scoped trailing-whitespace scan and scoped `git diff --check` passed |
| full `git diff --check` | blocked outside lane | pre-existing dirty `docs/main.pdf` binary whitespace noise still fails full check |

## Correction Summary

The current DPF OT artifacts remain useful smoke/comparator evidence, but they
are no longer described as the BayesFilter-owned default implementation path.
They are NumPy prototype/reference/comparison smoke evidence only.

Historical DPF OT subplans that still mention NumPy implementation are
superseded for implementation authority by the corrected master/P8/README/report
records and by the TF/TFP rewrite plan.  They remain a historical record of the
prototype smoke harness.

BayesFilter's default algorithmic implementation backend is TensorFlow /
TensorFlow Probability.  Differentiable or gradient-bearing implementation
paths must use TF/TFP unless a reviewed plan explicitly grants an exception.

Actual DPF OT implementation gap:
`TF_TFP_OT_DPF_IMPLEMENTATION_NOT_BUILT`.

## Claude Plan Review

- Iteration 1: `REJECT`; Claude found the write set too broad and NumPy
  verification insufficiently path-aware.
- Iteration 2: `ACCEPT`; Claude accepted the narrowed
  documentation/governance-only correction plan.
- Codex audit: agreed with both findings and accepted iteration 2.

## Claude Result Review

- Iteration 1: `ACCEPT`.
- Claude finding: root governance makes TF/TFP the default backend; NumPy is
  restricted to reference/comparison/closed-form/reporting/reviewed exceptions;
  DPF OT artifacts are consistently reclassified as NumPy
  prototype/reference/comparison smoke only; `TF_TFP_OT_DPF_IMPLEMENTATION_NOT_BUILT`
  is recorded; the rewrite plan includes the NumPy import gate and same-scalar
  `tf.GradientTape` check; no production, monograph, high-dimensional, vendored,
  or code drift is authorized by the inspected artifacts.
- Codex audit: agreed.

## Files Updated Or Created

- `AGENTS.md`
- `CLAUDE.md`
- `docs/plans/bayesfilter-dpf-ot-backend-governance-correction-plan-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-backend-governance-correction-result-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-rewrite-plan-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-implementation-master-program-2026-05-28.md`
- `docs/plans/bayesfilter-dpf-ot-implementation-p8-final-audit-and-handoff-result-2026-05-28.md`
- `experiments/dpf_implementation/README.md`
- `experiments/dpf_implementation/reports/dpf-ot-final-audit-2026-05-28.md`
- `experiments/dpf_implementation/reports/dpf-ot-lgssm-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/dpf-ot-range-bearing-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/dpf-ot-gradient-check-result-2026-05-28.md`

## Caveats

- No TF/TFP implementation was built in this correction pass.
- Existing NumPy prototype code remains in place and is intentionally relabeled,
  not deleted.
- Existing NumPy imports remain in prototype/reference/comparison files; this is
  documented as a current gap, not made compliant by relabeling.
- No production readiness, public API readiness, HMC readiness, posterior
  correctness, monograph validation, learned/neural OT promotion, or
  banking/model-risk claim follows.

## Verification

Commands run:

- `rg -n "TensorFlow|TensorFlow Probability|TF/TFP|NumPy|default backend|reviewed exception" AGENTS.md CLAUDE.md docs/plans/bayesfilter-dpf-ot-*.md experiments/dpf_implementation/README.md experiments/dpf_implementation/reports/dpf-ot-*.md`: pass; governance and classification wording present.
- `rg -n "import numpy|from numpy" experiments/dpf_implementation/filters experiments/dpf_implementation/resampling experiments/dpf_implementation/runners`: found existing NumPy imports in prototype implementation/runners; expected under this correction because no Python files were edited and docs reclassify them as prototype/reference/comparison smoke only.
- `rg -n "import numpy|from numpy" experiments/dpf_implementation/fixtures experiments/dpf_implementation/references experiments/dpf_implementation/reports`: found existing NumPy imports in fixtures/references; allowed as reference/comparison context.
- `rg -n "NumPy.*prototype|prototype/reference/comparison|TF_TFP_OT_DPF_IMPLEMENTATION_NOT_BUILT|not the BayesFilter-owned default implementation" docs/plans/bayesfilter-dpf-ot-*.md experiments/dpf_implementation/README.md experiments/dpf_implementation/reports/dpf-ot-*.md`: pass; correction labels present.
- `git diff --name-only -- experiments/dpf_implementation/*.py experiments/dpf_implementation/filters experiments/dpf_implementation/resampling experiments/dpf_implementation/runners experiments/dpf_implementation/fixtures experiments/dpf_implementation/references`: no output; this correction did not edit algorithmic Python files.
- `git diff --name-only -- bayesfilter tests docs/chapters docs/references.bib experiments/student_dpf_baselines experiments/controlled_dpf_baseline`: output only pre-existing controlled-baseline dirty files; no new correction edits were made there.
- `rg -n "[ \t]+$" AGENTS.md CLAUDE.md docs/plans/bayesfilter-dpf-ot-*.md experiments/dpf_implementation/README.md experiments/dpf_implementation/reports/dpf-ot-*.md`: no matches.
- `git diff --check -- AGENTS.md CLAUDE.md docs/plans/bayesfilter-dpf-ot-*.md experiments/dpf_implementation/README.md experiments/dpf_implementation/reports/dpf-ot-*.md`: pass for tracked scoped diff; untracked-file whitespace was covered by the `rg` scan above.
- `git diff --check`: fails outside this correction because dirty binary `docs/main.pdf` reports trailing whitespace.
- `git status --short --branch`: branch `main...origin/main [ahead 5]`; unrelated dirty files remain.

`py_compile` was not run because this correction touched no Python files.

## Next Recommended Action

Review and execute
`docs/plans/bayesfilter-dpf-ot-tf-tfp-rewrite-plan-2026-05-28.md` to build the
actual TF/TFP OT-DPF implementation path with a `tf.GradientTape` same-scalar
gradient check.
