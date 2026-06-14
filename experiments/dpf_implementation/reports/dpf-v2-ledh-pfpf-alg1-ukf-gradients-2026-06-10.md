# P4 Result: V2 Algorithm 1 UKF Gradient Replacement

metadata_date: 2026-06-10
phase: P4
status: LOCAL_PASS_P4_V2_ALG1_UKF_GRADIENTS_DIAGNOSTIC_ONLY_PENDING_CLAUDE_REVIEW

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | For V2 rows with valid gradient estimands, do Algorithm 1 UKF fixed-branch gradients execute finitely with uncertainty and without value-to-gradient promotion? |
| Baseline/comparator | P2 contracts, P3 value scalar, exact LGSSM Kalman score where available, and same-scalar finite differences as diagnostic-only checks on non-LGSSM gradient-runnable rows. |
| Primary criterion | Every P2 row appears; P2/P4 gradient-runnable rows are executed or explicitly downgraded; rows without a reviewed same-scalar gradient contract remain blocked with reasons; finite gradients include uncertainty, route fields, scalar and parameterization identifiers, and no promotion claim. |
| Not concluded | P4 gradient rows are diagnostic-only and do not certify numerical gradient correctness.; P4 finite differences are explanatory diagnostics only, not promotion gates.; P4 value evidence from P3 does not imply gradient correctness.; P4 does not use OT or annealed transport.; P4 does not establish stochastic-resampling gradient correctness.; P4 blocked rows are adapter work items, not negative scientific evidence.; P4 does not establish production readiness, HMC readiness, GPU performance, or broad model superiority. |

## Cells

| Model | P2 status | P4 status | Rows | Finite rows | Gradient reference | Reason |
| --- | --- | --- | ---: | ---: | --- | --- |
| `lgssm_2d_h25_rich` | `RUNNABLE_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `9` | `9` | `exact_kalman_lgssm_gradient` | finite diagnostic fixed-branch gradient rows only; no calibrated promotion band |
| `sv_1d_h18_rich` | `BLOCKED_REQUIRES_ADAPTER` | `BLOCKED_REQUIRES_ADAPTER` | `0` | `0` | `N/A_BLOCKED_REQUIRES_ADAPTER` | The current V2 stochastic-volatility row has a non-Gaussian observation likelihood.  A log-square Gaussian surrogate may be a BayesFilter extension, but it is not frozen here as source Algorithm 1 evidence. |
| `range_bearing_4d_h20_rich` | `RUNNABLE_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `9` | `9` | `diagnostic_finite_difference_only_no_exact_gradient_oracle` | finite diagnostic fixed-branch gradient rows only; no calibrated promotion band |
| `structural_ar1_quadratic_h16` | `BLOCKED_REQUIRES_ADAPTER` | `BLOCKED_REQUIRES_ADAPTER` | `0` | `0` | `N/A_BLOCKED_REQUIRES_ADAPTER` | The structural row uses stochastic m dynamics plus deterministic k completion.  A reviewed singular-completion Algorithm 1 adapter is required before source-core execution. |
| `spatial_sir_j3_rk4` | `RUNNABLE_ALG1` | `BLOCKED_REQUIRES_ADAPTER` | `0` | `0` | `N/A_BLOCKED_REQUIRES_ADAPTER` | P2 did not declare this row runnable for same-scalar P4 gradients. |
| `predator_prey_rk4` | `RUNNABLE_ALG1` | `RERUN_ALG1_DIAGNOSTIC_ONLY` | `9` | `9` | `diagnostic_finite_difference_only_no_exact_gradient_oracle` | finite diagnostic fixed-branch gradient rows only; no calibrated promotion band |

## Veto Diagnostics

| Diagnostic | Status |
| --- | --- |
| `p2_contract_absent_or_not_passed` | `False` |
| `p3_values_not_ready` | `False` |
| `row_count_or_order_mismatch` | `False` |
| `runnable_gradient_row_missing_rows` | `False` |
| `old_ledh_pfpf_ot_runtime_module_imported` | `False` |
| `old_route_used_as_current_algorithm1_evidence` | `False` |
| `algorithm1_route_fields_missing` | `False` |
| `gradient_row_nonfinite` | `False` |
| `missing_gradient_monte_carlo_uncertainty` | `False` |
| `gradient_scalar_or_parameterization_missing` | `False` |
| `finite_difference_as_promotion_gate` | `False` |
| `value_used_to_promote_gradient` | `False` |
| `stochastic_resampling_gradient_claimed` | `False` |
| `ot_or_annealed_transport_used` | `False` |

## Gradient Summaries

### lgssm_2d_h25_rich

| Particles | Seeds | Finite | Mean gradient | Component SE | Mean error norm | Error norm SE |
| --- | ---: | ---: | --- | --- | ---: | ---: |
| 4 | `3` | `3` | `[-1.7988641747509373, 0.47898892824397166]` | `[1.3009205704948628, 0.6446499050518739]` | `1.9263862603692952` | `1.2070836582844808` |
| 8 | `3` | `3` | `[-1.497993862187647, 0.38205372039440494]` | `[1.1853360122037346, 0.44832163208069165]` | `1.5365904334277432` | `1.094375340541418` |
| 16 | `3` | `3` | `[-1.3367731039550144, 0.16300966029458386]` | `[0.8789267879165555, 0.4082857453229335]` | `1.065789869289693` | `0.9318296506783853` |

### predator_prey_rk4

