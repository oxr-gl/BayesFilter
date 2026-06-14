# Result: Filterflow Full Comparison For BayesFilter OT-DPF

## Decision

`full_comparison_filterflow_reference_matched_with_fixed_sinkhorn_diagnostic_gap`

The full comparison plan was executed under the BayesFilter experimental
TF/TFP DPF evidence lane.  The BayesFilter filterflow-style annealed transport
mirror matches patched executable `filterflow` within the filterflow Monte
Carlo band on the matched LGSSM table.  The BayesFilter fixed-target Sinkhorn
branch remains a separate diagnostic gap at epsilon `0.25` and must not be
treated as the Corenflos/filterflow paper-style transport.

No production, public API, posterior, HMC, general nonlinear-SSM, external
macro-model, banking/model-risk, or monograph readiness is concluded.

## Artifacts

- Plan:
  `docs/plans/bayesfilter-dpf-filterflow-full-comparison-plan-2026-05-31.md`
- Result:
  `docs/plans/bayesfilter-dpf-filterflow-full-comparison-result-2026-05-31.md`
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-full-comparison-2026-05-31.md`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_full_comparison_2026-05-31.json`

## Claude Review

Plan review:

| Iteration | Status | Codex audit |
| --- | --- | --- |
| 1 | `ACCEPT` | Accepted. Claude confirmed the evidence contract, lane boundary, covariance ambiguity handling, fixed-target-vs-annealed separation, gradient overclaim controls, verification commands, and max-five review loop. |

Result review:

| Iteration | Status | Codex audit |
| --- | --- | --- |
| 1a | `HUNG_NO_OUTPUT` | The first read-only Claude review process produced no output after several bounded polls and was terminated. No findings were accepted from this run. |
| 1b | `ACCEPT` | Accepted. Claude found no blockers and confirmed the result executed the accepted plan, bounded the claims, separated filterflow-style annealed transport from fixed-target Sinkhorn, recorded the covariance ambiguity, preserved lane boundaries, provided adequate artifacts/validation, and avoided NumPy as a BayesFilter algorithmic backend. |

## Files Changed

New files from this execution:

- `docs/plans/bayesfilter-dpf-filterflow-full-comparison-result-2026-05-31.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-full-comparison-2026-05-31.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_full_comparison_2026-05-31.json`

Previously created reviewed plan:

- `docs/plans/bayesfilter-dpf-filterflow-full-comparison-plan-2026-05-31.md`

No production `bayesfilter/`, `tests/`, monograph chapter, high-dimensional
lane file, vendored student code, or `.localsource/filterflow` source file was
edited by this execution.

## Filterflow Reference

- Branch: `bayesfilter-py311-compat`
- Commit: `5d8300ba247c4c17e1a301a22560c24fd0670bfe`
- Upstream base: `5d8300ba247c4c17e1a301a22560c24fd0670bfe`
- Local source status: patched Python 3.11 compatibility branch, not pristine
  upstream source.
- Local diff summary:
  `scripts/base.py`, `scripts/simple_linear_common.py`, and
  `scripts/simple_linear_smoothness.py` contain the reviewed compatibility
  patch.

## Paper/Code Setting Ledger

The comparison uses the executable `filterflow` convention:

- state dimension: `2`;
- transition mean: `diag(theta_1, theta_2) x`;
- transition covariance: `I_2`;
- observation covariance: `0.1 I_2`;
- horizon: `T=150`;
- particles: `N=25`;
- realizations: `100`;
- theta grid: `0.25, 0.5, 0.75`;
- epsilon grid: `0.25, 0.5, 0.75`;
- resampling: `NeffCriterion(0.5, True)`;
- regularized transport: `scaling=0.9`,
  `convergence_threshold=1e-3`.

The paper and supplement state transition covariance `0.5 I_2`, while
executable filterflow uses `I_2`.  Prior bounded reruns showed the published
Table 1 scale is consistent with executable `I_2`, so this result treats the
paper statement as likely a typo or notation mismatch and records the
discrepancy explicitly.

## Comparison Matrix

| Lane | Status | Interpretation |
| --- | --- | --- |
| Paper Table 1 | `context_only` | Published context, not sole authority for executable comparison. |
| Exact Kalman | `pass` | BayesFilter and filterflow agree on the matched observation path; max absolute delta `7.26172e-08`. |
| Filterflow PF | `executed` | External classical baseline. |
| BayesFilter PF | `within_filterflow_mc_band` | Internal TF/TFP bootstrap PF calibration matched filterflow PF. |
| Filterflow RegularisedTransform | `executed` | External DPF reference. |
| BayesFilter filterflow-style transport | `within_filterflow_mc_band` | Matched paper-style annealed regularized transport semantics. |
| BayesFilter fixed-target Sinkhorn | `bayesfilter_veto_or_missing` | Diagnostic branch, not filterflow-equivalent. |
| BayesFilter LEDH-PF-PF-OT | `structured_not_run_as_matched_filterflow_table_lane` | Existing runner uses the repo fixture and proposal-correction diagnostics; not promoted to this filterflow-table comparison. |
| Smoothness/gradient contract | `finite_gradient_smoke_with_severe_unreconciled_magnitude_mismatch` | Finite-gradient smoke only; severe scalar/randomness/gradient-magnitude mismatch remains unreconciled. |

## Matched LGSSM Result

BayesFilter PF matched filterflow PF within the filterflow Monte Carlo band for
all three theta rows:

