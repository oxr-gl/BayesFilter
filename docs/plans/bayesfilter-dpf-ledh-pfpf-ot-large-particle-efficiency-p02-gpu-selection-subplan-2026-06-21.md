# P02 Trusted GPU Selection Preflight Subplan

Date: 2026-06-21

Status: DRAFT_FOR_REVIEW

## Phase Objective

Run trusted GPU preflight, choose the physical GPU according to a mechanical
user-policy rule (`GPU1` unless busy or unsuitable, otherwise `GPU0`), and
record the selected physical GPU and reason before any GPU benchmark.

## Entry Conditions Inherited From Previous Phase

- P01 wrapper implementation and static checks passed.
- The wrapper supports recording selected physical GPU and selection reason.
- No material plan-review blocker remains.

## Required Artifacts

- P02 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p02-gpu-selection-result-2026-06-21.md`
- Optional trusted preflight log:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-large-particle-efficiency-p02-nvidia-smi-2026-06-21.txt`
- Refreshed P03 and P04 subplans with selected physical GPU if needed.

## Required Checks, Tests, And Reviews

- Trusted/elevated `nvidia-smi` query with index, name, memory used, memory
  total, and utilization.
- Codex GPU selection audit:
  - prefer physical GPU1 when present and usable;
  - classify GPU1 as busy/unsuitable if it is absent, has total memory used of
    at least 2048 MiB, has at least 20% utilization, or has any single non-display compute process using at least 2048 MiB;
  - record light non-display compute processes below those thresholds as
    shared-GPU warnings rather than vetoes;
  - use physical GPU0 only when GPU1 is busy/unsuitable by that rule and GPU0
    is usable by the same thresholds;
  - stop for direction if both GPUs are busy/unsuitable.
- No Claude review is required unless the GPU policy or phase boundary changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which trusted physical GPU should the visible run use, and is the choice compliant with the user policy? |
| Baseline/comparator | GPU1 is the preferred physical GPU; GPU0 is fallback only. |
| Primary criterion | Trusted `nvidia-smi` succeeds and the selected physical GPU plus threshold-based reason are recorded. |
| Veto diagnostics | Untrusted GPU-only evidence, missing GPU status, GPU0 selected without a GPU1-busy/unsuitable threshold reason, both GPUs busy/unsuitable by threshold, or no usable GPU. |
| Explanatory diagnostics | GPU memory used/total, utilization, and light shared-GPU process warnings below veto thresholds. |
| Not concluded | No benchmark success, no runtime comparison, no device correctness beyond preflight. |
| Artifact | P02 result and optional preflight log. |

## Forbidden Claims Or Actions

- Do not interpret sandbox GPU failures as machine failures unless repeated in
  trusted context.
- Do not run large benchmarks before selection is recorded.
- Do not use GPU0 silently.

## Exact Next-Phase Handoff Conditions

Advance to P03 only if:

- selected physical GPU is recorded;
- wrapper commands can use `--cuda-visible-devices <selected>` and
  `--device /GPU:0`;
- P02 result states why GPU1 or GPU0 was selected.

## Stop Conditions

- Trusted GPU status cannot be obtained.
- No GPU is usable by the predeclared threshold rule.
- Both GPUs are busy/unsuitable by threshold and user direction is needed.
- The user must decide between competing GPU workloads.

## End-Of-Phase Actions

1. Run required trusted GPU preflight.
2. Write the P02 result/close record.
3. Draft or refresh the P03 subplan with selected GPU metadata.
4. Review the P03 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
