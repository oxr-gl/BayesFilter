# Phase 5 Subplan: Streaming Sinkhorn Loop Hygiene

Date: 2026-07-02

Status: `DRAFT_FOR_CLAUDE_REVIEW`

## Phase Objective

Replace the streaming finite Sinkhorn Python iteration loops and Python state
lists in the targeted helper symbols with TensorFlow loop state, while
preserving the current finite Sinkhorn values and VJPs on focused fixtures.

Target current-veto audit rows:

- `SINK-STOPPED-VALUE-RANGE`;
- `SINK-TOTAL-VALUE-RANGE`;
- `SINK-STOPPED-VJP-STATES`.

This phase must also decide, plainly and explicitly, whether stopped-key helper
rows remain current veto because they compute partial derivatives rather than
the total score route.

## Entry Conditions Inherited From Previous Phase

- Phase 2 fixed process-noise tensorization.
- Phase 3 fixed RK4 loop hygiene.
- Phase 4 fixed live manual forward/reverse time scans.
- Static audit still reports `FAIL_CURRENT_ROUTE` due only to Sinkhorn findings.

## Required Artifacts

- Implementation changes scoped to:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- Test updates scoped to:
  `tests/test_audit_ledh_clean_xla.py` or a focused Sinkhorn test module.
- Updated static audit artifact:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-static-audit-2026-07-02.json`
- Phase 5 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-streaming-sinkhorn-loop-hygiene-result-2026-07-02.md`
- Draft Phase 6 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase6-compiler-metrics-gate-subplan-2026-07-02.md`
- Updated execution ledger and Claude review ledger.

## Required Checks, Tests, Reviews

Before implementation:

- Codex skeptical audit of this subplan.
- Claude read-only review of the Phase 4 result and this Phase 5 subplan.

After implementation:

- `CUDA_VISIBLE_DEVICES=-1 python scripts/audit_ledh_clean_xla.py --format json --output docs/plans/bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase5-static-audit-2026-07-02.json`
- Focused Sinkhorn value parity for stopped-key and total-value helper loops
  against pre-refactor Python-loop references or frozen fixtures.
- Focused stopped-key VJP parity against the pre-refactor Python-state-list VJP
  reference or frozen fixture.
- Focused total-VJP parity for
  `_filterflow_streaming_finite_sinkhorn_potentials_total_vjp` against the
  pre-refactor Python-loop reference or frozen fixture.
- Existing manual/regional/audit tests used in Phase 4.
- Claude read-only review of the Phase 5 result before Phase 6 execution.

GPU/XLA runtime and HLO checks are deferred to Phase 6.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can streaming finite Sinkhorn iterations and stopped-key VJP state storage be represented with TensorFlow loop state without changing the current finite helper outputs on focused fixtures? |
| Baseline/comparator | Pre-Phase-5 helper semantics, preserved by test-local reference helpers or frozen fixtures. |
| Primary pass criterion | Target Python-loop/state-list Sinkhorn audit rows are absent/clean; focused value, stopped-key VJP, and total-VJP parity pass; stopped-key partial-derivative rows are explicitly classified and not called scores. |
| Veto diagnostics | Value, stopped-key VJP, or total-VJP parity fails; any Python step-iteration or Python state-accumulation construct remains in targeted helper symbols, including but not limited to `range(steps)`, `states = []`, or `states.append(...)`; stopped-key partial derivative is called a score; Phase 5 changes manual time scan or RK4 logic; audit loses coverage of stopped-key derivative warnings without explanation. |
| Explanatory diagnostics | Updated audit counts, value/VJP max absolute differences, remaining stopped-key classification, and source line anchors. |
| Not concluded | No HLO evidence, no GPU runtime evidence, no FD ladder rerun, no production HMC readiness. |
| Artifact | Phase 5 result markdown and Phase 5 static audit JSON. |

## Implementation Details

Target helpers in
`experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`:

- `_filterflow_streaming_finite_sinkhorn_potentials_stopped_scale_keys`;
- `_filterflow_streaming_finite_sinkhorn_potentials_total_vjp`;
- `_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys`.

Replace Python `for _ in range(steps)` with `tf.while_loop`. Replace stopped-key
VJP `states = []` / `states.append(...)` with `TensorArray` or equivalent
TensorFlow loop state. The real rule is semantic: no Python loop may perform
Sinkhorn step iteration, and no Python container may accumulate per-step
TensorFlow state inside the targeted helper symbols. The named token checks are
examples and static-audit anchors, not the full standard.

Do not change:

- manual P8p SIR route logic;
- RK4 helper logic;
- finite Sinkhorn equations;
- derivative target definitions.

Stopped-key helpers may remain partial-derivative helpers, but the result must
say plainly that they are not scores unless the missing total terms are
included elsewhere and verified.

## Forbidden Claims And Actions

- Do not claim clean XLA after Phase 5 unless all static current-veto rows are
  absent/clean and Claude review agrees that only compiler metrics remain.
- Do not call stopped partial derivatives scores.
- Do not edit manual route time scan or RK4 logic.
- Do not change finite-difference tolerances, score definitions, or gradient
  acceptance rules.
- Do not run long GPU jobs or HLO metrics in Phase 5.

## Exact Next-Phase Handoff Conditions

Phase 5 may hand off to Phase 6 only if:

- targeted Sinkhorn Python loops/state lists use TensorFlow loop state;
- focused Sinkhorn value, stopped-key VJP, and total-VJP parity pass;
- static audit status and remaining warnings are plainly recorded;
- Phase 5 result and Phase 6 subplan exist;
- Claude read-only review returns `VERDICT: AGREE`, or fixable findings are
  patched and rereviewed.

## Stop Conditions

Stop and write a blocker result if:

- focused Sinkhorn parity fails;
- focused total-VJP parity fails;
- TensorFlow loop state cannot preserve current helper outputs;
- changes spill into unrelated route logic;
- tests require GPU, network, package installation, or unrelated file changes;
- Claude and Codex do not converge after five rounds.

## Skeptical Pre-Execution Audit

Result: `PASS_PENDING_CLAUDE_REVIEW`

- Wrong baseline: avoided by requiring pre-Phase-5 helper semantics as
  comparator.
- Proxy promotion: avoided because Phase 5 is still local helper parity, not
  HLO/GPU evidence.
- Missing stop conditions: explicit above.
- Unfair comparison: parity must use same helper inputs and finite steps.
- Hidden assumption: stopped-key helpers remain partial derivatives unless
  total terms are included and verified.
- Environment mismatch: CPU-hidden local parity checks only; GPU evidence is
  deferred.
- Artifact mismatch: Phase 5 result must include updated audit JSON and
  Sinkhorn parity evidence.
