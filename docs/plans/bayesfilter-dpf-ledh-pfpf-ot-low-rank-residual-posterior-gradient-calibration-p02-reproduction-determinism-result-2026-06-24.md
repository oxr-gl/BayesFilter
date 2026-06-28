# P02 Three-Seed Reproduction And Jitter Result

Date: 2026-06-25

Status: `LOW_RANK_GRADIENT_REPAIR_REQUIRED`

## Phase Objective

P02 reran `lgssm_small_exact_ref` seeds `91001,91002,91003` for both
`streaming` and `low_rank` routes with three repeats under trusted GPU/XLA
settings.  The phase question was whether the seed `91003` residual exceedance
corresponds to posterior value, gradient, or peak-neighborhood harm, and whether
the residual behavior is stable across repeats.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Scientific/engineering question | Partially answered.  The trusted GPU/XLA reproduction ran and produced structured artifacts, but low-rank nonfinite-gradient vetoes prevent calibration or P03 handoff. |
| Baseline/comparator | Exact Kalman value/gradient oracle and paired streaming finite-particle route were used for the same seeds/probes. |
| Primary pass/fail criterion | Failed. Required rows did not all produce finite value/gradient diagnostics with no hard validity vetoes. |
| Veto diagnostics | Fired: low-rank route value/gradient nonfinite hard vetoes on seeds `91002` and `91003`. |
| Explanatory diagnostics | Residuals, repeat summaries, peak-neighborhood labels, timings, projection iterations, and streaming route diagnostics are recorded but are not promotion criteria after the hard veto. |
| Not concluded | No calibrated residual threshold, no holdout validation, no posterior correctness, no HMC readiness, no default/package/public API readiness, no statistical superiority, and no scientific-validity claim. |
| Preserved artifact | `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.json` and matching Markdown/log artifacts, with internal phase/title metadata quarantined as stale. |

## Execution Notes

Initial continuation from the reset memo found the expected environment
boundary:

- sandboxed `/dev/nvidia*` files were absent;
- sandboxed TensorFlow was CUDA-capable but reported no GPUs;
- trusted/elevated `/dev/nvidia*` checks and TensorFlow GPU checks passed.

The first trusted P02 launch reached GPU/XLA but failed before artifact
creation on an XLA `FakeParam` compile error from a dead skip branch in the
fixed-resampling route conditional.  The LGSSM fixture uses an all-active fixed
resampling mask, so the harness was patched to carry
`fixed_resampling_policy="all_active"` and avoid compiling the dead
`tf.cond` branch for this fixture.  The dynamic branch remains available for
non-static policies.

Focused verification after the patch:

```bash
python -m py_compile docs/benchmarks/benchmark_low_rank_ledh_lgssm_kalman_gate.py docs/benchmarks/benchmark_low_rank_ledh_posterior_gradient_calibration.py
python -m pytest tests/test_low_rank_ledh_lgssm_kalman_gate.py tests/test_low_rank_ledh_posterior_gradient_calibration.py -q
```

Result: compile passed; focused tests passed (`7 passed`).

One-seed trusted GPU smoke after the patch:

- command used seed `91001`, both routes, full horizon, one repeat;
- JSON/Markdown were written under `/tmp`;
- both rows reported `PASS` and hard vetoes `[]`.

## P02 Command Actually Run

```bash
python docs/benchmarks/benchmark_low_rank_ledh_posterior_gradient_calibration.py \
  --case-ids lgssm_small_exact_ref \
  --seeds 91001,91002,91003 \
  --route both \
  --num-particles 1024 \
  --time-steps 12 \
  --low-rank-rank 16 \
  --low-rank-assignment-epsilon 0.25 \
  --low-rank-alpha 1.0e-8 \
  --low-rank-max-projection-iterations 120 \
  --particle-chunk-size 64 \
  --warmups 0 \
  --repeats 3 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.md \
  --quiet
```

Stdout/stderr were captured to:
`docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/p02-reproduction-gpu.log`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Working tree | Dirty before and after this phase; unrelated pre-existing changes were preserved. |
| Python executable | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python` |
| Python version | `3.13.13` |
| TensorFlow / TFP | `2.20.0` / `0.25.0` |
| Device scope | `visible` |
| CUDA_VISIBLE_DEVICES | `1` |
| Device | `/GPU:0` |
| TensorFlow physical GPUs | `PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')` |
| TensorFlow logical GPUs | `LogicalDevice(name='/device:GPU:0', device_type='GPU')` |
| GPU trust basis | `owner_designated_managed_session_visible_gpu_trusted` |
| TF32 | requested `enabled`; execution recorded `True` |
| XLA/JIT | `True` |
| dtype | `float32` |
| Seeds | `91001,91002,91003` |
| Wall time | `994.8340680901892` seconds |
| JSON artifact | `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.json` |
| Markdown artifact | `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.md` |
| Log artifact | `docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/p02-reproduction-gpu.log` |

## Artifact Metadata Quarantine

The P02 JSON and generated Markdown are preserved as raw run artifacts, but
their internal `phase` field and generated Markdown title are quarantined as
stale metadata.  They still say
`LOW_RANK_RESIDUAL_POSTERIOR_GRADIENT_CALIBRATION_P01` / `P01` because the
reset-memo command did not override the harness default `--phase-id`.

