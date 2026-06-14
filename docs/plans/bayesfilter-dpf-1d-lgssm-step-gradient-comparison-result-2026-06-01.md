# Result: 1D LGSSM Step Gradient Comparison

## Decision

`one_d_lgssm_step_gradient_mismatch_detected`

## Scope

This result records the controlled one-dimensional LGSSM step-by-step gradient
comparison between BayesFilter TF/TFP annealed transport and the canonical
executable local filterflow reference. The evidenced comparison is the matched
fixed numeric fixture, same scalar ledger, and matched executable transport
output, plus AD-vs-finite-difference mismatch for the same scalar. It does not
verify or compare filterflow's internal annealing iteration count, epsilon
schedule, or convergence trajectory. It follows:

`docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-plan-2026-06-01.md`

Implementation and reports are experimental only. No production `bayesfilter/`,
`tests/`, monograph chapters, high-dimensional lane artifacts, vendored student
code, or DSGE/NAWM artifacts were edited. The runner does not mutate
`.localsource/filterflow`; the comparator is the current local patched
filterflow checkout, not pristine upstream or asserted clean.

## Artifacts

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_step_gradient_comparison_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-1d-lgssm-step-gradient-comparison-2026-06-01.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_lgssm_step_gradient_comparison_2026-06-01.json`
- `docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-review-loop-2026-06-01.md`

## Filterflow Reference Provenance

| Key | Value |
| --- | --- |
| path | `.localsource/filterflow` |
| branch | `bayesfilter-py311-compat` |
| commit | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| nested status | `M scripts/base.py; M scripts/simple_linear_common.py; M scripts/simple_linear_smoothness.py` |
| provenance note | current local patched checkout; not pristine upstream and not asserted clean |

## 1D Fixture

| Key | Value |
| --- | --- |
| Model | `x_t = theta x_{t-1} + sqrt(Q) eps_t`, `y_t = x_t + sqrt(R) eta_t` |
| `theta0` | `0.7` |
| `Q` | `0.04` |
| `R` | `0.04` |
| horizon | `2` |
| particles | `4` |
| initial particles | `[-1.5, -0.2, 0.4, 1.2]` |
| transition noises | `[[0.0, 0.1, -0.2, 0.3], [0.2, -0.1, 0.0, -0.3]]` |
| observations | `[0.05, -0.1]` |
| ESS threshold | `3.9996` |
| expected resampling flags | `[False, True]` |
| epsilon | `0.25` |
| scaling | `0.9` |
| convergence threshold | `1e-6` |
| max iterations | `200` |
| finite-difference step | `1e-4` |

## Main Finding

The forward step ledger matches tightly, but the AD gradients do not match the
finite-difference gradients.

| Metric | BayesFilter | filterflow | Delta |
| --- | ---: | ---: | ---: |
| total scalar | `0.06241077425770403` | `0.062410712242126465` | `6.20155775621356e-08` |
| GradientTape gradient | `-1.7463644027007494` | `-1.7820383310317993` | `0.035673928331049876` |
| finite-difference gradient | `-1.6753548204218038` | `-1.6754865646362305` | `0.0001317442144266323` |
| BayesFilter AD minus finite difference | `-0.0710095822789456` | N/A | N/A |
| filterflow AD minus finite difference | N/A | `-0.10655176639556885` | N/A |

## Step-Ledger Deltas

| Field | Max abs delta | Tolerance | Status |
| --- | ---: | ---: | --- |
| predicted particles | `4.7683715642676816e-08` | `5e-05` | pass |
| observation log likelihoods | `1.833844299525822e-06` | `5e-05` | pass |
| normalized log weights | `1.980896389142117e-06` | `5e-05` | pass |
| transport cost matrix | `3.5174783219460437e-07` | `5e-05` | pass |
| transport matrix | `1.487370371311414e-07` | `5e-05` | pass |
| post-transport particles | `4.768371586472142e-08` | `5e-05` | pass |
| per-step log normalizer | `3.165210882283276e-08` | `5e-05` | pass |
| row residual delta | `7.853376349231667e-08` | `1e-04` | pass |
| column residual delta | `1.1920928910669204e-07` | `1e-04` | pass |

Absolute residual veto diagnostics:

| Field | Value | Tolerance | Status |
| --- | ---: | ---: | --- |
| BayesFilter max row residual | `3.7740217395665354e-06` | `1e-04` | pass |
| BayesFilter max column residual | `4.440892098500626e-16` | `1e-04` | pass |
| filterflow max row residual | `3.6954879760742188e-06` | `1e-04` | pass |
| filterflow max column residual | `1.1920928955078125e-07` | `1e-04` | pass |

## Pass Status

| Check | Status |
| --- | --- |
| filterflow 1D execution | `succeeded` |
| fixed trigger pattern `[False, True]` | `pass` |
| BayesFilter/filterflow trigger match | `pass` |
| finite scalar and gradients | `pass` |
| scalar within tolerance | `pass` |
| step ledger within tolerance | `pass` |
| absolute residuals within tolerance | `pass` |
| BayesFilter gradient vs filterflow gradient | `fail` |
| BayesFilter GradientTape vs finite difference | `fail` |
| filterflow GradientTape vs finite difference | `fail` |

Transport diagnostic availability:

| Diagnostic | BayesFilter | filterflow | Comparison status |
| --- | --- | --- | --- |
| triggered-step iteration count | `62.0` | not available from this wrapper | explanatory only; not compared |
| epsilon schedule | not serialized | not serialized | not compared |
| convergence trajectory | not serialized | not serialized | not compared |

## Interpretation

This diagnostic closes the random-stream and scalar-accounting ambiguity for the
fixed 1D fixture: both implementations use the same numeric inputs, same
resampling trigger pattern, same transport matrix, same post-transport
particles, and nearly the same total scalar. It also shows that BayesFilter and
filterflow finite-difference gradients agree closely.

The remaining blocker is therefore not the forward likelihood ledger for this
fixture. It remains in the derivative path: both implementations' GradientTape
gradients diverge from their own same-scalar finite-difference gradients, and
filterflow's AD/custom-gradient result differs from BayesFilter's AD result.
The derivative-path mismatch remains unexplained by the current evidence.
Transport/custom-gradient semantics are one plausible next hypothesis, but this
result does not isolate the transport-map derivative itself.

## Claude Review

Plan review:

| Round | Claude status | Codex status |
| ---: | --- | --- |
| 1 | `REJECT` | accepted findings; patched ESS trigger guarantee, fixed tolerances, and scalar-overclaim guard |
| 2 | `ACCEPT` | Codex independently agreed |

Result review:

| Round | Claude status | Codex status |
| ---: | --- | --- |
| 1 | `REJECT` | accepted findings; patched result-review ledger, stronger validate-only invariants, and filterflow CPU-only manifest |
| 2 | `REJECT` | accepted findings; patched absolute residual veto checks and durable post-patch verification ledger |
| 3 | `REJECT` | accepted findings; narrowed internal-annealing claim and weakened blocker localization |
| 4 | `REJECT` | accepted findings; narrowed scope to forward scalar/ledger plus AD-vs-FD mismatch and made transport internals explanatory-only |
| 5 | `REJECT` | accepted finding; added filterflow checkout provenance and weakened source-mutation claim |

Round 5 still returned `REJECT`, so the result review is not Claude-accepted
under the original max-5 protocol. The final round finding was patched for user
inspection, but downstream promotion remains blocked unless the human approves
inspection-only acceptance or authorizes another review round.

Result review is recorded in:

`docs/plans/bayesfilter-dpf-1d-lgssm-step-gradient-comparison-review-loop-2026-06-01.md`

## Verification

Executed before result review:

| Command | Result |
| --- | --- |
| `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_step_gradient_comparison_tf.py` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_step_gradient_comparison_tf` | pass; decision `one_d_lgssm_step_gradient_mismatch_detected` |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_step_gradient_comparison_tf --validate-only` | pass |
| `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_lgssm_step_gradient_comparison_2026-06-01.json >/dev/null` | pass |
| schema/decision invariant check on JSON output | pass |
| NumPy import gate on touched BayesFilter TF/TFP runner | pass; no module-scope NumPy import |
| forbidden import-boundary search for student/vendored/highdim/DSGE/NAWM imports | pass; no matches |
| lane-scoped trailing whitespace check | pass |
| `git diff --check` | pass |
| `git status --short -- bayesfilter tests docs/chapters` | pass; no output |
| `git -C .localsource/filterflow rev-parse HEAD` | pass; `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| `git -C .localsource/filterflow status --short --branch` | pass; local patched checkout recorded |

