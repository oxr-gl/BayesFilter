# Plan DPF2: Differentiable Resampling Components

## Date

2026-05-28

## Lane Boundaries

- Use DPF0-DPF1 outputs and DPF monograph/literature sources as authority.
- Student artifacts are comparison-only context.
- Do not edit vendored student files and do not execute student code.
- Do not read or import high-dimensional nonlinear filtering lane materials,
  including for learned/neural paths.
- Do not edit production `bayesfilter/` code in this phase.

## Evidence Contract

Question: Which differentiable resampling components can be specified as
BayesFilter-owned optional components without overclaiming correctness?

Baseline/comparator: DPF0 obligations, DPF1 classical resampling semantics,
soft/Sinkhorn/OT literature claims, DPF monograph evidence, and student
future-work usability gates.

Primary criterion: component specifications state inputs, outputs, gradients,
bias/proxy semantics, tests, and non-implications.

Veto diagnostics: gradient finiteness treated as unbiased resampling or
posterior validity; learned/neural components require unreviewed artifacts;
student implementation copied; no bias/proxy label.

Explanatory diagnostics: finite-output/finite-gradient smokes from student and
monograph evidence artifacts.

What will not be concluded: no exact likelihood, unbiased resampling, HMC
target validity, or production default.

## Exact Inputs

- `docs/plans/bayesfilter-dpf-implementation-dpf0-implementation-obligations-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf0-result-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-spec-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf1-result-2026-05-28.md`;
- `docs/chapters/ch32_diff_resampling_neural_ot.tex`;
- `experiments/dpf_monograph_evidence/reports/resampling-sinkhorn-result.md`;
- `experiments/dpf_monograph_evidence/reports/learned-ot-residual-result.md`;
- `experiments/dpf_monograph_evidence/reports/dpf-monograph-research-evidence-note.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-future-work-usability-gates-result-2026-05-15.md`.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-dpf2-component-spec-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf2-bias-proxy-ledger-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf2-resampling-test-contract-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf2-deferred-neural-path-register-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf2-result-2026-05-28.md`.

## Skeptical Plan Audit Checklist

- Are hard and relaxed resampling semantics separated?
- Are gradient paths and stopped-gradient choices explicit?
- Are bias and proxy interpretations recorded?
- Are neural/artifact-dependent paths kept out unless separately specified?
- Are learned/neural paths deferred unless specified from BayesFilter-owned
  sources rather than student usability gates?
- Are tests downstream, not only finite-gradient probes?
- Are high-dimensional nonlinear filtering lane materials excluded?
- Are vendored student files untouched and unexecuted?

## Execution Steps

1. Specify soft and Sinkhorn/OT-style component contracts.
2. Identify required tests and artifact fields.
3. Label unsupported neural/amortized paths for future component specs.
4. Write result and next decision.

## Review Protocol

Claude Code Opus 4.7 max effort, read-only, `ACCEPT`/`REJECT`, max 5 iterations.

## Verification Commands

```bash
rg -n "bias-proxy-ledger|resampling-test-contract|deferred-neural-path|BayesFilter-owned|bias|proxy|gradient|not concluded|unbiased|HMC" docs/plans/bayesfilter-dpf-implementation-dpf2-*.md
git diff --check
git status --short --branch
```

## Stop Conditions

- component semantics cannot be stated without copying student code;
- neural artifacts become required before their own spec;
- high-dimensional nonlinear filtering lane material would be required;
- claims exceed component-level evidence.

## What Must Not Be Concluded

DPF2 does not validate a full DPF, likelihood estimator, posterior target, or
production implementation.

## Review Record

- Claude Code reviewer: `claude-opus-4-7`, `--effort max`.
- Iteration 1: `REJECT`; required exact inputs, explicit high-dimensional-lane
  exclusion for learned/neural paths, and no-vendored-edit boundary.
- Iteration 2: `REJECT`; required bias/proxy/test/deferred-neural output
  artifacts and learned-neural deferral checks.
- Iteration 3: `ACCEPT`.
- Codex audit: agreed with rejected findings, patched this plan, and accepted
  the iteration-3 result.
