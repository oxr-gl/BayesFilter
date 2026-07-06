# Actual-SIR Nystrom Compiled-Redo P06 Same-Shape Replication Summary

Date: 2026-06-23

Status: `PASS_ADVANCE_TO_P07_LARGER_N`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to P07 larger-N paired ladder | `PASS`: P04 and P05 both passed repaired compiled same-shape gates | No hard vetoes across 10 seeds; combined paired deltas remain under thresholds | Ten seeds support viability but not statistical ranking; timing remains descriptive and spans GPU1/GPU0 | Launch P07 first larger-N paired row at `B=5,T=20,N=2048`, seeds `81320..81324`, GPU1 if available otherwise GPU0 | No default readiness, no superiority, no posterior correctness, no HMC readiness, no dense equivalence |

## Inputs

| Gate | JSON | Seeds | GPU | Status |
| --- | --- | --- | --- | --- |
| P04 serious B5 | `docs/benchmarks/actual-sir-nystrom-compiled-redo-p04-serious-b5-t20-n1024-2026-06-23.json` | `81120..81124` | physical GPU1 | `PASS` |
| P05 disjoint replication | `docs/benchmarks/actual-sir-nystrom-compiled-redo-p05-repl-b5-t20-n1024-2026-06-23.json` | `81220..81224` | physical GPU0 | `PASS` |

## Combined Paired Comparability

| Metric | Value | Gate |
| --- | ---: | ---: |
| Number of seeds | `10` | N/A |
| Combined max abs log-likelihood delta | `7.10369873046875` | `<=10.0` |
| Combined mean abs log-likelihood delta | `2.591357421875` | `<=5.0` |
| Combined signed mean delta | `0.28294677734375` | descriptive |
| Median abs delta | `2.26849365234375` | descriptive |
| Positive deltas | `3` | descriptive |
| Negative deltas | `7` | descriptive |

Per-seed deltas:

| Gate | Seed | Nystrom minus streaming |
| --- | ---: | ---: |
| P04 | `81120` | `3.85498046875` |
| P04 | `81121` | `-3.249755859375` |
| P04 | `81122` | `-0.75054931640625` |
| P04 | `81123` | `-1.19964599609375` |
| P04 | `81124` | `-0.4627685546875` |
| P05 | `81220` | `7.10369873046875` |
| P05 | `81221` | `-1.2872314453125` |
| P05 | `81222` | `3.412841796875` |
| P05 | `81223` | `-1.021484375` |
| P05 | `81224` | `-3.57061767578125` |

## Timing Context

| Gate | Streaming warm median | Nystrom warm median | Ratio | Interpretation |
| --- | ---: | ---: | ---: | --- |
| P04 | `0.10740198497660458s` | `0.05731428205035627s` | `1.8739131178899058` | descriptive only |
| P05 | `0.1679728280287236s` | `0.07246675505302846s` | `2.317929482364808` | descriptive only |

Timing cannot support a ranking here because each row has one repeat, P04 and
P05 used different physical GPUs, and no uncertainty analysis was predeclared.

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS`: P04 and P05 both report `hard_vetoes=[]` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Timing, warm ratios, signed delta pattern, and residual magnitudes below threshold |
| Default-readiness | `NO` |
| Next evidence needed | P07 repaired compiled larger-N paired ladder, starting at `B=5,T=20,N=2048` |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `01213338c7037c468f38b01d013e4ce13526c9e4` |
| Command | Analysis of P04 and P05 JSON artifacts with a local Python summary command |
| Environment | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python`, Python `3.13.13`, TensorFlow version inherited from artifacts as `2.20.0` |
| CPU/GPU status | P04 used physical GPU1; P05 used physical GPU0 after trusted GPU preflight fallback |
| Data/model | Actual-SIR `zhao_cui_spatial_sir_austria_j9_T20`, `D=18,M=9,T=20` |
| Random seeds | `81120,81121,81122,81123,81124,81220,81221,81222,81223,81224` |
| Wall time | N/A for summary-only analysis |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-promotion-or-rejection-runbook-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p06-same-shape-replication-summary-result-2026-06-23.md` |

## Post-Run Red Team

Strongest alternative explanation: the same-shape gates may be too easy for the
candidate, and scale, sensitivity, full-history, transport-policy, or
gradient/HMC gates may still expose a blocker.

What would overturn continuation: a larger-N row that fails paired thresholds,
an artifact mismatch, or a stress/gradient failure that shows the current
fixed-rank candidate cannot serve the intended default path.

## Next Action

Launch P07 first larger-N paired row at `B=5,T=20,N=2048`, seeds
`81320..81324`, after trusted GPU preflight.  Runtime and memory remain
descriptive unless a later uncertainty protocol changes their role.
