# Phase 3 Subplan - Two-GPU Row Splitting - 2026-06-16

## Phase Objective

Create or verify a launcher that splits independent DPF value-evaluation rows,
chains, or seeds across GPU 0 and GPU 1.

This phase does not shard a single filter's particles across GPUs and does not
design distributed OT.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result records `PHASE_0_PASSED`.
- Phase 1 result records `PHASE_1_PASSED`.
- Phase 2 result records `PHASE_2_PASSED`.
- Single-GPU TF32 streaming value artifact exists and passed finite/JIT/GPU
  metadata checks.
- Worktree may be dirty; unrelated changes remain protected.

## Required Artifacts

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p3-two-gpu-row-splitting-result-2026-06-16.md`
- Updated execution ledger entry for Phase 3.
- New or updated opt-in two-GPU row-splitting launcher artifact, if needed.
- Per-GPU JSON/Markdown artifacts for bounded independent-row runs.
- An aggregate JSON/Markdown result that records row assignment and verifies
  no claim of particle-cloud sharding.
- Draft or refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p4-jit-safe-score-path-subplan-2026-06-16.md`

## Required Checks, Tests, And Reviews

Local checks:

1. Verify at least two GPUs are visible in trusted context before attempting
   two-GPU execution.
2. Use the Phase 2 single-GPU value runner as the per-device worker.
3. Split independent batch rows, chains, or seeds into disjoint per-GPU
   assignments.
4. Verify each per-GPU artifact is finite, JIT-compiled, device-placed on the
   requested GPU, and records TF32 metadata.
5. Verify the aggregate artifact records row assignment and explicitly states
   that no single particle cloud was sharded.

Review:

- Use Claude read-only review if a new launcher is implemented or if aggregate
  semantics differ from simple independent row splitting.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can independent DPF value-evaluation rows be split across two GPUs using the current streaming TF32 value worker? |
| Baseline/comparator | Phase 2 single-GPU TF32 value artifact and the same streaming benchmark harness run independently per GPU. |
| Primary pass criterion | Two per-GPU artifacts exist, are finite, JIT-compiled, correctly device-placed, and the aggregate records disjoint independent-row assignments. |
| Veto diagnostics | Fewer than two trusted GPUs visible; wrong device placement; non-finite value; missing JIT/precision metadata; row assignment overlap; any claim of particle-cloud sharding; score/HMC claim; production/public API claim. |
| Explanatory diagnostics | Per-GPU compile time, warm-call time, GPU memory metadata, and aggregate wall time. |
| Not concluded | No single-filter distributed OT, no speed superiority, no HMC readiness, no production default, no public API readiness. |
| Artifact preserving result | Phase 3 result plus per-GPU and aggregate JSON/Markdown artifacts. |

## Skeptical Audit Before Execution

Before running Phase 3 commands, check:

- wrong baseline: compare against Phase 2 single-GPU value worker, not HMC;
- proxy metric risk: timing is explanatory only;
- missing stop condition: wrong device, missing second GPU, overlap, or
  missing metadata must stop Phase 3 passage;
- unfair comparison: no speed ranking without a later comparison contract;
- hidden assumption: row splitting means independent rows, chains, or seeds;
- stale context: reconfirm GPU visibility in trusted context;
- environment mismatch: all GPU results require trusted context;
- artifact adequacy: aggregate must preserve row/device assignment.

## Forbidden Claims And Actions

- Do not claim one filter's particles are sharded across two GPUs.
- Do not implement distributed OT in this phase.
- Do not claim speed superiority from one bounded run.
- Do not claim score/HMC readiness.
- Do not change production defaults or public APIs.
- Do not modify unrelated dirty worktree files.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only after:

- Phase 3 result exists and records `PHASE_3_PASSED`;
- two trusted per-GPU artifacts exist and pass finite/JIT/device/precision
  metadata checks;
- aggregate artifact records disjoint independent row assignments;
- Phase 4 subplan exists and focuses on JIT-safe score-path repair;
- no human-required stop condition is active.

## Stop Conditions

Stop and write a blocker result if:

- fewer than two GPUs are visible in trusted context;
- per-GPU worker cannot be run without modifying unrelated files;
- device placement is wrong or ambiguous;
- artifacts omit required precision/JIT/device metadata;
- row assignment cannot be proven disjoint;
- continuing would require distributed OT, package installation, network fetch,
  credentials, destructive filesystem/git action, detached execution, or a
  production default change.
