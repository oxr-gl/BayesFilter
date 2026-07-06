# Actual-SIR Nystrom Stability Repair P05 Focused Repair Result

Date: 2026-06-23

Status: `PASS_FOCUSED_IMPLEMENTATION_READY_FOR_P06`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Implemented opt-in `positive_projected` Nystrom kernel diagnostic mode and proceed to P06 serious GPU gate | `PASS`: focused tests pass; raw remains default; opt-in mode is selectable, XLA-compatible on tiny fixture, and records projection diagnostics | No focused test failure, no default-policy change, no threshold change, no broad refactor | P05 tests do not prove serious-model rescue; `positive_projected` may be dense/diagnostic-only at `N=1024` | Run P06 on the two failing rows plus the control with only `--nystrom-kernel-mode positive_projected` toggled | No default readiness, no scalable/high-N readiness, no dense Sinkhorn equivalence, no posterior correctness, no HMC readiness |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Was the opt-in positive-projected Nystrom kernel diagnostic implemented correctly and narrowly enough to test? |
| Primary criterion | `PASS`: tests verify raw default, opt-in metadata, XLA acceptance, and a discriminating projection floor-hit fixture. |
| Veto diagnostics | `PASS`: no threshold/default/rank/epsilon/core-solver policy change. |
| Explanatory diagnostics | Tiny fixture projection floor hits and metadata propagation. |
| Not concluded | Serious-model rescue deferred to P06. |

## Implementation Summary

Touched files:

- `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
- `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`
- `tests/test_nystrom_transport_tf.py`
- `tests/test_actual_sir_nystrom_compiled_redo.py`

Implemented:

- `kernel_mode="raw"` default.
- `kernel_mode="positive_projected"` opt-in diagnostic mode.
- Dense diagnostic positive projection of the implied approximate Nystrom
  kernel only in the opt-in mode.
- Diagnostics:
  - `raw_kernel_min`
  - `projected_kernel_min`
  - `projection_floor_hits`
  - `nystrom_kernel_mode`
  - `nystrom_kernel_mode_scope`
- Benchmark CLI:
  `--nystrom-kernel-mode {raw,positive_projected}`.

The raw path keeps the existing factor application and remains the default.

## Required Checks

```bash
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py
```

Result: `PASS`.

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py
```

Result: `10 passed` with TensorFlow/gast deprecation warnings.

## Discriminating Fixture

`tests/test_nystrom_transport_tf.py` now includes
`test_positive_projected_kernel_mode_records_discriminating_floor_hits`.

This fixture intentionally uses a high diagnostic `denominator_floor=0.25` on a
small deterministic particle set.  The raw mode records `raw_kernel_min=nan`,
while `positive_projected` records:

- `raw_kernel_min < 0.25`;
- `projected_kernel_min >= 0.25`;
- `projection_floor_hits > 0.0`.

This proves P05 is not a no-op metadata change.

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` for focused implementation tests. |
| Statistically supported ranking | `NO`. |
| Descriptive-only differences | Tiny fixture diagnostics and test runtime. |
| Default-readiness | `NO`. |
| Next evidence needed | P06 serious GPU rows with `--nystrom-kernel-mode positive_projected`. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | CPU-hidden py_compile and focused pytest commands listed above |
| Environment | Python/TensorFlow test environment under `/home/ubuntu/anaconda3/envs/tfgpu` |
| GPU status | CPU-hidden by `CUDA_VISIBLE_DEVICES=-1`; no trusted GPU row in P05 |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p05-focused-repair-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p05-focused-repair-result-2026-06-23.md` |

## Post-Run Red Team

Strongest alternative explanation: positive projection may merely make the
diagnostic `N=1024` rows finite by changing the transport object enough to lose
paired comparability or by introducing dense materialization that is not viable
at high `N`.

What would overturn continuation: P06 finding any nonfinite output, residual
threshold failure, paired-threshold failure, control regression, missing GPU
evidence, or projection diagnostics showing the opt-in path was not exercised.

## Next Action

Run the refreshed P06 serious GPU repair gate with the exact flag:

```bash
--nystrom-kernel-mode positive_projected
```

All other paired-comparison invariants must remain fixed.
