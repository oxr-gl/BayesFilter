# Phase 6 Result: Compiler Metrics Gate

Date: 2026-07-02

Status: `PASS_TO_PHASE7_REVIEW`

## Phase Objective

Prove on a tiny trusted GPU/XLA fixture that the actual full manual route
compiles and executes with TensorFlow/XLA loop representation, and that the
compiled fixture is the total-derivative route rather than the stopped-key
partial-derivative route.

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Phase 6 passed for the tiny full-route GPU/XLA compiler metrics gate. |
| Primary criterion status | Met: trusted GPU/XLA run succeeded, `jit_compile=True`, all outputs were on `/GPU:0`, outputs were finite, concrete function count was `1`, warm same-signature call did not retrace, HLO text was available and contained while markers, and route evidence anchored `transport_ad_mode="full"` to the total-VJP transport helper path. |
| Veto diagnostic status | No Phase 6 veto fired. Trusted `nvidia-smi` passed; compiled execution did not fall back to CPU/non-XLA; output was finite; Phase 5 static/parity checks did not regress. |
| Main uncertainty | HLO is still large even for the tiny fixture: 27,766,809 characters and 52,059 lines. This is not a Phase 6 failure because while markers are present and warm-call behavior is good, but it is a scaling risk for larger fixtures. |
| Next justified action | Phase 7 numerical validation on the full route, with a bounded compiler-size watchpoint. |
| What is not concluded | No FD correctness, no statistical validity, no HMC readiness, no broad production readiness, and no claim that stopped-key helpers compute scores. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745`; worktree dirty (`git status --short` line count 899). |
| Commands | `nvidia-smi`; `python scripts/collect_ledh_clean_xla_phase6_metrics.py --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase6-compiler-metrics-2026-07-02.json --device /GPU:0 --expect-device-kind gpu --batch-seeds 81120 --time-steps 1 --num-particles 16 --theta 0.02,-0.01,0.01 --sinkhorn-iterations 2 --sinkhorn-epsilon 1.0 --annealed-scaling 0.9 --row-chunk-size 16 --col-chunk-size 16 --particle-chunk-size 16 --dtype float32 --tf32-mode enabled`; Phase 5 regression checks. |
| Environment | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python`; TensorFlow 2.19.1; TF32 enabled. |
| CPU/GPU status | Trusted GPU execution. `nvidia-smi` reported NVIDIA GeForce RTX 4080 SUPER. TensorFlow outputs were all on `/job:localhost/replica:0/task:0/device:GPU:0`. |
| Data version | P8p actual SIR d18 fixed tensor fixture, generated locally by the benchmark helper. |
| Random seeds | `batch_seeds=[81120]`; fixed stateless process-noise tensor policy inherited from Phase 2. |
| Wall time | Cold compile plus first call 24.426s; warm call 0.041s; HLO retrieval 4.693s; metrics script wall time 29.160s. |
| Output artifact | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase6-compiler-metrics-2026-07-02.json` |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase6-compiler-metrics-gate-subplan-2026-07-02.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase6-compiler-metrics-gate-result-2026-07-02.md` |

## Compiler Evidence

| Metric | Value |
| --- | --- |
| Decision | `PASS_TINY_FULL_ROUTE_GPU_XLA_COMPILER_METRICS` |
| `jit_compile` | `true` |
| Output finite | `true` |
| Concrete function count | `1` |
| Unexpected retrace | `false` |
| HLO text length | `27,766,809` |
| HLO line count | `52,059` |
| HLO `while` marker count | `199,199` lower-case matches |
| Route evidence kind | source-anchored static call-path evidence for the compiled fixture |
| Route anchors | 5 anchors |

The route evidence anchors show:

- `_manual_transport_vjp_tf` branches on `args.transport_ad_mode == "full"`;
- that branch calls `_filterflow_manual_streaming_finite_transport_total_vjp`;
- `_manual_forward_transport_tf` branches on `args.transport_ad_mode == "full"`;
- that branch calls `_filterflow_manual_streaming_finite_transport_total_vjp`;
- `batched_annealed_transport_core_tf` assigns the total-VJP helper when the
  mode is not the stabilized stopped-key branch.

This is source-anchored call-path evidence, not runtime call counters. The
result is acceptable for Phase 6 but weaker than instrumented runtime evidence.

## Regression Checks

```text
Phase 5 focused static/parity checks
..                                                                       [100%]
2 passed, 2 warnings in 5.00s

Phase 6 post-metrics static audit
decision: FAIL_CURRENT_ROUTE
current_veto_ids: SINK-STOPPED-VALUE-KEY, SINK-STOPPED-VJP-KEY
warning_ids: SINK-TOTAL-CUSTOM-TAPE
```

The post-metrics static audit is expected to remain `FAIL_CURRENT_ROUTE`
because stopped-key helpers remain in the repository and remain partial
derivative helpers. Those rows do not invalidate the full-route Phase 6
compiler fixture, but they still block any claim that the stopped-key helpers
compute scores.

## Post-Run Red-Team Note

The strongest misleading interpretation would be to claim that this proves
broad clean-XLA readiness. It does not. It proves only that a tiny
`T=1, N=16, one-seed` full-route fixture compiled and ran on GPU/XLA with
finite outputs, one concrete function, warm-call reuse, and HLO while markers.

The HLO is large for such a tiny fixture. That is the weakest part of the
compiler evidence. A later phase should watch HLO size or compile time when
increasing `T`, `N`, or Sinkhorn iterations.

## Next Handoff

Drafted next subplan:

`docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-numerical-validation-subplan-2026-07-02.md`

Phase 7 may begin only after Claude read-only review of this Phase 6 result and
the Phase 7 subplan returns `VERDICT: AGREE`, or fixable findings are patched
and rereviewed.
