# Annealed Transport Reference Alignment

## Decision

`ANNEALED_TRANSPORT_REFERENCE_ALIGNMENT_BLOCKED_MAX_REVIEW_ROUNDS_REACHED_AFTER_PATCHES`

## Gap Status

| Gap | Status | Evidence |
| --- | --- | --- |
| reference hierarchy | `locked` | fixed-target Sinkhorn is local comparator only; patched executable filterflow is canonical executable reference; executable `I_2` is reproduction setting |
| reusable annealed transport | `implemented` | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py` |
| annealed transport OT default | `wired_experimental` | `run_ot_dpf_tf` and `run_ledh_pfpf_ot_tf` default to `annealed_transport`; fixed-target Sinkhorn remains selectable comparator |
| LGSSM reusable component match | `matched_filterflow` | nine of nine epsilon/theta cells within filterflow Monte Carlo band |
| gradient/smoothness scalar contract | `severe_unreconciled_magnitude_risk_recorded` | BayesFilter GradientTape surface finite, but agreement not concluded |
| LEDH-PF-PF annealed transport | `finite_diagnostics` | 27/27 finite rows on matched LGSSM protocol |
| nonlinear ladder | `executed_with_caveats` | range-bearing, SV, structural AR(1) bounded diagnostics executed; no general nonlinear validity concluded |
| Claude result review | `blocked_max_review_rounds_reached_after_patches` | result review reached five `REJECT` rounds; accepted bookkeeping findings were patched, but Claude did not converge to `ACCEPT` |

## Key Results

| Check | Result |
| --- | --- |
| component match decision | `annealed_transport_component_matched_filterflow` |
| component match cells | `9/9` |
| component max absolute delta | `0.026786881508458538` |
| component max column residual | `2.1316282072803006e-14` |
| gradient contract decision | `annealed_transport_gradient_contract_severe_unreconciled_magnitude_risk_recorded` |
| BayesFilter gradient finite | `True` |
| LEDH decision | `ledh_pfpf_annealed_transport_lgssm_finite_diagnostics` |
| LEDH finite rows | `27/27` |
| LEDH max transport residual | `3.552713678800501e-15` |
| nonlinear ladder decision | `nonlinear_ladder_annealed_transport_executed_with_caveats` |

## Reference Hierarchy

- Fixed-target Sinkhorn is a BayesFilter local diagnostic/comparator only.
- Patched executable filterflow is the canonical executable reference for this
  audit/reproduction lane.
- Executable filterflow `I_2` transition covariance is the reproduction
  setting. The paper/supplement `0.5 I_2` text is treated as a likely typo or
  notation ambiguity unless a future audit overturns this.

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No DSGE/NAWM validation is concluded.
- No banking/model-risk claim is concluded.
- No monograph claim is concluded.
- Finite gradients alone do not establish gradient correctness.

## Continuation Governance Review

`GOVERNANCE_BLOCKER_CLOSED_FOR_INSPECTION_BY_CONTINUATION_REVIEW_ROUND_6`

The 2026-06-01 continuation review accepted the prior max-round bookkeeping
state as governance closure for inspection only. Technical gradient
reconciliation remains separate and non-promotional.
