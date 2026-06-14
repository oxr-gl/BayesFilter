# Result: OT-DPF Annealed Transport Remaining-Gaps Closure

## Decision

`GOVERNANCE_CLOSED_WRONG_MODEL_GRADIENT_GAP_CLOSED_GRADIENT_AGREEMENT_BLOCKED`

## Scope

This result records the continuation closure program for the BayesFilter-owned
experimental TF/TFP OT-DPF annealed-transport lane. It follows
`docs/plans/bayesfilter-dpf-annealed-transport-reference-alignment-result-2026-05-31.md`
and keeps all implementation under `experiments/dpf_implementation/tf_tfp/`.

No production `bayesfilter/`, `tests/`, monograph chapters, high-dimensional
lane artifacts, vendored student code, DSGE/NAWM artifacts, or
`.localsource/filterflow` source files were edited.

Plan:
`docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-plan-2026-06-01.md`

Review loop:
`docs/plans/bayesfilter-dpf-annealed-transport-remaining-gaps-closure-review-loop-2026-06-01.md`

## Governance Closure Status

`CLOSED_FOR_INSPECTION_BY_CLAUDE_CONTINUATION_ROUND_6`

The user authorized three additional Claude result-review rounds after the
previous five-round max-review block. Claude accepted continuation round 6 as
governance closure for inspection only: the prior bookkeeping blocker is
resolved, and remaining risks are correctly classified as non-promotional
caveats.

This governance closure does not establish gradient correctness, production
readiness, posterior correctness, HMC readiness, or general nonlinear-SSM
validity.

## Same-Model Gradient Diagnostic Status

Runner:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_smoothness_same_model_gradient_reconciliation_tf
```

Decision:
`same_model_gradient_wrong_model_gap_closed_gradient_agreement_not_concluded`

The prior BayesFilter gradient harness used the wrong model for the smoothness
question: the Section 5.1 two-observation LGSSM. The new runner uses the
filterflow smoothness constant-velocity LGSSM:

- `A(theta)=diag(theta_1, theta_2)+[[0,1],[0,0]]`;
- transition covariance `[[1/3, 1/2], [1/2, 1]]`;
- observation matrix `[[1,0]]`;
- observation covariance `[[0.01]]`;
- `T=100`, `mesh_size=4`, `N=25`, `batch_size=1`;
- `epsilon=0.25`, `scaling=0.85`, `convergence_threshold=1e-6`,
  `max_iter=200`;
- `NeffCriterion(0.9999, True)`;
- filterflow observations and initial particles exported from the local
  executable reference without mutating filterflow.

Key same-model diagnostics:

| Metric | Value |
| --- | ---: |
| rows | 16 |
| finite rows | 16 |
| BayesFilter likelihood RMSE vs filterflow | 184345.80209129627 |
| BayesFilter likelihood RMSE vs Kalman | 490562.36155074654 |
| filterflow likelihood RMSE vs Kalman | 323943.654172315 |
| BayesFilter gradient RMSE vs filterflow | 2.537001953821507e+145 |
| BayesFilter gradient RMSE vs Kalman | 2.537001953821507e+145 |
| filterflow gradient RMSE vs Kalman | 144487904.88971964 |
| BayesFilter gradient cosine vs filterflow | -0.014110786351377623 |
| BayesFilter gradient cosine vs Kalman | -0.06569613949112281 |
| filterflow gradient cosine vs Kalman | 0.8895568190836276 |

Interpretation:
the wrong-model gap is closed, and BayesFilter likelihoods/gradients are finite
on the same smoothness model. However, gradient agreement is decisively not
established. Scalar comparability also remains an explicit open blocker for
gradient agreement: even executable filterflow's smoothness DPF likelihoods are
far from Kalman on this bounded run, and BayesFilter is farther still. The
remaining technical blocker is therefore a same-model scalar/randomness/
transport-gradient/numerical-stability gap, not merely a wrong-model issue.

## Scientific Validity Limits

| Gap | Status | Interpretation |
| --- | --- | --- |
| Claude max-review governance block | `closed_for_inspection` | Continuation round 6 accepted the bookkeeping/classification state. |
| Wrong smoothness model in BayesFilter gradient harness | `closed` | New runner uses filterflow smoothness model and records model/seed/scalar contracts. |
| Scalar comparability for gradient validation | `open_blocking_for_gradient_agreement` | Same-model scalar definitions are recorded, but likelihood scales remain far apart, including filterflow versus Kalman. |
| Gradient agreement | `blocked` | Same-model finite diagnostics show huge magnitude/sign mismatch. |
| Bit-identical filterflow random stream | `open_controlled` | Observations and initial particles are extracted, but BayesFilter transition noises use a stateless CRN surrogate, not filterflow's internal `split_seed` stream. |
| Nonlinear ladder | `controlled_caveat` | Still bounded diagnostics only; no general nonlinear validity. |
| Patched filterflow reference | `controlled_caveat` | Canonical executable reference for this audit lane, not pristine upstream. |
| Fixed-target Sinkhorn | `controlled_caveat` | Local comparator only; annealed transport remains experimental OT default. |

## Artifacts

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_same_model_gradient_reconciliation_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-smoothness-same-model-gradient-reconciliation-2026-06-01.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_smoothness_same_model_gradient_reconciliation_2026-06-01.json`
- `experiments/dpf_implementation/reports/dpf-annealed-transport-remaining-gaps-closure-2026-06-01.md`
- `experiments/dpf_implementation/reports/outputs/dpf_annealed_transport_remaining_gaps_closure_2026-06-01.json`

