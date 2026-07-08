# Phase 0 Subplan: Coordinate And Mass Convention Audit

Date: 2026-07-08

## Status

`DRAFT_SUBPLAN`

## Phase Objective

Audit the exact coordinate path from quadratic initializer fit space to the
minimal SSL-LSTM HMC geometry initializer, without running HMC.

## Entry Conditions

- Worktree clean after initializer commit `9220d90`.
- The reusable initializer tests passed before commit.

## Required Artifacts

- Phase 0 coordinate audit result note.
- Visible ledger update.
- Draft Phase 1 initializer artifact smoke subplan.

## Required Checks

- Source inspection of:
  - `bayesfilter/inference/quadratic_map_covariance.py`
  - `bayesfilter/inference/quadratic_geometry.py`
  - `bayesfilter/inference/hmc_kernel_tuning.py`
  - `bayesfilter/inference/hmc.py`
  - `docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py`
  - `bayesfilter/nonlinear/ssl_lstm_zhaocui_hmc_minimal.py`
- Local non-runtime checks:
  - `git status --short`
  - `python -m py_compile bayesfilter/inference/quadratic_map_covariance.py bayesfilter/inference/hmc_kernel_tuning.py docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which coordinate space does each precision/covariance live in, and what must be passed to HMC geometry initialization? |
| Baseline/comparator | Existing minimal Phase 5 low-rank path and `initialize_hmc_kernel_geometry` contract. |
| Primary pass criterion | Result note states exact mapping from quadratic whitened `z` to original theta, HMC mass artifact covariance space, and trajectory diagnostic interpretation. |
| Veto diagnostics | Ambiguous coordinate state, untransformed whitened precision treated as original precision, no line-anchored source evidence, or HMC runtime launched. |
| Explanatory diagnostics | Existing `theta = center + prior_scale * z` transform, `diag(1/scale) @ P_z @ diag(1/scale)` precision transform, HMC geometry target trajectory formula. |
| Not concluded | No initializer quality, no HMC readiness, no posterior correctness, no convergence. |

## Forbidden Claims And Actions

- Do not run HMC.
- Do not claim HMC readiness or posterior correctness.
- Do not edit source unless the audit discovers a compile/doc typo that blocks
  the audit.

## Next-Phase Handoff Conditions

Phase 1 may begin only if the result note says:

- the reusable initializer covariance/precision is in original coordinates;
- or if not, exactly what transform is required before HMC geometry;
- HMC geometry initialization expects original unconstrained coordinates;
- the 1.57 heuristic is only an explanatory diagnostic unless Phase 2 defines it
  as a criterion.

## Stop Conditions

- Coordinate mapping cannot be established from source.
- Existing HMC initializer contract conflicts with the reusable initializer
  output.
- Local compile/status checks fail.

## Skeptical Plan Audit

| Risk | Phase 0 audit |
| --- | --- |
| Wrong baseline | Uses existing minimal Phase 5 and HMC initializer contracts only. |
| Proxy metric promoted | No numeric result promotes anything in Phase 0. |
| Missing stop conditions | Stop conditions are explicit. |
| Unfair comparison | No comparison. |
| Hidden assumptions | 1.57 is heuristic/explanatory only. |
| Stale context | Uses current source at `9220d90`. |
| Environment mismatch | No runtime/HMC/GPU. |
| Artifact mismatch | Result note directly answers coordinate question. |

Audit status: `PASSED_FOR_COORDINATE_AUDIT`.
