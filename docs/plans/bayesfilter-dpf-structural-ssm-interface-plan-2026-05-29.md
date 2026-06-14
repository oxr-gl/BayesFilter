# DPF Structural-SSM Interface Plan

Date: 2026-05-29

## Decision

`ACCEPTED_BY_CLAUDE_REVIEW_ITERATION_1`

## Evidence Contract

Question: can the experimental TF/TFP LEDH-PF-PF-OT DPF lane replace ad hoc
structural AR(1) handling with a reusable ch18b-inspired structural SSM
interface, then rerun the linear and nonlinear structural AR(1) evidence
without assigning artificial density to deterministic coordinates?

Primary comparators:

- Linear `c=d=0` structural AR(1): exact TF Kalman structural reference.
- Nonlinear structural AR(1): differentiable TF/TFP CUT4 comparator, not
  ground truth.

Primary criteria:

- Interface enforces stochastic/exogenous block `z_t` and deterministic
  completion block `s_t`.
- PF-PF correction uses stochastic transition/proposal densities only.
- Observation likelihood is evaluated on completed state `(z_t, s_t)`.
- Flow log-det is for the stochastic block only.
- Completion residual is recorded and can veto.
- Resampling policy ladder reports whether MLE/gradient behavior changes.

Veto diagnostics: non-finite scalar/gradient/log weights, invalid Kalman
reference for the linear case, deterministic completion residual above
tolerance, hidden density on deterministic block, invalid Sinkhorn residual,
NumPy implementation backend, production/test/vendored/monograph/highdim/DSGE
or NAWM drift, or value-only evidence being described as MLE/gradient
validation.

## Ch18b-Inspired Structural Contract

The structural state is partitioned as:

- stochastic/exogenous block `z_t`;
- deterministic/endogenous completion block `s_t`;
- full completed state `x_t = (z_t, s_t)`.

The model contract must provide:

- `initial_z_sample(num_particles, seed)`;
- `initial_z_log_prob(z)`;
- `initial_s_from_z(z)`;
- `transition_z_sample(previous_z, seed, time_index)`;
- `transition_z_log_prob(current_z, previous_z, time_index)`;
- `complete_s(previous_s, previous_z, current_z, theta)`;
- `observation_log_prob(current_z, current_s, observation, time_index)`;
- `completion_residual(previous_s, previous_z, current_z, current_s)`;
- optional local-linear Gaussian flow proposal over `z_t` only.

The deterministic block receives no independent transition density.  Any
proposal density, target transition density, and flow log determinant are over
`z_t` only.

## Ancestor And Context Semantics

Each particle state stores previous `z`, previous `s`, proposed/current `z`,
completed current `s`, and optional ancestor ids.  The completed full state is
exposed only after deterministic completion.  Resampling policies must state
whether they preserve ancestors, resample ancestor rows, relax only current
`z_t`, or relax the full structural context.

## Resampling Policy Ladder

Run bounded evidence rows for:

1. `none`: no resampling after weighting.
2. `categorical_ancestor`: stateless categorical ancestor resampling, if
   feasible with TensorFlow only.
3. `sinkhorn_current_z`: finite-Sinkhorn relaxed OT on current stochastic block
   only, then recomplete `s_t` using preserved or policy-declared context.
4. `sinkhorn_full_context`: finite-Sinkhorn relaxed OT on
   `(previous_z, previous_s, current_z)`, then recomplete `s_t`; explicitly
   labelled old/ad hoc comparator.

For each policy, record deterministic residuals, finite corrected weights, ESS,
Sinkhorn residuals when applicable, scalar value, gradient, grid MLE, observed
information SE, and SE-scaled MLE distance.

## Implementation Scope

Implement only under:

- `experiments/dpf_implementation/tf_tfp/structural/`
- `experiments/dpf_implementation/tf_tfp/runners/`
- `experiments/dpf_implementation/reports/`
- `docs/plans/`

Expected files:

- `experiments/dpf_implementation/tf_tfp/structural/__init__.py`
- `experiments/dpf_implementation/tf_tfp/structural/contracts_tf.py`
- `experiments/dpf_implementation/tf_tfp/structural/particle_state_tf.py`
- `experiments/dpf_implementation/tf_tfp/structural/resampling_policies_tf.py`
- `experiments/dpf_implementation/tf_tfp/structural/structural_filter_tf.py`
- `experiments/dpf_implementation/tf_tfp/structural/models/structural_ar1_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_structural_interface_linear_ar1_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_structural_interface_nonlinear_ar1_tf.py`

