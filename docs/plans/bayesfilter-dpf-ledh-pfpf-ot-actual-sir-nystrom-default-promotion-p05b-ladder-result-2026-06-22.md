# Actual-SIR Nystrom Default-Promotion P05B Ladder Result

Date: 2026-06-22

Status: `PASS_N2048_LADDER_ROW_RUNTIME_PATH_CONTAMINATED`

## Question

Does fixed-rank Nystrom keep passing actual-SIR d18 validity and paired
comparability when the serious row increases from `N=1024` to `N=2048`?

## Artifacts

- Subplan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-p05-replicated-ladder-subplan-2026-06-22.md`
- JSON: `docs/benchmarks/actual-sir-nystrom-default-promotion-p05b-ladder-b5-t20-n2048-2026-06-22.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-default-promotion-p05b-ladder-b5-t20-n2048-2026-06-22.md`

## Result

| Field | Value |
| --- | --- |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Shape | `B=5,T=20,N=2048,D=18,M=9` |
| Seeds | `81120,81121,81122,81123,81124` |
| GPU | Physical GPU1, UUID `GPU-a1ea1946-07c0-8ed5-2ba1-d96f82c89cd3` |
| TF32 recorded | `True` |
| Wall time | `2467.37197579816` seconds |

## Route Summary

| Route | Status | Warm median seconds | First call seconds | ESS fraction min | Final logsumexp residual | Row residual | Column residual |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `streaming` | `PASS` | `1160.5996048829984` | `1167.2142036410514` | `0.6740890145301819` | `0.0` | `4.89354133605957e-05` | `0.0` |
| `nystrom` | `PASS` | `69.52919894712977` | `70.01642461912706` | `0.6740890145301819` | `0.0` | `9.989738464355469e-05` | `4.76837158203125e-07` |

## Paired Comparability

| Metric | Value | Threshold |
| --- | ---: | ---: |
| Log-likelihood max absolute delta | `0.9002685546875` | `<= 10.0` |
| Log-likelihood mean absolute delta | `0.40667724609375` | `<= 5.0` |
| Filtered mean relative L2 | `0.0011970244179186358` | `<= 0.20` unless RMS passes |
| Filtered mean RMS | `0.2039326373277483` | `<= 2.5` unless relative L2 passes |
| Filtered variance relative L2 | `0.014085109685267421` | `<= 0.75` unless RMS passes |
| Filtered variance RMS | `0.017965052746096815` | `<= 25.0` unless relative L2 passes |
| Final particle mean relative L2 | `0.003222995768064684` | `<= 0.20` unless absolute L2 passes |
| Final particle mean absolute L2 | `0.8719963584758291` | `<= 25.0` unless relative L2 passes |
| Warm median streaming/Nystrom | `16.692261991476734` | descriptive only |

## Interpretation

The `N=2048` actual-SIR ladder row passed with no hard vetoes and strong paired
comparability.  This extends the P03/P05A evidence from replicated `N=1024`
validity to a larger particle count.

Runtime evidence from this row is not a fair speed comparison.  A follow-up
compiled streaming sanity diagnostic on the same physical GPU1,
`docs/benchmarks/actual-sir-streaming-compiled-sanity-b5-t20-n2048-gpu1-2026-06-22.json`,
ran the production-style compiled actual-SIR streaming path at
`B=5,T=20,N=2048` with TF32 enabled in `20.397380776004866` seconds for
compile plus first call and `0.29988364898599684` seconds for the measured warm
call.  The P05B paired harness instead ran a Python-level per-step route loop
with `row_chunk_size=128`, `col_chunk_size=128`, and `particle_chunk_size=64`,
so the `1160.60s` streaming warm call and `16.69x` streaming/Nystrom ratio are
contaminated by harness/runtime-path differences.  The validity and paired
comparability pass still stand; the speed ratio should be withdrawn pending a
compiled or otherwise comparable Nystrom-vs-streaming benchmark.

## Stage C Decision

Do not launch same-protocol paired `N=4096`.  First repair the runtime protocol:
either compile the Nystrom route comparably, or restrict high-N work to
Nystrom-only feasibility while clearly marking it as envelope evidence.  The
same-protocol Python-loop paired row is not useful for speed promotion.
