# Phase 1 Amendment Result: Fixed SIR Free Model Theta

Date: 2026-07-06

Status: `PASSED_WITH_BOUNDED_FALLBACK_REVIEW`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Apply the human amendment that `zhao_cui_spatial_sir_austria_j9_T20` uses model parameters as free parameters. The row now uses `sir_log_scale_theta` with theta `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)` and truth theta `[0,0,0]`. |
| Primary criterion status | Passed locally: the fixed SIR dataset manifest, active LEDH admission ledger, Phase 1 contract, and Phase 2 subplan expose the amended 3D theta contract. |
| Veto diagnostic status | Passed locally: the amendment does not claim author-source free-inference-theta faithfulness, does not admit full observed-data score evidence, and does not promote the legacy scoped parameterized row as a shortcut. |
| Main uncertainty | Full same-target observed-data LEDH value and no-tape score admission for SIR remain later-phase work. |
| Next justified action | Continue Phase 2 common forward API under the amended SIR contract. |
| What is not concluded | No SIR score is admitted, no exact nonlinear likelihood correctness is claimed, no HMC readiness is claimed, and no leaderboard promotion is made. |

## Evidence Contract Result

| Field | Status |
| --- | --- |
| Question | Does fixed SIR now expose model parameters as free parameters without crossing score-admission boundaries? |
| Baseline/comparator | Phase 1 zero-dimensional closeout, existing `ParameterizedZhaoCuiSIRSSM` log-scale surface, and the 2026-07-06 human amendment. |
| Primary criterion | Passed: fixed SIR uses `sir_log_scale_theta`, theta dimension 3, truth theta `[0,0,0]`, and the exact parameter order. |
| Veto diagnostics | Passed: no full observed-data SIR score admission; no source-faithful inference-theta claim; no scoped local-complete-data promotion. |
| Explanatory diagnostics | TensorFlow emitted plugin/CUDA initialization warnings during CPU-hidden manifest regeneration; the command completed and these warnings are not GPU evidence. |
| Not concluded | Same-target value/score correctness and leaderboard readiness remain unproved. |

## Artifacts Changed

- `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.csv`
- `tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json`
- `docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py`
- `tests/test_ledh_score_memory_n10000.py`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase0-launch-invariant-freeze-result-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-contract-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-freeze-result-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase2-common-forward-api-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase6-integration-leaderboard-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-visible-execution-ledger-2026-07-06.md`

## Checks Run

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py
```

Result: passed; manifest regenerated with fixed SIR `sir_log_scale_theta`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py \
  tests/test_ledh_score_memory_n10000.py::test_fixed_spatial_sir_ledh_full_row_score_remains_blocked \
  tests/test_ledh_score_memory_n10000.py::test_all_highdim_ledh_score_integration_statuses_are_truthful \
  -q
```

Result: passed, `11 passed, 2 warnings`.

```bash
python -m py_compile \
  scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py \
  docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py
```

Result: passed.

## Review Repair Loop

Claude review round 1 returned `VERDICT: REVISE` in:

```text
/home/chakwong/BayesFilter/.claude_reviews/20260706-150836-ledh-same-target-forward-score-phase1-fixed-sir-amendment
```

Finding accepted: `tests/test_ledh_score_memory_n10000.py` still runs the
legacy scoped parameterized-SIR diagnostic, but its printed JSON result had
been mislabeled as the fixed full SIR row. That could promote scoped score
evidence as fixed-row evidence.

Repair:

- restored the printed `row_id` to
  `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`;
- added `target_scope = legacy_scoped_parameterized_sir_diagnostic`;
- added nonclaims that the diagnostic is not full observed-data fixed-SIR score
  admission and not a substitute for the amended fixed SIR same-target score
  gate.

Focused post-repair checks:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py \
  tests/test_ledh_score_memory_n10000.py::test_fixed_spatial_sir_ledh_full_row_score_remains_blocked \
  tests/test_ledh_score_memory_n10000.py::test_all_highdim_ledh_score_integration_statuses_are_truthful \
  -q
```

Result: passed, `11 passed, 2 warnings`.

Claude review round 2 used the same bounded gate. The primary review timed
out, but bounded fallback returned `VERDICT: AGREE` in:

```text
/home/chakwong/BayesFilter/.claude_reviews/20260706-151700-ledh-same-target-forward-score-phase1-fixed-sir-amendment-r2
```

This is weaker than a full primary review and is recorded as such. It is
accepted for this amendment because the round-1 material finding was repaired
and the focused local checks carry the evidence burden.

```bash
git diff --check -- \
  scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py \
  tests/highdim/test_filtering_value_gradient_benchmark_p8_datasets.py \
  tests/test_ledh_score_memory_n10000.py \
  docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py \
  docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md \
  docs/plans/bayesfilter-ledh-same-target-forward-score-phase0-launch-invariant-freeze-result-2026-07-06.md \
  docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-contract-2026-07-06.md \
  docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-freeze-result-2026-07-06.md \
  docs/plans/bayesfilter-ledh-same-target-forward-score-phase2-common-forward-api-subplan-2026-07-06.md \
  docs/plans/bayesfilter-ledh-same-target-forward-score-phase6-integration-leaderboard-subplan-2026-07-06.md \
  docs/plans/bayesfilter-ledh-same-target-forward-score-visible-execution-ledger-2026-07-06.md \
  docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.json \
  docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.csv \
  docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-dataset-manifest-2026-06-11.md \
  docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json
```

Result: passed.

## Next-Phase Handoff

Phase 2 must treat fixed SIR as a 3D `sir_log_scale_theta` row. It must still
block any SIR score until the fixed row has an admitted same-target
observed-data LEDH forward scalar and a no-tape score of that exact scalar.
