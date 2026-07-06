# P02 Feasible-N Paired GPU Efficiency Screen Result

Timestamp: 2026-06-21T05:05:14+08:00

Status: `P02_PASSED_BOUNDED_RESOURCE_PROXY_AND_ENVELOPE_AFTER_TIMEOUT_REPAIR`

## Objective

Run trusted GPU1 paired rows for the streaming and low-rank LEDH/PFPF-OT TF32
routes over the predeclared upward ladder, enforcing fixed row timeouts and
evaluating validity, TF32, same-GPU, bounded output-comparability, and
resource-proxy screens before any efficiency interpretation.

## Artifacts

- Paired GPU JSON:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.json`
- Paired GPU Markdown:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.md`
- Row artifacts:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21-row-*.json`
  and matching Markdown files.

## Command And Environment

Official row run:

`timeout 7200 python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode paired-gpu --cuda-visible-devices 1 --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.md --quiet`

Aggregate refresh after classification repair:

`python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode paired-gpu --cuda-visible-devices 1 --reuse-existing-row-artifacts --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.md --quiet`

Targeted timeout-evidence repair after Claude review:

`timeout 1200 python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode paired-gpu --routes streaming --particle-counts 32768 --cuda-visible-devices 1 --row-timeout-seconds 900 --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.md --quiet`

Trusted aggregate refresh after timeout-evidence repair:

`timeout 300 python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode paired-gpu --cuda-visible-devices 1 --reuse-existing-row-artifacts --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.md --quiet`

Environment:

- `CUDA_VISIBLE_DEVICES=1`
- TF32 recorded: `True`
- Device scope: `visible`
- Row subprocess timeouts: `True`
- P02 row timeout: `900s`

## Local Checks

Passed after timeout-enforcement repair:

- `python -m py_compile docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_pfpf_efficiency.py -q`
- Tiny timeout smoke confirmed child-row timeout status can be recorded.
- JSON inspection confirmed P02 aggregate `status: PASS`, no hard vetoes, TF32
  recorded true, `CUDA_VISIBLE_DEVICES: 1`, and row subprocess timeouts enabled.
- After Claude flagged reconstructed timeout evidence, the harness was patched
  to write a parent-enforced timeout sidecar for timed-out child rows.
- Focused repair checks passed:
  `python -m py_compile docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py`
  and
  `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_low_rank_ledh_pfpf_efficiency.py -q`.
- The repaired `N=32768` streaming sidecar exists at
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21-row-streaming-n32768.json`
  with `artifact_role: parent_enforced_row_timeout_sidecar`,
  `status: TIMEOUT`, and `timeout_status: timeout_enforced`.
- The repaired P02 aggregate was refreshed in trusted GPU context and records
  one visible physical GPU, one logical GPU, `CUDA_VISIBLE_DEVICES: 1`, and
  `tf32_execution_recorded: true`.

## Evidence Summary

Paired rows with bounded output-comparability `PASS`:

| N | Streaming median seconds | Low-rank median seconds | Speed ratio streaming/low-rank | Memory ratio streaming/low-rank | Resource screen |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1024 | 1.3083033449947834 | 1.9422224329318851 | 0.6736114889888446 | 0.9967218689427687 | false |
| 2048 | 3.1174110020510852 | 2.177177645964548 | 1.431858814015146 | 0.9939944304002812 | true |
| 4096 | 9.249396051978692 | 3.4667823128402233 | 2.6680060117189646 | 0.9923867312559714 | true |
| 8192 | 31.58525244309567 | 8.713284426135942 | 3.6249536797346003 | 0.9807197521626695 | true |
| 16384 | 114.00965318712406 | 8.214295451063663 | 13.87941958824491 | 0.9778087665854533 | true |

Boundary row:

- `N=32768`: streaming `TIMEOUT` under the fixed `900s` row timeout with a
  route-fired parent-enforced timeout sidecar; low-rank `PASS` with median
  `13.422581671969965s`.

Low-rank-only rows after the streaming boundary:

- `N=50000`: low-rank `PASS`, median `19.07510154112242s`.
- `N=100000`: low-rank `PASS`, median `39.08503817790188s`.

## Decision

P02 supports a bounded resource-proxy efficiency claim under the reviewed
contract:

- adjacent paired rows `N=2048`, `4096`, `8192`, and `16384` pass the
  predeclared speed screen after comparability gates;
- memory screen does not pass and should not be claimed;
- the `N=32768` streaming timeout plus low-rank pass supports executable
  envelope evidence for that row only.

## Non-Claims

This does not establish posterior correctness, HMC readiness, public API
readiness, production/default readiness, dense Sinkhorn equivalence, broad
scalable-OT selection, statistical ranking, memory improvement, or streaming
superiority at unpaired 50k/100k rows.

## Next Subplan Review

P03 may start.  P03 should treat `N=50000` and `N=100000` as already observed
low-rank rows in the P02 artifact and may either reuse/confirm them under the
P03 result contract or write a close record that incorporates the P02
low-rank-only large-N rows without making unpaired speed claims.
