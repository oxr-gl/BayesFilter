# Result: OT-DPF Reference Alignment And Annealed Transport Gap Closure

## Decision

`BLOCKED_MAX_REVIEW_ROUNDS_REACHED_AFTER_PATCHES`

## Scope

This result records the reviewed BayesFilter-owned experimental TF/TFP OT-DPF
reference-alignment and annealed-transport gap-closure program. It implements a
first-class filterflow-style annealed transport component, demotes fixed-target
Sinkhorn to comparator/diagnostic status, and executes bounded LGSSM,
gradient-contract, LEDH, and nonlinear-ladder evidence without editing
production `bayesfilter/`, `tests/`, monograph chapters, the high-dimensional
lane, vendored student code, DSGE/NAWM-specific artifacts, or
`.localsource/filterflow` source.

Plan:
`docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-plan-2026-05-31.md`

Review loop:
`docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-review-loop-2026-05-31.md`

Consolidated report:
`experiments/dpf_implementation/reports/dpf-annealed-transport-reference-alignment-2026-05-31.md`

## Claude Review

| Artifact | Iterations | Claude status | Codex-supervisor status |
| --- | ---: | --- | --- |
| plan | 1 | `ACCEPT` | all findings classified `ACCEPT`; no patch required beyond ledger entry |
| result | 5 | `REJECT_MAX_ROUNDS_REACHED` | Rounds 1-5 patched accepted bookkeeping and stale gradient-risk wording findings; Claude did not converge to `ACCEPT`, so downstream acceptance is blocked pending human decision or explicit authorization for another review round |

## Codex-Supervisor Audit Classifications

Plan review round 1 classifications:

- `ACCEPT`: reference hierarchy/write-boundary controls were already present.
- `ACCEPT`: annealed transport, gradient, LEDH, nonlinear, stop, and
  verification controls were already present.
- `ACCEPT`: phase order matched the requested seven-gap sequence.
- `ACCEPT`: Claude/Codex review protocol was already present.
- `ACCEPT`: the initially empty review ledger was expected before first review;
  the control added was the Round 1 ledger entry.

Result review round 1 classifications:

- `ACCEPT`: result review-loop placeholders were incomplete; patched this
  result and the review-loop ledger.
- `ACCEPT`: acceptance/no-blocker wording was premature before result review
  completion; patched decision/status for resubmission.
- `PARTIAL`: gradient evidence was already caveated, but the wording
  understated the severe unresolved gradient magnitude mismatch; patched the
  risk wording.
- `ACCEPT`: Claude positive checks required no patch.

Result review round 2 classifications:

- `ACCEPT`: stale softer gradient decision label remained in the gradient
  subsection; patched to severe unreconciled magnitude risk.
- `ACCEPT`: Claude positive checks required no patch.

Result review rounds 3-5 classifications:

- `ACCEPT`: consolidated/top-level report and summary JSON had stale softer
  gradient-risk labels; patched to severe unresolved gradient-magnitude risk.
- `ACCEPT`: prior gap-closure, full-comparison, and final-gaps generator
  defaults and outputs had stale pending-review or softer gradient-warning
  labels; patched status strings and regenerated affected reports/JSON.
- `ACCEPT`: top-level acceptance wording was no longer valid after five Claude
  result-review rejections; patched this result/report/summary to blocked
  max-review-rounds status.

## Files Changed

