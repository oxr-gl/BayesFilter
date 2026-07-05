# Phase 4 Subplan: Manual Scan Hygiene

Date: 2026-07-02

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Phase Objective

Replace the P8p SIR manual score route's Python forward/reverse time scans and
Python `records` list with TensorFlow loop state. This phase targets only
`_manual_value_and_score_from_components` in
`docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`.

The target audit rows are:

- `SIR-MANUAL-TIME-STATIC`;
- `SIR-MANUAL-RECORD-LIST`;
- `SIR-MANUAL-FWD-RANGE`;
- `SIR-MANUAL-REV-REVERSED`.

## Entry Conditions Inherited From Previous Phase

- Phase 2 removed the manual process-noise seed loop.
- Phase 3 removed RK4 Python aux list and reverse substep loop findings.
- The route still correctly reports `FAIL_CURRENT_ROUTE` due to manual
  time-scan and Sinkhorn findings.

## Required Artifacts

- Implementation changes scoped to:
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- Test updates scoped to:
  `tests/test_audit_ledh_clean_xla.py`
- Updated static audit artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-static-audit-2026-07-02.json`
- Phase 4 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-manual-scan-hygiene-result-2026-07-02.md`
- Draft Phase 5 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-streaming-sinkhorn-loop-hygiene-subplan-2026-07-02.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-visible-execution-ledger-2026-07-02.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-claude-review-ledger-2026-07-02.md`

## Required Checks, Tests, Reviews

Before implementation:

- Codex skeptical audit of this subplan.
- Claude read-only review of the Phase 3 result and this Phase 4 subplan.

After implementation:

- `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py --format json --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-static-audit-2026-07-02.json`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`
- Focused same-input parity test comparing the old Python-record manual route
  semantics against the new TensorFlow-loop route on a tiny deterministic
  problem. If the old route is replaced in place, preserve a test-local
  independent reference or a frozen fixture before editing.
- Nearby existing static checks used in earlier phases.
- Claude read-only review of the Phase 4 result before Phase 5 execution.

GPU/XLA runtime and HLO checks are not required in Phase 4.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the manual score route's time recursion and reverse recursion be represented with TensorFlow loop state without changing the same-scalar value/score on a focused deterministic fixture? |
| Baseline/comparator | The pre-Phase-4 manual route semantics on the same tensors, theta, fixed noise, and fixed masks, preserved by a test-local reference or frozen fixture. |
| Primary pass criterion | Static audit reports the four manual-scan rows as absent/clean; focused same-input parity passes for log likelihood and score; remaining Sinkhorn findings remain visible. |
| Veto diagnostics | Value or score parity fails; Python `records` list, `range(time_steps)`, or `reversed(records)` remains; process-noise or RK4 findings regress; Sinkhorn findings disappear without Phase 5 work; implementation changes score definition or finite-difference criteria. |
| Explanatory diagnostics | Updated audit counts, parity max absolute differences, source line anchors, and remaining Sinkhorn finding IDs. |
| Not concluded | No Sinkhorn cleanup, no HLO evidence, no GPU runtime evidence, no full FD ladder rerun, no clean-XLA claim. |
| Artifact | Phase 4 result markdown and Phase 4 static audit JSON. |

## Implementation Details

Use `tf.while_loop` for the manual route forward time scan and store required
forward-pass values in `TensorArray` or tensor loop state. Use a reverse
`tf.while_loop` for the adjoint scan.

The implementation must keep the existing mathematical target:

- same finite Sinkhorn transport helper calls;
- same fixed transition noise tensor from Phase 2;
- same RK4 transition helper from Phase 3;
- same log-weight normalization and VJP primitives;
- same score component accounting unless a parity test proves exact agreement.

Do not change Sinkhorn helper internals in this phase. The expected audit
decision after Phase 4 remains `FAIL_CURRENT_ROUTE`, because Sinkhorn findings
remain.

## Forbidden Claims And Actions

- Do not claim clean XLA after Phase 4.
- Do not edit Sinkhorn helper loops or stopped-key routes in this phase.
- Do not change finite-difference tolerances, score definitions, or gradient
  acceptance rules.
- Do not call stopped partial derivatives scores.
- Do not run long GPU jobs or HLO metrics in Phase 4.

## Exact Next-Phase Handoff Conditions

Phase 4 may hand off to Phase 5 only if:

- manual forward and reverse time scans use TensorFlow loop state;
- the four manual-scan static audit rows are absent/clean;
- focused value/score parity passes;
- route still reports `FAIL_CURRENT_ROUTE` due to remaining Sinkhorn findings;
- Phase 4 result and Phase 5 subplan exist;
- Claude read-only review returns `VERDICT: AGREE`, or fixable findings are
  patched and rereviewed.

## Stop Conditions

Stop and write a blocker result if:

- focused value/score parity fails;
- TensorFlow loop state cannot preserve required record values;
- changes spill into Sinkhorn refactors;
- tests require GPU, network, package installation, or unrelated file changes;
- Claude and Codex do not converge after five rounds.

## Skeptical Pre-Execution Audit

Result: `PASS_PENDING_CLAUDE_REVIEW`

- Wrong baseline: avoided by requiring a pre-Phase-4 same-input manual-route
  comparator.
- Proxy promotion: avoided because Phase 4 removes manual scan Python surfaces
  only and cannot claim clean XLA.
- Missing stop conditions: explicit above.
- Unfair comparison: parity must use the same tensors, theta, fixed noise, and
  fixed masks.
- Hidden assumption: the plan states the expected audit decision remains
  `FAIL_CURRENT_ROUTE`.
- Environment mismatch: CPU-hidden static/local parity checks only; GPU evidence
  is deferred.
- Artifact mismatch: Phase 4 result must include updated audit JSON and
  same-input parity evidence.
