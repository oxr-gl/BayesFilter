# LEDH-PFPF-OT Streaming Manual VJP Master Program

status: DRAFT_FOR_CLAUDE_REVIEW
date: 2026-06-23
supervisor_executor: Codex
readonly_reviewer: Claude Opus max effort, bounded exact-path review only

## Objective

Build, verify, and hand off a true streaming/blockwise manual VJP route for
LEDH-PFPF-OT transport gradients.  The target is to replace the current
streaming custom-gradient backward pass that replays the streaming value under
`tf.GradientTape` with a hand-coded blockwise VJP whose memory exposure is
controlled by row and column chunks.

The program exists because P82 stopped at `N=10000` when the current
`manual_streaming_finite_sinkhorn_stopped_scale_keys` route failed on GPU memory
during reverse-gradient replay.  The earlier dense manual VJP route proved the
adjoint idea on tiny dense programs, but it materializes dense `[B,N,N]` objects
and cannot be the large-particle route.

## Standing Evidence Contract

| Field | Contract |
|---|---|
| Engineering question | Can we implement a streaming/blockwise LEDH-PFPF-OT manual VJP that avoids both dense `[B,N,N]` retained transport matrices and `GradientTape` replay inside the streaming transport backward pass? |
| Comparator | Tiny dense manual VJP and tiny TensorFlow autodiff only as diagnostic oracles; P82 FD remains downstream and cannot run until the actual-gradient side passes. |
| Primary pass criterion | The new route passes primitive block-VJP parity, end-to-end dense-vs-streaming gradient parity on tiny fixtures, source scans proving no streaming-backward `GradientTape`, CPU-hidden focused tests, then reviewed GPU memory rungs through `N=10000`. |
| Veto diagnostics | Any `GradientTape` in the new streaming custom-gradient backward path; hidden dense `[B,N,N]` materialization in the large-N route; missing stopped-scale/key contract; nonfinite values or gradients; unsupported mode accepted; P82 FD launched before valid actual-gradient artifact. |
| Explanatory diagnostics | Block parity errors, padding/exact-chunk differences, runtime, memory, allocator behavior, device placement, MCSE, and review notes. |
| Not concluded | Posterior correctness, HMC/NUTS readiness, default-gradient readiness, production readiness, scientific superiority, Zhao-Cui source-faithfulness, or FD agreement unless later gates explicitly establish them. |
| Artifacts | This master program, phase subplans/results, visible runbook, execution ledger, review ledger, stop handoff, implementation diffs, tests, JSON result artifacts, and GPU logs when run. |

## Program Artifacts

- Visible execution runbook:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-gated-execution-runbook-2026-06-23.md`
- Claude review ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-claude-review-ledger-2026-06-23.md`
- Visible execution ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-execution-ledger-2026-06-23.md`
- Visible stop handoff:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-stop-handoff-2026-06-23.md`

The runbook must define the role contract, phase index, evidence contract,
default/assumption audit, skeptical plan audit, visible state machine,
one-exact-path Claude review protocol, human-required stop conditions, and final
handoff requirements.  It is an execution-control artifact, not authority to
change scientific criteria, default policy, GPU boundaries, or P82 FD entry
conditions.

## Forbidden Claims And Actions

- Do not rerun or reintroduce `transport_ad_mode=full` as a governed
  `N=10000` route.
- Do not use Zhao-Cui as the active comparator for this program.
- Do not treat autodiff as an oracle except for tiny diagnostic parity checks.
- Do not launch P82 FD comparison until a valid `N=10000` actual-gradient
  artifact exists for the new route.
- Do not claim memory success from tiny parity tests.
- Do not expose the new route as a default or public production route.
- Do not change default policy, HMC policy, funding/model boundaries, or
  scientific claims.
- Do not revert unrelated dirty worktree changes.

## Phase Ladder

| Phase | Objective | Subplan | Required result |
|---|---|---|---|
| S0 | Governance, inventory, and route boundary lock. | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase0-governance-inventory-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase0-governance-inventory-result-2026-06-23.md` |
| S1 | Derive the streaming/blockwise VJP contracts for softmin, transport from potentials, and finite Sinkhorn recursion. | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase1-derivation-contract-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase1-derivation-contract-result-2026-06-23.md` |
| S2 | Implement and test blockwise softmin VJP. | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase2-softmin-vjp-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase2-softmin-vjp-result-2026-06-23.md` |
| S3 | Implement and test blockwise transport-from-potentials VJP. | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase3-transport-vjp-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase3-transport-vjp-result-2026-06-23.md` |
| S4 | Implement and test streaming finite Sinkhorn recursion VJP. | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase4-sinkhorn-recursion-vjp-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase4-sinkhorn-recursion-vjp-result-2026-06-23.md` |
| S5 | Wire a new opt-in streaming manual VJP route and remove `GradientTape` replay from that route. | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase5-custom-gradient-wiring-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase5-custom-gradient-wiring-result-2026-06-23.md` |
| S6 | Run local parity, padding, source-scan, and tiny filter-loop tests. | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase6-local-parity-ladder-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase6-local-parity-ladder-result-2026-06-23.md` |
| S7 | Run trusted GPU memory/feasibility ladder through `N=10000`. | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-gpu-memory-ladder-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-gpu-memory-ladder-result-2026-06-23.md` |
| S8 | Prepare P82 return handoff and exact FD-gated next steps. | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase8-p82-handoff-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase8-p82-handoff-result-2026-06-23.md` |
| S9 | Closeout code-doc audit and final stop handoff. | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase9-closeout-subplan-2026-06-23.md` | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase9-closeout-result-2026-06-23.md` |

S7 is the critical memory-feasibility gate.  If any trusted GPU rung fails,
OOMs, writes no JSON artifact, records nonfinite required outputs, or records
the wrong route metadata, the program must write an S7 blocker result and stop
or proceed only to S9 blocker closeout.  The S7 failure path must also update
the visible stop handoff with the failure status, blocking reason, artifact
paths, and explicit prohibition on S8/P82 advancement.  A failed S7 cannot
advance to S8/P82 handoff.

## Subplan Contract

Every phase subplan must state:

- phase objective;
- entry conditions inherited from the previous phase;
- required artifacts;
- required checks/tests/reviews;
- evidence contract;
- forbidden claims/actions;
- exact next-phase handoff conditions;
- stop conditions.

At the end of each executed phase, Codex must:

1. run the required local checks;
2. write a phase result or blocker result;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.

## Review Loop

Claude may be used as a read-only reviewer for material subplans and phase
results.  Claude is not an execution authority and cannot authorize crossing
human, runtime, model-file, funding, product-capability, GPU, default-policy, or
scientific-claim boundaries.

Use the `memory.md` one-path pattern:

```text
READ-ONLY BOUNDED REVIEW. Review exactly this path and nothing else unless the
file itself explicitly asks you to inspect a cited line: <one path>. Do not
edit, run commands, launch agents, or review the whole repo. Question: <one
question>. End with VERDICT: AGREE or VERDICT: REVISE.
```

If Claude does not respond, run a tiny read-only probe.  If the probe responds,
redesign the prompt.  If review finds a fixable problem, patch the same
subplan/result visibly, rerun focused checks, and repeat review.  Stop after
five Claude review rounds for the same blocker and write a blocker result.

## Launch Boundary

After this master program and visible runbook pass review, execution starts at
S0.  Implementation changes are not authorized until S1 closes with a reviewed
derivation contract and S2 entry conditions are satisfied.  GPU commands are not
authorized until S7, and must use trusted/escalated execution.
