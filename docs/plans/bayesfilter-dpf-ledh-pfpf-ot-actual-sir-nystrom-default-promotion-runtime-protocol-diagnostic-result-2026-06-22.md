# Actual-SIR Nystrom Runtime Protocol Diagnostic Result

Date: 2026-06-22

Status: `P05B_SPEED_INTERPRETATION_WITHDRAWN`

## Question

Was the long P05B `N=2048` runtime caused by GPU/TF32 slowness, or by the
paired Nystrom benchmark protocol?

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Determine whether the same machine/GPU can run the production-style compiled actual-SIR streaming path quickly at `B=5,T=20,N=2048`. |
| Comparator | P05B paired harness streaming route timing. |
| Primary diagnostic | Same physical GPU1, TF32 enabled, compiled `benchmark_p8j_tf32_batched_actual_sir.py`, finite output, GPU output tensor, warm-call runtime. |
| Vetoes | Missing GPU output, nonfinite output, TF32 not enabled, failed artifact write. |
| Explanatory diagnostics | Compile plus first call, warm call, chunks, history mode, GPU memory. |
| Nonclaim | This diagnostic does not validate Nystrom, rank candidates, posterior correctness, or default readiness. |

## Artifacts

- Compiled streaming diagnostic JSON: `docs/benchmarks/actual-sir-streaming-compiled-sanity-b5-t20-n2048-gpu1-2026-06-22.json`
- Compiled streaming diagnostic Markdown: `docs/benchmarks/actual-sir-streaming-compiled-sanity-b5-t20-n2048-gpu1-2026-06-22.md`
- P05B paired JSON: `docs/benchmarks/actual-sir-nystrom-default-promotion-p05b-ladder-b5-t20-n2048-2026-06-22.json`
- P05B paired result note: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-default-promotion-p05b-ladder-result-2026-06-22.md`

## Result

| Diagnostic | Value |
| --- | ---: |
| Compiled streaming compile plus first call | `20.397380776004866s` |
| Compiled streaming warm call | `0.29988364898599684s` |
| Compiled streaming chunk sizes | `row=2048,col=2048,particle=1024` |
| Compiled streaming history mode | `value-only` |
| P05B Python-loop streaming first call | `1167.2142036410514s` |
| P05B Python-loop streaming warm call | `1160.5996048829984s` |
| P05B Python-loop Nystrom warm call | `69.52919894712977s` |
| P05B chunk sizes | `row=128,col=128,particle=64` |

## Interpretation

The same physical GPU1 and TF32 stack run the compiled production-style
actual-SIR streaming path quickly at `N=2048`.  Therefore the P05B streaming
runtime is not evidence that TF32/GPU is slow on this machine.  The P05B speed
ratio is contaminated by a benchmark-protocol mismatch: the paired harness uses
a Python-level per-step route loop with small chunks, while the production-style
streaming benchmark uses a compiled XLA value core and larger chunks.

P05B still supports its hard-veto and paired-comparability conclusion.  It does
not support a speed ranking or default-promotion speed claim.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Withdraw P05B speed interpretation and pause paired scale rows | Compiled streaming sanity passed on GPU1 | No diagnostic vetoes | Nystrom route has not yet been compiled comparably | Build or test a compiled/comparable Nystrom benchmark path, or run Nystrom-only envelope rows with no speed/default claim | No Nystrom superiority, no default readiness, no HMC readiness, no posterior correctness |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | P05B validity/comparability hard vetoes still pass |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | P05B runtime ratio is withdrawn as contaminated |
| Default-readiness | `NO` |
| Next evidence needed | Comparable compiled Nystrom-vs-streaming timing or explicitly Nystrom-only high-N feasibility |

