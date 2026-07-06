# Actual-SIR Nystrom Compiled Redo Result

Date: 2026-06-22

Status: `REDO_P02_GPU_SMOKE_PASSED_OLD_RUNTIME_BENCHMARKS_QUARANTINED`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Redo actual-SIR Nystrom benchmarks under compiled comparable route conditions | P02 compiled GPU smoke passed at `B=1,T=3,N=128` | No hard vetoes | No serious-size replicated evidence yet; no uncertainty model; no stress/HMC gates | Run a moderate compiled paired row, then a serious row only if the moderate row passes | No default readiness, no statistical ranking, no posterior correctness, no HMC readiness |

## Why Redo

The prior actual-SIR Nystrom timing artifacts are non-authoritative for speed or
ranking.  They used a Python-level route loop and small chunks for the paired
Nystrom harness, while the production-style streaming route is normally run as
a compiled XLA value core.  A same-GPU compiled streaming sanity row at
`B=5,T=20,N=2048` took `20.397380776004866s` compile plus first call and
`0.29988364898599684s` warm call, proving the old `1160.5996048829984s`
streaming timing was a benchmark-protocol artifact.

## Implementation Repair

- Added tensor-only graph-compatible Nystrom core:
  `experiments/dpf_implementation/tf_tfp/resampling/nystrom_transport_tf.py`
  function `nystrom_transport_resample_tensors_tf`.
- Kept the old diagnostic wrapper `nystrom_transport_resample_tf`, now backed
  by the tensor core.
- Replaced `.numpy()` early stopping in the Nystrom Sinkhorn loop with a
  graph-compatible fixed loop that freezes updates after first convergence.
- Added compiled redo harness:
  `docs/benchmarks/benchmark_actual_sir_nystrom_compiled_redo.py`.

## Verification

| Check | Result |
| --- | --- |
| `pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_default_promotion.py` | `7 passed` |
| `pytest -q tests/test_nystrom_transport_tf.py tests/test_actual_sir_nystrom_compiled_redo.py` | `5 passed` |
| CPU tiny compiled redo | `PASS`, routes `streaming,nystrom`, paired log-likelihood delta `0.0` |
| GPU compiled redo smoke | `PASS`, `hard_vetoes=[]` |

## GPU Smoke Artifact

- JSON: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p02-gpu-smoke-2026-06-22.json`
- Markdown: `docs/benchmarks/actual-sir-nystrom-compiled-redo-p02-gpu-smoke-2026-06-22.md`

## GPU Smoke Summary

| Field | Value |
| --- | --- |
| Shape | `B=1,T=3,N=128,D=18,M=9` |
| GPU | physical GPU1 selected |
| TF32 | enabled |
| JIT compile | `True` |
| Status | `PASS` |
| Hard vetoes | `[]` |
| Streaming compile plus first call | `15.939500648993999s` |
| Streaming warm call | `0.011182473972439766s` |
| Nystrom compile plus first call | `103.2542302198708s` |
| Nystrom warm call | `0.013364152982831001s` |
| Paired log-likelihood max abs delta | `0.32093048095703125` |
| Nystrom max row residual | `1.2874603271484375e-05` |
| Nystrom max column residual | `2.384185791015625e-07` |

## Inference Status

| Ledger | Status |
| --- | --- |
| Hard veto screen | `PASS` for compiled P02 smoke |
| Statistically supported ranking | `NO` |
| Descriptive-only differences | Warm timings are descriptive only and too small/short for ranking |
| Default-readiness | `NO` |
| Next evidence needed | Moderate compiled paired row, then serious-size replicated row if moderate passes |

## Next Gate

Run a moderate compiled paired row before any serious default-promotion ladder:
`B=1,T=20,N=1024`, seed `81120`, GPU1 if available, TF32 enabled,
`history-mode value-only`, one repeat.  This is a protocol/effectiveness gate,
not a default-promotion gate.  If it passes, then define the serious redo ladder
from scratch.