- `docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-plan-2026-05-31.md`
- `docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-result-2026-05-31.md`
- `docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-review-loop-2026-05-31.md`
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/common_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_matched_ledh_pfpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_component_match_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_annealed_transport_gradient_contract_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_ledh_pfpf_annealed_transport_lgssm_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_nonlinear_ladder_annealed_transport_tf.py`
- report and JSON outputs under `experiments/dpf_implementation/reports/`

No production `bayesfilter/`, `tests/`, or `docs/chapters/` files were edited.

## Reference Hierarchy Status

`LOCKED`

- Fixed-target Sinkhorn is a local BayesFilter exploratory/comparator path, not
  the Corenflos/filterflow algorithm and not paper-authoritative.
- The patched executable filterflow checkout is the canonical executable
  filterflow reference for this audit/reproduction lane.
- Executable filterflow `I_2` transition covariance is the correct
  reproduction setting; paper/supplement `0.5 I_2` is treated as likely typo or
  notation ambiguity unless future audit overturns it.

## Annealed Transport Component Status

`IMPLEMENTED`

Implemented:
`experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`

The component implements filterflow RegularisedTransform-style annealed
transport with:

- TF/TFP implementation backend;
- batched particles/log weights;
- optional ESS mask with skipped-row preservation;
- filterflow-style centering and cost scaling;
- annealed potential iteration schedule;
- transform matrix and transported particles;
- finite checks and diagnostics;
- explicit `fixed_target_sinkhorn_status` saying fixed-target Sinkhorn is not
  this algorithm.

## Experimental OT Default Status

`WIRED_EXPERIMENTAL`

`run_ot_dpf_tf` and `run_ledh_pfpf_ot_tf` now default to
`transport_method="annealed_transport"`. The old fixed-target Sinkhorn path is
still available only via `transport_method="fixed_target_sinkhorn"` and is
labelled `fixed_target_sinkhorn_local_comparator_tf`.

## LGSSM Reusable-Component Match

Runner:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_annealed_transport_component_match_tf
```

Decision: `annealed_transport_component_matched_filterflow`

| Metric | Value |
| --- | ---: |
| rows | 9 |
| within filterflow MC band | 9 |
| nonfinite rows | 0 |
| max abs delta | 0.026786881508458538 |
| max transform row diagnostic | 0.5659112334251404 |
| max column residual | 2.1316282072803006e-14 |
| min triggered rows | 14900 |

The reusable component, not the old inline audit mirror, matches the canonical
executable filterflow RegularisedTransform reference across all nine
epsilon/theta cells.

The column residual is the filterflow-style source-weight consistency check.
The row-sum quantity is retained as a transform diagnostic, not a finite
Sinkhorn marginal-veto criterion.

## Gradient/Smoothness Scalar Contract

Runner:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_annealed_transport_gradient_contract_tf
```

Decision: `annealed_transport_gradient_contract_severe_unreconciled_magnitude_risk_recorded`

| Metric | Value |
| --- | --- |
| filterflow scalar | `total_log_likelihood_from_simple_linear_smoothness` |
| BayesFilter scalar | `total_log_likelihood_common_observations_common_random_numbers` |
| filterflow gradient count | `16` |
| BayesFilter gradient count | `16` |
| BayesFilter gradients finite | `True` |
| gradient claim status | `finite_gradient_smoke_not_agreement` |

Interpretation: BayesFilter `GradientTape` gradients are finite, but gradient
agreement is not concluded. The remaining issue is a severe unreconciled
scalar/randomness/gradient-magnitude mismatch, not basic differentiability.

## LEDH-PF-PF Annealed Transport

Runner:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_annealed_transport_lgssm_tf
```

Decision: `ledh_pfpf_annealed_transport_lgssm_finite_diagnostics`

| Metric | Value |
| --- | ---: |
| rows | 27 |
| finite rows | 27 |
| nonfinite rows | 0 |
| max abs error per time | 0.015512713400855773 |
| max transport residual | 3.552713678800501e-15 |
| max abs corrected log weight | 14.856345448972045 |
| min Jacobian singular value | 0.30151134457776363 |

LEDH remains a different proposal from filterflow RegularisedTransform; exact
likelihood-table equality is not required or claimed.

## Nonlinear Ladder

