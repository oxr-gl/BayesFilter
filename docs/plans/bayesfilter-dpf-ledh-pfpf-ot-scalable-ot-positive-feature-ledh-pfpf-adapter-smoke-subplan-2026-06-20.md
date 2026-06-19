# Positive-Feature LEDH-PFPF-OT Adapter Smoke Subplan

Date: 2026-06-20
Owner: current agent
Lane: positive-feature Sinkhorn semantic-replacement

## Phase Objective

Plan the next positive-feature-only step after independent lane closeout: a
small opt-in adapter smoke that checks whether the positive-feature transport
object can satisfy the LEDH-PFPF-OT resampling-step tensor contract at the
existing transport seam.

This is a planning subphase only.  It does not replace the current
LEDH-PFPF-OT Sinkhorn/annealed transport path, does not compare against the
peer low-rank lane, and does not run trusted GPU/TF32 evidence.

## Entry Conditions Inherited From Previous Phase

- Positive-feature independent closeout passed:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-closeout-result-2026-06-20.md`
- Active independent-lane clarification exists:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-independent-lane-clarification-to-peer-2026-06-20.md`
- Current positive-feature implementation exists:
  `experiments/dpf_implementation/tf_tfp/resampling/positive_feature_transport_tf.py`
- Existing LEDH-PFPF-OT transport seam exists:
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
  function `batched_annealed_transport_core_tf`.
- Streaming value path calls that seam:
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
  function `streaming_batched_ledh_pfpf_ot_value_core_tf`.
- No ranking, default, public API, posterior correctness, HMC readiness, TF32
  help, or speedup claim is authorized.

## Required Artifacts For Execution

If this subplan is executed, the implementation should create only opt-in
adapter-smoke artifacts, for example:

- adapter or harness file:
  `docs/benchmarks/scalable_ot_positive_feature_ledh_pfpf_adapter_smoke.py`
- focused test:
  `tests/test_positive_feature_ledh_pfpf_adapter_smoke.py`
- JSON diagnostic:
  `docs/benchmarks/scalable-ot-positive-feature-ledh-pfpf-adapter-smoke-2026-06-20.json`
- Markdown diagnostic:
  `docs/benchmarks/scalable-ot-positive-feature-ledh-pfpf-adapter-smoke-2026-06-20.md`
- phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-ledh-pfpf-adapter-smoke-result-2026-06-20.md`

Any production-facing module change must be blocked unless a later reviewed
implementation subplan explicitly authorizes it.  A first smoke may use a
benchmark harness wrapper that returns the same tensor fields as
`BatchedAnnealedTransportTensors` without editing the LEDH-PFPF-OT value path.

## Required Checks, Tests, And Reviews

Planning checks now:

```bash
test -f docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-positive-feature-independent-closeout-result-2026-06-20.md
test -f experiments/dpf_implementation/tf_tfp/resampling/positive_feature_transport_tf.py
test -f experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py
test -f experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py
rg -n "def batched_annealed_transport_core_tf|class BatchedAnnealedTransportTensors" experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py
rg -n "batched_annealed_transport_core_tf" experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py
```

Required execution checks for a later implementation phase:

```bash
python -m py_compile docs/benchmarks/scalable_ot_positive_feature_ledh_pfpf_adapter_smoke.py tests/test_positive_feature_ledh_pfpf_adapter_smoke.py experiments/dpf_implementation/tf_tfp/resampling/positive_feature_transport_tf.py
pytest -q tests/test_positive_feature_ledh_pfpf_adapter_smoke.py
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/scalable_ot_positive_feature_ledh_pfpf_adapter_smoke.py --output docs/benchmarks/scalable-ot-positive-feature-ledh-pfpf-adapter-smoke-2026-06-20.json --markdown-output docs/benchmarks/scalable-ot-positive-feature-ledh-pfpf-adapter-smoke-2026-06-20.md
python -m json.tool docs/benchmarks/scalable-ot-positive-feature-ledh-pfpf-adapter-smoke-2026-06-20.json
```

Review:

- Codex skeptical audit is required before execution.
- Claude read-only review is optional for this planning subphase and should be
  used only if a material boundary or implementation-seam ambiguity appears.
- Trusted GPU/TF32 checks require a separate gated subplan and elevated/trusted
  execution context.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can an opt-in positive-feature adapter satisfy the LEDH-PFPF-OT resampling-step tensor contract on a tiny fixed CPU fixture? |
| Baseline/comparator | Existing `BatchedAnnealedTransportTensors` contract and current `batched_annealed_transport_core_tf` mask semantics.  Existing dense/streaming Sinkhorn behavior is a contract reference only, not a promotion comparator. |
| Primary pass criterion | Later execution must produce finite shape-valid particles/log weights, preserve inactive rows when `fixed_resampling_mask` is false, produce normalized uniform log weights on active rows, return an accepted sentinel transport matrix shape (`[B,0,0]`) or a reviewed compatible object, and record positive-feature residual diagnostics with empty hard vetoes. |
| Veto diagnostics | Missing entry artifacts, shape mismatch, nonfinite particles/features/scalings, nonpositive features, active/inactive mask semantic failure, log-weight normalization failure, residual failure, graph/eager incompatibility in the intended smoke mode, public/default/API edit, peer-lane dependency, or unsupported claim. |
| Explanatory diagnostics | Runtime, residual magnitudes, feature count, epsilon, candidate moment deltas, dense/streaming context, and TensorFlow environment warnings. |
| Not concluded | No ranking, speedup, posterior correctness, HMC readiness, TF32 help, GPU scalability, public API readiness, production/default readiness, dense Sinkhorn equivalence, or broad scalable-OT selection. |
| Artifact preserving result | Later adapter-smoke JSON/Markdown, focused test output, and phase result. |

## Skeptical Plan Audit

| Audit item | Control |
| --- | --- |
| Wrong baseline risk | Use the LEDH tensor/mask contract as the reference, not dense Sinkhorn equivalence. |
| Proxy promotion risk | Runtime and moment deltas are explanatory; the smoke promotes only "adapter contract viable for later testing." |
| Missing stop condition risk | Stop conditions block public/default edits, peer dependency, GPU/TF32 evidence, and unsupported claims. |
| Unfair comparison risk | No peer low-rank or dense-vs-positive ranking is performed. |
| Hidden assumption risk | The plan names the exact seam and requires active/inactive mask checks. |
| Stale context risk | Entry checks verify current positive-feature closeout and LEDH seam files before execution. |
| Environment mismatch risk | First execution is CPU-scoped; TensorFlow GPU warnings under `CUDA_VISIBLE_DEVICES=-1` are not GPU evidence. |
| Artifact-answer mismatch risk | The adapter smoke answers only whether an opt-in adapter can satisfy a tiny tensor contract. |

Skeptical audit decision: `PASSED_FOR_POSITIVE_FEATURE_ADAPTER_SMOKE_PLANNING`.

## Forbidden Claims And Actions

- Do not replace the current LEDH-PFPF-OT transport path by default.
- Do not edit public exports, package metadata, or default policies.
- Do not compare against or wait for the peer low-rank lane.
- Do not claim speedup, TF32 benefit, posterior correctness, HMC readiness,
  production readiness, dense Sinkhorn equivalence, or scientific superiority.
- Do not run GPU/TF32 checks in this subplan.
- Do not change thresholds after seeing results.

## Exact Next-Phase Handoff Conditions

A later implementation phase may begin only if:

- this subplan is committed or otherwise visible under `docs/plans`;
- planning checks pass;
- the implementation remains opt-in and positive-feature-owned;
- no peer-lane artifact is required;
- no trusted GPU/TF32 evidence is needed for the first smoke;
- a result artifact path is predeclared before execution.

If the CPU adapter smoke later passes, the next justified phase is a separate
gated trusted-GPU/TF32 adapter smoke plan.  If it fails for a contract reason,
write a blocker result and do not proceed to TF32.

## Stop Conditions

Stop and write a blocker if the adapter cannot satisfy the existing
`BatchedAnnealedTransportTensors` shape/rank contract without changing public
defaults, if mask semantics are ambiguous, if the first smoke would require GPU
evidence, if the route requires peer low-rank artifacts, or if any requested
interpretation exceeds the evidence contract.

## End-Of-Phase Checklist

1. Run the planning checks listed above.
2. Write or update the planning result if this subplan is accepted.
3. Before implementation, run a fresh skeptical audit and preserve the evidence
   contract in the result artifact.
