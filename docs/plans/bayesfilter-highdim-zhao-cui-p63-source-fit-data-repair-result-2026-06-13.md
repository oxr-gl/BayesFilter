# P63 Result: Source Fit-Data And computeL Repair

metadata_date: 2026-06-13
status: EXECUTED_WITH_REMAINING_P60_BLOCKER
executor: Codex
reviewer: none; Claude intentionally left alone
plan: docs/plans/bayesfilter-highdim-zhao-cui-p63-source-fit-data-repair-plan-2026-06-13.md
predecessor: docs/plans/bayesfilter-highdim-zhao-cui-p62-defensive-tau-repair-result-2026-06-13.md

## Decision Table

| Field | Result |
| --- | --- |
| Decision | P63 implementation repair is complete for the narrow source-fit-data drift. |
| Primary criterion | Passed: P59/P60 fit data now records source-pushed augmented samples, source `computeL` recentering, deterministic fixed-variant weighted resampling, and local fit points. |
| Veto diagnostics | P60 still blocks on same-route rank convergence; no d=18 correctness claim is allowed. |
| Main uncertainty | The bounded fixed-TTSIRT route still has large low-vs-high rank normalizer/log-marginal deltas at the tiny diagnostic setting. |
| Next justified action | Diagnose rank/capacity and bounded-domain effects without reverting to artificial reference-grid fit data. |
| Not concluded | No paper-scale spatial SIR success, no d=50/d=100 claim, no HMC production readiness, no `AlgebraicMapping(1)` parity, no adaptive Zhao-Cui parity. |

## What Changed

- Added source-derived P59 fit data plumbing in `bayesfilter/highdim/source_route.py`.
- P59/P60 no longer fit from `_p59_author_sir_reference_points` for the main P59-9a/P59-9b fit path.
- Fit data is now produced from:
  - source-style prior/retained samples;
  - source-style push and likelihood weight update;
  - augmented `[theta, x_t, x_{t-1}]` samples;
  - `source_route_recenter(..., expansion_factor=4.0, covariance_jitter=1e-5)`;
  - deterministic fixed-variant weighted resampling;
  - local coordinates `L^{-1}(sample - mu)`.
- Added manifest fields:
  - `fit_data_mode = source_pushed_computeL_resampled_local_fit`;
  - `coordinate_frame_source = source_computeL_weighted_augmented_samples`;
  - `fixed_variant_resampling = deterministic_systematic_quantile`.
- Preserved P62 positive defensive tau: `1e-8`.

## Source Anchors

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:22-30`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:49-66`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:84-99`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:1-35`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/ssmodel.m:45-55`

## Commands Run

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_36d_target_fit.py tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: `14 passed, 2 warnings in 539.21s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY'
import json
import bayesfilter.highdim as h
r = h.p60_author_sir_same_route_rank_comparator(sample_count=1, fit_sample_count=2)
print(json.dumps({
    "status": r.status,
    "blockers": r.blockers,
    "log_marginal_likelihoods": r.manifest.get("log_marginal_likelihoods"),
    "log_marginal_abs_delta": r.manifest.get("log_marginal_abs_delta"),
    "normalizer_increment_abs_deltas": r.manifest.get("normalizer_increment_abs_deltas"),
    "probe_log_density_median_abs_delta": r.manifest.get("probe_log_density_median_abs_delta"),
    "retained_log_density_median_abs_delta": r.manifest.get("retained_log_density_median_abs_delta"),
}, indent=2, default=str))
PY
```

Result:

```json
{
  "status": "BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE",
  "blockers": [
    "log_marginal_delta_threshold_exceeded",
    "normalizer_increment_delta_threshold_exceeded"
  ],
  "log_marginal_likelihoods": [
    -377.31228935146066,
    -412.9490465878503
  ],
  "log_marginal_abs_delta": 35.636757236389656,
  "normalizer_increment_abs_deltas": [
    17.21607649243728,
    18.420680743952374
  ],
  "probe_log_density_median_abs_delta": 0.0,
  "retained_log_density_median_abs_delta": 0.0
}
```

## Interpretation

P63 removes the artificial fit-data drift. The d=18 comparator now confirms both
candidate rows use `source_pushed_computeL_resampled_local_fit`, and the source
fit local clipping fraction was `0.0` for both steps in both candidates.

The remaining failure is not the previous fit-data-source blocker. It is now a
rank/capacity/normalizer stability blocker in the bounded fixed-TTSIRT route:
low and high rank candidates produce identical probe/retained density medians
but substantially different normalizer increments and total log marginal
likelihood.

## Run Manifest

| Field | Value |
| --- | --- |
| git commit | `2648501` |
| CPU/GPU status | CPU-only requested with `CUDA_VISIBLE_DEVICES=-1`; TensorFlow still emitted CUDA plugin import warnings. |
| data/model | `zhao_cui_sir_austria_model()`, simulated observations with seed `5901` |
| random seeds | source prior seed `6301`; process push seeds `6401`, `6402`; simulation seed `5901` |
| plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p63-source-fit-data-repair-plan-2026-06-13.md` |
| result file | `docs/plans/bayesfilter-highdim-zhao-cui-p63-source-fit-data-repair-result-2026-06-13.md` |

## Remaining Gap

The next repair should not weaken P60 thresholds or return to artificial local
reference grids. It should investigate why the bounded fixed-TTSIRT
normalizer/log-marginal estimates remain unstable under the same-route
low/high-rank diagnostic after source-derived fit data is used.
