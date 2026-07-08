# Phase 3 Subplan: RK4 Loop Hygiene

Date: 2026-07-02

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Phase Objective

Replace the P8p SIR RK4 forward aux list and reverse `reversed(aux)` loop with
TensorFlow loop state. This phase targets only:

- `_sir_transition_mean_with_aux_tf`;
- `_sir_transition_mean_vjp_tf`.

It should make the Phase 1 audit rows `SIR-RK4-FWD-LIST`,
`SIR-RK4-FWD-RANGE`, and `SIR-RK4-REV-REVERSED` disappear or become
`ABSENT_CLEAN_OR_MOVED`.

## Entry Conditions Inherited From Previous Phase

- Phase 1 static audit exists and detects current unclean surfaces.
- Phase 2 removed the manual process-noise seed loop while preserving the old
  stateless seed policy.
- The route still correctly reports `FAIL_CURRENT_ROUTE`.

## Required Artifacts

- Implementation changes scoped to:
  `docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`
- Test updates scoped to:
  `tests/test_audit_ledh_clean_xla.py`
- Updated static audit artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-static-audit-2026-07-02.json`
- Phase 3 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-rk4-loop-hygiene-result-2026-07-02.md`
- Draft Phase 4 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase4-manual-scan-hygiene-subplan-2026-07-02.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-visible-execution-ledger-2026-07-02.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-claude-review-ledger-2026-07-02.md`

## Required Checks, Tests, Reviews

Before implementation:

- Codex skeptical audit of this subplan.
- Claude read-only review of the Phase 2 result and this Phase 3 subplan.

After implementation:

- `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py --format json --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase3-static-audit-2026-07-02.json`
- `CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_audit_ledh_clean_xla.py`
- A focused RK4 parity test comparing the edited TensorFlow-loop implementation
  against an independent reference implementation on a small deterministic
  tensor. The reference must be test-local or otherwise outside the edited
  production symbols.
- A focused VJP parity test comparing `_sir_transition_mean_vjp_tf` against
  gradients from a local `tf.GradientTape` applied to the independent reference
  forward map.
- Aux-output parity for the tensors required by the reverse pass, not just
  primal-state parity.
- Nearby existing static checks used in Phases 1 and 2.
- Claude read-only review of the Phase 3 result before Phase 4 execution.

GPU/XLA runtime checks are not required in Phase 3.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can RK4 forward aux capture and reverse VJP be represented with TensorFlow loop state without changing the local RK4 transition/VJP semantics? |
| Baseline/comparator | Current RK4 forward computation and manual VJP algebra in `_sir_transition_mean_with_aux_tf` / `_sir_transition_mean_vjp_tf`. |
| Primary pass criterion | Static audit reports `SIR-RK4-FWD-LIST`, `SIR-RK4-FWD-RANGE`, and `SIR-RK4-REV-REVERSED` as absent/clean; focused RK4 primal, aux, and VJP parity tests pass against an independent reference; remaining unclean classes remain visible. |
| Veto diagnostics | RK4 forward value changes versus the independent reference; required aux tensors differ from the independent reference; VJP parity versus tape on the independent reference fails; Python aux list or `reversed(aux)` remains; implementation spills into manual time scan, Sinkhorn, or unrelated score logic; static audit loses remaining required findings. |
| Explanatory diagnostics | Updated audit counts, focused RK4/VJP max absolute differences, source line anchors. |
| Not concluded | No manual time-scan cleanup, no Sinkhorn cleanup, no HLO evidence, no full FD rerun, no clean-XLA claim. |
| Artifact | Phase 3 result markdown and Phase 3 static audit JSON. |

## Implementation Details

Refactor `_sir_transition_mean_with_aux_tf` to use `tf.while_loop` for RK4
substeps and save per-substep tensors in `tf.TensorArray` or stacked tensors.
The returned aux object should be a dictionary of tensors or TensorArrays whose
first dimension is the substep index.

Refactor `_sir_transition_mean_vjp_tf` to use a reverse `tf.while_loop` over
the substep dimension. The reverse loop should reproduce the same algebra as
the current Python `for record in reversed(aux)` implementation.

Add a focused test-local independent reference for RK4. This reference may use
plain Python loops and Python lists because it is a CPU-hidden comparison oracle,
not the compiled route. It must not call the edited `_sir_transition_mean_with_aux_tf`
or `_sir_transition_mean_vjp_tf` symbols. The VJP comparator should use
`tf.GradientTape` on this independent reference forward map and compare
gradients with respect to points, kappa, and nu.

Do not change:

- the RK4 formula;
- `_sir_rhs_tf` or `_sir_rhs_vjp_tf` algebra;
- process-noise tensorization from Phase 2;
- manual time scan structure;
- Sinkhorn helper logic.

Scope guard: implementation edits in Phase 3 are limited to the two named
benchmark symbols, the focused RK4 tests, the static audit/test expectation
updates needed to reflect removed RK4 findings, and phase artifacts. Any edit
outside those surfaces must stop for review.

The expected audit decision after Phase 3 remains `FAIL_CURRENT_ROUTE`, because
manual time-scan and Sinkhorn findings remain.

## Forbidden Claims And Actions

- Do not claim clean XLA after Phase 3.
- Do not edit manual forward/reverse time scans or Sinkhorn loops in this
  phase.
- Do not change finite-difference tolerances, score definitions, or gradient
  acceptance rules.
- Do not call stopped partial derivatives scores.
- Do not run long GPU jobs or HLO metrics in Phase 3.

## Exact Next-Phase Handoff Conditions

Phase 3 may hand off to Phase 4 only if:

- RK4 forward and VJP use TensorFlow loop state;
- RK4 static audit rows are absent/clean;
- focused RK4 value/VJP parity passes;
- route still reports `FAIL_CURRENT_ROUTE` due to remaining non-RK4 findings;
- Phase 3 result and Phase 4 subplan exist;
- Claude read-only review returns `VERDICT: AGREE`, or fixable findings are
  patched and rereviewed.

## Stop Conditions

Stop and write a blocker result if:

- RK4 value or VJP parity fails;
- TensorFlow loop state cannot preserve the existing aux values;
- changes spill into time-scan or Sinkhorn refactors;
- tests require GPU, network, package installation, or unrelated file changes;
- Claude and Codex do not converge after five rounds.

## Skeptical Pre-Execution Audit

Result: `PASS_PENDING_CLAUDE_REVIEW`

- Wrong baseline: avoided by comparing to the local RK4 value/VJP semantics.
- Proxy promotion: avoided because Phase 3 removes only RK4 Python-loop
  surfaces and cannot claim clean XLA.
- Missing stop conditions: explicit above.
- Unfair comparison: focused RK4 parity compares the same local map and VJP.
- Hidden assumption: the plan states the expected audit decision remains
  `FAIL_CURRENT_ROUTE`.
- Environment mismatch: CPU-hidden static/local parity checks only; GPU evidence
  is deferred.
- Artifact mismatch: Phase 3 result must include updated audit JSON and RK4
  parity evidence.
