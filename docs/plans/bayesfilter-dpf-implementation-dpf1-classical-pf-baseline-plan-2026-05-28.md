# Plan DPF1: Classical Bootstrap/SIR Particle Filter Baseline

## Date

2026-05-28

## Lane Boundaries

- Use DPF0 outputs as authority; student artifacts are comparison-only context.
- Do not edit vendored student files and do not execute student code.
- Do not read or edit the high-dimensional nonlinear filtering lane.
- Do not edit production `bayesfilter/` code in this phase.

## Evidence Contract

Question: What BayesFilter-owned classical PF baseline is required before
differentiable DPF components can be evaluated?

Baseline/comparator: Kalman-filter LGSSM references, existing nonlinear fixture
records, and DPF0 implementation obligations.

Primary criterion: a reviewed implementation specification for log weights,
ESS, resampling, likelihood-estimator semantics, seeds, dtype/shape contracts,
and LGSSM recovery tests.

Veto diagnostics: ambiguous likelihood semantics; resampling bias hidden;
student code copied; no independent reference; production API edits before DPF6.

Explanatory diagnostics: student PF/EDH/PFPF panels and controlled-baseline
qualitative comparisons.

What will not be concluded: no differentiable resampling validity, no PF-PF
validity, no production readiness, no HMC validity.

## Exact Inputs

- `docs/plans/bayesfilter-dpf-implementation-dpf0-implementation-obligations-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf0-result-2026-05-28.md`;
- `docs/chapters/ch19_particle_filters.tex`;
- `experiments/dpf_monograph_evidence/reports/linear-gaussian-recovery-result.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-gap-closure-result-2026-05-10.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-linear-stress-result-2026-05-10.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-nonlinear-smoke-result-2026-05-10.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-nonlinear-reference-panel-result-2026-05-10.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-smoke-result.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-comparison-audit.md`;
- `docs/chapters/ch32_production_checklist.tex`.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-spec-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf1-reference-test-contract-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf1-student-comparison-context-register-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf1-result-2026-05-28.md`.

## Skeptical Plan Audit Checklist

- Is the classical PF baseline independent of student implementation code?
- Are student reports used only as comparison context, not correctness evidence?
- Are vendored student files untouched and unexecuted?
- Are student comparison rows excluded from acceptance evidence?
- Are log-normalizer and likelihood-estimator semantics explicit?
- Are resampling conditions and ESS definitions explicit?
- Are seeds and stochastic diagnostics reproducible?
- Are exact-reference claims limited to LGSSM reference cells?

## Execution Steps

1. Specify the baseline PF algorithm and result schema.
2. Specify LGSSM recovery and nonlinear smoke/reference tests.
3. Specify artifact fields and stop labels.
4. Defer code unless the reviewed result explicitly authorizes it.

## Review Protocol

Claude Code Opus 4.7 max effort, read-only, `ACCEPT`/`REJECT`, max 5 iterations.

## Verification Commands

```bash
git diff --check
rg -n "reference-test-contract|comparison-only|not acceptance evidence|student|vendor|production|HMC|not concluded" docs/plans/bayesfilter-dpf-implementation-dpf1-*.md
git status --short --branch
```

## Stop Conditions

- no independent reference is available for first-rung correctness;
- likelihood estimate semantics remain ambiguous;
- student comparison rows would be used as acceptance evidence;
- vendored student code would need to be copied, edited, or executed;
- implementation requires production API changes.

## What Must Not Be Concluded

DPF1 does not validate differentiable PF, DPF-HMC, learned OT, or production
BayesFilter behavior.

## Review Record

- Claude Code reviewer: `claude-opus-4-7`, `--effort max`.
- Iteration 1: `REJECT`; required exact inputs and explicit no-vendored-student
  boundary.
- Iteration 2: `REJECT`; required exact output artifacts and student comparison
  not-as-acceptance-evidence stop condition.
- Iteration 3: `ACCEPT`.
- Codex audit: agreed with rejected findings, patched this plan, and accepted
  the iteration-3 result.
