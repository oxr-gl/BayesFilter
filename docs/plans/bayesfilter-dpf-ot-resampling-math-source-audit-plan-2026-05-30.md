# Plan: DPF OT Resampling Math Source Audit

## Evidence Contract

Question: does the BayesFilter DPF lane implement the mathematics of
differentiable particle filtering via entropy-regularized optimal transport in
a way that supports the current OT-resampling claims, and are the LaTeX
chapter and experimental code consistent with the inspected primary sources?

Primary sources to inspect:

- Corenflos, Thornton, Deligiannidis, and Doucet, "Differentiable Particle
  Filtering via Entropy-Regularized Optimal Transport", ICML 2021.
- Zhu, Murphy, and Jonschkowski, "Towards Differentiable Resampling", 2020, as
  soft-resampling context.
- Cuturi, "Sinkhorn Distances", NeurIPS 2013, as Sinkhorn/EOT background.
- Peyre and Cuturi, "Computational Optimal Transport", 2019, as OT background
  only if local full text is available.
- Reich 2013 may be used only for ensemble-transform context already cached
  locally.

Primary pass/fail criterion: each claim about OT resampling must be classified
as source-supported, project-derived, implementation-only, or unsupported.  In
particular, distinguish finite-$N$ value preservation, affine-test-function
preservation, asymptotic consistency, differentiability of the chosen relaxed
operator, categorical-resampling equivalence, and unbiased likelihood
estimation.

Veto diagnostics:

- source unavailable for the Corenflos paper;
- local code claims categorical or likelihood preservation for barycentric
  Sinkhorn without a derivation;
- LaTeX claims exact posterior/likelihood preservation beyond the inspected
  sources;
- code implements a different coupling, marginal convention, or barycentric map
  than the documented object without recording the difference.

Explanatory diagnostics:

- finite Sinkhorn marginal residuals;
- linear structural AR(1) MLE shift under relaxed OT;
- implementation labels such as "relaxed finite Sinkhorn not categorical";
- asymptotic statements from the paper that do not imply finite sample
  equality.

What will not be concluded: no production readiness, no HMC validity, no
posterior correctness, no broad rejection of OT resampling as a differentiable
surrogate, and no monograph chapter edit.  Any chapter change is deferred to a
patch/register artifact.

## Allowed Write Set

- `.localsource/dpf_ot_audit/`
- `docs/plans/bayesfilter-dpf-ot-resampling-math-source-audit-*.md`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- vendored or student code
- high-dimensional nonlinear filtering lane
- monograph chapters
- production code

## Skeptical Audit Before Execution

| Risk | Status | Note |
|---|---:|---|
| stale context | pass | Current trigger is the structural AR(1) OT MLE shift and ch32/code scan. |
| wrong paper | pass | Seed paper is the cited Corenflos et al. ICML OT-DPF paper. |
| source unavailable | pending | Fetch or record blocker. |
| overclaim by finite residuals | pass | Marginal residuals are numerical diagnostics only. |
| asymptotic/finite-N confusion | pass | Audit explicitly separates those layers. |
| code/document mismatch | pending | To be checked after source extraction. |
| hidden production drift | pass | No production edits allowed. |
| monograph drift | pass | No chapter edits allowed. |
| high-dimensional-lane contamination | pass | Audit is DPF/OT lane only. |
| artifact answers question | pass | Result will decide source support and code/doc consistency. |

## Verification Commands

```bash
rg -n "categorical|unbiased|likelihood|posterior|barycentric|Sinkhorn|finite" docs/chapters/ch32_diff_resampling_neural_ot.tex experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py experiments/dpf_implementation/tf_tfp/structural/resampling_policies_tf.py
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp
git diff --check
git status --short --branch
```
