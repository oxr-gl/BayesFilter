# Plan: Filterflow Final Gaps Closure For OT-DPF Audit

## Evidence Contract

Question: can we close, or convert into precise blockers, the three remaining
filterflow audit gaps after the executable LGSSM transport match?

The three gaps are:

1. exact Corenflos Section 5.1 paper/code settings reconciliation;
2. filterflow smoothness and gradient-field replication on the supplement
   linear-Gaussian experiment;
3. BayesFilter fixed-target Sinkhorn epsilon `0.25` residual diagnosis.

Primary sources and comparators:

- Corenflos et al. paper text and supplement under
  `.localsource/dpf_ot_audit/`;
- executable patched external filterflow branch `bayesfilter-py311-compat`,
  upstream base `5d8300ba247c4c17e1a301a22560c24fd0670bfe`;
- BayesFilter experimental audit code under
  `experiments/dpf_implementation/tf_tfp/`.

Primary criteria:

- the paper/code ledger records which Section 5.1 settings agree exactly,
  which settings differ, and whether the executable code or paper text is used
  for each replicated result;
- the smoothness run executes a bounded CPU-only filterflow reproduction with
  finite log-likelihoods and finite GradientTape gradients for the regularized
  transform, plus Kalman finite-difference gradient diagnostics on the same
  mesh and observation path;
- the fixed-target Sinkhorn diagnosis determines whether the epsilon `0.25`
  residual veto is explained by iteration budget, fixed-epsilon formulation, or
  an unresolved numerical/stability gap.

Veto diagnostics:

- Claude Code plan/result review is unavailable;
- patched filterflow cannot execute in the local isolated environment;
- paper/code settings are silently merged into one claim;
- value-only likelihood evidence is promoted to gradient evidence;
- smoothness gradients are non-finite without a localized structured blocker;
- fixed-target Sinkhorn diagnosis changes BayesFilter default behavior instead
  of recording an experimental diagnosis;
- new BayesFilter-owned differentiable code imports NumPy as an implementation
  backend;
- implementation requires production `bayesfilter/`, `tests/`, monograph,
  high-dimensional lane, DSGE/NAWM, or vendored student edits.

Explanatory diagnostics:

- paper/supplement anchors inspected;
- filterflow script anchors inspected;
- filterflow branch, commit, diff summary, Python/TensorFlow/NumPy versions;
- Section 5.1 table values and executable-code values where available;
- smoothness likelihood RMSE/rank correlation and gradient RMSE/cosine against
  Kalman finite-difference diagnostics;
- fixed-target Sinkhorn residual by iteration budget, epsilon, theta, and
  resampling state summary.

What will not be concluded:

- no production readiness;
- no public API readiness;
- no posterior correctness;
- no HMC readiness;
- no general nonlinear-SSM validity;
- no claim that CUT4, LEDH-PF-PF, or structural-SSM evidence is improved;
- no claim that patched filterflow is untouched upstream code;
- no claim that a bounded smoothness run reproduces every figure/table in the
  paper;
- no claim that fixed-target Sinkhorn is paper-equivalent if the annealed
  filterflow transport is the matched object.

## Inputs

- `AGENTS.md`
- `CLAUDE.md`
- `/home/chakwong/.codex/skills/scholarly-literature-audit/SKILL.md`
- `/home/chakwong/python/claudecodex/policies/scholarly-literature-audit-policy.md`
- `docs/plans/bayesfilter-dpf-filterflow-gap-closure-result-2026-05-30.md`
- `.localsource/dpf_ot_audit/corenflos2021_differentiable_particle_filtering_eot.txt`
- `.localsource/dpf_ot_audit/corenflos2021_differentiable_particle_filtering_eot_supp.txt`
- `.localsource/filterflow/scripts/simple_linear_comparison.py`
- `.localsource/filterflow/scripts/simple_linear_smoothness.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/plan.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/sinkhorn.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/utils.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/common_tf.py`

## Outputs

- `docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-plan-2026-05-30.md`
- `docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-result-2026-05-30.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_final_gaps_closure_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-final-gaps-closure-2026-05-30.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_final_gaps_closure_2026-05-30.json`

## Allowed Write Set

- this plan and its result;
- the new final-gaps runner, report, and JSON output.

## Forbidden Write Set

- production `bayesfilter/`;
- `tests/`;
- monograph chapters under `docs/chapters/`;
- high-dimensional nonlinear filtering lane artifacts;
- DSGE/NAWM-specific code or validation artifacts;
- vendored student code;
- `.localsource/filterflow` source code;
- unrelated dirty files.

