# Actual-SIR Nystrom Compiled-Redo P09 Rank/Epsilon Sensitivity Partial Result

Date: 2026-06-23

Status: `STOPPED_ON_SENSITIVITY_VETO`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Stop the automatic P09 grid and classify sensitivity failure | `FAIL` for the full predeclared grid: row `rank=16,epsilon=1.0` failed paired log-likelihood thresholds | Hard vetoes fired only through paired comparability: `paired_log_likelihood_max_abs_delta`, `paired_log_likelihood_mean_abs_delta` | The failure may indicate only that low rank plus high epsilon is too weak; it does not invalidate the default `rank=32,epsilon=0.5` candidate | Plan a narrowed policy/sensitivity repair: exclude or retest weak settings, then evaluate the default-neighborhood grid before P10 | No default promotion, no Nystrom rejection, no statistical ranking, no superiority, no posterior correctness, no HMC readiness |

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09-rank-epsilon-sensitivity-plan-2026-06-23.md`
- Passing row JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09-sensitivity-r16-eps0p25-2026-06-23.json`
- Passing row JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09-sensitivity-r16-eps0p5-2026-06-23.json`
- Failing row JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09-sensitivity-r16-eps1p0-2026-06-23.json`

## Row Outcomes

| Row | Status | Hard vetoes | Max abs delta | Mean abs delta | Threshold status |
| --- | --- | --- | ---: | ---: | --- |
| `rank=16,epsilon=0.25` | `PASS` | `[]` | `1.90203857421875` | `0.67137451171875` | Passed |
| `rank=16,epsilon=0.5` | `PASS` | `[]` | `2.66204833984375` | `1.0049560546875` | Passed |
| `rank=16,epsilon=1.0` | `FAIL` | `['paired:paired_log_likelihood_max_abs_delta', 'paired:paired_log_likelihood_mean_abs_delta']` | `10.30291748046875` | `5.30792236328125` | Failed |

Per-seed deltas for the failing row:

| Seed | Nystrom minus streaming |
| ---: | ---: |
| `81920` | `-7.38519287109375` |
| `81921` | `1.04803466796875` |
| `81922` | `4.041259765625` |
| `81923` | `-10.30291748046875` |
| `81924` | `3.76220703125` |

## Failure Classification

This is a valid sensitivity veto, not a GPU/environment blocker:

- the row wrote JSON and Markdown artifacts;
- both streaming and Nystrom routes individually reported `PASS`;
- Nystrom residuals were within threshold;
- GPU/TF32/JIT evidence was present;
- aggregate failure came only from paired log-likelihood thresholds.

The result weakens any claim that the route is robust across the full
predeclared `rank x epsilon` grid.  It does not reject the repaired compiled
Nystrom route or the default candidate `rank=32,epsilon=0.5`, which has passed
prior gates.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | Sequential P09 grid wrapper launching `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` rows under the P09 plan |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU status | Trusted preflight selected physical GPU1; row artifacts record GPU1 |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Random seeds | `81920,81921,81922,81923,81924` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09-rank-epsilon-sensitivity-plan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09-rank-epsilon-sensitivity-partial-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `FAIL` for full-grid robustness because paired comparability vetoes fired at `rank=16,epsilon=1.0` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Timing and warm ratios are descriptive |
| Default-readiness | `NO` |
| Next evidence needed | A reviewed narrowed sensitivity repair plan before continuing to P10 |

## Post-Run Red Team

Strongest alternative explanation: `rank=16,epsilon=1.0` is simply outside the
reasonable default-neighborhood policy, while `rank=32,epsilon=0.5` and nearby
settings may still be stable.

What would overturn continued viability: a narrowed default-neighborhood grid
around `rank=32,epsilon=0.5` fails paired thresholds or shows instability near
the intended default setting.

## Next Action

Do not continue automatically to P10 yet.  First write and launch a narrowed P09
repair/sensitivity continuation that tests the default neighborhood and
classifies `rank=16,epsilon=1.0` as either excluded weak setting or evidence of
unacceptable brittleness.
