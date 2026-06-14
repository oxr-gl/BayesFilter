# P62 Result: Fixed Source-Route Defensive Tau Repair

metadata_date: 2026-06-13
status: P0_P1_REPAIR_PASS_D18_COMPARATOR_STILL_BLOCKED
plan_artifact: docs/plans/bayesfilter-highdim-zhao-cui-p62-fixed-source-route-repair-master-program-2026-06-13.md
executor: Codex
reviewer: none; Claude intentionally left alone for this execution

## Decision Table

| Decision | Primary Criterion Status | Veto Diagnostic Status | Main Uncertainty | Next Justified Action | Nonclaims |
| --- | --- | --- | --- | --- | --- |
| Accept the P62 defensive-mass repair. | PASS: P59/P60 fixed TTSIRT builders now use positive `tau=1e-8`, manifest active defensive mass, and build both low/high P60 d=18 candidates. | PASS for the P1 veto: no `NORMALIZER_FLOOR_EXCEEDED` blocker remains in the d=18 rerun. P60 still blocks on comparator thresholds. | The d=18 same-route rank deltas are still too large, so later source-loop discrepancies remain. | Proceed to P2/P3 source-loop fidelity repairs: source `computeL`/weighted recentering and source fit-data resampling before treating P60 thresholds as scientific evidence. | No d=18 correctness claim, no d=50/d=100 claim, no HMC production-readiness claim, no adaptive Zhao-Cui parity claim. |

## Source-Lock Result

The repaired value is the author executable TTSIRT default:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m:185-188`: `defaultTau = 1E-8`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:116-120`: `full_sol` calls `TTSIRT(...)` without passing the script-local `tau`.

The source script still declares `tau = 10`, but that value is not wired into
the executable `full_sol` path used for this lane.  P62 therefore records
`source_declared_tau_unwired = 10.0` and uses
`source_executable_ttsirt_default_tau = 1e-8`.

## Code Changes

- `bayesfilter/highdim/source_route.py`
  - Added `P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU = 1e-8`.
  - Added source anchors for the defensive tau decision.
  - Replaced the P59/P60 fixed TTSIRT density `tau=0.0` construction with the source-locked positive tau.
  - Added manifest fields for `defensive_tau`, `defensive_tau_source`, `source_declared_tau_unwired`, and `source_executable_ttsirt_default_tau`.
- `bayesfilter/highdim/transport.py`
  - `FixedTTSIRTTransport.manifest_payload()` now reports `defensive_mass_positive`, `defensive_tau`, and `defensive_tau_source`.
- `bayesfilter/highdim/__init__.py`
  - Exported the P62 tau constant for tests and downstream plan checks.
- `tests/highdim/test_p59_author_sir_36d_target_fit.py`
  - Added positive defensive-mass assertions.
- `tests/highdim/test_p60_author_sir_rank_comparator.py`
  - Changed the P60 gate so a missing high-rank row is no longer accepted after the defensive-tau repair.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `2648501` |
| CPU/GPU status | CPU-only intent: `CUDA_VISIBLE_DEVICES=-1`; TensorFlow emitted CUDA plugin startup warnings but no GPU result is used. |
| Environment | `/home/chakwong/anaconda3/envs/tf-gpu`, Python 3.11 via current shell |
| Plan file | `docs/plans/bayesfilter-highdim-zhao-cui-p62-fixed-source-route-repair-master-program-2026-06-13.md` |
| Result file | `docs/plans/bayesfilter-highdim-zhao-cui-p62-defensive-tau-repair-result-2026-06-13.md` |
| Seeds | Existing P59/P60 deterministic seeds: model simulation seed `5901`; branch seeds in P59 step builders unchanged. |
| Data version | Built-in Zhao-Cui Austria SIR fixture, `zhao_cui_sir_austria_d18`. |

## Commands Run

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py bayesfilter/highdim/transport.py bayesfilter/highdim/__init__.py tests/highdim/test_p59_author_sir_36d_target_fit.py tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_36d_target_fit.py tests/highdim/test_p59_author_sir_step_spec_assembly.py tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: `14 passed, 2 warnings in 388.00s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -c "import json, bayesfilter.highdim as h; r=h.p60_author_sir_same_route_rank_comparator(sample_count=1, fit_sample_count=2); print(json.dumps({'status': r.status, 'blockers': r.blockers, 'low': None if r.low_result is None else r.low_result.status, 'high': None if r.high_result is None else r.high_result.status, 'manifest': r.manifest}, indent=2, default=str))"
```

Result:

- status: `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE`
- blockers:
  - `log_marginal_delta_threshold_exceeded`
  - `normalizer_increment_delta_threshold_exceeded`
- low candidate: `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY`
- high candidate: `PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY`
- high candidate defensive tau: `1e-8`
- old blocker absent: no `NORMALIZER_FLOOR_EXCEEDED`

Key comparator diagnostics:

| Diagnostic | Value | Threshold |
| --- | ---: | ---: |
| low log marginal | `-132.67807591879463` | N/A |
| high log marginal | `-168.06589906988285` | N/A |
| log marginal absolute delta | `35.38782315108821` | `5.0` |
| normalizer increment absolute deltas | `(17.471575452455085, 17.91624769863312)` | `5.0` |
| probe log-density median absolute delta | `0.0` | `10.0` |
| retained log-density median absolute delta | `0.0` | `10.0` |

## Interpretation

P62 fixed the immediate executable-source discrepancy that caused the high-rank
d=18 row to fail before rank comparison: active defensive mass is now positive
and source-anchored.  The d=18 test still does not pass the same-route rank
convergence gate.  The remaining blockers are now threshold failures after both
candidate rows build, which points back to the known source-loop fidelity gaps
rather than to the defensive normalizer floor.

## Remaining Gaps

1. Source `computeL` / weighted recentering / affine scaling / determinant
   accounting is still not fully matched.
2. Source fit-data path is still not matched: the author uses propagated
   weighted samples, `datasample`, and `InputData(samples_init, samples_debug)`.
3. The current P59/P60 rank comparator is still a bounded fixed-HMC diagnostic,
   not full paper-scale d=18 filtering correctness.
4. d=50/d=100 feasibility remains out of scope until d=18 source-loop fidelity
   and rank convergence are established.

