# Actual-SIR Nystrom Default-Promotion P05 Replicated Ladder Interim Result

Date: 2026-06-22

Status: `PARTIAL_LADDER_PASSED_THROUGH_N2048_RUNTIME_PROTOCOL_REPAIR_REQUIRED`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Keep Nystrom in default-promotion testing but repair the runtime protocol before more paired scale rows | Passed P03 `N=1024`, P05A seed replication `N=1024`, and P05B `N=2048` validity/comparability | No hard vetoes in completed P05 rows | P05B speed timings are contaminated by a Python-loop/tiny-chunk harness path; no uncertainty model; no stress/HMC gates | Use compiled/comparable timing protocol for speed evidence, or run high-N Nystrom-only envelope rows without speed/default claims | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness |

## Completed P05 Evidence

| Stage | Shape | Seeds | GPU | Status | Hard vetoes | Paired comparability |
| --- | --- | --- | --- | --- | --- | --- |
| P03 basis | `B=5,T=20,N=1024` | `81120..81124` | GPU0 fallback | `PASS` | `[]` | `PASS` |
| P05A seed replication | `B=5,T=20,N=1024` | `81220..81224` | GPU1 | `PASS` | `[]` | `PASS` |
| P05B ladder | `B=5,T=20,N=2048` | `81120..81124` | GPU1 | `PASS` | `[]` | `PASS` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` for completed P05 rows |
| Viable candidates | Nystrom `rank=32`, `epsilon=0.5`, `max_iterations=160` remains viable |
| Statistically supported ranking | `NO`; P05B timing ratios are withdrawn for speed interpretation because the streaming comparator was not run on the compiled production-style path |
| Default-readiness | `NO`; default promotion requires more gates |
| Descriptive-only differences | Validity and paired comparability passed through `N=2048`; runtime comparison needs a repaired protocol |
| Next evidence needed | Compiled/comparable Nystrom timing probe, or explicitly Nystrom-only high-N envelope rows, then stress and gradient/HMC gates |

## Nonclaims

- No default readiness claim.
- No posterior correctness claim.
- No HMC readiness claim.
- No public API readiness claim.
- No statistical superiority claim.
- No dense Sinkhorn equivalence claim.

## Next Step

Before launching more paired scale rows, repair the benchmark protocol.  A
same-GPU compiled streaming sanity row at `B=5,T=20,N=2048` completed with
`20.397380776004866s` compile plus first call and `0.29988364898599684s` warm
call, while the P05B paired harness used a Python-level loop with small chunks
and reported `1160.5996048829984s` for streaming warm time.  This shows the
P05B speed ratio is not comparable to the production-style compiled streaming
baseline.
