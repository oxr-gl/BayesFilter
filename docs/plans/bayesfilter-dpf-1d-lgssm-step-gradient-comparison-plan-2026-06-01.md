# Plan: 1D LGSSM Step Gradient Comparison

## Scope

This plan creates the smallest controlled diagnostic for the remaining
BayesFilter TF/TFP annealed-transport gradient mismatch against the canonical
executable local filterflow reference.

This is the BayesFilter-owned experimental DPF implementation/evidence lane
only. It must not edit production `bayesfilter/`, `tests/`, monograph chapters
under `docs/chapters/`, high-dimensional nonlinear filtering lane artifacts,
vendored student code, DSGE/NAWM-specific artifacts, or `.localsource/filterflow`
source files.

## Evidence Contract

Question: for a controlled one-dimensional LGSSM, do BayesFilter and filterflow
produce the same numerical values for the particle filter scalar and its
derivative when every particle, observation, transition noise, resampling
trigger, and annealed-transport input is fixed?

Primary comparator: the canonical executable local filterflow reference under
`.localsource/filterflow`, using its `RegularisedTransform` transport primitive
without mutating filterflow source.

Primary pass criterion: BayesFilter and filterflow must agree, within the
predeclared floating-point tolerances below, on the same-scalar step ledger:

- predicted particles;
- observation log likelihoods;
- log weights;
- ESS and resampling trigger;
- annealed transport cost matrix;
- transport matrix;
- post-transport particles;
- row and column residuals;
- per-step log normalizers;
- total scalar;
- GradientTape gradient and centered finite-difference gradient with respect to
  the scalar transition parameter.

Predeclared tolerances:

| Quantity | Tolerance |
| --- | ---: |
| fixed numeric input equality | exact after JSON round trip |
| ESS flags | exact boolean match |
| predicted particles | `max_abs <= 5e-5` |
| observation log likelihoods | `max_abs <= 5e-5` |
| normalized log weights | `max_abs <= 5e-5` |
| transport cost matrix | `max_abs <= 5e-5` |
| transport matrix | `max_abs <= 5e-5` |
| post-transport particles | `max_abs <= 5e-5` |
| per-step log normalizer | `max_abs <= 5e-5` |
| total scalar | `abs <= 5e-5` |
| row residual | `<= 1e-4` |
| column residual | `<= 1e-4` |
| GradientTape vs finite difference within implementation | `abs <= 1e-3` or `rel <= 1e-2` |
| BayesFilter gradient vs filterflow gradient | `abs <= 1e-3` or `rel <= 1e-2` |

The transport and scalar tolerances allow float32 executable filterflow internals
to be compared with the TF/TFP BayesFilter implementation without choosing
thresholds after seeing results.

Veto diagnostics:

- non-finite scalar or gradient;
- mismatched scalar sign or normalization;
- unmatched fixed inputs;
- unmatched ESS trigger;
- unmatched transport matrix beyond tolerance;
- failed row or column transport residuals;
- inability to isolate or run the one-dimensional filterflow computation.

Explanatory diagnostics only:

- exact Kalman likelihood or finite-difference checks;
- per-stage absolute deltas;
- cost scale and Sinkhorn iteration count;
- whether BayesFilter GradientTape agrees with BayesFilter finite difference;
- whether filterflow GradientTape agrees with filterflow finite difference.

Not concluded even on pass: production readiness, public API readiness,
posterior correctness, HMC readiness, general nonlinear-SSM validity,
DSGE/NAWM validation, banking/model-risk claims, or monograph claims.

## Diagnostic Model

Use a one-dimensional LGSSM:

```text
x_t = theta x_{t-1} + sqrt(Q) eps_t
y_t = x_t + sqrt(R) eta_t
```

Fixed settings:

- scalar parameter `theta0 = 0.7`;
- horizon `T = 2`;
- particles `N = 4`;
- `Q = 0.04`;
- `R = 0.04`;
- initial particles `[-1.5, -0.2, 0.4, 1.2]`;
- transition noises
  `[[0.0, 0.1, -0.2, 0.3], [0.2, -0.1, 0.0, -0.3]]`;
- observations `[0.05, -0.1]`;
- initial log weights uniform;
- ESS threshold `0.9999 * N`, so the first uniform pre-update state should not
  resample, while the second step should resample after the first observation
  creates nonuniform weights;
- annealed transport epsilon `0.25`, scaling `0.9`, convergence threshold
  `1e-6`, max iterations `200`;
- finite-difference step `1e-4`.

Precomputed ESS trigger check for this fixture:

- first pre-update ESS is `4.0`, so with threshold `3.9996` the first
  pre-transition resampling flag is false;
- after the first observation update at `theta0=0.7`, predicted particles are
  approximately `[-1.05, -0.12, 0.24, 0.90]`;
- the normalized weights are approximately
  `[1.42e-7, 5.2239e-1, 4.7752e-1, 8.65e-5]`;
- the resulting ESS is approximately `2.0001`, below `3.9996`, so the second
  pre-transition resampling flag is true.

If the runner computes a different trigger pattern for this exact fixture, that
is a veto and the plan must stop with a structured blocker instead of selecting
a nearby fixture after seeing results.

## Algorithm Contract

Both implementations evaluate the same bounded two-step scalar:

1. start from fixed particles and normalized log weights;
2. before each transition, compute ESS and apply annealed transport only when
   the fixed ESS policy triggers;
3. transition with the fixed transition noise tensor;
4. evaluate Gaussian observation log likelihood;
5. update log weights and add the log predictive normalizer;
6. return the total log likelihood scalar.

