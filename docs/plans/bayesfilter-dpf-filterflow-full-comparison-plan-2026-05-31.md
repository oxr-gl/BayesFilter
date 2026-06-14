# Plan: Filterflow Full Comparison For BayesFilter OT-DPF

## Decision

`PLAN_READY_FOR_CLAUDE_REVIEW`

## Scope

This plan defines the full comparison of BayesFilter experimental TF/TFP
OT-DPF lanes against the established local Corenflos/JTT94 `filterflow`
reference for the LGSSM setting associated with Corenflos et al. Section 5.1.

This is a BayesFilter-owned DPF implementation/evidence-lane plan only.  It
does not execute the comparison yet.  Execution requires this plan to pass the
Claude Code review loop below.

## Evidence Contract

Question: when calibrated to the same LGSSM, observation path, transition
covariance convention, time horizon, particle count, seed protocol,
resampling trigger, cost scaling, epsilon schedule, and output scalar, do the
BayesFilter experimental TF/TFP OT-DPF lanes reproduce the qualitative and
quantitative behavior of the patched executable `filterflow` implementation?

Primary external comparator: `.localsource/filterflow` branch
`bayesfilter-py311-compat`, upstream base commit
`5d8300ba247c4c17e1a301a22560c24fd0670bfe`.  The local checkout is patched
for Python 3.11 compatibility and is not pristine upstream source.

Primary literature context: Corenflos et al. main paper Section 5.1 and
Table 1, plus the supplement smoothness/gradient experiment.  The paper and
supplement state transition covariance `0.5 I_2`, while executable
`filterflow` uses `I_2`; prior bounded reruns showed the published Table 1
scale is consistent with executable `I_2`.  The comparison therefore uses the
executable `I_2` convention and records the paper text as a likely typo or
notation mismatch, not as a silent override.

Primary BayesFilter comparators:

- `bayesfilter_pf`: TF/TFP bootstrap PF baseline;
- `bayesfilter_filterflow_style_transport`: TF/TFP audit mirror of
  filterflow's annealed regularized transport semantics;
- `bayesfilter_fixed_target_sinkhorn`: existing finite fixed-target Sinkhorn
  relaxed OT-DPF diagnostic branch;
- `bayesfilter_ledh_pfpf_ot`: LEDH-PF-PF with OT, only if its LGSSM runner can
  be matched to the same model and scalar without changing production code.

Primary criteria:

- For the Section-5.1 likelihood table, compare
  `(estimated log likelihood - exact Kalman log likelihood) / T` means and
  standard deviations over the matched seed/realization protocol.
- A BayesFilter lane is classified as `matched_to_filterflow` only if every
  required theta/epsilon cell is finite, uses the same mathematical object,
  and lies within the executable filterflow Monte Carlo band used in the prior
  matched audit, with no sign, scale, or ordering inversion.
- The paper-style annealed transport path and the BayesFilter fixed-target
  Sinkhorn branch must be reported as distinct mathematical objects unless the
  result derives and verifies an equivalence.
- Gradient and smoothness diagnostics are separate from likelihood-table
  reproduction.  Finite gradients are required for a gradient smoke pass, but
  finite gradients alone do not establish gradient agreement.

Veto diagnostics:

- `filterflow` compatibility environment unavailable or `filterflow` scripts no
  longer execute;
- wrong transition covariance convention used without an explicit ledger row;
- Kalman exact likelihood differs materially between BayesFilter and
  `filterflow` on the same observation path;
- BayesFilter and `filterflow` outputs are compared under different output
  scalars or different observation paths;
- non-finite likelihoods, weights, corrected log weights, gradients, or
  transport matrices;
- failed Sinkhorn marginal residuals not marked as a branch-specific veto;
- fixed-target Sinkhorn results treated as equivalent to filterflow's annealed
  regularized transport without evidence;
- value-only likelihood evidence promoted to posterior correctness, HMC
  readiness, production readiness, or gradient correctness;
- new BayesFilter-owned algorithmic code imports NumPy as implementation
  backend;
- unauthorized edits to production `bayesfilter/`, `tests/`, monograph
  chapters, high-dimensional lane files, vendored student code, or
  `.localsource/filterflow` source.

Explanatory diagnostics:

- filterflow branch, commit, diff summary, and local compatibility patch
  summary;
- exact commands, CPU-only manifest, package versions, and wall time;
- paper/table values used as context, not as sole authority;
- Kalman reference values and BayesFilter-vs-filterflow Kalman deltas;
- PF and DPF per-time likelihood-error tables;
- ESS, resampling counts, resampling trigger semantics, and ancestor policy;
- cost scaling, epsilon target, annealing schedule, Sinkhorn iteration budget,
  stopping tolerance, stabilization mode, and row/column residuals;