Runner:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_nonlinear_ladder_annealed_transport_tf
```

Decision: `nonlinear_ladder_annealed_transport_executed_with_caveats`

| Model | Source decision | Interpretation |
| --- | --- | --- |
| range-bearing | `DPF_NONLINEAR_SSM_RANGE_BEARING_STRESS_PASSED` | UKF approximate diagnostic; no ground truth claim |
| stochastic volatility | `DPF_NONLINEAR_SSM_SV_GRADIENT_MLE_PASSED_SMOKE` | CUT4 differentiable comparator; smoke only |
| structural AR(1) | `DPF_STRUCTURAL_INTERFACE_NONLINEAR_AR1_EXECUTED_WITH_POLICY_LADDER` | CUT4 comparator and deterministic residual contract |

This is bounded nonlinear evidence after annealed-transport default wiring; it
does not establish general nonlinear-SSM validity.

## Verification

| Command | Result |
| --- | --- |
| `python -m py_compile` on touched Python files | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_annealed_transport_component_match_tf` | pass |
| `...run_filterflow_annealed_transport_component_match_tf --validate-only` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_annealed_transport_gradient_contract_tf` | pass |
| `...run_filterflow_annealed_transport_gradient_contract_tf --validate-only` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_annealed_transport_lgssm_tf` | pass |
| `...run_ledh_pfpf_annealed_transport_lgssm_tf --validate-only` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_nonlinear_ladder_annealed_transport_tf` | pass |
| `...run_nonlinear_ladder_annealed_transport_tf --validate-only` | pass |
| `python -m json.tool` on new 2026-05-31 JSON outputs | pass |
| `rg -n "import numpy\|from numpy"` on touched BayesFilter TF/TFP files | pass, no matches |
| import-boundary search for `student/vendored/vendor/highdim/DSGE/NAWM` on touched TF/TFP files | pass for imports; one caveat string says no DSGE/NAWM validation |
| lane-scoped trailing-whitespace check | pass |
| `git diff --check` | pass |
| `git status --short -- bayesfilter tests docs/chapters` | pass, no output |

CPU-only note: runners set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import.
TensorFlow emitted CUDA plugin-registration and `cuInit` warnings despite
hidden GPUs; manifests record CPU-only execution. Matplotlib emitted cache
directory warnings; those did not affect the evidence.

## Unresolved Risks

- Gradient agreement is not established. The BayesFilter same-scalar surface is
  finite, but filterflow/BayesFilter scalar randomness and gradient-magnitude
  reconciliation remains severely unresolved.
- The nonlinear ladder is bounded diagnostic evidence only.
- Patched filterflow is canonical executable reference for this audit lane but
  remains a local compatibility-patched checkout.
- Fixed-target Sinkhorn remains available as comparator and must not be
  re-promoted without separate derivation/review.
- Worktree contains substantial unrelated dirty/untracked files preserved from
  prior work.

## Blockers

Execution completed for the seven requested gap-closure phases, but result
review did not converge to Claude `ACCEPT` within five rounds. Downstream
acceptance is therefore blocked pending human decision or explicit
authorization for another review round. The gradient scalar-contract issue
remains a severe unresolved risk and next-step target.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Hold for human decision after max review rounds | LGSSM reusable component matches filterflow; LEDH and nonlinear bounded diagnostics execute | no production/test/monograph/highdim/vendored/DSGE/NAWM edits; finite diagnostics pass; Claude result review did not converge to `ACCEPT` within five rounds | severe unresolved gradient scalar/randomness/magnitude mismatch and max-review governance block | decide whether to accept the patched artifacts for inspection or authorize one additional Claude review; then build a stricter same-randomness gradient reproduction | production readiness, posterior correctness, HMC readiness, general nonlinear-SSM validity |

## Next Action

Create a narrow gradient-reconciliation plan that compares the same exact
objective, observations, particles/noises, sign, and normalization between
filterflow and BayesFilter, then checks against Kalman analytic or
finite-difference gradients.

## Continuation Governance Review

`GOVERNANCE_BLOCKER_CLOSED_FOR_INSPECTION_BY_CONTINUATION_REVIEW_ROUND_6`

On 2026-06-01, the user authorized three additional Claude result-review rounds.
Claude accepted continuation round 6 as governance closure for inspection:
the prior max-round bookkeeping blocker is resolved, and the remaining issues
are properly classified as non-promotional caveats. This does not close the
technical gradient-reconciliation gap and does not promote production,
posterior, HMC, or general nonlinear-SSM readiness.

Continuation artifacts:

- `docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-plan-2026-06-01.md`
- `docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-review-loop-2026-06-01.md`