| theta | delta: BayesFilter minus filterflow | within filterflow SD |
| ---: | ---: | --- |
| `0.25` | `0.00430025` | true |
| `0.50` | `-0.00361567` | true |
| `0.75` | `0.0180054` | true |

BayesFilter filterflow-style annealed transport matched filterflow
RegularisedTransform within the filterflow Monte Carlo band for all nine
epsilon/theta cells:

| epsilon | theta | delta: BayesFilter minus filterflow | within filterflow SD |
| ---: | ---: | ---: | --- |
| `0.25` | `0.25` | `-0.0230848` | true |
| `0.25` | `0.50` | `-0.0164834` | true |
| `0.25` | `0.75` | `-0.0267869` | true |
| `0.50` | `0.25` | `-0.0225735` | true |
| `0.50` | `0.50` | `-0.0157859` | true |
| `0.50` | `0.75` | `-0.0199113` | true |
| `0.75` | `0.25` | `-0.0223452` | true |
| `0.75` | `0.50` | `-0.0161795` | true |
| `0.75` | `0.75` | `-0.0182495` | true |

BayesFilter fixed-target Sinkhorn matched only at epsilons `0.5` and `0.75`.
At epsilon `0.25`, the branch vetoed before producing matched likelihood
rows.  This is a branch-specific diagnostic gap, not evidence against
filterflow-style annealed transport.

## Smoothness/Gradient Result

The bounded filterflow smoothness/gradient smoke executed and produced finite
likelihoods and gradients:

| Metric | Value |
| --- | ---: |
| finite likelihoods | `true` |
| finite gradients | `true` |
| likelihood RMSE vs Kalman finite-diff surface | `323943.654172315` |
| gradient RMSE vs Kalman finite-diff surface | `144487904.8897196` |
| gradient max absolute delta | `511228982.96222275` |
| gradient cosine vs Kalman finite difference | `0.8895568190836275` |
| gradient sign agreement | `0.9375` |

This is finite-gradient smoke evidence only.  The large scale differences mean
it is not a gradient-agreement result and not a full supplement figure/table
reproduction.

## Fixed-Target Sinkhorn Result

The fixed-target Sinkhorn diagnostic reproduced and localized the epsilon
`0.25` issue:

| epsilon | budget | max residual | below tolerance |
| ---: | ---: | ---: | --- |
| `0.25` | `100` | `0.00012399118874682064` | false |
| `0.25` | `500` | `5.138093904899499e-06` | true |
| `0.25` | `1000` | `1.0097943943521148e-07` | true |

The probed initial cloud had ESS `25` for every row, so ESS-triggered
resampling would not occur.  The old fixed-target veto is therefore an
unconditional non-triggered computation plus iteration-budget issue in the
BayesFilter diagnostic branch.

## Red Flags

| ID | Severity | Status | Detail |
| --- | --- | --- | --- |
| `paper_transition_covariance_ambiguity` | medium | `recorded_and_controlled` | Paper/supplement says `0.5 I_2`; executable filterflow uses `I_2` and matches Table 1 scale. |
| `patched_filterflow_not_pristine` | medium | `recorded` | Local filterflow is a Python 3.11 compatibility branch. |
| `fixed_target_sinkhorn_not_paper_equivalent` | high | `epsilon_0.25_unconditional_nontriggered_budget_gap` | Fixed-target Sinkhorn remains diagnostic only. |
| `smoothness_gradient_severe_unreconciled_magnitude_mismatch` | high | `finite_gradient_smoke_with_severe_unreconciled_magnitude_mismatch` | Gradients are finite but severe scalar/randomness/gradient-magnitude mismatch remains unreconciled. |

## Verification

Executed:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py
```

Status: pass.

```bash
rg -n "import numpy|from numpy|student_dpf_baselines|vendor|highdim|NAWM|DSGE" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py
```

Status: no matches.

```bash
rg -n "[ \t]+$" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_full_comparison_tf.py
```

Status: no matches.

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_full_comparison_tf
```

Output:

```text
full_comparison_filterflow_reference_matched_with_fixed_sinkhorn_diagnostic_gap
```

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_full_comparison_tf --validate-only
```

Status: pass.

```bash
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_full_comparison_2026-05-31.json
```

Status: pass.

Pending final verification after Claude result review:

- lane-scoped trailing whitespace over all touched files;
- `git diff --check`;
- `git status --short -- bayesfilter tests docs/chapters`;
- `git status --short --branch`.

## Unresolved Risks

- The local `filterflow` checkout is patched for Python 3.11 compatibility and
  is not pristine upstream source.
- The paper/code transition covariance discrepancy remains a source ambiguity,
  although the executable `I_2` convention is the only version currently
  matching the paper table scale.
- The BayesFilter fixed-target Sinkhorn branch is not paper-equivalent and
  still has a concrete epsilon `0.25` diagnostic gap.
- The smoothness/gradient smoke has finite gradients but large scale
  differences versus Kalman finite-difference diagnostics.
- LEDH-PF-PF-OT was not included as a matched filterflow-table lane because the
  existing runner does not produce the exact matched filterflow protocol and
  scalar without additional work.

## Blockers

No blocker remains for the full comparison result itself.  The remaining items
are scoped risks and follow-up implementation tasks.

## Next Recommended Action

Patch the BayesFilter fixed-target Sinkhorn diagnostic branch so it does not
compute Sinkhorn on rows where ESS does not trigger resampling, then rerun the
full comparison to confirm that the epsilon `0.25` veto disappears from
non-triggered initial rows.  Keep that patch separate from the paper-style
filterflow annealed transport mirror.
