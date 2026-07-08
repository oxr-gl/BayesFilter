# Actual-SIR Nystrom Default-Promotion P05A Seed Replication Result

Date: 2026-06-22

Status: `PASS_ADVANCE_TO_STAGE_B`

## Question

Does the Nystrom route replicate the P03 actual-SIR `N=1024` pass on a second
five-seed batch?

## Artifacts

- Subplan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-p05-replicated-ladder-subplan-2026-06-22.md`
- JSON: `docs/benchmarks/actual-sir-nystrom-default-promotion-p05a-seed-repl-b5-t20-n1024-2026-06-22.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-default-promotion-p05a-seed-repl-b5-t20-n1024-2026-06-22.md`

## Result

| Field | Value |
| --- | --- |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Shape | `B=5,T=20,N=1024,D=18,M=9` |
| Seeds | `81220,81221,81222,81223,81224` |
| GPU | Physical GPU1, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| TF32 recorded | `True` |
| Wall time | `701.3043887231033` seconds |

## Route Summary

| Route | Status | Warm median seconds | ESS fraction min | Final logsumexp residual | Row residual | Column residual |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `streaming` | `PASS` | `313.9717076071538` | `0.6537096500396729` | `0.0` | `5.942583084106445e-05` | `0.0` |
| `nystrom` | `PASS` | `34.23629658506252` | `0.6537096500396729` | `0.0` | `9.357929229736328e-05` | `2.384185791015625e-07` |

## Paired Comparability

| Metric | Value | Threshold |
| --- | ---: | ---: |
| Log-likelihood max absolute delta | `3.45458984375` | `<= 10.0` |
| Log-likelihood mean absolute delta | `2.49368896484375` | `<= 5.0` |
| Filtered mean relative L2 | `0.00097213458885444` | `<= 0.20` unless RMS passes |
| Filtered mean RMS | `0.16561167869890225` | `<= 2.5` unless relative L2 passes |
| Filtered variance relative L2 | `0.014587687775281098` | `<= 0.75` unless RMS passes |
| Filtered variance RMS | `0.018617196951760853` | `<= 25.0` unless relative L2 passes |
| Final particle mean relative L2 | `0.0030060412977140514` | `<= 0.20` unless absolute L2 passes |
| Final particle mean absolute L2 | `0.8133871677233709` | `<= 25.0` unless relative L2 passes |
| Warm median streaming/Nystrom | `9.170726361336095` | descriptive only |

## Interpretation

Stage A replicated the `N=1024` serious actual-SIR pass on a second seed batch.
This strengthens the viability case, but still does not establish statistical
ranking or default readiness.  The next gated row is Stage B at `N=2048`.

## Decision

Advance to P05B if trusted GPU preflight selects a usable GPU.  Keep runtime as
descriptive and preserve all default-readiness nonclaims.
