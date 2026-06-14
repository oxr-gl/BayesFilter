# P8d Repair Execution Result

Date: 2026-06-14

Status: `PARTIAL_P8D_ARTIFACT_EMITTED_WITH_REAL_GAPS`

## Summary

P8d full numeric execution was launched after Gate 1 local validation, Gate 2 Claude read-only implementation review, and Gate 3 evidence-contract recording.

The run emitted the planned P8d JSON/CSV/Markdown artifacts, but the result is partial. The artifact reports `real_gap_cell_count = 11`, so P8d does not close Phase 8 and must not be treated as a clean benchmark completion.

## Command Actually Run

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --enable-p8d-execution
```

CPU/GPU status: CPU-only deliberate. `CUDA_VISIBLE_DEVICES=-1` was set before TensorFlow import.

TensorFlow still emitted CUDA factory/cuInit warnings and one CPU allocator OOM warning during a blocked cell. These are recorded as run diagnostics; they do not change the CPU-only status.

## Preconditions

Gate 1 local checks passed:

- `py_compile` passed.
- Focused P8d pytest passed after the manifest regression guard was added: `8 passed, 2 warnings`.
- `git diff --check` passed for the P8d lane files.

Gate 2 Claude read-only review:

- R2 returned `VERDICT: REVISE` for missing manifest regression coverage.
- Codex patched the P8d lane and reran focused checks.
- R3 returned `VERDICT: AGREE`.

Gate 3 evidence contract:

- recorded in `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-gate3-evidence-contract-and-run-subplan-2026-06-14.md`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| Dirty state | `1886 git-status-short entries` |
| Environment | CPU-only TensorFlow with CUDA hidden by policy |
| Dtype | `tf.float64` |
| Wall time | `640.698495` seconds |
| LGSSM seed | `81100` |
| SV/KSC seed | `81101` |
| Spatial SIR seed | `81103` |
| Predator-prey seed | `81104` |
| Generalized SV seed | `81105` |
| DPF seeds | `[81120, 81121, 81122, 81123, 81124]` |
| DPF particle count | `8` |

## Output Artifacts

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-numeric-results-2026-06-13.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-value-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-score-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-curvature-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-status-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-stochastic-uncertainty-table-2026-06-13.csv`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-numeric-summary-2026-06-13.md`

## Artifact Counts

| Count | Value |
| --- | ---: |
| `full_cell_count` | 42 |
| `executed_cell_count` | 27 |
| `structured_not_applicable_cell_count` | 4 |
| `real_gap_cell_count` | 11 |
| `pending_or_not_applicable_cell_count` | 15 |

Status token:

```text
PARTIAL_P8D_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS
partial_numeric_execution_remaining_adapter_and_callback_gaps
```

## Remaining Real Gaps

| Algorithm | Row | Status |
| --- | --- | --- |
| `cut4` | `zhao_cui_spatial_sir_austria_j9_T20` | `blocked_p8d_deterministic_smoke_failed`: CPU OOM allocating shape `[68719476736,36]` |
| `zhao_cui_scalar_or_multistate` | `benchmark_lgssm_exact_oracle_m3_T50` | `blocked_model_specific_evaluator_adapter_required` |
| `zhao_cui_scalar_or_multistate` | `zhao_cui_spatial_sir_austria_j9_T20` | `blocked_model_specific_evaluator_adapter_required` |
| `zhao_cui_scalar_or_multistate` | `zhao_cui_predator_prey_T20` | `blocked_model_specific_evaluator_adapter_required` |
| `zhao_cui_scalar_or_multistate` | `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `blocked_model_specific_evaluator_adapter_required` |
| `bootstrap_dpf_current` | `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `blocked_pending_model_specific_dpf_callbacks` |
| `bootstrap_dpf_current` | `zhao_cui_spatial_sir_austria_j9_T20` | `blocked_pending_model_specific_dpf_callbacks` |
| `ledh_pfpf_alg1_ukf_current` | `zhao_cui_sv_actual_nongaussian_T1000` | `blocked_dpf_five_seed_execution_failed`: Algorithm 1 corrected log weights are non-finite |
| `ledh_pfpf_alg1_ukf_current` | `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `blocked_pending_model_specific_dpf_callbacks` |
| `ledh_pfpf_alg1_ukf_current` | `zhao_cui_spatial_sir_austria_j9_T20` | `blocked_pending_model_specific_dpf_callbacks` |
| `ledh_pfpf_alg1_ukf_current` | `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `blocked_dpf_five_seed_execution_failed`: Algorithm 1 corrected log weights are non-finite |

## Structured Not Applicable Cells

The four structured not-applicable cells are exact Kalman outside LGSSM or the declared KSC Gaussian-mixture surrogate. They are not counted as real gaps.

## DPF Seed Audit

Executed DPF value cells used exactly five seeds and reported Monte Carlo standard errors:

| Algorithm | Row | Seed count | MC SE |
| --- | --- | ---: | ---: |
| `bootstrap_dpf_current` | `benchmark_lgssm_exact_oracle_m3_T50` | 5 | 3.047389507070607 |
| `bootstrap_dpf_current` | `zhao_cui_sv_actual_nongaussian_T1000` | 5 | 6.343333923981979 |
| `bootstrap_dpf_current` | `zhao_cui_predator_prey_T20` | 5 | 10.141202371254643 |
| `bootstrap_dpf_current` | `zhao_cui_generalized_sv_synthetic_from_estimated_values` | 5 | 0.6013597082699425 |
| `ledh_pfpf_alg1_ukf_current` | `benchmark_lgssm_exact_oracle_m3_T50` | 5 | 1.3918178595906876 |
| `ledh_pfpf_alg1_ukf_current` | `zhao_cui_predator_prey_T20` | 5 | 2.229962620580741 |

DPF score and Hessian evidence was not promoted.

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Do not close P8/Phase 8 from P8d. Preserve P8d as a partial numeric artifact with explicit remaining real gaps. |
| Primary criterion status | Failed for full closure because `real_gap_cell_count = 11`; passed only for artifact emission and explicit accounting. |
| Veto diagnostic status | No old LEDH-PFPF-OT evidence used; true not-applicable cells preserved; DPF executed value cells have five seeds; DPF gradients not promoted. |
| Main uncertainty | Whether remaining Zhao-Cui adapters and KSC/Spatial-SIR DPF callbacks should be implemented, skipped by revised scope, or split into a new phase. |
| Next justified action | Draft a P8e blocker-closure or scope-reduction subplan before further execution. |
| Not concluded | Posterior correctness, optimality, asymptotic validity, DPF gradient correctness, source-faithful Zhao-Cui production equivalence, full filter ranking, or Phase 8 closure. |

## Post-Run Red-Team Note

Strongest alternative explanation: some real gaps may be engineering route gaps rather than evidence against the scientific idea; the spatial SIR CUT4 OOM in particular may reflect an unsafe dense tensor construction.

What would overturn the current decision: a reviewed P8e plan that either implements the missing adapters/callbacks with focused finite checks or narrows the benchmark scope without silently converting real route gaps into structured not-applicable cells.

Weakest part of the evidence: executed nonlinear DPF cells use small particle count `8`, so they are wiring/value summaries only and cannot support accuracy, ranking, or gradient claims.

