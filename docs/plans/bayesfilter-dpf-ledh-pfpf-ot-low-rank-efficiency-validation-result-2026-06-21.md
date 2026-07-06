# Low-Rank LEDH/PFPF-OT TF32 Efficiency Validation Result

Timestamp: 2026-06-21T05:39:56+08:00

Status: `LOW_RANK_LEDH_EFFICIENCY_SUPPORTED_BOUNDED`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Low-rank route helps LEDH/PFPF-OT TF32 in the governed benchmark under a bounded resource-proxy efficiency claim. |
| Primary criterion status | Passed by speed screen on adjacent feasible paired rows `N=2048`, `4096`, `8192`, and `16384` after validity, TF32, same-GPU, and output-comparability gates. |
| Veto diagnostic status | No hard vetoes in P02 aggregate; P02 `N=32768` streaming timeout is direct route-fired sidecar evidence; P03 large-N low-rank rows passed validity/nonmaterialization checks. |
| Main uncertainty | One-seed/synthetic benchmark evidence only; timing values are descriptive except for the predeclared paired speed screen. |
| Next justified action | Consider engineering integration or broader validation only under a new plan with real target workloads and explicit posterior/default-readiness gates. |
| Not concluded | No posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, memory improvement, or statistical ranking. |

## Evidence Summary

P02 paired GPU screen:

- Artifact:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.json`
- Status: `PASS`
- GPU: GPU1 selected via `CUDA_VISIBLE_DEVICES=1`; one visible physical GPU in
  manifest.
- TF32: recorded `True`.
- Bounded output-comparability: `PASS` for paired rows through `N=16384`.
- Speed screen: passed at adjacent feasible rows `N=2048`, `4096`, `8192`,
  and `16384`.
- Memory screen: did not pass; no memory-improvement claim is supported.
- Boundary: streaming `TIMEOUT` at `N=32768` under fixed `900s` row timeout,
  with route-fired timeout sidecar
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21-row-streaming-n32768.json`;
  low-rank passed the same `N=32768` row.

P03 large-N low-rank executable-envelope screen:

- Artifact:
  `docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.json`
- Status: `PASS`
- GPU: GPU1 selected via `CUDA_VISIBLE_DEVICES=1`; one visible physical GPU in
  manifest.
- TF32: recorded `True`.
- Rows:

| N | Status | Warm median seconds | Peak memory delta bytes | ESS fraction min | Factor residual | Claim role |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 50000 | `PASS` | 8.957678684964776 | 81125888 | 0.9999864101409912 | 1.4901161193847656e-08 | low-rank-only envelope |
| 100000 | `PASS` | 19.56813136092387 | 86015744 | 0.9999861717224121 | 1.4901161193847656e-08 | low-rank-only envelope |

## Interpretation

The low-rank solver route helps the LEDH/PFPF-OT TF32 benchmark in the bounded
sense the program was designed to test:

- it passed the paired speed-screen after output-comparability gates at
  feasible paired sizes;
- streaming reached the fixed timeout boundary at `N=32768` while low-rank
  passed that same row;
- low-rank also completed low-rank-only large-N rows at `N=50000` and
  `N=100000` without materializing a dense transport matrix.

The large-N rows are executable-envelope evidence only.  They do not prove
that low-rank is faster than streaming at `N=50000` or `N=100000`, because
streaming was not paired at those sizes after the predeclared `N=32768`
timeout boundary.

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for claimed rows; no hard vetoes in P02/P03 aggregates. |
| Statistically supported ranking | Not supported; no uncertainty analysis or multi-seed ranking evidence. |
| Descriptive-only differences | Runtime and memory values are descriptive outside the predeclared paired speed screen. |
| Default-readiness | Not supported. |
| Next evidence needed | Real target workloads, multi-seed/replicated timing if ranking is needed, posterior-quality checks, and explicit default/API/HMC gates under a separate plan. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `43bcb2015127712705d7ac77d3f0c9b01d349733` |
| Environment | TensorFlow `2.20.0`, TensorFlow Probability `0.25.0`, Python `3.13.13` |
| GPU status | GPU1 selected; P02/P03 manifests show one visible physical GPU under `CUDA_VISIBLE_DEVICES=1`. |
| Seeds | Harness seed `20260621` |
| P02 command | `timeout 7200 python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode paired-gpu --cuda-visible-devices 1 --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-paired-gpu-2026-06-21.md --quiet` plus targeted `N=32768` timeout repair and trusted aggregate refresh recorded in P02 result. |
| P03 command | `timeout 3000 python docs/benchmarks/scalable_ot_low_rank_ledh_pfpf_efficiency.py --mode large-n --cuda-visible-devices 1 --output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.json --markdown-output docs/benchmarks/scalable-ot-low-rank-ledh-pfpf-efficiency-large-n-2026-06-21.md --quiet` |
| Plan file | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-master-program-2026-06-21.md` |

## Claude Review

- Master plan review round 2: `VERDICT: AGREE`.
- P02 result repair review round 2: `VERDICT: AGREE`.
- P04 final closeout review: `VERDICT: AGREE`.

## Non-Claims

This result does not establish posterior correctness, HMC readiness, public API
readiness, production/default readiness, dense Sinkhorn equivalence, broad
scalable-OT selection, memory improvement, statistically supported ranking, or
streaming superiority at unpaired `N=50000/100000` rows.
