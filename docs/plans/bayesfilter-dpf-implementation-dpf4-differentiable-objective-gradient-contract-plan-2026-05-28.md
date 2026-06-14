# Plan DPF4: Differentiable Objective And Gradient Contract

## Date

2026-05-28

## Lane Boundaries

- Use only DPF0-DPF3 outputs and DPF monograph/literature sources as authority.
- Do not import high-dimensional nonlinear filtering or HMC lanes as authority
  unless the claim is already cited inside accepted DPF outputs.
- Student artifacts are comparison-only context.
- Do not edit vendored student files and do not execute student code.
- Do not edit production `bayesfilter/` code in this phase.

## Evidence Contract

Question: What objective is differentiated by the DPF implementation, and what
does its gradient mean?

Baseline/comparator: DPF0 obligations, DPF1 classical likelihood semantics,
DPF2 relaxed component semantics, and DPF3 PF-PF correction semantics.

Primary criterion: every proposed differentiable objective is labeled as
filtering proxy, surrogate likelihood, transport residual, component loss, or
posterior/HMC candidate with required downstream evidence.

Veto diagnostics: proxy gradient promoted to exact likelihood score; gradient
finiteness promoted to posterior validity; HMC target created without
separate sampler evidence; missing stop-gradient/relaxation semantics.

Explanatory diagnostics: finite-gradient probes and DPF monograph value-gradient
evidence.

What will not be concluded: no HMC convergence, no posterior correctness, no
production optimizer default, no scientific validity from training loss alone.

## Exact Inputs

- `docs/plans/bayesfilter-dpf-implementation-dpf0-implementation-obligations-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-spec-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf2-component-spec-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf3-flow-pfpf-spec-2026-05-28.md`;
- `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`;
- `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`;
- `experiments/dpf_monograph_evidence/reports/hmc-value-gradient-result.md`;
- `experiments/dpf_monograph_evidence/reports/resampling-sinkhorn-result.md`;
- `experiments/dpf_monograph_evidence/reports/learned-ot-residual-result.md`;
- `experiments/dpf_monograph_evidence/reports/dpf-monograph-research-evidence-note.md`.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-dpf4-objective-classification-ledger-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf4-gradient-contract-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf4-downstream-evidence-requirements-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf4-result-2026-05-28.md`.

## Skeptical Plan Audit Checklist

- Is the differentiated scalar identified?
- Are stochastic gradient estimators and seeds defined?
- Are stopped-gradient, reparameterized, and relaxed paths separated?
- Are proxy objectives separated from likelihood/posterior objectives?
- Are downstream validation requirements explicit?
- Are high-dimensional nonlinear filtering and external HMC lanes excluded as
  authority?
- Are vendored student files untouched and unexecuted?

## Execution Steps

1. Inventory candidate objectives.
2. Classify gradient semantics and non-implications.
3. Specify finite-gradient and downstream checks.
4. Block any HMC/posterior target without a separate plan.
5. Write result.

## Review Protocol

Claude Code Opus 4.7 max effort, read-only, `ACCEPT`/`REJECT`, max 5 iterations.

## Verification Commands

```bash
rg -n "objective-classification-ledger|downstream-evidence-requirements|what it is not|proxy|surrogate|likelihood|posterior|HMC|not concluded|gradient" docs/plans/bayesfilter-dpf-implementation-dpf4-*.md
git diff --check
git status --short --branch
```

## Stop Conditions

- objective cannot be classified;
- likelihood/posterior semantics are ambiguous;
- HMC is required for phase success.
- high-dimensional nonlinear filtering or HMC lane material would be required as
  authority;
- vendored student code would need to be edited or executed.

## What Must Not Be Concluded

DPF4 does not validate posterior inference, HMC, production optimization, or
scientific claims.

## Review Record

- Claude Code reviewer: `claude-opus-4-7`, `--effort max`.
- Iteration 1: `REJECT`; required exact inputs and explicit lane/vendor
  boundaries.
- Iteration 2: `REJECT`; required objective-classification and downstream
  evidence output artifacts plus "what it is not" verification.
- Iteration 3: `ACCEPT`.
- Codex audit: agreed with rejected findings, patched this plan, and accepted
  the iteration-3 result.
