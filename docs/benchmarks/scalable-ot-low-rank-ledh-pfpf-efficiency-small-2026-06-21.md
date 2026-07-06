# Low-Rank LEDH/PFPF-OT Efficiency Harness

- Status: `PASS`
- Phase: `LOW_RANK_LEDH_EFFICIENCY_P01`
- Mode: `small`
- Algorithm: `LEDH/PFPF-OT with streaming transport versus P = Q diag(1/g) R^T lazy low-rank resampling`
- Hard vetoes: `[]`
- Paired claim status: `NOT_SUPPORTED_CURRENT_EVIDENCE`
- JSON artifact: `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-small-2026-06-21.json`

## Rows

| N | Route | Status | Vetoes | Warm median | Peak memory delta | ESS fraction min | Invocations |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 32 | `streaming` | `PASS` | `[]` | `2.9665716849267483` | `None` | `0.9999984776848823` | `2` |
| 32 | `low_rank` | `PASS` | `[]` | `0.6626364290714264` | `None` | `0.9999984776848823` | `2` |

## Paired Rows

| N | Comparability | Memory ratio | Speed ratio | Resource screen |
| ---: | --- | ---: | ---: | --- |
| 32 | `PASS` | `None` | `4.47692211713126` | `True` |

## Run Manifest

- Git commit: `43bcb2015127712705d7ac77d3f0c9b01d349733`
- Device scope: `cpu`
- CUDA_VISIBLE_DEVICES: `-1`
- TF32 recorded: `False`
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
