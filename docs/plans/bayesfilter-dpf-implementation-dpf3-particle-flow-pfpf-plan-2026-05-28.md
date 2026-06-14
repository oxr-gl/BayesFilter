# Plan DPF3: Particle-Flow / PF-PF Proposal And Correction

## Date

2026-05-28

## Lane Boundaries

- Use DPF0-DPF1 outputs and DPF monograph/literature sources as authority.
- Student EDH/PFPF results are comparison-only and never source authority.
- Do not edit vendored student files and do not execute student code.
- Do not read or edit the high-dimensional nonlinear filtering lane.
- Do not edit production `bayesfilter/` code in this phase.

## Evidence Contract

Question: What particle-flow and PF-PF proposal/correction specification is
needed for a BayesFilter-owned DPF?

Baseline/comparator: DPF0 obligations, DPF1 classical PF baseline, DPF monograph
particle-flow/PF-PF derivations, affine-flow parity evidence, and controlled
range-bearing fixtures.

Primary criterion: proposal density, Jacobian correction, corrected log weights,
flow-step controls, finite checks, and affine parity tests are specified with
clear assumptions.

Veto diagnostics: missing Jacobian/proposal correction; nonlinear flow claims
from affine evidence; student flow code copied; kernel PFF included despite
exclusion pending debug.

Explanatory diagnostics: EDH/PFPF student panels and controlled baseline
same-regime proxy comparison.

What will not be concluded: no general nonlinear flow correctness, no HMC
validity, no production readiness, no universal flow-step policy.

## Exact Inputs

- `docs/plans/bayesfilter-dpf-implementation-dpf0-implementation-obligations-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf0-result-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf1-classical-pf-spec-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf1-result-2026-05-28.md`;
- `docs/chapters/ch19b_dpf_literature_survey.tex`;
- `docs/chapters/ch19c_dpf_implementation_literature.tex`;
- `docs/chapters/ch19d_dpf_hmc_dsge_macrofinance_assessment.tex`;
- `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`;
- `experiments/dpf_monograph_evidence/reports/affine-flow-pfpf-result.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-edh-pfpf-adapter-spike-result-2026-05-11.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-flow-dpf-readiness-review-result-2026-05-11.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-replicated-edh-pfpf-panel-result-2026-05-12.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-full-horizon-edh-pfpf-confirmation-result-2026-05-12.md`;
- `experiments/student_dpf_baselines/reports/student-dpf-baseline-full-horizon-edh-pfpf-sensitivity-result-2026-05-12.md`;
- `experiments/student_dpf_baselines/reports/advanced-particle-filter-kernel-pff-debug-gate-result-2026-05-11.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-smoke-result.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-fixed-grid-result.md`;
- `experiments/controlled_dpf_baseline/reports/controlled-dpf-baseline-comparison-audit.md`.

## Outputs

- `docs/plans/bayesfilter-dpf-implementation-dpf3-flow-pfpf-spec-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf3-excluded-flow-risk-register-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf3-kernel-pff-exclusion-check-2026-05-28.md`;
- `docs/plans/bayesfilter-dpf-implementation-dpf3-result-2026-05-28.md`.

## Skeptical Plan Audit Checklist

- Are proposal and target densities explicit?
- Is the Jacobian sign/convention audited?
- Are affine parity and nonlinear diagnostics separated?
- Are kernel PFF and stochastic-flow paths gated separately?
- Are student EDH/PFPF results comparison-only?
- Are production `bayesfilter/` files untouched?

## Execution Steps

1. Specify affine-flow parity obligations.
2. Specify PF-PF corrected-weight contract.
3. Specify range-bearing controlled fixture diagnostics.
4. Record excluded/deferred flow families.
5. Write result that keeps student EDH/PFPF rows comparison-only.

## Review Protocol

Claude Code Opus 4.7 max effort, read-only, `ACCEPT`/`REJECT`, max 5 iterations.

## Verification Commands

```bash
rg -n "excluded-flow-risk-register|kernel-pff-exclusion-check|kernel PFF remains excluded|Jacobian|proposal|corrected|affine|not concluded" docs/plans/bayesfilter-dpf-implementation-dpf3-*.md
git diff --check
git status --short --branch
```

## Stop Conditions

- corrected-weight formula cannot be traced or audited;
- flow implementation would require copied student code;
- nonlinear claims exceed controlled-fixture evidence;
- production `bayesfilter/` edits would be required.

## What Must Not Be Concluded

DPF3 does not establish a production nonlinear filtering method or posterior
target.  It specifies the flow/PF-PF contract.

## Review Record

- Claude Code reviewer: `claude-opus-4-7`, `--effort max`.
- Iteration 1: `REJECT`; required exact inputs, explicit student-comparison-only
  output/review language, and no production edits.
- Iteration 2: `REJECT`; required excluded-flow/kernel-PFF output artifacts and
  stronger verification of kernel-PFF exclusion.
- Iteration 3: `ACCEPT`.
- Codex audit: agreed with rejected findings, patched this plan, and accepted
  the iteration-3 result.
