# P01 Diagnostic Adequacy And Missing-Instrumentation Gate Result

Date: 2026-06-23

Status: `P01_PASS_MINIMAL_INSTRUMENTATION`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Accept diagnostics as adequate for P02 after adding missing compiled-row denominator serialization | `PASS`: focused tests passed and P02 subplan was refreshed | `PASS`: no default/raw behavior change, threshold change, or repair selection occurred | Diagnostics can guide selection, but do not prove any repair will preserve paired comparability | Begin P02 repair selection with Claude read-only review | No repair effectiveness, no default readiness, no ranking, no scientific validity |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Are diagnostics sufficient to select one less-intrusive repair, or is minimal opt-in instrumentation needed? |
| Baseline/comparator | Current Nystrom diagnostics and compiled redo harness output fields. |
| Primary pass criterion | `PASS`: required diagnostic fields are now available in tensor code and compiled-row serialization; focused tests passed. |
| Veto diagnostics | `PASS`: no default behavior change, CLI incompatibility, threshold change, or missing P02 handoff. |
| Explanatory diagnostics | Factor diagonal/ranges, core spectrum/ranges, kernel projection fields, scaling ranges, finite flags, residuals, paired deltas, and denominator fields are available. |
| Not concluded | No repair selection, no repair effectiveness, no default readiness. |

## What Changed

P01 found that `nystrom_transport_resample_tensors_tf` already exposed
`min_kernel_denominator` and `denominator_floor_hits`, but
`docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` did not
serialize those fields into the compiled actual-SIR Nystrom row.

Minimal patch:

- added `min_kernel_denominator` and `denominator_floor_hits` to
  `NystromValueTensors`;
- threaded both fields through `_nystrom_value_core`, the compiled Nystrom
  output tuple, and the Nystrom result row;
- added focused assertions in
  `tests/test_actual_sir_nystrom_compiled_redo.py`.

This is instrumentation only.  It does not add a repair mode, change thresholds,
change rank/epsilon defaults, or change the raw Nystrom computation.

## Local Checks

Focused CPU-hidden tests:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py
```

Log:

- `docs/plans/logs/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-focused-tests-2026-06-23.log`

Result: `10 passed, 14695 warnings in 22.87s`.

Focused serialization check:

```bash
python - <<'PY'
...
print('P01 denominator diagnostic serialization check PASS')
PY
```

Result: `P01 denominator diagnostic serialization check PASS`.

## P02 Refresh

P02 subplan was refreshed to inherit the P01 diagnostic surface:

- `min_kernel_denominator`;
- `denominator_floor_hits`;
- factor diagonal/range fields;
- core spectrum/range fields;
- kernel projection fields;
- scaling ranges;
- finite flags;
- residuals;
- paired deltas.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu`; CPU-hidden by `CUDA_VISIBLE_DEVICES=-1` before TensorFlow imports |
| GPU status | Intentionally hidden for focused CPU diagnostic tests |
| Data/model | Tiny CPU test fixtures only; no serious actual-SIR GPU row in P01 |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-diagnostic-adequacy-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-less-intrusive-stability-p01-diagnostic-adequacy-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` for instrumentation adequacy. |
| Statistically supported ranking | `NO`. |
| Descriptive-only differences | Diagnostic fields only; no method comparison. |
| Default-readiness | `NO`. |
| Next evidence needed | P02 repair selection and review. |

## Post-Run Red Team

Strongest alternative explanation: denominator diagnostics may not be the
dominant failure mechanism.  P02 must still consider factor normalization,
log-stable scaling, spectral variants, fixed-policy restriction, and
positive-projection diagnostic evidence without overclaiming.

Weakest part of evidence: P01 validates serialization and unit mechanics, not
serious GPU repair behavior.

What would overturn this P01 decision: a P02 or P04 artifact showing the
serialized denominator fields are missing, stale, or not connected to the
compiled Nystrom row.

## Next Action

Begin P02 less-intrusive repair selection and Claude read-only review.
