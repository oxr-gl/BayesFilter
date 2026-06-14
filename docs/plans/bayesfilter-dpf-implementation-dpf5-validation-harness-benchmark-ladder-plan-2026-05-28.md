# Plan DPF5: Validation Harness And Benchmark Ladder

## Date

2026-05-28

## Lane Boundaries

- DPF5 defines the validation harness only; it does not authorize production
  package edits.
- Student aggregate agreement is explanatory only and cannot be a promotion
  criterion.
- Do not edit vendored student files and do not execute student code.
- Do not read or edit the high-dimensional nonlinear filtering lane.
- Do not edit production `bayesfilter/` code in this phase.

## Evidence Contract

Question: What validation harness is needed to evaluate a BayesFilter-owned DPF
without overclaiming?

Baseline/comparator: DPF1 classical PF, DPF2 components, DPF3 flow/PF-PF, DPF4
gradient contract, Kalman LGSSM references, affine parity fixtures,
range-bearing controlled fixtures, and frozen student aggregate proxy evidence.

Primary criterion: a tiered harness specifies correctness, numerical,
gradient, proxy, and performance checks with promotion/veto rules.

Veto diagnostics: proxy metrics used as correctness; single-seed stochastic
results promoted; runtime-only ranking despite failed numerical diagnostics;
student agreement used as validation.

Explanatory diagnostics: smoke runtimes, ESS, resampling pressure, finite
outputs, qualitative same-regime comparisons.

What will not be concluded: no production readiness, HMC readiness, broad
high-dimensional readiness, or default-policy change.

## Exact Inputs

- `docs/plans/bayesfilter-dpf-implementation-dpf0-implementation-obligations-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-spec-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf2-component-spec-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf3-flow-pfpf-spec-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf4-gradient-contract-2026-05-28.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-smoke-result.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-comparison-audit.md`;
- `experiments/dpf_monograph_evidence/reports/linear-gaussian-recovery-result.md`;
- `experiments/dpf_monograph_evidence/reports/affine-flow-pfpf-result.md`;
- `experiments/dpf_monograph_evidence/reports/resampling-sinkhorn-result.md`;
- `experiments/dpf_monograph_evidence/reports/hmc-value-gradient-result.md`;
- `experiments/dpf_monograph_evidence/reports/dpf-monograph-research-evidence-note.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-nonlinear-smoke-result-2026-05-10.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-nonlinear-reference-panel-result-2026-05-10.md`;
- `docs/chapters/ch32_production_checklist.tex`.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-dpf5-validation-harness-spec-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf5-benchmark-ladder-matrix-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf5-seed-uncertainty-policy-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf5-cpu-gpu-runtime-policy-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf5-result-2026-05-28.md`;
- future benchmark script paths only if authorized by result.

## Skeptical Plan Audit Checklist

- Are veto diagnostics evaluated before speed/ranking?
- Are Monte Carlo uncertainty and seed policy stated?
- Are artifact sizes and runtime bounds stated?
- Are CPU/GPU policies clear?
- Are promotion criteria downstream, not proxy-only?
- Is student aggregate agreement excluded from promotion criteria?
- Are production `bayesfilter/` files untouched?

## Execution Steps

1. Define benchmark tiers from smoke to validation.
2. Define metrics, vetoes, and artifacts.
3. Define seed and uncertainty policy.
4. Define what cannot be ranked.
5. Write result.

## Review Protocol

Claude Code Opus 4.7 max effort, read-only, `ACCEPT`/`REJECT`, max 5 iterations.

## Verification Commands

```bash
rg -n "benchmark-ladder-matrix|seed-uncertainty-policy|cpu-gpu-runtime-policy|veto|seed|runtime|CPU|GPU|proxy|not concluded|promotion" docs/plans/bayesfilter-dpf-implementation-dpf5-*.md
git diff --check
git status --short --branch
```

## Stop Conditions

- no independent correctness rung is available;
- benchmark artifacts would be too large;
- GPU is required without trusted-permission plan.
- student aggregate agreement would be used as promotion evidence;
- production package edits would be required.

## What Must Not Be Concluded

DPF5 does not make a production/default decision; it defines evidence needed for
such a decision.

## Review Record

- Claude Code reviewer: `claude-opus-4-7`, `--effort max`.
- Iteration 1: `REJECT`; required exact inputs, explicit student-agreement stop
  condition, and no production-package edit boundary.
- Iteration 2: `REJECT`; required benchmark matrix, seed/uncertainty policy, and
  CPU/GPU runtime policy artifacts.
- Iteration 3: `ACCEPT`.
- Codex audit: agreed with rejected findings, patched this plan, and accepted
  the iteration-3 result.