Canonical P02 identity must therefore come from this result note, the P02
subplan, the command actually run, the artifact filenames, and the execution
ledger, not from the raw artifact's internal phase/title fields.  Future tools
or reviewers must not classify the artifact as P01 based on those internal
metadata fields.  This metadata issue does not rescue the hard veto and should
be fixed before future phase artifacts.

## Row Outcomes

| Seed | Route | Status | Hard vetoes | Peak match | Max value abs error | Max gradient relative error | Min gradient cosine |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: |
| 91001 | `streaming` | `PASS` | `[]` | `False` | `1.8691673278808594` | `95.39123646636848` | `0.5425920843771693` |
| 91001 | `low_rank` | `PASS` | `[]` | `False` | `1.9766120910644531` | `1.3879955018116232` | `0.7790965268517905` |
| 91002 | `streaming` | `PASS` | `[]` | `True` | `0.84759521484375` | `0.46733367846566354` | `0.9336252867698753` |
| 91002 | `low_rank` | `FAIL` | `qr_plus:route_value_gradient_nonfinite` | `True` | `0.8533077239990234` | `0.27357667743077113` | `0.9620311935393715` |
| 91003 | `streaming` | `PASS` | `[]` | `True` | `0.9239311218261719` | `71.04166096343143` | `-0.22177463496854144` |
| 91003 | `low_rank` | `FAIL` | `center`, `q_plus`, `q_minus`, `r_plus`, `r_minus`, `qr_plus`: `route_value_gradient_nonfinite` | `True` | `0.9209480285644531` | `nan` | `nan` |

Important interpretation discipline:

- The low-rank route hard veto is gradient validity, not value finiteness.  The
  affected low-rank probe value errors were finite, but route-gradient
  diagnostics became nonfinite.
- The streaming route passed hard vetoes for all three seeds, but streaming
  descriptive gradient errors remain explanatory only and do not establish
  statistical superiority or posterior correctness.
- The repeat summaries were stable within this artifact, but the nonfinite
  low-rank gradient veto blocks residual-threshold calibration.

## Nonfinite Low-Rank Probe Details

Seed `91002`, low-rank route:

- `qr_plus`, theta `[0.05000000074505806, 0.05000000074505806]`:
  gradient cosine, max coordinate error, and relative norm error were `nan`;
  value absolute error was finite at `0.8533077239990234`.

Seed `91003`, low-rank route:

- `center`, theta `[0.0, 0.0]`: gradient diagnostics `nan`; value absolute
  error `0.8679141998291016`.
- `q_plus`, theta `[0.05000000074505806, 0.0]`: gradient diagnostics `nan`;
  value absolute error `0.8985481262207031`.
- `q_minus`, theta `[-0.05000000074505806, 0.0]`: gradient diagnostics `nan`;
  value absolute error `0.8378353118896484`.
- `r_plus`, theta `[0.0, 0.05000000074505806]`: gradient diagnostics `nan`;
  value absolute error `0.8930473327636719`.
- `r_minus`, theta `[0.0, -0.05000000074505806]`: gradient diagnostics `nan`;
  value absolute error `0.8393001556396484`.
- `qr_plus`, theta `[0.05000000074505806, 0.05000000074505806]`: gradient
  diagnostics `nan`; value absolute error `0.9209480285644531`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Stop before P03 and require low-rank gradient repair. | Failed: not all required low-rank rows produced finite value/gradient diagnostics. | Fired: `route_value_gradient_nonfinite` on low-rank seeds `91002` and `91003`. | The artifact identifies nonfinite gradients but not yet the internal solver operation causing them. | Run the smallest repair diagnostic that localizes the nonfinite low-rank gradient path under GPU/XLA before any calibration grid. | This does not reject the full research direction, does not calibrate a residual threshold, and does not validate or invalidate heldout/default readiness. |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Failed for the locked low-rank candidate due to nonfinite route-gradient diagnostics. |
| Statistically supported ranking | None. Three seeds/repeats without uncertainty analysis do not support route ranking. |
| Descriptive-only differences | Value errors, gradient relative errors, cosine similarities, peak labels, residuals, timings, ESS, and projection iterations are descriptive after the hard veto. |
| Default-readiness | Not assessed and not supported. |
| Next evidence needed | A focused GPU/XLA gradient repair artifact showing finite low-rank route values/gradients on the P02 failing probes, followed by a rerun of P02. |

## Post-Run Red-Team Note

Strongest alternative explanation: the nonfinite gradients may be caused by a
specific differentiability issue in the low-rank coupling solver or harness
parameterization, not by the low-rank residual itself.  The result therefore
rejects the current locked candidate artifact for calibration, not the entire
low-rank research direction.

What would overturn this stop decision: a focused repair showing the current
P02 artifact misclassified gradients as nonfinite because of a harness bug,
followed by a rerun that produces finite low-rank route gradients and no hard
validity vetoes for all required P02 rows.

Weakest part of the evidence: the artifact does not yet localize the internal
operation that first emits a nonfinite gradient.  That localization is the next
smallest discriminating artifact.

## Phase Handoff

P02 does not hand off to P03.  The P02 subplan says that if gradients are
nonfinite, execution should stop for repair instead of running the P03
calibration grid.

Recommended next state:

- `LOW_RANK_GRADIENT_REPAIR_REQUIRED`

Recommended next command class:

- a bounded, focused TensorFlow GPU/XLA diagnostic on the failing low-rank
  probes (`91002:qr_plus` and seed `91003` center/probe neighborhood), recording
  the first nonfinite value/gradient source inside the low-rank route.
