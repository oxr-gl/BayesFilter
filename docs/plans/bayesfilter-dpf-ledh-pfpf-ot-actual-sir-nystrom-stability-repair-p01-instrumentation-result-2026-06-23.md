# P01 Instrumentation Implementation Result

Date: 2026-06-23

Status: `PASS`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to P02 failure localization diagnostics | `PASS`: focused CPU-hidden tests passed and diagnostics are opt-in | No implementation/test veto fired | Serious-model GPU diagnostics still need P02 artifacts | Run P02 failing/control rows with `--nystrom-diagnostics` enabled | No repair, no default readiness, no statistical ranking, no posterior correctness, no HMC readiness |

## Implementation Summary

Added opt-in diagnostic fields to the fixed-rank Nystrom route and compiled
actual-SIR harness:

- factor diagonal min/max and max diagonal error;
- landmark core min/max eigenvalue, condition proxy, and effective rank when
  diagnostics are enabled;
- left factor, core matrix, and Sinkhorn scaling min/max summaries;
- harness-level aggregation across route invocations;
- CLI flag `--nystrom-diagnostics`, disabled by default.

Default algorithmic behavior remains `cholesky` with diagnostics disabled unless
the caller explicitly enables diagnostics.

## Local Checks

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py
```

Result: `8 passed`.

Warnings were TensorFlow/TFP/gast deprecation warnings and did not affect the
focused pass/fail criterion.

## Artifact And Code Touch Set

- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
- `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`
- `tests/test_nystrom_transport_tf.py`
- `tests/test_actual_sir_nystrom_compiled_redo.py`
- This result file.
- Refreshed P02 subplan.

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` for focused implementation checks |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Diagnostic values in tiny fixtures only |
| Default-readiness | `NO` |
| Next evidence needed | P02 trusted GPU failure-localization artifacts |

## Handoff To P02

P02 may begin because:

- instrumentation exists and is opt-in;
- focused tests passed;
- default behavior was not promoted or changed;
- P02 subplan has exact rows, artifacts, logs, and manifest requirements.

## Nonclaims

- P01 did not repair the serious-model nonfinite failure.
- P01 did not establish robustness or default readiness.
- P01 did not rank tuning options.
