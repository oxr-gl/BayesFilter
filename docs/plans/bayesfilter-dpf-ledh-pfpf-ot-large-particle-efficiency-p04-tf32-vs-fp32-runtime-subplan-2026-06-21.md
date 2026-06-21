# P04 Same-Route TF32-Vs-FP32 Runtime Subplan

Date: 2026-06-21

Status: DRAFT_FOR_REVIEW

## Phase Objective

Run a matched-shape same-route runtime comparison between streaming FP32 with
TF32 enabled and streaming FP32 with TF32 disabled, using the same wrapper and
trusted selected GPU.

## Entry Conditions Inherited From Previous Phase

- P03 passed mandatory large-`N` streaming reach gates or wrote a blocker that
  still permits a smaller matched runtime diagnostic.
- Selected physical GPU and wrapper path are known.
- Runtime interpretation remains descriptive unless replicated uncertainty is
  added in a later plan.

## Required Artifacts

- P04 JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-2026-06-21.json`
- P04 Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-2026-06-21.md`
- P04 child artifact directory:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-gpu-children-2026-06-21/`
- P04 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p04-tf32-vs-fp32-runtime-result-2026-06-21.md`

## Required Checks, Tests, And Reviews

- Run wrapper with two arms at matched shape:
  - `fp32_tf32_enabled`;
  - `fp32_tf32_disabled`.
- Preferred matched shape:
  - particle count `10000`;
  - batch size `1`;
  - time steps `80`;
  - state dimension `20`;
  - observation dimension `20`;
  - active-all transport;
  - callback proposal;
  - sinkhorn iterations `4`;
  - row/column chunk sizes `1024`;
  - particle chunk size `256`;
  - warmups `0`;
  - repeats `1`.
- If P03 shows `10000` is too slow or failed for a non-harness reason, use the
  largest P03-passing rung with child elapsed time at most 1800 seconds and
  record the downgrade.
- Numeric runtime budget:
  - phase wall-clock budget is 3 hours;
  - per-arm child timeout is 3600 seconds;
  - the preferred matched shape is `10000` particles;
  - downgrade only by the explicit child-elapsed-time rule above.
- Post-run JSON audit:
  - both arms passed hard gates;
  - both arms match shape/config except TF32 mode;
  - both arms have finite outputs and GPU placement;
  - timing ratio is recorded as descriptive only.
- Claude read-only review if the result text risks overclaiming speedup.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | At matched large-`N` shape, is TF32-enabled streaming descriptively faster than TF32-disabled streaming on the same route and selected GPU? |
| Baseline/comparator | Same-route FP32 with TF32 disabled is the comparator; FP32 with TF32 enabled is the candidate. |
| Primary criterion | Both arms pass hard finite/device/storage/default-metadata gates and produce a matched-shape timing summary. |
| Veto diagnostics | Failed arm, mismatched shape/config, CPU fallback, non-finite output, dense storage, missing artifact, or TF32 mode mismatch. |
| Explanatory diagnostics | Warm median, compile plus first-call time, memory metadata, and timing ratio. |
| Not concluded | No statistical speedup claim, no quality superiority, no posterior correctness, no HMC readiness. |
| Artifact | P04 JSON/Markdown and P04 result. |

## Forbidden Claims Or Actions

- Do not claim statistical speedup from a single repeat.
- Do not compare TF32 and FP32 if any non-TF32 config differs.
- Do not use FP64 as the runtime baseline for this phase.

## Exact Next-Phase Handoff Conditions

Advance to P05 only if:

- P04 records whether the matched runtime diagnostic is valid;
- any timing ratio is labeled descriptive;
- P04 result identifies the largest shape with a valid matched comparison.

## Stop Conditions

- Both arms cannot be run under identical route/config.
- Runtime would exceed the numeric phase or child budget.
- A hard-gate failure invalidates timing interpretation.

## End-Of-Phase Actions

1. Run required post-run checks.
2. Write the P04 result/close record.
3. Draft or refresh the P05 subplan.
4. Review the P05 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
