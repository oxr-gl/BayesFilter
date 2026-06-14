# Plan: Filterflow Gap-Closure Program For BayesFilter OT-DPF

## Decision

`PLAN_READY_FOR_CLAUDE_REVIEW`

## Evidence Contract

Question: can the six remaining gaps from the reviewed BayesFilter
TF/TFP OT-DPF versus Corenflos/JTT94 `filterflow` comparison be closed or
converted into narrower reviewed risks without changing production code,
monograph chapters, high-dimensional lane files, vendored student code, or
external `filterflow` source?

Primary external comparator: patched local `filterflow` branch
`bayesfilter-py311-compat`, upstream base commit
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`.

Primary BayesFilter implementation lane: experimental TF/TFP code under
`experiments/dpf_implementation/tf_tfp/`.

Primary criteria:

- fixed-target Sinkhorn is only computed where ESS actually triggers
  resampling in the experimental matched-audit filter path;
- unconditional fixed-target Sinkhorn remains available only as a separately
  labelled component diagnostic;
- filterflow-style annealed regularized transport remains matched to
  `filterflow` RegularisedTransform across all nine epsilon/theta cells;
- matched LEDH-PF-PF-OT uses the exact filterflow observation path, executable
  `I_2` covariance convention, `T=150`, `N=25`, theta grid
  `0.25, 0.5, 0.75`, and reports the same per-time log-likelihood-error
  scalar against Kalman, while not being required to equal filterflow because
  it is a different proposal;
- smoothness/gradient evidence reconciles or explicitly records scalar
  normalization and scale gaps, and never treats finite gradients alone as
  gradient correctness;
- the patched filterflow reference environment and the `0.5 I_2` versus `I_2`
  covariance ambiguity are permanently recorded in the result.

Veto diagnostics:

- exact Claude review command/model/effort is unavailable;
- fixed-target Sinkhorn still vetoes non-triggered rows in the matched filter
  path after the gating patch;
- the filterflow-style annealed transport mirror stops matching filterflow;
- Kalman alignment fails on the matched observation path;
- LEDH matched runner emits non-finite PF-PF corrected weights, log dets,
  likelihood proxy, or ESS;
- gradient/smoothness result is overclaimed as agreement without resolving the
  scalar/scale contract;
- new BayesFilter-owned algorithmic code imports NumPy as implementation
  backend;
- implementation would require production `bayesfilter/`, `tests/`, monograph,
  high-dimensional lane, vendored student, external macro-model, or
  `.localsource/filterflow` source edits.

Explanatory diagnostics:

- filterflow branch, commit, diff summary, Python version, TensorFlow version,
  NumPy version inside the external subprocess, command, CPU-only manifest;
- exact filterflow smoke status;
- covariance ambiguity ledger;
- ESS trigger counts and skipped fixed-Sinkhorn row counts;
- unconditional fixed-Sinkhorn residual ladder retained as component diagnostic;
- PF, filterflow-style OT, fixed-target OT, and LEDH-PF-PF-OT per-time
  likelihood-error tables;
- LEDH PF-PF corrected weight ranges, log-det ranges, ESS ranges, Sinkhorn
  residuals, and proposal-density accounting;
- gradient/smoothness scalar-normalization ledger and finite-gradient
  diagnostics.

What will not be concluded:

- no production readiness;
- no public API readiness;
- no posterior correctness;
- no HMC readiness;
- no general nonlinear-SSM validity;
- no DSGE/NAWM validation;
- no banking/model-risk claim;
- no monograph claim;
- no claim that patched `filterflow` is pristine upstream source;
- no claim that fixed-target Sinkhorn is filterflow-equivalent unless a future
  derivation and verification prove that statement;
- no claim that finite gradients alone establish gradient correctness.

## Inputs

- `AGENTS.md`
- `CLAUDE.md`
- `docs/plans/bayesfilter-dpf-filterflow-full-comparison-plan-2026-05-31.md`
- `docs/plans/bayesfilter-dpf-filterflow-full-comparison-result-2026-05-31.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_final_gaps_closure_tf.py`
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/flows/ledh_tf.py`
- `experiments/dpf_implementation/tf_tfp/flows/jacobians_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_ledh_pfpf_ot_tf.py`
- `.localsource/filterflow/scripts/simple_linear_comparison.py`
- `.localsource/filterflow/scripts/simple_linear_smoothness.py`

## Outputs

- `docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-plan-2026-05-31.md`
- `docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-result-2026-05-31.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_gap_closure_program_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_matched_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_gradient_audit_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-gap-closure-program-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-matched-ledh-pfpf-ot-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-smoothness-gradient-audit-2026-05-31.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_gap_closure_program_2026-05-31.json`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_matched_ledh_pfpf_ot_2026-05-31.json`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_smoothness_gradient_audit_2026-05-31.json`

## Allowed Write Set

- the output artifacts listed above;
- narrow edits to
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
  to gate fixed-target Sinkhorn by ESS in the experimental audit path only.

## Forbidden Write Set

