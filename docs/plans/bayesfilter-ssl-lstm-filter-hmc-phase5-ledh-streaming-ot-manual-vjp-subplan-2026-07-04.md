# Phase 5 Subplan: LEDH Streaming-OT Manual VJP Adapter

Date: 2026-07-04

Status: `BLOCKED_MANUAL_VJP_IMPL_UNAVAILABLE`

## Phase Objective

Build or repair the LEDH streaming-OT adapter so the target gradient uses a
manual VJP path through the streaming transport operations, not ordinary
automatic differentiation through the transport solve.

## Entry Conditions Inherited From Previous Phase

- Phase 2 protocol is active.
- SGQF/UKF status has been recorded without changing shared benchmark
  criteria.
- Phase 4 is blocked because the repository does not yet contain an SSL-LSTM
  Zhao-Cui adapter to wire; that blocker does not alter LEDH planning.
- LEDH remains a candidate filter under the same SSL-LSTM benchmark.
- The current LEDH streaming value/score helper still uses a
  `tf.GradientTape` wrapper rather than a manual VJP path, so the requested
  target gradient route is not yet implemented.

## Required Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase5-ledh-streaming-ot-manual-vjp-result-2026-07-04.md`
- Source/code inventory of current LEDH streaming-OT value/score paths.
- Manual VJP design note that identifies primal intermediates, cotangent flow,
  chunking/streaming state, and finite-memory artifact fields.
- Code/tests for manual VJP adapter or a blocker result if current transport
  internals cannot support it.
- Value/score and VJP diagnostic JSON artifacts on tiny SSL-LSTM fixtures.
- Refreshed Phase 6 subplan.

## Required Checks, Tests, And Reviews

- Verify the target path does not rely on GradientTape through the transport
  solve as final evidence.
- Compare manual VJP against finite differences on tiny deterministic fixtures.
- Run chunking/streaming invariance checks where applicable.
- Run non-finite and zero-gradient connectivity checks.
- Claude read-only review for VJP topology, boundary safety, and claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can LEDH streaming OT expose a deterministic manual-VJP value/score adapter for SSL-LSTM? |
| Baseline/comparator | Phase 2 protocol and existing LEDH streaming code inventory; finite differences are independent diagnostics only. |
| Primary pass criterion | Manual VJP adapter passes contract tests, finite-difference diagnostics, and streaming/chunking checks on tiny fixtures. |
| Veto diagnostics | Target path uses ordinary autodiff through transport solve, non-finite VJP, chunking mismatch beyond tolerance, disconnected cotangent, or missing artifact metadata. |
| Explanatory diagnostics | Runtime, memory/chunk counts, transport residuals, score residuals, and compile mode. |
| Not concluded | Dense Sinkhorn equivalence, posterior correctness, HMC success, or method ranking. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase5-ledh-streaming-ot-manual-vjp-result-2026-07-04.md` |

## Forbidden Claims And Actions

- Do not use existing GradientTape score helpers as final target evidence.
- Do not claim streaming OT correctness from value-only checks.
- Do not treat the Phase 4 Zhao-Cui blocker as a blocker for LEDH work.
- Do not demote the shared benchmark or use a different SSL-LSTM fixture only
  for LEDH unless the difference is declared as a blocker.
- Do not run long HMC chains in this phase.
- Do not change default production policy.

## Exact Next-Phase Handoff Conditions

Phase 6 may start only when:

- each candidate filter has status: admitted, failed with reason, or blocked
  with exact blocker;
- LEDH manual VJP evidence or blocker is recorded;
- all admitted adapters satisfy the Phase 2 artifact schema;
- Phase 6 subplan is refreshed for the shared benchmark runner.

## Stop Conditions

- Manual VJP cannot be specified without a larger transport-core redesign.
- Current streaming internals do not expose required intermediates and the fix
  requires a human-approved scope change.
- Finite-difference diagnostics are inconclusive because fixtures are ill-posed.
- Claude and Codex do not converge on VJP boundary safety after five rounds.

## End-Of-Phase Protocol

1. Run manual-VJP, chunking, and value/score checks.
2. Write the Phase 5 result/close record.
3. Draft or refresh the Phase 6 subplan.
4. Review Phase 6 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
