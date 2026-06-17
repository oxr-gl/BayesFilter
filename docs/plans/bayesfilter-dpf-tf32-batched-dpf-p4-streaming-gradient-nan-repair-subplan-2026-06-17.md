# Phase 4 Repair Subplan - Streaming Transport NaN Gradient - 2026-06-17

## Phase Objective

Repair or route around the non-finite raw TensorFlow gradient produced by the
memory-efficient streaming active transport plan, while preserving the active
transport value contract and without claiming HMC/posterior correctness.

This phase targets the blocker recorded in:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-active-transport-score-jit-repair-result-2026-06-17.md`

## Entry Conditions Inherited From Previous Phase

- Phase 0 through Phase 3 passed.
- Phase 4 no-resampling score/JIT passed.
- Active-transport score/JIT now compiles far enough to emit JSON under
  `jit_compile=True`.
- Active-odd dense transport score arms are finite and match.
- Active-odd streaming transport values match dense values.
- Active-odd streaming transport raw scores are non-finite.
- No-resampling score/JIT regression remains passing after loop-bound repairs.

## Required Artifacts

- This subplan.
- A NaN-localization diagnostic artifact:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-streaming-gradient-nan-localization-2026-06-17.md`
- Updated implementation only if the localization supports a narrow repair:
  - `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  - `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- Primary active-odd FP64 score/JIT JSON/Markdown/log artifacts.
- Mandatory no-resampling FP64 score/JIT regression JSON/Markdown/log
  artifacts.
- Focused test logs under `docs/benchmarks/logs/`.
- Repair result:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-streaming-gradient-nan-repair-result-2026-06-17.md`
- Updated ledger and stop handoff.

## Required Checks, Tests, And Reviews

Local checks:

1. Preserve the research question: can active streaming transport expose a
   finite score path for the tiny active-odd fixture?
2. Localize the NaN to one of these routes before editing code:
   - streaming Sinkhorn potential gradient;
   - streaming column normalizer gradient;
   - streaming transport application gradient;
   - interaction between transport branch and filter recursion.
3. Prefer the smallest repair that passes the primary gate:
   - numeric stabilization of raw streaming gradient if local and value-safe;
   - dense-gradient / streaming-value hybrid if raw streaming backward is
     unstable but dense gradient is finite;
   - custom gradient only with a separate reviewed contract.
4. If using a dense-gradient / streaming-value hybrid, state explicitly that it
   is not yet the memory-optimal 100k-particle score path. It may be a
   correctness bridge for tiny HMC-facing diagnostics only.
5. Run `py_compile` on patched files.
6. Run focused tests for streaming transport/value parity.
7. Rerun primary active-odd FP64 score/JIT diagnostic.
8. Rerun mandatory no-resampling FP64 score/JIT regression.
9. Run `git diff --check`.

Review:

- Claude review is optional for implementation only if the repair remains a
  narrow diagnostic/hybrid route and does not claim production/HMC readiness.
  Claude review is required before a custom-gradient claim or a default-policy
  change.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the active streaming transport score path be made finite under JIT on the tiny active-odd fixture without changing active transport values? |
| Baseline/comparator | Current active-odd artifact with finite dense scores and NaN streaming scores; no-resampling rerun that passes; dense transport score arm as tiny reference. |
| Primary pass criterion | Active-odd FP64 gradient-structure harness exits 0, `overall_passed: true`, all arms finite, `jit_compile: true`, values match dense reference, streaming score matches dense reference within `1e-5` score tolerance. |
| Veto diagnostics | Non-finite score; value mismatch; JIT failure; no-resampling regression; unreviewed custom-gradient semantics; HMC/posterior/default readiness claim. |
| Explanatory diagnostics | Which subcomponent first produces NaN gradient; whether dense-gradient fallback is used; compile/warm timings; score drift table. |
| Not concluded | No HMC readiness, no posterior validity, no production default, no memory-optimal 100k-particle score claim, no finite-difference correctness unless separately tested. |
| Artifact preserving result | NaN-localization note, JSON/Markdown benchmark artifacts, focused test logs, repair result. |

## Exact Commands

Primary active-odd FP64 gate:

```bash
CUDA_VISIBLE_DEVICES=-1 TF_CPP_MIN_LOG_LEVEL=1 \
timeout 240 /home/ubuntu/anaconda3/envs/tfgpu/bin/python \
  docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_gradient_structure.py \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --batch-size 1 \
  --time-steps 3 \
  --num-particles 8 \
  --state-dim 2 \
  --obs-dim 2 \
  --transport-policy active-odd \
  --sinkhorn-iterations 3 \
  --repeats 1 \
  --dtype float64 \
  --tf32-mode disabled \
  --structure-value-atol 1.0e-6 \
  --structure-value-rtol 1.0e-6 \
  --structure-score-atol 1.0e-5 \
  --structure-score-rtol 1.0e-5 \
  --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-nan-repair-2026-06-17.json \
  --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-nan-repair-2026-06-17.md \
  > docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-nan-repair-2026-06-17.log 2>&1
```

Mandatory no-resampling FP64 regression:

```bash
CUDA_VISIBLE_DEVICES=-1 TF_CPP_MIN_LOG_LEVEL=1 \
timeout 240 /home/ubuntu/anaconda3/envs/tfgpu/bin/python \
  docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_gradient_structure.py \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --batch-size 1 \
  --time-steps 3 \
  --num-particles 8 \
  --state-dim 2 \
  --obs-dim 2 \
  --transport-policy no-resampling \
  --sinkhorn-iterations 3 \
  --repeats 1 \
  --dtype float64 \
  --tf32-mode disabled \
  --structure-value-atol 1.0e-6 \
  --structure-value-rtol 1.0e-6 \
  --structure-score-atol 1.0e-5 \
  --structure-score-rtol 1.0e-5 \
  --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-nan-repair-2026-06-17.json \
  --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-nan-repair-2026-06-17.md \
  > docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-nan-repair-2026-06-17.log 2>&1
```

## Forbidden Claims And Actions

- Do not claim HMC readiness.
- Do not claim posterior correctness.
- Do not claim production/default/public API readiness.
- Do not claim 100k-particle score memory scalability if the repair uses a
  dense-gradient fallback.
- Do not add NumPy to BayesFilter-owned algorithmic implementation paths.
- Do not change TF32 default policy in this phase.
- Do not continue to Phase 5 unless the primary active-odd gate passes.

## Handoff Conditions

Phase 5 may begin only if:

- the repair result records `PHASE_4_STREAMING_GRADIENT_NAN_REPAIR_PASSED`;
- active-odd FP64 gate records `overall_passed: true`;
- no-resampling regression records `overall_passed: true`;
- the result clearly states whether the score route is raw streaming,
  dense-gradient hybrid, or custom-gradient;
- all local checks pass;
- no forbidden claim is made.

## Stop Conditions

Stop and write a blocker if:

- NaNs persist in streaming score after the chosen narrow repair;
- dense-gradient hybrid is needed but unacceptable for the user's current
  target;
- custom-gradient semantics are needed before a reviewed custom-gradient plan
  exists;
- value equality regresses;
- no-resampling regresses;
- continuing requires a broader algorithmic redesign.
