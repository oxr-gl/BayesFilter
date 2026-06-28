# Actual-SIR Nystrom Compiled Redo P04 Serious B5 Gate Result

Date: 2026-06-23

Status: `PASS_SERIOUS_B5_GATE`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Advance the repaired compiled redo lane to a replicated seed-batch gate | `PASS`: serious `B=5,T=20,N=1024` row wrote artifact with `hard_vetoes=[]` | No numerical, residual, GPU, TF32, compile-latency, or paired-threshold vetoes | One batched seed set only; no replicated uncertainty model; no stress/HMC gates | Run a second `B=5,T=20,N=1024` repaired compiled seed batch with disjoint seeds | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness, no superiority claim |

## Artifacts

- Plan: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-compiled-redo-p04-serious-b5-gate-plan-2026-06-23.md`
- JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p04-serious-b5-t20-n1024-2026-06-23.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p04-serious-b5-t20-n1024-2026-06-23.md`

## Result Summary

| Field | Value |
| --- | --- |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Shape | `B=5,T=20,N=1024,D=18,M=9` |
| Seeds | `81120,81121,81122,81123,81124` |
| GPU | Physical GPU1 |
| TF32 | enabled |
| JIT compile | `True` |
| Wall time | `35.00179703696631s` |

## Route Summary

| Route | Status | Compile plus first call | Warm median | Hard vetoes |
| --- | --- | ---: | ---: | --- |
| streaming | `PASS` | `19.750352774048224s` | `0.10740198497660458s` | `[]` |
| nystrom | `PASS` | `14.019542706897482s` | `0.05731428205035627s` | `[]` |

## Nystrom Diagnostics

| Diagnostic | Value |
| --- | ---: |
| Final logsumexp residual | `0.0` |
| Max row residual | `9.548664093017578e-05` |
| Max column residual | `2.384185791015625e-06` |
| Route invocations | `20` |
| Iterations used max | `3` |
| Finite factors | `True` |
| Finite particles | `True` |

## Paired Comparability

| Metric | Value | Threshold |
| --- | ---: | ---: |
| Log-likelihood max abs delta | `3.85498046875` | `<=10.0` |
| Log-likelihood mean abs delta | `1.9035400390625` | `<=5.0` |
| Warm median streaming/Nystrom | `1.8739131178899058` | descriptive only |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Warm timing ratio and per-seed deltas are descriptive only |
| Default-readiness | `NO` |
| Next evidence needed | Replicated disjoint seed-batch gate, then consider larger-N ladder |

## Interpretation

The repaired compiled route now passes the serious actual-SIR `B=5,T=20,N=1024`
gate.  The compile-latency repair remains effective at this batched shape:
Nystrom compile plus first call was `14.02s` and warm call was `0.057s`.

The paired log-likelihood deltas remain within threshold, but they are not
statistical evidence of equality or superiority.  The next appropriate gate is
a disjoint replicated seed batch at the same shape.