## Skeptical Pre-Execution Audit

| Risk | Status | Mitigation |
| --- | --- | --- |
| stale context | pass | Build on the accepted gap-closure result, not the older failed fixed-Sinkhorn interpretation. |
| wrong comparator | pass | Use patched executable filterflow and inspected paper/supplement text as separate comparators. |
| paper/code conflation | pass | Record paper text settings separately from executable script settings. |
| value-only overclaim | pass | Smoothness gradients are a separate gate; likelihood table reproduction cannot close gradient evidence. |
| blocker semantics | pass | A localized smoothness-gradient failure may close the gap only as a structured blocker, not as validation. |
| arbitrary thresholds | pass | Use finite/non-finite vetoes plus descriptive gradient diagnostics, not promotion thresholds. |
| fixed-Sinkhorn overpatch | pass | Diagnose iteration/formulation behavior; do not promote fixed-target Sinkhorn as paper-equivalent. |
| hidden production drift | pass | Forbidden write set excludes production and tests. |
| monograph/highdim drift | pass | Forbidden write set excludes chapters and high-dimensional lane. |
| vendored contamination | pass | Student/vendored code is not used or edited. |
| artifact answers question | pass | Output JSON/report contain separate ledgers for the three named gaps. |

## Execution Steps

1. Review this plan with Claude Code.
2. Implement a bounded final-gaps runner that:
   - records paper and supplement anchors;
   - records filterflow code anchors and executable branch status;
   - runs a CPU-only filterflow smoothness subprocess on a small mesh;
   - computes Kalman finite-difference smoothness diagnostics on the same mesh;
   - computes regularized-transform GradientTape diagnostics from filterflow;
   - reruns fixed-target Sinkhorn residual probes at epsilon `0.25` over a
     bounded iteration-budget ladder on the matched LGSSM state stream.
   The fixed-target Sinkhorn ladder is capped at budgets
   `25, 50, 100, 200, 500, 1000` and stops early only if every probed state has
   residual at or below `1e-5`.  Residual improvement is diagnostic only and
   must not be reinterpreted as paper-equivalence.
3. Write JSON and Markdown report artifacts.
4. Validate the JSON/report and rerun the runner in validate-only mode.
5. Write the result artifact with a decision table for all three gaps.
6. Review the result with Claude Code and patch agreed findings.
7. Run final verification.

## Claude Review Protocol

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Run Claude Code with elevated/trusted permissions per `AGENTS.md`, and provide
the bounded review prompt either as stdin or as the command prompt argument.
Claude must return `ACCEPT` or `REJECT` with findings.  Codex audits Claude's
findings.  If rejected and Codex agrees, patch and resubmit.  Loop until
`ACCEPT` or max five iterations.  On iteration five, accept only for user
inspection unless there is a major blocker.  Record the exact review command
and iteration status in the result artifact.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_final_gaps_closure_tf.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_final_gaps_closure_tf
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_final_gaps_closure_tf --validate-only
```

```bash
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_final_gaps_closure_2026-05-30.json >/dev/null
```

```bash
rg -n "import numpy|from numpy|student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_final_gaps_closure_tf.py
```

```bash
rg -n "[ \t]+$" docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-plan-2026-05-30.md docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-result-2026-05-30.md experiments/dpf_implementation/reports/dpf-filterflow-final-gaps-closure-2026-05-30.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_final_gaps_closure_tf.py
```

```bash
git diff --check
```

```bash
git status --short -- bayesfilter tests docs/chapters
```

```bash
git status --short -- docs/chapters .localsource/filterflow third_party experiments/controlled_dpf_baseline
```

```bash
git status --short -- docs/plans | rg -n "highdim|NAWM|DSGE|student|controlled_dpf" || true
```

```bash
git status --short --branch
```

## Stop Conditions

- exact Claude command/model/effort is unavailable;
- filterflow isolated environment is unavailable;
- smoothness subprocess cannot import patched filterflow;
- smoothness gradients are non-finite and cannot be localized to a structured
  blocker, or are overclaimed as validation despite the blocker;
- fixed-target Sinkhorn diagnosis would require changing production or default
  behavior;
- fixed-target Sinkhorn diagnosis exceeds the capped budget ladder or becomes a
  tuning sweep;
- required verification fails in a way that invalidates the evidence;
- unauthorized production, tests, monograph, vendored, high-dimensional, or
  DSGE/NAWM edits would be needed.
