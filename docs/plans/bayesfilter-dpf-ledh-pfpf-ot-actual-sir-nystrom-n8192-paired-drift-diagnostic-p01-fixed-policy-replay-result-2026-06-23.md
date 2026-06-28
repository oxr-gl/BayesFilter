# P01 Result: Fixed-Policy Replay And Seed Replication

Date: 2026-06-23

Status: `REPLAYED_SINGLE_SEED_DRIFT`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | The original failed seed reproduced, but nearby seeds did not fail; P02 repair selection is not authorized under the reviewed plan. |
| Primary criterion status | Passed as a diagnostic/classification phase: all three artifacts were written and valid. |
| Veto diagnostic status | Seed `82921` fired `paired:paired_log_likelihood_mean_abs_delta`; seeds `82922` and `82923` had no hard vetoes. |
| Main uncertainty | The drift is reproducible for seed `82921`, but not repeated across the two nearby one-seed rows. More replication would be needed before a repair/tuning phase is justified. |
| Next justified action | Proceed to P04 closeout as `REPLAYED_SINGLE_SEED_DRIFT`, unless the owner explicitly approves broader replication. |
| What is not being concluded | No default readiness, no repair success, no statistical ranking, no posterior correctness, no HMC readiness, no broad rank/epsilon robustness. |

## Classification

P01 classification: `REPLAYED_SINGLE_SEED_DRIFT`

Reason:

- Replay seed `82921` failed paired mean threshold again.
- Nearby seed `82922` passed.
- Nearby seed `82923` passed.
- All rows used the frozen fixed policy and had finite route outputs and valid
  Nystrom residuals.

Under the reviewed P01 handoff, only `REPRODUCED_AND_REPEATED_DRIFT` can proceed
to P02 repair selection. Therefore P02 is not opened.

## Evidence Summary

Fixed policy for all rows:

- `rank=32`;
- `epsilon=0.5`;
- `kernel_mode=raw`;
- `scaling_normalization=none`;
- `core_solver=cholesky`;
- `float32`, TF32 enabled, JIT compiled;
- route `both`;
- history mode `value-only`;
- trusted physical GPU1.

| Seed | Status | Hard vetoes | Paired max delta | Paired mean delta | Row residual | Column residual | Wall seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `82921` | `FAIL` | `['paired:paired_log_likelihood_mean_abs_delta']` | `6.96771240234375` | `6.96771240234375` | `8.71419906616211e-05` | `4.291534423828125e-06` | `32.306093647144735` |
| `82922` | `PASS` | `[]` | `0.80084228515625` | `0.80084228515625` | `9.226799011230469e-05` | `1.430511474609375e-06` | `31.89013680582866` |
| `82923` | `PASS` | `[]` | `3.7215576171875` | `3.7215576171875` | `9.655952453613281e-05` | `3.337860107421875e-06` | `31.9615833919961` |

Paired thresholds:

- max absolute delta threshold: `10.0`;
- mean absolute delta threshold: `5.0`.

## Artifacts

- `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-replay-seed82921-r32-eps0p5-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-replay-seed82921-r32-eps0p5-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-n8192-drift-p01-replay-seed82921-r32-eps0p5-2026-06-23.log`
- `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82922-r32-eps0p5-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82922-r32-eps0p5-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-n8192-drift-p01-seed82922-r32-eps0p5-2026-06-23.log`
- `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82923-r32-eps0p5-2026-06-23.json`
- `docs/benchmarks/actual-sir-nystrom-n8192-drift-p01-seed82923-r32-eps0p5-2026-06-23.md`
- `docs/plans/logs/actual-sir-nystrom-n8192-drift-p01-seed82923-r32-eps0p5-2026-06-23.log`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, TensorFlow `2.20.0` |
| GPU status | Trusted GPU1 selected; TensorFlow saw it as `/GPU:0` under `CUDA_VISIBLE_DEVICES=1`. |
| Random seeds | `82921`, `82922`, `82923`. |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p01-fixed-policy-replay-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p01-fixed-policy-replay-result-2026-06-23.md` |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Seed `82921` reproducibly fails the paired mean threshold; nearby seeds `82922` and `82923` pass. |
| Statistically supported ranking | None. These are one-seed hard-screen diagnostics. |
| Descriptive-only differences | Runtime, residual magnitudes below thresholds, and paired deltas for passing seeds are descriptive only. |
| Default-readiness | No. |
| Next evidence needed | Closeout, or a separately approved broader replication plan before repair/tuning. |

## Interpretation

The original failure is reproducible and not a GPU0-only artifact: seed `82921`
failed again on physical GPU1 with the same paired delta. However, the drift did
not repeat on nearby seeds `82922` and `82923`. That makes this a
seed-specific hard-screen failure under current evidence, not yet a repair-ready
repeated high-N failure.

## Post-Run Red-Team Note

Strongest alternative explanation: seed `82921` may expose a deterministic
model/particle realization where fixed `rank=32,epsilon=0.5` is insufficient,
while nearby seeds remain within tolerance.

What would overturn this result: discovering that seed `82921` replay used a
different policy, comparator, threshold, or data path than the nearby rows; the
artifacts do not indicate that.

Weakest part of the evidence: only two nearby seeds were checked, so this is
not a statistical estimate of failure probability.
