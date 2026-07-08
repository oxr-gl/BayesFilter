# Manual Adjoint Phase 6 Subplan: Streaming/Chunked Memory Route

status: DRAFT_READY_AFTER_M5_REVIEW
date: 2026-06-22
phase: M6-STREAMING-MEMORY

## Phase Objective

Implement or reject a streaming/chunked manual-adjoint route based on bounded
memory/runtime evidence.  This phase is the first one allowed to make a
measured memory-feasibility statement, and only for the tested route.

## Entry Conditions

- M5 opt-in tiny integration/smoke passes and review converges.
- M5 records the remaining memory bottleneck and the streaming/chunked design
  question.
- M4 memory ledger is still valid or has been updated.
- The dense opt-in route remains explicitly non-memory-disciplined.

## Required Artifacts

- Streaming/chunked implementation diff, or a blocker result rejecting the
  route.
- Focused tests for dense-vs-streaming parity on small cases.
- Runtime/memory diagnostics.
- Phase 6 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase6-streaming-memory-route-result-2026-06-22.md`
- Refreshed M7 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase7-p82-validation-handoff-subplan-2026-06-22.md`

## Required Checks / Tests / Reviews

- Dense-vs-streaming value/gradient parity on small cases.
- Shape/finite-value tests across chunk sizes.
- Bounded runtime/memory ladder, starting small before any large case.
- Explicit stop/reject result if the streaming route cannot preserve the M3/M5
  stopped-key scalar without dense `[B,N,N]` memory.
- Trusted GPU only for commands that initialize/use GPU.
- `python -m py_compile` for edited Python files.
- `git diff --check`.
- Claude read-only review of memory claims and route boundaries.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does a streaming/chunked manual-adjoint route preserve small-case parity while materially reducing memory pressure enough to justify P82 handoff preparation? |
| Baseline/comparator | M5 opt-in dense route, M3/M5 stopped-key scalar, dense-vs-streaming parity tests, and bounded memory/runtime ladder. |
| Primary criterion | Streaming/chunked route passes parity and finite checks, records memory/runtime evidence, and avoids raw full-AD N10000.  If not, write a blocker and do not proceed to P82 handoff. |
| Veto diagnostics | Parity failure; nonfinite gradients; memory near device ceiling with no progress; unsupported mode accepted; missing GPU trust context; overclaiming untested sizes. |
| Explanatory diagnostics | Chunk sizes, peak memory/proxy memory, runtime, device placement, gradient deltas, and residuals. |
| Not concluded | No P82 FD agreement, no HMC/default/posterior readiness, no production readiness. |

## Forbidden Claims / Actions

- Do not claim general streaming memory improvement beyond tested cases.
- Do not run the full P82 validation unless M7 authorizes it.
- Do not change defaults.
- Do not hide OOM/unbounded-runtime failures as inconclusive successes.

## Next-Phase Handoff Conditions

M7 may proceed only if M6 records:

- supported streaming/chunked route and settings;
- dense-vs-streaming parity evidence;
- memory/runtime evidence sufficient to plan N10000 actual-gradient gate;
- exact remaining risks and stop conditions for P82 return.

## Stop Conditions

Stop if streaming parity fails, if memory remains infeasible, if trusted GPU
evidence is unavailable for GPU claims, or if the route requires a different
scientific scalar than the one P82 intends to validate.

Stop and write a blocker if the only available route still materializes dense
`[B,N,N]` transport/cost/state at the intended scale.  Do not treat the M5
dense opt-in route as a memory solution.
