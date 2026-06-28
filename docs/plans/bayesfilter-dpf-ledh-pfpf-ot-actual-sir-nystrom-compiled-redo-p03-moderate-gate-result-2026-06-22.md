# Actual-SIR Nystrom Compiled Redo P03 Moderate Gate Result

Date: 2026-06-22

Status: `PASS_WITH_XLA_COMPILE_LATENCY_WARNING`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Compiled redo can advance past the moderate validity/comparability gate, but serious ladder should address compile latency first | `PASS`: paired compiled `B=1,T=20,N=1024` row wrote artifact with `hard_vetoes=[]` | No numerical, residual, GPU, TF32, or paired-threshold vetoes | Nystrom XLA compile plus first call was `804.5176504359115s`; warm timing is descriptive and one-seed only | Run a compile-latency repair/profiling gate or a warm-only replicated protocol before serious default-promotion ladder | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness, no speed superiority |

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p03-moderate-gate-plan-2026-06-22.md`
- JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p03-moderate-b1-t20-n1024-2026-06-22.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p03-moderate-b1-t20-n1024-2026-06-22.md`

## Result Summary

| Field | Value |
| --- | --- |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Shape | `B=1,T=20,N=1024,D=18,M=9` |
| Seed | `81120` |
| GPU | Physical GPU1 |
| TF32 | enabled |
| JIT compile | `True` |
| Wall time | `821.6970312679186s` |

## Route Summary

| Route | Status | Compile plus first call | Warm median | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `15.772794160991907s` | `0.062396966852247715s` | `[]` |
| nystrom | `PASS` | `804.5176504359115s` | `0.09494141908362508s` | `[]` |

## Nystrom Diagnostics

| Diagnostic | Value |
| --- | ---: |
| Final logsumexp residual | `0.0` |
| Max row residual | `9.870529174804688e-05` |
| Max column residual | `4.76837158203125e-07` |
| Route invocations | `20` |
| Iterations used max | `3` |
| Finite factors | `True` |
| Finite particles | `True` |

## Paired Comparability

| Metric | Value | Threshold |
| --- | ---: | ---: |
| Log-likelihood max abs delta | `0.1632080078125` | `<=10.0` |
| Log-likelihood mean abs delta | `0.1632080078125` | `<=5.0` |
| Warm median streaming/Nystrom | `0.6572154435282669` | descriptive only |

## Interpretation

The moderate compiled redo row passed the hard-veto and paired-comparability
screen.  This supports continuing the redo lane under the repaired benchmark
protocol.  It does not support a speed ranking: the row has one seed and one
repeat, and the Nystrom route paid a very large XLA compile cost.

The main new issue is compile latency.  XLA emitted a slow-compile warning for
the compiled Nystrom graph, and the Nystrom compile plus first call took about
`804.52s` even though the warm call took about `0.095s`.  This suggests the
runtime kernel is viable after compilation, but the current compiled graph is
too expensive to recompile frequently.

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Warm timings and warm ratio are descriptive only |
| Default-readiness | `NO` |
| Next evidence needed | Compile-latency repair/profiling or a precompiled warm-only replicated protocol, then serious replicated row |

## Post-Run Red Team

The strongest alternative explanation is that the fixed Python-for-loop Nystrom
implementation unrolled too much work into the XLA graph at `T=20`, causing a
compile-time artifact.  A result that would overturn the current next step
would be a graph refactor or non-XLA graph-mode path that preserves residual and
paired diagnostics while reducing first-call latency by orders of magnitude.

