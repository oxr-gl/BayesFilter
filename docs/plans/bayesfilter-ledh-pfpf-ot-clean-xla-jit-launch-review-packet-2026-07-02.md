# Clean XLA JIT Launch Review Packet

Date: 2026-07-02

Role contract: Codex is supervisor/executor.  Claude is read-only reviewer
only.

Review paths:

- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-master-program-2026-07-02.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase0-inventory-target-freeze-subplan-2026-07-02.md`
- This packet.

Objective: launch a governed program to repair the corrected LEDH-PFPF-OT full
total-derivative route so GPU/XLA JIT receives TensorFlow loop structure rather
than giant Python-unrolled graphs.

Plain scientific target:

- Current route passed a 2026-07-01 same-scalar raw-direction FD gate.
- Current route still has compiler hygiene problems.
- "XLA compiled" is not enough; clean XLA requires loop representation and
  tests that detect Python-unrolled compiled-path code.
- Stopped partial derivatives must not be called scores.

Phase 0 scope:

- Inventory only.
- No implementation edits.
- No long GPU runs.
- Must identify concrete file/line surfaces for:
  - time-scan Python unrolling;
  - reverse-scan Python unrolling;
  - Python tensor record lists;
  - seed-loop randomness inside JIT;
  - RK4 forward/reverse Python substep loops;
  - streaming Sinkhorn finite-step Python loops;
  - score-bearing stop-gradient risks.

Primary question for Claude:

Is this a valid launch and Phase 0 plan before implementation, or does it have
a material flaw in baseline, evidence contract, stop conditions, artifact
coverage, boundary safety, or plain scientific wording?

Required verdict ending:

`VERDICT: AGREE` or `VERDICT: REVISE`
