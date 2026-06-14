# Plan: 1D-to-Smoothness LGSSM Continuation Ladder

## Scope

This plan creates a reviewed continuation ladder that moves the controlled
one-dimensional scalar-state LGSSM diagnostic toward the executable filterflow
smoothness LGSSM one axis at a time. The purpose is to identify the first rung
where BayesFilter/filterflow agreement, residual diagnostics, scalar contract,
or gradient diagnostics fail.

This is the BayesFilter-owned experimental DPF implementation/evidence lane
only. Do not edit production `bayesfilter/`, `tests/`, monograph chapters under
`docs/chapters/`, high-dimensional nonlinear filtering lane artifacts, vendored
student code, DSGE/NAWM artifacts, or `.localsource/filterflow` source.

## Evidence Contract

Primary question: at which single-axis transition does BayesFilter/filterflow
agreement first fail as the controlled scalar-state diagnostic approaches the
filterflow smoothness LGSSM?

Primary comparator: the canonical executable current local patched filterflow
checkout under `.localsource/filterflow`. The comparator identity is the
recorded HEAD commit plus local-diff/status fingerprint, not an authority claim
about a pristine upstream branch. The branch string, including
`bayesfilter-py311-compat` when reported by Git, is descriptive only and need
not resolve as a normal local or remote ref. This checkout is not pristine
upstream and is not asserted clean. The runner and result must record the
comparator HEAD commit SHA, symbolic branch/head string, local-diff status,
Python version, package manifest, and exact filterflow command. The evidence
applies only to that recorded executable comparator state. The runner must
record a comparator fingerprint before R1 and after every rung. If any
comparator fingerprint field changes during the run, the current rung and all
later rungs must be marked `blocked_by_comparator_drift`; do not automatically
restart inside the same run.

Primary pass criterion per rung:

- filterflow subprocess executes;
- CPU-only manifests show no visible GPU devices;
- BayesFilter/filterflow trigger pattern matches;
- forward scalar and step ledger match within predeclared tolerances;
- absolute row and column residuals pass the configured tolerance;
- finite scalar values are recorded.

Rung execution contract:

- every rung must set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import;
- every rung must record a parent-process CPU-only manifest showing GPU devices
  were hidden;
- every filterflow subprocess must inherit `CUDA_VISIBLE_DEVICES=-1` before
  TensorFlow import and must return its own CPU-only manifest showing no visible
  GPU devices;
- every rung must record that no student, vendored, high-dimensional,
  DSGE/NAWM, production `bayesfilter/`, `tests/`, monograph chapter, or
  filterflow-source code path was used or edited.

Gradient diagnostics:

- same-scalar finite-difference gradients are important diagnostics;
- AD gradients are explanatory only unless same-scalar AD-vs-FD agreement is
  established;
- no gradient correctness is concluded from finite AD values alone.
- R6 and R7 promotion is scalar/forward-ledger/residual only. Finite-difference
  and AD gradients may localize the first failure, but cannot pass a rung and
  cannot prove scalar equivalence.

Veto diagnostics:

- non-finite scalar or gradient;
- filterflow blocker;
- trigger mismatch;
- scalar or forward ledger mismatch;
- absolute residual violation;
- unrecorded scalar contract;
- forbidden write/import;
- inability to preserve fixed variables for a rung.

Explanatory diagnostics:

- AD gradient;
- finite-difference gradient;
- resampling frequency;
- Sinkhorn residuals;
- available iteration counts;
- runtime;
- first-failure location.

Artifact contract:

- JSON and report must emit a canonical per-rung ledger.
- Each rung ledger row must include `rung`, `status` with one of `pass`,
  `veto`, `blocked`, or `diagnostic_only`, `evidence_bearing` boolean,
  `blocker_reason`, `failure_observed_directly` boolean, `inherited_blocker`,
  `first_failing_rung`, `first_blocked_rung`, comparator fingerprint
  before/after the rung, fixed variables, varied variables, primary pass/fail
  metrics, veto diagnostics, and explanatory diagnostics.
- The top-level result must include a single `first_failing_rung` field. If all
  evidence-bearing rungs pass, this field is `none_observed_in_bounded_ladder`.
- The top-level result must also include `first_blocked_rung`. Blocked rungs
  must repeat the upstream blocker in `inherited_blocker` so readers cannot
  confuse the first blocked rung with the first evidence-bearing failure.
