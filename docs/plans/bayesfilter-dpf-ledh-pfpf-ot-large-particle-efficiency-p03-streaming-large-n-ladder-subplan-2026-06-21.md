# P03 Streaming Large-N Reach Ladder Subplan

Date: 2026-06-21

Status: DRAFT_FOR_REVIEW

## Phase Objective

Run the production-default GPU TF32 streaming LEDH-PFPF-OT route over a
predeclared large-particle ladder to test operational large-`N` reach and
storage invariants.

## Entry Conditions Inherited From Previous Phase

- P02 selected a trusted physical GPU and recorded the reason.
- Wrapper static checks passed in P01.
- Commands will use `--cuda-visible-devices <selected-physical-gpu>` and
  `--device /GPU:0`, because CUDA remaps the selected physical GPU to logical
  GPU0 inside the child process.
- Immediately before P03 launch, rerun trusted `nvidia-smi` for the selected
  physical GPU. The selected GPU must still be uncontaminated for this lane:
  no unrelated compute process may be present on the selected GPU, except
  display/remoting processes on GPU0 if GPU0 is explicitly selected by the P02
  fallback rule. This stricter just-in-time gate is required because P03 timing
  and memory evidence are invalid if another algorithm lane shares the same GPU
  during the ladder.

## Required Artifacts

- P03 JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-2026-06-21.json`
- P03 Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-2026-06-21.md`
- P03 child artifact directory:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-gpu-children-2026-06-21/`
- P03 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p03-streaming-large-n-ladder-result-2026-06-21.md`

## Required Checks, Tests, And Reviews

- Run wrapper in trusted GPU context for particle counts:
  - `1000`;
  - `5000`;
  - `10000`;
  - `20000`, only if prior rungs pass and the numeric budget rule below is
    satisfied.
- Shape defaults for P03:
  - batch size `1`;
  - time steps `80`;
  - state dimension `20`;
  - observation dimension `20`;
  - transport policy `active-all`;
  - proposal mode `callback`;
  - sinkhorn iterations `4`;
  - row/column chunk sizes `1024`;
  - particle chunk size `256`;
  - warmups `0`;
  - repeats `1`;
  - dtype `float32`;
  - TF32 mode `enabled`;
  - `return_history=False`.
- Post-run JSON audit:
  - each required rung passed;
  - each child output is finite;
  - each child output device contains GPU;
  - each child records production-default precision metadata;
  - no dense transport matrix materialized;
  - no full pre-flow tensor stored;
  - no history returned;
  - parent selected physical GPU metadata is present;
  - child `CUDA_VISIBLE_DEVICES` and logical GPU placement are present.
- Numeric runtime budget:
  - phase wall-clock budget is 4 hours;
  - per-rung child timeout is 3600 seconds;
  - `1000`, `5000`, and `10000` are mandatory;
  - `20000` is attempted only if all mandatory rungs pass, elapsed P03 time is
    at most 2 hours, the `10000` child elapsed time is at most 1200 seconds, and
    no GPU-memory warning/OOM occurred.
- Just-in-time GPU lease/contamination checks:
  - before wrapper launch, trusted `nvidia-smi` must show no unrelated compute
    process on the selected physical GPU;
  - during the first child startup, trusted `nvidia-smi` must show only this
    P03 parent/child process family on the selected GPU;
  - if an unrelated process appears on the selected GPU before mandatory rungs
    complete, stop this lane's P03 run, preserve any completed child artifacts
    as contaminated diagnostic-only evidence, write a P03 blocker/repair
    result, and do not interpret runtime or memory as efficiency evidence;
  - do not stop, kill, pause, or otherwise manage the peer lane's process
    without explicit human approval.
- Claude read-only review of P03 result only if the interpretation would
  materially affect closeout claims or if a repair changes the evidence
  contract.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current default streaming GPU TF32 route run the predeclared large-`N` ladder with finite outputs and no dense storage artifacts? |
| Baseline/comparator | Primary candidate only: streaming FP32+TF32 default. Dense is not a large-`N` comparator in this phase. |
| Primary criterion | Required rungs pass hard finite/device/storage/default-metadata gates and artifacts are complete. |
| Veto diagnostics | Mandatory-rung OOM/timeout, non-finite output, CPU fallback, missing child artifact, dense matrix materialized, full pre-flow tensor storage, `return_history=True`, wrong precision metadata, missing parent selected-GPU metadata, missing child remapped-device evidence, or unrelated compute-process contamination on the selected GPU during P03. |
| Explanatory diagnostics | Warm-call median, compile plus first-call time, memory metadata, stdout/stderr tails, and output previews. |
| Not concluded | No posterior correctness, no speedup, no statistical ranking, no dense equivalence, no HMC readiness. |
| Artifact | P03 JSON/Markdown, child artifacts, and P03 result. |

## Forbidden Claims Or Actions

- Do not claim TF32 speedup from P03 alone.
- Do not claim dense route failure unless P05 runs and records it.
- Do not change particle-count promotion criteria after seeing results.
- Do not continue to larger unplanned `N` without writing a refreshed subplan
  or explicit closeout recommendation.
- Do not use a partially completed or contaminated P03 run as runtime,
  memory-efficiency, or large-`N` promotion evidence.
- Do not interrupt the peer low-rank lane; only stop P03 processes launched by
  this lane unless the user explicitly approves broader process control.

## Exact Next-Phase Handoff Conditions

Advance to P04 only if:

- P03 passes required hard gates for at least the mandatory rungs `1000`,
  `5000`, and `10000`;
- no unrelated selected-GPU compute process contaminated the run before the
  mandatory rungs completed;
- if `20000` is skipped, the result records which numeric optional-rung rule
  caused the skip;
- P03 result separates memory/scale reach from runtime interpretation.

## Stop Conditions

- A mandatory rung fails a hard veto that invalidates the harness or route.
- GPU execution cannot be trusted.
- Another lane or unrelated process appears on the selected physical GPU during
  P03 and contaminates efficiency evidence.
- Mandatory-rung runtime exceeds the numeric phase or child budget and no
  partial result can answer the question.

## End-Of-Phase Actions

1. Run required local/post-run checks.
2. Write the P03 result/close record.
3. Draft or refresh the P04 subplan.
4. Review the P04 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
