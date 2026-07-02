# Reset Memo: LEDH-PFPF-OT N10000 Chunk Sizing

date: 2026-06-24
status: CURRENT_ROUTE_GUIDANCE

## Scope

This memo records an empirical chunk-sizing rule for the compiled manual-reverse
XLA LEDH-PFPF-OT SIR d=18 timing lane at `N=10000`, `T=3`, `float32`, TF32
enabled, streaming transport, and
`manual_streaming_finite_sinkhorn_stopped_scale_keys`.

This memo is about timing and allocator behavior only.  It does not certify FD
agreement, five-seed feasibility, HMC readiness, posterior correctness,
scientific validity, or production readiness.

## Rule

For this route and problem shape, prefer exact row/column transport chunks, but
keep each block moderate.  The current best tested row/column chunk size is:

```text
row_chunk_size = 2500
col_chunk_size = 2500
```

Use `2500 x 2500` as the empirical default for subsequent bounded N10000
manual-reverse XLA timing or FD-consistency work unless a new reviewed
chunk-sizing plan supersedes it.

## Evidence Summary

| Case | Block pairs | Effective padded pair slots | Compile + first call (s) | Warm call (s) | Allocator peak (GiB) | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| `N=10000`, chunk `2048` | 25 | 104857600 | 421.3336761600076 | 2.3217804890009575 | 0.31909871101379395 | Valid, slower than `2500`. |
| `N=10000`, chunk `2500` | 16 | 100000000 | 340.6117727160163 | 1.5704608989763074 | 0.3162567615509033 | Best tested shape. |
| `N=10000`, chunk `3334` | 9 | 100040004 | 426.22349167799985 | 2.3859367769910023 | 0.384676456451416 | Fewer blocks but slower. |
| `N=10000`, chunk `5000` | 4 | 100000000 | 374.984015738999 | 10.04070115898503 | 0.5389814376831055 | Exact but too large; reject. |
| `N=10240`, chunk `2560` | 16 | 104857600 | 352.64430643300875 | 1.7404677319864277 | 0.3317444324493408 | Binary-friendly but slower raw and normalized. |

The `2500 x 2500` run was about `1.48x` faster than `2048 x 2048` on the
single warm-call timing and about `6.39x` faster than `5000 x 5000`.

The binary-boundary test was not favorable: `N=10240/chunk=2560` was about
`10.8%` slower raw and about `5.7%` slower after normalizing by effective pair
slots than `N=10000/chunk=2500`.

## Interpretation

The lesson is not simply "use the largest exact chunk" or "use binary-friendly
sizes."  The observed rule is:

1. Exact tiling helps reduce wasted pair slots.
2. Oversized exact chunks can produce much worse XLA/GPU kernel behavior.
3. Binary-friendly chunk boundaries did not improve this route.
4. `2500 x 2500` is the best tested balance of exact tiling, block size, XLA
   compile behavior, warm-call timing, and allocator peak.

## Artifact Ledger

- `2048` result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2048-result-2026-06-24.json`
- `2500` plan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2500-plan-2026-06-24.md`
- `2500` result note:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2500-result-2026-06-24.md`
- `2500` result JSON:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2500-result-2026-06-24.json`
- `3334` result note:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk3334-result-2026-06-24.md`
- `5000` result note:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk5000-result-2026-06-24.md`
- `10240/2560` binary-boundary result note:
  `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10240-xla-chunk2560-binary-boundary-result-2026-06-24.md`

## Guardrails For Future Agents

- Do not infer FD agreement from these timing runs.
- Do not use Zhao-Cui as a comparator or oracle for these chunk-sizing claims.
- Do not reopen `transport_ad_mode=full`; that path was rejected for memory
  explosion.
- Do not treat `nvidia-smi` reservation as actual peak memory; use TensorFlow
  allocator telemetry for these diagnostics.
- Run GPU/XLA timing commands with trusted GPU permissions per `AGENTS.md`.
- If retuning chunk sizes, write a bounded plan first and compare against
  `N=10000/chunk=2500` raw warm-call timing plus normalized pair-slot timing
  when `N` changes.