- Aggregated plots/tables may be included only after the canonical rung ledger;
  they cannot replace the rung ledger.

## Rungs

The ladder is executed sequentially. Later rungs should be reported as
structured blockers when an earlier rung produces a veto that invalidates using
that rung as a stable base.

1. `R1_T4_residual_ladder`:
   Keep the fixed scalar-state `T=4` fixture. Vary only
   `convergence_threshold` and `max_iterations` to determine whether the shared
   row-residual veto around `5.23e-4` under tolerance `1e-4` disappears. R2 is
   evidence-bearing only if R1 clears the fixed `1e-4` row and column residual
   veto. Weaker residual thresholds may be reported only as diagnostic
   sensitivity checks and cannot promote R1 or unblock R2. If the T=4 row
   residual remains near `5.23e-4` after the R1 sweep, R1 is the first failing
   rung and R2-R8 must be recorded as `blocked_by_R1_residual_veto`.
   Bounded sweep set:
   `convergence_threshold in {1e-6, 1e-7, 1e-8}` and
   `max_iterations in {200, 500, 1000}`. R1 stops early only when both
   BayesFilter and filterflow pass the fixed row/column residual veto and all
   scalar/ledger criteria; otherwise it records all nine cells and fails. If
   multiple cells pass, select the authoritative inherited setting for R2-R8 by
   least `max_iterations`, then loosest `convergence_threshold`, then smallest
   maximum absolute row residual. Record the selected cell explicitly.

2. `R2_1d_horizon_ladder`:
   Extend scalar-state horizon `T=4 -> 8 -> 16 -> 32 -> 100`, using generated
   fixed observations/noises and stable seed protocol after R1 identifies a
   viable residual setting.

3. `R3_1d_particle_count_ladder`:
   Extend particle count `N=4 -> 8 -> 16 -> 25` at the selected horizon and
   scalar-state model.

4. `R4_1d_random_stream_alignment`:
   Move from hand-written/generated inputs to filterflow-style generated
   observations, initial particles, and transition noises. Required matched
   variables: scalar-state transition equation, observation equation,
   transition covariance, observation covariance, initial covariance, horizon,
   particle count, theta value/grid, epsilon value/grid, ESS trigger threshold,
   observation path, initial particle matrix, transition-noise tensor, and seed
   manifest. Allowed unmatched variables, if technically unavoidable, are
   limited to floating-point dtype/backend ordering and subprocess formatting;
   unmatched variables make R4 diagnostic-only unless the result proves they do
   not affect the compared ledger.

5. `R5_1d_resampling_policy_match`:
   Match the smoothness resampling policy, especially `ESS <= 0.9999 N`.
   Record resampling frequency and residual behavior.

6. `R6_1d_parameter_grid_surface`:
   Move from single `theta=0.7` to a small scalar theta grid. Compare scalar
   surface, finite-difference gradients, and AD diagnostics.

7. `R7_1d_smoothness_scalar_contract`:
   Match smoothness scalar contract: total vs mean log likelihood, sign,
   normalization, finite-difference step, batch handling, and surface
   convention.

8. `R8_2d_constant_velocity_bridge`:
   Introduce the actual filterflow smoothness model in the smallest bounded
   version first:
   `A(theta)=diag(theta_1, theta_2)+[[0,1],[0,0]]`,
   transition covariance `[[1/3, 1/2], [1/2, 1]]`, observation matrix
   `[[1,0]]`, observation covariance `[[0.01]]`.

## Tolerances

Forward ledger tolerances inherit the controlled 1D comparison. Evidence-bearing
residual tolerances are fixed. A rung may record a stricter tolerance or a
weaker diagnostic-only tolerance, but weakening a veto tolerance cannot pass the
rung, cannot promote evidence, and cannot unblock later rungs. Only R1 may
sweep algorithm settings (`convergence_threshold`, `max_iterations`) to try to
meet the fixed residual veto.

| Quantity | Tolerance |
| --- | ---: |
| predicted particles | `5e-5` |
| observation log likelihoods | `5e-5` |
| normalized log weights | `5e-5` |
| transport cost matrix | `5e-5` |
| transport matrix | `5e-5` |
| post-transport particles | `5e-5` |
| per-step log normalizer | `5e-5` |
| total scalar | `5e-5` |
| absolute row residual | `1e-4` |
| absolute column residual | `1e-4` |
| BayesFilter/filterflow finite-difference gradient | `abs <= 1e-3` or `rel <= 1e-2` |

