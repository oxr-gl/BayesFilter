# Actual-SIR Nystrom Compiled Redo P03B While-Loop Compile Repair Result

Date: 2026-06-23

Status: `PASS_COMPILE_LATENCY_REPAIRED`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Accept the `tf.while_loop` compile-latency repair and resume compiled redo testing | `PASS`: same moderate row wrote artifact with `hard_vetoes=[]` | No numerical, residual, GPU, TF32, or paired-threshold vetoes | One-seed moderate row only; no replicated uncertainty or stress/HMC gates | Run the next compiled serious gate from scratch under the repaired implementation | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness |

## Code Repair

- Replaced the Nystrom low-rank Sinkhorn Python loop with `tf.while_loop` and
  true early stop.
- Replaced the compiled redo Nystrom actual-SIR time recursion Python loop with
  `tf.while_loop`.
- Focused tests after repair: `pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py`
  reported `5 passed`.

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p03b-while-loop-compile-repair-plan-2026-06-23.md`
- JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p03b-while-loop-repair-b1-t20-n1024-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p03b-while-loop-repair-b1-t20-n1024-2026-06-23.md`

## Before/After

| Metric | P03 before repair | P03B after repair |
| --- | ---: | ---: |
| Nystrom compile plus first call | `804.5176504359115s` | `12.189794685924426s` |
| Nystrom warm call | `0.09494141908362508s` | `0.02689056284725666s` |
| Streaming compile plus first call | `15.772794160991907s` | `16.429368857992813s` |
| Streaming warm call | `0.062396966852247715s` | `0.06890799989923835s` |
| Wall time | `821.6970312679186s` | `29.781615315005183s` |

## P03B Result Summary

| Field | Value |
| --- | --- |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Shape | `B=1,T=20,N=1024,D=18,M=9` |
| Seed | `81120` |
| GPU | Physical GPU1 |
| TF32 | enabled |
| JIT compile | `True` |
| Paired log-likelihood max abs delta | `2.957275390625` |
| Paired log-likelihood mean abs delta | `2.957275390625` |
| Nystrom max row residual | `9.936094284057617e-05` |
| Nystrom max column residual | `9.5367431640625e-07` |
| Route invocations | `20` |
| Iterations used max | `3` |

## Interpretation

The compile-latency diagnosis was correct: Python-loop unrolling caused the
previous Nystrom compile explosion.  The `tf.while_loop` repair reduced the
moderate-row Nystrom compile plus first call from about `804.5s` to about
`12.2s` while preserving hard-veto and paired-comparability pass status.

The paired log-likelihood delta changed from the pre-repair P03 value
`0.1632080078125` to `2.957275390625`, still within the predeclared threshold.
That change is acceptable for this repair gate but should be tracked in the
next serious row because the Sinkhorn loop now stops through graph control flow.

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` |
| Compile-latency repair | `PASS` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Warm timings and deltas are descriptive only |
| Default-readiness | `NO` |
| Next evidence needed | Repaired compiled serious row with replicated seeds or a staged one-seed `B=5,T=20,N=1024` gate |

