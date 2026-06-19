# P8j Phase 4 Result: OT-Resampled LEDH-PFPF-OT SIR Smoke

metadata_date: 2026-06-17
status: PASS_PENDING_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-dpf-sir-d18-leaderboard-master-program-2026-06-17.md
phase: 4
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Local Phase 4 gate passed after a command-configuration repair; await Claude review before Phase 5. |
| Primary criterion status | Passed locally.  Focused SIR DPF tests passed and one-seed N=4 OT-resampled Algorithm 1 UKF LEDH smoke is finite with the inherited P8h Sinkhorn solver settings. |
| Veto diagnostic status | No local veto remains open.  The first default-Sinkhorn attempt failed and is recorded as a configuration defect, not a model change or scientific failure. |
| Main uncertainty | Claude has not yet reviewed the Phase 4 result or Phase 5 subplan.  No five-seed tuned particle-count evidence exists yet. |
| Next justified action | Claude review of this Phase 4 result and the Phase 5 SIR d18 particle-count tuning subplan. |
| What is not concluded | No five-seed DPF value evidence, no particle-count adequacy, no leaderboard refresh, no score/Hessian/theta-gradient/HMC/NUTS readiness, no Zhao-Cui TT/SIRT or MATLAB parity. |

## Checks Run

Focused SIR DPF tests:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -q -k "sir_dpf"
```

Result:

- `3 passed, 32 deselected, 2 warnings`

Diff check before smoke:

```bash
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-subplan-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-claude-review-ledger-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-execution-ledger-2026-06-17.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-visible-stop-handoff-2026-06-17.md
```

Result:

- passed

## Smoke Artifact

Command: one-seed N=4 OT-resampled Algorithm 1 UKF LEDH smoke via
`_dpf_single_run(..., resampling_route=P8H_DEFAULT_RESAMPLING_ROUTE)`,
deliberate CPU-only with `CUDA_VISIBLE_DEVICES=-1`.

The repaired command explicitly used the inherited P8h Sinkhorn solver settings:

- `sinkhorn_epsilon=1.0`;
- `sinkhorn_iterations=200`;
- `sinkhorn_tolerance=1e-6`.

Artifact:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-2026-06-17.json`

Summary:

| Field | Value |
| --- | --- |
| Status | `executed_one_seed_ot_ledh_sir_smoke` |
| Row | `zhao_cui_spatial_sir_austria_j9_T20` |
| Algorithm | `ledh_pfpf_alg1_ukf_current` |
| Resampling route | `ot_sinkhorn_barycentric_covariance_carry` |
| Particle count | `4` |
| Seed | `81120` |
| Log likelihood | `-2215.0697771431705` |
| Average log likelihood | `-110.75348885715853` |
| Minimum ESS | `1.0` |
| Mean ESS | `1.7428145717002863` |
| Resampling count | `12` |

Route identifiers:

- `method_generation`: `li_coates_algorithm1_ukf_covariance_lifecycle`;
- `flow_source_route`: `li_coates_2017_algorithm1_ledh_pfpf`;
- `resampling_route`: `ot_sinkhorn_barycentric_covariance_carry`;
- `transport_method`: `fixed_target_sinkhorn`;
- `covariance_carry_route`: `same_transport_barycentric_covariance_carry`;
- `pfpf_correction_route`: `algorithm1_pfpf_corrected_log_weight_pre_resampling`;
- `canonical_transport_matrix_convention`: `target_by_source_row_stochastic`;
- `relaxed_resampling_not_categorical`: `true`;
- `previous_ledh_pfpf_ot_evidence_status`: `quarantined`.

## Configuration Repair Note

The first Phase 4 smoke attempt used `_dpf_single_run()` defaults
(`epsilon=0.5`, `iterations=80`, `tolerance=1e-7`) and failed before writing
JSON with:

```text
FloatingPointError: Sinkhorn row residual exceeded tolerance envelope
```

A focused diagnostic using the P8h profile solver settings
(`epsilon=1.0`, `iterations=200`, `tolerance=1e-6`) passed without changing the
SIR model, observations, callback route, or algorithm implementation.  The
Phase 4 subplan command was patched to make those inherited settings explicit.

## Smoke Nonclaims

- one-seed N=4 OT LEDH smoke only;
- not five-seed DPF value evidence;
- not particle-count adequacy;
- not leaderboard completion;
- not score, Hessian, theta-gradient, HMC, or NUTS evidence;
- not Zhao-Cui TT/SIRT source-faithfulness or MATLAB parity.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `94069066a70df6f1f0f2b53d32b9d452bd67f891` |
| Dirty state | `385` git-status-short entries at result-writing time; substantial pre-existing dirty/untracked work outside P8j remains. |
| Commands | Focused pytest, `git diff --check`, failed default-Sinkhorn smoke, focused inherited-setting diagnostic, repaired one-seed OT LEDH smoke. |
| Environment | TensorFlow/TensorFlow Probability, deliberate CPU-only. |
| CPU/GPU status | `CUDA_VISIBLE_DEVICES=-1`; TensorFlow emitted CUDA initialization warnings, but GPU was intentionally hidden for this smoke. |
| Data version | Current local P8 source-scope/adapter matrix and SIR synthetic dataset generator. |
| Seeds | Smoke seed `81120`. |
| Output artifacts | This result and the Phase 4 smoke JSON. |
| Plan file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-subplan-2026-06-17.md` |
| Result file | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase4-ot-ledh-sir-smoke-result-2026-06-17.md` |

## Handoff

Phase 5 may not execute until Claude reviews this Phase 4 result and the Phase
5 SIR particle-count tuning subplan.  A finite N=4 OT smoke authorizes only the
next tuning plan review; it does not establish particle adequacy or leaderboard
completion.