Result-review round 1 patches added stronger validate-only invariants and an
explicit filterflow subprocess CPU-only manifest. Result-review round 2 patches
added absolute residual veto checks and this durable post-patch verification
ledger.

Post-patch verification:

| Command | Result |
| --- | --- |
| `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_step_gradient_comparison_tf.py` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_step_gradient_comparison_tf` | pass; decision `one_d_lgssm_step_gradient_mismatch_detected` |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_1d_lgssm_step_gradient_comparison_tf --validate-only` | pass |
| `python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_1d_lgssm_step_gradient_comparison_2026-06-01.json >/dev/null` | pass |
| schema/decision/CPU-only invariant check on JSON output | pass |
| NumPy import gate on touched BayesFilter TF/TFP runner | pass; no module-scope NumPy import |
| forbidden import-boundary search for student/vendored/highdim/DSGE/NAWM imports | pass; no matches |
| lane-scoped trailing whitespace check | pass |
| `git diff --check` | pass |
| `git status --short -- bayesfilter tests docs/chapters` | pass; no output |

The runner records CPU-only intent before TensorFlow import for the parent
process and inside the executable filterflow subprocess. TensorFlow still emits
CUDA plugin/cuInit log messages under `CUDA_VISIBLE_DEVICES=-1`, but both
payload manifests report no visible GPU devices.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Accept forward-ledger match | Step ledger and scalar match within tolerance | no forward-value veto | only fixed 1D fixture | use this fixture as the minimal reproducer | production readiness, posterior correctness |
| Keep gradient agreement blocked | AD gradients do not match finite differences | gradient promotion vetoed | derivative path mismatch remains unexplained; transport/custom-gradient semantics are one plausible next hypothesis | isolate the derivative of the transport map itself: post-transport particle JVP versus finite difference and filterflow custom-gradient VJP | gradient correctness beyond this fixture |

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No DSGE/NAWM validation is concluded.
- No banking/model-risk claim is concluded.
- No monograph claim is concluded.
- No gradient correctness beyond this fixed 1D scalar fixture is concluded.