- runtime and seed-to-seed variability;
- finite-gradient smoke diagnostics, gradient cosine/sign/RMSE versus Kalman
  finite-difference diagnostics where available.

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
- no claim that fixed-target Sinkhorn is filterflow-equivalent unless a later
  result proves that exact statement;
- no claim that the smoothness/gradient smoke reproduces the full supplement
  figure or learning table.

## Inputs

- `AGENTS.md`
- `CLAUDE.md`
- `/home/chakwong/.codex/skills/scholarly-literature-audit/SKILL.md`
- `/home/chakwong/python/claudecodex/policies/scholarly-literature-audit-policy.md`
- `.localsource/dpf_ot_audit/corenflos2021_differentiable_particle_filtering_eot.pdf`
- `.localsource/dpf_ot_audit/corenflos2021_differentiable_particle_filtering_eot_supp.pdf`
- `docs/plans/bayesfilter-dpf-ot-resampling-math-source-audit-result-2026-05-30.md`
- `docs/plans/bayesfilter-dpf-filterflow-lgssm-cross-implementation-audit-result-2026-05-30.md`
- `docs/plans/bayesfilter-dpf-filterflow-lgssm-matched-cross-audit-result-2026-05-30.md`
- `docs/plans/bayesfilter-dpf-filterflow-gap-closure-result-2026-05-30.md`
- `docs/plans/bayesfilter-dpf-filterflow-final-gaps-closure-result-2026-05-30.md`
- `.localsource/filterflow/scripts/simple_linear_comparison.py`
- `.localsource/filterflow/scripts/simple_linear_smoothness.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/plan.py`
- `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/sinkhorn.py`
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_gap_closure_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_final_gaps_closure_tf.py`

## Planned Outputs

If this plan is later executed, create:

- `docs/plans/bayesfilter-dpf-filterflow-full-comparison-result-2026-05-31.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-full-comparison-2026-05-31.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_full_comparison_2026-05-31.json`

This plan artifact is:

- `docs/plans/bayesfilter-dpf-filterflow-full-comparison-plan-2026-05-31.md`

## Allowed Write Set

For this planning task:

- `docs/plans/bayesfilter-dpf-filterflow-full-comparison-plan-2026-05-31.md`

For a later reviewed execution of this plan:

- `docs/plans/bayesfilter-dpf-filterflow-full-comparison-result-2026-05-31.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-full-comparison-2026-05-31.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_full_comparison_2026-05-31.json`

## Forbidden Write Set

- production `bayesfilter/`;
- `tests/`;
- monograph chapters under `docs/chapters/`;
- high-dimensional nonlinear filtering lane files;
- DSGE/NAWM-specific code or validation artifacts;
- vendored student code;
- `.localsource/filterflow` source code, unless a separate reviewed plan
  authorizes a compatibility patch;
- unrelated dirty files.

## Full Comparison Matrix

The future execution should fill the following matrix.

| Lane | Source | Purpose | Primary scalar | Promotion status |
| --- | --- | --- | --- | --- |
| Paper Table 1 | Corenflos main paper | Published context | Per-time log-likelihood error | Context only |
| Exact Kalman | Filterflow and BayesFilter | LGSSM oracle | Log likelihood | Required alignment gate |
| Filterflow PF | Patched filterflow | External classical baseline | Per-time log-likelihood error | Comparator |
| BayesFilter PF | TF/TFP | Internal classical baseline | Same scalar | Must match filterflow PF band |
| Filterflow RegularisedTransform | Patched filterflow | External DPF reference | Same scalar | Primary DPF comparator |
| BayesFilter filterflow-style transport | TF/TFP audit mirror | Matched paper-style OT path | Same scalar | Must match filterflow DPF band |
| BayesFilter fixed-target Sinkhorn | TF/TFP | Existing diagnostic branch | Same scalar plus residuals | Diagnostic, not paper-equivalent |
| BayesFilter LEDH-PF-PF-OT | TF/TFP | Default experimental architecture check | Same scalar if feasible | Exploratory comparator |
| Smoothness/gradient smoke | Filterflow and BayesFilter where available | Differentiability diagnostic | Named likelihood/log-normalizer scalar gradient | Finite diagnostic only |

## Method

1. Reconfirm the local `filterflow` state:
   - branch `bayesfilter-py311-compat`;
   - upstream base commit `5d8300ba247c4c17e1a301a22560c24fd0670bfe`;
   - diff summary limited to reviewed Python 3.11 compatibility edits.
2. Re-read the Corenflos paper and supplement anchors used for Section 5.1 and
   smoothness diagnostics.  Record source-support, claim-support, and
   paper/code discrepancy ledgers.
3. Recover or regenerate a matched LGSSM data bundle:
   - executable `filterflow` transition covariance convention `I_2`;
   - horizon `T=150`;
   - particles `N=25`;
   - theta grid `0.25, 0.5, 0.75`;
   - epsilon grid `0.25, 0.5, 0.75`;
   - observation covariance `0.1 I_2`;
   - 100 filter realizations or the reviewed bounded substitute if runtime is
     too large.
4. Run exact Kalman in both implementations or in one shared checked path and
   verify the same-observation likelihood agrees within numerical tolerance.
5. Run filterflow PF and RegularisedTransform lanes in the isolated
   `.localenv/filterflow-py311` environment.
6. Run BayesFilter PF and BayesFilter filterflow-style transport lanes under
   CPU-only TF/TFP.
7. Run BayesFilter fixed-target Sinkhorn as a separate diagnostic branch with
   explicit residual, iteration, and trigger ledgers.
8. Run BayesFilter LEDH-PF-PF-OT on the matched LGSSM only if the same scalar
   can be produced without production edits or ambiguous proposal correction.
9. Run bounded smoothness/gradient smoke diagnostics:
   - fixed observations and common random numbers where feasible;
   - named scalar;
   - finite GradientTape gradients for BayesFilter differentiable paths;
   - filterflow gradient diagnostics only as external reference;
   - finite-difference comparator labelled reference-only.
10. Write JSON and Markdown outputs with:
    - comparison tables;
    - discrepancy ledger;
    - red-flag ledger;
    - non-implications;
    - run manifest;
    - verification results.
11. Review the result with Claude Code using the same max-five loop before any
    conclusion is promoted.

## Skeptical Pre-Execution Audit

| Risk | Status | Mitigation |
| --- | --- | --- |
| stale context | pass | This plan builds on the accepted matched-audit, gap-closure, and final-gaps results from 2026-05-30. |
| wrong paper setting | watch | Transition covariance discrepancy is explicit; execution uses executable `I_2` convention and records paper text as likely typo/notation mismatch. |
| wrong comparator | pass | Primary comparator is patched executable `filterflow`, with paper Table 1 as context and Kalman as exact LGSSM oracle. |
| value-only overclaim | pass | Likelihood-table matching and gradient/smoothness diagnostics are separate gates. |
| fixed-target overclaim | pass | Fixed-target Sinkhorn is diagnostic unless equivalence is derived and verified. |
| LEDH overclaim | pass | LEDH-PF-PF-OT is exploratory in this comparison unless it can produce the same scalar under matched conditions. |
| arbitrary thresholds | pass | The main match band is the executable filterflow Monte Carlo band from the matched protocol, not a universal threshold. |
| missing stop conditions | pass | Stop conditions are listed below. |
| hidden production drift | pass | Production `bayesfilter/` and `tests/` are forbidden. |
| monograph drift | pass | `docs/chapters/` is forbidden. |
| highdim-lane contamination | pass | High-dimensional nonlinear filtering lane files are forbidden. |
| vendored-code contamination | pass | Student/vendored code is neither edited nor used as authority. |
| artifact answers question | pass | The planned outputs directly compare filterflow and BayesFilter methods under matched LGSSM semantics. |

## Stop Conditions

- exact Claude command/model/effort is unavailable for plan review;
- `filterflow` compatibility environment cannot execute and no source-level
  comparison can answer the question;
- the matched observation path cannot be recovered or regenerated;
- transition covariance convention cannot be resolved and recorded;
- Kalman reference mismatch on the same observations is material;
- required BayesFilter lane would need production, test, monograph, highdim,
  vendored, or `.localsource/filterflow` source edits;
- a BayesFilter-owned differentiable path requires NumPy as implementation
  backend;
- fixed-target Sinkhorn residual veto occurs and cannot be isolated to that
  diagnostic branch;
- JSON/report validation fails in a way that invalidates the comparison;
- Claude review finds a major blocker that Codex agrees with.

## Verification Commands For Later Execution

```bash
git -C .localsource/filterflow status --short --branch
```

```bash
git -C .localsource/filterflow rev-parse HEAD
```

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_full_comparison_tf
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_full_comparison_tf --validate-only
```

```bash
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_full_comparison_2026-05-31.json >/dev/null
```

```bash
rg -n "student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py
```

```bash
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py
```

```bash
rg -n "[ \t]+$" docs/plans/bayesfilter-dpf-filterflow-full-comparison-plan-2026-05-31.md docs/plans/bayesfilter-dpf-filterflow-full-comparison-result-2026-05-31.md experiments/dpf_implementation/reports/dpf-filterflow-full-comparison-2026-05-31.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py
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

Review this plan with Claude Code exactly as:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Run Claude Code with elevated/trusted permissions per `AGENTS.md`.  Claude
must review read-only and must return `ACCEPT` or `REJECT` first, followed by
findings.  Codex audits Claude's findings.  If Claude rejects and Codex agrees,
patch this plan and resubmit.  Loop until `ACCEPT` or max five iterations.  On
iteration five, accept only for user inspection unless there is a major
blocker.

The later execution result must use the same review loop before the comparison
is treated as reviewed evidence.

