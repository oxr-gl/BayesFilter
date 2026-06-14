# Plan: Filterflow LGSSM Matched Cross-Audit Rerun

## Decision

`PLAN_READY_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: after patching the external filterflow checkout for Python 3.11,
does BayesFilter's experimental TF/TFP OT-DPF reproduce filterflow's
Section-5.1-style LGSSM likelihood-error behavior when the comparison uses the
same fixed observation path, theta grid, time horizon, particle count, Neff
resampling threshold, epsilon values, and cost-scaling convention?

Primary external comparator: `.localsource/filterflow` branch
`bayesfilter-py311-compat`, based on upstream commit
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`.

Primary BayesFilter comparators:

- `bayesfilter_pf`: bootstrap PF calibration lane;
- `bayesfilter_scaled_fixed_sinkhorn_ess`: current finite Sinkhorn relaxed OT
  lane with filterflow-style centered/diameter-scaled cost but fixed target
  epsilon;
- `bayesfilter_filterflow_style_transport_ess`: experimental TF lane in the
  audit runner that mirrors filterflow's centered/diameter scaling, epsilon
  annealing, potential-update stopping, and transport-matrix application.

Primary criterion: compare `(estimated log likelihood - exact Kalman log
likelihood) / T` means and standard deviations over 100 filter realizations.
Classify each BayesFilter lane against the executable filterflow lane, not only
against the paper table.  A lane is `matched_within_filterflow_mc_band` only if
all three theta cells differ from the corresponding filterflow mean by no more
than one filterflow sample standard deviation and has no sign/order/scale
inversion.  This is a reproduction-audit band, not a universal correctness
threshold.

Veto diagnostics:

- filterflow no longer executes on the patched branch;
- the comparison does not use the same fixed observation path;
- Kalman likelihood in BayesFilter and filterflow differs materially on the
  same observations;
- BayesFilter row is non-finite;
- current fixed Sinkhorn lane hits Sinkhorn residual vetoes;
- filterflow-style transport implementation changes BayesFilter production
  code or imports filterflow as implementation logic;
- unauthorized edits to production `bayesfilter/`, `tests/`, vendored code,
  monograph chapters, or high-dimensional lane files.

Explanatory diagnostics: filterflow commit/branch/diff summary, package
versions, exact commands, Kalman values, per-time likelihood errors,
resampling counts, ESS summaries, Sinkhorn residuals, transport row/column-sum
diagnostics, cost scales, epsilon schedule, and runtime.

What will not be concluded: no production readiness, no public API readiness,
no posterior correctness, no HMC readiness, no general nonlinear-SSM validity,
no claim that finite relaxed OT is categorical PF, and no claim that the local
patched filterflow branch is untouched upstream code.

## Allowed Write Set

- this plan;
- `docs/plans/bayesfilter-dpf-filterflow-lgssm-matched-cross-audit-result-2026-05-30.md`;
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`;
- `experiments/dpf_implementation/reports/dpf-filterflow-lgssm-matched-cross-audit-2026-05-30.md`;
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_lgssm_matched_cross_audit_2026-05-30.json`.

## Forbidden Write Set

- production `bayesfilter/`;
- `tests/`;
- vendored student code;
- monograph chapters under `docs/chapters/`;
- high-dimensional nonlinear filtering lane files;
- `.localsource/filterflow` source files beyond the already-reviewed
  compatibility patch;
- unrelated dirty files.

## Method

1. Verify `.localsource/filterflow` is on branch `bayesfilter-py311-compat` and
   record its diff summary against upstream.
2. Use `.localenv/filterflow-py311/bin/python` in a subprocess to run
   filterflow's `simple_linear_comparison.py` logic without editing filterflow:
   recover the fixed observation path, initial particle cloud, exact Kalman
   table, PF table, and RegularisedTransform tables for epsilons `0.25`,
   `0.5`, and `0.75`.
3. Implement a new experimental runner under
   `experiments/dpf_implementation/tf_tfp/runners/` that:
   - sets `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import;
   - consumes the filterflow observation path and initial particles;
   - computes exact Kalman log likelihood in TF for the same observations;
   - runs BayesFilter PF and OT lanes over 100 filter realizations;
   - reports the same per-time error scalar as filterflow;
   - keeps filterflow source as external comparator only.
4. Add the filterflow-style transport lane only inside the audit runner:
   - centered particles;
   - diameter times `sqrt(dimension)` scaling;
   - squared-distance cost divided by 2;
   - epsilon initialized at `max_min(scaled_x)^2`;
   - geometric annealing by `scaling^2` to target epsilon;
   - potential update threshold `1e-3`;
   - transport matrix applied to original particles;
   - uniform weights after flagged resampling.
5. Write JSON and report artifacts with comparator tables, discrepancy ledger,
   and non-implications.

## Skeptical Pre-Execution Audit

| Risk | Status | Mitigation |
| --- | --- | --- |
| stale context | pass | Read current filterflow compat result, cross-audit result, filterflow source, and BayesFilter runner. |
| wrong comparator | pass | Primary comparator is now executable patched filterflow, not the old blocked result. |
| wrong data protocol | watch | Use one fixed filterflow observation path; 100 Monte Carlo filter realizations. |
| cost/epsilon mismatch | watch | Current fixed Sinkhorn and filterflow-style annealed transport are separate labelled lanes. |
| proxy overclaim | pass | Likelihood-error table is reproduction evidence only. |
| hidden production drift | pass | Forbidden write set excludes production and tests. |
| monograph/highdim drift | pass | Forbidden write set excludes chapter and highdim files. |
| vendored contamination | pass | Student code not used. |
| artifact answers question | pass | Outputs directly compare executable filterflow rows to BayesFilter rows. |

## Claude Review Protocol

Review this plan and the final result with:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Claude must return `ACCEPT` or `REJECT` with findings.  Codex audits Claude's
findings.  If rejected and Codex agrees, patch and resubmit.  Loop until
`ACCEPT` or max five iterations.

## Verification Commands

- `git -C .localsource/filterflow status --short --branch`
- `git -C .localsource/filterflow rev-parse HEAD`
- filterflow subprocess command recorded in JSON;
- `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_matched_cross_audit_tf`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_matched_cross_audit_tf --validate-only`
- `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_lgssm_matched_cross_audit_2026-05-30.json`
- `rg -n "student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
- `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
- lane-scoped trailing whitespace check;
- `git diff --check`;
- `git status --short -- bayesfilter tests docs/chapters`;
- `git status --short --branch`.

## Stop Conditions

- Claude review finds a major blocker that Codex agrees with;
- patched filterflow cannot execute;
- filterflow observation path cannot be recovered;
- BayesFilter Kalman and filterflow Kalman disagree materially on the same
  observation path;
- implementing the filterflow-style lane would require production code edits;
- required verification fails in a way that invalidates the comparison.
