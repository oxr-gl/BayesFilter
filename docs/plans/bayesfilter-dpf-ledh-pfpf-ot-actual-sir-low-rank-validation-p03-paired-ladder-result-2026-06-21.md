# P03 Paired Actual-SIR Ladder Result

Date: 2026-06-21

Status: `TUNING_REQUIRED`

## Phase Objective

Run paired same-seed actual-SIR d18 streaming versus low-rank rows on feasible
particle counts to test validity, bounded comparability, and practical
resource evidence before any large-N envelope runs.

## Entry Conditions

- P02 tiny actual-SIR route smoke passed.
- Trusted GPU context was available.
- GPU1 was preferred and available.
- The P03 evidence contract required same physical GPU UUID, TF32 enabled,
  `warmups=1`, `repeats=3`, compiled streaming timing, paired comparability
  gates, and warm median `streaming / low_rank >= 1.25` on at least two
  adjacent paired rows for bounded efficiency support.

## Artifacts

| Artifact | Path |
| --- | --- |
| P03 aggregate JSON | `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21.json` |
| P03 aggregate Markdown | `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21.md` |
| Attempted row JSON | `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.json` |
| Attempted row Markdown | `docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.md` |
| Refreshed P04 blocked subplan | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p04-large-n-envelope-subplan-2026-06-21.md` |
| P04 blocked result | `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-validation-p04-large-n-envelope-result-2026-06-21.md` |

## Commands And Checks Run

Trusted GPU precheck:

```bash
nvidia-smi --query-gpu=index,uuid,name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits
```

P03 paired row:

```bash
timeout 3600 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py --route both --streaming-timing-source compiled_core --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 1024 --transport-policy active-all --warmups 1 --repeats 3 --dtype float32 --device-scope visible --cuda-visible-devices 1 --device /GPU:0 --expect-device-kind gpu --tf32-mode enabled --phase-id ACTUAL-SIR-LR-P03-GPU1-PAIRED-B5-T20-N1024 --output docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.json --markdown-output docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.md
```

Focused result checks:

```bash
python -c "import json; d=json.load(open('docs/benchmarks/actual-sir-low-rank-route-validation-paired-gpu-2026-06-21-row-b5-t20-n1024.json')); print(d['status'], d['hard_vetoes'], d['paired_comparability']['warm_median_streaming_over_low_rank'])"
```

Post-run GPU status was checked with trusted `nvidia-smi`.

## Evidence Summary

| Field | Value |
| --- | --- |
| Attempted row | `B=5,T=20,N=1024`, seeds `81120,81121,81122,81123,81124` |
| Row status | `PASS` at the harness hard-veto level |
| Physical GPU | GPU1, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| TF32 | enabled and recorded true |
| Actual-SIR semantics | `PASS` |
| Hard vetoes | `[]` |
| Streaming warm median | `0.9723010780289769` seconds |
| Low-rank warm median | `58.549089503940195` seconds |
| Warm median ratio | `0.016606596042173186` |
| Low-rank factor residual | `8.986273314803839e-06` |
| Low-rank projection iterations max | `240.0` |
| Row wall time | `633.6386418200564` seconds |

## Gate Assessment

| Gate | Status |
| --- | --- |
| Finite outputs | `PASS` |
| Actual-SIR semantics | `PASS` |
| Route-fired evidence | `PASS`; both routes invoked on all 20 active resampling steps |
| Low-rank nonmaterialization | `PASS`; sentinel transport shape, no dense matrix materialization |
| Low-rank factor diagnostics | `PASS`; finite/nonnegative factors and positive `g` |
| GPU/TF32 provenance | `PASS`; same physical GPU UUID recorded |
| Paired log-likelihood agreement | `FAIL`; max absolute delta `58.0933837890625` and mean absolute delta `42.93328857421875` exceed thresholds `10.0` and `5.0` |
| Paired filtered-mean agreement | Passes by relative L2 `0.024529629672863727 <= 0.20`; RMS `4.1791288726681` exceeds `2.5` but the gate is an OR gate |
| Paired filtered-variance agreement | Passes by RMS `4.421087662174504 <= 25.0`; relative L2 `3.460364375696834` exceeds `0.75` but the gate is an OR gate |
| Paired final-particle mean agreement | Passes by both alternatives |
| Warm-time promotion screen | `FAIL`; ratio `0.016606596042173186` is below required `1.25` |
| Adjacent support rows | `FAIL`; zero rows passed all support gates |

## Decision Table

| Field | Status |
| --- | --- |
| Decision | `TUNING_REQUIRED` for the current low-rank route configuration on actual-SIR d18. |
| Primary criterion status | Failed at the first required paired row; no adjacent support rows exist. |
| Veto diagnostic status | Hard validity did not veto the route, but paired comparability and speed promotion gates failed. |
| Main uncertainty | This is one row and one configured route; it rejects promotion of the current configured candidate, not all possible low-rank route repairs. |
| Next justified action | Stop this validation program before P04. A new tuning/repair plan would need to adjust the low-rank route/configuration and rerun P02/P03 gates. |
| What is not concluded | No speedup, no large-N actual-SIR envelope support, no posterior correctness, no default/API/HMC readiness, no dense Sinkhorn equivalence, no broad scalable-OT selection, and no statistical ranking. |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the attempted row. |
| Paired comparability | Failed due to log-likelihood deltas. |
| Statistically supported ranking | Not supported. |
| Descriptive-only differences | Runtime and memory values are descriptive except for the predeclared P03 warm-time screen, which failed. |
| Default-readiness | Not supported. |
| Next evidence needed | A reviewed tuning/repair subplan with predeclared parameters and the same actual-SIR paired gates. |

## Stop And Handoff

P03 stops after the first required paired row. Running larger P03 rows would
not repair the failed paired support basis. Running P04 low-rank-only rows
would produce executable-envelope diagnostics only; the master contract allowed
that language only after P03 established a valid continuation basis. P04 is
therefore refreshed as blocked by `P03_TUNING_REQUIRED`. This follows the
pre-execution P03 subplan handoff rule: advance to P04 only after a valid
paired basis, and stop as `TUNING_REQUIRED` if low-rank runs but paired
comparability or practical resource evidence fails.

## Nonclaims

- No speedup claim.
- No large-N actual-SIR executable-envelope claim for this lane.
- No posterior correctness claim.
- No HMC readiness claim.
- No public API readiness claim.
- No production/default readiness claim.
- No dense Sinkhorn equivalence claim.
- No broad scalable-OT selection claim.
- No statistical ranking claim.