BayesFilter uses `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
Filterflow uses `.localsource/filterflow/filterflow/resampling/differentiable/regularized_transport/plan.py`
through a subprocess wrapper. Fixed-target Sinkhorn is not used.

## Outputs

Plan:
`docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-plan-2026-06-01.md`

Review loop:
`docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-review-loop-2026-06-01.md`

Result:
`docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-result-2026-06-01.md`

Runner/report artifacts:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_step_gradient_comparison_tf.py`;
- `experiments/dpf_implementation/reports/dpf-filterflow-1d-lgssm-step-gradient-comparison-2026-06-01.md`;
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_lgssm_step_gradient_comparison_2026-06-01.json`.

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-plan-2026-06-01.md`;
- `docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-review-loop-2026-06-01.md`;
- `docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-result-2026-06-01.md`;
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_step_gradient_comparison_tf.py`;
- `experiments/dpf_implementation/reports/dpf-filterflow-1d-lgssm-step-gradient-comparison-2026-06-01.md`;
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_lgssm_step_gradient_comparison_2026-06-01.json`.

## Forbidden Write Set

- production `bayesfilter/`;
- `tests/`;
- monograph chapters under `docs/chapters/`;
- high-dimensional nonlinear filtering lane artifacts;
- vendored student code;
- DSGE/NAWM-specific artifacts;
- `.localsource/filterflow` source files;
- unrelated dirty files.

## Skeptical Pre-Execution Audit

- Wrong baseline: the comparator is executable local filterflow, not fixed-target
  Sinkhorn and not pristine upstream claims.
- Proxy metric risk: finite gradients are not promotion criteria; same-scalar
  ledger agreement is the promotion criterion.
- Randomness risk: all particles, observations, and transition noises are
  explicit numeric tensors rather than independent random streams.
- Scalar risk: the result must record sign and normalization. The promotion
  criterion is same-scalar ledger agreement culminating in the total log
  likelihood scalar, while per-step normalizers and transport internals are
  required trace evidence and do not imply broader posterior or algorithmic
  correctness.
- Trigger risk: the result must record ESS and flags so a missing transport
  event cannot silently pass.
- Hidden production drift: writes are lane-scoped and experimental only.
- Monograph drift: no chapter edits or monograph claims.
- Contamination risk: no student, vendored, highdim, DSGE, or NAWM imports in
  BayesFilter code.
- Artifact relevance: the runner answers the step-ledger gradient question; it
  does not rerun the smoothness surface or nonlinear ladder.

Audit status before execution: passes if Claude accepts this plan and the runner
can enforce fixed inputs and same-scalar ledger recording.

## Phase Order

1. Review this plan with Claude Code.
2. Independently classify Claude findings as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
   `CLARIFY` in the review-loop artifact.
3. Patch accepted or partially accepted findings and resubmit until `ACCEPT` or
   max 5 rounds.
4. Implement the runner and report/result writers.
5. Run the CPU-only diagnostic and validate-only mode.
6. Run verification commands.
7. Review the result with Claude using the same loop.
8. Patch agreed findings and rerun targeted verification if needed.

## Stop Conditions

- exact Claude command/model/effort unavailable;
- TF/TFP unavailable;
- filterflow executable environment unavailable for this subprocess;
- one-dimensional filterflow computation cannot be isolated without mutating
  `.localsource/filterflow`;
- BayesFilter implementation would require NumPy as algorithmic backend;
- scalar sign/normalization cannot be reconciled;
- required verification fails in a way that invalidates the evidence;
- execution would require forbidden edits.

If filterflow direct one-dimensional primitive execution is blocked, record a
structured blocker and do not claim the 1D comparison passed. A BayesFilter-only
or local-mirror diagnostic may be recorded as explanatory only.

## Claude Review Protocol

Use Claude Code exactly as:

```bash
claude -p --model claude-opus-4-7 --effort max
```

If unavailable, stop and report blocker. Do not substitute.

Claude must return `ACCEPT` or `REJECT` with findings. Codex must independently
classify each finding as `ACCEPT`, `PARTIAL`, `DISPUTE`, or `CLARIFY`. Disputed
findings must be answered in the next Claude prompt with file/section evidence.
Codex must not treat Claude `ACCEPT` as sufficient unless Codex also agrees that
the current artifacts enforce the required controls.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_step_gradient_comparison_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_step_gradient_comparison_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_step_gradient_comparison_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_lgssm_step_gradient_comparison_2026-06-01.json >/dev/null
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_step_gradient_comparison_tf.py
rg -n "^\\s*(from|import)\\s+.*(student|vendored|vendor|highdim|dsge|DSGE|nawm|NAWM)" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_step_gradient_comparison_tf.py
rg -n "[ \t]$" docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-*.md experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_step_gradient_comparison_tf.py experiments/dpf_implementation/reports/dpf-filterflow-1d-lgssm-step-gradient-comparison-2026-06-01.md
git diff --check
git status --short -- bayesfilter tests docs/chapters
git status --short --branch
```

The NumPy gate is expected to have no module-scope NumPy imports in BayesFilter
TF/TFP code. NumPy may appear inside the filterflow subprocess string only for
external reference serialization/reporting; such use must be recorded if present.

## Hard Caveats

- No production readiness.
- No public API readiness.
- No posterior correctness.
- No HMC readiness.
- No general nonlinear-SSM validity.
- No DSGE/NAWM validation.
- No banking/model-risk claim.
- No monograph claim.
- Fixed-target Sinkhorn is a local comparator only and is not used here.
- Patched filterflow is the canonical executable reference for this audit lane,
  not pristine upstream source.
- Passing this diagnostic would only establish agreement for this fixed 1D
  scalar fixture.
