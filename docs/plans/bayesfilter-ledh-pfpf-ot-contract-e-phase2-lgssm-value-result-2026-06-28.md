# Phase 2 Result: Contract E LGSSM value gate

Date: 2026-06-28

Status: `PHASE2_PASSED`

Master program:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-residual-affine-testing-master-program-2026-06-28.md`

Runbook:
`docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-visible-gated-execution-runbook-2026-06-28.md`

## Phase Objective

Test whether the Contract E reset arm reduces the LGSSM value gap relative to
old barycentric OT and matches the exact Kalman value within stated Monte Carlo
uncertainty on 1d and 2d \(T=10\) fixtures.

## Artifacts

- Diagnostic script:
  `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py`
- CPU-hidden smoke JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-smoke-2026-06-28.json`
- CPU-hidden smoke Markdown:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-smoke-2026-06-28.md`
- Material GPU/XLA JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-2026-06-28.json`
- Material GPU/XLA Markdown:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-2026-06-28.md`
- Phase 3 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-lgssm-gradient-subplan-2026-06-28.md`

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Passed for the LGSSM value gate under the frozen Phase 2 contract. |
| Baseline/comparator | Exact FP64 Kalman value; no-OT weighted LEDH arm; old barycentric OT reset. |
| Primary criterion | Passed: Contract E is within two MCSE of Kalman and has smaller absolute Kalman-value error than old barycentric OT on both 1d and 2d fixtures. |
| Veto diagnostics | Passed: finite values, MCSE present, trusted GPU visible, XLA requested and compile log observed in the command transcript, TF32 enabled, covariance residual below gate, conditioning below gate, seed schedule recorded. |
| Explanatory diagnostics | Per-seed values, MCSE, old-OT/no-OT deltas, covariance trace ratios, transport residuals, and Contract E condition spectra are in the JSON artifact. |
| Not concluded | No gradient correctness, no SIR/SV correctness, no production readiness, no posterior correctness, no HMC readiness. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `c815edc52162779e969b2982723b2f52770fd849` |
| Working tree | Dirty; unrelated existing changes preserved. |
| Python | `Python 3.11.14` |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` |
| TensorFlow | `2.19.1` in material artifact |
| Device | Trusted GPU-visible run on `LogicalDevice(name='/device:GPU:0', device_type='GPU')` |
| GPU preflight | `nvidia-smi` saw NVIDIA GeForce RTX 4080 SUPER; TensorFlow saw one physical and one logical GPU. |
| TF32/XLA | TF32 enabled; material command transcript showed XLA CUDA service initialization and a compiled-cluster log.  The JSON records `xla: true`; it is request/provenance metadata, not a standalone proof of compilation. |
| Seeds | `SEED_COUNT=10`, seed indices `9100..9109`; initial seeds `[seed,17]`, transition seeds `[seed,29]`, Contract E residual seeds `[seed,43+t]`. |
| Material particle count | `N=1000` frozen before execution. |
| Time steps/state dims | `T=10`, state dims `[1,2]`. |
| Sinkhorn setting | `epsilon=0.5`, finite steps `20`. |
| Reset arms | `ledh_no_ot`, `old_barycentric_ot`, `contract_e`. |
| Old barycentric mapping | `annealed_transport_tf._filterflow_manual_dense_finite_transport_matrix_value_stopped_scale_keys` followed by `tf.linalg.matmul(matrix, post_flow)`. |
| Value scalar | Transition-first LGSSM log marginal likelihood accumulator `sum_t incremental_t` from `core_ledh._normalize_log_weights`. |
| Material wall time | Final reviewed rerun `/usr/bin/time -p`: `real 29.18`, `user 37.38`, `sys 5.83`. |

## Commands Run

Compile/static checks:

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py
git diff --check -- docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py
```

CPU-hidden wiring smoke:

```bash
python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py \
  --device-scope cpu \
  --num-particles 64 \
  --seed-count 10 \
  --time-steps 10 \
  --state-dims 1 \
  --settings 0.5:8 \
  --gate-mode smoke \
  --xla \
  --tf32-mode enabled \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-smoke-2026-06-28.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-smoke-2026-06-28.md
```

Trusted GPU preflight:

```bash
nvidia-smi
python -c "import tensorflow as tf; tf.config.experimental.enable_tensor_float_32_execution(True); print('tf', tf.__version__); print('physical', tf.config.list_physical_devices('GPU')); print('logical', tf.config.list_logical_devices('GPU')); print('tf32', tf.config.experimental.tensor_float_32_execution_enabled())"
```

Material GPU/XLA gate:

```bash
/usr/bin/time -p python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_value.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --num-particles 1000 \
  --seed-count 10 \
  --time-steps 10 \
  --state-dims 1 2 \
  --settings 0.5:20 \
  --gate-mode material \
  --xla \
  --tf32-mode enabled \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-2026-06-28.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase2-lgssm-value-2026-06-28.md
```