## Claude Review

Plan review:

| Round | Claude status | Codex status |
| ---: | --- | --- |
| 1 | `REJECT` | accepted findings; patched append-only, scalar, stop-condition, verification, and ledger-separation controls |
| 2 | `ACCEPT` | Codex independently agreed |

Governance continuation review:

| Round | Claude status | Codex status |
| ---: | --- | --- |
| 6 | `ACCEPT` | prior max-review bookkeeping blocker closed for inspection only |

Result review:

| Round | Claude status | Codex status |
| ---: | --- | --- |
| 1 | `REJECT` | accepted findings; patched scalar-comparability caveat and verification placeholders |
| 2 | `ACCEPT` | Codex independently agreed; no patch required |

## Verification

Executed after result-review round 1 patches:

| Command | Result |
| --- | --- |
| `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_smoothness_same_model_gradient_reconciliation_tf.py` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_smoothness_same_model_gradient_reconciliation_tf` | pass |
| `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_smoothness_same_model_gradient_reconciliation_tf --validate-only` | pass |
| `python -m json.tool` on same-model and remaining-gaps JSON outputs | pass |
| schema check for `model_contract`, `seed_contract`, `scalar_contract`, `decision_table`, `caveat_ledger`, seeds, and initial-particle checksum | pass |
| NumPy import gate on touched BayesFilter TF/TFP runner | pass; no module-scope NumPy import |
| forbidden import-boundary search for student/vendored/highdim/DSGE/NAWM imports | pass; no matches |
| result-summary check for governance, same-model, scientific-validity, caveat, and decision-table text | pass |
| lane-scoped trailing whitespace check | pass |

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Accept governance closure for inspection | Claude continuation round 6 accepted bookkeeping/classification state | no governance major blocker remains | technical gradient mismatch remains | proceed with same-model gradient diagnostics, not promotion | gradient correctness, production readiness, scientific validity |
| Close wrong-model gradient harness gap | BayesFilter now uses filterflow smoothness LGSSM and recorded model/seed/scalar contracts | finite rows pass | bit-identical filterflow transition-noise stream not reconstructed | derive/export exact filterflow random stream or audit annealed-transport gradient numerics | gradient agreement |
| Keep gradient agreement blocked | same-model likelihood and gradient magnitude/sign mismatch remains severe | gradient promotion vetoed | source could be scalar comparability, CRN mismatch, transport-gradient instability, or remaining implementation discrepancy | create a narrower component-level gradient audit for one time step and exact transport matrix/potential derivatives | posterior correctness, HMC readiness, general nonlinear-SSM validity |

## Next Action

Create a narrow one-step annealed-transport gradient audit that exports a single
filterflow pre-resampling particle cloud, log weights, transport matrix, and
post-resampling cloud, then compares BayesFilter TF/TFP transport values and
Jacobian-vector products against the executable filterflow component. This is
the smallest next artifact that can distinguish random-stream mismatch from
transport-gradient implementation mismatch.
