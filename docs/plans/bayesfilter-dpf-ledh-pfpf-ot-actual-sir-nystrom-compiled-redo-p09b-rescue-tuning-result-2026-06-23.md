# Actual-SIR Nystrom Compiled-Redo P09B Rescue Tuning Result

Date: 2026-06-23

Status: `EPSILON_FLOOR_RESCUE_IDENTIFIED`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Treat the P09 nonfinite failure as an epsilon-floor/tuning-stability problem and exclude `epsilon=0.25` from the supported policy unless separately repaired | `PASS_DIAGNOSTIC`: failure reproduced at `epsilon=0.25`; `epsilon=0.3` and `0.375` rescued the row | Nonfinite vetoes persist for `epsilon=0.25` across rank, jitter, denominator floor, and smaller N; no vetoes for `epsilon=0.3/0.375` | One seed batch and one actual-SIR shape; safe floor needs confirmation under stress/history/gradient gates | Narrow the supported Nystrom policy to `epsilon>=0.3` for this route and run a policy-confirmation gate before P10 | No default readiness, no statistical ranking, no superiority claim, no posterior correctness, no HMC readiness |

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09b-rescue-tuning-plan-2026-06-23.md`
- Summary JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09b-rescue-summary-2026-06-23.json`
- Row JSON/Markdown artifacts: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p09b-*.json` and `.md`

## Diagnostic Summary

| Row | N | Rank | Epsilon | Jitter | Floor | Classification | Max delta | Mean delta |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| reproduce | `1024` | `32` | `0.25` | `1e-8` | `1e-30` | `FAIL_NUMERIC` | `nan` | `nan` |
| rank64 | `1024` | `64` | `0.25` | `1e-8` | `1e-30` | `FAIL_NUMERIC` | `nan` | `nan` |
| rank128 | `1024` | `128` | `0.25` | `1e-8` | `1e-30` | `FAIL_NUMERIC` | `nan` | `nan` |
| eps0p3 | `1024` | `32` | `0.3` | `1e-8` | `1e-30` | `PASS_RESCUE` | `1.51568603515625` | `0.731591796875` |
| eps0p375 | `1024` | `32` | `0.375` | `1e-8` | `1e-30` | `PASS_RESCUE` | `2.39056396484375` | `1.42574462890625` |
| jitter1e-7 | `1024` | `32` | `0.25` | `1e-7` | `1e-30` | `FAIL_NUMERIC` | `nan` | `nan` |
| jitter1e-6 | `1024` | `32` | `0.25` | `1e-6` | `1e-30` | `FAIL_NUMERIC` | `nan` | `nan` |
| jitter1e-5 | `1024` | `32` | `0.25` | `1e-5` | `1e-30` | `FAIL_NUMERIC` | `nan` | `nan` |
| floor1e-24 | `1024` | `32` | `0.25` | `1e-8` | `1e-24` | `FAIL_NUMERIC` | `nan` | `nan` |
| floor1e-18 | `1024` | `32` | `0.25` | `1e-8` | `1e-18` | `FAIL_NUMERIC` | `nan` | `nan` |
| floor1e-12 | `1024` | `32` | `0.25` | `1e-8` | `1e-12` | `FAIL_NUMERIC` | `nan` | `nan` |
| smalln256 | `256` | `32` | `0.25` | `1e-8` | `1e-30` | `FAIL_NUMERIC` | `nan` | `nan` |
| smalln512 | `512` | `32` | `0.25` | `1e-8` | `1e-30` | `FAIL_NUMERIC` | `nan` | `nan` |

All `epsilon=0.25` rows failed with:

- `nystrom:nonfinite_log_likelihood`
- `nystrom:nonfinite_nystrom_factors`
- `nystrom:nonfinite_nystrom_particles`

The failure persisted after increasing rank to `64` and `128`, increasing
Cholesky jitter to `1e-5`, increasing denominator floor to `1e-12`, and reducing
particle count to `N=256` and `N=512`.

Both epsilon-boundary rescue rows passed:

- `rank=32,epsilon=0.3`: max delta `1.51568603515625`, mean delta `0.731591796875`
- `rank=32,epsilon=0.375`: max delta `2.39056396484375`, mean delta `1.42574462890625`

## Classification

This is a tuning/policy problem with a sharp unsafe epsilon floor, not evidence
that the compiled Nystrom route is broadly unusable.

Evidence for tuning/policy classification:

- failure reproduces deterministically for the same row;
- failure is tied to `epsilon=0.25`;
- rank, jitter, denominator floor, and smaller N do not rescue `epsilon=0.25`;
- raising epsilon to `0.3` or `0.375` rescues finite execution and paired
  comparability on the same seeds.

This supports excluding `epsilon=0.25` from the admissible policy for this
route unless a separate numerical implementation repair is made.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | Sequential P09B rescue wrapper launching `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py` |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow `2.20.0` |
| GPU status | Trusted preflight selected physical GPU1 |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Random seeds | `81920,81921,81922,81923,81924` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09b-rescue-tuning-plan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p09b-rescue-tuning-result-2026-06-23.md` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `FAIL` for `epsilon=0.25`; `PASS` for rescue rows `epsilon=0.3` and `0.375` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Runtime, warm ratios, and relative deltas across rescue rows |
| Default-readiness | `NO` |
| Next evidence needed | Policy-confirmation gate for `epsilon>=0.3`/default `epsilon=0.5`, then P10 stress |

## Post-Run Red Team

Strongest alternative explanation: the rescue may be specific to the tested seed
batch and actual-SIR shape.  Stress policies, full-history mode, and gradient
use may still fail.

What would overturn the tuning interpretation: `epsilon=0.3` or `0.5` failing
under the next policy-confirmation gate, stress/history gate, or gradient/HMC
mechanics gate.

## Next Action

Write and run a policy-confirmation gate that treats `epsilon=0.25` as excluded
and tests the intended policy neighborhood, for example:

- `rank=32,epsilon=0.3`
- `rank=32,epsilon=0.5`
- `rank=64,epsilon=0.3`
- `rank=64,epsilon=0.5`

If that gate passes, continue to P10 transport-policy and history stress.
