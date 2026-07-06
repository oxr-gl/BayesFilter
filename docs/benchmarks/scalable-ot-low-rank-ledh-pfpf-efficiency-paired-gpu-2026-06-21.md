# Low-Rank LEDH/PFPF-OT Efficiency Harness

- Status: `PASS`
- Phase: `LOW_RANK_LEDH_EFFICIENCY_P02`
- Mode: `paired-gpu`
- Algorithm: `LEDH/PFPF-OT with streaming transport versus P = Q diag(1/g) R^T lazy low-rank resampling`
- Hard vetoes: `[]`
- Paired claim status: `SUPPORTED_BOUNDED`
- JSON artifact: `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.json`

## Rows

| N | Route | Status | Vetoes | Warm median | Peak memory delta | ESS fraction min | Invocations |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 1024 | `streaming` | `PASS` | `[]` | `1.3083033449947834` | `75035136` | `0.9999872446060181` | `2` |
| 1024 | `low_rank` | `PASS` | `[]` | `1.9422224329318851` | `75281920` | `0.9999872446060181` | `2` |
| 2048 | `streaming` | `PASS` | `[]` | `3.1174110020510852` | `75293440` | `0.9999878406524658` | `2` |
| 2048 | `low_rank` | `PASS` | `[]` | `2.177177645964548` | `75748352` | `0.9999878406524658` | `2` |
| 4096 | `streaming` | `PASS` | `[]` | `9.249396051978692` | `75782144` | `0.9999872446060181` | `2` |
| 4096 | `low_rank` | `PASS` | `[]` | `3.4667823128402233` | `76363520` | `0.9999872446060181` | `2` |
| 8192 | `streaming` | `PASS` | `[]` | `31.58525244309567` | `76503296` | `0.9999867677688599` | `2` |
| 8192 | `low_rank` | `PASS` | `[]` | `8.713284426135942` | `78007296` | `0.9999867677688599` | `2` |
| 16384 | `streaming` | `PASS` | `[]` | `114.00965318712406` | `78802688` | `0.9999878406524658` | `2` |
| 16384 | `low_rank` | `PASS` | `[]` | `8.214295451063663` | `80591104` | `0.9999878406524658` | `2` |
| 32768 | `streaming` | `TIMEOUT` | `['row_timeout']` | `None` | `None` | `None` | `None` |
| 32768 | `low_rank` | `PASS` | `[]` | `13.422581671969965` | `86369536` | `0.9999878406524658` | `2` |
| 50000 | `streaming` | `SKIPPED` | `[]` | `None` | `None` | `None` | `None` |
| 50000 | `low_rank` | `PASS` | `[]` | `19.07510154112242` | `92630528` | `0.9999864101409912` | `2` |
| 100000 | `streaming` | `SKIPPED` | `[]` | `None` | `None` | `None` | `None` |
| 100000 | `low_rank` | `PASS` | `[]` | `39.08503817790188` | `109548032` | `0.9999861717224121` | `2` |

## Paired Rows

| N | Comparability | Memory ratio | Speed ratio | Resource screen |
| ---: | --- | ---: | ---: | --- |
| 1024 | `PASS` | `0.9967218689427687` | `0.6736114889888446` | `False` |
| 2048 | `PASS` | `0.9939944304002812` | `1.431858814015146` | `True` |
| 4096 | `PASS` | `0.9923867312559714` | `2.6680060117189646` | `True` |
| 8192 | `PASS` | `0.9807197521626695` | `3.6249536797346003` | `True` |
| 16384 | `PASS` | `0.9778087665854533` | `13.87941958824491` | `True` |
| 32768 | `NOT_EVALUATED` | `None` | `None` | `False` |

## Executable Envelope Rows

| N | Streaming status | Low-rank status | Support |
| ---: | --- | --- | --- |
| 32768 | `TIMEOUT` | `PASS` | `executable_envelope_for_that_row_only` |

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
