# DPF BayesFilter/FilterFlow Final Comparison Closeout And Robustness Plan

metadata_date: 2026-06-07
status: DRAFT_PENDING_CLAUDE_REVIEW

## Scope Correction

The user removed item 4 from the work.  This plan therefore excludes all
student-repository work.  No command under a student repository, no student
adapter, and no student-derived match/mismatch/correctness conclusion is in
scope.

Included work:

1. write a consolidated BayesFilter/FilterFlow closeout statement;
2. run a stochastic-sanity diagnostic that freezes seeded ancestor schedules
   before comparison;
3. run or validate the longer-horizon/particle ladder diagnostic;
5. document the comparison contract and the residual limitations in the DPF
   chapter.

## Question

After the V2 production BayesFilter/FilterFlow tie-out, what can we responsibly
say about DPF agreement, and do small robustness diagnostics reveal any blocker
to that statement?

## Evidence Contract

Primary promotion criterion:

- The final closeout may say BayesFilter and the executable local
  FilterFlow-side adapters match on the frozen deterministic V2 comparison
  contract if and only if the existing V2 density, no-resampling path,
  fixed-ancestor path, and fixed-branch AD-gradient artifacts validate and the
  result ledger preserves the non-claims.

Diagnostics that can veto:

- any student command or student-derived metric;
- any `.localsource/filterflow` mutation;
- treating BayesFilter, FilterFlow, TT, dense quadrature, paper tables,
  stochastic simulation, or any student repository as an oracle;
- relaxing tolerances, fixtures, scalars, branches, comparators, or gradient
  contracts after seeing results without a reviewed amendment;
- using finite differences as a gradient gate;
- nonfinite scalar/path/AD-gradient values in the V2 validation artifacts;
- unclassified BF/FF mismatch on a primary V2 deterministic field.

Diagnostics that are explanatory only:

- finite-difference diagnostics;
- the seeded-ancestor robustness diagnostic in this plan;
- the 1D LGSSM horizon ladder and its Sinkhorn residual diagnostics;
- TensorFlow CPU-only CUDA/cuInit stderr.

What will not be concluded:

- no filter correctness proof;
- no claim that BayesFilter or FilterFlow is mathematically correct;
- no stochastic-resampling distribution correctness claim;
- no differentiable-resampling or gradient-through-random-ancestor claim;
- no student match, mismatch, correctness, or failure claim;
- no TT/SIRT, paper-table, GPU, HMC, DSGE, scalability, deployment, or
  production-readiness claim.

Result artifacts:

- this plan;
- `docs/plans/bayesfilter-dpf-bf-filterflow-final-comparison-closeout-and-robustness-claude-review-ledger-2026-06-07.md`;
- `experiments/dpf_implementation/reports/outputs/dpf_bf_filterflow_seeded_ancestor_robustness_2026-06-07.json`;
- `experiments/dpf_implementation/reports/dpf-bf-filterflow-seeded-ancestor-robustness-2026-06-07.md`;
- `docs/plans/bayesfilter-dpf-bf-filterflow-final-comparison-closeout-and-robustness-result-2026-06-07.md`;
- DPF chapter edits in `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`.

## Skeptical Plan Audit

Wrong baseline risk:

- The comparison is not against an oracle.  It is a same-contract
  implementation tie-out between BayesFilter and executable local
  FilterFlow-side adapters.

Proxy metric risk:

- FD, stochastic schedule probes, ladder residuals, ESS, and moments are
  diagnostics only.  They cannot promote or demote the V2 deterministic
  agreement claim except by revealing a contract violation or nonfinite
  artifact.

Missing stop condition risk:

- Stop on any material Claude blocker after five review rounds, any student
  command requirement, any `.localsource/filterflow` mutation need, any
  scientific-contract change, or missing required infrastructure.

Unfair comparison risk:

- The seeded-ancestor diagnostic freezes ancestor schedules and compares both
  implementations on the same schedules.  It is not RNG equality and not a
  stochastic distribution test.

Environment mismatch risk:

- All TensorFlow evidence commands are CPU-only with `CUDA_VISIBLE_DEVICES=-1`
  before TensorFlow import.  FilterFlow subprocesses inherit CPU-only mode.

Artifact-answer risk:

- The final closeout answers only whether the deterministic BF/FF tie-out and
  small robustness diagnostics support the scoped comparison statement.  It
  does not answer whether DPF is scientifically correct.

Audit decision: PASS_FOR_CLAUDE_PLAN_REVIEW.

## Phases

### P0 Claude Plan Review

Run Claude Code review on this plan.  Loop until PASS/convergence or max five
rounds.  Patch material plan blockers before evidence execution.

### P1 Existing V2 Artifact Validation

Run the V2 validation commands:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_density_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_noresampling_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_fixed_resampling_tf --validate-only
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_gradients_tf --validate-only
```

Pass interpretation: V2 artifacts remain structurally valid under their frozen
contracts.  This validates the basis for the consolidated BF/FF closeout.

### P2 Seeded-Ancestor Robustness Diagnostic

Run:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_bf_filterflow_seeded_ancestor_robustness_tf
```

This creates deterministic pseudo-stochastic ancestor schedules from recorded
seeds, then freezes those schedules before comparing BayesFilter and
FilterFlow-side adapters.  It is a branch-robustness diagnostic only.

Pass interpretation: the diagnostic produced finite rows and no same-schedule
BF/FF delta.  Non-pass interpretation: classify the mismatch before any
closeout; do not infer stochastic resampling correctness or failure.

### P3 Horizon Ladder Diagnostic

Run or validate the existing controlled 1D LGSSM horizon ladder:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_horizon_ladder_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_horizon_ladder_tf --validate-only
```

The ladder is explanatory.  Its known residual-veto state does not invalidate
the V2 deterministic comparison if BF/FF implementation ledgers agree and the
residual is classified as a diagnostic solver residual.

### P4 DPF Chapter Documentation

Edit `docs/chapters/ch19f_dpf_debugging_crosswalk.tex` to add a concrete
BayesFilter/FilterFlow deterministic tie-out contract:

- frozen particles, innovations, observations, scalars, and ancestor schedules;
- matched V2 density, no-resampling, fixed-ancestor, and fixed-branch AD
  gradients;
- SIR gradient contract block;
- FD diagnostic-only policy;
- seeded-ancestor and horizon-ladder diagnostics as explanatory robustness;
- explicit non-claims.

Validate at least LaTeX syntax/build with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

from `docs/`.

### P5 Result Closeout And Claude Review

Write the final result ledger.  Run Claude result/governance review until PASS
or max five rounds.  Patch only reviewed blockers.  The final result must state
student work was removed from scope and no student commands were run.
