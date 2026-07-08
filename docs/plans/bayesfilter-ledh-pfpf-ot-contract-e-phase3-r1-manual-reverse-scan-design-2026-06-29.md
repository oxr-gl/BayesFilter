# Contract E Phase 3 Manual Reverse-Scan Design

Date: 2026-06-29

Status: `R1_DESIGN_ONLY`

Subplan:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-design-subplan-2026-06-29.md`

Route manifest:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-route-manifest-2026-06-29.json`

## Purpose

This design binds the intended Contract E Phase 3 score route before any
gradient implementation or material rerun.  The current Phase 3 diagnostic has
only a transport-level manual VJP and an outer generic score tape; that route
remains non-promotable.

The future material route is:

```text
manual_likelihood_reverse_scan_no_autodiff
```

Material mode remains blocked by:

```text
PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN
```

## Source Anchors

| Role | Path | Anchor |
| --- | --- | --- |
| Current blocked Phase 3 scalar | `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py` | `_make_compiled_contract_e` |
| Current blocked taped score diagnostic | `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py` | `_make_compiled_value_and_gradient` |
| Existing manual LGSSM score pattern | `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py` | `_lgssm_manual_value_and_score` |
| Existing manual transport forward | `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py` | `_transport_forward` |
| Existing manual transport VJP | `tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py` | `_transport_vjp` |
| Manual LEDH flow VJP | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py` | `_batched_ledh_linearized_flow_vjp` |
| Manual log-weight VJP | `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py` | `_normalize_log_weights_with_floor_vjp`, `_log_weight_correction_vjp` |

## Reverse-Scan Shape

The future route should follow the old LGSSM manual score structure:

1. Forward `tf.while_loop`:
   store all quantities needed by a hand-coded reverse pass.
2. Reverse `tf.while_loop`:
   propagate cotangents backward through transport, normalization, log-density
   corrections, LEDH flow, reparameterized transition noise, and the LGSSM
   parameterization.
3. Score accumulation:
   accumulate three LGSSM parameter cotangents per seed.

No Python loops are allowed inside the XLA-critical score route.  Diagnostic
Python orchestration outside compiled route construction remains separate from
the material route.

## Boundary Table

| ID | Boundary | Existing source anchor | R1 classification | R2/R3 action |
| --- | --- | --- | --- | --- |
| B01 | LGSSM parameterization to transition matrix and covariances | `_theta_to_lgssm` | manual carry already present in old route | Reuse old score accumulation formulas. |
| B02 | Fixed initial particles and transition noise reparameterization | `_lgssm_manual_value_and_score` | manual carry already present in old route | Preserve fixed-noise seed schedule. |
| B03 | LEDH affine flow | `_batched_ledh_linearized_flow_with_aux_tf`, `_batched_ledh_linearized_flow_vjp` | manual VJP available | Reuse checkpoint structure. |
| B04 | Transition log density | `_transition_gaussian_log_density_vjp` | manual VJP available | Reuse. |
| B05 | Observation log density | `_observation_gaussian_log_density_vjp` | manual VJP available | Reuse with LGSSM residual convention. |
| B06 | Log-weight correction identity | `_log_weight_correction_vjp` | manual VJP available | Reuse. |
| B07 | Normalize, floor, and likelihood increment | `_normalize_log_weights_with_floor_vjp` | manual VJP available | Reuse; preserve floor branch diagnostics. |
| B08 | Sinkhorn transport | `_transport_forward`, `_transport_vjp` | manual VJP available for old route; Contract E first stage must bind dense/streaming choice | R3 chooses selected transport primitive after R2 reset decision. |
| B09 | Time reverse scan | `_lgssm_manual_value_and_score` | manual pattern available | Extend to include Contract E reset cotangents. |
| B10 | Diagnostic outputs | current Phase 3 diagnostic TensorArrays | non-gradient monitors | Must not participate in material score route. |

## Contract E Reset Sub-Boundaries

Every reset sub-boundary is blocked pending R2.  R2 must either provide a
manual VJP, mark a deliberately stopped derivative with a bias/nonclaim ledger,
or close the Contract E gradient as blocked.

| ID | Reset sub-boundary | Current forward expression | R1 classification |
| --- | --- | --- | --- |
| E01 | Weighted target moments | `target_mean, target_cov = weighted_moments(post_flow, weights)` | `blocked_pending_r2` |
| E02 | Barycentric first stage | `y_plus = matrix @ post_flow` | `blocked_pending_r2` |
| E03 | Plus-cloud uniform moments | `plus_cov = uniform_moments(y_plus)` | `blocked_pending_r2` |
| E04 | Covariance gap | `gap = target_cov - plus_cov` | `blocked_pending_r2` |
| E05 | Target projector/rank/eigen classification | `projector_psd(target_cov, spectral_floor)` | `blocked_pending_r2` |
| E06 | Residual covariance | `residual_cov = gap + tau * projector` | `blocked_pending_r2` |
| E07 | Residual covariance square root | `sqrt_psd(residual_cov, 0)` | `blocked_pending_r2` |
| E08 | Residual-noise recentering/injection | `y_tilde = y_plus + xi B` | `blocked_pending_r2` |
| E09 | Tilde-cloud uniform moments | `tilde_mean, tilde_cov = uniform_moments(y_tilde)` | `blocked_pending_r2` |
| E10 | Target covariance square root | `sqrt_psd(target_cov, 0)` | `blocked_pending_r2` |
| E11 | Tilde covariance pseudo-inverse square root | `pinv_sqrt_psd(tilde_cov, spectral_floor)` | `blocked_pending_r2` |
| E12 | Affine moment-restoration map | `affine = target_sqrt @ tilde_pinv_sqrt` | `blocked_pending_r2` |
| E13 | Final recentering to reset cloud | `y_star = target_mean + (y_tilde - tilde_mean) affine` | `blocked_pending_r2` |
| E14 | Diagnostic moment/conditioning monitors | covariance, rank, condition diagnostics | `non_gradient_monitor` |

## Material Unblocking Rule

R2 may decide the reset policy, but R2 cannot remove or weaken the material
blocker.  Material mode can be re-enabled only after a later phase implements
and audits the full manual likelihood reverse scan in code, including the
chosen reset policy.

## Nonclaims

- No Contract E reset VJP is implemented here.
- No gradient correctness claim is made.
- No FD, Kalman comparison, GPU/XLA, production, HMC, or nonlinear-model claim
  is made.
