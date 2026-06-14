# DPF Non-LGSSM Cross-Implementation Matching Plan

metadata_date: 2026-06-06

## Question

For the non-LGSSM models now present in the BayesFilter high-dimensional and
student-baseline lanes, which small declared computations match across
BayesFilter, executable float64 FilterFlow, and the two student repositories?

This is common-sense consistency testing only.  No implementation is an oracle.
Agreement means two implementations evaluate the same declared computation on a
small fixture; it does not prove the filtering algorithm is scientifically
correct.

## Six-Step Execution Plan

1. Inventory the non-LGSSM model surfaces and identify only genuinely shared
   mathematical objects.
2. Promote stochastic volatility from `PREP_ONLY` to an executable density
   value/gradient tie-out between BayesFilter and float64 FilterFlow.
3. Record BayesFilter SIR and predator-prey first-gate model contracts as
   interface evidence, not cross-implementation equality evidence.
4. Re-run or validate the student nonlinear/range-bearing panel as
   comparison-only evidence, not as a BayesFilter/FilterFlow tie-out.
5. Classify each cell as `MATCHED`, `EXPLAINED_MISMATCH`,
   `INTERFACE_BLOCKED`, or `PREP_ONLY`; every mismatch must have a concrete
   mismatch class.
6. Review the plan and result with Claude, looping until convergence or a
   maximum of five review iterations.

## Evidence Contract

Primary question:

- can non-LGSSM implementations be tied out on shared small density/value and
  gradient computations, or can we explain why the available surfaces are not
  comparable?

Baseline/comparator:

- executable local float64 FilterFlow branch
  `.localsource/filterflow` for BayesFilter-vs-FilterFlow cells;
- quarantined student implementations under
  `experiments/student_dpf_baselines` for student comparison-only cells.

Primary pass criterion:

- every executed equality cell is `MATCHED` within declared tolerance, or is
  `EXPLAINED_MISMATCH` with a concrete mismatch class and evidence.

Veto diagnostics:

- nonfinite scalar or gradient in an executed equality cell;
- unclassified mismatch;
- using FilterFlow, BayesFilter, TT, paper tables, dense quadrature, or student
  repos as an oracle;
- comparing gradients across different parameterizations without applying the
  chain rule;
- comparing filtering paths across different proposals, particles, random
  numbers, resampling branches, or scalar objectives;
- mutating `.localsource/filterflow`;
- TensorFlow import before `CUDA_VISIBLE_DEVICES=-1` in CPU-only runs.

Explanatory diagnostics:

- density component deltas, parameter-gradient deltas, interface inventories,
  existing student panel status, finite-difference checks, and previous
  BayesFilter first-gate model contract results.

What will not be concluded even if the run passes:

- no filtering-algorithm correctness;
- no paper-scale reproduction;
- no TT correctness;
- no claim that FilterFlow, BayesFilter, or any student repo is scientifically
  correct;
- no HMC, DSGE, GPU, or production-readiness claim.

Planned artifacts:

- runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_nonlgssm_cross_implementation_matching_tf.py`;
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_nonlgssm_cross_implementation_matching_2026-06-06.json`;
- report:
  `experiments/dpf_implementation/reports/dpf-nonlgssm-cross-implementation-matching-2026-06-06.md`;
- result:
  `docs/plans/bayesfilter-dpf-nonlgssm-cross-implementation-matching-result-2026-06-06.md`;
- Claude ledger:
  `docs/plans/bayesfilter-dpf-nonlgssm-cross-implementation-matching-claude-review-ledger-2026-06-06.md`.

## Skeptical Plan Audit

Audit status: `PASS_WITH_GUARDRAILS`.

Wrong baseline risk:

- FilterFlow is not an oracle; the plan treats it as an executable comparator
  only.  Student repos are also comparison-only.

Proxy-metric risk:

- student RMSE/range-bearing panels are not promotion criteria for BayesFilter
  equality.  They are interface evidence only unless the same density contract
  is explicitly built.

Fair-comparison risk:

- stochastic volatility is comparable only at the density level in this slice:
  `x_t = gamma x_{t-1} + sigma eta_t`,
  `y_t | x_t ~ Normal(0, beta exp(x_t/2))`, with `mu=0` in FilterFlow.  The
  initial prior is not compared because FilterFlow's SV model surface exposes
  transition and observation models but no matching stationary initial density.

Gradient-risk:

- BayesFilter stores SV parameters as
  `(Phi^{-1}(gamma), log(beta))`; FilterFlow uses direct physical tensors
  `F` and observation Cholesky.  The equality cell must compare direct physical
  gradients `(d/dgamma, d/dbeta)` or explicitly apply the chain rule before
  comparing unconstrained BayesFilter gradients.

Hidden assumption risk:

- SIR and predator-prey are BayesFilter first-gate model contracts only in this
  slice.  No matching FilterFlow/student implementation was identified, so
  forcing an equality test would be misleading.

Stop conditions:

- stop after one executable non-LGSSM equality slice plus interface inventory;
  stop immediately on nonfinite/unclassified executed mismatch; stop the Claude
  loop after convergence or five iterations.

## Execution Cells

| Cell | Implementations | Object | Expected status |
|---|---|---|---|
| SV transition/observation density value and gradient | BayesFilter, FilterFlow | shared 1D SV density components, physical parameters `gamma`, `beta`, fixed particles | `MATCHED` if within tolerance |
| Student SV surface inventory | BayesFilter, student repos | parameterization and exposed log-density/filter APIs | `PREP_ONLY` or `INTERFACE_BLOCKED` |
| Student range-bearing nonlinear panel | student repos | existing shared range-bearing comparison panel | `PREP_ONLY` |
| Spatial SIR | BayesFilter, FilterFlow, student repos | comparable implementation inventory | `INTERFACE_BLOCKED` unless a same-model surface is found |
| Predator-prey | BayesFilter, FilterFlow, student repos | comparable implementation inventory | `INTERFACE_BLOCKED` unless a same-model surface is found |

## Planned Commands

Plan review:

```bash
bash scripts/claude_worker.sh --name nonlgssm_matching_plan_review "Review docs/plans/bayesfilter-dpf-nonlgssm-cross-implementation-matching-plan-2026-06-06.md for material blockers only."
```

Execution:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_nonlgssm_cross_implementation_matching_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_nonlgssm_cross_implementation_matching_tf --validate-only
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_nonlgssm_cross_implementation_matching_tf.py
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_nonlgssm_cross_implementation_matching_2026-06-06.json
git diff --check
```

Result review:

```bash
bash scripts/claude_worker.sh --name nonlgssm_matching_result_review "Review docs/plans/bayesfilter-dpf-nonlgssm-cross-implementation-matching-result-2026-06-06.md and the runner/JSON artifacts for material blockers only."
```
