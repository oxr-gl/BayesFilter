# Low-Rank LEDH/PFPF-OT Efficiency Harness

- Status: `PASS`
- Phase: `LOW_RANK_LEDH_EFFICIENCY_P03`
- Mode: `large-n`
- Algorithm: `LEDH/PFPF-OT with streaming transport versus P = Q diag(1/g) R^T lazy low-rank resampling`
- Hard vetoes: `[]`
- Paired claim status: `NOT_EVALUATED_LOW_RANK_ONLY`
- JSON artifact: `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.json`

## Rows

| N | Route | Status | Vetoes | Warm median | Peak memory delta | ESS fraction min | Invocations |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 50000 | `low_rank` | `PASS` | `[]` | `8.957678684964776` | `81125888` | `0.9999864101409912` | `1` |
| 100000 | `low_rank` | `PASS` | `[]` | `19.56813136092387` | `86015744` | `0.9999861717224121` | `1` |

## Paired Rows

| N | Comparability | Memory ratio | Speed ratio | Resource screen |
| ---: | --- | ---: | ---: | --- |

## Executable Envelope Rows

| N | Streaming status | Low-rank status | Support |
| ---: | --- | --- | --- |

## Run Manifest

- Git commit: `43bcb2015127712705d7ac77d3f0c9b01d349733`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `1`
- TF32 recorded: `True`
- Fixture: `ledh_lgssm_efficiency_common_v1`

## Non-Claims

- bounded resource-proxy efficiency harness only
- no posterior correctness claim
- no HMC readiness claim
- no public API readiness claim
- no production/default readiness claim
- no dense Sinkhorn equivalence claim
- no broad scalable-OT selection claim
- no statistical ranking claim
- no streaming superiority claim at unpaired large-N rows
