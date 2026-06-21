# P01 Harness Implementation And Static Checks Subplan

Date: 2026-06-21

Status: DRAFT_FOR_REVIEW

## Phase Objective

Create a compact parent benchmark wrapper that runs the existing streaming
LGSSM harness across particle-count rungs and precision arms in fresh
processes, preserves child JSON/Markdown artifacts, and emits a concise
large-particle efficiency summary without flooding stdout.

## Entry Conditions Inherited From Previous Phase

- P00 governance passed.
- The evidence contract, nonclaims, GPU policy, and phase index are locked.
- Claude/Codex review found no unresolved material plan issue.

## Required Artifacts

- New or refreshed wrapper:
  `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_large_particle_efficiency.py`
- New or refreshed test in:
  `tests/test_experimental_batched_benchmark_harness.py`
- P01 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p01-harness-result-2026-06-21.md`
- Refreshed P02 subplan if implementation changes the GPU-selection surface.

## Required Checks, Tests, And Reviews

- `python -m py_compile docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_large_particle_efficiency.py`
- `pytest -q tests/test_experimental_batched_benchmark_harness.py -k large_particle_efficiency`
  after adding a focused test whose function name contains
  `large_particle_efficiency`.
- Static source/content checks that the wrapper:
  - calls `benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`;
  - runs child processes rather than importing TensorFlow repeatedly in-process;
  - captures child stdout/stderr tails;
  - checks `finite_output`;
  - checks GPU placement when GPU is requested;
  - checks `transport.dense_transport_matrix_materialized is False`;
  - checks `stores_full_pre_flow_particles is False`;
  - checks `return_history is False`;
  - records physical GPU selection metadata supplied by P02 in the parent
    wrapper artifact;
  - marks runtime and memory as descriptive.
- Claude read-only review only if the wrapper materially changes claim
  boundaries or baseline definitions.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the parent wrapper correctly preserve the evidence needed to run large-`N` streaming TF32/FP32 tests without introducing a misleading comparator or artifact gap? |
| Baseline/comparator | The wrapper delegates to the existing streaming LGSSM harness; it does not implement algorithm math itself. |
| Primary criterion | Static and tiny CPU tests pass; wrapper hard-screen logic catches finite/device/storage/history/default-metadata failures, and the focused test is selected by the documented `-k large_particle_efficiency` command. |
| Veto diagnostics | Missing artifact path, stdout flood, in-process TensorFlow arm reuse, missing invariant check, wrong child harness, or claim text that upgrades runtime to statistical superiority. |
| Explanatory diagnostics | Tiny CPU output values and child stderr tails. |
| Not concluded | No GPU viability, no large-`N` pass, no TF32 benefit, no posterior correctness. |
| Artifact | P01 result plus wrapper/test files. |

## Forbidden Claims Or Actions

- Do not run large GPU ladders in P01.
- Do not add new algorithmic implementation paths.
- Do not use NumPy as a BayesFilter-owned algorithmic backend; NumPy is allowed
  only for reporting and artifact parsing in the wrapper.
- Do not modify unrelated HMC, low-rank, or peer-agent files.

## Exact Next-Phase Handoff Conditions

Advance to P02 only if:

- wrapper compiles;
- focused test passes;
- wrapper hard-screen logic is present;
- P01 result records changed files, checks, residual risks, and nonclaims;
- P02 subplan remains consistent with wrapper CLI.

## Stop Conditions

- Wrapper cannot run the existing streaming harness in fresh processes.
- Static or focused tests fail for a reason not repaired in five review rounds.
- Implementing the wrapper would require changing the filter algorithm itself.

## End-Of-Phase Actions

1. Run required local checks.
2. Write the P01 result/close record.
3. Draft or refresh the P02 subplan.
4. Review the P02 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