## Stop Conditions

- exact Claude command unavailable;
- TF/TFP unavailable;
- filterflow executable environment unavailable;
- comparator branch, commit, local-diff status, Python version, package
  manifest, or exact command cannot be recorded;
- comparator checkout changes after R1 begins;
- implementation requires NumPy as BayesFilter algorithmic backend;
- matching filterflow would require mutating `.localsource/filterflow`;
- forbidden write set would be touched;
- an early rung veto invalidates later rungs as evidence.

When an early rung veto occurs, record later rungs as `blocked_by_<rung>` rather
than forcing the full smoothness ladder.

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-plan-2026-06-02.md`
- `docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-result-2026-06-02.md`
- `docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-review-loop-2026-06-02.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_to_smoothness_ladder_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-1d-to-smoothness-ladder-2026-06-02.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_to_smoothness_ladder_2026-06-02.json`

The continuation-ladder runner and its JSON/report are new artifacts to be
created by this plan. The prior runners
`run_filterflow_1d_lgssm_step_gradient_comparison_tf.py` and
`run_filterflow_1d_lgssm_horizon_ladder_tf.py` are read-only context inputs
that establish the fixed T=2/T=4 residual baseline; they are not the output
runner for this plan.

## Skeptical Pre-Execution Audit

- Wrong baseline risk: comparator is current local patched filterflow, not
  fixed-target Sinkhorn and not pristine upstream.
- Overclaim risk: passing a rung establishes only that rung.
- Gradient risk: AD gradients remain diagnostic unless AD-vs-FD agrees.
- Residual risk: the known `T=4` row residual veto must be resolved before
  later rungs are evidence-bearing.
- Hidden drift risk: no production, tests, chapter, highdim, student, vendored,
  DSGE/NAWM, or filterflow-source edits.
- Artifact relevance: the ladder must identify first failure and not merely
  aggregate mixed diagnostics.

Audit status: proceed only after Claude accepts this plan.

## Claude Review Protocol

Use Claude Code exactly as:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Claude must return `ACCEPT` or `REJECT` with findings. Codex independently
classifies every finding as `ACCEPT`, `PARTIAL`, `DISPUTE`, or `CLARIFY`.
Patch accepted/partial findings and resubmit until `ACCEPT` or max 5 rounds.
Use the same protocol for the result.

## Verification

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_to_smoothness_ladder_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_to_smoothness_ladder_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_to_smoothness_ladder_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_to_smoothness_ladder_2026-06-02.json >/dev/null
python -c "import json; p=json.load(open('experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_to_smoothness_ladder_2026-06-02.json')); assert p['run_manifest']['pre_import_cuda_visible_devices']=='-1'; assert p['run_manifest']['gpu_devices_visible']==[]; assert all(row['parent_cpu_only_manifest']['gpu_devices_visible']==[] for row in p['rung_ledger'] if 'parent_cpu_only_manifest' in row); assert all(row['filterflow_cpu_only_manifest']['gpu_devices_visible']==[] for row in p['rung_ledger'] if 'filterflow_cpu_only_manifest' in row)"
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_to_smoothness_ladder_tf.py
rg -n "^\\s*(from|import)\\s+.*(student|vendored|vendor|highdim|dsge|DSGE|nawm|NAWM)" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_to_smoothness_ladder_tf.py
rg -n "[ \t]$" docs/plans/bayesfilter-dpf-1d-to-smoothness-lgssm-continuation-ladder-*.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_to_smoothness_ladder_tf.py experiments/dpf_implementation/reports/dpf-filterflow-1d-to-smoothness-ladder-2026-06-02.md
git diff --check
git status --short -- bayesfilter tests docs/chapters
git status --short --branch
```

## Hard Caveats

- No production readiness.
- No public API readiness.
- No posterior correctness.
- No HMC readiness.
- No general nonlinear-SSM validity.
- No DSGE/NAWM validation.
- No banking/model-risk claim.
- No monograph claim.
- Current local patched filterflow is the executable reference, not pristine
  upstream.
- Passing a rung only establishes agreement for that rung.
