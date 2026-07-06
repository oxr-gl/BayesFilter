# P02A Low-Rank Gradient Repair Diagnostic Result

Date: 2026-06-25

Status: `LOW_RANK_LIKELIHOOD_GRADIENT_DISCONNECTED`

## Phase Objective

P02A ran the repair-loop diagnostic required after P02 stopped with
`LOW_RANK_GRADIENT_REPAIR_REQUIRED`.  It targeted only the P02 failing
low-rank seed/probe pairs and did not advance to P03.

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Answered for the failing probes: the low-rank route likelihood and final-particle paths are disconnected from `theta`. |
| Baseline/comparator | Canonical P02 result note plus the P02 raw data payload and same LGSSM exact-reference fixture/probe definitions.  The P02 raw artifact's internal phase/title metadata is stale and must not be used for phase identity. |
| Primary pass/fail criterion | Passed as a localization diagnostic: JSON/Markdown artifacts identify value-gradient, likelihood-gradient, prior-gradient, final-particle-gradient, route-output, and factor diagnostics for every failing probe. |
| Veto diagnostics | Fired for the candidate: likelihood gradients are disconnected/nonfinite and final-particle gradients are disconnected/nonfinite on all P02 failing probes. |
| Explanatory diagnostics | Route outputs, factors, particles, and `g` were finite; selected factor/induced residuals and projection iterations are recorded. |
| Not concluded | No residual-threshold calibration, no P03 handoff, no holdout validation, no posterior correctness, no HMC readiness, no default/package/public API readiness, no statistical superiority, and no scientific-validity claim. |
| Preserved artifact | `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02a-gradient-repair-diagnostic-2026-06-25.json` plus Markdown/log artifacts. |

P02 baseline metadata caveat: the P02 reproduction JSON/Markdown data payload
is used only for failing-probe content.  Its internal phase/title fields are
quarantined as stale metadata; P02 identity comes from the P02 result note,
command, filenames, and execution ledger.

## Command Actually Run

```bash
python docs/benchmarks/benchmark_low_rank_ledh_gradient_nonfinite_diagnostic.py \
  --case-id lgssm_small_exact_ref \
  --num-particles 1024 \
  --time-steps 12 \
  --low-rank-rank 16 \
  --low-rank-assignment-epsilon 0.25 \
  --low-rank-alpha 1.0e-8 \
  --low-rank-max-projection-iterations 120 \
  --particle-chunk-size 64 \
  --dtype float32 \
  --tf32-mode enabled \
  --device-scope visible \
  --cuda-visible-devices 1 \
  --device /GPU:0 \
  --expect-device-kind gpu \
  --output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02a-gradient-repair-diagnostic-2026-06-25.json \
  --markdown-output docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02a-gradient-repair-diagnostic-2026-06-25.md \
  --quiet
```

Stdout/stderr were captured to:
`docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/p02a-gradient-repair-diagnostic-gpu.log`.

Execution anomaly: the script wrote complete JSON/Markdown artifacts and then
the TensorFlow process remained alive while still holding GPU memory.  It was
terminated manually after artifact validation.  The final shell status is
therefore `143`, but the structured artifacts report `ended_at` and
`wall_time_seconds`.

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
| Candidate | `r16_eps0p25_alpha1em08_it120` |
| Failing probes | `91002:qr_plus`; `91003:center,q_plus,q_minus,r_plus,r_minus,qr_plus` |
| Artifact wall time | `131.44918191293254` seconds |
| JSON artifact | `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02a-gradient-repair-diagnostic-2026-06-25.json` |
| Markdown artifact | `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02a-gradient-repair-diagnostic-2026-06-25.md` |
| Log artifact | `docs/logs/low-rank-residual-posterior-gradient-calibration-2026-06-24/p02a-gradient-repair-diagnostic-gpu.log` |

## Diagnostic Outcome

| Seed | Probe | Value gradient | Likelihood gradient | Prior gradient | Final-particle gradient | Route outputs | Factor/particle validity |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 91002 | `qr_plus` | finite, connected | disconnected/nonfinite | finite, connected | disconnected/nonfinite | finite | factors, particles, and `g` finite/valid |
| 91003 | `center` | finite, connected | disconnected/nonfinite | finite, connected | disconnected/nonfinite | finite | factors, particles, and `g` finite/valid |
| 91003 | `q_plus` | finite, connected | disconnected/nonfinite | finite, connected | disconnected/nonfinite | finite | factors, particles, and `g` finite/valid |
| 91003 | `q_minus` | finite, connected | disconnected/nonfinite | finite, connected | disconnected/nonfinite | finite | factors, particles, and `g` finite/valid |
| 91003 | `r_plus` | finite, connected | disconnected/nonfinite | finite, connected | disconnected/nonfinite | finite | factors, particles, and `g` finite/valid |
| 91003 | `r_minus` | finite, connected | disconnected/nonfinite | finite, connected | disconnected/nonfinite | finite | factors, particles, and `g` finite/valid |
| 91003 | `qr_plus` | finite, connected | disconnected/nonfinite | finite, connected | disconnected/nonfinite | finite | factors, particles, and `g` finite/valid |

Important nuance: the finite value gradient in this diagnostic is prior-only on
the failing probes.  For example, `91003:center` reports value gradient
`[-0.0, -0.0]`, likelihood gradient disconnected, and prior gradient
`[-0.0, -0.0]`; the nonzero off-center probes similarly match the prior
gradient.  Therefore the finite value-gradient field does not repair the P02
posterior-gradient hard veto.

## Interpretation

P02A localizes the P02 low-rank failure to gradient connectivity in the
low-rank route likelihood/final-particle path.  It does not show nonfinite route
values, nonfinite route outputs, nonfinite factors, nonfinite particles,
negative factors, or nonpositive `g`.

The next repair should inspect the low-rank route operations that can sever
gradient flow from scaled LGSSM covariances through particles and weights into
`route_outputs.log_likelihood`.  Any source-code hint, including possible
`tf.stop_gradient` involvement, is a hypothesis outside the P02A artifact
evidence until a route-internal connectivity probe confirms it.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Stop before P03 and repair the low-rank likelihood-gradient path. | Diagnostic objective met: source class localized for all P02 failing probes. | Candidate still vetoed: likelihood and final-particle gradients are disconnected/nonfinite. | The specific TensorFlow operation that severs connectivity remains unidentified. | Add the smallest route-internal gradient-connectivity probe, then patch only the confirmed break and rerun P02A followed by P02. | This is not threshold calibration, holdout validation, posterior correctness, HMC readiness, default readiness, statistical superiority, or scientific validity evidence. |

## Inference-Status Table

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Failed for the locked low-rank candidate: likelihood/final-particle gradients disconnected on all P02 failing probes. |
| Statistically supported ranking | None. P02A is a deterministic localization diagnostic on preselected failing probes. |
| Descriptive-only differences | Residual magnitudes and projection iterations are explanatory only. |
| Default-readiness | Not assessed and not supported. |
| Next evidence needed | A focused repair artifact showing connected finite low-rank likelihood/final-particle gradients on the P02A probes, followed by a full trusted GPU/XLA P02 rerun with all hard vetoes passing. |

## Post-Run Red-Team Note

Strongest alternative explanation: the diagnostic could still be measuring a
diagnostic-specific connectivity pattern rather than the exact P02 path.
Mitigation: the diagnostic uses the same scaled fixture, low-rank route core,
candidate settings, failing probes, GPU, TF32, and XLA path as P02.

Weakest evidence point: the result localizes the failure class but not the exact
operation causing disconnection.  A route-internal connectivity probe is needed
before making an implementation repair.