## Outputs

- `docs/plans/bayesfilter-dpf-structural-ssm-interface-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/dpf-structural-interface-linear-ar1-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/dpf-structural-interface-nonlinear-ar1-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_structural_interface_linear_ar1_2026-05-29.json`
- `experiments/dpf_implementation/reports/outputs/dpf_structural_interface_nonlinear_ar1_2026-05-29.json`

## Allowed Write Set

- Listed implementation and output files.
- This plan/result pair.
- Existing experimental structural AR(1) fixture helper may receive a narrow
  reviewed extension for linear fixture parameters only.

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `docs/references.bib`
- high-dimensional nonlinear filtering lane artifacts;
- vendored student code;
- DSGE/NAWM model implementations;
- production API files;
- NumPy implementation backend.

## Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| stale context | pass | Read AGENTS, CLAUDE, ch18b, P5/P6 blockers, linear structural warning, ad hoc runners, Kalman reference, fixture, and Sinkhorn code. |
| wrong comparator | pass | Linear uses exact Kalman; nonlinear uses CUT4 only as differentiable comparator. |
| value-only overclaim | pass | Same-scalar gradients and MLE diagnostics are primary. |
| arbitrary thresholds | pass | SE distance is calibration; residual/Sinkhorn finite checks are vetoes. |
| missing stop conditions | pass | Stop rules cover unavailable Claude/TF, deterministic-density violations, residual failures, and forbidden writes. |
| hidden production drift | pass | Production writes forbidden. |
| monograph drift | pass | ch18b is read-only. |
| vendored contamination | pass | Student/vendored work is unused. |
| highdim contamination | pass | High-dimensional lane is excluded. |
| DSGE/NAWM drift | pass | Toy structural AR(1) only. |
| artifact fitness | pass | Interface and policy ladder directly target the ad hoc structural failure mode. |

## Stop Conditions

Stop or write a structured blocker if:

- exact Claude command/model/effort is unavailable;
- TF/TFP is unavailable;
- implementation requires NumPy backend;
- exact Kalman comparator cannot be used for `c=d=0`;
- deterministic block density appears in PF-PF correction;
- flow log-det cannot be restricted to stochastic block;
- completion residual cannot be recorded;
- required verification fails in a way that invalidates evidence;
- unauthorized production/tests/vendored/monograph/highdim/DSGE/NAWM edits
  would be needed.

## Verification Commands

- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_interface_linear_ar1_tf`
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_interface_linear_ar1_tf --validate-only`
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_interface_linear_ar1_tf --check-reproducibility`
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_interface_nonlinear_ar1_tf`
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_interface_nonlinear_ar1_tf --validate-only`
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_structural_interface_nonlinear_ar1_tf --check-reproducibility`
- `python -m py_compile` over touched Python files.
- `python -m json.tool` over new JSON outputs.
- `rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp`
- import-boundary search for student/vendored/highdim/DSGE/NAWM imports.
- lane-scoped trailing whitespace check.
- `git diff --check`
- `git status --short --branch`
- `git status --short -- bayesfilter tests`

## Claude Review Loop

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

If unavailable, stop and report a blocker.  Claude reviews read-only and must
return `ACCEPT` or `REJECT` with findings.  Codex audits findings, patches
agreed blockers, and resubmits up to five iterations.  On iteration 5, accept
only for user inspection unless a major blocker remains.  Unresolved objections
are risks, not validation.

## What Must Not Be Concluded

No production readiness, public API readiness, HMC readiness, posterior
correctness, DSGE/NAWM validation, banking/model-risk claim, or monograph claim
is concluded.  CUT4 is a differentiable comparator, not ground truth.  Exact
Kalman validates only the `c=d=0` structural toy fixture.

## Review Record

- Iteration 1: `ACCEPT`.  Claude found the evidence contract, structural
  interface contract, no-density deterministic block rule, flow log-det scope,
  resampling ladder, write sets, stop conditions, and verification commands
  aligned with the requested DPF lane.