- production `bayesfilter/`;
- `tests/`;
- monograph chapters under `docs/chapters/`;
- high-dimensional nonlinear filtering lane files;
- DSGE/NAWM-specific code or validation artifacts;
- vendored student code;
- `.localsource/filterflow` source files;
- unrelated dirty files.

## Phase Order

1. Review this plan with Claude Code.
2. Patch fixed-target Sinkhorn ESS gating in the experimental matched-audit
   runner:
   - compute fixed Sinkhorn only on batch rows where `ESS <= 0.5 N`;
   - preserve particles and weights unchanged where no resampling triggers;
   - record skipped non-triggered row counts and no-resampling status;
   - keep unconditional component diagnostics in the final-gaps runner.
3. Create the matched LEDH-PF-PF-OT runner:
   - recover the exact filterflow observation path;
   - use executable `I_2` covariance convention;
   - run theta grid `0.25, 0.5, 0.75` and epsilon grid where applicable;
   - include bounded LEDH diagnostics over all theta/epsilon cells and a
     reviewed bounded realization count if the full 100-realization LEDH path
     is too expensive;
   - report why LEDH is compared diagnostically rather than required to match
     filterflow.
4. Create the smoothness/gradient audit runner:
   - recover supplement settings from filterflow code;
   - record total, per-time, negative, and normalized scalar variants where
     feasible;
   - compare filterflow gradient, Kalman finite-difference, and analytic
     Kalman-gradient diagnostics if feasible;
   - record BayesFilter gradient availability or structured blocker.
5. Create the gap-closure program runner:
   - run the patched full comparison;
   - run matched LEDH diagnostics;
   - run smoothness/gradient audit;
   - record filterflow environment freeze and covariance ambiguity ledger;
   - write JSON and Markdown reports.
6. Run verification commands.
7. Write the result artifact.
8. Review the result with Claude Code and patch agreed findings.

## Skeptical Pre-Execution Audit

| Risk | Status | Mitigation |
| --- | --- | --- |
| stale context | pass | Read the reviewed full-comparison plan/result and current audit runners. |
| wrong comparator | pass | Primary comparator remains patched executable filterflow, not student code or paper table alone. |
| paper/code covariance ambiguity hidden | pass | The plan requires a permanent ledger and uses executable `I_2` for code comparisons. |
| fixed-target overclaim | pass | Fixed-target Sinkhorn remains a diagnostic branch and is not paper-equivalent. |
| filterflow-style path regression | watch | The plan requires preserving and rerunning the already-matched annealed transport mirror. |
| LEDH overclaim | pass | LEDH is a different proposal and is not required to equal filterflow. |
| gradient overclaim | pass | Finite gradients are smoke evidence only unless scalar/scale agreement is reconciled. |
| missing stop conditions | pass | Stop conditions are listed below. |
| hidden production drift | pass | Production and tests are forbidden. |
| monograph/highdim drift | pass | Monograph chapters and high-dimensional lane files are forbidden. |
| vendored contamination | pass | Student/vendored code is not used or edited. |
| artifact answers question | pass | Outputs directly address the six named gaps. |

## Stop Conditions

- Claude review command/model/effort unavailable;
- fixed-target gating requires production or shared API edits;
- filterflow compatibility environment cannot execute even a smoke command;
- Kalman reference mismatch on the matched observation path;
- filterflow-style annealed transport no longer matches filterflow across all
  nine cells;
- LEDH matched diagnostics are non-finite in a way that invalidates the
  proposal-density/accounting evidence;
- gradient/smoothness audit cannot identify the scalar being compared and
  would invite overclaim;
- NumPy is required as BayesFilter implementation backend;
- required verification fails in a way that invalidates the evidence;
- unauthorized production, test, monograph, highdim, vendored, external
  macro-model, or `.localsource/filterflow` source edits would be needed.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_gap_closure_program_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_matched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_gradient_audit_tf.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_lgssm_matched_cross_audit_tf
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_matched_ledh_pfpf_ot_tf
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_smoothness_gradient_audit_tf
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_gap_closure_program_tf
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_gap_closure_program_tf --validate-only
```

```bash
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_gap_closure_program_2026-05-31.json >/dev/null
```

```bash
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_gap_closure_program_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_matched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_gradient_audit_tf.py
```

```bash
rg -n "student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_gap_closure_program_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_matched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_gradient_audit_tf.py
```

```bash
rg -n "[ \t]+$" docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-plan-2026-05-31.md docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-result-2026-05-31.md experiments/dpf_implementation/reports/dpf-filterflow-gap-closure-program-2026-05-31.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_gap_closure_program_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_matched_ledh_pfpf_ot_tf.py experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_gradient_audit_tf.py
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

## Claude Review Protocol

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Run Claude Code with elevated/trusted permissions per `AGENTS.md`.  Claude
must review read-only and return `ACCEPT` or `REJECT` first, followed by
findings.  Codex audits Claude's findings.  If rejected and Codex agrees,
patch and resubmit.  Loop until `ACCEPT` or max five iterations.  On iteration
five, accept only for user inspection unless there is a major blocker.

Review this plan before execution and review the final result after execution
using the same loop.

