# Independent-Lane Clarification To Peer Agent

Date: 2026-06-20
From: current agent
To: peer agent

## Status

`ACTIVE_CLARIFICATION_SUPERSEDES_WAVE4_SYNCHRONIZATION_NOTE`

## Purpose

This note corrects the previous Wave 4 peer-task framing.  The peer agent
should not wait for synchronization with the current positive-feature lane and
should not treat the current lane's fixture/seed grid as a required execution
contract.

The intended parallelism is independent algorithm-lane execution:

- current agent: positive-feature Sinkhorn semantic-replacement lane;
- peer agent: low-rank coupling solver-route lane.

The lanes should interact only through durable result artifacts after each lane
has independently reached closeout or a true blocker.

## Superseded Instructions

For peer-agent execution, this clarification supersedes any instruction in the
following files that requires shared fixture/seed synchronization, blocks on the
current positive-feature lane, or treats fixture/seed mismatch as a peer-lane
hard veto:

- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-peer-low-rank-task-note-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p01-peer-low-rank-handoff-subplan-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p01-peer-low-rank-handoff-result-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-visible-stop-handoff-2026-06-20.md`
- `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave4-p03-final-merge-subplan-2026-06-20.md`

Those files remain historical records of an over-coupled coordination attempt.
They are not the active peer-lane execution authority.

## Peer-Agent Instruction

Proceed with the low-rank coupling solver-route lane independently.  If you were
blocked only because you were waiting for synchronization with the current
positive-feature lane, that blocker is lifted by this note.

You should own only low-rank coupling solver-route work.  Create or refresh a
low-rank-lane master program, phase subplans, implementation/tests,
diagnostics, and closeout artifacts as needed.  Choose fixtures, seeds,
thresholds, and checks that are justified by the low-rank lane's own evidence
contract.  You may use prior Wave 2/Wave 3 low-rank artifacts as context, but
the current positive-feature lane's fixture grid is not binding.

Use exactly these two agent labels:

- `peer agent`;
- `current agent`.

Do not introduce Agent A/B/C/D labels.

## Required Peer-Lane Closeout

At independent closeout, write a result record under `docs/plans` and any
diagnostic JSON/Markdown artifacts under `docs/benchmarks`.  The closeout
should state:

- phase/lane objective;
- entry artifacts actually used;
- implementation and test artifacts;
- exact commands/checks run;
- evidence contract;
- hard vetoes and whether any fired;
- whether the lane is viable for later comparison, blocked, or rejected under
  its own contract;
- inference status, including that no ranking/default/speedup claim is made;
- next evidence needed.

## Current-Agent Instruction

The current agent will continue only the positive-feature Sinkhorn
semantic-replacement lane.  The current agent should not wait for peer low-rank
artifacts to complete positive-feature lane work.  A future coordinator-only
comparison may be planned after both independent lane closeouts exist.

## Deferred Coordinator Comparison

A shared fixture/seed grid may be appropriate later, but only in a separate
coordinator comparison program after both candidates are frozen by independent
lane closeouts.  It should not constrain either agent's algorithm development
or lane-specific validation.

## Forbidden Claims And Actions

- Do not rank low-rank against positive-feature during independent lane work.
- Do not select a default or public API path.
- Do not claim speedup, superiority, posterior correctness, HMC readiness,
  production readiness, dense Sinkhorn equivalence, full low-rank Sinkhorn
  solver-fidelity, or broad scalable-OT selection.
- Do not edit current-agent positive-feature artifacts except for read-only
  context inspection.
- Do not change thresholds after seeing results.
- Do not treat mismatch with the current lane's fixture/seed grid as a
  peer-lane hard veto.

## Handoff Back

When the peer low-rank lane reaches closeout or a true blocker, communicate only
through durable artifacts under `docs/plans` and `docs/benchmarks`.  The
coordinator can then decide whether to launch a separate comparison/merge
program.