## Result Summary

Final material artifact status: `passed`.

| Dim | Arm | Mean | Kalman | Delta | MCSE | abs z MCSE | Cov residual | Condition |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `ledh_no_ot` | `-6.912147` | `-6.914505` | `0.002358` | `0.001444` | `1.634` | `NA` | `NA` |
| 1 | `old_barycentric_ot` | `-6.619977` | `-6.914505` | `0.294528` | `0.002288` | `128.728` | `NA` | `NA` |
| 1 | `contract_e` | `-6.917480` | `-6.914505` | `-0.002975` | `0.002316` | `1.285` | `3.804e-07` | `1.000` |
| 2 | `ledh_no_ot` | `-13.793434` | `-13.784139` | `-0.009296` | `0.006716` | `1.384` | `NA` | `NA` |
| 2 | `old_barycentric_ot` | `-12.963488` | `-13.784139` | `0.820651` | `0.005976` | `137.314` | `NA` | `NA` |
| 2 | `contract_e` | `-13.792360` | `-13.784139` | `-0.008221` | `0.006239` | `1.318` | `8.003e-07` | `1.328` |

## Same-Phase Repair Record

The first material run produced value agreement for both dimensions but failed
the predeclared 2d covariance-restoration gate: Contract E 2d covariance
residual was `8.50e-4` against the `5e-4` limit.  The old-OT and value
comparators were not changed.

Codex inspected the implementation and found that the small \(d_x\times d_x\)
moment-restoration algebra used TensorFlow matmul/einsum paths under TF32
execution.  That made the diagnostic covariance gate sensitive to TF32 GEMM
rounding even though the algebra being checked is only 1d/2d reset-moment
restoration.  Codex repaired the diagnostic implementation by computing the
small Contract E moment, square-root reconstruction, affine map, and affine
particle application with explicit elementwise reductions.  This keeps the
material route GPU/XLA/TF32, but avoids using TF32 GEMM for the tiny covariance
gate itself.

After the repair:

- the CPU-hidden smoke still passed;
- the material GPU/XLA run passed without changing \(N\), seeds, scalar,
  Sinkhorn setting, thresholds, comparators, or old-OT baseline;
- the final artifact records `arms_distinguishable_metadata` for auditability,
  but this metadata is explanatory and is not used as a pass/fail veto;
- the 2d covariance residual dropped to `8.00e-7`;
- the 1d and 2d value gates both passed.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 2 LGSSM value gate as passed. | Passed: Contract E is within two MCSE of exact Kalman and improves over old barycentric OT for 1d and 2d. | Passed after same-phase numerical repair and bounded result review: finite values, GPU/XLA/TF32 evidence, MCSE, covariance restoration, conditioning, seed schedule, and old-OT mapping are recorded. | This is still a value gate only; gradient behavior may fail even when value passes. | Launch Phase 3 precheck under the reviewed subplan. | No gradient correctness, no nonlinear-model correctness, no production/HMC/posterior claim. |
| Advance to Phase 3 precheck. | Phase 3 subplan freezes the same scalar/comparator discipline and the FD step-size rule. | Phase 3 must still implement and pass its own gradient evidence gates before any downstream claim. | Same-scalar gradient agreement may expose a different issue than value matching. | Create/compile the Phase 3 gradient diagnostic and run the CPU-hidden wiring smoke before any material GPU/XLA gradient run. | Phase 2 does not certify same-scalar derivatives. |

## Post-Run Red-Team Note

The strongest alternative explanation is that Contract E is essentially
restoring the no-OT weighted cloud moments in LGSSM, so value agreement here may
not imply a generally useful reset for nonlinear models.  The result would be
weakened if Phase 3 shows same-scalar gradient disagreement, if SIR/SV FD gates
fail, or if larger/tougher LGSSM fixtures reveal covariance conditioning
failures.

The weakest part of the evidence is scope: this is a small 1d/2d LGSSM value
diagnostic with \(N=1000\) and 10 seeds.  It is a necessary repair signal for
the old barycentric covariance-loss bug, not a production certification.

## Nonclaims

This result does not conclude:

- Contract E gradient correctness;
- SIR/SV or other nonlinear correctness;
- posterior correctness;
- HMC readiness;
- production readiness;
- broad Contract E validity beyond this LGSSM value gate.

## Next Action

Phase 2 closes as passed after bounded Claude result review returned
`VERDICT: AGREE`.  Advance to Phase 3 precheck.  The next action is to create
and compile `docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py`
under the reviewed Phase 3 subplan, then run the CPU-hidden wiring smoke before
any material GPU/XLA gradient run.
