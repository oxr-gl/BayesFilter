# Claude Read-Only Review Bundle: LEDH Same-Target Phase 4

metadata_date: 2026-07-06
review_scope: bounded_phase4_manual_no_tape_score
codex_role: supervisor_and_executor
claude_role: read_only_reviewer

## Objective

Review the Phase 4 manual no-tape score implementation and Phase 5 handoff.

The review question is narrow:

Did Codex admit tiny no-tape score checks only for Phase 3 value-admitted rows,
keep the scoped parameterized SIR diagnostic from being promoted, and require
fixed-SIR score to use the same target scalar and full manual transport
derivative?

## Files To Inspect

- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase4-manual-score-implementation-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase4-manual-score-implementation-result-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase5-per-model-score-tests-subplan-2026-07-06.md`
- `docs/benchmarks/benchmark_ledh_same_target_fixed_sir_score.py`
- `tests/test_ledh_fixed_sir_manual_score_phase4.py`
- `tests/test_ledh_lgssm_manual_score_phase4.py`
- `tests/test_ledh_score_memory_n10000.py`
- `bayesfilter/highdim/ledh_forward_contract.py`

Do not inspect unrelated files unless required to answer the bounded question.

## Intended Phase 4 Outcome

Tiny score admitted locally:

- `benchmark_lgssm_exact_oracle_m3_T50`
- `zhao_cui_spatial_sir_austria_j9_T20`

Still score-blocked:

- `zhao_cui_sv_actual_nongaussian_T1000`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`
- `zhao_cui_predator_prey_T20`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values`

Historical/diagnostic only:

- `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`

## Important Boundaries

- No `GradientTape`, `ForwardAccumulator`, `gradient`, `jacobian`,
  `batch_jacobian`, or `watch` is allowed in admitted score helpers.
- Fixed SIR admitted score must reject stopped-scale/stabilized transport and
  require `transport_ad_mode="full"`.
- Fixed SIR public row id must be
  `zhao_cui_spatial_sir_austria_j9_T20`.
- Fixed SIR target scalar must be
  `observed_data_log_likelihood_estimator`.
- Fixed SIR theta coordinate must be `sir_log_scale_theta`.
- The old parameterized SIR diagnostic machinery may be reused internally for
  the repaired VJP, but its scoped row cannot be promoted as the fixed full row.
- Phase 4 does not claim `N=10000` memory correctness or leaderboard readiness.

## Local Checks Already Run

CPU-only checks intentionally hid GPU devices with `CUDA_VISIBLE_DEVICES=-1`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_ledh_fixed_sir_manual_score_phase4.py -q
```

Result: `5 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/test_ledh_lgssm_manual_score_phase4.py \
  tests/test_ledh_fixed_sir_manual_score_phase4.py \
  tests/test_ledh_score_memory_n10000.py::test_fixed_spatial_sir_ledh_full_row_has_phase4_tiny_score_but_n10000_pending \
  tests/test_ledh_score_memory_n10000.py::test_all_highdim_ledh_score_integration_statuses_are_truthful -q
```

Result: `13 passed, 2 warnings`.

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile <Phase 4 code and tests>
```

Result: passed.

```text
git diff --check -- <Phase 4 files>
```

Result: passed.

## Pass Criteria

Return `VERDICT: AGREE` only if:

- Phase 4 score work is limited to LGSSM and fixed SIR;
- fixed SIR uses main observed-data row identity, not the scoped diagnostic row;
- fixed SIR score uses the Phase 2/3 same-target forward contract;
- fixed SIR admitted route rejects stopped-scale/stabilized transport;
- fixed SIR score components cover the required five total derivative channels;
- Phase 5 handoff lists LGSSM and fixed SIR only for admitted full-row
  `N=10000` score-memory tests;
- no `N=10000`, leaderboard, HMC, posterior, or scientific-superiority claim
  is made from Phase 4 tiny checks.

Return `VERDICT: REVISE` if any material blocker remains.

## Forbidden Reviewer Actions

Claude must not edit files, run commands, launch agents, authorize gates, or
make scientific/product claims. Claude is read-only reviewer only.

## Required Output Format

Use concise bullets. End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
