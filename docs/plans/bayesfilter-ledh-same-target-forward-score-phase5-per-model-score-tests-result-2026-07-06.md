# Phase 5 Result: Per-Model Score And Memory Tests

metadata_date: 2026-07-06
status: PASSED_TWO_FULL_ROWS
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 5

## Phase Objective

Write and run one score correctness/memory test per admitted model, including
tiny correctness and trusted GPU `N=10000` checks.

## Skeptical Plan Audit

| Risk checked | Result |
| --- | --- |
| Wrong rows | Only LGSSM and fixed SIR were run as admitted full rows. |
| Scoped row promoted | Scoped parameterized SIR diagnostic was not counted as fixed-SIR evidence. |
| Hidden GPU failure | GPU was probed in trusted context before `N=10000` tests. |
| Skips treated as pass | CPU-hidden local sweep reported GPU-only tests as skipped; trusted GPU runs provided pass evidence. |
| Memory-only promotion | Both rows required same-scalar directional correctness and memory under budget. |

Audit status: passed.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Do admitted LEDH score routes remain correct and memory-bounded at `N=10000`? |
| Baseline/comparator | Phase 4 tiny same-scalar checks plus trusted GPU directional finite differences at `N=10000`. |
| Primary criterion | Passed for LGSSM and fixed SIR. |
| Veto diagnostics | No OOM; no hidden autodiff sentinel failure; finite directional scores; memory below 14000 MiB budget; no wrong-row/scoped-row promotion. |
| Explanatory diagnostics | Wall time, peak memory, absolute/relative FD error. |
| Not concluded | HMC readiness, posterior correctness, scientific superiority, or fair runtime ranking. |

## Trusted GPU Device Probe

```text
nvidia-smi
```

Result: trusted context reported NVIDIA GeForce RTX 4080 Laptop GPU, 16376 MiB
total memory, CUDA 13.1.

## Passing Rows

| Row | Score route | Particles | Abs error | Rel error | Peak MiB | Budget MiB | Artifact |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | `compact_forward_sensitivity_no_autodiff_same_scalar_lgssm_ledh_pfpf_ot` | 10000 | 4.5494946698809713e-10 | 1.202675980538481e-09 | 197.2001953125 | 14000 | `docs/plans/ledh-phase5-lgssm-score-memory-n10000-2026-07-06.json` |
| `zhao_cui_spatial_sir_austria_j9_T20` | `manual_total_vjp_no_autodiff_same_scalar_fixed_sir_logscale_ledh_pfpf_ot` | 10000 | 0.001092374324798584 | 0.001272708410397172 | 3166.76904296875 | 14000 | `docs/plans/ledh-phase5-fixed-sir-score-memory-n10000-2026-07-06.json` |

## Blocked Rows

Rows that remain blocked because Phase 3 did not admit same-target forward
scalars:

- `zhao_cui_sv_actual_nongaussian_T1000`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`
- `zhao_cui_predator_prey_T20`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`

The scoped `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`
diagnostic remains non-full-row evidence.

## Commands And Checks

Trusted GPU `N=10000` LGSSM:

```text
BAYESFILTER_RUN_LEDHD_SCORE_MEMORY_N10000=1 \
BAYESFILTER_LEDHD_SCORE_MEMORY_BUDGET_MIB=14000 \
MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_ledh_score_memory_n10000.py::test_lgssm_ledh_compact_score_float64_correctness_and_memory_n10000 -q
```

Result: `1 passed, 2 warnings in 408.38s (0:06:48)` for the artifact-writing
run.

Trusted GPU `N=10000` fixed SIR:

```text
BAYESFILTER_RUN_LEDHD_SCORE_MEMORY_N10000=1 \
BAYESFILTER_LEDHD_SCORE_MEMORY_BUDGET_MIB=14000 \
MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_ledh_score_memory_n10000.py::test_fixed_spatial_sir_ledh_full_row_score_correctness_and_memory_n10000 -q
```

Result: `1 passed, 2 warnings in 616.30s (0:10:16)` for the artifact-writing
run.

CPU-hidden local sweep:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_ledh_score_memory_n10000.py \
  tests/test_ledh_fixed_sir_manual_score_phase4.py \
  tests/test_ledh_lgssm_manual_score_phase4.py -q
```

Result: `17 passed, 2 skipped, 2 warnings`.

Other checks:

- `python -m py_compile tests/test_ledh_score_memory_n10000.py`: passed.
- `git diff --check` on Phase 5 files: passed.

## Phase 6 Handoff

Phase 6 may rebuild the LEDH-inclusive leaderboard with admitted full-row LEDH
score evidence for:

- `benchmark_lgssm_exact_oracle_m3_T50`
- `zhao_cui_spatial_sir_austria_j9_T20`

Phase 6 must preserve blocked statuses for actual SV, KSC SV, predator-prey,
and generalized SV. It must keep scoped parameterized SIR diagnostic evidence
separate from full observed-data row evidence.

## Nonclaims

- No HMC/NUTS readiness.
- No posterior correctness.
- No exact nonlinear likelihood correctness for fixed SIR.
- No scientific superiority.
- No fair runtime ranking against frozen non-LEDH baseline rows.