| Particles | Seeds | Finite | Mean gradient | Component SE | Mean error norm | Error norm SE |
| --- | ---: | ---: | --- | --- | ---: | ---: |
| 4 | `3` | `3` | `[-14.237024889593323]` | `[5.156918779547913]` | `None` | `None` |
| 8 | `3` | `3` | `[-13.763931602488091]` | `[3.5626807432569527]` | `None` | `None` |
| 16 | `3` | `3` | `[-11.393210813355287]` | `[0.8468858656543369]` | `None` | `None` |

### range_bearing_4d_h20_rich

| Particles | Seeds | Finite | Mean gradient | Component SE | Mean error norm | Error norm SE |
| --- | ---: | ---: | --- | --- | ---: | ---: |
| 4 | `3` | `3` | `[27.94567180308474, -29.98381065618071]` | `[16.895385592729657, 27.637881126248967]` | `None` | `None` |
| 8 | `3` | `3` | `[25.93608570024425, -24.621920059567913]` | `[14.928771120943312, 25.52145421045497]` | `None` | `None` |
| 16 | `3` | `3` | `[-1.1850882957983042, -28.38529353558656]` | `[1.6383604663640128, 15.97536121845927]` | `None` | `None` |

## Gate Definition

- Local decision semantics: LOCAL_PASS means the P4 artifact satisfies the local pre-Claude diagnostic gradient gate.  It is not an unconditional pass, correctness promotion, stochastic-score proof, or HMC-readiness claim.
- P2 blocked carry-forward allowed: `True`
- Gradient-contract block allowed: `True`
- P2 runnable gradient rule: A P2 value-runnable row may still be gradient-blocked if P2 did not declare a reviewed same-scalar gradient contract.
- Promotion rule: P4 gradient evidence is diagnostic-only.  Finite AD gradients and finite-difference residuals cannot promote correctness.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `LOCAL_PASS_P4_V2_ALG1_UKF_GRADIENTS_DIAGNOSTIC_ONLY_PENDING_CLAUDE_REVIEW` | every P2 row appears; P4-runnable rows executed or explicitly downgraded; blocked rows remain visible with reasons; finite gradients carry uncertainty | `{'p2_contract_absent_or_not_passed': False, 'p3_values_not_ready': False, 'row_count_or_order_mismatch': False, 'runnable_gradient_row_missing_rows': False, 'old_ledh_pfpf_ot_runtime_module_imported': False, 'old_route_used_as_current_algorithm1_evidence': False, 'algorithm1_route_fields_missing': False, 'gradient_row_nonfinite': False, 'missing_gradient_monte_carlo_uncertainty': False, 'gradient_scalar_or_parameterization_missing': False, 'finite_difference_as_promotion_gate': False, 'value_used_to_promote_gradient': False, 'stochastic_resampling_gradient_claimed': False, 'ot_or_annealed_transport_used': False}` | non-LGSSM gradients have no exact oracle in P4 | Claude P4 read-only review, then P5 consumes P2-P4 artifacts | no stochastic-score, HMC, OT-extension, performance, or production claim |

## Post-Run Red-Team Note

Strongest alternative explanation: finite non-LGSSM gradients demonstrate AD execution only, not correctness, because P4 lacks exact nonlinear gradient oracles.

Result that would overturn the local decision: Claude finds scalar mismatch, missing route fields, value-to-gradient promotion, old-route leakage, or unsupported gradient rows treated as passes.

Weakest part of the evidence: P4 is diagnostic-only by design and excludes stochastic resampling gradients.

## Run Manifest

- command: `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m experiments.dpf_implementation.tf_tfp.runners.run_v2_ledh_pfpf_alg1_ukf_gradients_tf`
- git branch: `main`
- git commit: `26485010c28e11b3591da59b7ca375d4764c3d8d`
- CPU/GPU status: CPU-only, `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import
- visible GPU devices: `[]`
- P2 JSON: `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_alg1_ukf_contracts_2026-06-10.json`
- P3 JSON: `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_alg1_ukf_values_2026-06-10.json`
- gradient seeds: `[101, 202, 303]`
- gradient particle counts: `[4, 8, 16]`
- pseudo-time steps: `[0.5, 0.5]`
- UKF parameters: `{'alpha': 1.0, 'beta': 2.0, 'kappa': 0.0}`
- finite-difference step: `1e-05`
- JSON: `experiments/dpf_implementation/reports/outputs/dpf_v2_ledh_pfpf_alg1_ukf_gradients_2026-06-10.json`
- report: `experiments/dpf_implementation/reports/dpf-v2-ledh-pfpf-alg1-ukf-gradients-2026-06-10.md`
- result: `docs/plans/bayesfilter-dpf-ledh-pfpf-alg1-ukf-ledh-pfpf-ot-rerun-p4-v2-gradients-result-2026-06-10.md`
- wall time seconds: `142.45358040276915`

## Nonclaims

- P4 gradient rows are diagnostic-only and do not certify numerical gradient correctness.
- P4 finite differences are explanatory diagnostics only, not promotion gates.
- P4 value evidence from P3 does not imply gradient correctness.
- P4 does not use OT or annealed transport.
- P4 does not establish stochastic-resampling gradient correctness.
- P4 blocked rows are adapter work items, not negative scientific evidence.
- P4 does not establish production readiness, HMC readiness, GPU performance, or broad model superiority.

## Gate Status

P4 is pending Claude read-only review.
