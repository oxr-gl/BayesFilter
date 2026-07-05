# P82 Phase 6 Subplan: Tiny Manual-Streaming GPU Smoke

status: REVIEWED_CLAUDE_R4_AGREE_READY_FOR_EXECUTION
date: 2026-06-23
phase: P6-TINY-MANUAL-STREAMING-GPU-SMOKE

## Phase Objective

Run the smallest trusted GPU/TF32 smoke that exercises the P5-wired manual
streaming transport-gradient route through the SIR d18 actual-gradient path,
using the regression harness in `ad-only` mode.

This is a backend/mechanics smoke only.  It is not P82 validation and it must
not run the governed `N=10000` actual-gradient or `N=1000` regression-FD jobs.

## Entry Conditions

- P5 result status is `REVIEWED_PASSED_CLAUDE_AGREE`.
- The manual route is selectable through the P82 benchmark CLI as:

```text
--transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys
```

- P5 preserved default `"raw"` behavior unless the manual route is explicitly
  selected.
- The old `transport_ad_mode=full` governed N10000 route remains forbidden.
- GPU commands require trusted/escalated execution under repository policy.

## Required Artifacts

- Tiny smoke JSON:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-2026-06-23.json`
- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-result-2026-06-23.md`
- Updated P82 execution ledger, Claude review ledger, and stop handoff.

## Required Checks / Tests / Reviews

Before GPU work, rerun the focused CPU-hidden checks:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-*.md
```

Trusted/escalated GPU preflight:

```bash
nvidia-smi
MPLCONFIGDIR=/tmp python -c "import tensorflow as tf; print(tf.__version__); print(tf.config.list_physical_devices()); print(tf.config.list_physical_devices('GPU'))"
```

Trusted/escalated tiny smoke:

```bash
MPLCONFIGDIR=/tmp timeout 900 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 1 --num-particles 8 \
  --batch-seeds 81120 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode reverse-gradient \
  --fd-mode ad-only \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 Phase 6 tiny manual streaming transport-gradient GPU smoke" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --sinkhorn-iterations 2 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 8 --col-chunk-size 8 --particle-chunk-size 8 \
  --dtype float32 --tf32-mode enabled \
  --basis-set raw \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-2026-06-23.json
```

After the smoke, write the Phase 6 result and run one-path Claude read-only
review of that result.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the P5-wired manual streaming transport-gradient route execute on a tiny SIR d18 GPU/TF32 actual-gradient smoke? |
| Baseline/comparator | P5 CPU-hidden parser/forwarding tests; this phase checks GPU-visible mechanics only. |
| Primary criterion | Trusted GPU preflight succeeds; the tiny smoke exits 0; output JSON records GPU-visible placement, `transport_plan_mode=streaming`, `gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, `regression_fd.fd_mode=ad-only`, finite objective, finite gradient, and no FD line is run. |
| Veto diagnostics | Non-escalated GPU command used as evidence; GPU not visible when `expect-device-kind=gpu`; output metadata records the wrong plan, gradient, or AD mode; `regression_fd.fd_mode` is not `ad-only`; nonfinite objective/gradient; OOM; timeout; artifact missing; default behavior changed; FD protocol changed; any P82 validation, N10000, or N1000 run is launched. |
| Explanatory diagnostics | Runtime, TensorFlow warnings, TF32 metadata, chunk metadata, one-seed gradient values. |
| Not concluded | No FD agreement, no N10000 feasibility, no N1000 regression-FD result, no full SIR d18 validation, no posterior/HMC/default/scientific-superiority readiness, no Zhao-Cui comparator readiness, and no source-faithfulness claim. |
| Artifact preserving result | Tiny JSON, Phase 6 result markdown, ledger updates, and Claude review ledger entry. |

## Forbidden Claims / Actions

- Do not run governed P82 validation.
- Do not run `N=10000` actual-gradient work.
- Do not run `N=1000` regression-FD work.
- Do not use `transport_ad_mode=full`.
- Do not treat the tiny smoke as FD consistency evidence.
- Do not change defaults or promote the manual route as production-ready.
- Do not use Zhao-Cui as comparator in this phase.

## Exact Next-Phase Handoff Conditions

If Phase 6 passes local checks, trusted GPU smoke, and one-path Claude review,
Phase 7 may draft a bounded actual-gradient feasibility subplan.  Phase 7 must
still be separate and must predeclare particle count, seed policy, runtime
budget, memory/metadata vetoes, and whether it is only a feasibility rung or
part of the governed FD comparison.

## Stop Conditions

Stop and write a blocker if trusted GPU preflight fails, if the tiny smoke OOMs
or times out, if output metadata does not prove the manual route was selected,
if finite diagnostics fail, if the smoke would require a default change, or if
Claude review does not converge after five rounds on a material issue.
