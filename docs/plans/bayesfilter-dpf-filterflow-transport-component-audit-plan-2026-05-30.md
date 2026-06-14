# Plan: Filterflow Transport Component Audit

## Evidence Contract

Question: why did the BayesFilter audit-only `filterflow-style` annealed
transport lane fail the matched LGSSM audit even though filterflow itself runs
and the BayesFilter fixed-Sinkhorn lane agrees for the easier epsilon rows?

Primary comparator: the external patched filterflow branch
`.localsource/filterflow` at upstream base commit
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`, using
`filterflow.resampling.differentiable.regularized_transport.plan.transport`
on one frozen LGSSM particle/log-weight state.

Primary criterion: a BayesFilter-side TensorFlow reconstruction of the
filterflow transport operator must match the filterflow transport matrix,
transported particles, row sums, column sums, epsilon-start value, and Sinkhorn
iteration count to numerical tolerance when the same particles, normalized log
weights, epsilon, scaling, threshold, and max iteration budget are used.

Veto diagnostics:

- filterflow external environment cannot execute;
- the frozen state is not an actual LGSSM resampling state with ESS below the
  threshold;
- the exact formula reconstruction does not match filterflow;
- row/column transport semantics do not satisfy filterflow's own tests:
  row sums near one and column sums near `N * weights`;
- non-finite transport matrix, transported particles, or potentials;
- hidden edits to production `bayesfilter/`, `tests/`, monograph chapters,
  vendored student code, or high-dimensional-lane files.

Explanatory diagnostics:

- matrix max/RMSE difference for each candidate variant;
- transported-particle max/RMSE difference;
- row-sum and column-sum residuals;
- potential max/RMSE difference;
- epsilon start under candidate interpretations;
- cost scale, ESS, time index, theta, epsilon, scaling, threshold, and dtype.

What will not be concluded:

- no production readiness;
- no public API readiness;
- no HMC readiness;
- no posterior correctness;
- no general nonlinear-SSM validity;
- no claim that finite relaxed OT is categorical PF;
- no claim that patched filterflow is upstream-clean;
- no claim that the BayesFilter outer audit runner is fixed unless a separate
  matched audit rerun is executed.

## Inputs

- `docs/plans/bayesfilter-dpf-filterflow-lgssm-matched-cross-audit-result-2026-05-30.md`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/plan.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/sinkhorn.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/utils.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/biased.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`

## Outputs

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_transport_component_audit_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-transport-component-audit-2026-05-30.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_transport_component_audit_2026-05-30.json`
- `docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-result-2026-05-30.md`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-plan-2026-05-30.md`
- `docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-result-2026-05-30.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_transport_component_audit_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-transport-component-audit-2026-05-30.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_transport_component_audit_2026-05-30.json`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane files;
- vendored student code;
- `.localsource/filterflow`, except for read-only execution of the already
  patched local branch.

## Skeptical Pre-Execution Audit

- Stale context: use the newer matched audit result, not the older blocked
  filterflow audit result.
- Wrong baseline: compare directly to filterflow `transport`, not to an
  inferred likelihood table.
- Wrong state: freeze an actual LGSSM state whose ESS triggers resampling.
- Wrong epsilon semantics: separately test filterflow's coordinate-range
  epsilon schedule and the BayesFilter audit-only max-cost schedule.
- Wrong transport orientation: separately test the axis where `logw` is added.
- Proxy overclaim: a component match does not prove the full outer filter.
- Hidden drift: do not edit production code, monograph chapters, vendored code,
  or high-dimensional-lane artifacts.
- Artifact fit: the JSON/report must show which formula variant matches or
  fails and why.

Audit status before execution: passed with the caveat that algorithmic random
streams remain filterflow-local.  The comparison uses one frozen component
state and is not a likelihood-level rerun.

## Candidate Variants

The runner must compare at least:

- `legacy_axis_row_epsilon0_max_cost`: mirrors the failed BayesFilter audit-only
  transport formula from the matched audit runner.
- `axis_column_epsilon0_max_cost`: fixes only the log-weight axis.
- `axis_row_epsilon0_filterflow_range`: fixes only the annealing start scale.
- `axis_column_epsilon0_filterflow_range`: reconstructs filterflow's formula.

## Stop Conditions

- Stop if Claude Code is unavailable for plan/result review.
- Stop if `.localenv/filterflow-py311/bin/python` is missing.
- Stop if filterflow cannot import or execute the component call.
- Stop if no LGSSM resampling-trigger state is found.
- Stop if the exact formula reconstruction fails to match filterflow, because
  then the audit implementation itself is suspect.
- Stop if verification indicates unauthorized production, tests, monograph,
  vendored, or high-dimensional-lane edits.

## Claude Review Protocol

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Claude reviews read-only and returns `ACCEPT` or `REJECT` with findings.  Codex
audits Claude's findings.  If rejected and Codex agrees, patch and resubmit.
Loop until `ACCEPT` or five iterations.  On iteration five, accept only for user
inspection unless there is a major blocker.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_transport_component_audit_tf.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_transport_component_audit_tf
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_transport_component_audit_tf --validate-only
```

```bash
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_transport_component_audit_2026-05-30.json >/dev/null
```

```bash
rg -n "import numpy|from numpy|student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_transport_component_audit_tf.py
```

```bash
rg -n "[ \t]+$" docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-plan-2026-05-30.md docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-result-2026-05-30.md experiments/dpf_implementation/reports/dpf-filterflow-transport-component-audit-2026-05-30.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_transport_component_audit_tf.py
```

```bash
git diff --check
```

```bash
git status --short -- bayesfilter tests docs/chapters
```

```bash
git status --short --branch
```
