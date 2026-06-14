# Plan: Filterflow Gap Closure For OT-DPF Audit

## Evidence Contract

Question: can we close the currently actionable filterflow gaps for the
Corenflos/JTT94 LGSSM audit by using the patched external filterflow checkout
as an executable reference, correcting the BayesFilter experimental
filterflow-style transport mirror, and rerunning the matched LGSSM comparison?

Primary external comparator: `.localsource/filterflow` branch
`bayesfilter-py311-compat`, based on upstream commit
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`.

Primary BayesFilter comparison target: experimental audit code under
`experiments/dpf_implementation/tf_tfp/`, not production `bayesfilter/`.

Primary criterion:

- filterflow remains executable under the local compatibility branch;
- the filterflow paper/code setting ledger is explicit, including the known
  covariance ambiguity between paper text and filterflow script settings;
- the BayesFilter audit-only filterflow-style transport mirror uses the
  component-audited semantics:
  - centered particles;
  - filterflow diameter times `sqrt(dimension)` scaling;
  - squared-distance cost divided by two;
  - epsilon annealing starts at coordinate range squared on the scaled cloud;
  - geometric annealing by `scaling^2`;
  - `transport_from_potentials` adds `logw` on the column axis;
  - row sums are near one and column sums are near `N * source_weight`;
- the matched LGSSM outer audit is rerun on the same observation path, theta
  grid, epsilon grid, particle count, ESS trigger, and Monte Carlo count.

Veto diagnostics:

- Claude Code plan/result review is unavailable;
- patched filterflow no longer executes;
- BayesFilter and filterflow Kalman values disagree on the same observation
  path;
- the corrected filterflow-style mirror emits non-finite particles, weights,
  or likelihoods;
- transport row/column residual semantics contradict the component audit;
- implementing the fix requires production `bayesfilter/`, `tests/`,
  monograph, vendored student, or high-dimensional-lane edits;
- required verification fails in a way that invalidates the evidence.

Explanatory diagnostics:

- filterflow branch, commit, diff summary, and package/runtime status;
- Section-5.1-style setting ledger and paper/code covariance ambiguity;
- Kalman alignment;
- PF-to-PF calibration;
- fixed-Sinkhorn results and residual vetoes;
- corrected filterflow-style annealed transport results;
- per-time log-likelihood error mean/std and deltas against filterflow;
- ESS, resampling counts, cost scales, transport residuals where available.

What will not be concluded:

- no production readiness;
- no public API readiness;
- no posterior correctness;
- no HMC readiness;
- no general nonlinear-SSM validity;
- no gradient/smoothness replication;
- no claim that finite relaxed OT is categorical PF;
- no claim that patched filterflow is untouched upstream code;
- no claim that the paper table is exactly reproduced unless the result
  explicitly reconciles the paper/code setting ambiguity.

## Inputs

- `AGENTS.md`
- `CLAUDE.md`
- `docs/plans/bayesfilter-dpf-filterflow-py311-compat-result-2026-05-30.md`
- `docs/plans/bayesfilter-dpf-filterflow-lgssm-matched-cross-audit-result-2026-05-30.md`
- `docs/plans/bayesfilter-dpf-filterflow-transport-component-audit-result-2026-05-30.md`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/plan.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/sinkhorn.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/utils.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_transport_component_audit_tf.py`

## Outputs

- `docs/plans/bayesfilter-dpf-filterflow-gap-closure-plan-2026-05-30.md`
- `docs/plans/bayesfilter-dpf-filterflow-gap-closure-result-2026-05-30.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_gap_closure_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-lgssm-gap-closure-2026-05-30.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_lgssm_gap_closure_2026-05-30.json`

The existing matched audit runner may be patched only to fix its experimental
filterflow-style mirror.  The new gap-closure runner must write separate
artifacts so earlier audit outputs remain historically interpretable.

## Allowed Write Set

- this plan and its result;
- the new gap-closure runner, report, and JSON output;
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
  for the narrow experimental mirror correction only.

## Forbidden Write Set

- production `bayesfilter/`;
- `tests/`;
- vendored student code;
- monograph chapters under `docs/chapters/`;
- high-dimensional nonlinear filtering lane files;
- `.localsource/filterflow` source files;
- unrelated dirty files.

## Skeptical Pre-Execution Audit

| Risk | Status | Mitigation |
| --- | --- | --- |
| stale context | pass | Use the latest component audit result, not the older blocked filterflow audit. |
| wrong comparator | pass | Comparator is executable patched filterflow, not BayesFilter itself. |
| value-only overclaim | pass | Likelihood reproduction does not prove gradient/smoothness. |
| arbitrary threshold | pass | The match band is filterflow Monte Carlo sample SD for this reproduction audit only. |
| transport-axis drift | pass | Patch follows the component-audited column-axis `logw` semantics. |
| epsilon semantics drift | pass | Patch follows filterflow coordinate-range epsilon start and `scaling^2` annealing. |
| hidden production drift | pass | Forbidden write set excludes production and tests. |
| monograph/highdim drift | pass | Forbidden write set excludes chapters and high-dimensional lane. |
| vendored contamination | pass | Student/vendored code is not used. |
| artifact answers question | pass | Outputs separately record plan, fixed runner, outer audit JSON/report, and result note. |

## Execution Steps

1. Review this plan with Claude Code.
2. Patch only the experimental BayesFilter filterflow-style mirror:
   - add `logw` on the column axis in `transport_from_potentials`;
   - use coordinate-range squared on the scaled cloud for epsilon start;
   - make the batched annealing loop follow filterflow's `reduce_all`
     continuation semantics;
   - correct row/column residual labels.
3. Add a gap-closure runner that reuses the matched-audit machinery but writes
   separate gap-closure JSON/report artifacts.
4. Rerun the matched LGSSM audit.
5. Write the result artifact with a decision table:
   - filterflow executable status;
   - paper/code settings ledger status;
   - Kalman alignment status;
   - PF calibration status;
   - corrected filterflow-style outer audit status;
   - fixed-Sinkhorn small-epsilon status;
   - gradient/smoothness replication status.
6. Review the result with Claude Code and patch agreed findings.
7. Run verification.

## Claude Review Protocol

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Claude must return `ACCEPT` or `REJECT` with findings.  Codex audits Claude's
findings.  If rejected and Codex agrees, patch and resubmit.  Loop until
`ACCEPT` or max five iterations.  On iteration five, accept only for user
inspection unless there is a major blocker.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_gap_closure_tf.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_transport_component_audit_tf --validate-only
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_gap_closure_tf
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_gap_closure_tf --validate-only
```

```bash
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_lgssm_gap_closure_2026-05-30.json >/dev/null
```

```bash
rg -n "import numpy|from numpy|student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_gap_closure_tf.py
```

```bash
rg -n "[ \t]+$" docs/plans/bayesfilter-dpf-filterflow-gap-closure-plan-2026-05-30.md docs/plans/bayesfilter-dpf-filterflow-gap-closure-result-2026-05-30.md experiments/dpf_implementation/reports/dpf-filterflow-lgssm-gap-closure-2026-05-30.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_gap_closure_tf.py
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

## Stop Conditions

- Claude review finds a major blocker that Codex agrees with;
- exact Claude command/model/effort is unavailable;
- filterflow compatibility branch cannot execute;
- corrected mirror requires production edits;
- Kalman alignment fails;
- JSON/report validation fails;
- unauthorized production, tests, monograph, vendored, or high-dimensional-lane
  edits would be needed.
