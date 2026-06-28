# Nystrom LEDH/PFPF-OT Effectiveness Leaderboard Pilot

- Status: `PASS`
- Phase: `P02_PAIRED_GPU_PILOT`
- Mode: `paired-gpu`
- Hard vetoes: `[]`
- Paired claim status: `VIABLE_PAIRED_PILOT`
- Ranking status: `NOT_STATISTICALLY_SUPPORTED_SINGLE_PILOT`
- JSON artifact: `docs/benchmarks/scalable-ot-nystrom-ledh-pfpf-effectiveness-leaderboard-p02-pilot-2026-06-22.json`

## Rows

| N | Route | Status | Vetoes | Warm median | Peak memory delta | ESS fraction min | Row residual | Column residual |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1024 | `streaming` | `PASS` | `[]` | `1.2561137701850384` | `75035136` | `0.9999866485595703` | `0.05696451663970947` | `0.0` |
| 1024 | `nystrom` | `PASS` | `[]` | `0.43136452697217464` | `75232000` | `0.9999866485595703` | `8.153915405273438e-05` | `5.960464477539063e-08` |
| 4096 | `streaming` | `PASS` | `[]` | `9.22424711799249` | `75743744` | `0.9999880790710449` | `0.08770555257797241` | `0.0` |
| 4096 | `nystrom` | `PASS` | `[]` | `1.4885019741486758` | `76194048` | `0.9999880790710449` | `3.3855438232421875e-05` | `5.960464477539063e-08` |

## Paired Rows

| N | Comparability | State L2 | Log-likelihood L2 | Memory ratio | Time ratio |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1024 | `PASS` | `0.001142063246528734` | `3.814697265625e-06` | `0.9973832411739685` | `2.911954255955925` |
| 4096 | `PASS` | `0.0018328784170517653` | `1.430511474609375e-05` | `0.9940900370590626` | `6.197000258107247` |

## Inference Status

| Ledger | Status |
| --- | --- |
| `hard_veto_screen` | `PASS` |
| `statistically_supported_ranking` | `NO` |
| `descriptive_only_differences` | `runtime and memory ratios are descriptive in this single pilot` |
| `default_readiness` | `NO` |
| `next_evidence_needed` | `replicated paired ladder with uncertainty analysis before ranking or default claims` |

## Run Manifest

- Git commit: `5ea363e594516be236ca7c78ab2067b28a5b6eb5`
- CUDA_VISIBLE_DEVICES: `1`
- Selected physical GPU: `1`
- GPU selection note: `GPU1 selected by trusted preflight: 18 MiB used and 0 percent utilization; GPU0 had 1253 MiB used and 32 percent utilization`
- TF32 recorded: `True`
- Device scope: `visible`

## Non-Claims

- paired usefulness pilot only
- no speedup claim
- no superiority claim
- no statistical ranking claim
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no production/default route change
- no dense Sinkhorn equivalence claim
