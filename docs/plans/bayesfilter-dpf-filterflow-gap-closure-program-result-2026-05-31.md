# Result: Filterflow Gap-Closure Program For BayesFilter OT-DPF

## Decision

`ACCEPTED_WITH_SEVERE_UNRECONCILED_GRADIENT_MISMATCH_RISK`

## Scope

This result records the reviewed gap-closure program for the BayesFilter
experimental TF/TFP OT-DPF lane versus the patched Corenflos/JTT94
`filterflow` reference. It closes or narrows the six requested gaps without
editing production `bayesfilter/`, `tests/`, monograph chapters, the
high-dimensional filtering lane, vendored student code, DSGE/NAWM-specific
code, or `.localsource/filterflow` source.

Plan:
`docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-plan-2026-05-31.md`

Primary result artifacts:

- `experiments/dpf_implementation/reports/dpf-filterflow-gap-closure-program-2026-05-31.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_gap_closure_program_2026-05-31.json`
- `experiments/dpf_implementation/reports/dpf-filterflow-full-comparison-2026-05-31.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_full_comparison_2026-05-31.json`
- `experiments/dpf_implementation/reports/dpf-filterflow-matched-ledh-pfpf-ot-2026-05-31.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_matched_ledh_pfpf_ot_2026-05-31.json`
- `experiments/dpf_implementation/reports/dpf-filterflow-smoothness-gradient-audit-2026-05-31.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_smoothness_gradient_audit_2026-05-31.json`

## Claude Review

| Artifact | Iterations | Status | Notes |
| --- | ---: | --- | --- |
| plan | 1 | `ACCEPT` | Claude Code accepted the plan before execution. |
| result | 2 | `ACCEPT` | Iteration 1 rejected only because review status fields still said pending; Codex agreed, patched the ledger/status fields, and Claude accepted iteration 2. |

Required command:

```bash
claude -p --model claude-opus-4-7 --effort max
```

## Files Changed

- `docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-plan-2026-05-31.md`
- `docs/plans/bayesfilter-dpf-filterflow-gap-closure-program-result-2026-05-31.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_lgssm_matched_cross_audit_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_matched_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_gradient_audit_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_gap_closure_program_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-gap-closure-program-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-full-comparison-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-matched-ledh-pfpf-ot-2026-05-31.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-smoothness-gradient-audit-2026-05-31.md`
- JSON outputs under `experiments/dpf_implementation/reports/outputs/`

No production `bayesfilter/`, `tests/`, or `docs/chapters/` files were edited
by this program.

## Gap Closure Summary

| Gap | Status | Evidence |
| --- | --- | --- |
| fixed-target Sinkhorn ESS gating | `closed_nontriggered_veto_removed` | In the matched audit path, fixed-target Sinkhorn is now computed only on ESS-triggered rows. Non-triggered rows are skipped and no longer veto. |
| filterflow-style annealed transport | `within_filterflow_mc_band` | Preserved as the Corenflos/filterflow paper-style reference path and still within filterflow Monte Carlo bands across the nine epsilon/theta cells. |
| matched LEDH-PF-PF-OT LGSSM runner | `finite_diagnostics` | Bounded matched protocol produced 27 finite rows, finite PF-PF corrected weights, finite log-det diagnostics, finite ESS, and finite Sinkhorn residuals. |
| gradient/smoothness audit | `finite_gradient_smoke_with_severe_unreconciled_magnitude_warning` | Filterflow gradients are finite, but scalar/gradient-magnitude mismatch remains severe; gradient agreement is not concluded. |
| filterflow environment freeze | `recorded_and_smoke_passed` | Branch, commit, local diff summary, Python/package versions, CPU-only command, and smoke status were recorded. |
| covariance ambiguity ledger | `recorded_permanent_note` | Paper/supplement say `0.5 I_2`; executable filterflow uses `I_2`; current comparisons use executable `I_2` because prior bounded reruns match Table 1 scale. |

## Fixed-Target Sinkhorn Gating

The experimental matched audit path now gates fixed-target Sinkhorn by the
actual ESS trigger. If ESS does not trigger resampling, the row records
no-resampling status and skipped Sinkhorn rows; Sinkhorn residuals from those
non-triggered rows do not veto.

Post-patch status:

- full comparison decision:
  `full_comparison_filterflow_reference_matched_with_fixed_sinkhorn_diagnostic_gap`
- fixed-target Sinkhorn table status: `within_filterflow_mc_band`
- non-triggered initial-row residual ladder remains only as an unconditional
  component diagnostic, not as filterflow-equivalence evidence.

The earlier epsilon `0.25` non-triggered-row veto has been removed from the
matched filter path. The residual-budget ladder still records that unconditional
fixed-Sinkhorn diagnostics can show a small residual budget gap at epsilon
`0.25`; that is now explicitly scoped as a diagnostic branch.

## Filterflow-Style Transport

The filterflow-style annealed transport mirror remains the paper-matched OT
reference. It is not replaced by the fixed-target Sinkhorn diagnostic path.

Status:

- BayesFilter filterflow-style transport: `within_filterflow_mc_band`
- filterflow RegularisedTransform comparison: all nine epsilon/theta cells
  remain within one filterflow standard deviation in the refreshed full
  comparison artifact.

## Matched LEDH-PF-PF-OT

Runner:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_matched_ledh_pfpf_ot_tf
```

Result:

| Metric | Value |
| --- | ---: |
| rows | 27 |
| executed rows | 27 |
| finite rows | 27 |
| nonfinite rows | 0 |
| max abs error per time | 0.015366632407813465 |
| max Sinkhorn residual | 9.479688597990865e-08 |
| max abs corrected log weight | 14.856345448972045 |
| min Jacobian singular value | 0.30151134457776363 |

Interpretation: LEDH-PF-PF-OT has finite bounded diagnostics on the matched
filterflow LGSSM protocol. It is not required to match filterflow
RegularisedTransform exactly because it is a different proposal.

## Smoothness And Gradient Audit

Runner:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_smoothness_gradient_audit_tf
```

