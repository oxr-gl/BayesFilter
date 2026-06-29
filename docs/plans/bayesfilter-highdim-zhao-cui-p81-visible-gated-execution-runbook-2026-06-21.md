# P81 Visible Gated Execution Runbook

status: BLOCKED_PENDING_LANE_DIRECTION
date: 2026-06-21

## Governance

Codex is supervisor and executor.  Claude Opus may review bounded packets as a
read-only reviewer.  Claude is not an execution authority and cannot authorize
human, runtime, GPU, model-file, funding, product-capability, or scientific
claim boundary crossings.

Local code edits, docs/plans writes, bounded source/code/doc reads, focused
CPU-hidden checks, and Claude read-only review are allowed under this runbook.
GPU/CUDA/NVIDIA commands must be run with trusted/escalated permissions per
local policy.  No package installs, network fetches, detached agents,
destructive git/filesystem actions, default-policy changes, or large benchmark
escalations are allowed without separate approval.

## Phase Protocol

For every phase:

1. Draft or refresh the dedicated subplan before execution.
2. Run the skeptical plan audit before any non-trivial command.
3. Execute only the artifacts and commands allowed by the subplan.
4. Run required local checks.
5. Write a phase result or blocker close record.
6. Draft or refresh the next subplan.
7. Review the result/next-subplan packet with Claude until convergence or five
   rounds for the same blocker.
8. Continue only if the gate status is reviewed as ready.

## Current Gate

Phase 12 read-only audit blocked direct continuation.  The repo has symbolic
TT-MPO/operator route language and local-factor tiny tie-out, but no
sufficiently defined compressed transition operator, hybrid retained-TT
contraction, approximation/error contract, or theta-derivative equation set for
implementation.  P81 should stop pending a human lane decision: deterministic
TT-MPO/hybrid derivation as `extension_or_invention`, or source-faithful fixed
TTSIRT retained-object route.

## Stop Conditions

Stop and write a blocker result if:

- same-branch finite differences drift branch hashes;
- score/value outputs are nonfinite;
- the current code requires a global default change to pass;
- Phase 3 cannot remain horizon-0 bounded;
- Claude finds a material issue that does not converge after five rounds;
- any GPU/large-run boundary is needed before a reviewed Phase 4 subplan.
