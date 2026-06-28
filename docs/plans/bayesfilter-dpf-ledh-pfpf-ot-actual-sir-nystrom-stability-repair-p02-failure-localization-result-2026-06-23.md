# P02 Failure Localization Diagnostics Result

Date: 2026-06-23

Status: `PASS_AMBIGUOUS_LOCALIZATION_NEEDS_PREFIX_TRACE`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Continue to a sharper P03 prefix/first-failure diagnostic before selecting a repair family | `PARTIAL_PASS`: required artifacts were written and the control row passed with finite diagnostics, but both failing rows were all-NaN in aggregate Nystrom diagnostics | Known hard vetoes reproduced for both failing rows; control had no hard vetoes | Aggregate diagnostics identify the failure as inside/at the Nystrom factor-scaling route but not the first failing time/stage | Run P03 prefix rows and first-failure-oriented diagnostics before tuning or repair | No repair, no default readiness, no statistical ranking, no posterior correctness, no HMC readiness |

## Artifacts

| Row | JSON | Markdown | Log |
| --- | --- | --- | --- |
| `rank=32,epsilon=0.25` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r32-eps0p25-2026-06-23.json` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r32-eps0p25-2026-06-23.md` | `docs/plans/logs/actual-sir-nystrom-stability-repair-p02-r32-eps0p25-2026-06-23.log` |
| `rank=64,epsilon=0.3` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r64-eps0p3-2026-06-23.json` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r64-eps0p3-2026-06-23.md` | `docs/plans/logs/actual-sir-nystrom-stability-repair-p02-r64-eps0p3-2026-06-23.log` |
| `rank=32,epsilon=0.5` control | `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r32-eps0p5-control-2026-06-23.json` | `docs/benchmarks/actual-sir-nystrom-stability-repair-p02-r32-eps0p5-control-2026-06-23.md` | `docs/plans/logs/actual-sir-nystrom-stability-repair-p02-r32-eps0p5-control-2026-06-23.log` |

## Row Outcomes

| Row | Status | Hard vetoes | Finite factors | Finite particles | Core condition proxy | Effective rank min | Factor diag min/max | Residuals |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| `rank=32,epsilon=0.25` | `FAIL` | `nonfinite_log_likelihood`, `nonfinite_nystrom_factors`, `nonfinite_nystrom_particles` | `False` | `False` | `nan` | `0.0` | `nan / nan` | `nan / nan` |
| `rank=64,epsilon=0.3` | `FAIL` | `nonfinite_log_likelihood`, `nonfinite_nystrom_factors`, `nonfinite_nystrom_particles` | `False` | `False` | `nan` | `0.0` | `nan / nan` | `nan / nan` |
| `rank=32,epsilon=0.5` control | `PASS` | `[]` | `True` | `True` | `59.143653869628906` | `32.0` | `0.018687579780817032 / 1.0013513565063477` | row `9.500980377197266e-05`, column `1.9073486328125e-06` |

The control row also passed paired comparability: max absolute log-likelihood
delta `3.20867919921875`, mean absolute delta `1.72391357421875`.

## Classification

P02 reproduces the two known nonfinite failures under the new diagnostic path
and shows that diagnostics do not break the viable `rank=32,epsilon=0.5`
control.

However, the failing rows end with all aggregate Nystrom summaries as `nan`.
This localizes the failure to the Nystrom factor/core/scaling route but does not
identify the first time step or first stage.  We should not choose a repair
family yet.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Commands | Three trusted GPU launches of `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` with `--nystrom-diagnostics` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` recorded in row artifacts |
| GPU status | Physical GPU1 selected per owner preference; artifacts record GPU1 CUDA visibility and selected GPU metadata |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Shape | `B=5,T=20,N=1024,D=18,M=9` |
| Random seeds | `81920,81921,81922,81923,81924` |
| Dtype/precision | `float32`, TF32 enabled, JIT enabled |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p02-failure-localization-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-stability-repair-p02-failure-localization-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `FAIL` for the two known failing rows; `PASS` for control |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Diagnostic magnitudes and timings |
| Default-readiness | `NO` |
| Next evidence needed | P03 prefix/first-failure diagnostics |

## Post-Run Red Team

Strongest alternative explanation: the aggregate diagnostic reductions are too
late in the computation; once a single time/seed becomes nonfinite, all summary
fields become `nan`, hiding the initiating stage.

What would overturn this interpretation: a per-prefix or per-time diagnostic
showing finite factor/core/scaling values before a later downstream
log-likelihood failure, or showing that the first nonfinite is caused outside
Nystrom.

## Handoff To P03

P03 should run a minimal prefix diagnostic before repair ablations:

- failing `rank=32,epsilon=0.25` at `T=1,2,4,8,12,16,20` until the first failing
  prefix is bracketed;
- failing `rank=64,epsilon=0.3` at the same prefixes if needed;
- control `rank=32,epsilon=0.5` at the smallest failing prefix and at `T=20`.

No tuning or repair should be selected until this sharper first-failure
diagnostic is recorded or a true blocker is written.