Result:

| Metric | Value |
| --- | ---: |
| status | `severe_unreconciled_gradient_magnitude_mismatch_risk_recorded` |
| horizon | 100 |
| total likelihood RMSE | 323943.654172315 |
| per-time likelihood RMSE | 3239.4365417231497 |
| total gradient RMSE | 144487904.8897196 |
| per-time gradient RMSE proxy | 1444879.048897196 |
| gradient norm ratio DPF/Kalman FD | 137214.58717183248 |
| gradient cosine vs Kalman FD | 0.8895568190836275 |
| gradient sign agreement | 0.9375 |

Interpretation: finite gradients are smoke evidence only. Total/per-time
normalization and sign/cosine diagnostics do not reconcile the severe gradient
magnitude mismatch. A same-scalar BayesFilter `GradientTape` surface was
recorded as a structured scope limit pending scalar-contract reconciliation.

## Filterflow Reference Freeze

| Key | Value |
| --- | --- |
| branch | `bayesfilter-py311-compat` |
| commit | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| upstream base | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| source status | local Python 3.11 compatibility branch with modified `scripts/base.py`, `scripts/simple_linear_common.py`, and `scripts/simple_linear_smoothness.py` |
| Python | `3.11.14` |
| TensorFlow | `2.19.1` |
| NumPy | `1.26.4` |
| smoke status | `pass` |
| CPU policy | `CUDA_VISIBLE_DEVICES=-1` |

Patched filterflow remains external reference code, not BayesFilter
implementation code.

## Covariance Ambiguity Ledger

Permanent note:

- paper/supplement statement: transition covariance `0.5 I_2`
- executable filterflow setting: transition covariance `I_2`
- current reproduction policy: use executable filterflow `I_2` for code
  comparisons because prior bounded reruns indicate Table 1 scale matches
  executable `I_2`
- reversal condition: a separate paper-notation audit overturns the executable
  code interpretation

## Verification

| Command | Result |
| --- | --- |
| `python -m py_compile ...run_filterflow_lgssm_matched_cross_audit_tf.py ...run_filterflow_full_comparison_tf.py` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_full_comparison_tf` | pass, `full_comparison_filterflow_reference_matched_with_fixed_sinkhorn_diagnostic_gap` |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_full_comparison_tf --validate-only` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_gap_closure_program_tf` | pass, `filterflow_gap_closure_program_completed_with_severe_unreconciled_gradient_mismatch_risk` |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_gap_closure_program_tf --validate-only` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_matched_ledh_pfpf_ot_tf` | pass, `matched_ledh_pfpf_ot_finite_diagnostics` |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_matched_ledh_pfpf_ot_tf --validate-only` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_smoothness_gradient_audit_tf` | pass, `smoothness_gradient_severe_unreconciled_magnitude_risk_recorded` |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_smoothness_gradient_audit_tf --validate-only` | pass |
| `python -m json.tool` on the four 2026-05-31 JSON outputs and the matched cross-audit JSON | pass |
| `rg -n "import numpy\|from numpy"` on touched BayesFilter runners | pass, no matches |
| `rg -n "student\|vendored\|vendor\|highdim\|DSGE\|NAWM"` on touched BayesFilter runners | pass, no matches |

Notes:

- TensorFlow emitted CUDA plugin-registration and `cuInit` warnings even under
  `CUDA_VISIBLE_DEVICES=-1`; the run manifests record CPU-only execution and no
  visible GPU devices.
- Matplotlib warned that `/home/chakwong/.config/matplotlib` was not writable
  and used temporary cache directories; this did not affect the evidence.

## Remaining Risks

- Gradient/smoothness agreement is not established. The bounded audit found
  finite gradients but a large scalar/gradient scale gap versus Kalman
  finite-difference diagnostics.
- Fixed-target Sinkhorn remains diagnostic and is not filterflow-equivalent
  unless separately derived and verified.
- The matched LEDH-PF-PF-OT run is bounded diagnostic evidence, not a full
  production or general nonlinear-SSM validation.
- The local filterflow reference is patched for Python 3.11 compatibility and
  is not pristine upstream source.
- The paper/code transition covariance ambiguity is controlled but not
  mathematically resolved.
- The worktree contains substantial unrelated pre-existing dirty and untracked
  files; those were preserved.

## Blockers

No execution blocker remains for the six requested gap-closure items. The
gradient scalar-contract mismatch is an unresolved research risk, not a blocker
to recording this gap-closure result.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Record gap-closure program as accepted with severe unreconciled gradient-magnitude risk | Five of six gaps closed or controlled; gradient gap narrowed to explicit scalar-contract risk | No lane, production, monograph, highdim, vendored, or DSGE/NAWM veto triggered | Severe smoothness-gradient scalar/magnitude mismatch | Build a same-scalar BayesFilter `GradientTape` smoothness harness and reconcile filterflow/Kalman scalar normalization before using gradient comparisons as validation | production readiness, posterior correctness, HMC readiness, general nonlinear-SSM validity, fixed-target/filterflow equivalence |

## Next Action

Create a narrow reviewed follow-up plan for the smoothness-gradient scalar
contract: identify the exact objective used by filterflow Appendix E.1,
construct the same scalar in BayesFilter TF/TFP with fixed observations and
common random numbers, and compare against Kalman analytic or finite-difference
gradients before drawing any gradient-correctness conclusion.
